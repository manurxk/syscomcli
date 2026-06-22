"""
API endpoints para administración de autenticación
FASE 2: MEJORAS DE SEGURIDAD
"""
from flask import Blueprint, request, jsonify, session, current_app as app
from app.auth.services.auth_service import AuthService
from app.dao.auth.auth_dao import AuthDao
from app.auth.utils.decorators import role_required
from app.core.base_dao import BaseDAO
from werkzeug.security import generate_password_hash
import secrets

adminauthapi = Blueprint('admin_auth', __name__, url_prefix='/api/v1/admin/auth')

_dao = BaseDAO(db_name_env="DB_NAME_NUEVA")


@adminauthapi.route('/usuarios/<int:id_usuario>/desbloquear', methods=['POST'])
@role_required('ADMINISTRADOR', 'SUPERADMIN')  # Solo administradores
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
        try:
            row = _dao.execute_query_one(sql, (id_usuario,), commit=True)

            if row:
                app.logger.info(f"Usuario {row['usu_nick']} desbloqueado por admin {session.get('usu_nick')}")
                return jsonify({
                    'success': True,
                    'message': f"Usuario {row['usu_nick']} desbloqueado exitosamente"
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Usuario no encontrado'
                }), 404

        except Exception as e:
            app.logger.error(f"Error al desbloquear usuario: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al desbloquear usuario: {str(e)}'
            }), 500

    except Exception as e:
        app.logger.error(f"Error en desbloquear_usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/usuarios/<int:id_usuario>/resetear-password', methods=['POST'])
@role_required('ADMINISTRADOR', 'SUPERADMIN')  # Solo administradores
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
                requiere_cambio_clave = TRUE,
                fecha_cambio_clave = CURRENT_TIMESTAMP,
                usu_nro_intentos = 0,
                fecha_bloqueo = NULL,
                motivo_bloqueo = NULL,
                bloqueado_hasta = NULL
            WHERE id_usuario = %s
            RETURNING usu_nick
        """

        try:
            row = _dao.execute_query_one(sql, (password_hash, id_usuario), commit=True)

            if row:
                sql_sesiones = """
                    UPDATE sesiones
                    SET est_sesion = FALSE,
                        fecha_cierre = CURRENT_TIMESTAMP,
                        tipo_cierre = 'ADMIN_FORCE'
                    WHERE id_usuario = %s AND est_sesion = TRUE
                """
                _dao.execute_query(sql_sesiones, (id_usuario,), commit=True)

                # Aquí enviarías el email con la contraseña temporal
                # if enviar_email:
                #     enviar_email_password_temporal(email, password_temporal)

                app.logger.info(f"Password reseteado por admin para usuario {row['usu_nick']}")

                return jsonify({
                    'success': True,
                    'data': {
                        'password_temporal': password_temporal,  # Solo para desarrollo
                        'mensaje': 'Contraseña reseteada. El usuario debe cambiarla en el próximo login'
                    },
                    'message': f"Contraseña reseteada para usuario {row['usu_nick']}"
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Usuario no encontrado'
                }), 404

        except Exception as e:
            app.logger.error(f"Error al resetear password: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al resetear contraseña: {str(e)}'
            }), 500

    except Exception as e:
        app.logger.error(f"Error en resetear_password_admin: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/sesiones-activas', methods=['GET'])
@role_required('ADMINISTRADOR', 'SUPERADMIN')  # Solo administradores
def listar_sesiones_activas():
    """
    Lista todas las sesiones activas
    """
    try:
        sql = """
            SELECT * FROM v_sesiones_activas
            ORDER BY ultima_actividad DESC
        """
        
        try:
            filas = _dao.execute_query(sql)

            sesiones = []
            for fila in filas:
                sesion = {col: (valor.isoformat() if hasattr(valor, 'isoformat') else valor) for col, valor in fila.items()}
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

    except Exception as e:
        app.logger.error(f"Error en listar_sesiones_activas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/sesiones/<int:id_sesion>', methods=['DELETE'])
@role_required('ADMINISTRADOR', 'SUPERADMIN')  # Solo administradores
def cerrar_sesion_remota(id_sesion):
    """
    Cierra una sesión remotamente
    """
    try:
        # Obtener token de sesión
        sql = "SELECT token_sesion FROM sesiones WHERE id_sesion = %s"

        try:
            row = _dao.execute_query_one(sql, (id_sesion,))

            if row:
                token_sesion = row['token_sesion']

                # Cerrar sesión usando función PostgreSQL
                exitoso = AuthService.cerrar_sesion(token_sesion, tipo_cierre='ADMIN_FORCE')

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

    except Exception as e:
        app.logger.error(f"Error en cerrar_sesion_remota: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@adminauthapi.route('/intentos-login', methods=['GET'])
@role_required('ADMINISTRADOR', 'SUPERADMIN')  # Solo administradores
def listar_intentos_login():
    """
    Lista los intentos de login (últimos 50 por defecto)

    Query params:
        - usuario: filtrar por usuario
        - limit: límite de resultados (default 50)
        - resultado: filtrar por resultado exacto (EXITOSO, FALLIDO_CLAVE, FALLIDO_BLOQUEADO, FALLIDO_USUARIO_INEXISTENTE, FALLIDO_SESIONES_MAXIMAS)
    """
    try:
        usuario_filtro = request.args.get('usuario')
        limit = int(request.args.get('limit', 50))
        resultado_filtro = request.args.get('resultado')

        sql = """
            SELECT
                id_acceso, usuario_intentado, id_usuario, resultado,
                fecha_intento, ip_origen, user_agent, csrf_valido
            FROM accesos_sistema
            WHERE 1=1
        """
        params = []

        if usuario_filtro:
            sql += " AND usuario_intentado ILIKE %s"
            params.append(f'%{usuario_filtro}%')

        if resultado_filtro:
            sql += " AND resultado = %s"
            params.append(resultado_filtro.upper())

        sql += " ORDER BY fecha_intento DESC LIMIT %s"
        params.append(limit)

        try:
            filas = _dao.execute_query(sql, params)

            intentos = []
            for fila in filas:
                intentos.append({
                    'id_acceso': fila['id_acceso'],
                    'usuario_intentado': fila['usuario_intentado'],
                    'id_usuario': fila['id_usuario'],
                    'resultado': fila['resultado'],
                    'fecha_intento': fila['fecha_intento'].isoformat() if fila['fecha_intento'] else None,
                    'ip_origen': str(fila['ip_origen']) if fila['ip_origen'] else None,
                    'user_agent': fila['user_agent'],
                    'csrf_valido': fila['csrf_valido']
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

    except Exception as e:
        app.logger.error(f"Error en listar_intentos_login: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

