from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

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

    def getMetricasDashboard(self):
        """
        Obtiene métricas rápidas para el dashboard central de reportes.
        Incluye KPIs de ventas, agenda y consultorio.
        """
        metricas = {
            'ventas_mes': 0,
            'citas_mes': 0,
            'pacientes_activos': 0,
            'recaudado_hoy': 0,
            # KPIs Ventas
            'porcentaje_cobrado': 0,
            'cuentas_pendientes': 0,
            # KPIs Agenda
            'porcentaje_asistencia': 0,
            'citas_canceladas': 0,
            # KPIs Clínico
            'diagnosticos_frecuentes': 0,
            'satisfaccion_paciente': 0,
        }
        
        # 1. Ventas del mes (libro_ventas)
        sql_ventas = """
            SELECT COALESCE(SUM(monto_total), 0) 
            FROM libro_ventas 
            WHERE DATE_TRUNC('month', libro_fecha) = DATE_TRUNC('month', CURRENT_DATE)
        """
        
        # 2. Citas del mes
        sql_citas = """
            SELECT COUNT(*) 
            FROM citas 
            WHERE DATE_TRUNC('month', cita_fecha) = DATE_TRUNC('month', CURRENT_DATE)
              AND cita_activo = TRUE
        """
        
        # 3. Pacientes activos
        sql_pacientes = """
            SELECT COUNT(*) FROM pacientes
        """
        
        # 4. Recaudado hoy (cobranzas)
        sql_recaudacion = """
            SELECT COALESCE(SUM(monto_cobrado), 0) 
            FROM cobranzas 
            WHERE DATE_TRUNC('day', fecha_cobranza) = DATE_TRUNC('day', CURRENT_DATE)
              AND est_cobranza != 'ANULADA'
        """
        
        # 5. Porcentaje cobrado este mes (cobranzas vs ventas)
        sql_porcentaje_cobrado = """
            SELECT
                CASE WHEN COALESCE(SUM(lv.monto_total), 0) = 0 THEN 0
                     ELSE ROUND(
                         (COALESCE(SUM(co.monto_cobrado), 0) * 100.0) / COALESCE(SUM(lv.monto_total), 1)
                     )
                END
            FROM libro_ventas lv
            LEFT JOIN cobranzas co ON co.id_factura = lv.id_factura
                AND co.est_cobranza != 'ANULADA'
            WHERE DATE_TRUNC('month', lv.libro_fecha) = DATE_TRUNC('month', CURRENT_DATE)
        """
        
        # 6. Cuentas pendientes de cobro
        sql_pendientes = """
            SELECT COUNT(*)
            FROM cuentas_cobrar
            WHERE est_cuenta_cobrar = 'PENDIENTE'
        """
        
        # 7. Citas atendidas vs total este mes (para asistencia y canceladas)
        sql_agenda_mes = """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE ec.est_cita_nombre IN ('COMPLETADA', 'ATENDIDA')) AS atendidas,
                COUNT(*) FILTER (WHERE ec.est_cita_nombre = 'CANCELADA') AS canceladas
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE DATE_TRUNC('month', c.cita_fecha) = DATE_TRUNC('month', CURRENT_DATE)
              AND c.cita_activo = TRUE
        """
        
        # 8. Diagnósticos únicos usados este mes
        sql_diagnosticos = """
            SELECT COUNT(DISTINCT rd.id_diagnostico)
            FROM registro_diagnosticos rd
            JOIN consultas c ON rd.id_consulta = c.id_consulta
            WHERE DATE_TRUNC('month', c.consulta_fecha) = DATE_TRUNC('month', CURRENT_DATE)
              AND c.est_consulta = 'A'
              AND rd.est_registro_diagnostico = 'A'
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        
        if not con:
            app.logger.error("No se pudo conectar a la base de datos en getMetricasDashboard")
            return metricas
            
        cur = con.cursor()
        
        try:
            # 1. Ventas del Mes
            try:
                cur.execute("""
                    SELECT COALESCE(SUM(monto_total), 0) 
                    FROM libro_ventas 
                    WHERE DATE_TRUNC('month', libro_fecha) = DATE_TRUNC('month', CURRENT_DATE)
                """)
                metricas['ventas_mes'] = int(cur.fetchone()[0] or 0)
            except Exception as e:
                app.logger.warning(f"Error query ventas_mes: {e}")

            # 2. Citas del Mes
            try:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM citas 
                    WHERE DATE_TRUNC('month', cita_fecha) = DATE_TRUNC('month', CURRENT_DATE)
                      AND cita_activo = TRUE
                """)
                metricas['citas_mes'] = int(cur.fetchone()[0] or 0)
            except Exception as e:
                app.logger.warning(f"Error query citas_mes: {e}")

            # 3. Pacientes Activos
            try:
                cur.execute("SELECT COUNT(*) FROM pacientes")
                metricas['pacientes_activos'] = int(cur.fetchone()[0] or 0)
            except Exception as e:
                app.logger.warning(f"Error query pacientes_activos: {e}")

            # 4. Recaudado Hoy
            try:
                cur.execute("""
                    SELECT COALESCE(SUM(monto_cobrado), 0) 
                    FROM cobranzas 
                    WHERE DATE_TRUNC('day', fecha_cobranza) = DATE_TRUNC('day', CURRENT_DATE)
                """)
                metricas['recaudado_hoy'] = int(cur.fetchone()[0] or 0)
            except Exception as e:
                app.logger.warning(f"Error query recaudado_hoy: {e}")

            # 5. Porcentaje Cobrado
            try:
                cur.execute("""
                    SELECT
                        CASE WHEN COALESCE(SUM(monto_total), 0) = 0 THEN 0
                             ELSE ROUND((COALESCE(SUM(monto_cobrado), 0) * 100.0) / COALESCE(SUM(monto_total), 1))
                        END
                    FROM (
                        SELECT COALESCE(SUM(lv.monto_total), 0) as monto_total,
                               (SELECT COALESCE(SUM(co.monto_cobrado), 0) 
                                FROM cobranzas co 
                                WHERE DATE_TRUNC('month', co.fecha_cobranza) = DATE_TRUNC('month', CURRENT_DATE)) as monto_cobrado
                        FROM libro_ventas lv
                        WHERE DATE_TRUNC('month', lv.libro_fecha) = DATE_TRUNC('month', CURRENT_DATE)
                    ) sub
                """)
                metricas['porcentaje_cobrado'] = int(cur.fetchone()[0] or 0)
            except Exception as e:
                app.logger.warning(f"Error query porcentaje_cobrado: {e}")

            # 6. Cuentas Pendientes
            try:
                cur.execute("SELECT COUNT(*) FROM cuentas_cobrar WHERE est_cuenta_cobrar = 'PENDIENTE'")
                metricas['cuentas_pendientes'] = int(cur.fetchone()[0] or 0)
            except Exception as e:
                app.logger.warning(f"Error query cuentas_pendientes: {e}")

            # 7. Agenda
            try:
                cur.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(*) FILTER (WHERE ec.est_cita_nombre IN ('COMPLETADA', 'ATENDIDA')) as atendidas,
                        COUNT(*) FILTER (WHERE ec.est_cita_nombre = 'CANCELADA') as canceladas
                    FROM citas c
                    JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                    WHERE DATE_TRUNC('month', c.cita_fecha) = DATE_TRUNC('month', CURRENT_DATE)
                      AND c.cita_activo = TRUE
                """)
                fila = cur.fetchone()
                if fila:
                    total = int(fila[0] or 0)
                    atendidas = int(fila[1] or 0)
                    metricas['citas_canceladas'] = int(fila[2] or 0)
                    if total > 0:
                        metricas['porcentaje_asistencia'] = round((atendidas * 100.0) / total)
                        metricas['satisfaccion_paciente'] = metricas['porcentaje_asistencia']
            except Exception as e:
                app.logger.warning(f"Error query agenda: {e}")

            # 8. Diagnósticos
            try:
                cur.execute("""
                    SELECT COUNT(DISTINCT rd.id_diagnostico)
                    FROM registro_diagnosticos rd
                    JOIN consultas c ON rd.id_consulta = c.id_consulta
                    WHERE DATE_TRUNC('month', c.consulta_fecha) = DATE_TRUNC('month', CURRENT_DATE)
                      AND c.est_consulta = 'A'
                      AND rd.est_registro_diagnostico = 'A'
                """)
                metricas['diagnosticos_frecuentes'] = int(cur.fetchone()[0] or 0)
            except Exception as e:
                app.logger.warning(f"Error query diagnosticos: {e}")
                
        except Exception as e:
            app.logger.error(f"Error general en getMetricasDashboard: {str(e)}")
        finally:
            cur.close()
            con.close()
            
        return metricas

    def getVentasReport(self, fecha_desde, fecha_hasta, metodo_pago=None):
        """
        Obtiene ventas agrupadas por día para el gráfico, consumiendo libro_ventas.
        Soporta filtro opcional por método de pago (condicion_venta de factura).
        """
        sql = """
            SELECT 
                lv.libro_fecha AS fecha,
                COUNT(*) AS cantidad_comprobantes,
                SUM(lv.monto_gravado) AS total_gravado,
                SUM(lv.monto_iva) AS total_iva,
                SUM(lv.monto_total) AS total_general
            FROM libro_ventas lv
            LEFT JOIN facturas f ON lv.id_factura = f.id_factura
            LEFT JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            WHERE lv.libro_fecha >= %s AND lv.libro_fecha <= %s
        """
        
        parametros = [fecha_desde, fecha_hasta]
        
        if metodo_pago and metodo_pago.lower() != 'todos':
            # Se asume que metodo_pago es 'Contado' o 'Credito'
            sql += " AND LOWER(cv.des_condicion_venta) LIKE LOWER(%s)"
            parametros.append(f"%{metodo_pago}%")
            
        sql += " GROUP BY lv.libro_fecha ORDER BY lv.libro_fecha ASC"
        
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
                resultados.append({
                    'fecha': f[0].strftime('%Y-%m-%d') if f[0] else '',
                    'cantidad_comprobantes': int(f[1] or 0),
                    'total_gravado': int(f[2] or 0),
                    'total_iva': int(f[3] or 0),
                    'total_general': int(f[4] or 0)
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
                lv.monto_total AS total
            FROM libro_ventas lv
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
            
        sql += " ORDER BY lv.libro_fecha ASC, lv.id_libro_venta ASC"
        
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []
        
        try:
            cur.execute(sql, tuple(parametros))
            for f in cur.fetchall():
                resultados.append({
                    'fecha': f[0].strftime('%Y-%m-%d') if f[0] else '',
                    'numero_comprobante': f[1],
                    'nombre_cliente': f[2],
                    'ruc_cliente': f[3],
                    'metodo_pago': f[4],
                    'gravado': int(f[5] or 0),
                    'iva': int(f[6] or 0),
                    'total': int(f[7] or 0)
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
                COUNT(*) AS cantidad,
                SUM(lv.monto_total) AS total
            FROM libro_ventas lv
            LEFT JOIN facturas f ON lv.id_factura = f.id_factura
            LEFT JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            WHERE lv.libro_fecha >= %s AND lv.libro_fecha <= %s
            GROUP BY COALESCE(cv.des_condicion_venta, 'Contado')
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []
        
        try:
            cur.execute(sql, (fecha_desde, fecha_hasta))
            for f in cur.fetchall():
                resultados.append({
                    'metodo_pago': f[0],
                    'cantidad': int(f[1] or 0),
                    'total': int(f[2] or 0)
                })
        except Exception as e:
            app.logger.error(f"Error en getVentasPorMetodoPago: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resultados

    def getAgendamientoReport(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Métricas agrupadas por estado de cita para Agendamiento"""
        sql = """
            SELECT 
                ec.est_cita_nombre AS estado,
                COUNT(*) AS cantidad
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha >= %s AND c.cita_fecha <= %s AND c.cita_activo = TRUE
        """
        parametros = [fecha_desde, fecha_hasta]
        
        if id_especialista and str(id_especialista) != '0':
            sql += " AND c.id_especialista = %s"
            parametros.append(id_especialista)
            
        sql += " GROUP BY ec.est_cita_nombre"
        
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []
        try:
            cur.execute(sql, tuple(parametros))
            for f in cur.fetchall():
                resultados.append({'estado': f[0], 'cantidad': int(f[1] or 0)})
        except Exception as e:
            app.logger.error(f"Error en getAgendamientoReport: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resultados

    def getAgendamientoPorDia(self, fecha_desde, fecha_hasta, id_especialista=None):
        """Evolución diaria de citas por estado clave (Atendidas, Canceladas, Ausentes)"""
        sql = """
            SELECT 
                c.cita_fecha::DATE AS fecha,
                COUNT(*) FILTER (WHERE ec.est_cita_nombre IN ('COMPLETADA', 'ATENDIDA')) AS cant_atendidas,
                COUNT(*) FILTER (WHERE ec.est_cita_nombre = 'CANCELADA') AS cant_canceladas,
                COUNT(*) FILTER (WHERE ec.est_cita_nombre IN ('INASISTENCIA', 'AUSENTE')) AS cant_ausencias
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha >= %s AND c.cita_fecha <= %s AND c.cita_activo = TRUE
        """
        parametros = [fecha_desde, fecha_hasta]
        
        if id_especialista and str(id_especialista) != '0':
            sql += " AND c.id_especialista = %s"
            parametros.append(id_especialista)
            
        sql += " GROUP BY c.cita_fecha::DATE ORDER BY c.cita_fecha::DATE ASC"
        
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []
        try:
            cur.execute(sql, tuple(parametros))
            for f in cur.fetchall():
                resultados.append({
                    'fecha': f[0].strftime('%Y-%m-%d') if f[0] else '',
                    'cant_atendidas': int(f[1] or 0),
                    'cant_canceladas': int(f[2] or 0),
                    'cant_ausencias': int(f[3] or 0)
                })
        except Exception as e:
            app.logger.error(f"Error en getAgendamientoPorDia: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resultados

    def getConsultasPorEspecialidad(self, fecha_desde, fecha_hasta):
        """Cantidad de consultas agrupadas por especialidad médica"""
        sql = """
            WITH consultas_reales AS (
                SELECT 
                    COALESCE(e1.des_especialidad, e2.des_especialidad, 'Sin Especialidad') AS especialidad
                FROM consultas c
                INNER JOIN especialistas ee ON c.id_profesional = ee.id_especialista
                LEFT JOIN citas cit ON c.id_cita = cit.id_cita
                LEFT JOIN especialidades e1 ON cit.id_especialidad = e1.id_especialidad
                LEFT JOIN (
                    SELECT DISTINCT ON (id_especialista) id_especialista, id_especialidad 
                    FROM especialista_especialidades
                ) ese ON ee.id_especialista = ese.id_especialista
                LEFT JOIN especialidades e2 ON ese.id_especialidad = e2.id_especialidad
                WHERE c.consulta_fecha::DATE >= %s AND c.consulta_fecha::DATE <= %s AND c.est_consulta = 'A'
            ),
            citas_atendidas AS (
                SELECT 
                    esp.des_especialidad AS especialidad
                FROM citas cit
                INNER JOIN estados_citas ec ON cit.id_estado_cita = ec.id_estado_cita
                INNER JOIN especialidades esp ON cit.id_especialidad = esp.id_especialidad
                WHERE cit.cita_fecha::DATE >= %s AND cit.cita_fecha::DATE <= %s
                  AND ec.est_cita_nombre IN ('ATENDIDA', 'COMPLETADA', 'CONFIRMADA')
                  AND cit.cita_activo = TRUE
                  AND NOT EXISTS (SELECT 1 FROM consultas c2 WHERE c2.id_cita = cit.id_cita)
            )
            SELECT especialidad, COUNT(*) AS cantidad
            FROM (
                SELECT especialidad FROM consultas_reales
                UNION ALL
                SELECT especialidad FROM citas_atendidas
            ) combined
            GROUP BY 1
            ORDER BY cantidad DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []
        try:
            # Pasamos los parámetros 2 veces (una para cada CTE)
            cur.execute(sql, (fecha_desde, fecha_hasta, fecha_desde, fecha_hasta))
            for f in cur.fetchall():
                resultados.append({'especialidad': f[0], 'cantidad': int(f[1] or 0)})
        except Exception as e:
            app.logger.error(f"Error en getConsultasPorEspecialidad: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resultados

    def getTopDiagnosticos(self, fecha_desde, fecha_hasta):
        """Top 5 de diagnósticos más frecuentes en el rango de fechas"""
        sql = """
            SELECT d.des_diagnostico, COUNT(*) AS cantidad
            FROM registro_diagnosticos rd
            JOIN diagnosticos d ON rd.id_diagnostico = d.id_diagnostico
            JOIN consultas c ON rd.id_consulta = c.id_consulta
            WHERE c.consulta_fecha::DATE >= %s AND c.consulta_fecha::DATE <= %s 
              AND c.est_consulta = 'A' AND rd.est_registro_diagnostico = 'A'
            GROUP BY d.des_diagnostico
            ORDER BY cantidad DESC
            LIMIT 5
        """
        conexion = Conexion()
        con = conexion.getConexion()
        if not con: return []
        cur = con.cursor()
        resultados = []
        try:
            cur.execute(sql, (fecha_desde, fecha_hasta))
            for f in cur.fetchall():
                resultados.append({'diagnostico': f[0], 'cantidad': int(f[1] or 0)})
        except Exception as e:
            app.logger.error(f"Error en getTopDiagnosticos: {str(e)}")
        finally:
            cur.close()
            con.close()
        return resultados
