import os
from datetime import timedelta

SECRET_KEY_LARGO_MINIMO = 32


def init_settings(app):
    """Initialize application settings and configuration."""
    # SECRET_KEY obligatoria: sin respaldo aleatorio (cada reinicio invalidaria las sesiones)
    secret_key = os.getenv('SECRET_KEY', '')
    if len(secret_key) < SECRET_KEY_LARGO_MINIMO:
        raise RuntimeError(
            f"SECRET_KEY ausente o con menos de {SECRET_KEY_LARGO_MINIMO} caracteres en .env. "
            "Generar una con: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    app.secret_key = secret_key
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

    # Cookie de sesion: Secure solo con HTTPS (1 en el servidor; 0 en local para que el puerto 5005 por HTTP siga funcionando)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', '0') == '1'

    # WhatsApp Notifications (Ultramsg)
    app.config['ULTRAMSG_INSTANCE_ID'] = os.getenv('ULTRAMSG_INSTANCE_ID')
    app.config['ULTRAMSG_TOKEN'] = os.getenv('ULTRAMSG_TOKEN')
    app.config['ULTRAMSG_API_URL'] = os.getenv('ULTRAMSG_API_URL', 'https://api.ultramsg.com')

    # General configuration
    app.config['NOMBRE_CLINICA'] = os.getenv('NOMBRE_CLINICA', 'SYSCLIN')

    # MFA por correo (EmailService) - sin credenciales reales aun: log-only
    app.config['SMTP_HOST'] = os.getenv('SMTP_HOST')
    app.config['SMTP_PORT'] = os.getenv('SMTP_PORT', '587')
    app.config['SMTP_USER'] = os.getenv('SMTP_USER')
    app.config['SMTP_PASSWORD'] = os.getenv('SMTP_PASSWORD')
    app.config['SMTP_FROM'] = os.getenv('SMTP_FROM')
    app.config['MFA_CODE_TTL_MINUTES'] = int(os.getenv('MFA_CODE_TTL_MINUTES', '5'))

    # Path prefixes
    app.config['MODULO_REFERENCIALES'] = "/referenciales"
    app.config['MODULO_GESTION'] = "/modulos"
    app.config['API_V1'] = "/api/v1"
