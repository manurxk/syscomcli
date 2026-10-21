from datetime import datetime, timedelta
from decimal import Decimal

import psycopg2.errors

from flask import current_app as app
from app.core.base_dao import BaseDAO
from app.core.moneda import get_moneda, redondear
from app.dao.ventas.movimientos.cobranza.CobranzaDao import CobranzaDao


# ── numero_a_letras ────────────────────────────────────────────────────────
# Reutilizado tal cual del legacy (app/dao/legacy/modulos/ventas/factura/FacturaDao.py)
def numero_a_letras(monto, moneda=None) -> str:
    """Convierte un monto a texto. Sin `moneda` (o PYG) usa guaraníes; con otra moneda usa su nombre y los centavos como NN/100. Rango 0-999 999 999."""
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

    decimales = int(moneda['decimales_moneda']) if moneda else 0
    monto_dec = redondear(monto, decimales)
    monto_int = int(monto_dec)
    centavos = int((monto_dec - monto_int) * 100)
    if moneda and not moneda.get('es_moneda_local'):
        nombre_moneda = moneda['des_moneda'].title()
        nombre_uno = nombre_moneda
    else:
        nombre_moneda, nombre_uno = 'Guaraníes', 'Guaraní'
    if monto_int == 0 and centavos == 0:
        return f'Cero {nombre_moneda}'
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
    nombre = nombre_uno if monto_int == 1 else nombre_moneda
    if centavos:
        return f'{texto} {nombre} con {centavos:02d}/100'
    return f'{texto} {nombre}'


# ── FacturaDao ─────────────────────────────────────────────────────────────
class FacturaDao(BaseDAO):
    """Acceso a datos de factura (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    # ── Consultas ─────────────────────────────────────────────────────────
    def getFacturas(self):
        """Lista los registros de factura."""
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
                m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
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

    def getFacturasHoy(self):
        """Lista las facturas emitidas en la fecha actual."""
        sql = """
            SELECT f.id_factura, f.factura_numero, f.factura_total
            FROM facturas f
            WHERE f.fecha_factura = CURRENT_DATE
        """
        return self.execute_query(sql)

    def getUltimasFacturas(self, limite=5):
        """Últimas facturas registradas, con paciente, condición y estado (dashboard)."""
        sql = """
            SELECT
                f.id_factura, f.factura_numero, f.factura_total,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                cv.des_condicion_venta,
                ef.des_estado_factura,
                m.cod_moneda, m.simbolo_moneda, m.decimales_moneda, m.es_moneda_local,
                TO_CHAR(f.fecha_creacion, 'DD/MM HH24:MI') AS fecha_hora
            FROM facturas f
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            JOIN estados_factura ef ON f.id_estado_factura = ef.id_estado_factura
            JOIN monedas m ON f.id_moneda = m.id_moneda
            ORDER BY f.fecha_creacion DESC, f.id_factura DESC
            LIMIT %s
        """
        return self.execute_query(sql, (limite,))

    def getFacturaById(self, id_factura):
        """Devuelve el registro de factura por su id, o None si no existe."""
        sql = """
            SELECT
                f.id_factura, f.factura_numero, f.fecha_factura, f.fecha_vencimiento,
                f.factura_subtotal, f.factura_descuento, f.factura_impuestos, f.factura_total,
                f.factura_total_letras, f.codigo_sifen, f.numero_timbrado, f.observaciones,
                f.id_paciente, f.id_pedido, f.id_timbrado, f.id_punto_expedicion,
                f.id_tipo_comprobante, f.id_condicion_venta, f.id_moneda, f.id_estado_factura,
                f.fecha_anulacion, f.motivo_anulacion,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula, pp.per_telefono AS paciente_telefono,
                pp.per_correo AS paciente_correo,
                pp.per_tipo_documento AS paciente_tipo_documento, pp.per_ruc AS paciente_ruc,
                pac.pac_historia_clinica,
                tc.des_tipo_comprobante,
                cv.des_condicion_venta, cv.dias_credito,
                ef.des_estado_factura,
                m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
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
        """Devuelve las líneas de detalle de factura para el id indicado."""
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
    def _calcularItem(d: dict, decimales: int = 0) -> dict:
        """Descompone IVA en un ítem. El precio ingresado ya incluye IVA."""
        p_con_iva = Decimal(str(d.get('item_precio_con_iva', 0)))
        cantidad = Decimal(str(d.get('item_cantidad', 1)))
        descuento = Decimal(str(d.get('item_descuento', 0)))
        tasa = Decimal(str(d.get('impuesto_porcentaje', 0)))

        total = (p_con_iva * cantidad) - descuento
        divisor = Decimal('1') + (tasa / Decimal('100'))
        subtotal = redondear(total / divisor, decimales)
        iva_monto = total - subtotal
        precio_base = redondear(subtotal / cantidad, decimales) if cantidad > 0 else Decimal('0')

        return {
            'item_descripcion': d.get('item_descripcion', ''),
            'item_cantidad': int(cantidad),
            'item_precio_con_iva': redondear(p_con_iva, decimales),
            'item_precio_unitario': precio_base,
            'item_descuento': redondear(descuento, decimales),
            'item_subtotal': subtotal,
            'impuesto_porcentaje': float(tasa),
            'impuesto_monto': redondear(iva_monto, decimales),
            'item_total': redondear(total, decimales),
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

        moneda = get_moneda(data.get('id_moneda'))
        id_moneda = moneda['id_moneda']
        decimales = int(moneda['decimales_moneda'])

        # Descuento de la factura: se prorratea entre los ítems para que el IVA se
        # calcule sobre el precio ya descontado (si se resta al final, el IVA queda inflado).
        descuento = redondear(data.get('factura_descuento', 0), decimales)
        if descuento:
            brutos = [Decimal(str(d.get('item_precio_con_iva', 0))) * Decimal(str(d.get('item_cantidad', 1)))
                      - Decimal(str(d.get('item_descuento', 0))) for d in detalles_enriquecidos]
            total_bruto = sum(brutos)
            if descuento < 0 or descuento > total_bruto:
                raise ValueError('El descuento no puede ser negativo ni mayor al total de la factura.')
            restante = descuento
            for i, (d, bruto) in enumerate(zip(detalles_enriquecidos, brutos)):
                parte = restante if i == len(brutos) - 1 else redondear(descuento * bruto / total_bruto, decimales)
                d['item_descuento'] = Decimal(str(d.get('item_descuento', 0))) + parte
                restante -= parte

        detalles_calc = [self._calcularItem(d, decimales) for d in detalles_enriquecidos]

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
            # El descuento ya está dentro de cada ítem (prorrateo de arriba)
            subtotal = sum(d['item_subtotal'] for d in detalles_calc)
            impuestos = sum(d['impuesto_monto'] for d in detalles_calc)
            total = subtotal + impuestos
            # Para el libro de ventas: base gravada (ítems con IVA) y monto exento por separado
            monto_gravado = sum(d['item_subtotal'] for d in detalles_calc if d['impuesto_porcentaje'] > 0)
            monto_exento = sum(d['item_subtotal'] for d in detalles_calc if d['impuesto_porcentaje'] == 0)
            try:
                total_letras = numero_a_letras(total, moneda)
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
                id_moneda,
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
                    numero_timbrado, usuario_creacion, id_moneda
                )
                VALUES (%s,'FACTURA',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                data['fecha_factura'],
                factura_numero,
                data['id_paciente'],
                id_factura,
                monto_gravado,
                monto_exento,
                impuestos,
                total,
                numero_timbrado,
                usuario_creacion,
                id_moneda,
            ))

            # 8. INSERT cuentas_cobrar. Crédito (dias_credito > 0): queda pendiente hasta
            #    su vencimiento. Contado: vence el mismo día y se cobra acá mismo en la
            #    caja abierta, para que la venta entre al cierre/arqueo de caja.
            cur.execute(
                "SELECT dias_credito FROM condiciones_venta WHERE id_condicion_venta=%s",
                (data['id_condicion_venta'],)
            )
            cond = cur.fetchone()
            es_credito = bool(cond and cond[0] and cond[0] > 0)
            cobro = data.get('cobro') or {}
            if not es_credito and not cobro.get('id_caja'):
                raise ValueError('Para facturar al contado elija la caja donde entra el cobro.')

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
                    fecha_vencimiento, monto_total, monto_pendiente, usuario_creacion, id_moneda
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_cuenta_cobrar
            """, (
                f'CTA-{año}-{num_cta:04d}',
                id_factura,
                data['id_paciente'],
                fecha_vencimiento if es_credito else data['fecha_factura'],
                total,
                total,
                usuario_creacion,
                id_moneda,
            ))
            id_cuenta_cobrar = cur.fetchone()[0]

            if not es_credito:
                detalles_cobro = cobro.get('detalles') or []
                if not detalles_cobro:
                    raise ValueError('Elija la forma de cobro de la factura al contado.')
                # Con una sola forma de cobro, cobra el total; con varias, deben sumar el total.
                if len(detalles_cobro) == 1:
                    detalles_cobro[0]['monto_cobrado'] = total
                elif redondear(sum(Decimal(str(d.get('monto_cobrado', 0))) for d in detalles_cobro), decimales) != total:
                    raise ValueError('Las formas de cobro deben sumar el total de la factura.')
                CobranzaDao().registrarEnTransaccion(cur, {
                    'id_cuenta_cobrar': id_cuenta_cobrar,
                    'id_factura': id_factura,
                    'id_caja': cobro['id_caja'],
                    'detalles': detalles_cobro,
                    'observaciones': f'Cobro de factura al contado {factura_numero}',
                }, usuario_creacion)

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
    def anular(self, id_factura, usuario_anulacion=None, motivo=None):
        """Anula una factura con sp_anular_factura: estado ANULADA, sus cobranzas (el cobro sale
        de la caja), su cuenta a cobrar (ANULADA) y su fila del libro de ventas (en 0), todo en
        la misma transacción. Devuelve False si ya estaba anulada."""
        def _fn(cur):
            try:
                cur.execute("""
                    CALL sp_anular_factura(
                        p_id_factura => %s, p_usuario_anulacion => %s,
                        o_anulada => NULL, o_cobranzas_anuladas => NULL, o_cuentas_anuladas => NULL,
                        p_motivo => %s)
                """, (id_factura, usuario_anulacion, motivo))
            except psycopg2.errors.RaiseException as e:
                raise ValueError(e.diag.message_primary) from e
            anulada, cobranzas, cuentas = cur.fetchone()
            if anulada:
                app.logger.info(f"Factura {id_factura} anulada ({cobranzas} cobranzas, {cuentas} cuentas)")
            return anulada

        return self.execute_transaction(_fn)
