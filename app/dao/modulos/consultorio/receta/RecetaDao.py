from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date

class RecetaDao:
    """DAO para gestionar recetas médicas"""
    
    def getRecetas(self):
        """Obtiene todas las recetas con sus datos completos"""
        recetaSQL = """
            SELECT
                r.id_receta,
                r.id_consulta,
                r.id_paciente,
                r.id_profesional,
                r.receta_numero,
                r.receta_fecha,
                r.receta_validez_dias,
                r.receta_observaciones,
                r.receta_indicaciones_generales,
                -- Datos del paciente
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                r.fecha_creacion
            FROM recetas r
            JOIN pacientes p ON r.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON r.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE r.est_receta = 'A'
            ORDER BY r.receta_fecha DESC, r.id_receta DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(recetaSQL)
            recetas = cur.fetchall()
            
            return [{
                'id_receta': rec[0],
                'id_consulta': rec[1],
                'id_paciente': rec[2],
                'id_profesional': rec[3],
                'receta_numero': rec[4],
                'receta_fecha': rec[5].strftime('%d/%m/%Y') if rec[5] else None,
                'receta_validez_dias': rec[6],
                'receta_observaciones': rec[7],
                'receta_indicaciones_generales': rec[8],
                'historia_clinica': rec[9],
                'paciente_nombre': rec[10],
                'paciente_cedula': rec[11],
                'profesional_nombre': rec[12],
                'profesional_matricula': rec[13],
                'fecha_registro': rec[14].strftime('%d/%m/%Y') if rec[14] else None
            } for rec in recetas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las recetas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getRecetaById(self, id_receta):
        """Obtiene una receta específica por ID"""
        recetaSQL = """
            SELECT
                r.id_receta,
                r.id_consulta,
                r.id_paciente,
                r.id_profesional,
                r.receta_numero,
                r.receta_fecha,
                r.receta_validez_dias,
                r.receta_observaciones,
                r.receta_indicaciones_generales,
                r.est_receta,
                -- Datos del paciente
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                r.fecha_creacion,
                r.usuario_creacion
            FROM recetas r
            JOIN pacientes p ON r.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON r.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE r.id_receta = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(recetaSQL, (id_receta,))
            rec = cur.fetchone()
            
            if not rec:
                return None
            
            return {
                'id_receta': rec[0],
                'id_consulta': rec[1],
                'id_paciente': rec[2],
                'id_profesional': rec[3],
                'receta_numero': rec[4],
                'receta_fecha': rec[5].strftime('%Y-%m-%d') if rec[5] else None,
                'receta_validez_dias': rec[6],
                'receta_observaciones': rec[7],
                'receta_indicaciones_generales': rec[8],
                'activo': rec[9] == 'A',
                'historia_clinica': rec[10],
                'paciente_nombre': rec[11],
                'paciente_cedula': rec[12],
                'profesional_nombre': rec[13],
                'profesional_matricula': rec[14],
                'fecha_registro': rec[15].strftime('%Y-%m-%d') if rec[15] else None,
                'usuario_creacion': rec[16]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener receta por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getRecetaDetalle(self, id_receta):
        """Obtiene el detalle completo de una receta (medicamentos)"""
        detalleSQL = """
            SELECT
                rd.id_receta_detalle,
                rd.id_receta,
                rd.id_medicamento,
                rd.medicamento_dosis,
                rd.medicamento_frecuencia,
                rd.medicamento_duracion,
                rd.medicamento_cantidad,
                rd.medicamento_indicaciones,
                rd.medicamento_posologia,
                m.des_medicamento,
                m.medicamento_concentracion
            FROM receta_detalle rd
            JOIN medicamentos m ON rd.id_medicamento = m.id_medicamento
            WHERE rd.id_receta = %s AND rd.est_receta_detalle = 'A'
            ORDER BY rd.id_receta_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_receta,))
            detalles = cur.fetchall()
            
            return [{
                'id_receta_detalle': d[0],
                'id_receta': d[1],
                'id_medicamento': d[2],
                'medicamento_dosis': d[3],
                'medicamento_frecuencia': d[4],
                'medicamento_duracion': d[5],
                'medicamento_cantidad': d[6],
                'medicamento_indicaciones': d[7],
                'medicamento_posologia': d[8],
                'medicamento_nombre': d[9],
                'medicamento_concentracion': d[10]
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle de receta: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def guardarReceta(self, id_consulta, id_paciente, id_profesional, receta_fecha,
                     receta_validez_dias=30, receta_indicaciones_generales=None,
                     receta_observaciones=None, usuario_creacion='ADMIN'):
        """Guarda una nueva receta"""
        
        if not all([id_consulta, id_paciente, id_profesional, receta_fecha]):
            app.logger.error("Faltan campos obligatorios para guardar receta")
            return None
        
        # Generar número de receta
        receta_numero = self._generarNumeroReceta()
        
        insertRecetaSQL = """
            INSERT INTO recetas(
                id_consulta, id_paciente, id_profesional, receta_numero,
                receta_fecha, receta_validez_dias, receta_indicaciones_generales,
                receta_observaciones, est_receta, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'A', %s)
            RETURNING id_receta
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando receta para paciente ID: {id_paciente}")
            
            cur.execute(insertRecetaSQL, (
                id_consulta,
                id_paciente,
                id_profesional,
                receta_numero,
                receta_fecha,
                receta_validez_dias,
                receta_indicaciones_generales,
                receta_observaciones,
                usuario_creacion
            ))
            
            receta_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Receta guardada exitosamente con ID: {receta_id}")
            return receta_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar receta: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarRecetaDetalle(self, id_receta, id_medicamento, medicamento_dosis,
                             medicamento_frecuencia, medicamento_duracion,
                             medicamento_cantidad=None, medicamento_indicaciones=None,
                             medicamento_posologia=None):
        """Guarda un medicamento en el detalle de la receta"""
        
        insertDetalleSQL = """
            INSERT INTO receta_detalle(
                id_receta, id_medicamento, medicamento_dosis,
                medicamento_frecuencia, medicamento_duracion, medicamento_cantidad,
                medicamento_indicaciones, medicamento_posologia, est_receta_detalle
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'A')
            RETURNING id_receta_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_receta,
                id_medicamento,
                medicamento_dosis,
                medicamento_frecuencia,
                medicamento_duracion,
                medicamento_cantidad,
                medicamento_indicaciones,
                medicamento_posologia
            ))
            
            detalle_id = cur.fetchone()[0]
            con.commit()
            
            return detalle_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar detalle de receta: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroReceta(self):
        """Genera un número único de receta"""
        año_actual = date.today().year
        
        selectSQL = """
            SELECT MAX(CAST(SUBSTRING(receta_numero FROM '[0-9]+$') AS INTEGER))
            FROM recetas
            WHERE receta_numero LIKE %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            patron = f'REC-{año_actual}-%'
            cur.execute(selectSQL, (patron,))
            resultado = cur.fetchone()
            
            siguiente_numero = (resultado[0] or 0) + 1
            return f'REC-{año_actual}-{str(siguiente_numero).zfill(4)}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de receta: {str(e)}")
            return f'REC-{año_actual}-0001'
        finally:
            cur.close()
            con.close()
    
    def updateReceta(self, id_receta, receta_observaciones=None,
                    receta_indicaciones_generales=None, usuario_modificacion='ADMIN'):
        """Actualiza una receta existente"""
        
        updateSQL = """
            UPDATE recetas
            SET 
                receta_observaciones = COALESCE(%s, receta_observaciones),
                receta_indicaciones_generales = COALESCE(%s, receta_indicaciones_generales),
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_receta = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, (
                receta_observaciones,
                receta_indicaciones_generales,
                usuario_modificacion,
                id_receta
            ))
            
            con.commit()
            return cur.rowcount > 0
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar receta: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteReceta(self, id_receta):
        """Elimina lógicamente una receta"""
        deleteSQL = """
            UPDATE recetas
            SET est_receta = 'I',
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id_receta = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_receta,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar receta: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def getRecetasPorPaciente(self, id_paciente):
        """Obtiene todas las recetas de un paciente"""
        recetaSQL = """
            SELECT
                r.id_receta,
                r.receta_numero,
                r.receta_fecha,
                r.receta_validez_dias,
                r.receta_indicaciones_generales
            FROM recetas r
            WHERE r.id_paciente = %s AND r.est_receta = 'A'
            ORDER BY r.receta_fecha DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(recetaSQL, (id_paciente,))
            recetas = cur.fetchall()
            
            return [{
                'id_receta': rec[0],
                'receta_numero': rec[1],
                'receta_fecha': rec[2].strftime('%d/%m/%Y') if rec[2] else None,
                'receta_validez_dias': rec[3],
                'receta_indicaciones_generales': rec[4]
            } for rec in recetas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener recetas del paciente: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()


















