from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, timedelta

class RecordatorioDaoNuevo:
    """
    DAO simplificado para gestión de recordatorios de citas médicas
    Nueva estructura: una fila por cita con columnas booleanas para cada tipo
    """
    
    def crearOActualizarRecordatorio(self, id_cita, cita_fecha, cita_hora_inicio,
                                     telefono=None, paciente_nombre=None,
                                     fecha_24h=None, fecha_12h=None,
                                     usuario_creacion=1):
        """
        Crea o actualiza el recordatorio de una cita (una sola fila)
        
        Args:
            id_cita: ID de la cita
            cita_fecha: Fecha de la cita (date)
            cita_hora_inicio: Hora de inicio de la cita (time)
            telefono: Teléfono del paciente (opcional)
            paciente_nombre: Nombre del paciente (opcional)
            fecha_24h: Fecha programada para recordatorio 24h (opcional)
            fecha_12h: Fecha programada para recordatorio 12h (opcional)
            usuario_creacion: ID del usuario
            
        Returns:
            bool: True si se creó/actualizó correctamente
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Verificar si ya existe
            cur.execute("SELECT id_recordatorio FROM recordatorios WHERE id_cita = %s", (id_cita,))
            existe = cur.fetchone()
            
            if existe:
                # Actualizar
                updateSQL = """
                    UPDATE recordatorios SET
                        recordatorio_cita_fecha = %s,
                        recordatorio_cita_hora_inicio = %s,
                        recordatorio_telefono = COALESCE(%s, recordatorio_telefono),
                        recordatorio_paciente_nombre = COALESCE(%s, recordatorio_paciente_nombre),
                        recordatorio_24h_fecha_programada = COALESCE(%s, recordatorio_24h_fecha_programada),
                        recordatorio_12h_fecha_programada = COALESCE(%s, recordatorio_12h_fecha_programada),
                        fecha_modificacion = CURRENT_TIMESTAMP
                    WHERE id_cita = %s
                """
                cur.execute(updateSQL, (
                    cita_fecha, cita_hora_inicio, telefono, paciente_nombre,
                    fecha_24h, fecha_12h, id_cita
                ))
            else:
                # Crear nuevo
                insertSQL = """
                    INSERT INTO recordatorios (
                        id_cita, recordatorio_cita_fecha, recordatorio_cita_hora_inicio,
                        recordatorio_telefono, recordatorio_paciente_nombre,
                        recordatorio_24h_fecha_programada, recordatorio_12h_fecha_programada,
                        usuario_creacion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(insertSQL, (
                    id_cita, cita_fecha, cita_hora_inicio,
                    telefono, paciente_nombre,
                    fecha_24h, fecha_12h,
                    usuario_creacion
                ))
            
            con.commit()
            app.logger.info(f"✅ Recordatorio creado/actualizado para cita {id_cita}")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"❌ Error al crear/actualizar recordatorio para cita {id_cita}: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def marcarInmediatoEnviado(self, id_cita, message_id, mensaje):
        """
        Marca el recordatorio inmediato como enviado
        
        Args:
            id_cita: ID de la cita
            message_id: ID del mensaje de UltraMsg
            mensaje: Texto del mensaje enviado
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            updateSQL = """
                UPDATE recordatorios SET
                    recordatorio_inmediato_enviado = TRUE,
                    recordatorio_inmediato_fecha_enviado = CURRENT_TIMESTAMP,
                    recordatorio_inmediato_ultramsg_id = %s,
                    recordatorio_inmediato_mensaje = %s,
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id_cita = %s
            """
            cur.execute(updateSQL, (message_id, mensaje, id_cita))
            con.commit()
            app.logger.info(f"✅ Recordatorio inmediato marcado como enviado para cita {id_cita}")
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"❌ Error al marcar inmediato como enviado: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def marcar24hEnviado(self, id_cita, message_id, mensaje):
        """
        Marca el recordatorio 24h como enviado
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            updateSQL = """
                UPDATE recordatorios SET
                    recordatorio_24h_enviado = TRUE,
                    recordatorio_24h_fecha_enviado = CURRENT_TIMESTAMP,
                    recordatorio_24h_ultramsg_id = %s,
                    recordatorio_24h_mensaje = %s,
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id_cita = %s
            """
            cur.execute(updateSQL, (message_id, mensaje, id_cita))
            con.commit()
            app.logger.info(f"✅ Recordatorio 24h marcado como enviado para cita {id_cita}")
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"❌ Error al marcar 24h como enviado: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def marcar12hEnviado(self, id_cita, message_id, mensaje):
        """
        Marca el recordatorio 12h como enviado
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            updateSQL = """
                UPDATE recordatorios SET
                    recordatorio_12h_enviado = TRUE,
                    recordatorio_12h_fecha_enviado = CURRENT_TIMESTAMP,
                    recordatorio_12h_ultramsg_id = %s,
                    recordatorio_12h_mensaje = %s,
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id_cita = %s
            """
            cur.execute(updateSQL, (message_id, mensaje, id_cita))
            con.commit()
            app.logger.info(f"✅ Recordatorio 12h marcado como enviado para cita {id_cita}")
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"❌ Error al marcar 12h como enviado: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def obtenerRecordatoriosPendientes24h(self, limite=100):
        """
        Obtiene citas con recordatorio 24h pendiente de enviar
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            selectSQL = """
                SELECT 
                    r.id_recordatorio,
                    r.id_cita,
                    r.recordatorio_cita_fecha,
                    r.recordatorio_cita_hora_inicio,
                    r.recordatorio_telefono,
                    r.recordatorio_paciente_nombre,
                    c.cita_motivo,
                    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre_completo,
                    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                    esp.des_especialidad
                FROM recordatorios r
                JOIN citas c ON r.id_cita = c.id_cita
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                JOIN personas pp ON p.id_persona = pp.id_persona
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                WHERE r.recordatorio_24h_enviado = FALSE
                    AND r.recordatorio_24h_fecha_programada <= NOW()
                    AND c.cita_activo = TRUE
                ORDER BY r.recordatorio_24h_fecha_programada ASC
                LIMIT %s
            """
            cur.execute(selectSQL, (limite,))
            recordatorios = cur.fetchall()
            
            resultado = []
            for r in recordatorios:
                resultado.append({
                    'id_recordatorio': r[0],
                    'id_cita': r[1],
                    'cita_fecha': r[2],
                    'cita_hora_inicio': r[3],
                    'telefono': r[4],
                    'paciente_nombre_cache': r[5],
                    'cita_motivo': r[6],
                    'paciente_nombre_completo': r[7],
                    'especialista_nombre': r[8],
                    'especialidad': r[9]
                })
            
            return resultado
        except Exception as e:
            app.logger.error(f"Error al obtener recordatorios 24h pendientes: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def obtenerRecordatoriosPendientes12h(self, limite=100):
        """
        Obtiene citas con recordatorio 12h pendiente de enviar
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            selectSQL = """
                SELECT 
                    r.id_recordatorio,
                    r.id_cita,
                    r.recordatorio_cita_fecha,
                    r.recordatorio_cita_hora_inicio,
                    r.recordatorio_telefono,
                    r.recordatorio_paciente_nombre,
                    c.cita_motivo,
                    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre_completo,
                    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                    esp.des_especialidad
                FROM recordatorios r
                JOIN citas c ON r.id_cita = c.id_cita
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                JOIN personas pp ON p.id_persona = pp.id_persona
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                WHERE r.recordatorio_12h_enviado = FALSE
                    AND r.recordatorio_12h_fecha_programada <= NOW()
                    AND c.cita_activo = TRUE
                ORDER BY r.recordatorio_12h_fecha_programada ASC
                LIMIT %s
            """
            cur.execute(selectSQL, (limite,))
            recordatorios = cur.fetchall()
            
            resultado = []
            for r in recordatorios:
                resultado.append({
                    'id_recordatorio': r[0],
                    'id_cita': r[1],
                    'cita_fecha': r[2],
                    'cita_hora_inicio': r[3],
                    'telefono': r[4],
                    'paciente_nombre_cache': r[5],
                    'cita_motivo': r[6],
                    'paciente_nombre_completo': r[7],
                    'especialista_nombre': r[8],
                    'especialidad': r[9]
                })
            
            return resultado
        except Exception as e:
            app.logger.error(f"Error al obtener recordatorios 12h pendientes: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def getRecordatorioPorCita(self, id_cita):
        """
        Obtiene el recordatorio de una cita (una sola fila)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            selectSQL = """
                SELECT 
                    id_recordatorio,
                    id_cita,
                    recordatorio_cita_fecha,
                    recordatorio_cita_hora_inicio,
                    recordatorio_telefono,
                    recordatorio_paciente_nombre,
                    recordatorio_inmediato_enviado,
                    recordatorio_inmediato_fecha_enviado,
                    recordatorio_inmediato_ultramsg_id,
                    recordatorio_24h_enviado,
                    recordatorio_24h_fecha_programada,
                    recordatorio_24h_fecha_enviado,
                    recordatorio_24h_ultramsg_id,
                    recordatorio_12h_enviado,
                    recordatorio_12h_fecha_programada,
                    recordatorio_12h_fecha_enviado,
                    recordatorio_12h_ultramsg_id
                FROM recordatorios
                WHERE id_cita = %s
            """
            cur.execute(selectSQL, (id_cita,))
            r = cur.fetchone()
            
            if not r:
                return None
            
            return {
                'id_recordatorio': r[0],
                'id_cita': r[1],
                'cita_fecha': r[2],
                'cita_hora_inicio': r[3],
                'telefono': r[4],
                'paciente_nombre': r[5],
                'inmediato_enviado': r[6],
                'inmediato_fecha_enviado': r[7].strftime('%Y-%m-%d %H:%M:%S') if r[7] else None,
                'inmediato_ultramsg_id': r[8],
                '24h_enviado': r[9],
                '24h_fecha_programada': r[10].strftime('%Y-%m-%d %H:%M:%S') if r[10] else None,
                '24h_fecha_enviado': r[11].strftime('%Y-%m-%d %H:%M:%S') if r[11] else None,
                '24h_ultramsg_id': r[12],
                '12h_enviado': r[13],
                '12h_fecha_programada': r[14].strftime('%Y-%m-%d %H:%M:%S') if r[14] else None,
                '12h_fecha_enviado': r[15].strftime('%Y-%m-%d %H:%M:%S') if r[15] else None,
                '12h_ultramsg_id': r[16]
            }
        except Exception as e:
            app.logger.error(f"Error al obtener recordatorio por cita: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()

