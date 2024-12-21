from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.estado_laboral.Estado_laboralDao import Estado_laboralDao

estado_laboralapi = Blueprint('estado_laboralapi', __name__)

# Trae todos los estado_laborales
@estado_laboralapi.route('/estado_laborales', methods=['GET'])
def getEstado_laborales():
    estado_laboraldao = Estado_laboralDao()

    try:
        estado_laborales = estado_laboraldao.getEstado_laborales()

        return jsonify({
            'success': True,
            'data': estado_laborales,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los estado_laborales: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un estado_laboral por ID
@estado_laboralapi.route('/estado_laborales/<int:estado_laboral_id>', methods=['GET'])
def getEstado_laboral(estado_laboral_id):
    estado_laboraldao = Estado_laboralDao()

    try:
        estado_laboral = estado_laboraldao.getEstado_laboralById(estado_laboral_id)

        if estado_laboral:
            return jsonify({
                'success': True,
                'data': estado_laboral,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado_laboral con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener estado_laboral: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo estado_laboral
@estado_laboralapi.route('/estado_laborales', methods=['POST'])
def addEstado_laboral():
    data = request.get_json()
    estado_laboraldao = Estado_laboralDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        estado_laboral_id = estado_laboraldao.guardarEstado_laboral(descripcion)
        if estado_laboral_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_estado_laboral': estado_laboral_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el estado_laboral. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar estado_laboral: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un estado_laboral
@estado_laboralapi.route('/estado_laborales/<int:estado_laboral_id>', methods=['PUT'])
def updateEstado_laboral(estado_laboral_id):
    data = request.get_json()
    estado_laboraldao = Estado_laboralDao()

    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    descripcion = data['descripcion']
    try:
        if estado_laboraldao.updateEstado_laboral(estado_laboral_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id_estado_laboral': estado_laboral_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado_laboral con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar estado_laboral: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un estado_laboral
@estado_laboralapi.route('/estado_laborales/<int:estado_laboral_id>', methods=['DELETE'])
def deleteEstado_laboral(estado_laboral_id):
    estado_laboraldao = Estado_laboralDao()

    try:
        if estado_laboraldao.deleteEstado_laboral(estado_laboral_id):
            return jsonify({
                'success': True,
                'mensaje': f'Estado_laboral con ID {estado_laboral_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado_laboral con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar estado_laboral: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500