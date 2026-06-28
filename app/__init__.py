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
from app.rutas.mantenimiento.referenciales.empresa.empresa_routes import empresamod
from app.rutas.mantenimiento.referenciales.empresa.empresa_api import empresaapi
from app.rutas.mantenimiento.referenciales.sede.sede_routes import sedemod
from app.rutas.mantenimiento.referenciales.sede.sede_api import sedeapi
from app.rutas.mantenimiento.referenciales.consultorio.consultorio_routes import consultoriomod
from app.rutas.mantenimiento.referenciales.consultorio.consultorio_api import consultorioapi
from app.rutas.agendamiento.referenciales.especialidad.especialidad_routes import especialidadmod
from app.rutas.agendamiento.referenciales.especialidad.especialidad_api import especialidadapi
from app.rutas.agendamiento.agenda_horarios.agenda_horarios_routes import agendahorariosmod
from app.rutas.agendamiento.agenda_horarios.agenda_horarios_api import agendahorariosapi
from app.rutas.agendamiento.cita.cita_routes import citamod
from app.rutas.agendamiento.cita.cita_api import citaapi
from app.rutas.agendamiento.lista_espera.lista_espera_routes import listaesperamod
from app.rutas.agendamiento.lista_espera.lista_espera_api import listaesperaapi
from app.rutas.clinico.referenciales.signo.signo_routes import signomod
from app.rutas.clinico.referenciales.signo.signo_api import signoapi
from app.rutas.clinico.referenciales.sintoma.sintoma_routes import sintomamod
from app.rutas.clinico.referenciales.sintoma.sintoma_api import sintomaapi
from app.rutas.clinico.referenciales.diagnostico.diagnostico_routes import diagnosticomod
from app.rutas.clinico.referenciales.diagnostico.diagnostico_api import diagnosticoapi
from app.rutas.clinico.referenciales.medicamento.medicamento_routes import medicamentomod
from app.rutas.clinico.referenciales.medicamento.medicamento_api import medicamentoapi
from app.rutas.clinico.referenciales.tipo_analisis.tipo_analisis_routes import tipo_analisismod
from app.rutas.clinico.referenciales.tipo_analisis.tipo_analisis_api import tipoanalisisapi
from app.rutas.clinico.referenciales.tipo_estudio.tipo_estudio_routes import tipo_estudiomod
from app.rutas.clinico.referenciales.tipo_estudio.tipo_estudio_api import tipoestudioapi
from app.rutas.clinico.referenciales.tipo_procedimiento.tipo_procedimiento_routes import tipo_procedimientomod
from app.rutas.clinico.referenciales.tipo_procedimiento.tipo_procedimiento_api import tipoprocedimientoapi
from app.rutas.clinico.referenciales.tipo_tratamiento.tipo_tratamiento_routes import tipo_tratamientomod
from app.rutas.clinico.referenciales.tipo_tratamiento.tipo_tratamiento_api import tipotratamientoapi
from app.rutas.clinico.referenciales.tipo_certificado_medico.tipo_certificado_medico_routes import tipo_certificado_medicomod
from app.rutas.clinico.referenciales.tipo_certificado_medico.tipo_certificado_medico_api import tipocertificadomedicoapi
from app.rutas.clinico.referenciales.instrumento.instrumento_routes import instrumentomod
from app.rutas.clinico.referenciales.instrumento.instrumento_api import instrumentoapi
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
app.register_blueprint(empresamod, url_prefix='/mantenimiento/referenciales/empresa')
app.register_blueprint(empresaapi, url_prefix='/api/v1')
app.register_blueprint(sedemod, url_prefix='/mantenimiento/referenciales/sede')
app.register_blueprint(sedeapi, url_prefix='/api/v1')
app.register_blueprint(consultoriomod, url_prefix='/mantenimiento/referenciales/consultorio')
app.register_blueprint(consultorioapi, url_prefix='/api/v1')
app.register_blueprint(especialidadmod, url_prefix='/agendamiento/referenciales/especialidad')
app.register_blueprint(especialidadapi, url_prefix='/api/v1')
app.register_blueprint(agendahorariosmod, url_prefix='/agendamiento/agenda-horarios')
app.register_blueprint(agendahorariosapi, url_prefix='/api/v1')
app.register_blueprint(citamod, url_prefix='/agendamiento/citas')
app.register_blueprint(citaapi, url_prefix='/api/v1')
app.register_blueprint(listaesperamod, url_prefix='/agendamiento/lista-espera')
app.register_blueprint(listaesperaapi, url_prefix='/api/v1')
app.register_blueprint(signomod, url_prefix='/clinico/referenciales/signo')
app.register_blueprint(signoapi, url_prefix='/api/v1')
app.register_blueprint(sintomamod, url_prefix='/clinico/referenciales/sintoma')
app.register_blueprint(sintomaapi, url_prefix='/api/v1')
app.register_blueprint(diagnosticomod, url_prefix='/clinico/referenciales/diagnostico')
app.register_blueprint(diagnosticoapi, url_prefix='/api/v1')
app.register_blueprint(medicamentomod, url_prefix='/clinico/referenciales/medicamento')
app.register_blueprint(medicamentoapi, url_prefix='/api/v1')
app.register_blueprint(tipo_analisismod, url_prefix='/clinico/referenciales/tipo-analisis')
app.register_blueprint(tipoanalisisapi, url_prefix='/api/v1')
app.register_blueprint(tipo_estudiomod, url_prefix='/clinico/referenciales/tipo-estudio')
app.register_blueprint(tipoestudioapi, url_prefix='/api/v1')
app.register_blueprint(tipo_procedimientomod, url_prefix='/clinico/referenciales/tipo-procedimiento')
app.register_blueprint(tipoprocedimientoapi, url_prefix='/api/v1')
app.register_blueprint(tipo_tratamientomod, url_prefix='/clinico/referenciales/tipo-tratamiento')
app.register_blueprint(tipotratamientoapi, url_prefix='/api/v1')
app.register_blueprint(tipo_certificado_medicomod, url_prefix='/clinico/referenciales/tipo-certificado-medico')
app.register_blueprint(tipocertificadomedicoapi, url_prefix='/api/v1')
app.register_blueprint(instrumentomod, url_prefix='/clinico/referenciales/instrumento')
app.register_blueprint(instrumentoapi, url_prefix='/api/v1')

# Context processors y helpers de template
init_context_processors(app)
registrar_funciones_template(app)

# TODO (post fase ventas): restaurar el scheduler de presupuestos cuando
# PresupuestoDao se migre a la estructura nueva.