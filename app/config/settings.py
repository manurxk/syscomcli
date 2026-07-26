import os
from datetime import timedelta

def init_settings(app):
    """Initialize application settings and configuration."""
    app.secret_key = b'***REMOVED***'
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

    # WhatsApp Notifications (Ultramsg)
    app.config['ULTRAMSG_INSTANCE_ID'] = os.getenv('ULTRAMSG_INSTANCE_ID', '***REMOVED***')
    app.config['ULTRAMSG_TOKEN'] = os.getenv('ULTRAMSG_TOKEN', '***REMOVED***')
    app.config['ULTRAMSG_API_URL'] = os.getenv('ULTRAMSG_API_URL', 'https://api.ultramsg.com')

    # General configuration
    app.config['NOMBRE_CLINICA'] = os.getenv('NOMBRE_CLINICA', 'Sysclin')

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
