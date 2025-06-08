from flask import Blueprint, request, jsonify, current_app as app
from app.dao.seguridad.modulo.ModuloDao import ModuloDao  # Ajusta esta ruta según tu estructura

moduloapi = Blueprint('moduloapi', __name__)

# Trae todos los módulos
@moduloapi.route('/modulos', methods=['GET'])
def getModulos():
    modulodao = ModuloDao()
    try:
        modulos = modulodao.getModulos()
        return jsonify({
            'success': True,
            'data': modulos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los módulos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un módulo por ID
@moduloapi.route('/modulos/<int:modulo_id>', methods=['GET'])
def getModulo(modulo_id):
    modulodao = ModuloDao()
    try:
        modulo = modulodao.getModuloById(modulo_id)
        if modulo:
            return jsonify({
                'success': True,
                'data': modulo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el módulo con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener módulo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo módulo
@moduloapi.route('/modulos', methods=['POST'])
def addModulo():
    data = request.get_json()
    modulodao = ModuloDao()

    if not data or 'mod_des' not in data or not data['mod_des'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo mod_des es obligatorio y no puede estar vacío.'
        }), 400

    try:
        mod_des = data['mod_des'].strip()
        modulo_id = modulodao.guardarModulo(mod_des)
        if modulo_id:
            return jsonify({
                'success': True,
                'data': {'mod_id': modulo_id, 'mod_des': mod_des},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el módulo. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar módulo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un módulo
@moduloapi.route('/modulos/<int:modulo_id>', methods=['PUT'])
def updateModulo(modulo_id):
    data = request.get_json()
    modulodao = ModuloDao()

    if not data or 'mod_des' not in data or not data['mod_des'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo mod_des es obligatorio y no puede estar vacío.'
        }), 400

    mod_des = data['mod_des'].strip()

    try:
        if modulodao.updateModulo(modulo_id, mod_des):
            return jsonify({
                'success': True,
                'data': {'mod_id': modulo_id, 'mod_des': mod_des},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el módulo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar módulo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un módulo
@moduloapi.route('/modulos/<int:modulo_id>', methods=['DELETE'])
def deleteModulo(modulo_id):
    modulodao = ModuloDao()
    try:
        if modulodao.deleteModulo(modulo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Módulo con ID {modulo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el módulo con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar módulo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
