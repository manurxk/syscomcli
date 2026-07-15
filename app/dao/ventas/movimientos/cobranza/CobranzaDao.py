from datetime import datetime

from flask import current_app as app
from app.core.base_dao import BaseDAO


class CobranzaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    # ── Consultas ─────────────────────────────────────────────────────────

    def getCobranzas(self):
        sql = """
            SELECT
                c.id_cobranza,
                c.cobranza_numero,
                c.id_cuenta_cobrar,
                c.id_factura,
                c.id_caja,
                c.monto_cobrado,
                c.observaciones,
                c.est_cobranza,
                cc.cuenta_numero,
                f.factura_numero,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                caja.des_caja,
                TO_CHAR(c.fecha_cobranza, 'DD/MM/YYYY HH24:MI') AS fecha_cobranza_fmt,
                TO_CHAR(c.fecha_creacion, 'DD/MM/YYYY')         AS fecha_registro
            FROM cobranzas c
            JOIN cuentas_cobrar cc ON c.id_cuenta_cobrar = cc.id_cuenta_cobrar
            JOIN facturas f        ON c.id_factura        = f.id_factura
            JOIN pacientes pac     ON cc.id_paciente       = pac.id_paciente
            JOIN personas pp       ON pac.id_persona       = pp.id_persona
            JOIN cajas caja        ON c.id_caja            = caja.id_caja
            ORDER BY c.fecha_cobranza DESC, c.id_cobranza DESC
        """
        return self.execute_query(sql)

    def getCobranzaById(self, id_cobranza):
        sql = """
            SELECT
                c.id_cobranza,
                c.cobranza_numero,
                c.id_cuenta_cobrar,
                c.id_factura,
                c.id_caja,
                c.monto_cobrado,
                c.observaciones,
                c.est_cobranza,
                c.usuario_creacion,
                cc.cuenta_numero,
                cc.monto_total     AS monto_total_cuenta,
                cc.monto_pagado    AS monto_pagado_cuenta,
                cc.monto_pendiente AS monto_pendiente_cuenta,
                f.factura_numero,
                f.factura_total,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica,
                caja.des_caja,
                TO_CHAR(c.fecha_cobranza, 'DD/MM/YYYY HH24:MI') AS fecha_cobranza_fmt,
                TO_CHAR(c.fecha_creacion, 'DD/MM/YYYY')          AS fecha_registro
            FROM cobranzas c
            JOIN cuentas_cobrar cc ON c.id_cuenta_cobrar = cc.id_cuenta_cobrar
            JOIN facturas f        ON c.id_factura        = f.id_factura
            JOIN pacientes pac     ON cc.id_paciente       = pac.id_paciente
            JOIN personas pp       ON pac.id_persona       = pp.id_persona
            JOIN cajas caja        ON c.id_caja            = caja.id_caja
            WHERE c.id_cobranza = %s
        """
        return self.execute_query_one(sql, (id_cobranza,))

    def getCobranzaDetalle(self, id_cobranza):
        sql = """
            SELECT
                cd.id_cobranza_detalle,
                cd.id_cobranza,
                cd.id_forma_cobro,
                cd.id_marca_tarjeta,
                cd.id_entidad_adherida,
                cd.id_entidad_emisora,
                cd.numero_cheque,
                cd.numero_tarjeta,
                cd.numero_cuotas,
                cd.monto_cobrado,
                cd.observaciones,
                fc.des_forma_cobro,
                mt.des_marca_tarjeta,
                ea.des_entidad_adherida,
                ee.des_entidad_emisora
            FROM cobranza_detalle cd
            JOIN formas_cobro fc              ON cd.id_forma_cobro      = fc.id_forma_cobro
            LEFT JOIN marcas_tarjeta mt        ON cd.id_marca_tarjeta    = mt.id_marca_tarjeta
            LEFT JOIN entidades_adheridas ea   ON cd.id_entidad_adherida = ea.id_entidad_adherida
            LEFT JOIN entidades_emisoras ee    ON cd.id_entidad_emisora  = ee.id_entidad_emisora
            WHERE cd.id_cobranza = %s
            ORDER BY cd.id_cobranza_detalle
        """
        return self.execute_query(sql, (id_cobranza,))

    def getCobranzasPorCuenta(self, id_cuenta_cobrar):
        sql = """
            SELECT
                c.id_cobranza,
                c.cobranza_numero,
                c.monto_cobrado,
                c.est_cobranza,
                TO_CHAR(c.fecha_cobranza, 'DD/MM/YYYY HH24:MI') AS fecha_cobranza_fmt
            FROM cobranzas c
            WHERE c.id_cuenta_cobrar = %s
            ORDER BY c.fecha_cobranza DESC
        """
        return self.execute_query(sql, (id_cuenta_cobrar,))

    # ── Helpers internos ─────────────────────────────────────────────────

    def _generarNumero(self, cur):
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        patron = f'COB-{año}-{mes}-%'
        cur.execute(
            "SELECT cobranza_numero FROM cobranzas "
            "WHERE cobranza_numero LIKE %s ORDER BY cobranza_numero DESC LIMIT 1",
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
        return f'COB-{año}-{mes}-{siguiente:04d}'

    def _verificarCajaAbierta(self, cur, id_caja):
        """Lanza ValueError si no hay apertura activa para la caja indicada."""
        cur.execute("""
            SELECT id_apertura_cierre
            FROM aperturas_cierre_caja
            WHERE id_caja = %s
              AND tipo_operacion = 'APERTURA'
              AND est_apertura_cierre = 'A'
            LIMIT 1
        """, (id_caja,))
        if not cur.fetchone():
            raise ValueError("No hay caja abierta. Debe abrir la caja antes de registrar una cobranza.")

    # ── Escritura ─────────────────────────────────────────────────────────

    def guardar(self, data: dict, usuario_creacion=None):
        """
        Registra una cobranza con su detalle multi-forma en una transacción única.
        Pasos: verificar caja abierta → generar número → INSERT cobranzas →
               INSERT cobranza_detalle (×N) → UPDATE cuentas_cobrar (montos + estado)
        """
        detalles = data.get('detalles') or []
        if not detalles:
            raise ValueError('La cobranza debe tener al menos una forma de cobro.')

        id_cuenta_cobrar = data.get('id_cuenta_cobrar')
        id_factura       = data.get('id_factura')
        id_caja          = data.get('id_caja')

        if not all([id_cuenta_cobrar, id_factura, id_caja]):
            raise ValueError('id_cuenta_cobrar, id_factura e id_caja son obligatorios.')

        monto_total = sum(int(d.get('monto_cobrado', 0)) for d in detalles)
        if monto_total <= 0:
            raise ValueError('El monto total cobrado debe ser mayor a cero.')

        def _fn(cur):
            # 1. Verificar caja abierta
            self._verificarCajaAbierta(cur, id_caja)

            # 2. Verificar que la cuenta existe y no está ya cobrada
            cur.execute(
                "SELECT monto_pendiente, est_cuenta_cobrar FROM cuentas_cobrar WHERE id_cuenta_cobrar = %s",
                (id_cuenta_cobrar,)
            )
            cta = cur.fetchone()
            if not cta:
                raise ValueError('La cuenta a cobrar no existe.')
            monto_pendiente_actual, estado_actual = cta
            if estado_actual == 'COBRADA':
                raise ValueError('Esta cuenta ya está completamente cobrada.')

            # 3. Generar número de cobranza
            numero = self._generarNumero(cur)

            # 4. INSERT cobranza cabecera
            cur.execute("""
                INSERT INTO cobranzas(
                    cobranza_numero, id_cuenta_cobrar, id_factura, id_caja,
                    monto_cobrado, observaciones, est_cobranza, usuario_creacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'REGISTRADA', %s)
                RETURNING id_cobranza
            """, (
                numero,
                id_cuenta_cobrar,
                id_factura,
                id_caja,
                monto_total,
                data.get('observaciones') or None,
                usuario_creacion,
            ))
            id_cobranza = cur.fetchone()[0]

            # 5. INSERT cobranza_detalle (una fila por forma de cobro)
            for d in detalles:
                cur.execute("""
                    INSERT INTO cobranza_detalle(
                        id_cobranza, id_forma_cobro, id_marca_tarjeta,
                        id_entidad_adherida, id_entidad_emisora,
                        numero_cheque, numero_tarjeta, numero_cuotas,
                        monto_cobrado, observaciones
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    id_cobranza,
                    d['id_forma_cobro'],
                    d.get('id_marca_tarjeta') or None,
                    d.get('id_entidad_adherida') or None,
                    d.get('id_entidad_emisora') or None,
                    d.get('numero_cheque') or None,
                    d.get('numero_tarjeta') or None,
                    d.get('numero_cuotas') or 1,
                    int(d['monto_cobrado']),
                    d.get('observaciones') or None,
                ))

            # 6. Actualizar montos en cuentas_cobrar y recalcular estado
            cur.execute("""
                UPDATE cuentas_cobrar
                SET monto_pagado    = monto_pagado + %s,
                    monto_pendiente = GREATEST(0, monto_total - (monto_pagado + %s)),
                    est_cuenta_cobrar = CASE
                        WHEN (monto_pagado + %s) >= monto_total                             THEN 'COBRADA'
                        WHEN (monto_pagado + %s) > 0
                             AND fecha_vencimiento < CURRENT_DATE                           THEN 'PARCIAL'
                        WHEN (monto_pagado + %s) > 0                                        THEN 'PARCIAL'
                        WHEN fecha_vencimiento < CURRENT_DATE                               THEN 'VENCIDA'
                        ELSE 'PENDIENTE'
                    END,
                    fecha_modificacion   = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_cuenta_cobrar = %s
            """, (
                monto_total, monto_total,
                monto_total, monto_total, monto_total,
                usuario_creacion,
                id_cuenta_cobrar,
            ))

            app.logger.info(f"Cobranza creada: {numero} (ID={id_cobranza})")
            return id_cobranza

        return self.execute_transaction(_fn)

    def anular(self, id_cobranza, usuario=None):
        """
        Anula una cobranza y revierte el pago en cuentas_cobrar.
        Ambas operaciones en la misma transacción.
        """
        cobranza = self.getCobranzaById(id_cobranza)
        if not cobranza:
            raise ValueError('Cobranza no encontrada.')
        if cobranza['est_cobranza'] == 'ANULADA':
            return False

        monto = cobranza['monto_cobrado']
        id_cta = cobranza['id_cuenta_cobrar']

        def _fn(cur):
            cur.execute("""
                UPDATE cobranzas
                SET est_cobranza         = 'ANULADA',
                    fecha_modificacion   = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_cobranza = %s AND est_cobranza != 'ANULADA'
            """, (usuario, id_cobranza))

            # Revertir montos en cuentas_cobrar
            cur.execute("""
                UPDATE cuentas_cobrar
                SET monto_pagado    = GREATEST(0, monto_pagado - %s),
                    monto_pendiente = LEAST(monto_total, monto_pendiente + %s),
                    est_cuenta_cobrar = CASE
                        WHEN GREATEST(0, monto_pagado - %s) = 0
                             AND fecha_vencimiento < CURRENT_DATE THEN 'VENCIDA'
                        WHEN GREATEST(0, monto_pagado - %s) = 0 THEN 'PENDIENTE'
                        WHEN fecha_vencimiento < CURRENT_DATE    THEN 'VENCIDA'
                        ELSE 'PARCIAL'
                    END,
                    fecha_modificacion   = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_cuenta_cobrar = %s
            """, (monto, monto, monto, monto, usuario, id_cta))

            return True

        return self.execute_transaction(_fn)
