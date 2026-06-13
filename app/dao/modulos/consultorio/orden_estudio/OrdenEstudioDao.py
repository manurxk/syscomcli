from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date

class OrdenEstudioDao:
    """DAO para gestionar órdenes de estudios médicos"""
    
    def getAllOrdenesEstudios(self):
        """Obtiene todas las órdenes de estudios con sus datos completos"""
        ordenSQL = """
            SELECT
                o.id_orden_estudio,
                o.id_consulta,
                o.id_paciente,
                o.id_profesional,
                o.orden_numero,
                o.orden_fecha,
                o.orden_tipo,
                o.orden_estado,
                o.orden_observaciones,
                o.orden_indicaciones,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                o.fecha_creacion
            FROM ordenes_estudios o
            JOIN pacientes pac ON o.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON o.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE o.est_orden = 'A'
            ORDER BY o.orden_fecha DESC, o.id_orden_estudio DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(ordenSQL)
            ordenes = cur.fetchall()
            
            return [{
                'id_orden_estudio': ord[0],
                'id_consulta': ord[1],
                'id_paciente': ord[2],
                'id_profesional': ord[3],
                'orden_numero': ord[4],
                'orden_fecha': ord[5].strftime('%d/%m/%Y') if ord[5] else None,
                'orden_tipo': ord[6],
                'orden_estado': ord[7],
                'orden_observaciones': ord[8],
                'orden_indicaciones': ord[9],
                'historia_clinica': ord[10],
                'paciente_nombre': ord[11],
                'paciente_cedula': ord[12],
                'profesional_nombre': ord[13],
                'profesional_matricula': ord[14],
                'fecha_registro': ord[15].strftime('%d/%m/%Y') if ord[15] else None
            } for ord in ordenes]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las órdenes de estudios: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getOrdenEstudioById(self, id_orden_estudio):
        """Obtiene una orden de estudio específica por ID con su detalle"""
        ordenSQL = """
            SELECT
                o.id_orden_estudio,
                o.id_consulta,
                o.id_paciente,
                o.id_profesional,
                o.orden_numero,
                o.orden_fecha,
                o.orden_tipo,
                o.orden_estado,
                o.orden_observaciones,
                o.orden_indicaciones,
                o.est_orden,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pp.per_telefono AS paciente_telefono,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                o.fecha_creacion,
                o.usuario_creacion
            FROM ordenes_estudios o
            JOIN pacientes pac ON o.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON o.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE o.id_orden_estudio = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(ordenSQL, (id_orden_estudio,))
            ord = cur.fetchone()
            
            if not ord:
                return None
            
            return {
                'id_orden_estudio': ord[0],
                'id_consulta': ord[1],
                'id_paciente': ord[2],
                'id_profesional': ord[3],
                'orden_numero': ord[4],
                'orden_fecha': ord[5].strftime('%Y-%m-%d') if ord[5] else None,
                'orden_tipo': ord[6],
                'orden_estado': ord[7],
                'orden_observaciones': ord[8],
                'orden_indicaciones': ord[9],
                'activo': ord[10] == 'A',
                'historia_clinica': ord[11],
                'paciente_nombre': ord[12],
                'paciente_cedula': ord[13],
                'paciente_telefono': ord[14],
                'profesional_nombre': ord[15],
                'profesional_matricula': ord[16],
                'fecha_registro': ord[17].strftime('%Y-%m-%d') if ord[17] else None,
                'usuario_creacion': ord[18]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener orden de estudio por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getOrdenEstudioDetalle(self, id_orden_estudio):
        """Obtiene el detalle completo de una orden de estudio"""
        detalleSQL = """
            SELECT
                od.id_orden_detalle,
                od.id_orden_estudio,
                od.id_tipo_estudio,
                od.id_tipo_analisis,
                od.des_estudio,
                od.estudio_estado,
                od.estudio_resultado,
                od.estudio_fecha_realizacion,
                od.observaciones,
                te.des_tipo_estudio,
                ta.des_tipo_analisis
            FROM orden_estudio_detalle od
            LEFT JOIN tipos_estudios te ON od.id_tipo_estudio = te.id_tipo_estudio
            LEFT JOIN tipos_analisis ta ON od.id_tipo_analisis = ta.id_tipo_analisis
            WHERE od.id_orden_estudio = %s
            ORDER BY od.id_orden_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_orden_estudio,))
            detalles = cur.fetchall()
            
            return [{
                'id_orden_detalle': d[0],
                'id_orden_estudio': d[1],
                'id_tipo_estudio': d[2],
                'id_tipo_analisis': d[3],
                'des_estudio': d[4],
                'estudio_estado': d[5],
                'estudio_resultado': d[6],
                'estudio_fecha_realizacion': d[7].strftime('%Y-%m-%d') if d[7] else None,
                'observaciones': d[8],
                'tipo_estudio': d[9],
                'tipo_analisis': d[10]
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle de la orden de estudio: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def guardarOrdenEstudio(self, id_consulta, id_paciente, id_profesional,
                           orden_fecha, orden_tipo, orden_estado='PENDIENTE',
                           orden_observaciones=None, orden_indicaciones=None,
                           usuario_creacion='ADMIN'):
        """Guarda una nueva orden de estudio"""
        
        if not all([id_consulta, id_paciente, id_profesional, orden_fecha, orden_tipo]):
            app.logger.error("Faltan campos obligatorios para guardar orden de estudio")
            return None
        
        # Generar número de orden si no se proporciona
        orden_numero = self._generarNumeroOrden()
        
        insertOrdenSQL = """
            INSERT INTO ordenes_estudios(
                id_consulta, id_paciente, id_profesional, orden_numero,
                orden_fecha, orden_tipo, orden_estado,
                orden_observaciones, orden_indicaciones, est_orden, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s)
            RETURNING id_orden_estudio
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando orden de estudio para paciente ID: {id_paciente}")
            
            cur.execute(insertOrdenSQL, (
                id_consulta,
                id_paciente,
                id_profesional,
                orden_numero,
                orden_fecha,
                orden_tipo,
                orden_estado,
                orden_observaciones,
                orden_indicaciones,
                usuario_creacion
            ))
            
            orden_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Orden de estudio guardada exitosamente con ID: {orden_id}")
            return orden_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar orden de estudio: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarOrdenEstudioDetalle(self, id_orden_estudio, des_estudio,
                                  id_tipo_estudio=None, id_tipo_analisis=None,
                                  estudio_estado='PENDIENTE', estudio_resultado=None,
                                  estudio_fecha_realizacion=None, observaciones=None):
        """Guarda un estudio en el detalle de la orden"""
        
        insertDetalleSQL = """
            INSERT INTO orden_estudio_detalle(
                id_orden_estudio, id_tipo_estudio, id_tipo_analisis,
                des_estudio, estudio_estado, estudio_resultado,
                estudio_fecha_realizacion, observaciones
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_orden_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_orden_estudio,
                id_tipo_estudio,
                id_tipo_analisis,
                des_estudio,
                estudio_estado,
                estudio_resultado,
                estudio_fecha_realizacion,
                observaciones
            ))
            
            detalle_id = cur.fetchone()[0]
            con.commit()
            
            return detalle_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar detalle de orden de estudio: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroOrden(self):
        """Genera un número único de orden de estudio"""
        año_actual = date.today().year
        
        selectSQL = """
            SELECT MAX(CAST(SUBSTRING(orden_numero FROM '[0-9]+$') AS INTEGER))
            FROM ordenes_estudios
            WHERE orden_numero LIKE %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            patron = f'ORD-{año_actual}-%'
            cur.execute(selectSQL, (patron,))
            resultado = cur.fetchone()
            
            siguiente_numero = (resultado[0] or 0) + 1
            return f'ORD-{año_actual}-{str(siguiente_numero).zfill(4)}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de orden: {str(e)}")
            return f'ORD-{año_actual}-0001'
        finally:
            cur.close()
            con.close()
    
    def updateOrdenEstudio(self, id_orden_estudio, orden_estado=None,
                          orden_observaciones=None, orden_indicaciones=None,
                          usuario_modificacion='ADMIN'):
        """Actualiza una orden de estudio existente"""
        
        updateSQL = """
            UPDATE ordenes_estudios
            SET 
                orden_estado = COALESCE(%s, orden_estado),
                orden_observaciones = COALESCE(%s, orden_observaciones),
                orden_indicaciones = COALESCE(%s, orden_indicaciones),
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_orden_estudio = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, (
                orden_estado,
                orden_observaciones,
                orden_indicaciones,
                usuario_modificacion,
                id_orden_estudio
            ))
            
            con.commit()
            app.logger.info(f"Orden de estudio {id_orden_estudio} actualizada exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar orden de estudio: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteOrdenEstudio(self, id_orden_estudio):
        """Elimina lógicamente una orden de estudio"""
        deleteSQL = """
            UPDATE ordenes_estudios
            SET est_orden = 'I',
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id_orden_estudio = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_orden_estudio,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar orden de estudio: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()


















