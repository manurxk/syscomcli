from app.core.base_dao import BaseDAO


class AccesoDao(BaseDAO):
    """Acceso a datos de las sesiones y el estado de acceso de los usuarios."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getUsuariosConEstadoAcceso(self):
        """Estado de identidad por usuario: MFA, bloqueo, sesiones activas."""
        sql = """
            SELECT
                u.id_usuario, u.usu_nick, u.est_usuario, u.mfa_habilitado,
                v.nombre_completo, v.grupo_nombre, v.esta_bloqueado,
                v.fecha_ultimo_login, v.ip_ultimo_login,
                COUNT(s.id_sesion) FILTER (WHERE s.est_sesion = TRUE AND s.fecha_expiracion > CURRENT_TIMESTAMP) AS sesiones_activas
            FROM usuarios u
            LEFT JOIN v_usuarios_seguridad v ON v.id_usuario = u.id_usuario
            LEFT JOIN sesiones s ON s.id_usuario = u.id_usuario
            GROUP BY u.id_usuario, u.usu_nick, u.est_usuario, u.mfa_habilitado,
                     v.nombre_completo, v.grupo_nombre, v.esta_bloqueado,
                     v.fecha_ultimo_login, v.ip_ultimo_login
            ORDER BY u.usu_nick
        """
        return self.execute_query(sql)

    def getSesionesPorUsuario(self, id_usuario):
        """Lista las sesiones del usuario."""
        sql = """
            SELECT id_sesion, ip_address, user_agent, fecha_inicio, fecha_ultimo_ping, fecha_expiracion
            FROM sesiones
            WHERE id_usuario = %s AND est_sesion = TRUE AND fecha_expiracion > CURRENT_TIMESTAMP
            ORDER BY fecha_ultimo_ping DESC NULLS LAST
        """
        return self.execute_query(sql, (id_usuario,))

    def getDetalleUsuario(self, id_usuario):
        """Datos de identidad/seguridad de un usuario para la ventana de detalle
        (ver usuario-detalle.html): estado de bloqueo, MFA, último login."""
        sql = """
            SELECT
                u.id_usuario, u.usu_nick, u.est_usuario, u.usu_nro_intentos,
                u.nivel_escalada_bloqueo, u.fecha_bloqueo, u.bloqueado_hasta, u.motivo_bloqueo,
                u.fecha_ultimo_login, u.ip_ultimo_login, u.fecha_creacion,
                v.nombre_completo, v.grupo_nombre, v.cargo_nombre,
                v.mfa_habilitado, v.correo, v.esta_bloqueado
            FROM usuarios u
            LEFT JOIN v_usuarios_seguridad v ON v.id_usuario = u.id_usuario
            WHERE u.id_usuario = %s
        """
        return self.execute_query_one(sql, (id_usuario,))

    def getHistorialAccesos(self, id_usuario, limite=50):
        """Últimos intentos de login (exitosos y fallidos) del usuario."""
        sql = """
            SELECT id_acceso, resultado, ip_origen, user_agent, fecha_intento
            FROM accesos_sistema
            WHERE id_usuario = %s
            ORDER BY fecha_intento DESC
            LIMIT %s
        """
        return self.execute_query(sql, (id_usuario, limite))

    def getResumenMfa(self, id_usuario):
        """Cuántos códigos MFA se enviaron, cuántos se llegaron a usar y cuándo
        fue el último envío."""
        sql = """
            SELECT COUNT(*) AS total_enviados,
                   COUNT(*) FILTER (WHERE usado = TRUE) AS total_usados,
                   MAX(fecha_generacion) AS ultimo_enviado
            FROM mfa_codigos
            WHERE id_usuario = %s
        """
        return self.execute_query_one(sql, (id_usuario,))

    def getDispositivosConfiables(self, id_usuario):
        """Dispositivos que se saltan el código MFA por 60 días (ver
        AuthService.crear_dispositivo_confiable)."""
        sql = """
            SELECT id_dispositivo, fecha_creacion, fecha_expiracion, ip_creacion, user_agent, revocado
            FROM mfa_dispositivos_confiables
            WHERE id_usuario = %s
            ORDER BY fecha_creacion DESC
        """
        return self.execute_query(sql, (id_usuario,))

    def getSolicitudesRecuperacion(self, id_usuario):
        """Solicitudes de recuperación de contraseña del usuario."""
        sql = """
            SELECT id_token, fecha_creacion, fecha_expiracion, usado, fecha_uso, ip_solicitud, email_destino
            FROM password_reset_tokens
            WHERE id_usuario = %s
            ORDER BY fecha_creacion DESC
        """
        return self.execute_query(sql, (id_usuario,))

    def revocarMfa(self, id_usuario, usuario_modificacion=None):
        """Desactiva el MFA del usuario, invalida códigos pendientes, revoca sus
        dispositivos confiables y cierra sus sesiones activas (tipo_cierre='MFA_REVOKE').
        El usuario deberá volver a vincular MFA desde cero la próxima vez que lo active:
        sin revocar los dispositivos, uno marcado antes seguiría salteando el código."""
        def _fn(cur):
            cur.execute(
                "UPDATE usuarios SET mfa_habilitado = FALSE WHERE id_usuario = %s",
                (id_usuario,)
            )
            cur.execute(
                "UPDATE mfa_codigos SET usado = TRUE WHERE id_usuario = %s AND usado = FALSE",
                (id_usuario,)
            )
            cur.execute(
                "UPDATE mfa_dispositivos_confiables SET revocado = TRUE WHERE id_usuario = %s AND revocado = FALSE",
                (id_usuario,)
            )
            cur.execute(
                """
                UPDATE sesiones
                SET est_sesion = FALSE, fecha_cierre = CURRENT_TIMESTAMP, tipo_cierre = 'MFA_REVOKE'
                WHERE id_usuario = %s AND est_sesion = TRUE
                """,
                (id_usuario,)
            )
            return True

        return self.execute_transaction(_fn)
