from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

class NotaCreditoDao:
    """DAO para gestionar notas de crédito"""
    
    def getNotasCredito(self):
        """Obtiene todas las notas de crédito"""
        notaSQL = """
            SELECT
                nc.id_nota_credito,
                nc.nota_credito_numero,
                nc.id_factura,
                nc.id_tipo_comprobante,
                nc.fecha_nota_credito,
                nc.motivo_nota_credito,
                nc.monto_total,
                nc.codigo_sifen,
                nc.numero_timbrado,
                nc.observaciones,
                nc.est_nota_credito,
                nc.fecha_creacion,
                -- Datos de la factura
                f.factura_numero,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                -- Datos del tipo de comprobante
                tc.des_tipo_comprobante
            FROM notas_credito nc
            JOIN facturas f ON nc.id_factura = f.id_factura
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON nc.id_tipo_comprobante = tc.id_tipo_comprobante
            ORDER BY nc.fecha_nota_credito DESC, nc.id_nota_credito DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(notaSQL)
            notas = cur.fetchall()
            
            return [{
                'id_nota_credito': nota[0],
                'nota_credito_numero': nota[1],
                'id_factura': nota[2],
                'id_tipo_comprobante': nota[3],
                'fecha_nota_credito': nota[4].strftime('%d/%m/%Y %H:%M') if nota[4] else None,
                'motivo_nota_credito': nota[5],
                'monto_total': nota[6],
                'codigo_sifen': nota[7],
                'numero_timbrado': nota[8],
                'observaciones': nota[9],
                'est_nota_credito': nota[10],
                'fecha_registro': nota[11].strftime('%d/%m/%Y') if nota[11] else None,
                'factura_numero': nota[12],
                'historia_clinica': nota[13],
                'paciente_nombre': nota[14],
                'tipo_comprobante': nota[15]
            } for nota in notas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las notas de crédito: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getNotaCreditoById(self, id_nota_credito):
        """Obtiene una nota de crédito específica por ID"""
        notaSQL = """
            SELECT
                nc.id_nota_credito,
                nc.nota_credito_numero,
                nc.id_factura,
                nc.id_tipo_comprobante,
                nc.fecha_nota_credito,
                nc.motivo_nota_credito,
                nc.monto_total,
                nc.codigo_sifen,
                nc.numero_timbrado,
                nc.observaciones,
                nc.est_nota_credito,
                nc.fecha_creacion,
                nc.usuario_creacion,
                -- Datos de la factura
                f.factura_numero,
                f.factura_total,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del tipo de comprobante
                tc.des_tipo_comprobante
            FROM notas_credito nc
            JOIN facturas f ON nc.id_factura = f.id_factura
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON nc.id_tipo_comprobante = tc.id_tipo_comprobante
            WHERE nc.id_nota_credito = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(notaSQL, (id_nota_credito,))
            nota = cur.fetchone()
            
            if not nota:
                return None
            
            return {
                'id_nota_credito': nota[0],
                'nota_credito_numero': nota[1],
                'id_factura': nota[2],
                'id_tipo_comprobante': nota[3],
                'fecha_nota_credito': nota[4].strftime('%Y-%m-%d %H:%M:%S') if nota[4] else None,
                'motivo_nota_credito': nota[5],
                'monto_total': nota[6],
                'codigo_sifen': nota[7],
                'numero_timbrado': nota[8],
                'observaciones': nota[9],
                'est_nota_credito': nota[10],
                'fecha_registro': nota[11].strftime('%Y-%m-%d') if nota[11] else None,
                'usuario_creacion': nota[12],
                'factura_numero': nota[13],
                'factura_total': nota[14],
                'historia_clinica': nota[15],
                'paciente_nombre': nota[16],
                'paciente_cedula': nota[17],
                'tipo_comprobante': nota[18]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener nota de crédito por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getNotaCreditoDetalle(self, id_nota_credito):
        """Obtiene el detalle completo de una nota de crédito"""
        detalleSQL = """
            SELECT
                ncd.id_nota_credito_detalle,
                ncd.id_nota_credito,
                ncd.id_factura_detalle,
                ncd.item_descripcion,
                ncd.item_cantidad,
                ncd.item_precio_unitario,
                ncd.monto_total
            FROM nota_credito_detalle ncd
            WHERE ncd.id_nota_credito = %s
            ORDER BY ncd.id_nota_credito_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_nota_credito,))
            detalles = cur.fetchall()
            
            return [{
                'id_nota_credito_detalle': d[0],
                'id_nota_credito': d[1],
                'id_factura_detalle': d[2],
                'item_descripcion': d[3],
                'item_cantidad': d[4],
                'item_precio_unitario': d[5],
                'monto_total': d[6]
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle de la nota de crédito: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroNotaCredito(self):
        """Genera un número único de nota de crédito"""
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        
        # Buscar el último número del mes
        sql = """
            SELECT nota_credito_numero 
            FROM notas_credito 
            WHERE nota_credito_numero LIKE %s
            ORDER BY nota_credito_numero DESC 
            LIMIT 1
        """
        patron = f'NC-{año}-{mes}-%'
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (patron,))
            ultimo = cur.fetchone()
            
            if ultimo and ultimo[0]:
                # Extraer el número secuencial
                partes = ultimo[0].split('-')
                if len(partes) == 4:
                    siguiente_num = int(partes[3]) + 1
                else:
                    siguiente_num = 1
            else:
                siguiente_num = 1
            
            return f'NC-{año}-{mes}-{siguiente_num:04d}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de nota de crédito: {str(e)}")
            return f'NC-{año}-{mes}-0001'
        finally:
            cur.close()
            con.close()
    
    def guardarNotaCredito(self, id_factura, id_tipo_comprobante, motivo_nota_credito,
                          monto_total, codigo_sifen=None, numero_timbrado=None,
                          observaciones=None, usuario_creacion='ADMIN'):
        """Registra una nueva nota de crédito"""
        
        if not all([id_factura, id_tipo_comprobante, motivo_nota_credito, monto_total]):
            app.logger.error("Faltan campos obligatorios para guardar nota de crédito")
            return None
        
        # Generar número de nota de crédito
        nota_credito_numero = self._generarNumeroNotaCredito()
        
        insertNotaSQL = """
            INSERT INTO notas_credito(
                nota_credito_numero, id_factura, id_tipo_comprobante,
                motivo_nota_credito, monto_total, codigo_sifen, numero_timbrado,
                observaciones, est_nota_credito, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'REGISTRADA', %s)
            RETURNING id_nota_credito
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando nota de crédito para factura ID: {id_factura}")
            
            cur.execute(insertNotaSQL, (
                nota_credito_numero,
                id_factura,
                id_tipo_comprobante,
                motivo_nota_credito,
                monto_total,
                codigo_sifen,
                numero_timbrado,
                observaciones,
                usuario_creacion
            ))
            
            nota_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Nota de crédito guardada exitosamente con ID: {nota_id}")
            return nota_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar nota de crédito: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarNotaCreditoDetalle(self, id_nota_credito, item_descripcion, item_cantidad,
                                  item_precio_unitario, monto_total, id_factura_detalle=None):
        """Guarda un detalle de nota de crédito"""
        
        if not all([id_nota_credito, item_descripcion, monto_total]):
            app.logger.error("Faltan campos obligatorios para guardar detalle de nota de crédito")
            return None
        
        insertDetalleSQL = """
            INSERT INTO nota_credito_detalle(
                id_nota_credito, id_factura_detalle, item_descripcion,
                item_cantidad, item_precio_unitario, monto_total
            )
            VALUES(%s, %s, %s, %s, %s, %s)
            RETURNING id_nota_credito_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_nota_credito,
                id_factura_detalle,
                item_descripcion,
                item_cantidad or 1,
                item_precio_unitario,
                monto_total
            ))
            
            detalle_id = cur.fetchone()[0]
            con.commit()
            return detalle_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar detalle de nota de crédito: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def updateNotaCredito(self, id_nota_credito, motivo_nota_credito=None,
                         observaciones=None, est_nota_credito=None,
                         usuario_modificacion='ADMIN'):
        """Actualiza una nota de crédito existente"""
        
        campos = []
        valores = []
        
        if motivo_nota_credito is not None:
            campos.append("motivo_nota_credito = %s")
            valores.append(motivo_nota_credito)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if est_nota_credito:
            campos.append("est_nota_credito = %s")
            valores.append(est_nota_credito)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_nota_credito)
        
        updateSQL = f"""
            UPDATE notas_credito
            SET {', '.join(campos)}
            WHERE id_nota_credito = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, tuple(valores))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar nota de crédito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def anularNotaCredito(self, id_nota_credito, motivo_anulacion, usuario='ADMIN'):
        """Anula una nota de crédito"""
        return self.updateNotaCredito(
            id_nota_credito=id_nota_credito,
            observaciones=motivo_anulacion,
            est_nota_credito='ANULADA',
            usuario_modificacion=usuario
        )
    
    def getNotasCreditoPorFactura(self, id_factura):
        """Obtiene todas las notas de crédito de una factura"""
        sql = """
            SELECT
                nc.id_nota_credito,
                nc.nota_credito_numero,
                nc.fecha_nota_credito,
                nc.monto_total,
                nc.est_nota_credito
            FROM notas_credito nc
            WHERE nc.id_factura = %s
            ORDER BY nc.fecha_nota_credito DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_factura,))
            notas = cur.fetchall()
            
            return [{
                'id_nota_credito': nota[0],
                'nota_credito_numero': nota[1],
                'fecha_nota_credito': nota[2].strftime('%d/%m/%Y %H:%M') if nota[2] else None,
                'monto_total': nota[3],
                'est_nota_credito': nota[4]
            } for nota in notas]
        except Exception as e:
            app.logger.error(f"Error al obtener notas de crédito de la factura: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()


















