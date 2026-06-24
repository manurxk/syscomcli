from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.config.settings import init_settings
from app.middleware import init_middleware
from app.auth import login_blueprint
from app.rutas.mantenimiento.personas.funcionario.funcionario_routes import funcionariomod
from app.rutas.mantenimiento.personas.funcionario.funcionario_api import funcionarioapi
from app.rutas.mantenimiento.personas.paciente.paciente_routes import pacientemod
from app.rutas.mantenimiento.personas.paciente.paciente_api import pacienteapi
from app.rutas.mantenimiento.usuario.usuario_routes import usuariomod
from app.rutas.mantenimiento.usuario.usuario_api import usuarioapi
from app.rutas.mantenimiento.referenciales.referenciales_api import referencialesapi
from app.rutas.mantenimiento.referenciales.referenciales_routes import referencialesmod
from app.rutas.mantenimiento.referenciales.cargo.cargo_routes import cargomod
from app.rutas.mantenimiento.referenciales.cargo.cargo_api import cargoapi
from app.rutas.mantenimiento.referenciales.especialidad.especialidad_routes import especialidadmod
from app.rutas.mantenimiento.referenciales.especialidad.especialidad_api import especialidadapi
from app.rutas.mantenimiento.referenciales.empresa.empresa_routes import empresamod
from app.rutas.mantenimiento.referenciales.empresa.empresa_api import empresaapi
from app.rutas.mantenimiento.referenciales.sede.sede_routes import sedemod
from app.rutas.mantenimiento.referenciales.sede.sede_api import sedeapi
from app.rutas.mantenimiento.referenciales.consultorio.consultorio_routes import consultoriomod
from app.rutas.mantenimiento.referenciales.consultorio.consultorio_api import consultorioapi
from app.rutas.agendamiento.agenda_horarios.agenda_horarios_routes import agendahorariosmod
from app.rutas.agendamiento.agenda_horarios.agenda_horarios_api import agendahorariosapi
from app.rutas.agendamiento.cita.cita_routes import citamod
from app.rutas.agendamiento.cita.cita_api import citaapi
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
app.register_blueprint(pacientemod, url_prefix='/mantenimiento/paciente')
app.register_blueprint(pacienteapi, url_prefix='/api/v1')
app.register_blueprint(usuariomod, url_prefix='/mantenimiento/usuario')
app.register_blueprint(usuarioapi, url_prefix='/api/v1')
app.register_blueprint(referencialesapi, url_prefix='/api/v1')
app.register_blueprint(referencialesmod, url_prefix='/mantenimiento/referenciales')
app.register_blueprint(cargomod, url_prefix='/mantenimiento/referenciales/cargo')
app.register_blueprint(cargoapi, url_prefix='/api/v1')
app.register_blueprint(especialidadmod, url_prefix='/mantenimiento/referenciales/especialidad')
app.register_blueprint(especialidadapi, url_prefix='/api/v1')
app.register_blueprint(empresamod, url_prefix='/mantenimiento/referenciales/empresa')
app.register_blueprint(empresaapi, url_prefix='/api/v1')
app.register_blueprint(sedemod, url_prefix='/mantenimiento/referenciales/sede')
app.register_blueprint(sedeapi, url_prefix='/api/v1')
app.register_blueprint(consultoriomod, url_prefix='/mantenimiento/referenciales/consultorio')
app.register_blueprint(consultorioapi, url_prefix='/api/v1')
app.register_blueprint(agendahorariosmod, url_prefix='/agendamiento/agenda-horarios')
app.register_blueprint(agendahorariosapi, url_prefix='/api/v1')
app.register_blueprint(citamod, url_prefix='/agendamiento/citas')
app.register_blueprint(citaapi, url_prefix='/api/v1')

# Context processors y helpers de template
init_context_processors(app)
registrar_funciones_template(app)

# TODO (post fase ventas): restaurar el scheduler de presupuestos cuando
# PresupuestoDao se migre a la estructura nueva.