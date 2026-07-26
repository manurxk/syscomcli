from app.core.base_dao import BaseDAO


class AccesoDao(BaseDAO):
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
        sql = """
            SELECT id_sesion, ip_address, user_agent, fecha_inicio, fecha_ultimo_ping, fecha_expiracion
            FROM sesiones
            WHERE id_usuario = %s AND est_sesion = TRUE AND fecha_expiracion > CURRENT_TIMESTAMP
            ORDER BY fecha_ultimo_ping DESC NULLS LAST
        """
        return self.execute_query(sql, (id_usuario,))

    def revocarMfa(self, id_usuario, usuario_modificacion=None):
        """Desactiva el MFA del usuario, invalida códigos pendientes y cierra
        sus sesiones activas (tipo_cierre='MFA_REVOKE'). El usuario deberá
        volver a vincular MFA desde cero la próxima vez que lo active."""
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
                """
                UPDATE sesiones
                SET est_sesion = FALSE, fecha_cierre = CURRENT_TIMESTAMP, tipo_cierre = 'MFA_REVOKE'
                WHERE id_usuario = %s AND est_sesion = TRUE
                """,
                (id_usuario,)
            )
            return True

        return self.execute_transaction(_fn)
