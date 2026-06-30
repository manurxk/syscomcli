from app.core.base_dao import BaseDAO
from datetime import date


class PedidoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPedidos(self):
        sql = """
            SELECT p.id_pedido, p.pedido_numero, p.id_paciente, p.id_profesional,
                   p.fecha_pedido, p.fecha_entrega, p.pedido_subtotal, p.pedido_descuento,
                   p.pedido_total, p.observaciones, p.pedido_estado, p.est_pedido,
                   CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                   pp.per_cedula AS paciente_cedula,
                   CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre
            FROM pedidos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            LEFT JOIN funcionarios f ON p.id_profesional = f.id_funcionario
            LEFT JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE p.est_pedido = TRUE
            ORDER BY p.fecha_pedido DESC, p.id_pedido DESC
        """
        pedidos = self.execute_query(sql)
        for p in pedidos:
            p['fecha_pedido'] = p['fecha_pedido'].strftime('%Y-%m-%d') if p['fecha_pedido'] else None
            p['fecha_entrega'] = p['fecha_entrega'].strftime('%Y-%m-%d') if p['fecha_entrega'] else None
        return pedidos

    def getPedidoById(self, id_pedido):
        sql = """
            SELECT p.id_pedido, p.pedido_numero, p.id_paciente, p.id_profesional,
                   p.fecha_pedido, p.fecha_entrega, p.pedido_subtotal, p.pedido_descuento,
                   p.pedido_total, p.observaciones, p.pedido_estado,
                   CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                   pp.per_cedula AS paciente_cedula,
                   CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre
            FROM pedidos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            LEFT JOIN funcionarios f ON p.id_profesional = f.id_funcionario
            LEFT JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE p.id_pedido = %s AND p.est_pedido = TRUE
        """
        pedido = self.execute_query_one(sql, (id_pedido,))
        if not pedido:
            return None
        pedido['fecha_pedido'] = pedido['fecha_pedido'].strftime('%Y-%m-%d') if pedido['fecha_pedido'] else None
        pedido['fecha_entrega'] = pedido['fecha_entrega'].strftime('%Y-%m-%d') if pedido['fecha_entrega'] else None
        pedido['detalles'] = self.getDetallePedido(id_pedido)
        return pedido

    def getDetallePedido(self, id_pedido):
        sql = """
            SELECT pd.id_pedido_detalle, pd.id_pedido, pd.id_item_servicio,
                   pd.item_descripcion, pd.item_cantidad, pd.item_precio_unitario,
                   pd.item_descuento, pd.item_subtotal, pd.observaciones
            FROM pedido_detalle pd
            WHERE pd.id_pedido = %s AND pd.est_pedido_detalle = TRUE
            ORDER BY pd.id_pedido_detalle
        """
        return self.execute_query(sql, (id_pedido,))

    def _generarNumero(self, cur):
        anio = date.today().year
        mes = date.today().strftime('%m')
        cur.execute(
            "SELECT pedido_numero FROM pedidos WHERE pedido_numero LIKE %s ORDER BY pedido_numero DESC LIMIT 1",
            (f'PED-{anio}-{mes}-%',)
        )
        ultimo = cur.fetchone()
        siguiente = 1
        if ultimo and ultimo[0]:
            partes = ultimo[0].split('-')
            if len(partes) == 4:
                siguiente = int(partes[3]) + 1
        return f'PED-{anio}-{mes}-{siguiente:04d}'

    def guardar(self, datos, usuario_creacion=None):
        detalles = datos.get('detalles') or []
        if not detalles:
            raise ValueError('El pedido debe tener al menos un ítem.')

        def _crear(cur):
            numero = self._generarNumero(cur)
            subtotal = sum(float(d['item_cantidad']) * float(d['item_precio_unitario']) - float(d.get('item_descuento') or 0) for d in detalles)
            descuento = float(datos.get('pedido_descuento') or 0)

            cur.execute(
                """
                INSERT INTO pedidos(
                    pedido_numero, id_paciente, id_profesional, fecha_pedido, fecha_entrega,
                    pedido_subtotal, pedido_descuento, pedido_total, observaciones,
                    pedido_estado, usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_pedido
                """,
                (numero, datos['id_paciente'], datos.get('id_profesional'), datos['fecha_pedido'],
                 datos.get('fecha_entrega'), subtotal, descuento, subtotal - descuento,
                 datos.get('observaciones'), 'PENDIENTE', usuario_creacion)
            )
            id_pedido = cur.fetchone()[0]

            for d in detalles:
                item_subtotal = float(d['item_cantidad']) * float(d['item_precio_unitario']) - float(d.get('item_descuento') or 0)
                cur.execute(
                    """
                    INSERT INTO pedido_detalle(
                        id_pedido, id_item_servicio, item_descripcion, item_cantidad,
                        item_precio_unitario, item_descuento, item_subtotal, observaciones,
                        usuario_creacion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (id_pedido, d.get('id_item_servicio'), d['item_descripcion'],
                     d['item_cantidad'], d['item_precio_unitario'], d.get('item_descuento') or 0,
                     item_subtotal, d.get('observaciones'), usuario_creacion)
                )
            return id_pedido

        return self.execute_transaction(_crear)

    def actualizarEstado(self, id_pedido, nuevo_estado, usuario_modificacion=None):
        sql = "UPDATE pedidos SET pedido_estado = %s, usuario_modificacion = %s WHERE id_pedido = %s"
        return self.execute_query(sql, (nuevo_estado, usuario_modificacion, id_pedido), commit=True) > 0

    def desactivar(self, id_pedido, usuario_modificacion=None):
        sql = "UPDATE pedidos SET est_pedido = FALSE, usuario_modificacion = %s WHERE id_pedido = %s"
        return self.execute_query(sql, (usuario_modificacion, id_pedido), commit=True) > 0
