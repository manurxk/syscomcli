from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.sala_atencion.Sala_atencionDao import Sala_atencionDao

salapi = Blueprint('salapi', __name__)

# Trae todas las salas de atención
@salapi.route('/sala_atenciones', methods=['GET'])
def getSala_atenciones():
    saldao = Sala_atencionDao()

    try:
        sala_atenciones = saldao.getSala_atenciones()

        return jsonify({
            'success': True,
            'data': sala_atenciones,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las salas de atención: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae una sala de atención por ID
@salapi.route('/sala_atenciones/<int:sala_atencion_id>', methods=['GET'])
def getSala_atencion(sala_atencion_id):
    saldao = Sala_atencionDao()

    try:
        sala_atencion = saldao.getSala_atencionById(sala_atencion_id)

        if sala_atencion:
            return jsonify({
                'success': True,
                'data': sala_atencion,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la sala de atención con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener sala de atención: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva sala de atención
@salapi.route('/sala_atenciones', methods=['POST'])
def addSala_atencion():
    data = request.get_json()
    saldao = Sala_atencionDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        sala_atencion_id = saldao.guardarSala_atencion(nombre)
        if sala_atencion_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_sala_atencion': sala_atencion_id, 'nombre': nombre},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la sala de atención. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar sala de atención: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza una sala de atención
@salapi.route('/sala_atenciones/<int:sala_atencion_id>', methods=['PUT'])
def updateSala_atencion(sala_atencion_id):
    data = request.get_json()
    saldao = Sala_atencionDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    nombre = data['nombre']
    try:
        if saldao.updateSala_atencion(sala_atencion_id, nombre.upper()):
            return jsonify({
                'success': True,
                'data': {'id_sala_atencion': sala_atencion_id, 'nombre': nombre},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la sala de atención con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar sala de atención: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina una sala de atención
@salapi.route('/sala_atenciones/<int:sala_atencion_id>', methods=['DELETE'])
def deleteSala_atencion(sala_atencion_id):
    saldao = Sala_atencionDao()

    try:
        # Usar el retorno de eliminarSala_atencion para determinar el éxito
        if saldao.deleteSala_atencion(sala_atencion_id):
            return jsonify({
                'success': True,
                'mensaje': f'sala de atención con ID {sala_atencion_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la sala de atención con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar sala de atención: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
