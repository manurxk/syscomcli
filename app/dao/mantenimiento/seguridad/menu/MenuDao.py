import threading
import time

from app.core.base_dao import BaseDAO

# Caché del menú por conjunto de roles. El sidebar se arma en cada request y el
# menú casi no cambia: se guardan las filas de la consulta (no las URLs). Se vacía
# al guardar la matriz de «Menú»; el vencimiento cubre cambios hechos por otro
# proceso o por migración. Si el usuario cambia de roles, su clave es distinta.
_CACHE_MENU_SEGUNDOS = 300
_cache_menu = {}
_cache_menu_lock = threading.Lock()


class MenuDao(BaseDAO):
    """Acceso a datos del menú por rol (páginas y matriz rol-página), con caché."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCodRol(self, id_rol):
        """Devuelve el código del rol por su id."""
        sql = "SELECT cod_rol FROM roles WHERE id_rol = %s"
        fila = self.execute_query_one(sql, (id_rol,))
        return fila["cod_rol"] if fila else None

    def getPaginas(self):
        """Lista las páginas del sistema que pueden figurar en el menú."""
        sql = """
            SELECT id_pagina, id_modulo, des_pagina, pag_direccion, icono, orden, grupo_menu
            FROM paginas
            WHERE est_pagina = TRUE
            ORDER BY grupo_menu, orden
        """
        return self.execute_query(sql)

    def getMatrizMenu(self, id_rol):
        """Devuelve qué páginas del menú tiene habilitadas el rol."""
        sql = """
            SELECT p.id_pagina, p.des_pagina, p.grupo_menu, p.orden, p.descripcion,
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
        """Guarda los cambios de la matriz rol-página y vacía la caché del menú."""
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

        resultado = self.execute_transaction(_fn)
        self.invalidarCacheMenu()
        return resultado

    @staticmethod
    def invalidarCacheMenu():
        """Vacía la caché del menú."""
        with _cache_menu_lock:
            _cache_menu.clear()

    def getMenuParaRoles(self, roles):
        """Menú visible para el conjunto de roles de un usuario (multi-rol sin duplicados)."""
        if not roles:
            return []
        clave = tuple(sorted(set(roles)))
        with _cache_menu_lock:
            guardado = _cache_menu.get(clave)
        if guardado and time.monotonic() - guardado[0] < _CACHE_MENU_SEGUNDOS:
            return guardado[1]
        sql = """
            SELECT DISTINCT id_pagina, title, endpoint, icono, orden, grupo_menu, descripcion
            FROM (
                SELECT p.id_pagina, p.des_pagina AS title, p.pag_direccion AS endpoint,
                       p.icono, p.orden, p.grupo_menu, p.descripcion
                FROM paginas p
                JOIN roles_paginas rp ON rp.id_pagina = p.id_pagina
                JOIN roles r ON r.id_rol = rp.id_rol
                WHERE rp.visible = TRUE
                  AND p.est_pagina = TRUE
                  AND r.cod_rol = ANY(%s)
            ) menu_visible
            ORDER BY grupo_menu, orden
        """
        filas = self.execute_query(sql, (list(roles),))
        with _cache_menu_lock:
            _cache_menu[clave] = (time.monotonic(), filas)
        return filas
