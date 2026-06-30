from app.core.base_dao import BaseDAO
from datetime import date


class PresupuestoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPresupuestos(self):
        sql = """
            SELECT p.id_presupuesto, p.presupuesto_numero, p.id_paciente, p.id_profesional,
                   p.fecha_presupuesto, p.fecha_validez, p.presupuesto_subtotal,
                   p.presupuesto_descuento, p.presupuesto_total, p.observaciones,
                   p.presupuesto_estado, p.est_presupuesto,
                   CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                   pp.per_cedula AS paciente_cedula,
                   CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre
            FROM presupuestos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
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
                   p.presupuesto_descuento, p.presupuesto_total, p.observaciones,
                   p.presupuesto_estado,
                   CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                   pp.per_cedula AS paciente_cedula,
                   CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre
            FROM presupuestos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
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
            numero = self._generarNumero(cur)
            subtotal = sum(float(d['item_cantidad']) * float(d['item_precio_unitario']) - float(d.get('item_descuento') or 0) for d in detalles)
            descuento = float(datos.get('presupuesto_descuento') or 0)

            cur.execute(
                """
                INSERT INTO presupuestos(
                    presupuesto_numero, id_paciente, id_profesional, fecha_presupuesto, fecha_validez,
                    presupuesto_subtotal, presupuesto_descuento, presupuesto_total, observaciones,
                    presupuesto_estado, usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_presupuesto
                """,
                (numero, datos['id_paciente'], datos.get('id_profesional'), datos['fecha_presupuesto'],
                 datos.get('fecha_validez'), subtotal, descuento, subtotal - descuento,
                 datos.get('observaciones'), 'PENDIENTE', usuario_creacion)
            )
            id_presupuesto = cur.fetchone()[0]

            for d in detalles:
                item_subtotal = float(d['item_cantidad']) * float(d['item_precio_unitario']) - float(d.get('item_descuento') or 0)
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

    def desactivar(self, id_presupuesto, usuario_modificacion=None):
        sql = "UPDATE presupuestos SET est_presupuesto = FALSE, usuario_modificacion = %s WHERE id_presupuesto = %s"
        return self.execute_query(sql, (usuario_modificacion, id_presupuesto), commit=True) > 0
