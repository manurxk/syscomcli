from datetime import datetime
from flask import current_app as app
from app.core.base_dao import BaseDAO
from decimal import Decimal

from app.core.moneda import redondear
from app.dao.ventas.movimientos.cuenta_cobrar.CuentaCobrarDao import CuentaCobrarDao


class NotaDebitoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getNotasDebito(self):
        sql = """
            SELECT
                nd.id_nota_debito,
                nd.nota_debito_numero,
                nd.id_factura,
                nd.id_tipo_comprobante,
                nd.motivo_nota_debito,
                nd.monto_total,
                nd.codigo_sifen,
                nd.numero_timbrado,
                nd.observaciones,
                nd.est_nota_debito,
                f.factura_numero,
                f.id_moneda, mo.cod_moneda, mo.simbolo_moneda, mo.decimales_moneda,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica,
                tc.des_tipo_comprobante,
                TO_CHAR(nd.fecha_nota_debito, 'DD/MM/YYYY') AS fecha_nota_debito_fmt,
                TO_CHAR(nd.fecha_creacion,    'DD/MM/YYYY') AS fecha_registro
            FROM notas_debito nd
            JOIN facturas f           ON nd.id_factura          = f.id_factura
            JOIN pacientes pac        ON f.id_paciente           = pac.id_paciente
            JOIN personas pp          ON pac.id_persona          = pp.id_persona
            JOIN monedas mo           ON f.id_moneda           = mo.id_moneda
            LEFT JOIN tipos_comprobantes tc ON nd.id_tipo_comprobante = tc.id_tipo_comprobante
            ORDER BY nd.fecha_nota_debito DESC, nd.id_nota_debito DESC
        """
        return self.execute_query(sql)

    def getNotaDebitoById(self, id_nota_debito):
        sql = """
            SELECT
                nd.id_nota_debito,
                nd.nota_debito_numero,
                nd.id_factura,
                nd.id_tipo_comprobante,
                nd.motivo_nota_debito,
                nd.monto_total,
                nd.codigo_sifen,
                nd.numero_timbrado,
                nd.observaciones,
                nd.est_nota_debito,
                nd.usuario_creacion,
                f.factura_numero,
                f.factura_total,
                f.id_moneda, mo.cod_moneda, mo.simbolo_moneda, mo.decimales_moneda,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica,
                tc.des_tipo_comprobante,
                TO_CHAR(nd.fecha_nota_debito, 'DD/MM/YYYY HH24:MI') AS fecha_nota_debito_fmt,
                TO_CHAR(nd.fecha_creacion,    'DD/MM/YYYY')          AS fecha_registro
            FROM notas_debito nd
            JOIN facturas f           ON nd.id_factura          = f.id_factura
            JOIN pacientes pac        ON f.id_paciente           = pac.id_paciente
            JOIN personas pp          ON pac.id_persona          = pp.id_persona
            JOIN monedas mo           ON f.id_moneda           = mo.id_moneda
            LEFT JOIN tipos_comprobantes tc ON nd.id_tipo_comprobante = tc.id_tipo_comprobante
            WHERE nd.id_nota_debito = %s
        """
        return self.execute_query_one(sql, (id_nota_debito,))

    def getNotaDebitoDetalle(self, id_nota_debito):
        sql = """
            SELECT
                id_nota_debito_detalle,
                id_nota_debito,
                id_factura_detalle,
                item_descripcion,
                item_cantidad,
                item_precio_unitario,
                monto_total
            FROM nota_debito_detalle
            WHERE id_nota_debito = %s
            ORDER BY id_nota_debito_detalle
        """
        return self.execute_query(sql, (id_nota_debito,))

    def _generarNumero(self, cur):
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        patron = f'ND-{año}-{mes}-%'
        cur.execute(
            "SELECT nota_debito_numero FROM notas_debito "
            "WHERE nota_debito_numero LIKE %s ORDER BY nota_debito_numero DESC LIMIT 1",
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
        return f'ND-{año}-{mes}-{siguiente:04d}'

    def guardar(self, data, usuario_creacion=None):
        detalles = data.get('detalles') or []
        if not detalles:
            raise ValueError('La nota de débito debe tener al menos un ítem.')

        def _op(cur):
            numero = self._generarNumero(cur)

            cur.execute("SELECT id_moneda, decimales_moneda FROM facturas f JOIN monedas m USING(id_moneda) WHERE f.id_factura = %s", (data['id_factura'],))
            fila_moneda = cur.fetchone()
            if not fila_moneda:
                raise ValueError('La factura indicada no existe.')
            id_moneda, decimales = fila_moneda

            monto_total = sum(
                redondear(d.get('monto_total') or 0, decimales) or
                redondear(Decimal(str(d.get('item_cantidad', 1))) * Decimal(str(d.get('item_precio_unitario', 0))), decimales)
                for d in detalles
            )

            # Suma el cargo a la deuda de la factura
            CuentaCobrarDao().ajustarPorNotaEnTransaccion(cur, data['id_factura'], monto_total, usuario_creacion)

            cur.execute("""
                INSERT INTO notas_debito(
                    nota_debito_numero, id_factura, id_tipo_comprobante,
                    motivo_nota_debito, monto_total,
                    codigo_sifen, numero_timbrado, observaciones,
                    est_nota_debito, usuario_creacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'REGISTRADA', %s)
                RETURNING id_nota_debito
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
            id_nd = cur.fetchone()[0]

            for d in detalles:
                mt = redondear(d.get('monto_total') or 0, decimales) or (
                    redondear(Decimal(str(d.get('item_cantidad', 1))) * Decimal(str(d.get('item_precio_unitario', 0))), decimales)
                )
                cur.execute("""
                    INSERT INTO nota_debito_detalle(
                        id_nota_debito, id_factura_detalle, item_descripcion,
                        item_cantidad, item_precio_unitario, monto_total
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    id_nd,
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
                    id_paciente, id_factura, id_nota_debito,
                    monto_gravado, monto_exento, monto_iva, monto_total,
                    numero_timbrado, usuario_creacion, id_moneda
                )
                VALUES (%s, 'NOTA_DEBITO', %s, %s, %s, %s, %s, 0, 0, %s, %s, %s, %s)
            """, (
                data.get('fecha_nota_debito') or datetime.now().date(),
                numero,
                id_paciente,
                data['id_factura'],
                id_nd,
                monto_total,
                monto_total,
                num_tim,
                usuario_creacion,
                id_moneda,
            ))

            app.logger.info(f"Nota de débito creada: {numero} (ID={id_nd})")
            return id_nd

        return self.execute_transaction(_op)

    def anular(self, id_nota_debito, usuario=None):
        """Anula la nota y quita de la cuenta a cobrar el cargo que había sumado."""
        def _op(cur):
            cur.execute("""
                UPDATE notas_debito
                SET est_nota_debito = 'ANULADA',
                    fecha_modificacion = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_nota_debito = %s AND est_nota_debito != 'ANULADA'
                RETURNING id_factura, monto_total
            """, (usuario, id_nota_debito))
            fila = cur.fetchone()
            if not fila:
                return False
            CuentaCobrarDao().ajustarPorNotaEnTransaccion(cur, fila[0], -fila[1], usuario)
            # En el libro de ventas la nota anulada sigue figurando, pero en 0
            cur.execute("""
                UPDATE libro_ventas
                SET monto_gravado = 0, monto_exento = 0, monto_iva = 0, monto_total = 0
                WHERE id_nota_debito = %s
            """, (id_nota_debito,))
            return True

        return self.execute_transaction(_op)
