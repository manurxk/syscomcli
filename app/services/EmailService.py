# /app/services/EmailService.py
"""
Servicio de envío de correo electrónico (MFA, recordatorios de cita, facturas)

Requiere configuración en variables de entorno:
- SMTP_HOST: host del servidor SMTP
- SMTP_PORT: puerto SMTP (default 587)
- SMTP_USER / SMTP_PASSWORD: credenciales
- SMTP_FROM: remitente (default = SMTP_USER)

Mientras SMTP_HOST no esté configurado, el servicio funciona en modo
"log-only": no bloquea el flujo de MFA, pero tampoco envía correo real.
Este fallback debe retirarse antes de producción (ver auditoría de código).
"""
import random
import smtplib
import ssl
import time
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
                "(los correos se escriben en el log en vez de enviarse realmente)."
            )

    def enviar_correo(self, destinatario, asunto, cuerpo_texto, cuerpo_html=None, adjuntos=None):
        """
        Envío genérico de correo, con soporte de adjuntos (ej. PDF de factura).

        Args:
            destinatario: correo del destinatario
            asunto: asunto del correo
            cuerpo_texto: cuerpo en texto plano
            cuerpo_html: cuerpo alternativo en HTML (opcional)
            adjuntos: lista de dicts {'nombre': str, 'contenido': bytes, 'mime': (tipo, subtipo)} (opcional)

        Returns:
            tuple: (success: bool, error: str, tipo_error: TipoError)
        """
        if not destinatario:
            return (False, "El destinatario no tiene un correo registrado.", TipoError.PERMANENTE)

        if not self.client_available:
            app.logger.warning(f"EMAIL_LOG_ONLY destino={destinatario} asunto={asunto}")
            return (True, None, None)

        try:
            msg = EmailMessage()
            msg['Subject'] = asunto
            msg['From'] = self.smtp_from
            msg['To'] = destinatario
            msg.set_content(cuerpo_texto)
            if cuerpo_html:
                msg.add_alternative(cuerpo_html, subtype='html')

            for adjunto in (adjuntos or []):
                maintype, subtype = adjunto.get('mime', ('application', 'octet-stream'))
                msg.add_attachment(
                    adjunto['contenido'],
                    maintype=maintype,
                    subtype=subtype,
                    filename=adjunto['nombre'],
                )

            contexto = ssl.create_default_context()
            intentos = 3
            for intento in range(1, intentos + 1):
                try:
                    with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as servidor:
                        servidor.starttls(context=contexto)
                        servidor.login(self.smtp_user, self.smtp_password)
                        servidor.send_message(msg)
                    app.logger.info(f"EMAIL_SENT destino={destinatario} asunto={asunto}")
                    return (True, None, None)
                except (smtplib.SMTPException, OSError) as e:
                    if intento == intentos:
                        raise
                    app.logger.warning(
                        f"Error temporal enviando correo (intento {intento}/{intentos}), reintentando: {e}"
                    )
                    time.sleep(2)

        except smtplib.SMTPAuthenticationError as e:
            app.logger.error(f"Error de autenticación SMTP: {e}")
            return (False, "Error de configuración del servidor de correo.", TipoError.CONFIGURACION)
        except (smtplib.SMTPException, OSError) as e:
            app.logger.error(f"Error temporal enviando correo: {e}")
            return (False, "No se pudo enviar el correo, intente nuevamente.", TipoError.TEMPORAL)
        except Exception as e:
            app.logger.error(f"Error inesperado enviando correo: {e}", exc_info=True)
            return (False, "Error inesperado al enviar el correo.", TipoError.DESCONOCIDO)

    def enviar_codigo_mfa(self, correo_destino, codigo, minutos_validez):
        """
        Envía el código de verificación MFA por correo.

        Returns:
            tuple: (success: bool, error: str, tipo_error: TipoError)
        """
        asunto = f"{app.config.get('NOMBRE_CLINICA', 'SYSCLIN')} - Código de verificación"
        cuerpo = (
            f"Su código de verificación es: {codigo}\n\n"
            f"Este código vence en {minutos_validez} minutos. "
            f"Si usted no solicitó este código, ignore este mensaje."
        )
        success, error, tipo_error = self.enviar_correo(correo_destino, asunto, cuerpo)
        if success and self.client_available:
            app.logger.info(f"MFA_EMAIL_SENT destino={correo_destino}")
        return (success, error, tipo_error)

    # ── Variación de plantilla (anti-spam) ──────────────────────────────────
    # Rotar entre varias redacciones evita que un proveedor de correo marque
    # como spam el envío masivo de mensajes idénticos.

    _SALUDOS = ["Hola {nombre},", "Estimado/a {nombre},", "Buen día {nombre},"]
    _CIERRES = ["¡Gracias!", "Saludos cordiales.", "Quedamos atentos ante cualquier consulta."]

    def _variar(self, lista):
        return random.choice(lista)

    def enviar_recordatorio_cita(self, correo_destino, nombre_paciente, cita_fecha, cita_hora,
                                  especialista, especialidad, motivo=None,
                                  nombre_clinica="SYSCLIN"):
        """
        Envía recordatorio de cita por correo, con variación de plantilla.

        Returns:
            tuple: (success: bool, error: str, tipo_error: TipoError)
        """
        saludo = self._variar(self._SALUDOS).format(nombre=nombre_paciente)
        cierre = self._variar(self._CIERRES)

        asunto = f"{nombre_clinica} - Recordatorio de su cita del {cita_fecha}"
        cuerpo = (
            f"{saludo}\n\n"
            f"Le recordamos su cita médica:\n"
            f"Fecha: {cita_fecha}\n"
            f"Hora: {cita_hora}\n"
            f"Profesional: {especialista}\n"
            f"Especialidad: {especialidad}\n"
        )
        if motivo:
            cuerpo += f"Motivo: {motivo}\n"
        cuerpo += f"\n{cierre}"

        return self.enviar_correo(correo_destino, asunto, cuerpo)

    def enviar_recuperacion_password(self, correo_destino, nombre_usuario, link_reseteo,
                                      horas_validez, nombre_clinica="SYSCLIN"):
        """
        Envía el enlace para restablecer la contraseña.

        Returns:
            tuple: (success: bool, error: str, tipo_error: TipoError)
        """
        saludo = self._variar(self._SALUDOS).format(nombre=nombre_usuario)
        cierre = self._variar(self._CIERRES)

        asunto = f"{nombre_clinica} - Recuperación de contraseña"
        cuerpo = (
            f"{saludo}\n\n"
            f"Solicitó restablecer su contraseña. Ingrese al siguiente enlace para elegir una nueva:\n"
            f"{link_reseteo}\n\n"
            f"Este enlace vence en {horas_validez} horas. "
            f"Si usted no solicitó esto, ignore este mensaje.\n\n"
            f"{cierre}"
        )
        return self.enviar_correo(correo_destino, asunto, cuerpo)

    def enviar_factura(self, correo_destino, numero_factura, nombre_cliente, monto_total,
                        pdf_bytes, nombre_clinica="SYSCLIN"):
        """
        Envía la factura (PDF) al cliente por correo.

        Returns:
            tuple: (success: bool, error: str, tipo_error: TipoError)
        """
        saludo = self._variar(self._SALUDOS).format(nombre=nombre_cliente)
        cierre = self._variar(self._CIERRES)

        asunto = f"{nombre_clinica} - Factura {numero_factura}"
        cuerpo = (
            f"{saludo}\n\n"
            f"Adjuntamos su factura {numero_factura} por un total de {monto_total}.\n\n"
            f"{cierre}"
        )
        adjuntos = [{
            'nombre': f"{numero_factura}.pdf",
            'contenido': pdf_bytes,
            'mime': ('application', 'pdf'),
        }]
        return self.enviar_correo(correo_destino, asunto, cuerpo, adjuntos=adjuntos)

    def enviar_orden_estudio(self, correo_destino, numero_orden, nombre_paciente, pdf_bytes, nombre_clinica="SYSCLIN"):
        """
        Envía la orden de estudios o análisis (PDF) al paciente por correo.

        Returns:
            tuple: (success: bool, error: str, tipo_error: TipoError)
        """
        saludo = self._variar(self._SALUDOS).format(nombre=nombre_paciente)
        cierre = self._variar(self._CIERRES)

        asunto = f"{nombre_clinica} - Orden de estudios {numero_orden}"
        cuerpo = (
            f"{saludo}\n\n"
            f"Adjuntamos su orden de estudios {numero_orden}, indicada en su consulta. "
            f"Preséntela en el laboratorio o centro donde se vaya a realizar los estudios.\n\n"
            f"{cierre}"
        )
        adjuntos = [{
            'nombre': f"orden_{numero_orden}.pdf",
            'contenido': pdf_bytes,
            'mime': ('application', 'pdf'),
        }]
        return self.enviar_correo(correo_destino, asunto, cuerpo, adjuntos=adjuntos)
