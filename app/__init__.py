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
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.pais.pais_routes import paismod
from app.rutas.referenciales.nacionalidad.nacionalidad_routes import naciomod  #nacionalidad
from app.rutas.referenciales.producto.producto_routes import promod
#from app.rutas.referenciales.persona.persona_routes import persmod  #persona
from app.rutas.referenciales.proveedor.proveedor_routes import provmod
from app.rutas.referenciales.cliente.cliente_routes import climod
from app.rutas.referenciales.sucursal.sucursal_routes import sucmod
from app.rutas.referenciales.deposito.deposito_routes import depomod
#from app.rutas.referenciales.estado_civil.estado_civil_routes import estacivmod  #estado civil
from app.rutas.referenciales.sexo.sexo_routes import sexomod
from app.rutas.referenciales.marca.marca_routes import marcmod
from app.rutas.referenciales.apertura.apertura_routes import apermod



from app.rutas.gestionar_personas.persona.persona_routes import persona_mod
from app.rutas.gestionar_personas.medico.medico_routes import medicomod
from app.rutas.gestionar_personas.paciente.paciente_routes import pacientemod

from app.rutas.referenciales.estado_civil.estado_civil_routes import estmod
from app.rutas.referenciales.genero.genero_routes import genmod
from app.rutas.gestionar_personas.usuario.usuario_routes import usumod


from app.rutas.modulos.modulo_agendamiento.mov.agenda_medica.agenda_medica_routes import agendamedmod



# importar gestionar compras
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedidos_compras_routes  import pdcmod

# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')

app.register_blueprint(paismod, url_prefix=f'{modulo0}/pais')

app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')  #nacionalidad

app.register_blueprint(promod, url_prefix=f'{modulo0}/producto')

#app.register_blueprint(persmod, url_prefix=f'{modulo0}/persona') #persona

app.register_blueprint(provmod, url_prefix=f'{modulo0}/proveedor')

app.register_blueprint(climod, url_prefix=f'{modulo0}/cliente')

app.register_blueprint(sucmod, url_prefix=f'{modulo0}/sucursal')

app.register_blueprint(depomod, url_prefix=f'{modulo0}/deposito')

#app.register_blueprint(estacivmod, url_prefix=f'{modulo0}/estadocivil')  #estado civil

app.register_blueprint(sexomod, url_prefix=f'{modulo0}/sexo')

app.register_blueprint(marcmod, url_prefix=f'{modulo0}/marca')

app.register_blueprint(apermod, url_prefix=f'{modulo0}/apertura')


app.register_blueprint(persona_mod, url_prefix=f'{modulo0}/persona')

app.register_blueprint(medicomod, url_prefix=f'{modulo0}/medico')

app.register_blueprint(pacientemod, url_prefix=f'{modulo0}/paciente')

app.register_blueprint(estmod, url_prefix=f'{modulo0}/estado_civil')

app.register_blueprint(genmod, url_prefix=f'{modulo0}/genero')


app.register_blueprint(usumod, url_prefix=f'{modulo0}/usuaruio')

app.register_blueprint(agendamedmod, url_prefix=f'{modulo0}/agenda_medica')


# registro de modulos - gestionar compras
modulo1 = '/gestionar-compras'
app.register_blueprint(pdcmod, url_prefix=f'{modulo1}/registrar-pedido-compras')

# APIS v1
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.apertura.apertura_api import aperapi
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi

from app.rutas.referenciales.pais.pais_api import paiapi

from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacioapi

from app.rutas.referenciales.producto.producto_api import proapi

#from app.rutas.referenciales.persona.persona_api import persapi

from app.rutas.referenciales.proveedor.proveedor_api import provapi

from app.rutas.referenciales.cliente.cliente_api import cliapi

from app.rutas.referenciales.sucursal.sucursal_api import sucapi

from app.rutas.referenciales.deposito.deposito_api import depoapi

#from app.rutas.referenciales.estado_civil.estado_civil_api import estacivapi

from app.rutas.referenciales.sexo.sexo_api import sexoapi

from app.rutas.referenciales.marca.marca_api import marcaapi


from app.rutas.gestionar_personas.persona.persona_api import personaapi

from app.rutas.gestionar_personas.medico.medico_api import medicoapi

from app.rutas.gestionar_personas.paciente.paciente_api import pacienteapi


from app.rutas.referenciales.genero.genero_api import genapi

from app.rutas.referenciales.estado_civil.estado_civil_api import estapi

from app.rutas.gestionar_personas.usuario.usuario_api import usuarioapi

from app.rutas.modulos.modulo_agendamiento.mov.agenda_medica.agenda_medica_api import agenda_medica_api


#pedido de compra
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_api import pdcapi
from app.rutas.referenciales.sucursal.sucursal_api import sucapi


apiversion1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=apiversion1)

app.register_blueprint(paiapi, url_prefix=apiversion1)

app.register_blueprint(nacioapi, url_prefix=apiversion1)

app.register_blueprint(proapi, url_prefix=apiversion1)

#app.register_blueprint(persapi, url_prefix=apiversion1)

app.register_blueprint(provapi, url_prefix=apiversion1)

app.register_blueprint(cliapi, url_prefix=apiversion1)

app.register_blueprint(depoapi, url_prefix=apiversion1)

#app.register_blueprint(estacivapi, url_prefix=apiversion1)

app.register_blueprint(sexoapi, url_prefix=apiversion1)

app.register_blueprint(marcaapi, url_prefix=apiversion1)

app.register_blueprint(aperapi, url_prefix=apiversion1)

app.register_blueprint(personaapi, url_prefix=apiversion1)

app.register_blueprint(medicoapi,url_prefix=apiversion1)

app.register_blueprint(pacienteapi, url_prefix=apiversion1)

app.register_blueprint(genapi, url_prefix=apiversion1)

app.register_blueprint(estapi, url_prefix=apiversion1)

app.register_blueprint(usuarioapi, url_prefix=apiversion1)

app.register_blueprint(agenda_medica_api, url_prefix=apiversion1)


# Gestionar compras API
apiversion1 = '/api/v1'
app.register_blueprint(pdcapi, url_prefix=f'{apiversion1}/{modulo1}/registrar-pedido-compras')
app.register_blueprint(sucapi, url_prefix=apiversion1)




















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
    