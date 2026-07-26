"""
Servicio de autenticación mejorado
FASE 2: MEJORAS DE SEGURIDAD
"""
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from flask import current_app as app, request
from werkzeug.security import check_password_hash
from app.core.base_dao import BaseDAO
from app.services.EmailService import EmailService

_dao = BaseDAO(db_name_env="DB_NAME_NUEVA")

MFA_MAX_INTENTOS_VALIDACION = 5


class AuthService:
    """Servicio centralizado para autenticación y gestión de sesiones"""

    @staticmethod
    def obtener_ip_cliente() -> str:
        """Obtiene la IP del cliente desde el request"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return request.remote_addr or '0.0.0.0'

    @staticmethod
    def obtener_user_agent() -> str:
        """Obtiene el User-Agent del cliente"""
        return request.headers.get('User-Agent', 'Unknown')

    @staticmethod
    def buscar_usuario_seguridad(usu_nick: str) -> Optional[Dict]:
        """
        Busca usuario usando la vista v_usuarios_seguridad
        Retorna información completa de seguridad
        """
        sql = """
            SELECT
                id_usuario, usu_nick, usu_clave, est_usuario, id_funcionario, id_rol,
                nombre_completo, grupo_nombre, cargo_nombre,
                fecha_ultimo_login, ip_ultimo_login, fecha_bloqueo, bloqueado_hasta,
                motivo_bloqueo, requiere_cambio_clave, fecha_cambio_clave,
                clave_nunca_expira, dias_validez_clave, max_sesiones_simultaneas,
                sesiones_activas, password_expirada, dias_hasta_expiracion, esta_bloqueado,
                mfa_habilitado, correo
            FROM v_usuarios_seguridad
            WHERE usu_nick = %s
        """
        try:
            fila = _dao.execute_query_one(sql, (usu_nick,))
            if not fila:
                return None
            return {
                'id_usuario': fila['id_usuario'],
                'usu_nick': fila['usu_nick'],
                'usu_clave': fila['usu_clave'],
                'usu_estado': fila['est_usuario'],
                'id_funcionario': fila['id_funcionario'],
                'id_grupo': fila['id_rol'],
                'nombre_completo': fila['nombre_completo'],
                'grupo_nombre': fila['grupo_nombre'],
                'cargo_nombre': fila['cargo_nombre'],
                'fecha_ultimo_login': fila['fecha_ultimo_login'],
                'ip_ultimo_login': fila['ip_ultimo_login'],
                'fecha_bloqueo': fila['fecha_bloqueo'],
                'bloqueado_hasta': fila['bloqueado_hasta'],
                'motivo_bloqueo': fila['motivo_bloqueo'],
                'requiere_cambio_password': fila['requiere_cambio_clave'],
                'fecha_cambio_password': fila['fecha_cambio_clave'],
                'password_nunca_expira': fila['clave_nunca_expira'],
                'dias_validez_password': fila['dias_validez_clave'],
                'max_sesiones_simultaneas': fila['max_sesiones_simultaneas'],
                'sesiones_activas': fila['sesiones_activas'],
                'password_expirada': fila['password_expirada'],
                'dias_hasta_expiracion': fila['dias_hasta_expiracion'],
                'esta_bloqueado': fila['esta_bloqueado'],
                'mfa_habilitado': fila['mfa_habilitado'],
                'correo': fila['correo']
            }
        except Exception as e:
            app.logger.error(f"Error al buscar usuario seguridad: {str(e)}")
            return None

    @staticmethod
    def obtener_roles_usuario(id_usuario: int) -> list:
        """Devuelve los códigos de rol activos de un usuario (multi-rol)."""
        sql = """
            SELECT r.cod_rol
            FROM usuarios_roles ur
            INNER JOIN roles r ON r.id_rol = ur.id_rol
            WHERE ur.id_usuario = %s AND ur.est_usuario_rol = TRUE
            ORDER BY ur.es_rol_principal DESC
        """
        try:
            filas = _dao.execute_query(sql, (id_usuario,))
            return [f['cod_rol'] for f in filas]
        except Exception as e:
            app.logger.error(f"Error al obtener roles de usuario: {str(e)}")
            return []

    @staticmethod
    def esta_usuario_bloqueado(id_usuario: int) -> bool:
        """Verifica si un usuario está bloqueado usando función PostgreSQL"""
        try:
            fila = _dao.execute_query_one("SELECT esta_usuario_bloqueado(%s) AS bloqueado", (id_usuario,))
            return bool(fila['bloqueado']) if fila else False
        except Exception as e:
            app.logger.error(f"Error al verificar bloqueo: {str(e)}")
            return False

    @staticmethod
    def registrar_intento_login(
        usuario_intentado: str,
        id_usuario: Optional[int],
        exitoso: bool,
        motivo_fallo: Optional[str],
        ip_address: str,
        user_agent: str,
        csrf_valido: Optional[bool] = None
    ) -> Optional[int]:
        """
        Registra un intento de login usando función PostgreSQL
        Retorna el ID del intento registrado
        """
        sql = "SELECT registrar_intento_login(%s, %s, %s, %s, %s, %s, %s) AS id_acceso"
        try:
            fila = _dao.execute_query_one(
                sql,
                (usuario_intentado, id_usuario, exitoso, motivo_fallo, ip_address, user_agent, csrf_valido),
                commit=True
            )
            return fila['id_acceso'] if fila else None
        except Exception as e:
            app.logger.error(f"Error al registrar intento login: {str(e)}")
            return None

    @staticmethod
    def crear_sesion(
        id_usuario: int,
        token_sesion: str,
        csrf_token: str,
        refresh_token: Optional[str],
        fecha_expiracion: datetime,
        ip_address: str,
        user_agent: str
    ) -> Optional[int]:
        """
        Crea una nueva sesión usando función PostgreSQL
        Retorna el ID de la sesión creada
        """
        sql = "SELECT crear_sesion(%s, %s, %s, %s, %s, %s, %s) AS id_sesion"
        try:
            fila = _dao.execute_query_one(
                sql,
                (id_usuario, token_sesion, csrf_token, refresh_token, fecha_expiracion, ip_address, user_agent),
                commit=True
            )
            return fila['id_sesion'] if fila else None
        except Exception as e:
            app.logger.error(f"Error al crear sesión: {str(e)}")
            return None

    @staticmethod
    def cerrar_sesion(token_sesion: str, tipo_cierre: str = 'LOGOUT') -> bool:
        """
        Cierra una sesión usando función PostgreSQL
        """
        sql = "SELECT cerrar_sesion(%s, %s) AS resultado"
        try:
            fila = _dao.execute_query_one(sql, (token_sesion, tipo_cierre), commit=True)
            return bool(fila['resultado']) if fila else False
        except Exception as e:
            app.logger.error(f"Error al cerrar sesión: {str(e)}")
            return False

    @staticmethod
    def contar_intentos_fallidos_ip(ip_address: str, minutos: int = 15) -> int:
        """Cuenta intentos de login fallidos desde una IP en una ventana de tiempo"""
        sql = """
            SELECT COUNT(*) AS total
            FROM accesos_sistema
            WHERE ip_origen = %s::inet
              AND resultado != 'EXITOSO'
              AND fecha_intento > CURRENT_TIMESTAMP - (%s || ' minutes')::interval
        """
        try:
            fila = _dao.execute_query_one(sql, (ip_address, minutos))
            return fila['total'] if fila else 0
        except Exception as e:
            app.logger.error(f"Error al contar intentos fallidos por IP: {str(e)}")
            return 0

    @staticmethod
    def login(
        usuario_nombre: str,
        password: str,
        csrf_token: Optional[str] = None
    ) -> Tuple[bool, Dict, str]:
        """
        Proceso de login mejorado con todas las validaciones

        Returns:
            Tuple[bool, Dict, str]: (exitoso, datos_usuario, mensaje)
        """
        ip_address = AuthService.obtener_ip_cliente()
        user_agent = AuthService.obtener_user_agent()

        # 0. Rate limiting por IP - protege contra fuerza bruta distribuida entre usuarios
        MAX_INTENTOS_FALLIDOS_IP = 10
        VENTANA_MINUTOS_IP = 15
        if AuthService.contar_intentos_fallidos_ip(ip_address, VENTANA_MINUTOS_IP) >= MAX_INTENTOS_FALLIDOS_IP:
            app.logger.warning(f"LOGIN_BLOCKED_IP ip={ip_address} reason=demasiados_intentos")
            return False, {}, "Demasiados intentos fallidos desde esta IP. Intente nuevamente más tarde."

        # 1. Buscar usuario en vista de seguridad
        usuario = AuthService.buscar_usuario_seguridad(usuario_nombre)

        if not usuario:
            # Usuario no existe - registrar intento fallido
            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=None,
                exitoso=False,
                motivo_fallo='usuario_no_existe',
                ip_address=ip_address,
                user_agent=user_agent,
                csrf_valido=None
            )
            app.logger.warning(f"LOGIN_FAIL user={usuario_nombre} reason=usuario_no_existe ip={ip_address}")
            return False, {}, "Usuario o contraseña incorrectos"

        id_usuario = usuario['id_usuario']

        # 2. Verificar usuario activo
        if not usuario['usu_estado']:
            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=id_usuario,
                exitoso=False,
                motivo_fallo='cuenta_bloqueada',
                ip_address=ip_address,
                user_agent=user_agent
            )
            app.logger.warning(f"LOGIN_FAIL user={usuario_nombre} reason=usuario_inactivo ip={ip_address}")
            return False, {}, "Usuario inactivo"

        # 3. Verificar si está bloqueado
        if usuario.get('esta_bloqueado') or AuthService.esta_usuario_bloqueado(id_usuario):
            bloqueado_hasta = usuario.get('bloqueado_hasta')
            if bloqueado_hasta:
                mensaje = f"Cuenta bloqueada hasta {bloqueado_hasta.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                mensaje = "Cuenta bloqueada. Contacte al administrador"

            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=id_usuario,
                exitoso=False,
                motivo_fallo='cuenta_bloqueada',
                ip_address=ip_address,
                user_agent=user_agent
            )
            app.logger.warning(f"LOGIN_FAIL user={usuario_nombre} reason=cuenta_bloqueada ip={ip_address}")
            return False, {}, mensaje

        # 4. Verificar contraseña
        password_correcta = check_password_hash(usuario['usu_clave'], password)

        if not password_correcta:
            # Contraseña incorrecta - registrar intento fallido
            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=id_usuario,
                exitoso=False,
                motivo_fallo='password_invalido',
                ip_address=ip_address,
                user_agent=user_agent
            )

            # Obtener intentos restantes
            try:
                fila = _dao.execute_query_one("SELECT usu_nro_intentos FROM usuarios WHERE id_usuario = %s", (id_usuario,))
                intentos = (fila['usu_nro_intentos'] if fila else 0) or 0
                intentos_restantes = max(0, 5 - intentos - 1)
            except Exception:
                intentos_restantes = 0

            app.logger.warning(f"LOGIN_FAIL user={usuario_nombre} reason=password_invalido ip={ip_address}")

            if intentos_restantes > 0:
                return False, {}, f"Contraseña incorrecta. Intentos restantes: {intentos_restantes}"
            else:
                return False, {}, "Contraseña incorrecta. Cuenta bloqueada por múltiples intentos fallidos"

        # 5. Verificar si requiere cambio de contraseña (solo si no tiene password_nunca_expira)
        if not usuario.get('password_nunca_expira') and usuario.get('requiere_cambio_password'):
            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=id_usuario,
                exitoso=True,
                motivo_fallo=None,
                ip_address=ip_address,
                user_agent=user_agent
            )
            return False, usuario, "Debe cambiar su contraseña antes de continuar"

        # 6. Verificar si password expirada (solo si no tiene password_nunca_expira)
        if not usuario.get('password_nunca_expira') and usuario.get('password_expirada'):
            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=id_usuario,
                exitoso=True,
                motivo_fallo=None,
                ip_address=ip_address,
                user_agent=user_agent
            )
            return False, usuario, "Su contraseña ha expirado. Debe cambiarla"

        # 7. Si el usuario tiene MFA habilitado, no crear sesión todavía:
        # se envía un código por correo y el login se completa en un segundo paso
        # (ver completar_login_mfa).
        if usuario.get('mfa_habilitado'):
            enviado, error_mfa = AuthService.generar_y_enviar_codigo_mfa(
                id_usuario=id_usuario,
                ip_address=ip_address,
                user_agent=user_agent
            )
            if not enviado:
                app.logger.error(f"Error al enviar código MFA para usuario {usuario_nombre}: {error_mfa}")
                return False, {}, "No se pudo enviar el código de verificación. Intente nuevamente"

            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=id_usuario,
                exitoso=True,
                motivo_fallo=None,
                ip_address=ip_address,
                user_agent=user_agent
            )

            app.logger.info(f"LOGIN_MFA_PENDIENTE user={usuario_nombre} ip={ip_address}")
            return False, {'id_usuario': id_usuario, 'usu_nick': usuario['usu_nick'], 'requiere_mfa': True}, \
                "Se envió un código de verificación a su correo"

        # 8. Sin MFA - crear sesión directamente
        datos_usuario = AuthService._finalizar_sesion(usuario, usuario_nombre, ip_address, user_agent, csrf_token)
        if not datos_usuario:
            return False, {}, "Error al crear sesión. Intente nuevamente"

        return True, datos_usuario, "Login exitoso"

    @staticmethod
    def _finalizar_sesion(usuario, usuario_nombre, ip_address, user_agent, csrf_token=None):
        """
        Crea la sesión, actualiza último login y registra el intento exitoso.
        Compartido por el login sin MFA y por completar_login_mfa().

        Returns:
            Optional[Dict]: datos de usuario listos para la sesión, o None si falló.
        """
        id_usuario = usuario['id_usuario']

        # Generar tokens
        session_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)

        # Obtener CSRF token si no se proporcionó
        if not csrf_token:
            from flask_wtf.csrf import generate_csrf
            csrf_token = generate_csrf()

        # Fecha de expiración (60 minutos por defecto, en UTC para coincidir con CURRENT_TIMESTAMP de PostgreSQL)
        fecha_expiracion = datetime.utcnow() + timedelta(minutes=60)

        # Crear sesión en BD
        sesion_id = AuthService.crear_sesion(
            id_usuario=id_usuario,
            token_sesion=session_token,
            csrf_token=csrf_token,
            refresh_token=refresh_token,
            fecha_expiracion=fecha_expiracion,
            ip_address=ip_address,
            user_agent=user_agent
        )

        if not sesion_id:
            app.logger.error(f"Error al crear sesión para usuario {usuario_nombre}")
            return None

        # Actualizar fecha_ultimo_login
        try:
            sql = """
                UPDATE usuarios
                SET fecha_ultimo_login = CURRENT_TIMESTAMP,
                    ip_ultimo_login = %s,
                    user_agent_ultimo_login = %s
                WHERE id_usuario = %s
            """
            _dao.execute_query(sql, (ip_address, user_agent, id_usuario), commit=True)
        except Exception as e:
            app.logger.error(f"Error al actualizar último login: {str(e)}")

        # Registrar intento exitoso
        AuthService.registrar_intento_login(
            usuario_intentado=usuario_nombre,
            id_usuario=id_usuario,
            exitoso=True,
            motivo_fallo=None,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Preparar datos de respuesta
        datos_usuario = {
            'id_usuario': id_usuario,
            'usu_nick': usuario['usu_nick'],
            'nombre_completo': usuario['nombre_completo'],
            'grupo': usuario['grupo_nombre'],
            'id_grupo': usuario['id_grupo'],
            'roles': AuthService.obtener_roles_usuario(id_usuario),
            'id_funcionario': usuario.get('id_funcionario'),
            'session_token': session_token,
            'csrf_token': csrf_token,
            'refresh_token': refresh_token,
            'sesion_id': sesion_id
        }

        # Advertencias
        advertencias = {}
        if usuario.get('dias_hasta_expiracion') and usuario['dias_hasta_expiracion'] <= 7:
            advertencias['password_expira_en_dias'] = usuario['dias_hasta_expiracion']
        if usuario.get('sesiones_activas', 0) > 0:
            advertencias['sesiones_activas'] = usuario['sesiones_activas']
        if usuario.get('fecha_ultimo_login'):
            advertencias['ultimo_login'] = usuario['fecha_ultimo_login'].strftime('%Y-%m-%d %H:%M:%S')
        if usuario.get('ip_ultimo_login'):
            advertencias['ultimo_login_ip'] = usuario['ip_ultimo_login']

        datos_usuario['advertencias'] = advertencias

        app.logger.info(f"LOGIN_SUCCESS user={usuario_nombre} ip={ip_address} sesion={sesion_id}")

        return datos_usuario

    @staticmethod
    def generar_y_enviar_codigo_mfa(id_usuario, ip_address=None, user_agent=None):
        """Genera un código OTP de 6 dígitos, lo guarda y lo envía por correo."""
        fila = _dao.execute_query_one(
            "SELECT correo FROM v_usuarios_seguridad WHERE id_usuario = %s", (id_usuario,)
        )
        correo = fila['correo'] if fila else None

        ttl_minutos = int(app.config.get('MFA_CODE_TTL_MINUTES', 5))
        codigo = f"{secrets.randbelow(1_000_000):06d}"
        fecha_expiracion = datetime.utcnow() + timedelta(minutes=ttl_minutos)

        exito, error, _tipo_error = EmailService().enviar_codigo_mfa(correo, codigo, ttl_minutos)
        if not exito:
            return False, error

        sql = """
            INSERT INTO mfa_codigos (id_usuario, codigo, fecha_expiracion, ip_solicitud, user_agent)
            VALUES (%s, %s, %s, %s, %s)
        """
        _dao.execute_query(sql, (id_usuario, codigo, fecha_expiracion, ip_address, user_agent), commit=True)
        return True, None

    @staticmethod
    def validar_codigo_mfa(id_usuario, codigo):
        """Valida el último código MFA pendiente del usuario. Retorna (valido: bool, mensaje: str)."""
        fila = _dao.execute_query_one(
            """
            SELECT id_mfa_codigo, codigo, fecha_expiracion, intentos_validacion
            FROM mfa_codigos
            WHERE id_usuario = %s AND usado = FALSE
            ORDER BY fecha_generacion DESC
            LIMIT 1
            """,
            (id_usuario,)
        )

        if not fila:
            return False, "No hay un código pendiente. Solicite uno nuevo."

        if fila['intentos_validacion'] >= MFA_MAX_INTENTOS_VALIDACION:
            return False, "Demasiados intentos fallidos. Solicite un nuevo código."

        if datetime.utcnow() > fila['fecha_expiracion']:
            return False, "El código expiró. Solicite uno nuevo."

        if fila['codigo'] != (codigo or '').strip():
            _dao.execute_query(
                "UPDATE mfa_codigos SET intentos_validacion = intentos_validacion + 1 WHERE id_mfa_codigo = %s",
                (fila['id_mfa_codigo'],), commit=True
            )
            return False, "Código incorrecto."

        _dao.execute_query(
            "UPDATE mfa_codigos SET usado = TRUE, fecha_uso = CURRENT_TIMESTAMP WHERE id_mfa_codigo = %s",
            (fila['id_mfa_codigo'],), commit=True
        )
        return True, None

    @staticmethod
    def completar_login_mfa(id_usuario, codigo, csrf_token=None):
        """
        Segundo paso del login cuando el usuario tiene MFA habilitado:
        valida el código y, si es correcto, crea la sesión (mismo camino que
        un login sin MFA, vía _finalizar_sesion).

        Returns:
            Tuple[bool, Dict, str]: (exitoso, datos_usuario, mensaje)
        """
        valido, mensaje_error = AuthService.validar_codigo_mfa(id_usuario, codigo)
        if not valido:
            return False, {}, mensaje_error

        fila_nick = _dao.execute_query_one("SELECT usu_nick FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = AuthService.buscar_usuario_seguridad(fila_nick['usu_nick']) if fila_nick else None
        if not usuario:
            return False, {}, "Usuario no encontrado"

        ip_address = AuthService.obtener_ip_cliente()
        user_agent = AuthService.obtener_user_agent()

        datos_usuario = AuthService._finalizar_sesion(usuario, usuario['usu_nick'], ip_address, user_agent, csrf_token)
        if not datos_usuario:
            return False, {}, "Error al crear sesión. Intente nuevamente"

        return True, datos_usuario, "Login exitoso"
