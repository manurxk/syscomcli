from psycopg2.extras import Json

from app.core.base_dao import BaseDAO


class FacturaBorradorDao(BaseDAO):
    """Borradores de factura: una factura a medio hacer que se puede retomar o descartar.
    No consume número de factura ni timbrado, y no entra al libro de ventas."""

    def getBorradores(self):
        """Lista los borradores, el más reciente primero, con el paciente y el avance."""
        sql = """
            SELECT b.id_factura_borrador, b.id_paciente,
                   p.per_nombre || ' ' || p.per_apellido AS paciente,
                   p.per_cedula AS cedula,
                   cv.des_condicion_venta,
                   jsonb_array_length(COALESCE(b.datos->'detalles', '[]'::jsonb)) AS cant_items,
                   COALESCE((SELECT SUM((e->>'item_cantidad')::numeric * (e->>'item_precio_con_iva')::numeric
                                        - COALESCE((e->>'item_descuento')::numeric, 0))
                             FROM jsonb_array_elements(COALESCE(b.datos->'detalles', '[]'::jsonb)) e), 0)
                     - COALESCE(NULLIF(b.datos->'campos'->>'txtDescuento', '')::numeric, 0) AS total,
                   TO_CHAR(COALESCE(b.fecha_modificacion, b.fecha_creacion), 'DD/MM/YYYY') AS fecha_fmt,
                   TO_CHAR(COALESCE(b.fecha_modificacion, b.fecha_creacion), 'DD/MM/YYYY HH24:MI') AS ultima_edicion,
                   COALESCE(pu.per_nombre || ' ' || pu.per_apellido, u.usu_nick) AS usuario
            FROM facturas_borrador b
            LEFT JOIN pacientes pac ON b.id_paciente = pac.id_paciente
            LEFT JOIN personas p    ON pac.id_persona = p.id_persona
            LEFT JOIN condiciones_venta cv ON cv.id_condicion_venta = NULLIF(b.datos->'campos'->>'selCondicionVenta', '')::int
            LEFT JOIN usuarios u    ON COALESCE(b.usuario_modificacion, b.usuario_creacion) = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas pu   ON f.id_persona = pu.id_persona
            ORDER BY COALESCE(b.fecha_modificacion, b.fecha_creacion) DESC
        """
        return self.execute_query(sql)

    def getBorradorById(self, id_borrador):
        sql = "SELECT id_factura_borrador, id_paciente, datos FROM facturas_borrador WHERE id_factura_borrador = %s"
        return self.execute_query_one(sql, (id_borrador,))

    def crearBorrador(self, id_paciente, datos, usuario_creacion=None):
        sql = """
            INSERT INTO facturas_borrador (id_paciente, datos, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_factura_borrador
        """
        return self.execute_query_one(sql, (id_paciente, Json(datos), usuario_creacion), commit=True)['id_factura_borrador']

    def actualizarBorrador(self, id_borrador, id_paciente, datos, usuario_modificacion=None):
        sql = """
            UPDATE facturas_borrador
            SET id_paciente = %s, datos = %s, usuario_modificacion = %s
            WHERE id_factura_borrador = %s
        """
        return self.execute_query(sql, (id_paciente, Json(datos), usuario_modificacion, id_borrador), commit=True) > 0

    def eliminarBorrador(self, id_borrador):
        return self.execute_query("DELETE FROM facturas_borrador WHERE id_factura_borrador = %s", (id_borrador,), commit=True) > 0
