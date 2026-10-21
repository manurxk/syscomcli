from app.core.base_dao import BaseDAO


class CuentaCobrarDao(BaseDAO):
    """Acceso a datos de cuenta a cobrar (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCuentasCobrar(self):
        """Lista los registros de cuenta a cobrar."""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.id_paciente,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
                cc.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                cc.numero_cuotas,
                cc.cuota_actual,
                cc.est_cuenta_cobrar,
                f.factura_numero,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pac.pac_historia_clinica,
                TO_CHAR(cc.fecha_emision,     'DD/MM/YYYY') AS fecha_emision_fmt,
                TO_CHAR(cc.fecha_vencimiento, 'DD/MM/YYYY') AS fecha_vencimiento_fmt,
                TO_CHAR(cc.fecha_creacion,    'DD/MM/YYYY') AS fecha_registro,
                CASE
                    WHEN cc.est_cuenta_cobrar IN ('COBRADA', 'ANULADA') THEN NULL
                    WHEN cc.fecha_vencimiento < CURRENT_DATE THEN
                        -(CURRENT_DATE - cc.fecha_vencimiento)
                    ELSE
                        (cc.fecha_vencimiento - CURRENT_DATE)
                END AS dias_vencimiento
            FROM cuentas_cobrar cc
            JOIN facturas f    ON cc.id_factura  = f.id_factura
            JOIN monedas m     ON cc.id_moneda   = m.id_moneda
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp   ON pac.id_persona = pp.id_persona
            ORDER BY cc.fecha_vencimiento ASC, cc.id_cuenta_cobrar DESC
        """
        return self.execute_query(sql)

    def getCuentaCobrarById(self, id_cuenta_cobrar):
        """Devuelve el registro de cuenta a cobrar por su id, o None si no existe."""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.id_paciente,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
                cc.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                cc.numero_cuotas,
                cc.cuota_actual,
                cc.est_cuenta_cobrar,
                cc.usuario_creacion,
                f.factura_numero,
                f.factura_total,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula  AS paciente_cedula,
                pp.per_telefono AS paciente_telefono,
                pac.pac_historia_clinica,
                TO_CHAR(cc.fecha_emision,     'DD/MM/YYYY') AS fecha_emision_fmt,
                TO_CHAR(cc.fecha_vencimiento, 'DD/MM/YYYY') AS fecha_vencimiento_fmt,
                TO_CHAR(cc.fecha_creacion,    'DD/MM/YYYY') AS fecha_registro
            FROM cuentas_cobrar cc
            JOIN facturas f    ON cc.id_factura  = f.id_factura
            JOIN monedas m     ON cc.id_moneda   = m.id_moneda
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp   ON pac.id_persona = pp.id_persona
            WHERE cc.id_cuenta_cobrar = %s
        """
        return self.execute_query_one(sql, (id_cuenta_cobrar,))

    def ajustarPorNotaEnTransaccion(self, cur, id_factura, delta, usuario=None, validar_pendiente=False,
                                    es_anulacion_de_nota=False):
        """Ajusta la cuenta a cobrar de una factura por una nota de crédito (delta < 0)
        o de débito (delta > 0), o por la anulación de una de ellas (delta invertido).
        Se ejecuta dentro de la transacción de la nota. Si la factura no tiene cuenta
        (facturas al contado anteriores al cobro automático) no hay nada que ajustar."""
        cur.execute(
            "SELECT id_cuenta_cobrar, monto_pendiente, est_cuenta_cobrar FROM cuentas_cobrar WHERE id_factura = %s FOR UPDATE",
            (id_factura,)
        )
        cta = cur.fetchone()
        if not cta:
            return
        id_cuenta_cobrar, monto_pendiente, estado_cuenta = cta

        # Una factura anulada no recibe notas nuevas; anular una nota vieja no revive su cuenta.
        if estado_cuenta == 'ANULADA':
            if es_anulacion_de_nota:
                return
            raise ValueError('La factura está anulada: no se pueden registrar notas sobre ella.')

        # Una nota de crédito mayor a lo que falta pagar sería una devolución de dinero,
        # y el sistema no maneja saldos a favor del paciente.
        if validar_pendiente and -delta > monto_pendiente:
            raise ValueError(
                f'La nota de crédito ({-delta:,.0f}) supera lo que falta pagar de la factura '
                f'({monto_pendiente:,.0f}). No se puede registrar.'.replace(',', '.')
            )

        cur.execute("""
            UPDATE cuentas_cobrar
            SET monto_total     = GREATEST(0, monto_total + %s),
                monto_pendiente = GREATEST(0, monto_pendiente + %s),
                est_cuenta_cobrar = CASE
                    WHEN GREATEST(0, monto_pendiente + %s) = 0  THEN 'COBRADA'
                    WHEN monto_pagado > 0                       THEN 'PARCIAL'
                    WHEN fecha_vencimiento < CURRENT_DATE       THEN 'VENCIDA'
                    ELSE 'PENDIENTE'
                END,
                fecha_modificacion   = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_cuenta_cobrar = %s
        """, (delta, delta, delta, usuario, id_cuenta_cobrar))

    def getCuentasCobrarPendientes(self):
        """Retorna solo las cuentas PENDIENTE o PARCIAL para el selector de cobranza."""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.monto_total,
                cc.monto_pendiente,
                cc.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                cc.est_cuenta_cobrar,
                f.factura_numero,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                TO_CHAR(cc.fecha_vencimiento, 'DD/MM/YYYY') AS fecha_vencimiento_fmt
            FROM cuentas_cobrar cc
            JOIN facturas f    ON cc.id_factura  = f.id_factura
            JOIN monedas m     ON cc.id_moneda   = m.id_moneda
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp   ON pac.id_persona = pp.id_persona
            WHERE cc.est_cuenta_cobrar IN ('PENDIENTE', 'PARCIAL')
              AND f.fecha_anulacion IS NULL
            ORDER BY cc.fecha_vencimiento ASC
        """
        return self.execute_query(sql)

    def getCuentasVencidas(self, limite=5):
        """Cuentas PENDIENTE/PARCIAL ya vencidas, de la más atrasada a la menos (dashboard)."""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.monto_pendiente,
                m.cod_moneda, m.simbolo_moneda, m.decimales_moneda, m.es_moneda_local,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                TO_CHAR(cc.fecha_vencimiento, 'DD/MM/YYYY') AS fecha_vencimiento_fmt,
                CURRENT_DATE - cc.fecha_vencimiento AS dias_atraso
            FROM cuentas_cobrar cc
            JOIN facturas f    ON cc.id_factura  = f.id_factura
            JOIN monedas m     ON cc.id_moneda   = m.id_moneda
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp   ON pac.id_persona = pp.id_persona
            WHERE cc.est_cuenta_cobrar IN ('PENDIENTE', 'PARCIAL')
              AND f.fecha_anulacion IS NULL
              AND cc.fecha_vencimiento < CURRENT_DATE
            ORDER BY cc.fecha_vencimiento ASC
            LIMIT %s
        """
        return self.execute_query(sql, (limite,))
