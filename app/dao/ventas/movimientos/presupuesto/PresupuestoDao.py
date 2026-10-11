from app.core.base_dao import BaseDAO
from app.core.moneda import get_moneda, redondear
from app.dao.ventas.movimientos.pedido.PedidoDao import PedidoDao
from datetime import date


class PresupuestoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPresupuestos(self):
        sql = """
            SELECT p.id_presupuesto, p.presupuesto_numero, p.id_paciente, p.id_profesional,
                   p.fecha_presupuesto, p.fecha_validez, p.presupuesto_subtotal,
                   p.presupuesto_descuento, p.presupuesto_total, p.id_moneda, p.observaciones,
                   p.presupuesto_estado, p.est_presupuesto,
                   CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                   pp.per_cedula AS paciente_cedula,
                   CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                   m.cod_moneda, m.simbolo_moneda, m.decimales_moneda
            FROM presupuestos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN monedas m ON p.id_moneda = m.id_moneda
            LEFT JOIN funcionarios f ON p.id_profesional = f.id_funcionario
            LEFT JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE p.est_presupuesto = TRUE
            ORDER BY p.fecha_presupuesto DESC, p.id_presupuesto DESC
        """
        presupuestos = self.execute_query(sql)
        for p in presupuestos:
            p['fecha_presupuesto'] = p['fecha_presupuesto'].strftime('%Y-%m-%d') if p['fecha_presupuesto'] else None
            p['fecha_validez'] = p['fecha_validez'].strftime('%Y-%m-%d') if p['fecha_validez'] else None
        return presupuestos

    def getPresupuestoById(self, id_presupuesto):
        sql = """
            SELECT p.id_presupuesto, p.presupuesto_numero, p.id_paciente, p.id_profesional,
                   p.fecha_presupuesto, p.fecha_validez, p.presupuesto_subtotal,
                   p.presupuesto_descuento, p.presupuesto_total, p.id_moneda, p.observaciones,
                   p.presupuesto_estado,
                   CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                   pp.per_cedula AS paciente_cedula,
                   CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                   m.cod_moneda, m.simbolo_moneda, m.decimales_moneda
            FROM presupuestos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN monedas m ON p.id_moneda = m.id_moneda
            LEFT JOIN funcionarios f ON p.id_profesional = f.id_funcionario
            LEFT JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE p.id_presupuesto = %s AND p.est_presupuesto = TRUE
        """
        presupuesto = self.execute_query_one(sql, (id_presupuesto,))
        if not presupuesto:
            return None
        presupuesto['fecha_presupuesto'] = presupuesto['fecha_presupuesto'].strftime('%Y-%m-%d') if presupuesto['fecha_presupuesto'] else None
        presupuesto['fecha_validez'] = presupuesto['fecha_validez'].strftime('%Y-%m-%d') if presupuesto['fecha_validez'] else None
        presupuesto['detalles'] = self.getDetallePresupuesto(id_presupuesto)
        return presupuesto

    def getDetallePresupuesto(self, id_presupuesto):
        sql = """
            SELECT pd.id_presupuesto_detalle, pd.id_presupuesto, pd.id_item_servicio,
                   pd.item_descripcion, pd.item_cantidad, pd.item_precio_unitario,
                   pd.item_descuento, pd.item_subtotal, pd.observaciones
            FROM presupuesto_detalle pd
            WHERE pd.id_presupuesto = %s AND pd.est_presupuesto_detalle = TRUE
            ORDER BY pd.id_presupuesto_detalle
        """
        return self.execute_query(sql, (id_presupuesto,))

    def _generarNumero(self, cur):
        anio = date.today().year
        mes = date.today().strftime('%m')
        cur.execute(
            "SELECT presupuesto_numero FROM presupuestos WHERE presupuesto_numero LIKE %s ORDER BY presupuesto_numero DESC LIMIT 1",
            (f'PRES-{anio}-{mes}-%',)
        )
        ultimo = cur.fetchone()
        siguiente = 1
        if ultimo and ultimo[0]:
            partes = ultimo[0].split('-')
            if len(partes) == 4:
                siguiente = int(partes[3]) + 1
        return f'PRES-{anio}-{mes}-{siguiente:04d}'

    def guardar(self, datos, usuario_creacion=None):
        detalles = datos.get('detalles') or []
        if not detalles:
            raise ValueError('El presupuesto debe tener al menos un ítem.')

        def _crear(cur):
            moneda = get_moneda(datos.get('id_moneda'), cur)
            id_moneda = moneda['id_moneda']
            decimales = int(moneda['decimales_moneda'])

            numero = self._generarNumero(cur)
            subtotal = sum(
                redondear(float(d['item_cantidad']) * float(d['item_precio_unitario']) - float(d.get('item_descuento') or 0), decimales)
                for d in detalles
            )
            descuento = redondear(datos.get('presupuesto_descuento') or 0, decimales)

            cur.execute(
                """
                INSERT INTO presupuestos(
                    presupuesto_numero, id_paciente, id_profesional, fecha_presupuesto, fecha_validez,
                    presupuesto_subtotal, presupuesto_descuento, presupuesto_total, id_moneda, observaciones,
                    presupuesto_estado, usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_presupuesto
                """,
                (numero, datos['id_paciente'], datos.get('id_profesional'), datos['fecha_presupuesto'],
                 datos.get('fecha_validez'), subtotal, descuento, subtotal - descuento, id_moneda,
                 datos.get('observaciones'), 'PENDIENTE', usuario_creacion)
            )
            id_presupuesto = cur.fetchone()[0]

            for d in detalles:
                item_subtotal = redondear(float(d['item_cantidad']) * float(d['item_precio_unitario']) - float(d.get('item_descuento') or 0), decimales)
                cur.execute(
                    """
                    INSERT INTO presupuesto_detalle(
                        id_presupuesto, id_item_servicio, item_descripcion, item_cantidad,
                        item_precio_unitario, item_descuento, item_subtotal, observaciones,
                        usuario_creacion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (id_presupuesto, d.get('id_item_servicio'), d['item_descripcion'],
                     d['item_cantidad'], d['item_precio_unitario'], d.get('item_descuento') or 0,
                     item_subtotal, d.get('observaciones'), usuario_creacion)
                )
            return id_presupuesto

        return self.execute_transaction(_crear)

    def actualizarEstado(self, id_presupuesto, nuevo_estado, usuario_modificacion=None):
        sql = "UPDATE presupuestos SET presupuesto_estado = %s, usuario_modificacion = %s WHERE id_presupuesto = %s"
        return self.execute_query(sql, (nuevo_estado, usuario_modificacion, id_presupuesto), commit=True) > 0

    def convertirEnPedido(self, id_presupuesto, usuario=None):
        """Crea un pedido con el paciente, profesional, moneda, descuento e ítems del
        presupuesto aprobado y lo marca CONVERTIDO, en una sola transacción.
        Devuelve el número del pedido creado."""
        presupuesto = self.getPresupuestoById(id_presupuesto)
        if not presupuesto:
            raise ValueError('No se encontró el presupuesto.')

        def _convertir(cur):
            # Bloqueo + revalidación del estado: evita convertir dos veces el mismo presupuesto
            cur.execute(
                "SELECT presupuesto_estado FROM presupuestos WHERE id_presupuesto = %s FOR UPDATE",
                (id_presupuesto,)
            )
            if cur.fetchone()[0] != 'APROBADO':
                raise ValueError('Solo se puede convertir en pedido un presupuesto aprobado.')

            id_pedido = PedidoDao().crearEnTransaccion(cur, {
                'id_paciente': presupuesto['id_paciente'],
                'id_profesional': presupuesto['id_profesional'],
                'id_moneda': presupuesto['id_moneda'],
                'fecha_pedido': date.today(),
                'pedido_descuento': presupuesto['presupuesto_descuento'],
                'observaciones': f"Generado desde el presupuesto {presupuesto['presupuesto_numero']}.",
                'detalles': [{
                    'id_item_servicio': d['id_item_servicio'],
                    'item_descripcion': d['item_descripcion'],
                    'item_cantidad': d['item_cantidad'],
                    'item_precio_unitario': d['item_precio_unitario'],
                    'item_descuento': d['item_descuento'],
                    'observaciones': d['observaciones'],
                } for d in presupuesto['detalles']],
            }, usuario)

            cur.execute(
                "UPDATE presupuestos SET presupuesto_estado = 'CONVERTIDO', usuario_modificacion = %s WHERE id_presupuesto = %s",
                (usuario, id_presupuesto)
            )
            cur.execute("SELECT pedido_numero FROM pedidos WHERE id_pedido = %s", (id_pedido,))
            return cur.fetchone()[0]

        return self.execute_transaction(_convertir)

    def desactivar(self, id_presupuesto, usuario_modificacion=None):
        sql = "UPDATE presupuestos SET est_presupuesto = FALSE, usuario_modificacion = %s WHERE id_presupuesto = %s"
        return self.execute_query(sql, (usuario_modificacion, id_presupuesto), commit=True) > 0
