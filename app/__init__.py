from datetime import timedelta
from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Protección CSRF
csrf = CSRFProtect()
csrf.init_app(app)

# Clave secreta
app.secret_key = b'_5#y2L"F6Q7z\n\xec]/'

# Tiempo de sesión: 15 minutos
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# Importar y registrar blueprint
from app.rutas.seguridad.login_routes import logmod
app.register_blueprint(logmod)

# Redirigir '/' a '/login'
@app.route('/')
def raiz():
    return redirect(url_for('login.login'))

# importar referenciales
from app.rutas.modulos.modulo_agendamiento.ref.ciudad.ciudad_routes import ciumod
from app.rutas.modulos.modulo_agendamiento.ref.pais.pais_routes import paismod
from app.rutas.modulos.modulo_agendamiento.ref.nacionalidad.nacionalidad_routes import naciomod
from app.rutas.modulos.modulo_ventas.ref.apertura.apertura_routes import apermod
from app.rutas.modulos.modulo_agendamiento.ref.estado_civil.estado_civil_routes import estmod
from app.rutas.modulos.modulo_agendamiento.ref.genero.genero_routes import genmod
from app.rutas.modulos.modulo_agendamiento.ref.turno.turno_routes import turmod
#Gestionar Personas
from app.rutas.gestionar_personas.persona.persona_routes import persona_mod
from app.rutas.gestionar_personas.medico.medico_routes import medicomod
from app.rutas.gestionar_personas.paciente.paciente_routes import pacientemod
from app.rutas.seguridad.usuario.usuario_routes import usumod


from app.rutas.seguridad.grupo.grupo_routes import grumod
from app.rutas.seguridad.modulo.modulo_routes import modmod
from app.rutas.seguridad.cargo.cargo_routes import carmod



#Modulo Agendamiento REF

from app.rutas.modulos.modulo_agendamiento.ref.dia.dia_routes import diamod
from app.rutas.modulos.modulo_agendamiento.ref.sala_atencion.sala_atencion_routes import salmod
from app.rutas.modulos.modulo_agendamiento.ref.especialidad.especialidad_routes import espmod
from app.rutas.modulos.modulo_agendamiento.ref.estado_laboral.estado_laboral_routes import estado_laboralmod
from app.rutas.modulos.modulo_agendamiento.ref.hora.hora_routes import hormod
from app.rutas.modulos.modulo_agendamiento.ref.estado_cita.estado_cita_routes import estdmod
#Modulo Agendamiento MOV
from app.rutas.modulos.modulo_agendamiento.mov.agenda_medica.agenda_medica_routes import agendamedmod
from app.rutas.modulos.modulo_agendamiento.mov.cita.cita_routes import citamod
from app.rutas.modulos.modulo_agendamiento.mov.ficha.ficha_routes import fichamod


# from app.rutas.modulos.modulo_agendamiento.mov.aviso_recordatorio.recordatorio_routes import avisomod
# app.register_blueprint(avisomod)




# registrar referenciales
modulo0 = '/agendamiento'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
from app.rutas.modulos.modulo_agendamiento.ref.ciudad.ciudad_api import ciuapi

app.register_blueprint(paismod, url_prefix=f'{modulo0}/pais')
from app.rutas.modulos.modulo_agendamiento.ref.pais.pais_api import paiapi

app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')
from app.rutas.modulos.modulo_agendamiento.ref.nacionalidad.nacionalidad_api import nacioapi

app.register_blueprint(estmod, url_prefix=f'{modulo0}/estado_civil')
from app.rutas.modulos.modulo_agendamiento.ref.estado_civil.estado_civil_api import estapi

app.register_blueprint(genmod, url_prefix=f'{modulo0}/genero')
from app.rutas.modulos.modulo_agendamiento.ref.genero.genero_api import genapi

app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno')
from app.rutas.modulos.modulo_agendamiento.ref.turno.turno_api import turapi

app.register_blueprint(apermod, url_prefix=f'{modulo0}/apertura')





#Registrar Personas
modulo2 = '/gestionar-personas'
app.register_blueprint(persona_mod, url_prefix=f'{modulo2}/persona')
from app.rutas.gestionar_personas.persona.persona_api import personaapi

app.register_blueprint(medicomod, url_prefix=f'{modulo2}/medico')
from app.rutas.gestionar_personas.medico.medico_api import medicoapi

app.register_blueprint(pacientemod, url_prefix=f'{modulo2}/paciente')
from app.rutas.gestionar_personas.paciente.paciente_api import pacienteapi

app.register_blueprint(usumod, url_prefix=f'{modulo2}/usuario')
from app.rutas.seguridad.usuario.usuario_api import usuarioapi


app.register_blueprint(carmod, url_prefix=f'{modulo2}/cargo')
from app.rutas.seguridad.cargo.cargo_api import cargoapi

app.register_blueprint(modmod, url_prefix=f'{modulo2}/modulo')
from app.rutas.seguridad.modulo.modulo_api import moduloapi

app.register_blueprint(grumod, url_prefix=f'{modulo2}/grupo')
from app.rutas.seguridad.grupo.grupo_api import grupoapi




#Registrar modulo agendamiendo REF
modulo3 = '/modulos'

app.register_blueprint(diamod, url_prefix=f'{modulo0}/dia')
from app.rutas.modulos.modulo_agendamiento.ref.dia.dia_api import diaapi

app.register_blueprint(salmod, url_prefix=f'{modulo3}/sala_atencion')
from app.rutas.modulos.modulo_agendamiento.ref.sala_atencion.sala_atencion_api import salapi

app.register_blueprint(espmod, url_prefix=f'{modulo3}/especialidad')
from app.rutas.modulos.modulo_agendamiento.ref.especialidad.especialidad_api import espapi

app.register_blueprint(estado_laboralmod, url_prefix=f'{modulo3}/estado_laboral')
from app.rutas.modulos.modulo_agendamiento.ref.estado_laboral.estado_laboral_api import estado_laboralapi

app.register_blueprint(estdmod, url_prefix=f'{modulo3}/estado_cita')
from app.rutas.modulos.modulo_agendamiento.ref.estado_cita.estado_cita_api import estadoapi

app.register_blueprint(hormod, url_prefix=f'{modulo3}/hora')
from app.rutas.modulos.modulo_agendamiento.ref.hora.hora_api import horapi


#Registrar modulo agendamiendo MOV
app.register_blueprint(agendamedmod, url_prefix=f'{modulo3}/agenda_medica')
from app.rutas.modulos.modulo_agendamiento.mov.agenda_medica.agenda_medica_api import agenda_medica_api

app.register_blueprint(citamod, url_prefix=f'{modulo3}/cita')
from app.rutas.modulos.modulo_agendamiento.mov.cita.cita_api import cita_api

app.register_blueprint(fichamod, url_prefix=f'{modulo3}/ficha')
from app.rutas.modulos.modulo_agendamiento.mov.ficha.ficha_api import fichaapi






apiversion1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=apiversion1)

app.register_blueprint(paiapi, url_prefix=apiversion1)

app.register_blueprint(nacioapi, url_prefix=apiversion1)



app.register_blueprint(personaapi, url_prefix=apiversion1)

app.register_blueprint(medicoapi,url_prefix=apiversion1)

app.register_blueprint(pacienteapi, url_prefix=apiversion1)

app.register_blueprint(genapi, url_prefix=apiversion1)

app.register_blueprint(estapi, url_prefix=apiversion1)

app.register_blueprint(usuarioapi, url_prefix=apiversion1)

app.register_blueprint(agenda_medica_api, url_prefix=apiversion1)



app.register_blueprint(moduloapi, url_prefix=apiversion1)
app.register_blueprint(cargoapi, url_prefix=apiversion1)
app.register_blueprint(grupoapi, url_prefix=apiversion1)



app.register_blueprint(turapi, url_prefix=apiversion1)
app.register_blueprint(diaapi, url_prefix=apiversion1)
app.register_blueprint(salapi, url_prefix=apiversion1)
app.register_blueprint(espapi, url_prefix=apiversion1)
app.register_blueprint(estado_laboralapi, url_prefix=apiversion1)

app.register_blueprint(cita_api, url_prefix=apiversion1)
app.register_blueprint(estadoapi, url_prefix=apiversion1)
app.register_blueprint(horapi, url_prefix=apiversion1)
app.register_blueprint(fichaapi, url_prefix=apiversion1)








from app.rutas.modulos.modulo_agendamiento.vista.agendamiento_vista_routes import bp_agendamiento_vista
app.register_blueprint(bp_agendamiento_vista)


from app.rutas.modulos.modulo_consultorio.vista.consultorio_vista_routes import bp_consultorio_vista
from app.rutas.modulos.modulo_ventas.vista.ventas_vista_routes import bp_ventas_vista

app.register_blueprint(bp_consultorio_vista)
app.register_blueprint(bp_ventas_vista)



from app.rutas.modulos.modulo_reportes.vista.reporte_vista_routes import bp_reporte_vista
app.register_blueprint(bp_reporte_vista)








from flask import render_template, request, redirect, url_for

@app.route('/buscar', methods=['GET'])
def buscar():
    # Obtener el término de búsqueda del formulario
    termino = request.args.get('termino').lower()

    # Definir las rutas posibles
    rutas = {
    'ciudad': 'ciudad.ciudadIndex',
    'ciudades': 'ciudad.ciudadIndex',
    'pais': 'pais.paisIndex',
    'paises': 'pais.paisIndex',
    'nacionalidad': 'nacionalidad.nacionalidadIndex',
    'nacionalidades': 'nacionalidad.nacionalidadIndex',
    'estado civil': 'estadocivil.estadocivilIndex',
    'estados civiles': 'estadocivil.estadocivilIndex',
    'persona': 'persona.personaIndex',
    'personas': 'persona.personaIndex',
    'paciente': 'paciente.pacienteIndex',
    'medico': 'medico.medicoIndex',
    'cita': 'estadocita.estadocitaIndex',
    'citas': 'estadocita.estadocitaIndex',
    'especialidad': 'especialidad.especialidadIndex',
    'especialidades': 'especialidad.especialidadIndex',
    'dia': 'dia.diaIndex',
    'dias': 'dia.diaIndex',
    'turno': 'turno.turnoIndex',
    'turnos': 'turno.turnoIndex'
}


    # Verificar si el término coincide con alguna clave en rutas
    if termino in rutas:
        # Redirigir a la página correspondiente
        return redirect(url_for(rutas[termino]))
    else:
        # Renderizar una página con un mensaje de "no encontrado"
        return render_template('no_encontrado.html', termino=termino)
    