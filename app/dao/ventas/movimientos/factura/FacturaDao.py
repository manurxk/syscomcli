from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from flask import current_app as app
from app.core.base_dao import BaseDAO


# ── numero_a_letras ────────────────────────────────────────────────────────
# Reutilizado tal cual del legacy (app/dao/legacy/modulos/ventas/factura/FacturaDao.py)
def numero_a_letras(monto) -> str:
    """Convierte un monto (int o Decimal) a texto en guaraníes. Rango 0-999 999 999."""
    UNIDADES = [
        '', 'un', 'dos', 'tres', 'cuatro', 'cinco',
        'seis', 'siete', 'ocho', 'nueve', 'diez',
        'once', 'doce', 'trece', 'catorce', 'quince',
        'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve',
        'veinte', 'veintiún', 'veintidós', 'veintitrés', 'veinticuatro',
        'veinticinco', 'veintiséis', 'veintisiete', 'veintiocho', 'veintinueve'
    ]
    DECENAS = [
        '', '', 'veinte', 'treinta', 'cuarenta', 'cincuenta',
        'sesenta', 'setenta', 'ochenta', 'noventa'
    ]
    CENTENAS = [
        '', 'cien', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos',
        'seiscientos', 'setecientos', 'ochocientos', 'novecientos'
    ]

    def _cientos(n: int) -> str:
        if n == 0:
            return ''
        c = n // 100
        resto = n % 100
        texto_c = ''
        if c > 0:
            if c == 1 and resto > 0:
                texto_c = 'ciento'
            elif c == 1:
                texto_c = 'cien'
            else:
                texto_c = CENTENAS[c]
        texto_r = ''
        if 1 <= resto <= 29:
            texto_r = UNIDADES[resto]
            if resto == 21:
                texto_r = 'veintiún'
        elif resto >= 30:
            d = resto // 10
            u = resto % 10
            texto_r = DECENAS[d]
            if u > 0:
                texto_r += ' y ' + UNIDADES[u]
        partes = [p for p in [texto_c, texto_r] if p]
        return ' '.join(partes)

    monto_int = int(Decimal(str(monto)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    if monto_int == 0:
        return 'Cero Guaraníes'
    if monto_int < 0 or monto_int > 999_999_999:
        raise ValueError(f'Monto fuera de rango para numero_a_letras: {monto_int}')

    millones = monto_int // 1_000_000
    miles = (monto_int % 1_000_000) // 1_000
    resto = monto_int % 1_000

    partes = []
    if millones > 0:
        partes.append('un millón' if millones == 1 else _cientos(millones) + ' millones')
    if miles > 0:
        partes.append('mil' if miles == 1 else _cientos(miles) + ' mil')
    if resto > 0:
        partes.append(_cientos(resto))

    texto = ' '.join(partes)
    texto = texto[0].upper() + texto[1:] if texto else ''
    moneda = 'Guaraní' if monto_int == 1 else 'Guaraníes'
    return f'{texto} {moneda}'


# ── FacturaDao ─────────────────────────────────────────────────────────────
class FacturaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    # ── Consultas ─────────────────────────────────────────────────────────
    def getFacturas(self):
        sql = """
            SELECT
                f.id_factura, f.factura_numero, f.fecha_factura,
                f.factura_subtotal, f.factura_descuento,
                f.factura_impuestos, f.factura_total,
                f.observaciones,
                f.id_paciente, f.id_pedido,
                f.id_timbrado, f.id_punto_expedicion,
                f.id_tipo_comprobante, f.id_condicion_venta,
                f.id_moneda, f.id_estado_factura,
                f.fecha_vencimiento, f.codigo_sifen, f.numero_timbrado,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica,
                tc.des_tipo_comprobante,
                cv.des_condicion_venta,
                ef.des_estado_factura,
                m.cod_moneda, m.simbolo_moneda,
                TO_CHAR(f.fecha_factura, 'DD/MM/YYYY') AS fecha_factura_fmt,
                TO_CHAR(f.fecha_creacion, 'DD/MM/YYYY') AS fecha_registro
            FROM facturas f
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON f.id_tipo_comprobante = tc.id_tipo_comprobante
            JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            JOIN estados_factura ef ON f.id_estado_factura = ef.id_estado_factura
            JOIN monedas m ON f.id_moneda = m.id_moneda
            ORDER BY f.fecha_factura DESC, f.id_factura DESC
        """
        return self.execute_query(sql)

    def getFacturaById(self, id_factura):
        sql = """
            SELECT
                f.id_factura, f.factura_numero, f.fecha_factura, f.fecha_vencimiento,
                f.factura_subtotal, f.factura_descuento, f.factura_impuestos, f.factura_total,
                f.factura_total_letras, f.codigo_sifen, f.numero_timbrado, f.observaciones,
                f.id_paciente, f.id_pedido, f.id_timbrado, f.id_punto_expedicion,
                f.id_tipo_comprobante, f.id_condicion_venta, f.id_moneda, f.id_estado_factura,
                f.fecha_anulacion,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula, pp.per_telefono AS paciente_telefono,
                pac.pac_historia_clinica,
                tc.des_tipo_comprobante,
                cv.des_condicion_venta, cv.dias_credito,
                ef.des_estado_factura,
                m.cod_moneda, m.simbolo_moneda,
                t.numero_timbrado AS timbrado_numero, t.codigo_establecimiento,
                pe.codigo_punto_expedicion, pe.nombre_punto_expedicion
            FROM facturas f
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON f.id_tipo_comprobante = tc.id_tipo_comprobante
            JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            JOIN estados_factura ef ON f.id_estado_factura = ef.id_estado_factura
            JOIN monedas m ON f.id_moneda = m.id_moneda
            LEFT JOIN timbrados t ON f.id_timbrado = t.id_timbrado
            LEFT JOIN puntos_expedicion pe ON f.id_punto_expedicion = pe.id_punto_expedicion
            WHERE f.id_factura = %s
        """
        return self.execute_query_one(sql, (id_factura,))

    def getFacturaDetalle(self, id_factura):
        sql = """
            SELECT
                fd.id_factura_detalle, fd.id_factura, fd.id_item_servicio,
                fd.id_tipo_item, fd.id_consulta, fd.item_descripcion,
                fd.item_cantidad, fd.item_precio_unitario, fd.item_precio_con_iva,
                fd.item_descuento, fd.item_subtotal,
                fd.id_tipo_impuesto, fd.impuesto_porcentaje, fd.impuesto_monto,
                fd.item_total,
                ti.des_tipo_item,
                timp.des_tipo_impuesto
            FROM factura_detalle fd
            LEFT JOIN tipos_items ti ON fd.id_tipo_item = ti.id_tipo_item
            LEFT JOIN tipos_impuestos timp ON fd.id_tipo_impuesto = timp.id_tipo_impuesto
            WHERE fd.id_factura = %s
            ORDER BY fd.id_factura_detalle
        """
        return self.execute_query(sql, (id_factura,))

    # ── Helpers internos ─────────────────────────────────────────────────
    @staticmethod
    def _calcularItem(d: dict) -> dict:
        """Descompone IVA en un ítem. El precio ingresado ya incluye IVA."""
        p_con_iva = Decimal(str(d.get('item_precio_con_iva', 0)))
        cantidad = Decimal(str(d.get('item_cantidad', 1)))
        descuento = Decimal(str(d.get('item_descuento', 0)))
        tasa = Decimal(str(d.get('impuesto_porcentaje', 0)))

        total = (p_con_iva * cantidad) - descuento
        divisor = Decimal('1') + (tasa / Decimal('100'))
        subtotal = (total / divisor).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        iva_monto = total - subtotal
        precio_base = (subtotal / cantidad).quantize(Decimal('1'), rounding=ROUND_HALF_UP) if cantidad > 0 else Decimal('0')

        return {
            'item_descripcion': d.get('item_descripcion', ''),
            'item_cantidad': int(cantidad),
            'item_precio_con_iva': int(p_con_iva),
            'item_precio_unitario': int(precio_base),
            'item_descuento': int(descuento),
            'item_subtotal': int(subtotal),
            'impuesto_porcentaje': float(tasa),
            'impuesto_monto': int(iva_monto),
            'item_total': int(total),
            'id_item_servicio': d.get('id_item_servicio'),
            'id_tipo_item': d.get('id_tipo_item'),
            'id_consulta': d.get('id_consulta'),
            'id_tipo_impuesto': d.get('id_tipo_impuesto'),
        }

    # ── Guardar (transacción completa) ───────────────────────────────────
    def guardar(self, data: dict, usuario_creacion=None):
        """
        Crea una factura con detalle en una transacción única.
        Pasos: número → INSERT factura → INSERT detalle → INSERT libro_ventas
               → si CREDITO: INSERT cuentas_cobrar → si pedido: UPDATE pedido FACTURADO
        """
        detalles_raw = data.get('detalles') or []
        if not detalles_raw:
            raise ValueError('La factura debe tener al menos un ítem en el detalle.')

        # Pre-cargar porcentajes de impuesto para ítems que envíen id_tipo_impuesto
        ids_impuesto = list({d['id_tipo_impuesto'] for d in detalles_raw if d.get('id_tipo_impuesto') and not d.get('impuesto_porcentaje')})
        porc_map: dict = {}
        if ids_impuesto:
            placeholders = ','.join(['%s'] * len(ids_impuesto))
            rows_ti = self.execute_query(
                f"SELECT id_tipo_impuesto, porcentaje_impuesto FROM tipos_impuestos WHERE id_tipo_impuesto IN ({placeholders})",
                tuple(ids_impuesto)
            )
            porc_map = {r['id_tipo_impuesto']: float(r['porcentaje_impuesto']) for r in rows_ti}

        detalles_enriquecidos = []
        for d in detalles_raw:
            item = dict(d)
            if not item.get('impuesto_porcentaje') and item.get('id_tipo_impuesto'):
                item['impuesto_porcentaje'] = porc_map.get(item['id_tipo_impuesto'], 0)
            detalles_enriquecidos.append(item)

        detalles_calc = [self._calcularItem(d) for d in detalles_enriquecidos]

        def _fn(cur):
            id_timbrado = data['id_timbrado']
            id_punto_expedicion = data['id_punto_expedicion']

            # 1. Generar número de factura con bloqueo de fila
            cur.execute("""
                SELECT t.codigo_establecimiento, pe.codigo_punto_expedicion,
                       pe.ultimo_numero_usado
                FROM puntos_expedicion pe
                JOIN timbrados t ON pe.id_timbrado = t.id_timbrado
                WHERE pe.id_punto_expedicion = %s
                FOR UPDATE
            """, (id_punto_expedicion,))
            row = cur.fetchone()
            if not row:
                raise ValueError('Punto de expedición no encontrado.')
            cod_estab, cod_punto, ultimo = row
            siguiente = ultimo + 1
            cur.execute(
                "UPDATE puntos_expedicion SET ultimo_numero_usado=%s WHERE id_punto_expedicion=%s",
                (siguiente, id_punto_expedicion)
            )
            factura_numero = f"{cod_estab}-{cod_punto}-{siguiente:07d}"

            # 2. Número de timbrado denormalizado para PDF
            cur.execute("SELECT numero_timbrado FROM timbrados WHERE id_timbrado=%s", (id_timbrado,))
            num_tim_row = cur.fetchone()
            numero_timbrado = num_tim_row[0] if num_tim_row else None

            # 3. Totales
            subtotal = sum(d['item_subtotal'] for d in detalles_calc)
            impuestos = sum(d['impuesto_monto'] for d in detalles_calc)
            descuento = int(data.get('factura_descuento', 0))
            total = subtotal + impuestos - descuento
            try:
                total_letras = numero_a_letras(total)
            except Exception:
                total_letras = None

            # 4. Fecha de vencimiento (si condición tiene días_credito)
            fecha_vencimiento = data.get('fecha_vencimiento')
            if not fecha_vencimiento:
                cur.execute(
                    "SELECT dias_credito FROM condiciones_venta WHERE id_condicion_venta=%s",
                    (data['id_condicion_venta'],)
                )
                cond_row = cur.fetchone()
                dias = cond_row[0] if cond_row and cond_row[0] else 0
                if dias > 0:
                    fecha_fac = data['fecha_factura']
                    if isinstance(fecha_fac, str):
                        from datetime import datetime
                        fecha_fac = datetime.strptime(fecha_fac, '%Y-%m-%d').date()
                    fecha_vencimiento = fecha_fac + timedelta(days=dias)

            # 5. INSERT factura
            cur.execute("""
                INSERT INTO facturas(
                    factura_numero, id_paciente, id_pedido,
                    id_timbrado, id_punto_expedicion,
                    id_tipo_comprobante, id_condicion_venta, id_moneda, id_estado_factura,
                    fecha_factura, fecha_vencimiento,
                    factura_subtotal, factura_descuento, factura_impuestos, factura_total,
                    factura_total_letras, codigo_sifen, numero_timbrado,
                    observaciones, usuario_creacion
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_factura
            """, (
                factura_numero,
                data['id_paciente'],
                data.get('id_pedido'),
                id_timbrado,
                id_punto_expedicion,
                data['id_tipo_comprobante'],
                data['id_condicion_venta'],
                data.get('id_moneda', 1),
                data['id_estado_factura'],
                data['fecha_factura'],
                fecha_vencimiento,
                subtotal,
                descuento,
                impuestos,
                total,
                total_letras,
                data.get('codigo_sifen'),
                numero_timbrado,
                data.get('observaciones'),
                usuario_creacion,
            ))
            id_factura = cur.fetchone()[0]

            # 6. INSERT factura_detalle
            for d in detalles_calc:
                cur.execute("""
                    INSERT INTO factura_detalle(
                        id_factura, id_item_servicio, id_tipo_item, id_consulta,
                        item_descripcion, item_cantidad,
                        item_precio_unitario, item_precio_con_iva,
                        item_descuento, item_subtotal,
                        id_tipo_impuesto, impuesto_porcentaje, impuesto_monto, item_total
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    id_factura,
                    d['id_item_servicio'], d['id_tipo_item'], d['id_consulta'],
                    d['item_descripcion'], d['item_cantidad'],
                    d['item_precio_unitario'], d['item_precio_con_iva'],
                    d['item_descuento'], d['item_subtotal'],
                    d['id_tipo_impuesto'], d['impuesto_porcentaje'],
                    d['impuesto_monto'], d['item_total'],
                ))

            # 7. INSERT libro_ventas
            cur.execute("""
                INSERT INTO libro_ventas(
                    libro_fecha, tipo_comprobante, numero_comprobante,
                    id_paciente, id_factura,
                    monto_gravado, monto_exento, monto_iva, monto_total,
                    numero_timbrado, usuario_creacion
                )
                VALUES (%s,'FACTURA',%s,%s,%s,%s,0,%s,%s,%s,%s)
            """, (
                data['fecha_factura'],
                factura_numero,
                data['id_paciente'],
                id_factura,
                subtotal,
                impuestos,
                total,
                numero_timbrado,
                usuario_creacion,
            ))

            # 8. Si condición es crédito (dias_credito > 0): INSERT cuentas_cobrar
            cur.execute(
                "SELECT dias_credito FROM condiciones_venta WHERE id_condicion_venta=%s",
                (data['id_condicion_venta'],)
            )
            cond = cur.fetchone()
            if cond and cond[0] and cond[0] > 0:
                año = datetime.now().year
                cur.execute(
                    "SELECT cuenta_numero FROM cuentas_cobrar WHERE cuenta_numero LIKE %s "
                    "ORDER BY cuenta_numero DESC LIMIT 1",
                    (f'CTA-{año}-%',)
                )
                ult = cur.fetchone()
                num_cta = int(ult[0].split('-')[2]) + 1 if ult else 1
                cur.execute("""
                    INSERT INTO cuentas_cobrar(
                        cuenta_numero, id_factura, id_paciente,
                        fecha_vencimiento, monto_total, monto_pendiente, usuario_creacion
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (
                    f'CTA-{año}-{num_cta:04d}',
                    id_factura,
                    data['id_paciente'],
                    fecha_vencimiento,
                    total,
                    total,
                    usuario_creacion,
                ))

            # 9. Si tiene pedido: marcar como FACTURADO
            if data.get('id_pedido'):
                cur.execute(
                    "UPDATE pedidos SET pedido_estado='FACTURADO', usuario_modificacion=%s "
                    "WHERE id_pedido=%s",
                    (usuario_creacion, data['id_pedido'])
                )

            app.logger.info(f"Factura creada: {factura_numero} (ID={id_factura})")
            return id_factura

        return self.execute_transaction(_fn)

    # ── Cambio de estado ─────────────────────────────────────────────────
    def anular(self, id_factura, usuario_anulacion=None):
        """Anula una factura (soft delete: fecha_anulacion + estado ANULADA)."""
        sql_estado = """
            SELECT id_estado_factura FROM estados_factura
            WHERE UPPER(des_estado_factura) = 'ANULADA' LIMIT 1
        """
        est = self.execute_query_one(sql_estado)
        if not est:
            raise ValueError("No existe el estado ANULADA en estados_factura.")
        sql = """
            UPDATE facturas
            SET id_estado_factura=%s,
                fecha_anulacion=now(),
                usuario_anulacion=%s,
                usuario_modificacion=%s
            WHERE id_factura=%s AND fecha_anulacion IS NULL
        """
        return self.execute_query(
            sql,
            (est['id_estado_factura'], usuario_anulacion, usuario_anulacion, id_factura),
            commit=True
        ) > 0
