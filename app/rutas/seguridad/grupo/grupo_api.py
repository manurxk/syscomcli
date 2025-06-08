from flask import Blueprint, request, jsonify, current_app as app
from app.dao.seguridad.grupo.GrupoDao import GrupoDao  # Ajusta la ruta según tu estructura

grupoapi = Blueprint('grupoapi', __name__)

# Trae todos los grupos
@grupoapi.route('/grupos', methods=['GET'])
def getGrupos():
    grupodao = GrupoDao()
    try:
        grupos = grupodao.getGrupos()
        return jsonify({
            'success': True,
            'data': grupos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los grupos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un grupo por ID
@grupoapi.route('/grupos/<int:grupo_id>', methods=['GET'])
def getGrupo(grupo_id):
    grupodao = GrupoDao()
    try:
        grupo = grupodao.getGrupoById(grupo_id)
        if grupo:
            return jsonify({
                'success': True,
                'data': grupo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el grupo con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener grupo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo grupo
@grupoapi.route('/grupos', methods=['POST'])
def addGrupo():
    data = request.get_json()
    grupodao = GrupoDao()

    if not data or 'gru_des' not in data or not data['gru_des'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo gru_des es obligatorio y no puede estar vacío.'
        }), 400

    try:
        gru_des = data['gru_des'].strip()
        grupo_id = grupodao.guardarGrupo(gru_des)
        if grupo_id:
            return jsonify({
                'success': True,
                'data': {'gru_id': grupo_id, 'gru_des': gru_des},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el grupo. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar grupo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un grupo
@grupoapi.route('/grupos/<int:grupo_id>', methods=['PUT'])
def updateGrupo(grupo_id):
    data = request.get_json()
    grupodao = GrupoDao()

    if not data or 'gru_des' not in data or not data['gru_des'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo gru_des es obligatorio y no puede estar vacío.'
        }), 400

    gru_des = data['gru_des'].strip()

    try:
        if grupodao.updateGrupo(grupo_id, gru_des):
            return jsonify({
                'success': True,
                'data': {'gru_id': grupo_id, 'gru_des': gru_des},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el grupo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar grupo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un grupo
@grupoapi.route('/grupos/<int:grupo_id>', methods=['DELETE'])
def deleteGrupo(grupo_id):
    grupodao = GrupoDao()
    try:
        if grupodao.deleteGrupo(grupo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Grupo con ID {grupo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el grupo con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar grupo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
