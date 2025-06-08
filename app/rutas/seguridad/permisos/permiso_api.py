from flask import Blueprint, request, jsonify, current_app as app
from app.dao.seguridad.permiso.permiso_dao import SeguridadDao

seguridad_api = Blueprint('seguridad_api', __name__)

# --- USUARIOS ---

@seguridad_api.route('/usuarios', methods=['GET'])
def get_usuarios():
    dao = SeguridadDao()
    try:
        usuarios = dao.getUsuarios()
        return jsonify({'success': True, 'data': usuarios, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener usuarios: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

# --- GRUPOS ---

@seguridad_api.route('/grupos', methods=['GET'])
def get_grupos():
    dao = SeguridadDao()
    try:
        grupos = dao.getGrupos()
        return jsonify({'success': True, 'data': grupos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener grupos: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

# --- PAGINAS ---

@seguridad_api.route('/paginas', methods=['GET'])
def get_paginas():
    dao = SeguridadDao()
    try:
        paginas = dao.getPaginas()
        return jsonify({'success': True, 'data': paginas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener páginas: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

# --- PERMISOS POR GRUPO ---

@seguridad_api.route('/grupos/<int:grupo_id>/permisos', methods=['GET'])
def get_permisos_por_grupo(grupo_id):
    dao = SeguridadDao()
    try:
        permisos = dao.getPermisosPorGrupo(grupo_id)
        return jsonify({'success': True, 'data': permisos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener permisos por grupo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@seguridad_api.route('/grupos/<int:grupo_id>/permisos', methods=['POST'])
def asignar_permiso(grupo_id):
    data = request.get_json()
    if not data or 'pagina_id' not in data:
        return jsonify({'success': False, 'error': 'Falta pagina_id en el cuerpo'}), 400

    pagina_id = data['pagina_id']
    dao = SeguridadDao()
    try:
        exito = dao.asignarPermisoAGrupo(grupo_id, pagina_id)
        if exito:
            return jsonify({'success': True, 'mensaje': 'Permiso asignado', 'error': None}), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo asignar el permiso'}), 500
    except Exception as e:
        app.logger.error(f"Error al asignar permiso: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@seguridad_api.route('/grupos/<int:grupo_id>/permisos/<int:pagina_id>', methods=['DELETE'])
def eliminar_permiso(grupo_id, pagina_id):
    dao = SeguridadDao()
    try:
        exito = dao.eliminarPermisoAGrupo(grupo_id, pagina_id)
        if exito:
            return jsonify({'success': True, 'mensaje': 'Permiso eliminado', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el permiso o no existía'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar permiso: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500
