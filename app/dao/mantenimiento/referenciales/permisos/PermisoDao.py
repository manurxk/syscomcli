from app.core.base_dao import BaseDAO


class PermisoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getModulos(self):
        sql = "SELECT id_modulo, des_modulo FROM modulos WHERE est_modulo = TRUE ORDER BY id_modulo"
        return self.execute_query(sql)

    def getAcciones(self):
        sql = "SELECT id_accion, cod_accion, des_accion FROM acciones WHERE est_accion = TRUE ORDER BY id_accion"
        return self.execute_query(sql)

    def getCodRol(self, id_rol):
        sql = "SELECT cod_rol FROM roles WHERE id_rol = %s"
        fila = self.execute_query_one(sql, (id_rol,))
        return fila["cod_rol"] if fila else None

    def getMatrizPermisos(self, id_rol):
        sql = """
            SELECT m.id_modulo, m.des_modulo,
                   a.id_accion, a.cod_accion, a.des_accion,
                   COALESCE(rp.permitido, FALSE) AS permitido
            FROM modulos m
            CROSS JOIN acciones a
            LEFT JOIN roles_permisos rp
                ON rp.id_modulo = m.id_modulo
               AND rp.id_accion = a.id_accion
               AND rp.id_rol = %s
            WHERE m.est_modulo = TRUE AND a.est_accion = TRUE
            ORDER BY m.id_modulo, a.id_accion
        """
        return self.execute_query(sql, (id_rol,))

    def guardarMatrizPermisos(self, id_rol, cambios, usuario_modificacion=None):
        def _fn(cur):
            for cambio in cambios:
                cur.execute(
                    """
                    INSERT INTO roles_permisos (id_rol, id_modulo, id_accion, permitido, usuario_creacion, usuario_modificacion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id_rol, id_modulo, id_accion)
                    DO UPDATE SET permitido = EXCLUDED.permitido,
                                  usuario_modificacion = EXCLUDED.usuario_modificacion,
                                  fecha_modificacion = now()
                    """,
                    (
                        id_rol,
                        cambio["id_modulo"],
                        cambio["id_accion"],
                        bool(cambio["permitido"]),
                        usuario_modificacion,
                        usuario_modificacion,
                    ),
                )
            return True

        return self.execute_transaction(_fn)
