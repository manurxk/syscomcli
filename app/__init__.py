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
from app.rutas.referenciales.pais.pais_routes import paismod
from app.rutas.referenciales.nacionalidad.nacionalidad_routes import naciomod
from app.rutas.referenciales.apertura.apertura_routes import apermod
from app.rutas.referenciales.estado_civil.estado_civil_routes import estmod
from app.rutas.referenciales.genero.genero_routes import genmod
from app.rutas.referenciales.turno.turno_routes import turmod
#Gestionar Personas
from app.rutas.gestionar_personas.persona.persona_routes import persona_mod
from app.rutas.gestionar_personas.medico.medico_routes import medicomod
from app.rutas.gestionar_personas.paciente.paciente_routes import pacientemod
from app.rutas.gestionar_personas.usuario.usuario_routes import usumod
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
# importar gestionar compras
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedidos_compras_routes  import pdcmod


# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
from app.rutas.modulos.modulo_agendamiento.ref.ciudad.ciudad_api import ciuapi

app.register_blueprint(paismod, url_prefix=f'{modulo0}/pais')
from app.rutas.referenciales.pais.pais_api import paiapi

app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')
from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacioapi

app.register_blueprint(estmod, url_prefix=f'{modulo0}/estado_civil')
from app.rutas.referenciales.estado_civil.estado_civil_api import estapi

app.register_blueprint(genmod, url_prefix=f'{modulo0}/genero')
from app.rutas.referenciales.genero.genero_api import genapi

app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno')
from app.rutas.referenciales.turno.turno_api import turnoapi



#Registrar Personas
modulo2 = '/gestionar-personas'
app.register_blueprint(persona_mod, url_prefix=f'{modulo2}/persona')
from app.rutas.gestionar_personas.persona.persona_api import personaapi

app.register_blueprint(medicomod, url_prefix=f'{modulo2}/medico')
from app.rutas.gestionar_personas.medico.medico_api import medicoapi

app.register_blueprint(pacientemod, url_prefix=f'{modulo2}/paciente')
from app.rutas.gestionar_personas.paciente.paciente_api import pacienteapi

app.register_blueprint(usumod, url_prefix=f'{modulo2}/usuario')
from app.rutas.gestionar_personas.usuario.usuario_api import usuarioapi



#Registrar modulo agendamiendo REF
modulo3 = '/modulos'

app.register_blueprint(diamod, url_prefix=f'{modulo0}/dia')
from app.rutas.referenciales.dia.dia_api import diaapi

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

# registro de modulos - gestionar compras
modulo10 = '/gestionar-compras'
app.register_blueprint(pdcmod, url_prefix=f'{modulo10}/registrar-pedido-compras')
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_api import pdcapi
from app.rutas.referenciales.sucursal.sucursal_api import sucapi





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




app.register_blueprint(turnoapi, url_prefix=apiversion1)
app.register_blueprint(diaapi, url_prefix=apiversion1)
app.register_blueprint(salapi, url_prefix=apiversion1)
app.register_blueprint(espapi, url_prefix=apiversion1)
app.register_blueprint(estado_laboralapi, url_prefix=apiversion1)

app.register_blueprint(cita_api, url_prefix=apiversion1)
app.register_blueprint(estadoapi, url_prefix=apiversion1)
app.register_blueprint(horapi, url_prefix=apiversion1)
app.register_blueprint(fichaapi, url_prefix=apiversion1)

# Gestionar compras API
apiversion1 = '/api/v1'
app.register_blueprint(pdcapi, url_prefix=f'{apiversion1}/{modulo10}/registrar-pedido-compras')
app.register_blueprint(sucapi, url_prefix=apiversion1)







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
    'ciudades': 'ciudad.ciudadIndex',  # Agregado
    'pais': 'pais.paisIndex',
    'paises': 'pais.paisIndex',  # Agregado
    'nacionalidad': 'nacionalidad.nacionalidadIndex',
    'nacionalidades': 'nacionalidad.nacionalidadIndex',  # Agregado
    'ocupacion': 'ocupacion.ocupacionIndex',
    'ocupaciones': 'ocupacion.ocupacionIndex',  # Agregado
    'estado civil': 'estadocivil.estadocivilIndex',
    'estados civiles': 'estadocivil.estadocivilIndex',  # Agregado
    'sexo': 'sexo.sexoIndex',
    'sexos': 'sexo.sexoIndex',  # Agregado
    'persona': 'persona.personaIndex',
    'personas': 'persona.personaIndex',  # Agregado
    'paciente': 'paciente.pacienteIndex',
    'medico': 'medico.medicoIndex',
    'cita': 'estadocita.estadocitaIndex',
    'citas': 'estadocita.estadocitaIndex',  # Agregado
    'especialidad': 'especialidad.especialidadIndex',
    'especialidades': 'especialidad.especialidadIndex',  # Agregado
    'dias': 'dia.diaIndex',
    'dia': 'dia.diaIndex',  # Agregado
    'diagnostico': 'diagnostico.diagnosticoIndex',
    'diagnosticos': 'diagnostico.diagnosticoIndex',  # Agregado
    'duracion consulta': 'duracionconsulta.duracionconsultaIndex',
    'duraciones consulta': 'duracionconsulta.duracionconsultaIndex',  # Agregado
    'turno': 'turno.turnoIndex',
    'turnos': 'turno.turnoIndex',  # Agregado
    'test utilizados': 'instrumento.instrumentoIndex',
    'tests utilizados': 'instrumento.instrumentoIndex',  # Agregado
    'tratamientos': 'tratamiento.tratamientoIndex',
    'tratamiento': 'tratamiento.tratamientoIndex'  # Agregado
    }

    # Verificar si el término coincide con alguna clave en rutas
    if termino in rutas:
        # Redirigir a la página correspondiente
        return redirect(url_for(rutas[termino]))
    else:
        # Renderizar una página con un mensaje de "no encontrado"
        return render_template('no_encontrado.html', termino=termino)
    