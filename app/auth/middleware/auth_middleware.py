"""
Middleware mejorado de autenticación
FASE 2: MEJORAS DE SEGURIDAD
"""
from flask import request, session, g, current_app as app
from datetime import datetime
from app.conexion.Conexion import Conexion
from app.auth.services.auth_service import AuthService


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
                'id_grupo': session.get('id_grupo')
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
            s.id_sesion, s.id_usuario, s.fecha_expiracion, s.sesion_activa,
            u.usu_nick, u.usu_estado, u.id_grupo,
            CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
            g.des_grupo AS grupo
        FROM sesiones s
        INNER JOIN usuarios u ON u.id_usuario = s.id_usuario
        LEFT JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
        LEFT JOIN personas p ON p.id_persona = f.id_persona
        LEFT JOIN grupos g ON g.id_grupo = u.id_grupo
        WHERE s.token_sesion = %s 
          AND s.sesion_activa = TRUE
          AND s.fecha_expiracion > CURRENT_TIMESTAMP
    """
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        cur.execute(sql, (session_token,))
        sesion_data = cur.fetchone()
        
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
        if not sesion_data[5]:  # usu_estado
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
        cur.execute(sql_ping, (sesion_data[0],))
        con.commit()
        
        # Cargar usuario en g.user
        g.user = {
            'id_usuario': sesion_data[1],
            'usu_nick': sesion_data[4],
            'nombre_persona': sesion_data[7],
            'grupo': sesion_data[8],
            'id_grupo': sesion_data[6],
            'sesion_id': sesion_data[0]
        }
        
        # Actualizar sesión Flask (compatibilidad)
        session['id_usuario'] = sesion_data[1]
        session['usu_nick'] = sesion_data[4]
        session['nombre_persona'] = sesion_data[7]
        session['grupo'] = sesion_data[8]
        session['id_grupo'] = sesion_data[6]
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
                'id_grupo': session.get('id_grupo')
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
    finally:
        cur.close()
        con.close()


