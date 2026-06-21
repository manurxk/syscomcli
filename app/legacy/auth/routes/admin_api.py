"""
API endpoints para administración de autenticación
FASE 2: MEJORAS DE SEGURIDAD
"""
from flask import Blueprint, request, jsonify, session, current_app as app
from app.auth.services.auth_service import AuthService
from app.auth.dao.auth_dao import AuthDao
from app.auth.utils.decorators import role_required
from app.conexion.Conexion import Conexion
from werkzeug.security import generate_password_hash
import secrets

adminauthapi = Blueprint('admin_auth', __name__, url_prefix='/api/v1/admin/auth')


@adminauthapi.route('/usuarios/<int:id_usuario>/desbloquear', methods=['POST'])
@role_required('Administrador')  # Solo administradores
def desbloquear_usuario(id_usuario):
    """
    Desbloquea un usuario
    """
    try:
        sql = """
            UPDATE usuarios 
            SET fecha_bloqueo = NULL, 
                motivo_bloqueo = NULL, 
                bloqueado_hasta = NULL,
                usu_nro_intentos = 0
            WHERE id_usuario = %s
            RETURNING usu_nick
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_usuario,))
            row = cur.fetchone()
            
            if row:
                con.commit()
                app.logger.info(f"Usuario {row[0]} desbloqueado por admin {session.get('usu_nick')}")
                return jsonify({
                    'success': True,
                    'message': f'Usuario {row[0]} desbloqueado exitosamente'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Usuario no encontrado'
                }), 404
                
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al desbloquear usuario: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al desbloquear usuario: {str(e)}'
            }), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error en desbloquear_usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/usuarios/<int:id_usuario>/resetear-password', methods=['POST'])
@role_required('Administrador')  # Solo administradores
def resetear_password_admin(id_usuario):
    """
    Resetea la contraseña de un usuario (admin)
    Genera una contraseña temporal y marca requiere_cambio_password = TRUE
    """
    try:
        data = request.get_json() or {}
        enviar_email = data.get('enviar_email', False)
        
        # Generar password temporal
        password_temporal = secrets.token_urlsafe(12)  # 16 caracteres aleatorios
        # Generar hash usando pbkdf2:sha256 para mantener consistencia
        password_hash = generate_password_hash(password_temporal, method='pbkdf2:sha256')
        
        sql = """
            UPDATE usuarios 
            SET usu_clave = %s,
                requiere_cambio_password = TRUE,
                fecha_cambio_password = CURRENT_TIMESTAMP,
                usu_nro_intentos = 0,
                fecha_bloqueo = NULL,
                motivo_bloqueo = NULL,
                bloqueado_hasta = NULL
            WHERE id_usuario = %s
            RETURNING usu_nick
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (password_hash, id_usuario))
            row = cur.fetchone()
            
            if row:
                # Cerrar todas las sesiones del usuario
                sql_sesiones = """
                    UPDATE sesiones
                    SET sesion_activa = FALSE,
                        fecha_cierre = CURRENT_TIMESTAMP,
                        tipo_cierre = 'admin_force'
                    WHERE id_usuario = %s AND sesion_activa = TRUE
                """
                cur.execute(sql_sesiones, (id_usuario,))
                
                con.commit()
                
                # Aquí enviarías el email con la contraseña temporal
                # if enviar_email:
                #     enviar_email_password_temporal(email, password_temporal)
                
                app.logger.info(f"Password reseteado por admin para usuario {row[0]}")
                
                return jsonify({
                    'success': True,
                    'data': {
                        'password_temporal': password_temporal,  # Solo para desarrollo
                        'mensaje': 'Contraseña reseteada. El usuario debe cambiarla en el próximo login'
                    },
                    'message': f'Contraseña reseteada para usuario {row[0]}'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Usuario no encontrado'
                }), 404
                
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al resetear password: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al resetear contraseña: {str(e)}'
            }), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error en resetear_password_admin: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/sesiones-activas', methods=['GET'])
@role_required('Administrador')  # Solo administradores
def listar_sesiones_activas():
    """
    Lista todas las sesiones activas
    """
    try:
        sql = """
            SELECT * FROM v_sesiones_activas
            ORDER BY ultima_actividad DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            
            # Obtener nombres de columnas
            columnas = [desc[0] for desc in cur.description]
            
            sesiones = []
            for row in rows:
                sesion = {}
                for i, col in enumerate(columnas):
                    valor = row[i]
                    if hasattr(valor, 'isoformat'):
                        valor = valor.isoformat()
                    sesion[col] = valor
                sesiones.append(sesion)
            
            return jsonify({
                'success': True,
                'data': sesiones,
                'total': len(sesiones)
            }), 200
            
        except Exception as e:
            app.logger.error(f"Error al listar sesiones: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al listar sesiones: {str(e)}'
            }), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error en listar_sesiones_activas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/sesiones/<int:id_sesion>', methods=['DELETE'])
@role_required('Administrador')  # Solo administradores
def cerrar_sesion_remota(id_sesion):
    """
    Cierra una sesión remotamente
    """
    try:
        # Obtener token de sesión
        sql = "SELECT token_sesion FROM sesiones WHERE id_sesion = %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_sesion,))
            row = cur.fetchone()
            
            if row:
                token_sesion = row[0]
                
                # Cerrar sesión usando función PostgreSQL
                exitoso = AuthService.cerrar_sesion(token_sesion, tipo_cierre='admin_force')
                
                if exitoso:
                    app.logger.info(f"Sesión {id_sesion} cerrada remotamente por admin {session.get('usu_nick')}")
                    return jsonify({
                        'success': True,
                        'message': 'Sesión cerrada exitosamente'
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'error': 'No se pudo cerrar la sesión'
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'error': 'Sesión no encontrada'
                }), 404
                
        except Exception as e:
            app.logger.error(f"Error al cerrar sesión remota: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al cerrar sesión: {str(e)}'
            }), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error en cerrar_sesion_remota: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/intentos-login', methods=['GET'])
@role_required('Administrador')  # Solo administradores
def listar_intentos_login():
    """
    Lista los intentos de login (últimos 50 por defecto)
    
    Query params:
        - usuario: filtrar por usuario
        - limit: límite de resultados (default 50)
        - exitoso: filtrar por éxito (true/false)
    """
    try:
        usuario_filtro = request.args.get('usuario')
        limit = int(request.args.get('limit', 50))
        exitoso_filtro = request.args.get('exitoso')
        
        sql = """
            SELECT 
                id_attempt, usuario_intentado, id_usuario, exitoso, motivo_fallo,
                fecha_intento, ip_address, user_agent, csrf_valido
            FROM login_attempts
            WHERE 1=1
        """
        params = []
        
        if usuario_filtro:
            sql += " AND usuario_intentado ILIKE %s"
            params.append(f'%{usuario_filtro}%')
        
        if exitoso_filtro is not None:
            sql += " AND exitoso = %s"
            params.append(exitoso_filtro.lower() == 'true')
        
        sql += " ORDER BY fecha_intento DESC LIMIT %s"
        params.append(limit)
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, params)
            rows = cur.fetchall()
            
            intentos = []
            for row in rows:
                intentos.append({
                    'id_attempt': row[0],
                    'usuario_intentado': row[1],
                    'id_usuario': row[2],
                    'exitoso': row[3],
                    'motivo_fallo': row[4],
                    'fecha_intento': row[5].isoformat() if row[5] else None,
                    'ip_address': row[6],
                    'user_agent': row[7],
                    'csrf_valido': row[8]
                })
            
            return jsonify({
                'success': True,
                'data': intentos,
                'total': len(intentos)
            }), 200
            
        except Exception as e:
            app.logger.error(f"Error al listar intentos login: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al listar intentos: {str(e)}'
            }), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error en listar_intentos_login: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

