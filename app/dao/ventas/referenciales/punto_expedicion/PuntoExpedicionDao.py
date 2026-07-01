from flask import current_app as app
from app.core.base_dao import BaseDAO


class PuntoExpedicionDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPuntosExpedicion(self, id_timbrado=None):
        if id_timbrado:
            sql = """
                SELECT pe.id_punto_expedicion, pe.id_timbrado, pe.codigo_punto_expedicion,
                       pe.nombre_punto_expedicion, pe.ultimo_numero_usado, pe.est_punto_expedicion,
                       t.numero_timbrado, t.codigo_establecimiento
                FROM puntos_expedicion pe
                JOIN timbrados t ON pe.id_timbrado = t.id_timbrado
                WHERE pe.id_timbrado = %s
                ORDER BY pe.codigo_punto_expedicion
            """
            return self.execute_query(sql, (id_timbrado,))
        sql = """
            SELECT pe.id_punto_expedicion, pe.id_timbrado, pe.codigo_punto_expedicion,
                   pe.nombre_punto_expedicion, pe.ultimo_numero_usado, pe.est_punto_expedicion,
                   t.numero_timbrado, t.codigo_establecimiento
            FROM puntos_expedicion pe
            JOIN timbrados t ON pe.id_timbrado = t.id_timbrado
            ORDER BY t.numero_timbrado, pe.codigo_punto_expedicion
        """
        return self.execute_query(sql)

    def getPuntoExpedicionById(self, id_punto_expedicion):
        sql = """
            SELECT pe.id_punto_expedicion, pe.id_timbrado, pe.codigo_punto_expedicion,
                   pe.nombre_punto_expedicion, pe.ultimo_numero_usado, pe.est_punto_expedicion,
                   t.numero_timbrado, t.codigo_establecimiento
            FROM puntos_expedicion pe
            JOIN timbrados t ON pe.id_timbrado = t.id_timbrado
            WHERE pe.id_punto_expedicion = %s
        """
        return self.execute_query_one(sql, (id_punto_expedicion,))

    def getPuntosVigentes(self):
        """Puntos de expedición activos cuyo timbrado sigue vigente — para el formulario de factura."""
        sql = """
            SELECT pe.id_punto_expedicion, pe.id_timbrado, pe.codigo_punto_expedicion,
                   pe.nombre_punto_expedicion, pe.ultimo_numero_usado,
                   t.numero_timbrado, t.codigo_establecimiento
            FROM puntos_expedicion pe
            JOIN timbrados t ON pe.id_timbrado = t.id_timbrado
            WHERE pe.est_punto_expedicion = TRUE
              AND t.est_timbrado = TRUE
              AND t.fecha_inicio <= CURRENT_DATE
              AND t.fecha_vencimiento >= CURRENT_DATE
            ORDER BY t.numero_timbrado, pe.codigo_punto_expedicion
        """
        return self.execute_query(sql)

    def codigoExiste(self, id_timbrado, codigo_punto_expedicion, excluir_id=None):
        sql = """
            SELECT 1 FROM puntos_expedicion
            WHERE id_timbrado=%s AND codigo_punto_expedicion=%s
        """
        params = [id_timbrado, codigo_punto_expedicion]
        if excluir_id:
            sql += " AND id_punto_expedicion != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardar(self, id_timbrado, codigo_punto_expedicion, nombre_punto_expedicion,
                est_punto_expedicion=True, usuario_creacion=None):
        sql = """
            INSERT INTO puntos_expedicion(
                id_timbrado, codigo_punto_expedicion, nombre_punto_expedicion,
                ultimo_numero_usado, est_punto_expedicion, usuario_creacion
            )
            VALUES (%s, %s, %s, 0, %s, %s)
            RETURNING id_punto_expedicion
        """
        fila = self.execute_query_one(
            sql,
            (id_timbrado, codigo_punto_expedicion.zfill(3),
             nombre_punto_expedicion, est_punto_expedicion, usuario_creacion),
            commit=True
        )
        return fila['id_punto_expedicion'] if fila else None

    def update(self, id_punto_expedicion, codigo_punto_expedicion, nombre_punto_expedicion,
               est_punto_expedicion=True, usuario_modificacion=None):
        sql = """
            UPDATE puntos_expedicion
            SET codigo_punto_expedicion=%s, nombre_punto_expedicion=%s,
                est_punto_expedicion=%s, usuario_modificacion=%s
            WHERE id_punto_expedicion=%s
        """
        return self.execute_query(
            sql,
            (codigo_punto_expedicion.zfill(3), nombre_punto_expedicion,
             est_punto_expedicion, usuario_modificacion, id_punto_expedicion),
            commit=True
        ) > 0

    def desactivar(self, id_punto_expedicion, usuario_modificacion=None):
        sql = """
            UPDATE puntos_expedicion
            SET est_punto_expedicion=FALSE, usuario_modificacion=%s
            WHERE id_punto_expedicion=%s
        """
        return self.execute_query(sql, (usuario_modificacion, id_punto_expedicion), commit=True) > 0

    def tieneFacturas(self, id_punto_expedicion):
        sql = "SELECT 1 FROM facturas WHERE id_punto_expedicion=%s LIMIT 1"
        return self.execute_query_one(sql, (id_punto_expedicion,)) is not None
