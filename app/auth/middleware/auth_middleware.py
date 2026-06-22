"""
Middleware mejorado de autenticación
FASE 2: MEJORAS DE SEGURIDAD
"""
from flask import request, session, g, current_app as app
from app.core.base_dao import BaseDAO

_dao = BaseDAO(db_name_env="DB_NAME_NUEVA")


def verificar_sesion_mejorada():
    """
    Middleware mejorado para verificar sesión activa
    
    Verifica:
    1. Session token existe
    2. Sesión está activa en BD
    3. Sesión no expiró
    4. Actualiza fecha_ultimo_ping
    5. Carga usuario y permisos en g.user
    """
    # Endpoints públicos (no requieren autenticación)
    public_endpoints = {
        "login.login",
        "login.logout",
        "static",
        "informacion.privacidad",
        "informacion.soporte",
        "informacion.contacto",
        "auth.login",  # Nuevo endpoint API
        "auth.solicitar_recuperacion",  # Recuperación de password
        "auth.confirmar_recuperacion"  # Confirmar recuperación
    }
    
    # Si es endpoint público, continuar
    if request.endpoint in public_endpoints or request.endpoint is None:
        return None
    
    # Permitir archivos estáticos
    if request.path.startswith("/static"):
        return None
    
    # Obtener session token
    session_token = session.get('session_token') or request.headers.get('X-Session-Token')
    
    if not session_token:
        # Fallback a sesión Flask tradicional (compatibilidad hacia atrás)
        if 'usu_nick' in session:
            # Cargar usuario básico en g.user
            g.user = {
                'id_usuario': session.get('id_usuario'),
                'usu_nick': session.get('usu_nick'),
                'nombre_persona': session.get('nombre_persona'),
                'grupo': session.get('grupo'),
                'roles': session.get('roles', [])
            }
            return None
        else:
            # Redirigir a login si es request HTML, o retornar 401 si es API
            if request.path.startswith('/api/'):
                from flask import jsonify
                return jsonify({
                    'success': False,
                    'error': 'No autenticado'
                }), 401
            else:
                from flask import redirect, url_for
                return redirect(url_for('login.login'))
    
    # Verificar sesión en BD
    sql = """
        SELECT
            s.id_sesion, s.id_usuario, s.fecha_expiracion, s.est_sesion,
            u.usu_nick, u.est_usuario,
            CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
            rp.cod_rol AS rol_principal,
            COALESCE(
                ARRAY_AGG(r.cod_rol) FILTER (WHERE r.cod_rol IS NOT NULL),
                ARRAY[]::VARCHAR[]
            ) AS roles
        FROM sesiones s
        INNER JOIN usuarios u ON u.id_usuario = s.id_usuario
        LEFT JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
        LEFT JOIN personas p ON p.id_persona = f.id_persona
        LEFT JOIN usuarios_roles ur ON ur.id_usuario = u.id_usuario AND ur.est_usuario_rol = TRUE
        LEFT JOIN roles r ON r.id_rol = ur.id_rol
        LEFT JOIN usuarios_roles ur_p ON ur_p.id_usuario = u.id_usuario AND ur_p.es_rol_principal = TRUE
        LEFT JOIN roles rp ON rp.id_rol = ur_p.id_rol
        WHERE s.token_sesion = %s
          AND s.est_sesion = TRUE
          AND s.fecha_expiracion > CURRENT_TIMESTAMP
        GROUP BY s.id_sesion, s.id_usuario, s.fecha_expiracion, s.est_sesion,
                 u.usu_nick, u.est_usuario, p.per_nombre, p.per_apellido, rp.cod_rol
    """
    
    try:
        sesion_data = _dao.execute_query_one(sql, (session_token,))

        if not sesion_data:
            # Sesión inválida o expirada
            session.clear()
            if request.path.startswith('/api/'):
                from flask import jsonify
                return jsonify({
                    'success': False,
                    'error': 'Sesión expirada o inválida'
                }), 401
            else:
                from flask import redirect, url_for, flash
                flash('Su sesión ha expirado', 'warning')
                return redirect(url_for('login.login'))

        # Verificar usuario activo
        if not sesion_data['est_usuario']:
            session.clear()
            if request.path.startswith('/api/'):
                from flask import jsonify
                return jsonify({
                    'success': False,
                    'error': 'Usuario inactivo'
                }), 403
            else:
                from flask import redirect, url_for, flash
                flash('Usuario inactivo', 'danger')
                return redirect(url_for('login.login'))

        # Actualizar fecha_ultimo_ping
        sql_ping = """
            UPDATE sesiones
            SET fecha_ultimo_ping = CURRENT_TIMESTAMP
            WHERE id_sesion = %s
        """
        _dao.execute_query(sql_ping, (sesion_data['id_sesion'],), commit=True)

        roles = list(sesion_data['roles'] or [])

        # Cargar usuario en g.user
        g.user = {
            'id_usuario': sesion_data['id_usuario'],
            'usu_nick': sesion_data['usu_nick'],
            'nombre_persona': sesion_data['nombre_completo'],
            'grupo': sesion_data['rol_principal'],
            'roles': roles,
            'sesion_id': sesion_data['id_sesion']
        }

        # Actualizar sesión Flask (compatibilidad)
        session['id_usuario'] = sesion_data['id_usuario']
        session['usu_nick'] = sesion_data['usu_nick']
        session['nombre_persona'] = sesion_data['nombre_completo']
        session['grupo'] = sesion_data['rol_principal']
        session['roles'] = roles
        session['session_token'] = session_token

        return None

    except Exception as e:
        app.logger.error(f"Error en middleware autenticación: {str(e)}")
        # En caso de error, permitir continuar con sesión Flask tradicional
        if 'usu_nick' in session:
            g.user = {
                'id_usuario': session.get('id_usuario'),
                'usu_nick': session.get('usu_nick'),
                'nombre_persona': session.get('nombre_persona'),
                'grupo': session.get('grupo'),
                'roles': session.get('roles', [])
            }
            return None
        else:
            if request.path.startswith('/api/'):
                from flask import jsonify
                return jsonify({
                    'success': False,
                    'error': 'Error de autenticación'
                }), 500
            else:
                from flask import redirect, url_for
                return redirect(url_for('login.login'))


