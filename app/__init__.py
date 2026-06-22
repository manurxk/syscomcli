from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.config.settings import init_settings
from app.middleware import init_middleware
from app.auth import login_blueprint
from app.rutas.mantenimiento.personas.funcionario.funcionario_routes import funcionariomod
from app.rutas.mantenimiento.personas.funcionario.funcionario_api import funcionarioapi
from app.context_processors import init_context_processors
from app.utils.template_helpers import registrar_funciones_template

# Initialize the Flask application
app = Flask(__name__)

# Initialize Extensions
csrf = CSRFProtect()
csrf.init_app(app)

# Load Settings and Configuration
init_settings(app)

# Initialize Middleware
init_middleware(app)

# Register Blueprints (Routes)
app.register_blueprint(login_blueprint)
app.register_blueprint(funcionariomod, url_prefix='/mantenimiento/funcionario')
app.register_blueprint(funcionarioapi, url_prefix='/api/v1')

# Context processors y helpers de template
init_context_processors(app)
registrar_funciones_template(app)

# TODO (post fase ventas): restaurar el scheduler de presupuestos cuando
# PresupuestoDao se migre a la estructura nueva.