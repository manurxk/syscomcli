"""
DAO para gestionar derivaciones entre especialistas
"""
from flask import current_app as app, session
from app.conexion.Conexion import Conexion
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes
from datetime import datetime


class DerivacionDao:
    
    def crearDerivacion(self, id_paciente, id_especialista_origen, id_especialista_destino=None, 
                       motivo_derivacion=None, observaciones=None, urgencia='NORMAL', usuario_creacion=None,
                       es_externo=False, externo_nombre=None, externo_apellido=None, 
                       externo_telefono=None, externo_matricula=None):
        """
        Crea una nueva derivación usando la función PostgreSQL
        Soporta especialistas internos y externos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Usar función PostgreSQL para crear derivación y notificación
            # Nota: El orden de parámetros es: id_paciente, id_especialista_origen, motivo, 
            #       id_especialista_destino, observaciones, urgencia, es_externo, datos_externos
            app.logger.info(f"DEBUG DerivacionDao.crearDerivacion: Ejecutando función SQL con parámetros: id_paciente={id_paciente}, id_especialista_origen={id_especialista_origen}, motivo={motivo_derivacion[:50] if motivo_derivacion else None}, id_especialista_destino={id_especialista_destino}, es_externo={es_externo}")
            
            cur.execute("""
                SELECT crear_derivacion(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_paciente, id_especialista_origen, motivo_derivacion, id_especialista_destino,
                  observaciones, urgencia, es_externo, externo_nombre, externo_apellido, 
                  externo_telefono, externo_matricula))
            
            resultado = cur.fetchone()
            if not resultado:
                app.logger.error("DEBUG DerivacionDao.crearDerivacion: La función SQL no retornó ningún resultado")
                con.rollback()
                return None
            
            id_derivacion = resultado[0]
            con.commit()
            
            app.logger.info(f"DEBUG DerivacionDao.crearDerivacion: Derivación creada exitosamente: ID {id_derivacion}")
            
            # Verificar si se creó la notificación
            if not es_externo and id_especialista_destino:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM notificaciones 
                    WHERE id_derivacion = %s
                """, (id_derivacion,))
                count_notif = cur.fetchone()[0]
                app.logger.info(f"DEBUG DerivacionDao.crearDerivacion: Notificaciones creadas para derivación {id_derivacion}: {count_notif}")
            
            return id_derivacion
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al crear derivación: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def getDerivaciones(self):
        """
        Obtiene todas las derivaciones.
        Si el usuario es especialista, filtra por sus derivaciones (enviadas o recibidas).
        Retorna también un campo 'tipo' que indica si es 'ENVIADA' o 'RECIBIDA'
        """
        id_especialista = None
        puede_ver_todos = puede_ver_todos_pacientes()
        
        if not puede_ver_todos:
            id_especialista = obtener_id_especialista_usuario()
        
        derivacionSQL = """
            SELECT
                d.id_derivacion,
                d.id_paciente,
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                d.id_especialista_origen,
                CONCAT(po.per_nombre, ' ', po.per_apellido) AS especialista_origen,
                d.id_especialista_destino,
                CASE 
                    WHEN d.es_externo = TRUE THEN 
                        CONCAT(d.especialista_externo_nombre, ' ', COALESCE(d.especialista_externo_apellido, '')) || ' (Externo)'
                    ELSE 
                        CONCAT(pd.per_nombre, ' ', pd.per_apellido)
                END AS especialista_destino,
                d.es_externo,
                d.especialista_externo_nombre,
                d.especialista_externo_apellido,
                d.especialista_externo_telefono,
                d.especialista_externo_matricula,
                d.motivo_derivacion,
                d.observaciones,
                d.urgencia,
                d.estado,
                d.fecha_derivacion,
                d.fecha_respuesta,
                d.fecha_aceptacion,
                d.motivo_rechazo,
                CASE 
                    WHEN %s IS NOT NULL AND d.id_especialista_origen = %s THEN 'ENVIADA'
                    WHEN %s IS NOT NULL AND d.id_especialista_destino = %s AND d.es_externo = FALSE THEN 'RECIBIDA'
                    ELSE NULL
                END AS tipo
            FROM derivaciones d
            JOIN pacientes p ON d.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas eo ON d.id_especialista_origen = eo.id_especialista
            JOIN funcionarios fo ON eo.id_funcionario = fo.id_funcionario
            JOIN personas po ON fo.id_persona = po.id_persona
            LEFT JOIN especialistas ed ON d.id_especialista_destino = ed.id_especialista
            LEFT JOIN funcionarios fd ON ed.id_funcionario = fd.id_funcionario
            LEFT JOIN personas pd ON fd.id_persona = pd.id_persona
            WHERE 1=1
        """
        
        if id_especialista:
            # Incluir derivaciones donde el especialista es origen O destino (incluyendo externas)
            # Para externas, verificamos si el especialista es el origen
            derivacionSQL += """
                AND (d.id_especialista_origen = %s OR 
                     (d.id_especialista_destino = %s AND d.es_externo = FALSE))
            """
        
        derivacionSQL += " ORDER BY d.fecha_derivacion DESC"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if id_especialista:
                # Pasar id_especialista 4 veces para el CASE y 2 veces para el WHERE
                cur.execute(derivacionSQL, (id_especialista, id_especialista, id_especialista, id_especialista, id_especialista, id_especialista))
            else:
                # Si no es especialista, pasar NULL para el CASE
                cur.execute(derivacionSQL, (None, None, None, None))
            
            derivaciones = cur.fetchall()
            
            app.logger.info(f"DEBUG DerivacionDao.getDerivaciones: Se encontraron {len(derivaciones)} derivaciones (id_especialista={id_especialista})")
            
            # Mapear los resultados correctamente según el nuevo orden del SELECT
            # Orden: id_derivacion, id_paciente, historia_clinica, paciente_nombre,
            #        id_especialista_origen, especialista_origen, id_especialista_destino,
            #        especialista_destino, es_externo, externo_nombre, externo_apellido,
            #        externo_telefono, externo_matricula, motivo_derivacion, observaciones,
            #        urgencia, estado, fecha_derivacion, fecha_respuesta, fecha_aceptacion, motivo_rechazo
            resultado = [{
                'id_derivacion': d[0],
                'id_paciente': d[1],
                'historia_clinica': d[2],
                'paciente_nombre': d[3],
                'id_especialista_origen': d[4],
                'especialista_origen': d[5],
                'id_especialista_destino': d[6],
                'especialista_destino': d[7],
                'es_externo': d[8],
                'externo_nombre': d[9],
                'externo_apellido': d[10],
                'externo_telefono': d[11],
                'externo_matricula': d[12],
                'motivo_derivacion': d[13],
                'observaciones': d[14],
                'urgencia': d[15],
                'estado': d[16],
                'fecha_derivacion': d[17].strftime('%d/%m/%Y %H:%M') if d[17] else None,
                'fecha_respuesta': d[18].strftime('%d/%m/%Y %H:%M') if d[18] else None,
                'fecha_aceptacion': d[19].strftime('%d/%m/%Y %H:%M') if d[19] else None,
                'motivo_rechazo': d[20],
                'tipo': d[21]  # ENVIADA, RECIBIDA, o NULL
            } for d in derivaciones]
            
            app.logger.info(f"DEBUG DerivacionDao.getDerivaciones: Retornando {len(resultado)} derivaciones mapeadas")
            return resultado
            
        except Exception as e:
            app.logger.error(f"Error al obtener derivaciones: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def getDerivacionesPendientes(self):
        """
        Obtiene derivaciones pendientes recibidas por el especialista logueado
        """
        id_especialista = obtener_id_especialista_usuario()
        
        app.logger.info(f"DEBUG DerivacionDao.getDerivacionesPendientes: id_especialista={id_especialista}")
        
        if not id_especialista:
            app.logger.warning("DEBUG DerivacionDao.getDerivacionesPendientes: No se encontró id_especialista, retornando lista vacía")
            return []
        
        derivacionSQL = """
            SELECT
                d.id_derivacion,
                d.id_paciente,
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                d.id_especialista_origen,
                CONCAT(po.per_nombre, ' ', po.per_apellido) AS especialista_origen,
                d.motivo_derivacion,
                d.observaciones,
                d.urgencia,
                d.fecha_derivacion,
                d.es_externo,
                d.especialista_externo_nombre,
                d.especialista_externo_apellido,
                d.especialista_externo_telefono
            FROM derivaciones d
            JOIN pacientes p ON d.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas eo ON d.id_especialista_origen = eo.id_especialista
            JOIN funcionarios fo ON eo.id_funcionario = fo.id_funcionario
            JOIN personas po ON fo.id_persona = po.id_persona
            WHERE d.id_especialista_destino = %s
                AND d.estado = 'PENDIENTE'
                AND d.es_externo = FALSE
            ORDER BY 
                CASE d.urgencia
                    WHEN 'URGENTE' THEN 1
                    WHEN 'ALTA' THEN 2
                    WHEN 'NORMAL' THEN 3
                    WHEN 'BAJA' THEN 4
                END,
                d.fecha_derivacion DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"DEBUG DerivacionDao.getDerivacionesPendientes: Ejecutando query con id_especialista={id_especialista}")
            cur.execute(derivacionSQL, (id_especialista,))
            derivaciones = cur.fetchall()
            
            app.logger.info(f"DEBUG DerivacionDao.getDerivacionesPendientes: Se encontraron {len(derivaciones)} derivaciones pendientes")
            
            return [{
                'id_derivacion': d[0],
                'id_paciente': d[1],
                'historia_clinica': d[2],
                'paciente_nombre': d[3],
                'id_especialista_origen': d[4],
                'especialista_origen': d[5],
                'motivo_derivacion': d[6],
                'observaciones': d[7],
                'urgencia': d[8],
                'fecha_derivacion': d[9].strftime('%d/%m/%Y %H:%M') if d[9] else None,
                'es_externo': d[10],
                'externo_nombre': d[11],
                'externo_apellido': d[12],
                'externo_telefono': d[13]
            } for d in derivaciones]
            
        except Exception as e:
            app.logger.error(f"Error al obtener derivaciones pendientes: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def getDerivacionById(self, id_derivacion):
        """
        Obtiene una derivación específica por ID
        """
        derivacionSQL = """
            SELECT
                d.id_derivacion,
                d.id_paciente,
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                d.id_especialista_origen,
                CONCAT(po.per_nombre, ' ', po.per_apellido) AS especialista_origen,
                d.id_especialista_destino,
                CASE 
                    WHEN d.es_externo = TRUE THEN 
                        CONCAT(d.especialista_externo_nombre, ' ', COALESCE(d.especialista_externo_apellido, '')) || ' (Externo)'
                    ELSE 
                        CONCAT(pd.per_nombre, ' ', pd.per_apellido)
                END AS especialista_destino,
                d.es_externo,
                d.especialista_externo_nombre,
                d.especialista_externo_apellido,
                d.especialista_externo_telefono,
                d.especialista_externo_matricula,
                d.motivo_derivacion,
                d.observaciones,
                d.urgencia,
                d.estado,
                d.fecha_derivacion,
                d.fecha_respuesta,
                d.fecha_aceptacion,
                d.motivo_rechazo,
                d.usuario_creacion,
                d.fecha_creacion
            FROM derivaciones d
            JOIN pacientes p ON d.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas eo ON d.id_especialista_origen = eo.id_especialista
            JOIN funcionarios fo ON eo.id_funcionario = fo.id_funcionario
            JOIN personas po ON fo.id_persona = po.id_persona
            LEFT JOIN especialistas ed ON d.id_especialista_destino = ed.id_especialista
            LEFT JOIN funcionarios fd ON ed.id_funcionario = fd.id_funcionario
            LEFT JOIN personas pd ON fd.id_persona = pd.id_persona
            WHERE d.id_derivacion = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(derivacionSQL, (id_derivacion,))
            d = cur.fetchone()
            
            if not d:
                return None
            
            return {
                'id_derivacion': d[0],
                'id_paciente': d[1],
                'historia_clinica': d[2],
                'paciente_nombre': d[3],
                'id_especialista_origen': d[4],
                'especialista_origen': d[5],
                'id_especialista_destino': d[6],
                'especialista_destino': d[7],
                'es_externo': d[8],
                'externo_nombre': d[9],
                'externo_apellido': d[10],
                'externo_telefono': d[11],
                'externo_matricula': d[12],
                'motivo_derivacion': d[13],
                'observaciones': d[14],
                'urgencia': d[15],
                'estado': d[16],
                'fecha_derivacion': d[17].strftime('%d/%m/%Y %H:%M') if d[17] else None,
                'fecha_respuesta': d[18].strftime('%d/%m/%Y %H:%M') if d[18] else None,
                'fecha_aceptacion': d[19].strftime('%d/%m/%Y %H:%M') if d[19] else None,
                'motivo_rechazo': d[20],
                'usuario_creacion': d[21],
                'fecha_creacion': d[22].strftime('%d/%m/%Y %H:%M') if d[22] else None
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener derivación por ID: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def aceptarDerivacion(self, id_derivacion, id_usuario):
        """
        Acepta una derivación usando la función PostgreSQL
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("""
                SELECT aceptar_derivacion(%s, %s)
            """, (id_derivacion, id_usuario))
            
            resultado = cur.fetchone()[0]
            con.commit()
            
            if resultado:
                app.logger.info(f"Derivación {id_derivacion} aceptada exitosamente")
                return True
            else:
                app.logger.warning(f"No se pudo aceptar la derivación {id_derivacion}")
                return False
                
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al aceptar derivación: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def rechazarDerivacion(self, id_derivacion, id_usuario, motivo_rechazo):
        """
        Rechaza una derivación usando la función PostgreSQL
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("""
                SELECT rechazar_derivacion(%s, %s, %s)
            """, (id_derivacion, id_usuario, motivo_rechazo))
            
            resultado = cur.fetchone()[0]
            con.commit()
            
            if resultado:
                app.logger.info(f"Derivación {id_derivacion} rechazada exitosamente")
                return True
            else:
                app.logger.warning(f"No se pudo rechazar la derivación {id_derivacion}")
                return False
                
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al rechazar derivación: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def cancelarDerivacion(self, id_derivacion, id_usuario):
        """
        Cancela una derivación (solo el especialista origen puede cancelar)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Verificar que el usuario es el especialista origen
            cur.execute("""
                SELECT id_especialista_origen 
                FROM derivaciones 
                WHERE id_derivacion = %s AND estado = 'PENDIENTE'
            """, (id_derivacion,))
            
            resultado = cur.fetchone()
            if not resultado:
                return False
            
            id_especialista_origen = resultado[0]
            id_especialista_usuario = obtener_id_especialista_usuario()
            
            if id_especialista_usuario != id_especialista_origen:
                app.logger.warning(f"Usuario {id_usuario} no es el origen de la derivación {id_derivacion}")
                return False
            
            # Cancelar derivación
            cur.execute("""
                UPDATE derivaciones
                SET estado = 'CANCELADA',
                    fecha_respuesta = CURRENT_TIMESTAMP,
                    usuario_modificacion = (SELECT usu_nick FROM usuarios WHERE id_usuario = %s),
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id_derivacion = %s
            """, (id_usuario, id_derivacion))
            
            con.commit()
            app.logger.info(f"Derivación {id_derivacion} cancelada exitosamente")
            return True
                
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al cancelar derivación: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def getEspecialistasDisponibles(self, excluir_especialista=None):
        """
        Obtiene lista de especialistas disponibles para derivación.
        Excluye al especialista actual si se proporciona.
        """
        especialistasSQL = """
            SELECT
                e.id_especialista,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
                e.esp_matricula,
                e.esp_color_agenda
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            WHERE f.fun_estado = TRUE
        """
        
        if excluir_especialista:
            especialistasSQL += " AND e.id_especialista != %s"
        
        especialistasSQL += " ORDER BY p.per_nombre"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if excluir_especialista:
                app.logger.info(f"Obteniendo especialistas disponibles excluyendo: {excluir_especialista}")
                cur.execute(especialistasSQL, (excluir_especialista,))
            else:
                app.logger.info("Obteniendo todos los especialistas disponibles")
                cur.execute(especialistasSQL)
            
            especialistas = cur.fetchall()
            app.logger.info(f"Especialistas encontrados: {len(especialistas)}")
            
            resultado = [{
                'id_especialista': e[0],
                'nombre_completo': e[1],
                'matricula': e[2],
                'color_agenda': e[3]
            } for e in especialistas]
            
            app.logger.info(f"Especialistas disponibles retornados: {len(resultado)}")
            return resultado
            
        except Exception as e:
            app.logger.error(f"Error al obtener especialistas disponibles: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()

