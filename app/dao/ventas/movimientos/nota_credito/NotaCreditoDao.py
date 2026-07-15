from datetime import datetime
from flask import current_app as app
from app.core.base_dao import BaseDAO


class NotaCreditoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getNotasCredito(self):
        sql = """
            SELECT
                nc.id_nota_credito,
                nc.nota_credito_numero,
                nc.id_factura,
                nc.id_tipo_comprobante,
                nc.motivo_nota_credito,
                nc.monto_total,
                nc.codigo_sifen,
                nc.numero_timbrado,
                nc.observaciones,
                nc.est_nota_credito,
                f.factura_numero,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica,
                tc.des_tipo_comprobante,
                TO_CHAR(nc.fecha_nota_credito, 'DD/MM/YYYY') AS fecha_nota_credito_fmt,
                TO_CHAR(nc.fecha_creacion,      'DD/MM/YYYY') AS fecha_registro
            FROM notas_credito nc
            JOIN facturas f           ON nc.id_factura          = f.id_factura
            JOIN pacientes pac        ON f.id_paciente           = pac.id_paciente
            JOIN personas pp          ON pac.id_persona          = pp.id_persona
            LEFT JOIN tipos_comprobantes tc ON nc.id_tipo_comprobante = tc.id_tipo_comprobante
            ORDER BY nc.fecha_nota_credito DESC, nc.id_nota_credito DESC
        """
        return self.execute_query(sql)

    def getNotaCreditoById(self, id_nota_credito):
        sql = """
            SELECT
                nc.id_nota_credito,
                nc.nota_credito_numero,
                nc.id_factura,
                nc.id_tipo_comprobante,
                nc.motivo_nota_credito,
                nc.monto_total,
                nc.codigo_sifen,
                nc.numero_timbrado,
                nc.observaciones,
                nc.est_nota_credito,
                nc.usuario_creacion,
                f.factura_numero,
                f.factura_total,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica,
                tc.des_tipo_comprobante,
                TO_CHAR(nc.fecha_nota_credito, 'DD/MM/YYYY HH24:MI') AS fecha_nota_credito_fmt,
                TO_CHAR(nc.fecha_creacion,      'DD/MM/YYYY')         AS fecha_registro
            FROM notas_credito nc
            JOIN facturas f           ON nc.id_factura          = f.id_factura
            JOIN pacientes pac        ON f.id_paciente           = pac.id_paciente
            JOIN personas pp          ON pac.id_persona          = pp.id_persona
            LEFT JOIN tipos_comprobantes tc ON nc.id_tipo_comprobante = tc.id_tipo_comprobante
            WHERE nc.id_nota_credito = %s
        """
        return self.execute_query_one(sql, (id_nota_credito,))

    def getNotaCreditoDetalle(self, id_nota_credito):
        sql = """
            SELECT
                id_nota_credito_detalle,
                id_nota_credito,
                id_factura_detalle,
                item_descripcion,
                item_cantidad,
                item_precio_unitario,
                monto_total
            FROM nota_credito_detalle
            WHERE id_nota_credito = %s
            ORDER BY id_nota_credito_detalle
        """
        return self.execute_query(sql, (id_nota_credito,))

    def _generarNumero(self, cur):
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        patron = f'NC-{año}-{mes}-%'
        cur.execute(
            "SELECT nota_credito_numero FROM notas_credito "
            "WHERE nota_credito_numero LIKE %s ORDER BY nota_credito_numero DESC LIMIT 1",
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
        return f'NC-{año}-{mes}-{siguiente:04d}'

    def guardar(self, data, usuario_creacion=None):
        detalles = data.get('detalles') or []
        if not detalles:
            raise ValueError('La nota de crédito debe tener al menos un ítem.')

        def _op(cur):
            numero = self._generarNumero(cur)

            monto_total = sum(
                int(d.get('monto_total') or 0) or
                int(d.get('item_cantidad', 1)) * int(d.get('item_precio_unitario', 0))
                for d in detalles
            )

            cur.execute("""
                INSERT INTO notas_credito(
                    nota_credito_numero, id_factura, id_tipo_comprobante,
                    motivo_nota_credito, monto_total,
                    codigo_sifen, numero_timbrado, observaciones,
                    est_nota_credito, usuario_creacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'REGISTRADA', %s)
                RETURNING id_nota_credito
            """, (
                numero,
                data['id_factura'],
                data.get('id_tipo_comprobante') or None,
                data['motivo'],
                monto_total,
                data.get('codigo_sifen') or None,
                data.get('numero_timbrado') or None,
                data.get('observaciones') or None,
                usuario_creacion,
            ))
            id_nc = cur.fetchone()[0]

            for d in detalles:
                mt = int(d.get('monto_total') or 0) or (
                    int(d.get('item_cantidad', 1)) * int(d.get('item_precio_unitario', 0))
                )
                cur.execute("""
                    INSERT INTO nota_credito_detalle(
                        id_nota_credito, id_factura_detalle, item_descripcion,
                        item_cantidad, item_precio_unitario, monto_total
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    id_nc,
                    d.get('id_factura_detalle') or None,
                    d['item_descripcion'],
                    d.get('item_cantidad', 1),
                    d.get('item_precio_unitario', 0),
                    mt,
                ))

            # Obtener id_paciente y numero_timbrado de la factura
            cur.execute(
                "SELECT id_paciente, numero_timbrado FROM facturas WHERE id_factura = %s",
                (data['id_factura'],)
            )
            fac = cur.fetchone()
            id_paciente = fac[0] if fac else None
            num_tim = fac[1] if fac else None

            cur.execute("""
                INSERT INTO libro_ventas(
                    libro_fecha, tipo_comprobante, numero_comprobante,
                    id_paciente, id_factura, id_nota_credito,
                    monto_gravado, monto_exento, monto_iva, monto_total,
                    numero_timbrado, usuario_creacion
                )
                VALUES (%s, 'NOTA_CREDITO', %s, %s, %s, %s, %s, 0, 0, %s, %s, %s)
            """, (
                data.get('fecha_nota_credito') or datetime.now().date(),
                numero,
                id_paciente,
                data['id_factura'],
                id_nc,
                monto_total,
                monto_total,
                num_tim,
                usuario_creacion,
            ))

            app.logger.info(f"Nota de crédito creada: {numero} (ID={id_nc})")
            return id_nc

        return self.execute_transaction(_op)

    def anular(self, id_nota_credito, usuario=None):
        filas = self.execute_query(
            """
            UPDATE notas_credito
            SET est_nota_credito = 'ANULADA',
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_nota_credito = %s AND est_nota_credito != 'ANULADA'
            """,
            (usuario, id_nota_credito),
            commit=True
        )
        return filas > 0
