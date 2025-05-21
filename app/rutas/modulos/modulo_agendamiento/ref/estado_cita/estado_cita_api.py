from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.modulo_agendamiento.ref.estado_cita.Estado_citaDao import Estado_citaDao

estadoapi = Blueprint('estadoapi', __name__)  # Cambié estapi por estadoapi

# Trae todos los estado_citas
@estadoapi.route('/estado_citas', methods=['GET'])
def getEstado_citas():
    estadodao = Estado_citaDao()  # Cambié estdao por estadodao

    try:
        estado_citas = estadodao.getEstado_citas()

        return jsonify({
            'success': True,
            'data': estado_citas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los estado_citas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un estado_cita por ID
@estadoapi.route('/estado_citas/<int:estado_cita_id>', methods=['GET'])
def getEstado_cita(estado_cita_id):
    estadodao = Estado_citaDao()  # Cambié estdao por estadodao

    try:
        estado_cita = estadodao.getEstado_citaById(estado_cita_id)

        if estado_cita:
            return jsonify({
                'success': True,
                'data': estado_cita,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado_cita con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener estado_cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo estado_cita
@estadoapi.route('/estado_citas', methods=['POST'])
def addEstado_cita():
    data = request.get_json()
    estadodao = Estado_citaDao()  # Cambié estdao por estadodao

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        estado_cita_id = estadodao.guardarEstado_cita(descripcion)
        if estado_cita_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_estado_cita': estado_cita_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el estado_cita. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar estado_cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un estado_cita
@estadoapi.route('/estado_citas/<int:estado_cita_id>', methods=['PUT'])
def updateEstado_cita(estado_cita_id):
    data = request.get_json()
    estadodao = Estado_citaDao()  # Cambié estdao por estadodao

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if estadodao.updateEstado_cita(estado_cita_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id_estado_cita': estado_cita_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado_cita con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar estado_cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un estado_cita
@estadoapi.route('/estado_citas/<int:estado_cita_id>', methods=['DELETE'])
def deleteEstado_cita(estado_cita_id):
    estadodao = Estado_citaDao()  # Cambié estdao por estadodao

    try:
        # Usar el retorno de eliminarEstado_cita para determinar el éxito
        if estadodao.deleteEstado_cita(estado_cita_id):
            return jsonify({
                'success': True,
                'mensaje': f'estado_cita con ID {estado_cita_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado_cita con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar estado_cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
