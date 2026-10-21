from app.core.base_dao import BaseDAO


class LibroVentasDao(BaseDAO):
    """Acceso a datos de libro de ventas (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        """Devuelve las facturas del período para el libro de ventas (rango de fechas)."""
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
                lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula
            FROM libro_ventas lv
            LEFT JOIN pacientes pac ON lv.id_paciente = pac.id_paciente
            LEFT JOIN personas  pp  ON pac.id_persona = pp.id_persona
            JOIN monedas m ON lv.id_moneda = m.id_moneda
            {where}
            ORDER BY lv.libro_fecha DESC, lv.id_libro_ventas DESC
        """
        return self.execute_query(sql, tuple(valores) if valores else None)

    def getResumenLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        """Devuelve el libro de ventas resumido en el período."""
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
                lv.tipo_comprobante,
                lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                COUNT(*)              AS cantidad,
                SUM(lv.monto_gravado) AS total_gravado,
                SUM(lv.monto_exento)  AS total_exento,
                SUM(lv.monto_iva)     AS total_iva,
                SUM(lv.monto_total)   AS total_total
            FROM libro_ventas lv
            JOIN monedas m ON lv.id_moneda = m.id_moneda
            {where}
            GROUP BY lv.tipo_comprobante, lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda
            ORDER BY lv.tipo_comprobante
        """
        return self.execute_query(sql, tuple(valores) if valores else None)

    def getTotalesLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        """Devuelve los totales generales del libro de ventas en el período."""
        condiciones = []
        valores     = []

        if fecha_desde:
            condiciones.append("libro_fecha >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("libro_fecha <= %s")
            valores.append(fecha_hasta)

        where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

        # Totales agrupados por moneda: sumar montos de monedas distintas sin
        # agrupar daria un numero sin sentido (ej. Gs. + USD mezclados).
        # La nota de credito resta (en el libro se guarda en positivo).
        signo = "CASE WHEN lv.tipo_comprobante = 'NOTA_CREDITO' THEN -1 ELSE 1 END"
        sql = f"""
            SELECT
                lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                COUNT(*)                         AS total_registros,
                SUM({signo} * lv.monto_gravado)  AS total_gravado,
                SUM({signo} * lv.monto_exento)   AS total_exento,
                SUM({signo} * lv.monto_iva)      AS total_iva,
                SUM({signo} * lv.monto_total)    AS total_total
            FROM libro_ventas lv
            JOIN monedas m ON lv.id_moneda = m.id_moneda
            {where}
            GROUP BY lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda
            ORDER BY m.cod_moneda
        """
        filas = self.execute_query(sql, tuple(valores) if valores else None)
        return [{k: (v if v is not None else 0) for k, v in f.items()} for f in filas]
