import threading
import time

from app.core.base_dao import BaseDAO

# Caché de permisos por conjunto de roles (mismo criterio que el menú en MenuDao):
# se vacía al guardar la matriz de «Permisos» y vence a los 5 minutos.
_CACHE_PERMISOS_SEGUNDOS = 300
_cache_permisos = {}
_cache_permisos_lock = threading.Lock()


class PermisoDao(BaseDAO):
    """Acceso a datos de la matriz de permisos por acción (módulo, acción y rol), con caché."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getModulos(self):
        """Lista los módulos sobre los que se definen permisos."""
        sql = "SELECT id_modulo, des_modulo FROM modulos WHERE est_modulo = TRUE ORDER BY id_modulo"
        return self.execute_query(sql)

    def getAcciones(self):
        """Lista las acciones de permiso (leer, crear, editar, eliminar)."""
        sql = "SELECT id_accion, cod_accion, des_accion FROM acciones WHERE est_accion = TRUE ORDER BY id_accion"
        return self.execute_query(sql)

    def getCodRol(self, id_rol):
        """Devuelve el código del rol por su id."""
        sql = "SELECT cod_rol FROM roles WHERE id_rol = %s"
        fila = self.execute_query_one(sql, (id_rol,))
        return fila["cod_rol"] if fila else None

    def getMatrizPermisos(self, id_rol):
        """Devuelve los permisos por módulo y acción del rol."""
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
        """Guarda los cambios de la matriz de permisos del rol y vacía la caché."""
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

        resultado = self.execute_transaction(_fn)
        self.invalidarCachePermisos()
        return resultado

    @staticmethod
    def invalidarCachePermisos():
        """Vacía la caché de permisos."""
        with _cache_permisos_lock:
            _cache_permisos.clear()

    def getPermisosParaRoles(self, roles):
        """Conjunto de (des_modulo, cod_accion) permitidos para los roles del usuario (unión de roles)."""
        if not roles:
            return frozenset()
        clave = tuple(sorted(set(roles)))
        with _cache_permisos_lock:
            guardado = _cache_permisos.get(clave)
        if guardado and time.monotonic() - guardado[0] < _CACHE_PERMISOS_SEGUNDOS:
            return guardado[1]
        sql = """
            SELECT DISTINCT m.des_modulo, a.cod_accion
            FROM roles_permisos rp
            JOIN roles r ON r.id_rol = rp.id_rol
            JOIN modulos m ON m.id_modulo = rp.id_modulo
            JOIN acciones a ON a.id_accion = rp.id_accion
            WHERE rp.permitido = TRUE
              AND m.est_modulo = TRUE AND a.est_accion = TRUE
              AND r.cod_rol = ANY(%s)
        """
        permisos = frozenset((f["des_modulo"].upper(), f["cod_accion"].upper())
                             for f in self.execute_query(sql, (list(roles),)))
        with _cache_permisos_lock:
            _cache_permisos[clave] = (time.monotonic(), permisos)
        return permisos
