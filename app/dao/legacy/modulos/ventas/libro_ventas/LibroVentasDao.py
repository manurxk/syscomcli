from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

class LibroVentasDao:
    """DAO para gestionar libro de ventas (registro contable)"""
    
    def getLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        """Obtiene todas las entradas del libro de ventas"""
        libroSQL = """
            SELECT
                lv.id_libro_venta,
                lv.libro_fecha,
                lv.id_factura,
                lv.id_nota_credito,
                lv.id_nota_debito,
                lv.tipo_comprobante,
                lv.numero_comprobante,
                lv.id_paciente,
                lv.monto_gravado,
                lv.monto_exento,
                lv.monto_iva,
                lv.monto_total,
                lv.codigo_sifen,
                lv.numero_timbrado,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula
            FROM libro_ventas lv
            JOIN pacientes pac ON lv.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
        """
        
        condiciones = []
        valores = []
        
        if fecha_desde:
            condiciones.append("lv.libro_fecha >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("lv.libro_fecha <= %s")
            valores.append(fecha_hasta)
        
        if condiciones:
            libroSQL += " WHERE " + " AND ".join(condiciones)
        
        libroSQL += " ORDER BY lv.libro_fecha DESC, lv.id_libro_venta DESC"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(libroSQL, tuple(valores) if valores else None)
            entradas = cur.fetchall()
            
            return [{
                'id_libro_venta': ent[0],
                'libro_fecha': ent[1].strftime('%d/%m/%Y') if ent[1] else None,
                'id_factura': ent[2],
                'id_nota_credito': ent[3],
                'id_nota_debito': ent[4],
                'tipo_comprobante': ent[5],
                'numero_comprobante': ent[6],
                'id_paciente': ent[7],
                'monto_gravado': ent[8],
                'monto_exento': ent[9],
                'monto_iva': ent[10],
                'monto_total': ent[11],
                'codigo_sifen': ent[12],
                'numero_timbrado': ent[13],
                'historia_clinica': ent[14],
                'paciente_nombre': ent[15],
                'paciente_cedula': ent[16]
            } for ent in entradas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener libro de ventas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getLibroVentasById(self, id_libro_venta):
        """Obtiene una entrada específica del libro de ventas por ID"""
        libroSQL = """
            SELECT
                lv.id_libro_venta,
                lv.libro_fecha,
                lv.id_factura,
                lv.id_nota_credito,
                lv.id_nota_debito,
                lv.tipo_comprobante,
                lv.numero_comprobante,
                lv.id_paciente,
                lv.monto_gravado,
                lv.monto_exento,
                lv.monto_iva,
                lv.monto_total,
                lv.codigo_sifen,
                lv.numero_timbrado,
                lv.fecha_creacion,
                lv.usuario_creacion,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula
            FROM libro_ventas lv
            JOIN pacientes pac ON lv.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            WHERE lv.id_libro_venta = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(libroSQL, (id_libro_venta,))
            ent = cur.fetchone()
            
            if not ent:
                return None
            
            return {
                'id_libro_venta': ent[0],
                'libro_fecha': ent[1].strftime('%Y-%m-%d') if ent[1] else None,
                'id_factura': ent[2],
                'id_nota_credito': ent[3],
                'id_nota_debito': ent[4],
                'tipo_comprobante': ent[5],
                'numero_comprobante': ent[6],
                'id_paciente': ent[7],
                'monto_gravado': ent[8],
                'monto_exento': ent[9],
                'monto_iva': ent[10],
                'monto_total': ent[11],
                'codigo_sifen': ent[12],
                'numero_timbrado': ent[13],
                'fecha_creacion': ent[14].strftime('%Y-%m-%d %H:%M:%S') if ent[14] else None,
                'usuario_creacion': ent[15],
                'historia_clinica': ent[16],
                'paciente_nombre': ent[17],
                'paciente_cedula': ent[18]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener entrada del libro de ventas por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getResumenLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        """Obtiene un resumen del libro de ventas (totales por tipo)"""
        resumenSQL = """
            SELECT
                tipo_comprobante,
                COUNT(*) AS cantidad,
                SUM(monto_gravado) AS total_gravado,
                SUM(monto_exento) AS total_exento,
                SUM(monto_iva) AS total_iva,
                SUM(monto_total) AS total_total
            FROM libro_ventas
        """
        
        condiciones = []
        valores = []
        
        if fecha_desde:
            condiciones.append("libro_fecha >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("libro_fecha <= %s")
            valores.append(fecha_hasta)
        
        if condiciones:
            resumenSQL += " WHERE " + " AND ".join(condiciones)
        
        resumenSQL += " GROUP BY tipo_comprobante ORDER BY tipo_comprobante"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(resumenSQL, tuple(valores) if valores else None)
            resumenes = cur.fetchall()
            
            return [{
                'tipo_comprobante': res[0],
                'cantidad': res[1],
                'total_gravado': res[2],
                'total_exento': res[3],
                'total_iva': res[4],
                'total_total': res[5]
            } for res in resumenes]
            
        except Exception as e:
            app.logger.error(f"Error al obtener resumen del libro de ventas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getTotalesLibroVentas(self, fecha_desde=None, fecha_hasta=None):
        """Obtiene los totales generales del libro de ventas"""
        totalesSQL = """
            SELECT
                COUNT(*) AS total_registros,
                SUM(monto_gravado) AS total_gravado,
                SUM(monto_exento) AS total_exento,
                SUM(monto_iva) AS total_iva,
                SUM(monto_total) AS total_total
            FROM libro_ventas
        """
        
        condiciones = []
        valores = []
        
        if fecha_desde:
            condiciones.append("libro_fecha >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("libro_fecha <= %s")
            valores.append(fecha_hasta)
        
        if condiciones:
            totalesSQL += " WHERE " + " AND ".join(condiciones)
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(totalesSQL, tuple(valores) if valores else None)
            totales = cur.fetchone()
            
            if totales:
                return {
                    'total_registros': totales[0] or 0,
                    'total_gravado': totales[1] or 0,
                    'total_exento': totales[2] or 0,
                    'total_iva': totales[3] or 0,
                    'total_total': totales[4] or 0
                }
            else:
                return {
                    'total_registros': 0,
                    'total_gravado': 0,
                    'total_exento': 0,
                    'total_iva': 0,
                    'total_total': 0
                }
        except Exception as e:
            app.logger.error(f"Error al obtener totales del libro de ventas: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def registrarEntradaLibroVentas(self, libro_fecha, tipo_comprobante, numero_comprobante,
                                   id_paciente, monto_gravado=0, monto_exento=0, monto_iva=0,
                                   monto_total=0, id_factura=None, id_nota_credito=None,
                                   id_nota_debito=None, codigo_sifen=None, numero_timbrado=None,
                                   usuario_creacion='SISTEMA'):
        """Registra una entrada en el libro de ventas"""
        
        if not all([libro_fecha, tipo_comprobante, numero_comprobante, id_paciente]):
            app.logger.error("Faltan campos obligatorios para registrar en libro de ventas")
            return None
        
        insertLibroSQL = """
            INSERT INTO libro_ventas(
                libro_fecha, id_factura, id_nota_credito, id_nota_debito,
                tipo_comprobante, numero_comprobante, id_paciente,
                monto_gravado, monto_exento, monto_iva, monto_total,
                codigo_sifen, numero_timbrado, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_libro_venta
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando entrada en libro de ventas: {tipo_comprobante} - {numero_comprobante}")
            
            cur.execute(insertLibroSQL, (
                libro_fecha,
                id_factura,
                id_nota_credito,
                id_nota_debito,
                tipo_comprobante,
                numero_comprobante,
                id_paciente,
                monto_gravado,
                monto_exento,
                monto_iva,
                monto_total,
                codigo_sifen,
                numero_timbrado,
                usuario_creacion
            ))
            
            libro_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Entrada registrada en libro de ventas con ID: {libro_id}")
            return libro_id
            
        except Exception as e:
            app.logger.error(f"Error al registrar entrada en libro de ventas: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()


















