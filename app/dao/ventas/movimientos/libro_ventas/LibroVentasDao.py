from app.core.base_dao import BaseDAO


class LibroVentasDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        condiciones = []
        valores     = []

        if fecha_desde:
            condiciones.append("lv.libro_fecha >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("lv.libro_fecha <= %s")
            valores.append(fecha_hasta)

        where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

        sql = f"""
            SELECT
                lv.id_libro_ventas,
                TO_CHAR(lv.libro_fecha, 'DD/MM/YYYY') AS libro_fecha_fmt,
                lv.tipo_comprobante,
                lv.numero_comprobante,
                lv.id_factura,
                lv.id_nota_credito,
                lv.id_nota_debito,
                lv.monto_gravado,
                lv.monto_exento,
                lv.monto_iva,
                lv.monto_total,
                lv.codigo_sifen,
                lv.numero_timbrado,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula
            FROM libro_ventas lv
            LEFT JOIN pacientes pac ON lv.id_paciente = pac.id_paciente
            LEFT JOIN personas  pp  ON pac.id_persona = pp.id_persona
            {where}
            ORDER BY lv.libro_fecha DESC, lv.id_libro_ventas DESC
        """
        return self.execute_query(sql, tuple(valores) if valores else None)

    def getResumenLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        condiciones = []
        valores     = []

        if fecha_desde:
            condiciones.append("libro_fecha >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("libro_fecha <= %s")
            valores.append(fecha_hasta)

        where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

        sql = f"""
            SELECT
                tipo_comprobante,
                COUNT(*)           AS cantidad,
                SUM(monto_gravado) AS total_gravado,
                SUM(monto_exento)  AS total_exento,
                SUM(monto_iva)     AS total_iva,
                SUM(monto_total)   AS total_total
            FROM libro_ventas
            {where}
            GROUP BY tipo_comprobante
            ORDER BY tipo_comprobante
        """
        return self.execute_query(sql, tuple(valores) if valores else None)

    def getTotalesLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        condiciones = []
        valores     = []

        if fecha_desde:
            condiciones.append("libro_fecha >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("libro_fecha <= %s")
            valores.append(fecha_hasta)

        where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

        sql = f"""
            SELECT
                COUNT(*)           AS total_registros,
                SUM(monto_gravado) AS total_gravado,
                SUM(monto_exento)  AS total_exento,
                SUM(monto_iva)     AS total_iva,
                SUM(monto_total)   AS total_total
            FROM libro_ventas
            {where}
        """
        row = self.execute_query_one(sql, tuple(valores) if valores else None)
        if row:
            return {k: (v or 0) for k, v in row.items()}
        return {'total_registros': 0, 'total_gravado': 0,
                'total_exento': 0, 'total_iva': 0, 'total_total': 0}
