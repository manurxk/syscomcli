from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date
from decimal import Decimal

class ReporteDao:
    """
    DAO para el módulo de Reportes.
    Fase 1: Infraestructura base y consultas para Dashboard y Ventas.
    Fase 2: Consultas detalladas para PDF.
    Fase 3: Agendamiento y Consultorio.
    """
    
    def __init__(self):
        # La conexión se instancia por método según el patrón del proyecto
        pass

    def getVentasReport(self, fecha_desde, fecha_hasta, metodo_pago=None):
        """
        Obtiene ventas agrupadas por día para el gráfico, consumiendo libro_ventas.
        Soporta filtro opcional por método de pago (condicion_venta de factura).
        """
        # Se agrupa tambien por moneda: sumar Gs. + USD en la misma fila daria un total sin sentido.
        # La nota de credito resta (en el libro se guarda en positivo).
        sql = """
            SELECT
                lv.libro_fecha AS fecha,
                lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                COUNT(*) AS cantidad_comprobantes,
                SUM(CASE WHEN lv.tipo_comprobante = 'NOTA_CREDITO' THEN -lv.monto_gravado ELSE lv.monto_gravado END) AS total_gravado,
                SUM(CASE WHEN lv.tipo_comprobante = 'NOTA_CREDITO' THEN -lv.monto_iva ELSE lv.monto_iva END) AS total_iva,
                SUM(CASE WHEN lv.tipo_comprobante = 'NOTA_CREDITO' THEN -lv.monto_total ELSE lv.monto_total END) AS total_general
            FROM libro_ventas lv
            JOIN monedas m ON lv.id_moneda = m.id_moneda
            LEFT JOIN facturas f ON lv.id_factura = f.id_factura
            LEFT JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            WHERE lv.libro_fecha >= %s AND lv.libro_fecha <= %s
        """

        parametros = [fecha_desde, fecha_hasta]

        if metodo_pago and metodo_pago.lower() != 'todos':
            # Se asume que metodo_pago es 'Contado' o 'Credito'
            sql += " AND LOWER(cv.des_condicion_venta) LIKE LOWER(%s)"
            parametros.append(f"%{metodo_pago}%")

        sql += """ GROUP BY lv.libro_fecha, lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda
                   ORDER BY lv.libro_fecha ASC"""

        conexion = Conexion()
        con = conexion.getConexion()

        if not con:
            return []

        cur = con.cursor()
        resultados = []

        try:
            cur.execute(sql, tuple(parametros))
            filas = cur.fetchall()

            for f in filas:
                dec = int(f[4] or 0)
                resultados.append({
                    'fecha': f[0].strftime('%Y-%m-%d') if f[0] else '',
                    'id_moneda': f[1], 'cod_moneda': f[2], 'simbolo_moneda': f[3], 'decimales_moneda': dec,
                    'cantidad_comprobantes': int(f[5] or 0),
                    'total_gravado': round(float(f[6] or 0), dec),
                    'total_iva': round(float(f[7] or 0), dec),
                    'total_general': round(float(f[8] or 0), dec)
                })
        except Exception as e:
            app.logger.error(f"Error al ejecutar getVentasReport: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
            
        return resultados

    def getVentasDetalle(self, fecha_desde, fecha_hasta, metodo_pago=None):
        """
        Retorna las filas individuales (no agrupadas) para la tabla del reporte de ventas.
        Fase 2.
        """
        sql = """
            SELECT
                lv.libro_fecha AS fecha,
                lv.numero_comprobante,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_cliente,
                COALESCE(p.per_cedula, 'S/R') AS ruc_cliente,
                COALESCE(cv.des_condicion_venta, 'Contado') AS metodo_pago,
                lv.monto_gravado AS gravado, -- simplificado para ReporteDao
                lv.monto_iva AS iva,
                lv.monto_total AS total,
                lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                lv.tipo_comprobante
            FROM libro_ventas lv
            JOIN monedas m ON lv.id_moneda = m.id_moneda
            LEFT JOIN pacientes pac ON lv.id_paciente = pac.id_paciente
            LEFT JOIN personas p ON pac.id_persona = p.id_persona
            LEFT JOIN facturas f ON lv.id_factura = f.id_factura
            LEFT JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            WHERE lv.libro_fecha >= %s AND lv.libro_fecha <= %s
        """
        parametros = [fecha_desde, fecha_hasta]

        if metodo_pago and metodo_pago.lower() != 'todos':
            sql += " AND LOWER(cv.des_condicion_venta) LIKE LOWER(%s)"
            parametros.append(f"%{metodo_pago}%")

        sql += " ORDER BY lv.libro_fecha ASC, lv.id_libro_ventas ASC"

        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []

        try:
            cur.execute(sql, tuple(parametros))
            for f in cur.fetchall():
                dec = int(f[11] or 0)
                resultados.append({
                    'fecha': f[0].strftime('%Y-%m-%d') if f[0] else '',
                    'numero_comprobante': f[1],
                    'nombre_cliente': f[2],
                    'ruc_cliente': f[3],
                    'metodo_pago': f[4],
                    'gravado': round(float(f[5] or 0), dec),
                    'iva': round(float(f[6] or 0), dec),
                    'total': round(float(f[7] or 0), dec),
                    'id_moneda': f[8], 'cod_moneda': f[9], 'simbolo_moneda': f[10], 'decimales_moneda': dec,
                    'tipo_comprobante': f[12]
                })
        except Exception as e:
            app.logger.error(f"Error en getVentasDetalle: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resultados

    def getVentasPorMetodoPago(self, fecha_desde, fecha_hasta):
        """
        Retorna los totales agrupados por método de pago para el gráfico de torta.
        Fase 2.
        """
        sql = """
            SELECT
                COALESCE(cv.des_condicion_venta, 'Contado') AS metodo_pago,
                lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                COUNT(*) AS cantidad,
                SUM(CASE WHEN lv.tipo_comprobante = 'NOTA_CREDITO' THEN -lv.monto_total ELSE lv.monto_total END) AS total
            FROM libro_ventas lv
            JOIN monedas m ON lv.id_moneda = m.id_moneda
            LEFT JOIN facturas f ON lv.id_factura = f.id_factura
            LEFT JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            WHERE lv.libro_fecha >= %s AND lv.libro_fecha <= %s
            GROUP BY COALESCE(cv.des_condicion_venta, 'Contado'), lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda
        """

        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []

        try:
            cur.execute(sql, (fecha_desde, fecha_hasta))
            for f in cur.fetchall():
                dec = int(f[4] or 0)
                resultados.append({
                    'metodo_pago': f[0],
                    'id_moneda': f[1], 'cod_moneda': f[2], 'simbolo_moneda': f[3], 'decimales_moneda': dec,
                    'cantidad': int(f[5] or 0),
                    'total': round(float(f[6] or 0), dec)
                })
        except Exception as e:
            app.logger.error(f"Error en getVentasPorMetodoPago: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resultados

    # ------------------------------------------------------------------
    # Reportes unificados (PDF 4). Agendamiento lee de v_agenda_dia y Consultorio de v_consultas_resumen.
    # id_especialista: cuando el usuario es Clínico lo fija el servidor desde la sesión (nunca un parámetro);
    # None o 0 significa «todos los especialistas».
    # ------------------------------------------------------------------

    def _filtro_especialista(self, id_especialista, columna='id_especialista'):
        """Fragmento « AND columna = %s» y su parámetro, o vacío si no hay filtro por especialista."""
        if id_especialista and str(id_especialista) != '0':
            return f" AND {columna} = %s", [id_especialista]
        return "", []

    def _consultar(self, sql, parametros=()):
        """SELECT que devuelve una lista de dicts (fechas como texto, Decimal como float). Ante un error lo
        registra y devuelve [], igual que el resto de los métodos de este DAO."""
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        try:
            cur.execute(sql, tuple(parametros))
            columnas = [c[0] for c in cur.description]
            filas = []
            for f in cur.fetchall():
                fila = {}
                for columna, valor in zip(columnas, f):
                    if isinstance(valor, datetime):
                        valor = valor.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(valor, date):
                        valor = valor.strftime('%Y-%m-%d')
                    elif isinstance(valor, Decimal):
                        valor = float(valor)
                    fila[columna] = valor
                filas.append(fila)
            return filas
        except Exception as e:
            app.logger.error(f"Error en ReporteDao._consultar: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # ---------------------------- Agendamiento ----------------------------
    # «Atendida» = estado COMPLETADA (criterio unificado del PDF 4).

    def getAgendamientoReport(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Cantidad de citas por estado."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT cod_estado_cita AS estado, COUNT(*) AS cantidad
            FROM v_agenda_dia
            WHERE fecha BETWEEN %s AND %s{filtro}
            GROUP BY cod_estado_cita
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra)

    def getAgendamientoPorDia(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Evolución diaria: atendidas, canceladas, ausentes y total de citas del día."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT fecha,
                   COUNT(*) FILTER (WHERE cod_estado_cita = 'COMPLETADA') AS cant_atendidas,
                   COUNT(*) FILTER (WHERE cod_estado_cita = 'CANCELADA') AS cant_canceladas,
                   COUNT(*) FILTER (WHERE cod_estado_cita = 'AUSENTE') AS cant_ausencias,
                   COUNT(*) AS cant_total
            FROM v_agenda_dia
            WHERE fecha BETWEEN %s AND %s{filtro}
            GROUP BY fecha
            ORDER BY fecha
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra)

    def getAgendamientoPorEspecialista(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Una fila por especialista: citas agendadas, atendidas, canceladas y ausentes."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT id_especialista, especialista_nombre,
                   string_agg(DISTINCT des_especialidad, ', ' ORDER BY des_especialidad) AS especialidades,
                   COUNT(*) AS agendadas,
                   COUNT(*) FILTER (WHERE cod_estado_cita = 'COMPLETADA') AS atendidas,
                   COUNT(*) FILTER (WHERE cod_estado_cita = 'CANCELADA') AS canceladas,
                   COUNT(*) FILTER (WHERE cod_estado_cita = 'AUSENTE') AS ausentes
            FROM v_agenda_dia
            WHERE fecha BETWEEN %s AND %s{filtro}
            GROUP BY id_especialista, especialista_nombre
            ORDER BY agendadas DESC, especialista_nombre
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra)

    def getAgendamientoPacientes(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Pacientes distintos con cita y pacientes nuevos (cita de primera vez) del período."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT COUNT(DISTINCT id_paciente) AS pacientes_distintos,
                   COUNT(DISTINCT id_paciente) FILTER (WHERE cita_es_primera_vez) AS pacientes_nuevos
            FROM v_agenda_dia
            WHERE fecha BETWEEN %s AND %s{filtro}
        """
        filas = self._consultar(sql, [fecha_desde, fecha_hasta] + extra)
        return filas[0] if filas else {'pacientes_distintos': 0, 'pacientes_nuevos': 0}

    def getPacientesAusentes(self, fecha_desde, fecha_hasta, id_especialista=None, limite=500):
        """Citas AUSENTE con los datos para llamar al paciente y sus ausencias anteriores (con el mismo
        especialista si hay filtro)."""
        filtro_a, extra_a = self._filtro_especialista(id_especialista, 'a.id_especialista')
        filtro_p, extra_p = self._filtro_especialista(id_especialista, 'p.id_especialista')
        sql = f"""
            SELECT a.fecha, to_char(a.cita_inicio, 'HH24:MI') AS hora,
                   a.id_paciente, a.paciente_nombre, a.paciente_cedula, a.paciente_telefono,
                   a.id_especialista, a.especialista_nombre,
                   (SELECT COUNT(*) FROM v_agenda_dia p
                     WHERE p.id_paciente = a.id_paciente AND p.cod_estado_cita = 'AUSENTE'
                       AND p.cita_inicio < a.cita_inicio{filtro_p}) AS ausencias_previas
            FROM v_agenda_dia a
            WHERE a.cod_estado_cita = 'AUSENTE' AND a.fecha BETWEEN %s AND %s{filtro_a}
            ORDER BY a.cita_inicio DESC
            LIMIT %s
        """
        return self._consultar(sql, extra_p + [fecha_desde, fecha_hasta] + extra_a + [limite])

    def getAusenciasReiteradas(self, fecha_desde, fecha_hasta, id_especialista=None, minimo=2, limite=50):
        """Pacientes con al menos `minimo` ausencias en el período."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT id_paciente, paciente_nombre, paciente_cedula,
                   COUNT(*) AS citas,
                   COUNT(*) FILTER (WHERE cod_estado_cita = 'AUSENTE') AS ausencias,
                   MAX(fecha) FILTER (WHERE cod_estado_cita = 'AUSENTE') AS ultima_ausencia
            FROM v_agenda_dia
            WHERE fecha BETWEEN %s AND %s{filtro}
            GROUP BY id_paciente, paciente_nombre, paciente_cedula
            HAVING COUNT(*) FILTER (WHERE cod_estado_cita = 'AUSENTE') >= %s
            ORDER BY ausencias DESC, ultima_ausencia DESC
            LIMIT %s
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra + [minimo, limite])

    def getCitasCanceladas(self, fecha_desde, fecha_hasta, id_especialista=None, limite=500):
        """Citas CANCELADA con el motivo y quién las canceló."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT fecha, to_char(cita_inicio, 'HH24:MI') AS hora, paciente_nombre, especialista_nombre,
                   motivo_cancelacion, cancelada_por, fecha_cancelacion
            FROM v_agenda_dia
            WHERE cod_estado_cita = 'CANCELADA' AND fecha BETWEEN %s AND %s{filtro}
            ORDER BY cita_inicio DESC
            LIMIT %s
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra + [limite])

    def getDetalleCitas(self, fecha_desde, fecha_hasta, id_especialista=None, limite=1000):
        """Listado de citas del período (para el detalle del PDF)."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT fecha, to_char(cita_inicio, 'HH24:MI') AS hora, paciente_nombre, especialista_nombre,
                   des_especialidad, des_estado_cita
            FROM v_agenda_dia
            WHERE fecha BETWEEN %s AND %s{filtro}
            ORDER BY cita_inicio
            LIMIT %s
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra + [limite])

    # ----------------------------- Consultorio ----------------------------
    # v_consultas_resumen trae una fila por consulta y por diagnóstico: las consultas se cuentan con
    # COUNT(DISTINCT id_consulta). Solo cuenta filas de `consultas` (no citas atendidas sin consulta).

    def getConsultasPorEspecialidad(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Cantidad de consultas por especialidad."""
        filtro, extra = self._filtro_especialista(id_especialista, 'v.id_especialista')
        sql = f"""
            SELECT COALESCE(e.des_especialidad, 'Sin especialidad') AS especialidad,
                   COUNT(DISTINCT v.id_consulta) AS cantidad
            FROM v_consultas_resumen v
            LEFT JOIN especialidades e ON e.id_especialidad = v.id_especialidad
            WHERE v.fecha BETWEEN %s AND %s{filtro}
            GROUP BY 1
            ORDER BY cantidad DESC, 1
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra)

    def getConsultasPorEspecialista(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Una fila por especialista con su especialidad y la cantidad de consultas."""
        filtro, extra = self._filtro_especialista(id_especialista, 'v.id_especialista')
        sql = f"""
            SELECT v.id_especialista, v.especialista_nombre,
                   string_agg(DISTINCT e.des_especialidad, ', ' ORDER BY e.des_especialidad) AS especialidades,
                   COUNT(DISTINCT v.id_consulta) AS consultas
            FROM v_consultas_resumen v
            LEFT JOIN especialidades e ON e.id_especialidad = v.id_especialidad
            WHERE v.fecha BETWEEN %s AND %s{filtro}
            GROUP BY v.id_especialista, v.especialista_nombre
            ORDER BY consultas DESC, v.especialista_nombre
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra)

    def getResumenConsultorio(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Consultas, pacientes distintos, pacientes nuevos y consultas abiertas (EN_ATENCION o pendientes de observación) del período."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT COUNT(DISTINCT id_consulta) AS consultas,
                   COUNT(DISTINCT id_paciente) AS pacientes_distintos,
                   COUNT(DISTINCT id_paciente) FILTER (WHERE cita_es_primera_vez) AS pacientes_nuevos,
                   COUNT(DISTINCT id_consulta) FILTER (WHERE consulta_estado IN ('EN_ATENCION', 'EN_OBSERVACION')) AS consultas_abiertas
            FROM v_consultas_resumen
            WHERE fecha BETWEEN %s AND %s{filtro}
        """
        filas = self._consultar(sql, [fecha_desde, fecha_hasta] + extra)
        return filas[0] if filas else {'consultas': 0, 'pacientes_distintos': 0,
                                       'pacientes_nuevos': 0, 'consultas_abiertas': 0}

    def getTopDiagnosticos(self, fecha_desde, fecha_hasta, id_especialista=None, limite=5):
        """Diagnósticos más frecuentes (con código CIE-10) en el período."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            SELECT cod_cie10, des_diagnostico AS diagnostico, COUNT(DISTINCT id_consulta) AS cantidad
            FROM v_consultas_resumen
            WHERE id_diagnostico IS NOT NULL AND fecha BETWEEN %s AND %s{filtro}
            GROUP BY cod_cie10, des_diagnostico
            ORDER BY cantidad DESC, des_diagnostico
            LIMIT %s
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra + [limite])

    def getConsultasPorDia(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Consultas por día, las de pacientes nuevos y las derivaciones hechas."""
        filtro, extra = self._filtro_especialista(id_especialista)
        sql = f"""
            WITH c AS (
                SELECT DISTINCT id_consulta, fecha, cita_es_primera_vez
                FROM v_consultas_resumen
                WHERE fecha BETWEEN %s AND %s{filtro}
            )
            SELECT c.fecha,
                   COUNT(*) AS consultas,
                   COUNT(*) FILTER (WHERE c.cita_es_primera_vez) AS pacientes_nuevos,
                   COALESCE(SUM(d.n), 0)::int AS derivaciones_hechas
            FROM c
            LEFT JOIN (SELECT id_consulta, COUNT(*) AS n FROM derivaciones
                        WHERE est_derivacion = TRUE GROUP BY id_consulta) d ON d.id_consulta = c.id_consulta
            GROUP BY c.fecha
            ORDER BY c.fecha
        """
        return self._consultar(sql, [fecha_desde, fecha_hasta] + extra)

    def getDerivaciones(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Derivaciones hechas (por especialidad destino) y, con un especialista, las recibidas.
        `derivaciones` no guarda quién recibe: una derivación se cuenta como recibida por el especialista
        cuando su especialidad destino es una de las suyas y la consulta es de otro especialista."""
        filtro, extra = self._filtro_especialista(id_especialista, 'c.id_especialista')
        hechas = self._consultar(f"""
            WITH c AS (SELECT DISTINCT id_consulta, id_especialista FROM v_consultas_resumen
                        WHERE fecha BETWEEN %s AND %s)
            SELECT e.des_especialidad AS especialidad, COUNT(*) AS cantidad
            FROM derivaciones d
            JOIN c ON c.id_consulta = d.id_consulta
            JOIN especialidades e ON e.id_especialidad = d.id_especialidad_destino
            WHERE d.est_derivacion = TRUE{filtro}
            GROUP BY e.des_especialidad
            ORDER BY cantidad DESC, e.des_especialidad
        """, [fecha_desde, fecha_hasta] + extra)
        recibidas = []
        if id_especialista and str(id_especialista) != '0':
            recibidas = self._consultar("""
                WITH c AS (SELECT DISTINCT id_consulta, id_especialista, id_especialidad FROM v_consultas_resumen
                            WHERE fecha BETWEEN %s AND %s)
                SELECT COALESCE(eo.des_especialidad, 'Sin especialidad') AS especialidad, COUNT(*) AS cantidad
                FROM derivaciones d
                JOIN c ON c.id_consulta = d.id_consulta
                LEFT JOIN especialidades eo ON eo.id_especialidad = c.id_especialidad
                WHERE d.est_derivacion = TRUE AND c.id_especialista <> %s
                  AND d.id_especialidad_destino IN (
                      SELECT id_especialidad FROM especialista_especialidades
                       WHERE id_especialista = %s AND est_especialista_especialidad = TRUE)
                GROUP BY 1
                ORDER BY cantidad DESC, 1
            """, [fecha_desde, fecha_hasta, id_especialista, id_especialista])
        return {'hechas': hechas, 'recibidas': recibidas,
                'total_hechas': sum(h['cantidad'] for h in hechas),
                'total_recibidas': sum(r['cantidad'] for r in recibidas)}

    # ------------------------------------------------------------------
    # Estadísticas reutilizables (inicio por rol, reportes y otras pantallas).
    # Los montos que se muestran como una sola cifra se limitan a la moneda
    # local, mismo criterio en todos los métodos de este bloque.
    # Para citas por estado de un día usar getAgendamientoReport(fecha, fecha).
    # ------------------------------------------------------------------

    def getResumenCuentasCobrar(self):
        """Cuentas PENDIENTE/PARCIAL de facturas no anuladas: totales y vencidas."""
        resumen = {'total': 0, 'vencidas': 0, 'monto_pendiente': 0,
                   'monto_vencido': 0, 'max_dias_atraso': 0}
        sql = """
            SELECT
                COUNT(*),
                COUNT(*) FILTER (WHERE esta_vencida),
                COALESCE(SUM(monto_pendiente) FILTER (WHERE es_moneda_local), 0),
                COALESCE(SUM(monto_pendiente) FILTER (WHERE es_moneda_local AND esta_vencida), 0),
                COALESCE(MAX(dias_atraso), 0)
            FROM v_saldo_cuentas_cobrar
            WHERE est_cuenta_cobrar = 'PENDIENTE' OR est_cuenta_cobrar = 'PARCIAL'
        """
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return resumen
        cur = con.cursor()
        try:
            cur.execute(sql)
            f = cur.fetchone()
            if f:
                resumen = {'total': int(f[0] or 0), 'vencidas': int(f[1] or 0),
                           'monto_pendiente': f[2] or 0, 'monto_vencido': f[3] or 0,
                           'max_dias_atraso': int(f[4] or 0)}
        except Exception as e:
            app.logger.error(f"Error en getResumenCuentasCobrar: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resumen

    def _redondear_monedas(self, filas, campos):
        """Redondea los montos de cada fila a los decimales de su moneda (decimales_moneda)."""
        for f in filas:
            dec = int(f.get('decimales_moneda') or 0)
            f['decimales_moneda'] = dec
            for campo in campos:
                f[campo] = round(float(f.get(campo) or 0), dec)
        return filas

    def getSaldoCuentasPorMoneda(self):
        """Saldo por cobrar (cuentas PENDIENTE/PARCIAL de facturas no anuladas) y vencido, una fila por moneda."""
        filas = self._consultar("""
            SELECT id_moneda, cod_moneda, simbolo_moneda, decimales_moneda,
                   COUNT(*) AS cuentas,
                   COUNT(*) FILTER (WHERE esta_vencida) AS vencidas,
                   COALESCE(SUM(monto_pendiente), 0) AS monto_pendiente,
                   COALESCE(SUM(monto_pendiente) FILTER (WHERE esta_vencida), 0) AS monto_vencido,
                   COALESCE(MAX(dias_atraso), 0) AS max_dias_atraso
            FROM v_saldo_cuentas_cobrar
            WHERE est_cuenta_cobrar = 'PENDIENTE' OR est_cuenta_cobrar = 'PARCIAL'
            GROUP BY id_moneda, cod_moneda, simbolo_moneda, decimales_moneda
            ORDER BY id_moneda
        """)
        return self._redondear_monedas(filas, ('monto_pendiente', 'monto_vencido'))

    def getCobradoPorMoneda(self, fecha_desde, fecha_hasta):
        """Cobranzas no anuladas del período, una fila por moneda (de v_caja_movimientos)."""
        filas = self._consultar("""
            SELECT id_moneda, cod_moneda, simbolo_moneda, decimales_moneda,
                   COUNT(*) AS cobranzas, COALESCE(SUM(monto), 0) AS cobrado
            FROM v_caja_movimientos
            WHERE tipo_movimiento = 'COBRANZA' AND estado <> 'ANULADA'
              AND fecha_movimiento::date BETWEEN %s AND %s
            GROUP BY id_moneda, cod_moneda, simbolo_moneda, decimales_moneda
            ORDER BY id_moneda
        """, [fecha_desde, fecha_hasta])
        return self._redondear_monedas(filas, ('cobrado',))

    def getFacturacionMensual(self, meses=6):
        """Facturación de los últimos `meses` meses (incluido el actual), por mes y moneda, con las notas de
        crédito restando (de v_facturacion_mensual)."""
        filas = self._consultar("""
            SELECT mes, id_moneda, cod_moneda, simbolo_moneda, decimales_moneda,
                   cantidad_facturas, cantidad_notas_credito, cantidad_comprobantes,
                   total_gravado, total_iva, total_neto, total_notas_credito
            FROM v_facturacion_mensual
            WHERE mes > date_trunc('month', CURRENT_DATE)::date - (%s * INTERVAL '1 month')
            ORDER BY mes, id_moneda
        """, [meses])
        return self._redondear_monedas(filas, ('total_gravado', 'total_iva', 'total_neto', 'total_notas_credito'))

    def getVentasDia(self, fecha):
        """Facturas no anuladas y cobranzas no anuladas de un día (montos en moneda local)."""
        resumen = {'facturas': 0, 'facturado': 0, 'cobranzas': 0, 'cobrado': 0}
        sql = """
            SELECT
                (SELECT COUNT(*) FROM facturas f
                  WHERE f.fecha_factura = %s AND f.fecha_anulacion IS NULL),
                (SELECT COALESCE(SUM(f.factura_total), 0) FROM facturas f
                   JOIN monedas m ON f.id_moneda = m.id_moneda AND m.es_moneda_local
                  WHERE f.fecha_factura = %s AND f.fecha_anulacion IS NULL),
                (SELECT COUNT(*) FROM cobranzas co
                  WHERE co.fecha_cobranza::DATE = %s AND co.est_cobranza != 'ANULADA'),
                (SELECT COALESCE(SUM(co.monto_cobrado), 0) FROM cobranzas co
                   JOIN monedas m ON co.id_moneda = m.id_moneda AND m.es_moneda_local
                  WHERE co.fecha_cobranza::DATE = %s AND co.est_cobranza != 'ANULADA')
        """
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return resumen
        cur = con.cursor()
        try:
            cur.execute(sql, (fecha, fecha, fecha, fecha))
            f = cur.fetchone()
            if f:
                resumen = {'facturas': int(f[0] or 0), 'facturado': f[1] or 0,
                           'cobranzas': int(f[2] or 0), 'cobrado': f[3] or 0}
        except Exception as e:
            app.logger.error(f"Error en getVentasDia: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resumen

    def getResumenConsultas(self, fecha, id_especialista=None):
        """Consultas registradas en el día y consultas abiertas (EN_ATENCION o pendientes de observación)."""
        resumen = {'consultas_dia': 0, 'abiertas': 0}
        sql = """
            SELECT
                COUNT(*) FILTER (WHERE c.consulta_fecha::DATE = %s),
                COUNT(*) FILTER (WHERE c.consulta_estado IN ('EN_ATENCION', 'EN_OBSERVACION'))
            FROM consultas c
            WHERE c.est_consulta = TRUE
        """
        parametros = [fecha]
        if id_especialista:
            sql += " AND c.id_especialista = %s"
            parametros.append(id_especialista)

        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return resumen
        cur = con.cursor()
        try:
            cur.execute(sql, tuple(parametros))
            f = cur.fetchone()
            if f:
                resumen = {'consultas_dia': int(f[0] or 0), 'abiertas': int(f[1] or 0)}
        except Exception as e:
            app.logger.error(f"Error en getResumenConsultas: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resumen

    def getResumenSeguridad(self, horas=24):
        """Intentos de acceso fallidos, sesiones y códigos MFA de las últimas `horas`,
        más los usuarios bloqueados en este momento (función esta_usuario_bloqueado)."""
        resumen = {'intentos_fallidos': 0, 'ips_distintas': 0, 'sesiones_activas': 0,
                   'usuarios_conectados': 0, 'mfa_enviados': 0, 'bloqueados': []}
        sql = """
            SELECT
                (SELECT COUNT(*) FROM accesos_sistema
                  WHERE resultado <> 'EXITOSO'
                    AND fecha_intento > CURRENT_TIMESTAMP - make_interval(hours => %s)),
                (SELECT COUNT(DISTINCT ip_origen) FROM accesos_sistema
                  WHERE resultado <> 'EXITOSO'
                    AND fecha_intento > CURRENT_TIMESTAMP - make_interval(hours => %s)),
                (SELECT COUNT(*) FROM sesiones
                  WHERE est_sesion = TRUE AND fecha_expiracion > CURRENT_TIMESTAMP),
                (SELECT COUNT(DISTINCT id_usuario) FROM sesiones
                  WHERE est_sesion = TRUE AND fecha_expiracion > CURRENT_TIMESTAMP),
                (SELECT COUNT(*) FROM mfa_codigos
                  WHERE fecha_generacion > CURRENT_TIMESTAMP - make_interval(hours => %s))
        """
        sql_bloqueados = """
            SELECT usu_nick, usu_nro_intentos
            FROM usuarios
            WHERE est_usuario = TRUE AND esta_usuario_bloqueado(id_usuario)
            ORDER BY usu_nick
        """
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return resumen
        cur = con.cursor()
        try:
            cur.execute(sql, (horas, horas, horas))
            f = cur.fetchone()
            if f:
                resumen.update({'intentos_fallidos': int(f[0] or 0), 'ips_distintas': int(f[1] or 0),
                                'sesiones_activas': int(f[2] or 0), 'usuarios_conectados': int(f[3] or 0),
                                'mfa_enviados': int(f[4] or 0)})
            cur.execute(sql_bloqueados)
            resumen['bloqueados'] = [{'usu_nick': b[0], 'intentos': int(b[1] or 0)} for b in cur.fetchall()]
        except Exception as e:
            app.logger.error(f"Error en getResumenSeguridad: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resumen
