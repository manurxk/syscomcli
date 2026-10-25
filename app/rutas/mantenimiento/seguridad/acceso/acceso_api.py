from flask import Blueprint, jsonify, current_app as app, session, request

from app.dao.mantenimiento.seguridad.acceso.AccesoDao import AccesoDao
from app.dao.auth.user_dao import UsuarioDao
from app.auth.services.auth_service import AuthService
from app.auth.utils.decorators import role_required
from app.core.base_dao import BaseDAO
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion
from app.utils.soporte import ocultar_soporte, es_usuario_soporte, es_superadmin_sesion

accesoapi = Blueprint('accesoapi', __name__)

_dao = BaseDAO(db_name_env="DB_NAME_NUEVA")


@accesoapi.route('/acceso/usuarios', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getUsuariosConEstadoAcceso():
    """GET: usuarios con su estado de acceso."""
    try:
        data = ocultar_soporte(AccesoDao().getUsuariosConEstadoAcceso())
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener estado de acceso: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@accesoapi.route('/acceso/usuarios/<int:id_usuario>/sesiones', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getSesionesPorUsuario(id_usuario):
    """GET: sesiones del usuario."""
    if not es_superadmin_sesion() and es_usuario_soporte(id_usuario):
        return jsonify({'success': False, 'error': 'Usuario no encontrado.'}), 404
    try:
        data = AccesoDao().getSesionesPorUsuario(id_usuario)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener sesiones del usuario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@accesoapi.route('/acceso/sesiones/<int:id_sesion>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def cerrarSesion(id_sesion):
    """DELETE: cierra la sesión indicada."""
    try:
        fila = _dao.execute_query_one("SELECT token_sesion, id_usuario FROM sesiones WHERE id_sesion = %s", (id_sesion,))
        if not fila or (not es_superadmin_sesion() and es_usuario_soporte(fila['id_usuario'])):
            return jsonify({'success': False, 'error': 'Sesión no encontrada'}), 404

        exitoso = AuthService.cerrar_sesion(fila['token_sesion'], tipo_cierre='ADMIN_FORCE')
        if not exitoso:
            return jsonify({'success': False, 'error': 'No se pudo cerrar la sesión'}), 400

        app.logger.info(f"Sesión {id_sesion} cerrada desde Mantener Acceso por {session.get('usu_nick')}")
        return jsonify({'success': True, 'mensaje': 'Sesión cerrada exitosamente'}), 200
    except Exception as e:
        app.logger.error(f"Error al cerrar sesión: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@accesoapi.route('/acceso/usuarios/<int:id_usuario>/desbloquear', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desbloquearUsuario(id_usuario):
    """POST: desbloquea la cuenta del usuario y la vuelve a nivel 0."""
    if not es_superadmin_sesion() and es_usuario_soporte(id_usuario):
        return jsonify({'success': False, 'error': 'Usuario no encontrado.'}), 404
    try:
        ok = UsuarioDao().resetearIntentos(id_usuario, usuario_modificacion=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'Usuario no encontrado.'}), 404
        app.logger.info(f"Usuario {id_usuario} desbloqueado desde Accesos por {session.get('usu_nick')}")
        AuditoriaDao().registrar_evento(
            id_usuario=session.get('id_usuario'),
            accion=AuditAccion.ACCOUNT_UNLOCKED,
            detalle=f"Cuenta id_usuario={id_usuario} desbloqueada desde Accesos por \"{session.get('usu_nick')}\"",
            ip_origen=request.remote_addr
        )
        return jsonify({'success': True, 'mensaje': 'Usuario desbloqueado.'}), 200
    except Exception as e:
        app.logger.error(f"Error al desbloquear usuario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@accesoapi.route('/acceso/usuarios/<int:id_usuario>/mfa/revocar', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def revocarMfa(id_usuario):
    """POST: revoca el MFA configurado del usuario."""
    if not es_superadmin_sesion() and es_usuario_soporte(id_usuario):
        return jsonify({'success': False, 'error': 'Usuario no encontrado.'}), 404
    try:
        AccesoDao().revocarMfa(id_usuario, usuario_modificacion=session.get('id_usuario'))
        app.logger.info(f"MFA revocado para usuario {id_usuario} por {session.get('usu_nick')}")
        return jsonify({
            'success': True,
            'mensaje': 'MFA desactivado. El usuario deberá vincularlo nuevamente.'
        }), 200
    except Exception as e:
        app.logger.error(f"Error al revocar MFA: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
