from flask import Flask
from flask import render_template


app = Flask(__name__)

# importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod #ciudad
from app.rutas.referenciales.paises.pais_routes import paimod   #pais
from app.rutas.referenciales.nacionalidad.nacionalidad_routes import naciomod  #nacionalidad
from app.rutas.referenciales.ocupacion.ocupacion_routes import ocupmod  #ocupacion
from app.rutas.referenciales.estado_civil.estado_civil_routes import estacivmod  #estado civil
from app.rutas.referenciales.estado_cita.estado_cita_routes import estacitmod  #estado de la cita
from app.rutas.referenciales.persona.persona_routes import persmod  #persona
from app.rutas.referenciales.especialidad.especialidad_routes import especimod  #especialidad
from app.rutas.referenciales.dia.dia_routes import diamod  #dia
from app.rutas.referenciales.duracion_consulta.duracion_consulta_routes import duraconsumod  #duracion de la consulta
from app.rutas.referenciales.instrumento.instrumento_routes import instmod  #instrumento utilizado
from app.rutas.referenciales.turno.turno_routes import turmod  #turno
from app.rutas.referenciales.tratamiento.tratamiento_routes import tratmod  #tratamiento
from app.rutas.referenciales.diagnostico.diagnostico_routes import diagmod  #diagnostico

# Importar rutas de inicio
from app.rutas.login.login_routes import loginmod
from app.rutas.login.vista_routes import vistamod

#importacion de Administrativa
from app.rutas.administracion.agenda.agenda_routes import agemod   # Agendamiento
from app.rutas.administracion.cita.cita_routes import citamod   # Cita
from app.rutas.administracion.paciente.paciente_routes import paciemod
from app.rutas.administracion.medico.medico_routes import medimod
from app.rutas.administracion.vistaAGENDAR.vistaAGENDAR_routes import vistagendamod
from app.rutas.administracion.consulta.consulta_routes import consumod



from app.rutas.administracion.medico.medico_routes import medimod




# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(loginmod, url_prefix=f'{modulo0}/login') 
app.register_blueprint(vistamod, url_prefix=f'{modulo0}/login') 
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad') #ciudad
app.register_blueprint(paimod, url_prefix=f'{modulo0}/paises') #pais
app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')  #nacionalidad
app.register_blueprint(ocupmod, url_prefix=f'{modulo0}/ocupacion')  #ocupacion
app.register_blueprint(estacivmod, url_prefix=f'{modulo0}/estadocivil')  #estado civil
app.register_blueprint(estacitmod, url_prefix=f'{modulo0}/estadocita')  #estado de la cita
app.register_blueprint(persmod, url_prefix=f'{modulo0}/persona') #persona
app.register_blueprint(especimod, url_prefix=f'{modulo0}/especialidad') #especialidad
app.register_blueprint(diamod, url_prefix=f'{modulo0}/dia') #dia
app.register_blueprint(duraconsumod, url_prefix=f'{modulo0}/duracionconsulta') #duracion de la consulta
app.register_blueprint(instmod, url_prefix=f'{modulo0}/instrumento') #instrumento utilizado
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno') #turno
app.register_blueprint(tratmod, url_prefix=f'{modulo0}/tratamiento') #tratamiento
app.register_blueprint(diagmod, url_prefix=f'{modulo0}/diagnostico') #diagnostico

# registrar agendamientos
modulo0 = '/administracion'
app.register_blueprint(agemod, url_prefix=f'{modulo0}/cita')  # cita
app.register_blueprint(citamod, url_prefix=f'{modulo0}/cita')  # cita
app.register_blueprint(paciemod, url_prefix=f'{modulo0}/cita')  # cita
app.register_blueprint(medimod, url_prefix=f'{modulo0}/cita')  # cita
app.register_blueprint(vistagendamod, url_prefix=f'{modulo0}/cita')  # cita
app.register_blueprint(consumod, url_prefix=f'{modulo0}/cita')  # cita








#ciudad
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
#pais
from app.rutas.referenciales.paises.pais_api import paisapi
#nacionalidad
from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacioapi
#nacionalidad
from app.rutas.referenciales.ocupacion.ocupacion_api import ocupapi
#estado civil
from app.rutas.referenciales.estado_civil.estado_civil_api import estacivapi
#estado de la cita
from app.rutas.referenciales.estado_cita.estado_cita_api import estacitapi
#persona
from app.rutas.referenciales.persona.persona_api import persapi
#especialidad
from app.rutas.referenciales.especialidad.especialidad_api import especiapi
#dia
from app.rutas.referenciales.dia.dia_api import diaapi
#duracion de la consulta
from app.rutas.referenciales.duracion_consulta.duracion_consulta_api import duraconsuapi
#instrumento utilizado
from app.rutas.referenciales.instrumento.instrumento_api import instapi
#turno
from app.rutas.referenciales.turno.turno_api import turnoapi
#tratamiento
from app.rutas.referenciales.tratamiento.tratamiento_api import tratapi
#diagnostico
from app.rutas.referenciales.diagnostico.diagnostico_api import diagapi
#cita
from app.rutas.administracion.cita.cita_api import citaapi




# APIS v1
#Ciudad
apiversion1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=apiversion1)

#Pais
apiversion1 = '/api/v1'
app.register_blueprint(paisapi, url_prefix=apiversion1)

#nacionalidad
apiversion1 = '/api/v1'
app.register_blueprint(nacioapi, url_prefix=apiversion1)

#ocupacion
apiversion1 = '/api/v1'
app.register_blueprint(ocupapi, url_prefix=apiversion1)

#Estado civil
apiversion1 = '/api/v1'
app.register_blueprint(estacivapi, url_prefix=apiversion1)

#Estado de la cita
apiversion1 = '/api/v1'
app.register_blueprint(estacitapi, url_prefix=apiversion1)

#persona
apiversion1 = '/api/v1'
app.register_blueprint(persapi, url_prefix=apiversion1)

#especialidad
apiversion1 = '/api/v1'
app.register_blueprint(especiapi, url_prefix=apiversion1)

#dia
apiversion1 = '/api/v1'
app.register_blueprint(diaapi, url_prefix=apiversion1)

#duracion de la consulta
apiversion1 = '/api/v1'
app.register_blueprint(duraconsuapi, url_prefix=apiversion1)

#instrumento utilizado
apiversion1 = '/api/v1'
app.register_blueprint(instapi, url_prefix=apiversion1)

#turno
apiversion1 = '/api/v1'
app.register_blueprint(turnoapi, url_prefix=apiversion1)

#tratamiento
apiversion1 = '/api/v1'
app.register_blueprint(tratapi, url_prefix=apiversion1)

#diagnostico
apiversion1 = '/api/v1'
app.register_blueprint(diagapi, url_prefix=apiversion1)

# Cita
version1 = '/api/v1'
app.register_blueprint(citaapi, url_prefix=version1)








@app.route('/login')
def login():
    return render_template('login-index.html')

@app.route('/vista')
def vista():
    return render_template('vista-index.html')












# importar gestionar compras
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedidos_compras_routes import pdcmod

# registro de modulos - gestionar compras
modulo1 = '/gestionar-compras'
app.register_blueprint(pdcmod, url_prefix=f'{modulo1}/registrar-pedido-compras')

# APIS v1
from app.rutas.referenciales.sucursal.sucursal_api import sucapi
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_api import pdcapi

apiversion1 = '/api/v1'
app.register_blueprint(sucapi, url_prefix=apiversion1)

# Gestionar compras API
app.register_blueprint(pdcapi, url_prefix=f'{apiversion1}/{modulo1}/registrar-pedido-compras')

















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
    'tratamiento': 'tratamiento.tratamientoIndex',  # Agregado
        'pedido de compras': 'pedidocompras.pedidoComprasIndex',  # Agregado
    'pedidos de compras': 'pedidocompras.pedidoComprasIndex',  # Agregado
    'paciente': 'paciente.pacienteIndex',  # Agregado
    'pacientes': 'paciente.pacienteIndex',  # Agregado
    'consulta': 'consulta.consultaIndex',  # Agregado
    'consultas': 'consulta.consultaIndex',  # Agregado
    'agendar vista': 'vistagendar.agendarIndex',  # Agregado
    'agendar vistas': 'vistagendar.agendarIndex'  # Agregado
    }

    # Verificar si el término coincide con alguna clave en rutas
    if termino in rutas:
        # Redirigir a la página correspondiente
        return redirect(url_for(rutas[termino]))
    else:
        # Renderizar una página con un mensaje de "no encontrado"
        return render_template('no_encontrado.html', termino=termino)
    
from flask import render_template, request, redirect, url_for


@app.route('/perfil')
def perfil():
    return render_template('perfil_usuario.html')


@app.route('/registrar')
def registrar():
    return render_template('registro.html')

      # Importar el blueprint de rutas principales

def create_app():
    app = Flask(__name__)
    
    # Registrar los Blueprints
    app.register_blueprint()

    return app
