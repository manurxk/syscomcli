# /app/services/EmailService.py
"""
Servicio de envío de correo electrónico (MFA por email, y futuros usos)

Requiere configuración en variables de entorno:
- SMTP_HOST: host del servidor SMTP
- SMTP_PORT: puerto SMTP (default 587)
- SMTP_USER / SMTP_PASSWORD: credenciales
- SMTP_FROM: remitente (default = SMTP_USER)

Mientras SMTP_HOST no esté configurado, el servicio funciona en modo
"log-only": no bloquea el flujo de MFA, pero tampoco envía correo real.
Este fallback debe retirarse antes de producción (ver auditoría de código).
"""
import smtplib
import ssl
from email.message import EmailMessage
from enum import Enum
from flask import current_app as app


class TipoError(Enum):
    TEMPORAL = "temporal"
    PERMANENTE = "permanente"
    CONFIGURACION = "configuracion"
    DESCONOCIDO = "desconocido"


class EmailService:
    def __init__(self):
        self.smtp_host = app.config.get('SMTP_HOST')
        self.smtp_port = int(app.config.get('SMTP_PORT', 587))
        self.smtp_user = app.config.get('SMTP_USER')
        self.smtp_password = app.config.get('SMTP_PASSWORD')
        self.smtp_from = app.config.get('SMTP_FROM') or self.smtp_user

        self.client_available = bool(self.smtp_host and self.smtp_user and self.smtp_password)

        if not self.client_available:
            app.logger.warning(
                "Configuración SMTP incompleta. EmailService funcionará en modo log-only "
                "(el código MFA se escribe en el log en vez de enviarse por correo real)."
            )

    def enviar_codigo_mfa(self, correo_destino, codigo, minutos_validez):
        """
        Envía el código de verificación MFA por correo.

        Returns:
            tuple: (success: bool, error: str, tipo_error: TipoError)
        """
        if not correo_destino:
            return (False, "El usuario no tiene un correo registrado.", TipoError.PERMANENTE)

        asunto = f"{app.config.get('NOMBRE_CLINICA', 'Sysclin')} - Código de verificación"
        cuerpo = (
            f"Su código de verificación es: {codigo}\n\n"
            f"Este código vence en {minutos_validez} minutos. "
            f"Si usted no solicitó este código, ignore este mensaje."
        )

        if not self.client_available:
            # Fallback de desarrollo: no bloquea el flujo mientras no haya credenciales SMTP reales.
            app.logger.warning(f"MFA_EMAIL_LOG_ONLY destino={correo_destino} codigo={codigo}")
            return (True, None, None)

        try:
            msg = EmailMessage()
            msg['Subject'] = asunto
            msg['From'] = self.smtp_from
            msg['To'] = correo_destino
            msg.set_content(cuerpo)

            contexto = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as servidor:
                servidor.starttls(context=contexto)
                servidor.login(self.smtp_user, self.smtp_password)
                servidor.send_message(msg)

            app.logger.info(f"MFA_EMAIL_SENT destino={correo_destino}")
            return (True, None, None)

        except smtplib.SMTPAuthenticationError as e:
            app.logger.error(f"Error de autenticación SMTP: {e}")
            return (False, "Error de configuración del servidor de correo.", TipoError.CONFIGURACION)
        except (smtplib.SMTPException, OSError) as e:
            app.logger.error(f"Error temporal enviando correo MFA: {e}")
            return (False, "No se pudo enviar el correo, intente nuevamente.", TipoError.TEMPORAL)
        except Exception as e:
            app.logger.error(f"Error inesperado enviando correo MFA: {e}", exc_info=True)
            return (False, "Error inesperado al enviar el correo.", TipoError.DESCONOCIDO)
