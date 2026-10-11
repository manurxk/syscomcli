from typing import Tuple, Optional, Dict
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.base_dao import BaseDAO


class AuthDao(BaseDAO):
    """DAO de cambio de contraseña y tokens de recuperación.

    No se guarda historial de contraseñas (decisión 2026-10-11): conservar
    los hashes de contraseñas anteriores sería un depósito de contraseñas."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def cambiar_password(self, id_usuario: int, password_actual: str, password_nueva: str, password_hash_actual: str) -> Tuple[bool, str]:
        """Cambia la contraseña de un usuario, validando contra el password actual."""
        if not check_password_hash(password_hash_actual, password_actual):
            return False, "La contraseña actual es incorrecta"

        password_nueva_hash = generate_password_hash(password_nueva, method='pbkdf2:sha256')

        try:
            sql = """
                UPDATE usuarios
                SET usu_clave = %s,
                    fecha_cambio_clave = CURRENT_TIMESTAMP,
                    requiere_cambio_clave = FALSE
                WHERE id_usuario = %s
            """
            self.execute_query(sql, (password_nueva_hash, id_usuario), commit=True)

            app.logger.info(f"Password cambiado exitosamente para usuario {id_usuario}")
            return True, "Contraseña cambiada exitosamente"
        except Exception as e:
            app.logger.error(f"Error al cambiar password: {str(e)}")
            return False, f"Error al cambiar contraseña: {str(e)}"

    def crear_password_reset_token(self, id_usuario: int, ip_solicitud: str, email_destino: str = None) -> Optional[str]:
        import uuid
        from datetime import datetime, timedelta

        token = str(uuid.uuid4())
        fecha_expiracion = datetime.now() + timedelta(hours=24)

        sql = """
            INSERT INTO password_reset_tokens (token, id_usuario, fecha_expiracion, ip_solicitud, email_destino)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING token
        """
        fila = self.execute_query_one(sql, (token, id_usuario, fecha_expiracion, ip_solicitud, email_destino), commit=True)
        return str(fila["token"]) if fila else None

    def validar_password_reset_token(self, token: str) -> Optional[Dict]:
        sql = """
            SELECT id_token, id_usuario, fecha_expiracion, usado, email_destino
            FROM password_reset_tokens
            WHERE token = %s AND usado = FALSE AND fecha_expiracion > CURRENT_TIMESTAMP
        """
        return self.execute_query_one(sql, (token,))

    def marcar_token_como_usado(self, token: str) -> bool:
        sql = """
            UPDATE password_reset_tokens
            SET usado = TRUE, fecha_uso = CURRENT_TIMESTAMP
            WHERE token = %s
        """
        return self.execute_query(sql, (token,), commit=True) > 0

    def resetear_password_con_token(self, token: str, password_nueva: str) -> Tuple[bool, str]:
        token_data = self.validar_password_reset_token(token)
        if not token_data:
            return False, "Token inválido o expirado"

        id_usuario = token_data['id_usuario']

        password_nueva_hash = generate_password_hash(password_nueva, method='pbkdf2:sha256')

        try:
            # mfa_habilitado se fuerza a TRUE: quien recuperó la contraseña ya demostró
            # conocer el correo vinculado a la cuenta (se exige que coincida antes de
            # generar el token), así que el próximo login exige además el código MFA.
            sql = """
                UPDATE usuarios
                SET usu_clave = %s,
                    fecha_cambio_clave = CURRENT_TIMESTAMP,
                    requiere_cambio_clave = FALSE,
                    usu_nro_intentos = 0,
                    nivel_escalada_bloqueo = 0,
                    fecha_bloqueo = NULL,
                    motivo_bloqueo = NULL,
                    bloqueado_hasta = NULL,
                    mfa_habilitado = TRUE
                WHERE id_usuario = %s
            """
            self.execute_query(sql, (password_nueva_hash, id_usuario), commit=True)

            self.marcar_token_como_usado(token)

            sql_sesiones = """
                UPDATE sesiones
                SET est_sesion = FALSE,
                    fecha_cierre = CURRENT_TIMESTAMP,
                    tipo_cierre = 'SECURITY'
                WHERE id_usuario = %s AND est_sesion = TRUE
            """
            self.execute_query(sql_sesiones, (id_usuario,), commit=True)

            app.logger.info(f"Password reseteado exitosamente para usuario {id_usuario} con token")
            return True, "Contraseña restablecida exitosamente"
        except Exception as e:
            app.logger.error(f"Error al resetear password: {str(e)}")
            return False, f"Error al restablecer contraseña: {str(e)}"
