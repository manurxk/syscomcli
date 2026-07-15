from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.referenciales.permisos.PermisoDao import PermisoDao
from app.auth.utils.decorators import role_required

permisosapi = Blueprint('permisosapi', __name__)


@permisosapi.route('/permisos/modulos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getModulos():
    try:
        data = PermisoDao().getModulos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener módulos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@permisosapi.route('/permisos/acciones', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getAcciones():
    try:
        data = PermisoDao().getAcciones()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener acciones: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@permisosapi.route('/permisos/roles/<int:id_rol>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getMatrizPermisos(id_rol):
    try:
        data = PermisoDao().getMatrizPermisos(id_rol)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener matriz de permisos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@permisosapi.route('/permisos/roles/<int:id_rol>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def guardarMatrizPermisos(id_rol):
    data = request.get_json() or {}
    cambios = data.get('cambios') or []

    if not isinstance(cambios, list) or not cambios:
        return jsonify({'success': False, 'error': 'No se recibieron cambios para guardar.'}), 400

    for cambio in cambios:
        if 'id_modulo' not in cambio or 'id_accion' not in cambio or 'permitido' not in cambio:
            return jsonify({'success': False, 'error': 'Cada cambio debe incluir id_modulo, id_accion y permitido.'}), 400

    roles_sesion = {r.upper() for r in session.get('roles', [])}
    if 'SUPERADMIN' not in roles_sesion:
        cod_rol_objetivo = PermisoDao().getCodRol(id_rol)
        if cod_rol_objetivo == 'SUPERADMIN':
            return jsonify({'success': False, 'error': 'Solo SUPERADMIN puede modificar los permisos del rol SUPERADMIN.'}), 403

    try:
        PermisoDao().guardarMatrizPermisos(id_rol, cambios, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': 'Permisos actualizados correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al guardar matriz de permisos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
