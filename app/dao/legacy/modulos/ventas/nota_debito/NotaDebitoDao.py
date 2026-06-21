from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

class NotaDebitoDao:
    """DAO para gestionar notas de débito"""
    
    def getNotasDebito(self):
        """Obtiene todas las notas de débito"""
        notaSQL = """
            SELECT
                nd.id_nota_debito,
                nd.nota_debito_numero,
                nd.id_factura,
                nd.id_tipo_comprobante,
                nd.fecha_nota_debito,
                nd.motivo_nota_debito,
                nd.monto_total,
                nd.codigo_sifen,
                nd.numero_timbrado,
                nd.observaciones,
                nd.est_nota_debito,
                nd.fecha_creacion,
                -- Datos de la factura
                f.factura_numero,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                -- Datos del tipo de comprobante
                tc.des_tipo_comprobante
            FROM notas_debito nd
            JOIN facturas f ON nd.id_factura = f.id_factura
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON nd.id_tipo_comprobante = tc.id_tipo_comprobante
            ORDER BY nd.fecha_nota_debito DESC, nd.id_nota_debito DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(notaSQL)
            notas = cur.fetchall()
            
            return [{
                'id_nota_debito': nota[0],
                'nota_debito_numero': nota[1],
                'id_factura': nota[2],
                'id_tipo_comprobante': nota[3],
                'fecha_nota_debito': nota[4].strftime('%d/%m/%Y %H:%M') if nota[4] else None,
                'motivo_nota_debito': nota[5],
                'monto_total': nota[6],
                'codigo_sifen': nota[7],
                'numero_timbrado': nota[8],
                'observaciones': nota[9],
                'est_nota_debito': nota[10],
                'fecha_registro': nota[11].strftime('%d/%m/%Y') if nota[11] else None,
                'factura_numero': nota[12],
                'historia_clinica': nota[13],
                'paciente_nombre': nota[14],
                'tipo_comprobante': nota[15]
            } for nota in notas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las notas de débito: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getNotaDebitoById(self, id_nota_debito):
        """Obtiene una nota de débito específica por ID"""
        notaSQL = """
            SELECT
                nd.id_nota_debito,
                nd.nota_debito_numero,
                nd.id_factura,
                nd.id_tipo_comprobante,
                nd.fecha_nota_debito,
                nd.motivo_nota_debito,
                nd.monto_total,
                nd.codigo_sifen,
                nd.numero_timbrado,
                nd.observaciones,
                nd.est_nota_debito,
                nd.fecha_creacion,
                nd.usuario_creacion,
                -- Datos de la factura
                f.factura_numero,
                f.factura_total,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del tipo de comprobante
                tc.des_tipo_comprobante
            FROM notas_debito nd
            JOIN facturas f ON nd.id_factura = f.id_factura
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON nd.id_tipo_comprobante = tc.id_tipo_comprobante
            WHERE nd.id_nota_debito = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(notaSQL, (id_nota_debito,))
            nota = cur.fetchone()
            
            if not nota:
                return None
            
            return {
                'id_nota_debito': nota[0],
                'nota_debito_numero': nota[1],
                'id_factura': nota[2],
                'id_tipo_comprobante': nota[3],
                'fecha_nota_debito': nota[4].strftime('%Y-%m-%d %H:%M:%S') if nota[4] else None,
                'motivo_nota_debito': nota[5],
                'monto_total': nota[6],
                'codigo_sifen': nota[7],
                'numero_timbrado': nota[8],
                'observaciones': nota[9],
                'est_nota_debito': nota[10],
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
            app.logger.error(f"Error al obtener nota de débito por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getNotaDebitoDetalle(self, id_nota_debito):
        """Obtiene el detalle completo de una nota de débito"""
        detalleSQL = """
            SELECT
                ndd.id_nota_debito_detalle,
                ndd.id_nota_debito,
                ndd.id_factura_detalle,
                ndd.item_descripcion,
                ndd.item_cantidad,
                ndd.item_precio_unitario,
                ndd.monto_total
            FROM nota_debito_detalle ndd
            WHERE ndd.id_nota_debito = %s
            ORDER BY ndd.id_nota_debito_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_nota_debito,))
            detalles = cur.fetchall()
            
            return [{
                'id_nota_debito_detalle': d[0],
                'id_nota_debito': d[1],
                'id_factura_detalle': d[2],
                'item_descripcion': d[3],
                'item_cantidad': d[4],
                'item_precio_unitario': d[5],
                'monto_total': d[6]
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle de la nota de débito: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroNotaDebito(self):
        """Genera un número único de nota de débito"""
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        
        # Buscar el último número del mes
        sql = """
            SELECT nota_debito_numero 
            FROM notas_debito 
            WHERE nota_debito_numero LIKE %s
            ORDER BY nota_debito_numero DESC 
            LIMIT 1
        """
        patron = f'ND-{año}-{mes}-%'
        
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
            
            return f'ND-{año}-{mes}-{siguiente_num:04d}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de nota de débito: {str(e)}")
            return f'ND-{año}-{mes}-0001'
        finally:
            cur.close()
            con.close()
    
    def guardarNotaDebito(self, id_factura, id_tipo_comprobante, motivo_nota_debito,
                         monto_total, codigo_sifen=None, numero_timbrado=None,
                         observaciones=None, usuario_creacion='ADMIN'):
        """Registra una nueva nota de débito"""
        
        if not all([id_factura, id_tipo_comprobante, motivo_nota_debito, monto_total]):
            app.logger.error("Faltan campos obligatorios para guardar nota de débito")
            return None
        
        # Generar número de nota de débito
        nota_debito_numero = self._generarNumeroNotaDebito()
        
        insertNotaSQL = """
            INSERT INTO notas_debito(
                nota_debito_numero, id_factura, id_tipo_comprobante,
                motivo_nota_debito, monto_total, codigo_sifen, numero_timbrado,
                observaciones, est_nota_debito, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'REGISTRADA', %s)
            RETURNING id_nota_debito
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando nota de débito para factura ID: {id_factura}")
            
            cur.execute(insertNotaSQL, (
                nota_debito_numero,
                id_factura,
                id_tipo_comprobante,
                motivo_nota_debito,
                monto_total,
                codigo_sifen,
                numero_timbrado,
                observaciones,
                usuario_creacion
            ))
            
            nota_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Nota de débito guardada exitosamente con ID: {nota_id}")
            return nota_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar nota de débito: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarNotaDebitoDetalle(self, id_nota_debito, item_descripcion, item_cantidad,
                                 item_precio_unitario, monto_total, id_factura_detalle=None):
        """Guarda un detalle de nota de débito"""
        
        if not all([id_nota_debito, item_descripcion, monto_total]):
            app.logger.error("Faltan campos obligatorios para guardar detalle de nota de débito")
            return None
        
        insertDetalleSQL = """
            INSERT INTO nota_debito_detalle(
                id_nota_debito, id_factura_detalle, item_descripcion,
                item_cantidad, item_precio_unitario, monto_total
            )
            VALUES(%s, %s, %s, %s, %s, %s)
            RETURNING id_nota_debito_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_nota_debito,
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
            app.logger.error(f"Error al guardar detalle de nota de débito: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def updateNotaDebito(self, id_nota_debito, motivo_nota_debito=None,
                        observaciones=None, est_nota_debito=None,
                        usuario_modificacion='ADMIN'):
        """Actualiza una nota de débito existente"""
        
        campos = []
        valores = []
        
        if motivo_nota_debito is not None:
            campos.append("motivo_nota_debito = %s")
            valores.append(motivo_nota_debito)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if est_nota_debito:
            campos.append("est_nota_debito = %s")
            valores.append(est_nota_debito)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_nota_debito)
        
        updateSQL = f"""
            UPDATE notas_debito
            SET {', '.join(campos)}
            WHERE id_nota_debito = %s
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
            app.logger.error(f"Error al actualizar nota de débito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def anularNotaDebito(self, id_nota_debito, motivo_anulacion, usuario='ADMIN'):
        """Anula una nota de débito"""
        return self.updateNotaDebito(
            id_nota_debito=id_nota_debito,
            observaciones=motivo_anulacion,
            est_nota_debito='ANULADA',
            usuario_modificacion=usuario
        )
    
    def getNotasDebitoPorFactura(self, id_factura):
        """Obtiene todas las notas de débito de una factura"""
        sql = """
            SELECT
                nd.id_nota_debito,
                nd.nota_debito_numero,
                nd.fecha_nota_debito,
                nd.monto_total,
                nd.est_nota_debito
            FROM notas_debito nd
            WHERE nd.id_factura = %s
            ORDER BY nd.fecha_nota_debito DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_factura,))
            notas = cur.fetchall()
            
            return [{
                'id_nota_debito': nota[0],
                'nota_debito_numero': nota[1],
                'fecha_nota_debito': nota[2].strftime('%d/%m/%Y %H:%M') if nota[2] else None,
                'monto_total': nota[3],
                'est_nota_debito': nota[4]
            } for nota in notas]
        except Exception as e:
            app.logger.error(f"Error al obtener notas de débito de la factura: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()


















