"""
API endpoints para autenticación mejorada
FASE 2: MEJORAS DE SEGURIDAD
"""
from flask import Blueprint, request, jsonify, session, current_app as app
from app.auth.services.auth_service import AuthService
from app.dao.auth.auth_dao import AuthDao
from app.auth.utils.password_validator import validar_politica_password
from app.auth.utils.decorators import role_required

authapi = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@authapi.route('/login', methods=['POST'])
def login():
    """
    Endpoint de login mejorado
    
    Body:
        {
            "username": "usuario",
            "password": "contraseña",
            "csrf_token": "token_csrf" (opcional)
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos no proporcionados'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        csrf_token = data.get('csrf_token')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Usuario y contraseña son requeridos'
            }), 400
        
        # Llamar al servicio de autenticación
        exitoso, datos_usuario, mensaje = AuthService.login(
            usuario_nombre=username,
            password=password,
            csrf_token=csrf_token
        )
        
        if exitoso:
            # Guardar en sesión Flask (compatibilidad hacia atrás)
            session.clear()
            session.permanent = True
            session['id_usuario'] = datos_usuario['id_usuario']
            session['usu_nick'] = datos_usuario['usu_nick']
            session['nombre_persona'] = datos_usuario['nombre_completo']
            session['grupo'] = datos_usuario['grupo']
            session['roles'] = datos_usuario.get('roles', [])
            session['session_token'] = datos_usuario['session_token']

            return jsonify({
                'success': True,
                'data': {
                    'usuario': {
                        'id_usuario': datos_usuario['id_usuario'],
                        'usu_nick': datos_usuario['usu_nick'],
                        'nombre_completo': datos_usuario['nombre_completo'],
                        'grupo': datos_usuario['grupo'],
                        'roles': datos_usuario.get('roles', [])
                    },
                    'session_token': datos_usuario['session_token'],
                    'csrf_token': datos_usuario['csrf_token'],
                    'advertencias': datos_usuario.get('advertencias', {})
                },
                'message': mensaje
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': mensaje,
                'requiere_cambio_password': 'requiere_cambio_password' in datos_usuario if datos_usuario else False
            }), 401
            
    except Exception as e:
        app.logger.error(f"Error en login: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@authapi.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint de logout mejorado
    """
    try:
        session_token = session.get('session_token') or request.headers.get('X-Session-Token')
        
        if session_token:
            AuthService.cerrar_sesion(session_token, tipo_cierre='LOGOUT')
        
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Sesión cerrada exitosamente'
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error en logout: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al cerrar sesión'
        }), 500


@authapi.route('/cambiar-password', methods=['POST'])
@role_required()  # Requiere estar autenticado
def cambiar_password():
    """
    Endpoint para cambiar contraseña
    
    Body:
        {
            "password_actual": "contraseña_actual",
            "password_nueva": "contraseña_nueva"
        }
    """
    try:
        id_usuario = session.get('id_usuario')
        
        if not id_usuario:
            return jsonify({
                'success': False,
                'error': 'Debe estar autenticado'
            }), 401
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos no proporcionados'
            }), 400
        
        password_actual = data.get('password_actual')
        password_nueva = data.get('password_nueva')
        
        if not password_actual or not password_nueva:
            return jsonify({
                'success': False,
                'error': 'Contraseña actual y nueva son requeridas'
            }), 400
        
        # Obtener datos del usuario
        usuario = AuthService.buscar_usuario_seguridad(session.get('usu_nick'))
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Validar política de nueva contraseña
        valido, mensaje = validar_politica_password(
            password=password_nueva,
            usuario_data=usuario,
            username=usuario['usu_nick']
        )
        
        if not valido:
            return jsonify({
                'success': False,
                'error': mensaje
            }), 400
        
        # Cambiar contraseña
        exitoso, mensaje = AuthDao().cambiar_password(
            id_usuario=id_usuario,
            password_actual=password_actual,
            password_nueva=password_nueva,
            password_hash_actual=usuario['usu_clave']
        )

        if exitoso:
            # Cerrar todas las sesiones excepto la actual
            session_token = session.get('session_token')
            if session_token:
                from app.core.base_dao import BaseDAO
                sql = """
                    UPDATE sesiones
                    SET est_sesion = FALSE,
                        fecha_cierre = CURRENT_TIMESTAMP,
                        tipo_cierre = 'SECURITY'
                    WHERE id_usuario = %s AND token_sesion != %s AND est_sesion = TRUE
                """
                BaseDAO(db_name_env="DB_NAME_NUEVA").execute_query(sql, (id_usuario, session_token), commit=True)
            
            app.logger.info(f"Password cambiado exitosamente para usuario {id_usuario}")
            return jsonify({
                'success': True,
                'message': mensaje
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': mensaje
            }), 400
            
    except Exception as e:
        app.logger.error(f"Error al cambiar password: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@authapi.route('/recuperar-password', methods=['POST'])
def solicitar_recuperacion():
    """
    Endpoint para solicitar recuperación de contraseña
    
    Body:
        {
            "username": "usuario" o "email": "email@ejemplo.com"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos no proporcionados'
            }), 400
        
        username = data.get('username')
        email = data.get('email')
        
        if not username and not email:
            return jsonify({
                'success': False,
                'error': 'Usuario o email es requerido'
            }), 400
        
        # Buscar usuario
        if username:
            usuario = AuthService.buscar_usuario_seguridad(username)
        else:
            # Buscar por email (necesitarías agregar esta funcionalidad)
            usuario = None
        
        # Por seguridad, siempre retornar el mismo mensaje
        mensaje_generico = "Si el usuario existe, recibirá instrucciones por email"
        
        if not usuario or not usuario.get('est_usuario'):
            return jsonify({
                'success': True,
                'message': mensaje_generico
            }), 200

        # Crear token de recuperación
        ip_solicitud = AuthService.obtener_ip_cliente()

        token = AuthDao().crear_password_reset_token(
            id_usuario=usuario['id_usuario'],
            ip_solicitud=ip_solicitud,
            email_destino=email
        )
        
        if token:
            # Aquí enviarías el email con el link
            # link = f"/reset-password?token={token}"
            # enviar_email(email_destino, link)
            
            app.logger.info(f"Token de recuperación creado para usuario {usuario['usu_nick']}")
            
            return jsonify({
                'success': True,
                'message': mensaje_generico,
                # En producción, no retornar el token
                # 'token': token  # Solo para desarrollo/testing
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Error al generar token de recuperación'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al solicitar recuperación: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@authapi.route('/confirmar-recuperacion', methods=['POST'])
def confirmar_recuperacion():
    """
    Endpoint para confirmar recuperación de contraseña con token
    
    Body:
        {
            "token": "token_uuid",
            "password_nueva": "nueva_contraseña"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos no proporcionados'
            }), 400
        
        token = data.get('token')
        password_nueva = data.get('password_nueva')
        
        if not token or not password_nueva:
            return jsonify({
                'success': False,
                'error': 'Token y nueva contraseña son requeridos'
            }), 400
        
        # Validar token
        token_data = AuthDao().validar_password_reset_token(token)
        if not token_data:
            return jsonify({
                'success': False,
                'error': 'Token inválido o expirado'
            }), 400

        # Obtener datos del usuario a partir del nick (la vista de seguridad busca por usu_nick, no por id)
        from app.core.base_dao import BaseDAO
        fila = BaseDAO(db_name_env="DB_NAME_NUEVA").execute_query_one(
            "SELECT usu_nick FROM usuarios WHERE id_usuario = %s", (token_data['id_usuario'],)
        )
        usuario = AuthService.buscar_usuario_seguridad(fila['usu_nick']) if fila else None

        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Validar política de nueva contraseña
        valido, mensaje = validar_politica_password(
            password=password_nueva,
            usuario_data=usuario,
            username=usuario['usu_nick']
        )
        
        if not valido:
            return jsonify({
                'success': False,
                'error': mensaje
            }), 400
        
        # Resetear contraseña
        exitoso, mensaje = AuthDao().resetear_password_con_token(token, password_nueva)
        
        if exitoso:
            app.logger.info(f"Password reseteado exitosamente con token {token[:8]}...")
            return jsonify({
                'success': True,
                'message': mensaje
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': mensaje
            }), 400
            
    except Exception as e:
        app.logger.error(f"Error al confirmar recuperación: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@authapi.route('/perfil', methods=['GET'])
@role_required()  # Requiere estar autenticado
def obtener_perfil():
    """
    Endpoint para obtener perfil del usuario autenticado
    """
    try:
        id_usuario = session.get('id_usuario')
        usu_nick = session.get('usu_nick')
        
        if not id_usuario or not usu_nick:
            return jsonify({
                'success': False,
                'error': 'Debe estar autenticado'
            }), 401
        
        usuario = AuthService.buscar_usuario_seguridad(usu_nick)
        
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id_usuario': usuario['id_usuario'],
                'usu_nick': usuario['usu_nick'],
                'nombre_completo': usuario['nombre_completo'],
                'grupo': usuario['grupo_nombre'],
                'cargo': usuario.get('cargo_nombre'),
                'fecha_ultimo_login': usuario['fecha_ultimo_login'].isoformat() if usuario['fecha_ultimo_login'] else None,
                'ip_ultimo_login': usuario['ip_ultimo_login'],
                'sesiones_activas': usuario['sesiones_activas'],
                'max_sesiones_simultaneas': usuario['max_sesiones_simultaneas'],
                'password_expirada': usuario['password_expirada'],
                'dias_hasta_expiracion': usuario['dias_hasta_expiracion'],
                'requiere_cambio_password': usuario['requiere_cambio_password']
            }
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener perfil: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


