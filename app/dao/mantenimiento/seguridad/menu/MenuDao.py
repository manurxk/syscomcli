from app.core.base_dao import BaseDAO


class MenuDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCodRol(self, id_rol):
        sql = "SELECT cod_rol FROM roles WHERE id_rol = %s"
        fila = self.execute_query_one(sql, (id_rol,))
        return fila["cod_rol"] if fila else None

    def getPaginas(self):
        sql = """
            SELECT id_pagina, id_modulo, des_pagina, pag_direccion, icono, orden, grupo_menu
            FROM paginas
            WHERE est_pagina = TRUE
            ORDER BY grupo_menu, orden
        """
        return self.execute_query(sql)

    def getMatrizMenu(self, id_rol):
        sql = """
            SELECT p.id_pagina, p.des_pagina, p.grupo_menu, p.orden,
                   COALESCE(rp.visible, FALSE) AS visible
            FROM paginas p
            LEFT JOIN roles_paginas rp
                ON rp.id_pagina = p.id_pagina
               AND rp.id_rol = %s
            WHERE p.est_pagina = TRUE
            ORDER BY p.grupo_menu, p.orden
        """
        return self.execute_query(sql, (id_rol,))

    def guardarMatrizMenu(self, id_rol, cambios, usuario_modificacion=None):
        def _fn(cur):
            for cambio in cambios:
                cur.execute(
                    """
                    INSERT INTO roles_paginas (id_rol, id_pagina, visible, usuario_creacion, usuario_modificacion)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id_rol, id_pagina)
                    DO UPDATE SET visible = EXCLUDED.visible,
                                  usuario_modificacion = EXCLUDED.usuario_modificacion,
                                  fecha_modificacion = now()
                    """,
                    (
                        id_rol,
                        cambio["id_pagina"],
                        bool(cambio["visible"]),
                        usuario_modificacion,
                        usuario_modificacion,
                    ),
                )
            return True

        return self.execute_transaction(_fn)

    def getMenuParaRoles(self, roles):
        """Menú visible para el conjunto de roles de un usuario (multi-rol sin duplicados)."""
        if not roles:
            return []
        sql = """
            SELECT DISTINCT id_pagina, title, endpoint, icono, orden, grupo_menu
            FROM (
                SELECT p.id_pagina, p.des_pagina AS title, p.pag_direccion AS endpoint,
                       p.icono, p.orden, p.grupo_menu
                FROM paginas p
                JOIN roles_paginas rp ON rp.id_pagina = p.id_pagina
                JOIN roles r ON r.id_rol = rp.id_rol
                WHERE rp.visible = TRUE
                  AND p.est_pagina = TRUE
                  AND r.cod_rol = ANY(%s)
            ) menu_visible
            ORDER BY grupo_menu, orden
        """
        return self.execute_query(sql, (list(roles),))
