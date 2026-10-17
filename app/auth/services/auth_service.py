"""
Servicio de autenticación mejorado
FASE 2: MEJORAS DE SEGURIDAD
"""
import re
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from flask import current_app as app, request
from werkzeug.security import check_password_hash
from app.core.base_dao import BaseDAO
from app.services.EmailService import EmailService
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion

_dao = BaseDAO(db_name_env="DB_NAME_NUEVA")

MFA_MAX_INTENTOS_VALIDACION = 5

# Bloqueo escalonado de cuenta: deben coincidir con registrar_intento_login (migrations/104)
BLOQUEO_UMBRAL_PRIMER_NIVEL = 5   # 5 fallos -> 30 min
BLOQUEO_UMBRAL_REINCIDENCIA = 3   # 3 fallos -> 1 h; 3 mas -> indefinido (desbloquea un administrador)

# Recuperacion de contrasena: maximo de correos por cuenta en la ventana
RECUPERACION_MAX_SOLICITUDES = 3
RECUPERACION_VENTANA_MINUTOS = 60


class AuthService:
    """Servicio centralizado para autenticación y gestión de sesiones"""

    @staticmethod
    def obtener_ip_cliente() -> str:
        """Obtiene la IP del cliente desde el request.

        No se lee X-Forwarded-For a mano (el cliente lo puede falsificar):
        detrás de nginx, ProxyFix (app/__init__.py) ya deja la IP real en remote_addr.
        """
        return request.remote_addr or '0.0.0.0'

    @staticmethod
    def obtener_user_agent() -> str:
        """Obtiene el User-Agent del cliente"""
        return request.headers.get('User-Agent', 'Unknown')

    @staticmethod
    def _mapear_usuario_seguridad(fila: Dict) -> Dict:
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
            return AuthService._mapear_usuario_seguridad(fila) if fila else None
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
    def _alertar_bloqueo_por_correo(id_usuario, correo, ip_address):
        """Avisa por correo al dueño de la cuenta que se bloqueó por intentos
        fallidos (ver login(), paso 4). No bloquea el flujo de login si el
        envío falla — es una alerta best-effort."""
        if not correo:
            return
        try:
            fila = _dao.execute_query_one(
                "SELECT bloqueado_hasta FROM usuarios WHERE id_usuario = %s", (id_usuario,)
            )
            bloqueado_hasta = fila.get('bloqueado_hasta') if fila else None
            detalle = (
                f"hasta el {bloqueado_hasta.strftime('%Y-%m-%d %H:%M')}"
                if bloqueado_hasta
                else "de forma indefinida (requiere que un administrador la desbloquee)"
            )
            asunto = f"{app.config.get('NOMBRE_CLINICA', 'SYSCLIN')} - Su cuenta fue bloqueada"
            cuerpo = (
                f"Detectamos múltiples intentos fallidos de inicio de sesión en su cuenta, "
                f"desde la IP {ip_address}.\n\n"
                f"Su cuenta quedó bloqueada {detalle}.\n\n"
                f"Si no fue usted, le recomendamos cambiar su contraseña apenas pueda ingresar de nuevo."
            )
            EmailService().enviar_correo(correo, asunto, cuerpo)
        except Exception as e:
            app.logger.error(f"Error al enviar alerta de bloqueo para usuario {id_usuario}: {str(e)}")

    @staticmethod
    def auditar_rate_limit(ip_address, ventana_minutos, detalle, id_usuario=None):
        """Registra RATE_LIMIT en auditoría una sola vez por IP y ventana: un ataque
        insistente no debe generar un evento por cada petición frenada."""
        try:
            ya_registrado = _dao.execute_query_one(
                """
                SELECT 1 AS hay FROM auditoria_sistema
                WHERE accion = %s AND ip_origen = %s::inet
                  AND fecha_evento > CURRENT_TIMESTAMP - (%s || ' minutes')::interval
                LIMIT 1
                """,
                (AuditAccion.RATE_LIMIT, ip_address, ventana_minutos)
            )
            if not ya_registrado:
                AuditoriaDao().registrar_evento(
                    id_usuario=id_usuario, accion=AuditAccion.RATE_LIMIT,
                    detalle=detalle, ip_origen=ip_address
                )
        except Exception as e:
            app.logger.error(f"Error al auditar RATE_LIMIT para ip {ip_address}: {str(e)}")

    @staticmethod
    def _auditar_bloqueo_cuenta(id_usuario, usuario_nombre, ip_address):
        """Registra ACCOUNT_LOCKED con el nivel de escalada alcanzado (ver login(), paso 4)."""
        try:
            fila = _dao.execute_query_one(
                "SELECT nivel_escalada_bloqueo, motivo_bloqueo FROM usuarios WHERE id_usuario = %s",
                (id_usuario,)
            )
            nivel = fila['nivel_escalada_bloqueo'] if fila else None
            motivo = fila['motivo_bloqueo'] if fila else ''
            AuditoriaDao().registrar_evento(
                id_usuario=id_usuario, accion=AuditAccion.ACCOUNT_LOCKED,
                detalle=f"Cuenta \"{usuario_nombre}\" bloqueada (nivel {nivel}): {motivo}",
                ip_origen=ip_address
            )
        except Exception as e:
            app.logger.error(f"Error al auditar bloqueo de usuario {id_usuario}: {str(e)}")

    @staticmethod
    def recuperacion_excedida(id_usuario: int) -> bool:
        """True si la cuenta ya recibió RECUPERACION_MAX_SOLICITUDES correos de recuperación
        en la ventana: evita usar la recuperación para inundar el correo del usuario."""
        try:
            fila = _dao.execute_query_one(
                """
                SELECT COUNT(*) AS total FROM password_reset_tokens
                WHERE id_usuario = %s
                  AND fecha_creacion > CURRENT_TIMESTAMP - (%s || ' minutes')::interval
                """,
                (id_usuario, RECUPERACION_VENTANA_MINUTOS)
            )
            return bool(fila) and fila['total'] >= RECUPERACION_MAX_SOLICITUDES
        except Exception as e:
            app.logger.error(f"Error al contar solicitudes de recuperación de {id_usuario}: {str(e)}")
            return False

    ROLES_AUTORIZAN_CORRECCION = ('ADMINISTRADOR',)

    @staticmethod
    def verificar_autorizacion_administrador(usuario_nombre: str, password: str) -> Dict:
        """Autorización puntual de un administrador presente (ej. corregir una cita cerrada):
        escribe SU usuario y contraseña en la PC de otro usuario, sin abrir sesión ni pedir MFA.

        Mismas defensas que el login: límite por IP, cuenta inactiva o bloqueada, y cada
        contraseña errónea cuenta para el bloqueo escalonado de ESA cuenta (se registra
        en Accesos como intento fallido). Devuelve {'id_usuario', 'usu_nick'} o lanza ValueError.
        """
        ip_address = AuthService.obtener_ip_cliente()
        user_agent = AuthService.obtener_user_agent()
        error_generico = "Usuario o contraseña de administrador incorrectos."

        if AuthService.contar_intentos_fallidos_ip(ip_address, 15) >= 10:
            AuthService.auditar_rate_limit(
                ip_address, 15, f"Autorización de administrador frenada (usuario intentado: '{usuario_nombre}')"
            )
            raise ValueError("Demasiados intentos fallidos desde esta PC. Intente nuevamente más tarde.")

        usuario = AuthService.buscar_usuario_seguridad(usuario_nombre or '')
        if not usuario:
            AuthService.registrar_intento_login(usuario_nombre, None, False, 'usuario_no_existe', ip_address, user_agent)
            raise ValueError(error_generico)

        id_usuario = usuario['id_usuario']
        if not usuario['usu_estado'] or usuario.get('esta_bloqueado') or AuthService.esta_usuario_bloqueado(id_usuario):
            AuthService.registrar_intento_login(usuario_nombre, id_usuario, False, 'cuenta_bloqueada', ip_address, user_agent)
            raise ValueError("La cuenta del administrador está inactiva o bloqueada.")

        if not check_password_hash(usuario['usu_clave'], password or ''):
            AuthService.registrar_intento_login(usuario_nombre, id_usuario, False, 'password_invalido', ip_address, user_agent)
            if AuthService.esta_usuario_bloqueado(id_usuario):
                AuthService._auditar_bloqueo_cuenta(id_usuario, usuario_nombre, ip_address)
                AuthService._alertar_bloqueo_por_correo(id_usuario, usuario.get('correo'), ip_address)
            raise ValueError(error_generico)

        roles = {(r or '').upper() for r in AuthService.obtener_roles_usuario(id_usuario)}
        if not roles.intersection(AuthService.ROLES_AUTORIZAN_CORRECCION):
            raise ValueError("El usuario indicado no tiene rol de Administrador.")

        return {'id_usuario': id_usuario, 'usu_nick': usuario['usu_nick']}

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

    DISPOSITIVO_CONFIABLE_DIAS = 60

    @staticmethod
    def crear_dispositivo_confiable(id_usuario: int, ip_address: str, user_agent: str) -> str:
        """Emite un token de 'dispositivo confiable': mientras sea válido (60 días),
        el login de un usuario con MFA se salta el paso del código. Se emite tras
        validar el código MFA con éxito (ver login.py, verificar_mfa)."""
        token = secrets.token_urlsafe(32)
        fecha_expiracion = datetime.utcnow() + timedelta(days=AuthService.DISPOSITIVO_CONFIABLE_DIAS)
        _dao.execute_query(
            """
            INSERT INTO mfa_dispositivos_confiables (id_usuario, token, fecha_expiracion, ip_creacion, user_agent)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_usuario, token, fecha_expiracion, ip_address, user_agent), commit=True
        )
        return token

    @staticmethod
    def revocar_dispositivo_confiable_por_token(token: Optional[str]) -> None:
        """Marca revocado el token de dispositivo confiable que se está por
        reemplazar (ver login.py, _emitir_dispositivo_confiable) — la rotación
        en cada login no debe dejar el token anterior 'Vigente' indefinidamente."""
        if not token:
            return
        _dao.execute_query(
            "UPDATE mfa_dispositivos_confiables SET revocado = TRUE WHERE token = %s",
            (token,), commit=True
        )

    @staticmethod
    def validar_dispositivo_confiable(id_usuario: int, token: Optional[str]) -> bool:
        """True si el token de dispositivo confiable es válido para este usuario
        (no vencido, no revocado)."""
        if not token:
            return False
        fila = _dao.execute_query_one(
            """
            SELECT id_dispositivo FROM mfa_dispositivos_confiables
            WHERE id_usuario = %s AND token = %s AND revocado = FALSE AND fecha_expiracion > CURRENT_TIMESTAMP
            """,
            (id_usuario, token)
        )
        return bool(fila)

    @staticmethod
    def login(
        usuario_nombre: str,
        password: str,
        csrf_token: Optional[str] = None,
        token_dispositivo: Optional[str] = None
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
            AuthService.auditar_rate_limit(
                ip_address, VENTANA_MINUTOS_IP,
                f"Login frenado: {MAX_INTENTOS_FALLIDOS_IP} o más intentos fallidos desde esta IP en "
                f"{VENTANA_MINUTOS_IP} min (usuario intentado: '{usuario_nombre}')"
            )
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

            app.logger.warning(f"LOGIN_FAIL user={usuario_nombre} reason=password_invalido ip={ip_address}")

            # Si este intento acaba de disparar el bloqueo (5 fallos el primero,
            # 3 las reincidencias, ver registrar_intento_login/escalada), auditar y
            # avisar por correo al dueño de la cuenta — no llegamos acá si ya
            # estaba bloqueada antes (ver paso 3), así que es un bloqueo recién ocurrido.
            if AuthService.esta_usuario_bloqueado(id_usuario):
                AuthService._auditar_bloqueo_cuenta(id_usuario, usuario_nombre, ip_address)
                AuthService._alertar_bloqueo_por_correo(id_usuario, usuario.get('correo'), ip_address)
                return False, {}, "Contraseña incorrecta. Cuenta bloqueada por múltiples intentos fallidos"

            try:
                fila = _dao.execute_query_one(
                    "SELECT usu_nro_intentos, nivel_escalada_bloqueo FROM usuarios WHERE id_usuario = %s",
                    (id_usuario,)
                )
                intentos = (fila['usu_nro_intentos'] if fila else 0) or 0
                nivel = (fila['nivel_escalada_bloqueo'] if fila else 0) or 0
                umbral = BLOQUEO_UMBRAL_PRIMER_NIVEL if nivel == 0 else BLOQUEO_UMBRAL_REINCIDENCIA
                intentos_restantes = max(0, umbral - intentos)
            except Exception:
                intentos_restantes = 0

            return False, {}, f"Contraseña incorrecta. Intentos restantes: {intentos_restantes}"

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

        # 6.5 Si tiene MFA habilitado pero todavía no tiene un correo vinculado
        # (ej. recién se le activó MFA), no hay a dónde mandar el código: se le
        # pide vincular uno antes de continuar (ver vincular_correo_y_enviar_mfa).
        if usuario.get('mfa_habilitado') and not usuario.get('correo'):
            AuthService.registrar_intento_login(
                usuario_intentado=usuario_nombre,
                id_usuario=id_usuario,
                exitoso=True,
                motivo_fallo=None,
                ip_address=ip_address,
                user_agent=user_agent
            )
            app.logger.info(f"LOGIN_REQUIERE_VINCULAR_CORREO user={usuario_nombre} ip={ip_address}")
            return False, {'id_usuario': id_usuario, 'usu_nick': usuario['usu_nick'], 'requiere_vincular_correo': True}, \
                "Debe vincular un correo para poder continuar (autenticación en dos pasos)"

        # 7. Si el usuario tiene MFA habilitado, no crear sesión todavía:
        # se envía un código por correo y el login se completa en un segundo paso
        # (ver completar_login_mfa).
        if usuario.get('mfa_habilitado'):
            # 7.1 Si el login viene de un dispositivo ya confiable (MFA validado hace
            # menos de 60 días en ese mismo navegador), se salta el código.
            if AuthService.validar_dispositivo_confiable(id_usuario, token_dispositivo):
                app.logger.info(f"LOGIN_MFA_DISPOSITIVO_CONFIABLE user={usuario_nombre} ip={ip_address}")
                datos_usuario = AuthService._finalizar_sesion(usuario, usuario_nombre, ip_address, user_agent, csrf_token)
                if not datos_usuario:
                    return False, {}, "Error al crear sesión. Intente nuevamente"
                return True, datos_usuario, "Login exitoso"

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
            # Usuario sin funcionario/persona: se muestra el nick (mismo criterio que auth_api)
            'nombre_completo': (usuario['nombre_completo'] or '').strip() or usuario['usu_nick'],
            'grupo': usuario['grupo_nombre'],
            'id_grupo': usuario['id_grupo'],
            'roles': AuthService.obtener_roles_usuario(id_usuario),
            'id_funcionario': usuario.get('id_funcionario'),
            'session_token': session_token,
            'csrf_token': csrf_token,
            'refresh_token': refresh_token,
            'sesion_id': sesion_id,
            'mfa_habilitado': bool(usuario.get('mfa_habilitado'))
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
    def vincular_correo_y_enviar_mfa(id_usuario, correo):
        """
        Paso previo al MFA cuando el usuario lo tiene habilitado pero todavía
        no tiene un correo vinculado (ver login(), rama requiere_vincular_correo).
        Vincula el correo y envía de inmediato el primer código de verificación.

        Si el usuario tiene un funcionario/persona asociado, el correo se guarda
        en personas.per_correo (mismo dato que usan facturas/recordatorios). Si
        no (ej. cuentas semilla como "manu", sin ficha de personal), se guarda
        en usuarios.correo — la vista v_usuarios_seguridad usa COALESCE entre
        ambas columnas.

        id_usuario viene de la sesión de Flask (mfa_pendiente_id_usuario), fijado
        únicamente tras validar la contraseña en login() — no se re-pide la
        contraseña acá, igual que en completar_login_mfa().

        Returns:
            Tuple[bool, str]: (exitoso, mensaje)
        """
        correo = (correo or '').strip()
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', correo):
            return False, "El correo no tiene un formato válido"

        filas_afectadas = _dao.execute_query(
            """
            UPDATE personas SET per_correo = %s
            WHERE id_persona = (
                SELECT f.id_persona FROM usuarios u
                JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
                WHERE u.id_usuario = %s
            )
            """,
            (correo, id_usuario), commit=True
        )
        if not filas_afectadas:
            filas_afectadas = _dao.execute_query(
                "UPDATE usuarios SET correo = %s WHERE id_usuario = %s",
                (correo, id_usuario), commit=True
            )
        if not filas_afectadas:
            return False, "No se pudo vincular el correo: usuario no encontrado."

        ip_address = AuthService.obtener_ip_cliente()
        user_agent = AuthService.obtener_user_agent()
        enviado, error_mfa = AuthService.generar_y_enviar_codigo_mfa(id_usuario, ip_address, user_agent)
        if not enviado:
            return False, f"Correo vinculado, pero no se pudo enviar el código: {error_mfa}"

        return True, "Correo vinculado. Se envió un código de verificación a su correo."

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
