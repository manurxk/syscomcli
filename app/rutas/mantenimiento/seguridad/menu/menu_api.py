from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.seguridad.menu.MenuDao import MenuDao
from app.auth.utils.decorators import role_required

menuapi = Blueprint('menuapi', __name__)


@menuapi.route('/menu/paginas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getPaginas():
    try:
        data = MenuDao().getPaginas()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener páginas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@menuapi.route('/menu/roles/<int:id_rol>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getMatrizMenu(id_rol):
    try:
        data = MenuDao().getMatrizMenu(id_rol)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener matriz de menú: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@menuapi.route('/menu/roles/<int:id_rol>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def guardarMatrizMenu(id_rol):
    data = request.get_json() or {}
    cambios = data.get('cambios') or []

    if not isinstance(cambios, list) or not cambios:
        return jsonify({'success': False, 'error': 'No se recibieron cambios para guardar.'}), 400

    for cambio in cambios:
        if 'id_pagina' not in cambio or 'visible' not in cambio:
            return jsonify({'success': False, 'error': 'Cada cambio debe incluir id_pagina y visible.'}), 400

    roles_sesion = {r.upper() for r in session.get('roles', [])}
    if 'SUPERADMIN' not in roles_sesion:
        cod_rol_objetivo = MenuDao().getCodRol(id_rol)
        if cod_rol_objetivo == 'SUPERADMIN':
            return jsonify({'success': False, 'error': 'Solo SUPERADMIN puede modificar el menú del rol SUPERADMIN.'}), 403

    try:
        MenuDao().guardarMatrizMenu(id_rol, cambios, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': 'Menú actualizado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al guardar matriz de menú: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
