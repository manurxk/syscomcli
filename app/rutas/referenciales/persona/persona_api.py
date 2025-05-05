from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.persona.PersonaDao import PersonaDao

# Definir el Blueprint para las rutas de Persona
perapi = Blueprint('perapi', __name__)

# Ruta para obtener todas las personas
@perapi.route('/personas', methods=['GET'])
def getPersonas():
    persona_dao = PersonaDao()

    try:
        personas = persona_dao.getPersonas()  # Obtener todas las personas
        return jsonify({
            'success': True,
            'data': personas,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener personas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Ruta para obtener una persona por ID
@perapi.route('/personas/<int:id_persona>', methods=['GET'])
def getPersona(id_persona):
    persona_dao = PersonaDao()

    try:
        persona = persona_dao.getPersonaById(id_persona)

        if persona:
            return jsonify({
                'success': True,
                'data': persona,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Ruta para agregar una nueva persona
@perapi.route('/personas', methods=['POST'])
def addPersona():
    data = request.get_json()
    persona_dao = PersonaDao()

    # Aseguramos que los campos requeridos estén presentes y no vacíos
    campos_requeridos = ['nombres', 'apellidos', 'ci', 'fechanac', 'sexo']

    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400  # Devuelve error 400 si algún campo está vacío o no presente

    try:
        # Guardamos la persona en la base de datos
        result = persona_dao.guardarPersona(
            data['nombres'].strip(),
            data['apellidos'].strip(),
            data['ci'].strip(),
            data['fechanac'],
            data['sexo'].strip()
        )

        if result:
            return jsonify({
                'success': True,
                'data': data,
                'error': None
            }), 201  # Código 201 para creación exitosa

        return jsonify({
            'success': False,
            'error': 'No se pudo crear la persona. Verifique los datos ingresados.'
        }), 400

    except Exception as e:
        app.logger.error(f"Error al agregar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Ruta para actualizar una persona
@perapi.route('/personas/<int:id_persona>', methods=['PUT'])
def updatePersona(id_persona):
    data = request.get_json()
    persona_dao = PersonaDao()

    # Aseguramos que los campos requeridos estén presentes y no vacíos
    campos_requeridos = ['nombres', 'apellidos', 'ci', 'fechanac', 'sexo']

    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400  # Devuelve error 400 si algún campo está vacío o no presente

    try:
        # Actualizar la persona en la base de datos
        result = persona_dao.updatePersona(
            id_persona,
            data['nombres'].strip(),
            data['apellidos'].strip(),
            data['ci'].strip(),
            data['fechanac'],
            data['sexo'].strip()
        )

        if result:
            return jsonify({
                'success': True,
                'data': {
                    'id_persona': id_persona,
                    'nombres': data['nombres'],
                    'apellidos': data['apellidos'],
                    'ci': data['ci'],
                    'fechanac': data['fechanac'],
                    'sexo': data['sexo']
                },
                'error': None
            }), 200  # Código 200 para éxito

        return jsonify({
            'success': False,
            'error': 'No se pudo actualizar la persona. Verifique los datos ingresados.'
        }), 400

    except Exception as e:
        app.logger.error(f"Error al actualizar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Ruta para eliminar una persona
@perapi.route('/personas/<int:id_persona>', methods=['DELETE'])
def deletePersona(id_persona):
    persona_dao = PersonaDao()

    try:
        result = persona_dao.deletePersona(id_persona)

        if result:
            return jsonify({
                'success': True,
                'mensaje': f'Persona con ID {id_persona} eliminada correctamente.',
                'error': None
            }), 200  # Código 200 para éxito

        return jsonify({
            'success': False,
            'error': 'No se pudo eliminar la persona o no se encontró el ID proporcionado.'
        }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
