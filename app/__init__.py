from flask import Flask
from flask_wtf.csrf import CSRFProtect
import atexit

from app.config.settings import init_settings
from app.middleware import init_middleware
from app.context_processors import init_context_processors
from app.blueprints import register_blueprints
from app.utils.template_helpers import registrar_funciones_template
from app.services.budget_automation_service import iniciar_scheduler, detener_scheduler

# Initialize the Flask application
app = Flask(__name__)

# Initialize Extensions
csrf = CSRFProtect()
csrf.init_app(app)

# Load Settings and Configuration
init_settings(app)

# Initialize Middleware
init_middleware(app)

# Initialize Context Processors (Template globals)
init_context_processors(app)

# Register Blueprints (Routes)
register_blueprints(app)

# Register Template Helper Functions (Must be at the end)
registrar_funciones_template(app)

# Iniciar scheduler de automatización de presupuestos (vencimientos diarios)
iniciar_scheduler(app)
atexit.register(detener_scheduler)