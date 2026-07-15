from datetime import datetime
from flask import current_app as app
from app.core.base_dao import BaseDAO


class RemisionDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getRemisiones(self):
        sql = """
            SELECT
                r.id_remision,
                r.remision_numero,
                r.id_paciente,
                r.id_pedido,
                r.id_factura,
                r.fecha_remision,
                r.fecha_entrega,
                r.observaciones,
                r.est_remision,
                r.fecha_creacion,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica
            FROM remisiones r
            JOIN pacientes pac ON r.id_paciente = pac.id_paciente
            JOIN personas pp  ON pac.id_persona = pp.id_persona
            ORDER BY r.fecha_remision DESC, r.id_remision DESC
        """
        rows = self.execute_query(sql)
        for r in rows:
            if r.get('fecha_remision'):
                r['fecha_remision_fmt'] = r['fecha_remision'].strftime('%d/%m/%Y')
                r['fecha_remision'] = r['fecha_remision'].strftime('%Y-%m-%d')
            if r.get('fecha_entrega'):
                r['fecha_entrega_fmt'] = r['fecha_entrega'].strftime('%d/%m/%Y')
                r['fecha_entrega'] = r['fecha_entrega'].strftime('%Y-%m-%d')
            if r.get('fecha_creacion'):
                r['fecha_creacion'] = r['fecha_creacion'].strftime('%d/%m/%Y')
        return rows

    def getRemisionById(self, id_remision):
        sql = """
            SELECT
                r.id_remision,
                r.remision_numero,
                r.id_paciente,
                r.id_pedido,
                r.id_factura,
                r.fecha_remision,
                r.fecha_entrega,
                r.observaciones,
                r.est_remision,
                r.fecha_creacion,
                r.usuario_creacion,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica
            FROM remisiones r
            JOIN pacientes pac ON r.id_paciente = pac.id_paciente
            JOIN personas pp  ON pac.id_persona = pp.id_persona
            WHERE r.id_remision = %s
        """
        row = self.execute_query_one(sql, (id_remision,))
        if row:
            if row.get('fecha_remision'):
                row['fecha_remision'] = row['fecha_remision'].strftime('%Y-%m-%d')
            if row.get('fecha_entrega'):
                row['fecha_entrega'] = row['fecha_entrega'].strftime('%Y-%m-%d')
            if row.get('fecha_creacion'):
                row['fecha_creacion'] = row['fecha_creacion'].strftime('%d/%m/%Y')
        return row

    def getRemisionDetalle(self, id_remision):
        sql = """
            SELECT
                rd.id_remision_detalle,
                rd.id_remision,
                rd.id_item_servicio,
                rd.item_descripcion,
                rd.item_cantidad,
                rd.item_unidad,
                rd.observaciones,
                its.des_item_servicio
            FROM remision_detalle rd
            LEFT JOIN items_servicios its ON rd.id_item_servicio = its.id_item_servicio
            WHERE rd.id_remision = %s
            ORDER BY rd.id_remision_detalle
        """
        return self.execute_query(sql, (id_remision,))

    def _generarNumero(self, cur):
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        patron = f'REM-{año}-{mes}-%'
        cur.execute(
            "SELECT remision_numero FROM remisiones WHERE remision_numero LIKE %s "
            "ORDER BY remision_numero DESC LIMIT 1",
            (patron,)
        )
        row = cur.fetchone()
        siguiente = 1
        if row and row[0]:
            partes = row[0].split('-')
            if len(partes) == 4:
                try:
                    siguiente = int(partes[3]) + 1
                except ValueError:
                    pass
        return f'REM-{año}-{mes}-{siguiente:04d}'

    def guardar(self, data, usuario_creacion=None):
        def _op(cur):
            numero = self._generarNumero(cur)
            cur.execute(
                """
                INSERT INTO remisiones(
                    remision_numero, id_paciente, id_pedido, id_factura,
                    fecha_remision, fecha_entrega, observaciones, est_remision,
                    usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_remision
                """,
                (
                    numero,
                    data['id_paciente'],
                    data.get('id_pedido') or None,
                    data.get('id_factura') or None,
                    data['fecha_remision'],
                    data.get('fecha_entrega') or None,
                    data.get('observaciones') or None,
                    data.get('est_remision', 'PENDIENTE'),
                    usuario_creacion,
                )
            )
            id_remision = cur.fetchone()[0]
            for d in data.get('detalles', []):
                cur.execute(
                    """
                    INSERT INTO remision_detalle(
                        id_remision, id_item_servicio, item_descripcion,
                        item_cantidad, item_unidad, observaciones
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        id_remision,
                        d.get('id_item_servicio') or None,
                        d['item_descripcion'],
                        d.get('item_cantidad', 1),
                        d.get('item_unidad') or None,
                        d.get('observaciones') or None,
                    )
                )
            return id_remision

        return self.execute_transaction(_op)

    def marcarEntregada(self, id_remision, usuario=None):
        filas = self.execute_query(
            """
            UPDATE remisiones
            SET est_remision = 'ENTREGADA',
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_remision = %s AND est_remision = 'PENDIENTE'
            """,
            (usuario, id_remision),
            commit=True
        )
        return filas > 0

    def anular(self, id_remision, usuario=None):
        filas = self.execute_query(
            """
            UPDATE remisiones
            SET est_remision = 'ANULADA',
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_remision = %s AND est_remision != 'ANULADA'
            """,
            (usuario, id_remision),
            commit=True
        )
        return filas > 0
