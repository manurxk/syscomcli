from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.auth.user_dao import UsuarioDao
from app.utils.soporte import ocultar_soporte, es_usuario_soporte
from app.dao.mantenimiento.seguridad.acceso.AccesoDao import AccesoDao
from app.auth.utils.decorators import role_required
from app.auth.utils.password_validator import validar_politica_password
from app.core.base_dao import BaseDAO
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion
from app.utils.mensajes_validacion import msg_obligatorio


usuarioapi = Blueprint('usuarioapi', __name__)

_dao_roles = BaseDAO(db_name_env="DB_NAME_NUEVA")


def _es_superadmin():
    """Indica si el usuario en sesión tiene el rol SUPERADMIN."""
    return 'SUPERADMIN' in {(r or "").strip().upper() for r in session.get("roles", [])}


def _tope_usuarios():
    """Tope de usuarios activos con funcionario (lo fija el Superadministrador en la empresa)."""
    return UsuarioDao().obtener_topes()[1]


def _mensaje_tope_usuarios():
    """Mensaje de error cuando se alcanzó el máximo de usuarios activos con funcionario."""
    return (f'Se alcanzó el máximo de {_tope_usuarios()} usuarios activos con funcionario. '
            'Desactive un usuario existente antes de crear o reactivar otro.')


def _protegido_de_soporte(id_usuario):
    """Respuesta 404 si el usuario pedido es el Superadministrador y quien consulta no lo es (no debe saber que existe)."""
    if not _es_superadmin() and es_usuario_soporte(id_usuario):
        return jsonify({'success': False, 'error': 'No se encontró el usuario con el ID proporcionado.'}), 404
    return None


@usuarioapi.route('/usuarios/cupo', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getCupoUsuarios():
    """Cupo usado de funcionarios y usuarios activos, para mostrar «x de N» en las pantallas."""
    dao = UsuarioDao()
    max_func, max_usu = dao.obtener_topes()
    return jsonify({'success': True, 'error': None, 'data': {
        'funcionarios': {'activos': dao.contar_funcionarios_activos(), 'maximo': max_func},
        'usuarios': {'activos': dao.contar_usuarios_activos_con_funcionario(), 'maximo': max_usu}}}), 200


# ============================================
# OBTENER TODOS LOS USUARIOS
# ============================================
@usuarioapi.route('/usuarios', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getUsuarios():
    """Obtiene la lista completa de usuarios"""
    usuariodao = UsuarioDao()

    try:
        usuarios = ocultar_soporte(usuariodao.getUsuarios())

        return jsonify({
            'success': True,
            'data': usuarios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener usuarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER USUARIO POR ID
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getUsuario(id_usuario):
    """Obtiene un usuario específico por su ID"""
    usuariodao = UsuarioDao()
    protegido = _protegido_de_soporte(id_usuario)
    if protegido:
        return protegido

    try:
        usuario = usuariodao.getUsuarioById(id_usuario)

        if usuario:
            return jsonify({
                'success': True,
                'data': usuario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# DETALLE DE SEGURIDAD/AUDITORÍA DE UN USUARIO
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>/detalle', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getDetalleUsuario(id_usuario):
    """Todo lo que se muestra en la ventana de detalle de un usuario: datos
    de identidad/bloqueo, historial de logins, resumen de MFA, dispositivos
    confiables, solicitudes de recuperación y sesiones activas."""
    protegido = _protegido_de_soporte(id_usuario)
    if protegido:
        return protegido
    try:
        acceso_dao = AccesoDao()
        detalle = acceso_dao.getDetalleUsuario(id_usuario)
        if not detalle:
            return jsonify({'success': False, 'error': 'No se encontró el usuario.'}), 404

        detalle['historial_accesos'] = acceso_dao.getHistorialAccesos(id_usuario)
        detalle['mfa_resumen'] = acceso_dao.getResumenMfa(id_usuario)
        detalle['dispositivos_confiables'] = acceso_dao.getDispositivosConfiables(id_usuario)
        detalle['solicitudes_recuperacion'] = acceso_dao.getSolicitudesRecuperacion(id_usuario)
        detalle['sesiones_activas'] = acceso_dao.getSesionesPorUsuario(id_usuario)

        return jsonify({'success': True, 'data': detalle, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener detalle de usuario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# OBTENER FUNCIONARIOS SIN USUARIO
# ============================================
@usuarioapi.route('/funcionarios/sin-usuario', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getFuncionariosSinUsuario():
    """Obtiene funcionarios activos que todavía no tienen usuario asignado"""
    usuariodao = UsuarioDao()

    try:
        funcionarios = usuariodao.getFuncionariosSinUsuario()

        return jsonify({
            'success': True,
            'data': funcionarios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener funcionarios sin usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER ROLES DISPONIBLES (catálogo)
# ============================================
@usuarioapi.route('/roles', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getRoles():
    """Lista los roles activos disponibles para asignar a un usuario.
    SUPERADMIN solo lo puede asignar otro Superadministrador."""
    try:
        roles = _dao_roles.execute_query(
            "SELECT id_rol, cod_rol, des_rol FROM roles WHERE est_rol = TRUE ORDER BY id_rol"
        )
        if not _es_superadmin():
            roles = [r for r in roles if r['cod_rol'] != 'SUPERADMIN']
        return jsonify({
            'success': True,
            'data': roles,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener roles: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# VALIDAR USERNAME DISPONIBLE
# ============================================
@usuarioapi.route('/usuarios/validar-username', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def validarUsername():
    """Valida que un username esté disponible"""
    data = request.get_json()
    usuariodao = UsuarioDao()

    username = data.get('username')
    id_usuario = data.get('id_usuario')

    if not username:
        return jsonify({
            'success': False,
            'error': msg_obligatorio('Username')
        }), 400

    try:
        disponible = usuariodao.validarUsernameDisponible(username, id_usuario)

        return jsonify({
            'success': True,
            'data': {'disponible': disponible},
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al validar username: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error al validar el username.'
        }), 500


# ============================================
# CREAR NUEVO USUARIO
# ============================================
@usuarioapi.route('/usuarios', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addUsuario():
    """Crea un nuevo usuario - Administrador o Superadministrador, con tope de usuarios"""
    data = request.get_json()
    usuariodao = UsuarioDao()

    campos_requeridos = ['username', 'password', 'id_funcionario', 'id_rol']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': msg_obligatorio(campo)
            }), 400

    if not _es_superadmin():
        rol = _dao_roles.execute_query_one("SELECT cod_rol FROM roles WHERE id_rol = %s", (data['id_rol'],))
        if rol and rol['cod_rol'] == 'SUPERADMIN':
            return jsonify({
                'success': False,
                'error': 'El rol indicado no es válido.'
            }), 403

    if data.get('est_usuario', True) and usuariodao.contar_usuarios_activos_con_funcionario() >= _tope_usuarios():
        return jsonify({
            'success': False,
            'error': _mensaje_tope_usuarios()
        }), 400

    password_valida, mensaje_password = validar_politica_password(
        data['password'], username=data.get('username')
    )
    if not password_valida:
        return jsonify({
            'success': False,
            'error': mensaje_password
        }), 400

    if data.get('password') != data.get('password_confirmacion'):
        return jsonify({
            'success': False,
            'error': 'Las contraseñas no coinciden.'
        }), 400

    try:
        usuario_id = usuariodao.guardarUsuario(
            username=data['username'],
            password=data['password'],
            id_funcionario=data['id_funcionario'],
            id_rol=data['id_rol'],
            est_usuario=data.get('est_usuario', True),
            usuario_creacion=session.get('id_usuario')
        )

        if usuario_id:
            AuditoriaDao().registrar_evento(
                id_usuario=session.get('id_usuario'),
                accion=AuditAccion.RECORD_CREATE,
                detalle=f"Alta de usuario \"{data['username']}\" (id_usuario={usuario_id})",
                ip_origen=request.remote_addr
            )
            return jsonify({
                'success': True,
                'data': {
                    'id_usuario': usuario_id,
                    'mensaje': 'Usuario creado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear el usuario. Verifique que el username no exista o que el funcionario no tenga ya un usuario asignado.'
            }), 400

    except Exception as e:
        app.logger.error(f"Error al crear usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500


# ============================================
# ACTUALIZAR USUARIO EXISTENTE
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateUsuario(id_usuario):
    """Actualiza un usuario existente - Administrador o Superadministrador (el Administrador no toca al Superadmin)"""
    data = request.get_json()
    usuariodao = UsuarioDao()
    protegido = _protegido_de_soporte(id_usuario)
    if protegido:
        return protegido
    if not _es_superadmin() and data.get('id_rol'):
        rol = _dao_roles.execute_query_one("SELECT cod_rol FROM roles WHERE id_rol = %s", (data['id_rol'],))
        if rol and rol['cod_rol'] == 'SUPERADMIN':
            return jsonify({'success': False, 'error': 'El rol indicado no es válido.'}), 403

    usuario_existente = usuariodao.getUsuarioById(id_usuario)
    if not usuario_existente:
        return jsonify({
            'success': False,
            'error': 'No se encontró el usuario con el ID proporcionado.'
        }), 404

    if not data.get('username'):
        return jsonify({
            'success': False,
            'error': msg_obligatorio('Username')
        }), 400

    reactivando = not usuario_existente['est_usuario'] and data.get('est_usuario', True)
    if (reactivando and usuario_existente['id_funcionario']
            and usuariodao.contar_usuarios_activos_con_funcionario() >= _tope_usuarios()):
        return jsonify({
            'success': False,
            'error': _mensaje_tope_usuarios()
        }), 400

    password = data.get('password')
    if password:
        password_valida, mensaje_password = validar_politica_password(
            password, username=data.get('username')
        )
        if not password_valida:
            return jsonify({
                'success': False,
                'error': mensaje_password
            }), 400
        if password != data.get('password_confirmacion'):
            return jsonify({
                'success': False,
                'error': 'Las contraseñas no coinciden.'
            }), 400

    try:
        resultado = usuariodao.updateUsuario(
            id_usuario=id_usuario,
            username=data['username'],
            est_usuario=data.get('est_usuario', True),
            password=password,
            usuario_modificacion=session.get('id_usuario')
        )

        if resultado:
            id_rol_nuevo = data.get('id_rol')
            if id_rol_nuevo:
                rol_actual = usuariodao.obtener_rol_principal(id_usuario)
                if not rol_actual or rol_actual['id_rol'] != id_rol_nuevo:
                    if not usuariodao.cambiar_rol_principal(id_usuario, id_rol_nuevo, session.get('id_usuario')):
                        usuariodao.asignar_rol_usuario(id_usuario, id_rol_nuevo, es_principal=True, usuario_creacion=session.get('id_usuario'))

            AuditoriaDao().registrar_evento(
                id_usuario=session.get('id_usuario'),
                accion=AuditAccion.RECORD_UPDATE,
                detalle=f"Edición de usuario \"{data['username']}\" (id_usuario={id_usuario})",
                ip_origen=request.remote_addr
            )
            if password:
                AuditoriaDao().registrar_evento(
                    id_usuario=session.get('id_usuario'),
                    accion=AuditAccion.PASSWORD_CHANGE,
                    detalle=f"Cambio de contraseña de usuario \"{data['username']}\" (id_usuario={id_usuario}) por administrador",
                    ip_origen=request.remote_addr
                )

            return jsonify({
                'success': True,
                'data': {
                    'id_usuario': id_usuario,
                    'mensaje': 'Usuario actualizado exitosamente'
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el usuario. Verifique que el username no esté en uso.'
            }), 400

    except Exception as e:
        app.logger.error(f"Error al actualizar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500


# ============================================
# DESACTIVAR USUARIO (SOFT DELETE)
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarUsuario(id_usuario):
    """Desactiva un usuario (soft delete) - Administrador o Superadministrador (el Administrador no toca al Superadmin)"""
    usuariodao = UsuarioDao()
    protegido = _protegido_de_soporte(id_usuario)
    if protegido:
        return protegido
    if id_usuario == session.get('id_usuario'):
        return jsonify({'success': False, 'error': 'No puede desactivar su propio usuario.'}), 400

    try:
        if usuariodao.desactivarUsuario(id_usuario, session.get('id_usuario')):
            AuditoriaDao().registrar_evento(
                id_usuario=session.get('id_usuario'),
                accion=AuditAccion.RECORD_DELETE,
                detalle=f"Baja de usuario (id_usuario={id_usuario})",
                ip_origen=request.remote_addr
            )
            return jsonify({
                'success': True,
                'mensaje': f'Usuario {id_usuario} desactivado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado o no se pudo desactivar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al desactivar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# RESETEAR INTENTOS DE LOGIN
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>/resetear-intentos', methods=['PATCH'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def resetearIntentos(id_usuario):
    """Resetea el contador de intentos fallidos de login"""
    usuariodao = UsuarioDao()
    protegido = _protegido_de_soporte(id_usuario)
    if protegido:
        return protegido

    try:
        if usuariodao.resetearIntentos(id_usuario, session.get('id_usuario')):
            AuditoriaDao().registrar_evento(
                id_usuario=session.get('id_usuario'),
                accion=AuditAccion.ACCOUNT_UNLOCKED,
                detalle=f"Cuenta id_usuario={id_usuario} desbloqueada (intentos reseteados) desde Usuarios por \"{session.get('usu_nick')}\"",
                ip_origen=request.remote_addr
            )
            return jsonify({
                'success': True,
                'mensaje': f'Intentos reseteados para usuario {id_usuario}.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo resetear los intentos.'
            }), 400

    except Exception as e:
        app.logger.error(f"Error al resetear intentos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
