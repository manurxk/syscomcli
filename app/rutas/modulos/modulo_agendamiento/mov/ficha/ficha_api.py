from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ficha.FichaDao import FichaDao

fichaapi = Blueprint('fichaapi', __name__)

# Trae todas las fichas
@fichaapi.route('/fichas', methods=['GET'])
def getFichas():
    fichadao = FichaDao()

    try:
        fichas = fichadao.getFichas()

        return jsonify({
            'success': True,
            'data': fichas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las fichas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@fichaapi.route('/fichas/<int:ficha_id>', methods=['GET'])
def getFicha(ficha_id):
    fichadao = FichaDao()

    try:
        ficha = fichadao.getFichaById(ficha_id)

        if ficha:
            return jsonify({
                'success': True,
                'data': ficha,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la ficha con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener ficha: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva ficha
@fichaapi.route('/fichas', methods=['POST'])
def addFicha():
    data = request.get_json()
    fichadao = FichaDao()

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
        ficha_id = fichadao.guardarFicha(descripcion)
        if ficha_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': ficha_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la ficha. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al agregar ficha: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@fichaapi.route('/fichas/<int:ficha_id>', methods=['PUT'])
def updateFicha(ficha_id):
    data = request.get_json()
    fichadao = FichaDao()

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
        if fichadao.updateFicha(ficha_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': ficha_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la ficha con el ID proporcionado o no se pudo actualizar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al actualizar ficha: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@fichaapi.route('/fichas/<int:ficha_id>', methods=['DELETE'])
def deleteFicha(ficha_id):
    fichadao = FichaDao()

    try:
        # Usar el retorno de deleteFicha para determinar el éxito
        if fichadao.deleteFicha(ficha_id):
            return jsonify({
                'success': True,
                'mensaje': f'Ficha con ID {ficha_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la ficha con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar ficha: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
