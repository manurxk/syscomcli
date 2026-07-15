from app.core.base_dao import BaseDAO


class CuentaCobrarDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCuentasCobrar(self):
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.id_paciente,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
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
                    WHEN cc.est_cuenta_cobrar = 'COBRADA' THEN NULL
                    WHEN cc.fecha_vencimiento < CURRENT_DATE THEN
                        -(CURRENT_DATE - cc.fecha_vencimiento)
                    ELSE
                        (cc.fecha_vencimiento - CURRENT_DATE)
                END AS dias_vencimiento
            FROM cuentas_cobrar cc
            JOIN facturas f    ON cc.id_factura  = f.id_factura
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp   ON pac.id_persona = pp.id_persona
            ORDER BY cc.fecha_vencimiento ASC, cc.id_cuenta_cobrar DESC
        """
        return self.execute_query(sql)

    def getCuentaCobrarById(self, id_cuenta_cobrar):
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.id_paciente,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
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
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp   ON pac.id_persona = pp.id_persona
            WHERE cc.id_cuenta_cobrar = %s
        """
        return self.execute_query_one(sql, (id_cuenta_cobrar,))

    def getCuentasCobrarPendientes(self):
        """Retorna solo las cuentas PENDIENTE o PARCIAL para el selector de cobranza."""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.monto_total,
                cc.monto_pendiente,
                cc.est_cuenta_cobrar,
                f.factura_numero,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                TO_CHAR(cc.fecha_vencimiento, 'DD/MM/YYYY') AS fecha_vencimiento_fmt
            FROM cuentas_cobrar cc
            JOIN facturas f    ON cc.id_factura  = f.id_factura
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp   ON pac.id_persona = pp.id_persona
            WHERE cc.est_cuenta_cobrar IN ('PENDIENTE', 'PARCIAL')
            ORDER BY cc.fecha_vencimiento ASC
        """
        return self.execute_query(sql)
