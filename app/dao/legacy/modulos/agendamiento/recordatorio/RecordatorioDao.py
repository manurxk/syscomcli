from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, timedelta

class RecordatorioDao:
    """
    DAO simplificado para gestión de recordatorios de citas médicas con UltraMsg
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
    
    def cancelarRecordatoriosCita(self, id_cita):
        """
        Cancela (resetea) los recordatorios pendientes de una cita.
        Se usa cuando la cita es actualizada o cancelada.
        Solo resetea los recordatorios que todavía NO fueron enviados,
        preservando el historial de los que ya se enviaron.
        
        Args:
            id_cita: ID de la cita
            
        Returns:
            bool: True si se actualizó correctamente
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            updateSQL = """
                UPDATE recordatorios SET
                    recordatorio_24h_enviado = CASE WHEN recordatorio_24h_enviado = FALSE THEN FALSE ELSE recordatorio_24h_enviado END,
                    recordatorio_24h_fecha_programada = CASE WHEN recordatorio_24h_enviado = FALSE THEN NULL ELSE recordatorio_24h_fecha_programada END,
                    recordatorio_12h_enviado = CASE WHEN recordatorio_12h_enviado = FALSE THEN FALSE ELSE recordatorio_12h_enviado END,
                    recordatorio_12h_fecha_programada = CASE WHEN recordatorio_12h_enviado = FALSE THEN NULL ELSE recordatorio_12h_fecha_programada END,
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id_cita = %s
            """
            cur.execute(updateSQL, (id_cita,))
            con.commit()
            app.logger.info(f"✅ Recordatorios pendientes cancelados para cita {id_cita}")
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"❌ Error al cancelar recordatorios para cita {id_cita}: {str(e)}", exc_info=True)
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
            
        Returns:
            bool: True si se actualizó correctamente
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
            app.logger.info(f"✅ Recordatorio inmediato marcado como enviado para cita {id_cita} (Message ID: {message_id})")
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
        
        Args:
            id_cita: ID de la cita
            message_id: ID del mensaje de UltraMsg
            mensaje: Texto del mensaje enviado
            
        Returns:
            bool: True si se actualizó correctamente
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
            app.logger.info(f"✅ Recordatorio 24h marcado como enviado para cita {id_cita} (Message ID: {message_id})")
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
        
        Args:
            id_cita: ID de la cita
            message_id: ID del mensaje de UltraMsg
            mensaje: Texto del mensaje enviado
            
        Returns:
            bool: True si se actualizó correctamente
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
            app.logger.info(f"✅ Recordatorio 12h marcado como enviado para cita {id_cita} (Message ID: {message_id})")
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
        
        Args:
            limite: Máximo número de recordatorios a procesar
            
        Returns:
            list: Lista de diccionarios con datos de recordatorios pendientes
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
                    esp.des_especialidad,
                    pm.pam_tel_madre,
                    pm.pam_tel_padre,
                    CASE WHEN DATE_PART('year', AGE(pp.per_fecha_nacimiento)) < 18 THEN TRUE ELSE FALSE END AS es_menor
                FROM recordatorios r
                JOIN citas c ON r.id_cita = c.id_cita
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                JOIN personas pp ON p.id_persona = pp.id_persona
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                LEFT JOIN pacientes_menores pm ON p.id_paciente = pm.id_paciente
                WHERE r.recordatorio_24h_enviado = FALSE
                    AND r.recordatorio_24h_fecha_programada <= NOW()
                    AND c.cita_activo = TRUE
                ORDER BY r.recordatorio_24h_fecha_programada ASC
                LIMIT %s
            """
            cur.execute(selectSQL, (limite,))
            recordatorios = cur.fetchall()
            
            for r in recordatorios:
                es_menor = r[12]
                tel_tutor = r[10] or r[11] if es_menor else None
                
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
                    'especialidad': r[9],
                    'es_menor': es_menor,
                    'telefono_tutor': tel_tutor
                })
            
            app.logger.info(f"Se encontraron {len(resultado)} recordatorios 24h pendientes")
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
        
        Args:
            limite: Máximo número de recordatorios a procesar
            
        Returns:
            list: Lista de diccionarios con datos de recordatorios pendientes
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
                    esp.des_especialidad,
                    pm.pam_tel_madre,
                    pm.pam_tel_padre,
                    CASE WHEN DATE_PART('year', AGE(pp.per_fecha_nacimiento)) < 18 THEN TRUE ELSE FALSE END AS es_menor
                FROM recordatorios r
                JOIN citas c ON r.id_cita = c.id_cita
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                JOIN personas pp ON p.id_persona = pp.id_persona
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                LEFT JOIN pacientes_menores pm ON p.id_paciente = pm.id_paciente
                WHERE r.recordatorio_12h_enviado = FALSE
                    AND r.recordatorio_12h_fecha_programada <= NOW()
                    AND c.cita_activo = TRUE
                ORDER BY r.recordatorio_12h_fecha_programada ASC
                LIMIT %s
            """
            cur.execute(selectSQL, (limite,))
            recordatorios = cur.fetchall()
            
            for r in recordatorios:
                es_menor = r[12]
                tel_tutor = r[10] or r[11] if es_menor else None
                
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
                    'especialidad': r[9],
                    'es_menor': es_menor,
                    'telefono_tutor': tel_tutor
                })
            
            app.logger.info(f"Se encontraron {len(resultado)} recordatorios 12h pendientes")
            return resultado
        except Exception as e:
            app.logger.error(f"Error al obtener recordatorios 12h pendientes: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def getRecordatorioPorCita(self, id_cita):
        """
        Obtiene el recordatorio de una cita (una sola fila con todos los tipos)
        
        Args:
            id_cita: ID de la cita
            
        Returns:
            dict: Diccionario con todos los datos del recordatorio o None si no existe
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
                    recordatorio_inmediato_mensaje,
                    recordatorio_24h_enviado,
                    recordatorio_24h_fecha_programada,
                    recordatorio_24h_fecha_enviado,
                    recordatorio_24h_ultramsg_id,
                    recordatorio_24h_mensaje,
                    recordatorio_12h_enviado,
                    recordatorio_12h_fecha_programada,
                    recordatorio_12h_fecha_enviado,
                    recordatorio_12h_ultramsg_id,
                    recordatorio_12h_mensaje
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
                'cita_fecha': r[2].strftime('%Y-%m-%d') if r[2] else None,
                'cita_hora_inicio': r[3].strftime('%H:%M:%S') if r[3] else None,
                'telefono': r[4],
                'paciente_nombre': r[5],
                'inmediato_enviado': r[6],
                'inmediato_fecha_enviado': r[7].strftime('%Y-%m-%d %H:%M:%S') if r[7] else None,
                'inmediato_ultramsg_id': r[8],
                'inmediato_mensaje': r[9],
                '24h_enviado': r[10],
                '24h_fecha_programada': r[11].strftime('%Y-%m-%d %H:%M:%S') if r[11] else None,
                '24h_fecha_enviado': r[12].strftime('%Y-%m-%d %H:%M:%S') if r[12] else None,
                '24h_ultramsg_id': r[13],
                '24h_mensaje': r[14],
                '12h_enviado': r[15],
                '12h_fecha_programada': r[16].strftime('%Y-%m-%d %H:%M:%S') if r[16] else None,
                '12h_fecha_enviado': r[17].strftime('%Y-%m-%d %H:%M:%S') if r[17] else None,
                '12h_ultramsg_id': r[18],
                '12h_mensaje': r[19]
            }
        except Exception as e:
            app.logger.error(f"Error al obtener recordatorio por cita: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def getAllRecordatorios(self, estado=None, fecha_desde=None, fecha_hasta=None, 
                           id_cita=None, page=1, per_page=50, solo_enviados=False):
        """
        Obtiene listado de recordatorios con filtros opcionales
        
        Args:
            estado: Filtrar por tipo de recordatorio ('inmediato', '24h', '12h')
            fecha_desde: Fecha desde (opcional)
            fecha_hasta: Fecha hasta (opcional)
            id_cita: Filtrar por cita específica (opcional)
            page: Número de página
            per_page: Registros por página
            solo_enviados: Si True, solo muestra recordatorios que tengan al menos uno enviado
            
        Returns:
            tuple: (lista de recordatorios, total)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Construir query base
            selectSQL = """
                SELECT 
                    r.id_recordatorio,
                    r.id_cita,
                    r.recordatorio_cita_fecha,
                    r.recordatorio_cita_hora_inicio,
                    r.recordatorio_telefono,
                    r.recordatorio_paciente_nombre,
                    r.recordatorio_inmediato_enviado,
                    r.recordatorio_inmediato_fecha_enviado,
                    r.recordatorio_inmediato_ultramsg_id,
                    r.recordatorio_inmediato_mensaje,
                    r.recordatorio_24h_enviado,
                    r.recordatorio_24h_fecha_programada,
                    r.recordatorio_24h_fecha_enviado,
                    r.recordatorio_24h_ultramsg_id,
                    r.recordatorio_24h_mensaje,
                    r.recordatorio_12h_enviado,
                    r.recordatorio_12h_fecha_programada,
                    r.recordatorio_12h_fecha_enviado,
                    r.recordatorio_12h_ultramsg_id,
                    r.recordatorio_12h_mensaje,
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
                WHERE 1=1
            """
            
            params = []
            
            # Aplicar filtros
            if id_cita:
                selectSQL += " AND r.id_cita = %s"
                params.append(id_cita)
            
            if fecha_desde:
                selectSQL += " AND DATE(r.recordatorio_cita_fecha) >= %s"
                params.append(fecha_desde)
            
            if fecha_hasta:
                selectSQL += " AND DATE(r.recordatorio_cita_fecha) <= %s"
                params.append(fecha_hasta)
            
            # Filtro por estado (tipo de recordatorio)
            if estado == 'inmediato':
                selectSQL += " AND r.recordatorio_inmediato_enviado = TRUE"
            elif estado == '24h':
                selectSQL += " AND r.recordatorio_24h_enviado = TRUE"
            elif estado == '12h':
                selectSQL += " AND r.recordatorio_12h_enviado = TRUE"
            
            # Filtro para solo mostrar enviados
            if solo_enviados:
                selectSQL += " AND (r.recordatorio_inmediato_enviado = TRUE OR r.recordatorio_24h_enviado = TRUE OR r.recordatorio_12h_enviado = TRUE)"
            
            selectSQL += " ORDER BY r.recordatorio_cita_fecha DESC, r.recordatorio_cita_hora_inicio DESC"
            
            # Contar total
            countSQL = selectSQL.replace(
                "SELECT r.id_recordatorio, r.id_cita",
                "SELECT COUNT(*)"
            ).split("ORDER BY")[0]
            
            cur.execute(countSQL, params)
            total = cur.fetchone()[0]
            
            # Aplicar paginación
            offset = (page - 1) * per_page
            selectSQL += " LIMIT %s OFFSET %s"
            params.extend([per_page, offset])
            
            # Obtener datos
            cur.execute(selectSQL, params)
            recordatorios = cur.fetchall()
            
            resultado = []
            for r in recordatorios:
                resultado.append({
                    'id_recordatorio': r[0],
                    'id_cita': r[1],
                    'cita_fecha': r[2].strftime('%d/%m/%Y') if r[2] else None,
                    'cita_hora_inicio': r[3].strftime('%H:%M') if r[3] else None,
                    'telefono': r[4],
                    'paciente_nombre_cache': r[5],
                    'inmediato_enviado': r[6],
                    'inmediato_fecha_enviado': r[7].strftime('%Y-%m-%d %H:%M:%S') if r[7] else None,
                    'inmediato_ultramsg_id': r[8],
                    'inmediato_mensaje': r[9],
                    '24h_enviado': r[10],
                    '24h_fecha_programada': r[11].strftime('%Y-%m-%d %H:%M:%S') if r[11] else None,
                    '24h_fecha_enviado': r[12].strftime('%Y-%m-%d %H:%M:%S') if r[12] else None,
                    '24h_ultramsg_id': r[13],
                    '24h_mensaje': r[14],
                    '12h_enviado': r[15],
                    '12h_fecha_programada': r[16].strftime('%Y-%m-%d %H:%M:%S') if r[16] else None,
                    '12h_fecha_enviado': r[17].strftime('%Y-%m-%d %H:%M:%S') if r[17] else None,
                    '12h_ultramsg_id': r[18],
                    '12h_mensaje': r[19],
                    'paciente_nombre_completo': r[20],
                    'especialista_nombre': r[21],
                    'especialidad': r[22]
                })
            
            return resultado, total
            
        except Exception as e:
            app.logger.error(f"Error al obtener recordatorios: {str(e)}", exc_info=True)
            return [], 0
        finally:
            cur.close()
            con.close()
