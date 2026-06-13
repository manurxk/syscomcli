from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import date

class AgendaDao:
    
    def getAllAgendas(self):
        """Obtiene todas las agendas configuradas (activas e inactivas)"""
        agendaSQL = """
            SELECT
                ah.id_agenda_horario,
                ah.id_especialista,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_especialista,
                ah.id_especialidad,
                esp.des_especialidad,
                ah.id_consultorio,
                c.des_consultorio,
                ah.id_dia_semana,
                ds.des_dia_semana,
                ds.dia_orden,
                ah.agen_hora_inicio,
                ah.agen_hora_fin,
                ah.agen_duracion_turno,
                ah.agen_turno,
                ah.agen_cupos_totales,
                ah.agen_fecha_desde,
                ah.agen_fecha_hasta,
                ah.est_agenda,
                e.esp_color_agenda
            FROM agenda_horarios ah
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN especialidades esp ON ah.id_especialidad = esp.id_especialidad
            JOIN consultorios c ON ah.id_consultorio = c.id_consultorio
            JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
            ORDER BY ah.est_agenda DESC, p.per_nombre, ds.dia_orden, ah.agen_hora_inicio
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(agendaSQL)
            agendas = cur.fetchall()
            
            return [{
                'id_agenda_horario': a[0],
                'id_especialista': a[1],
                'nombre_especialista': a[2],
                'id_especialidad': a[3],
                'especialidad': a[4],
                'id_consultorio': a[5],
                'consultorio': a[6],
                'id_dia_semana': a[7],
                'dia_semana': a[8],
                'dia_orden': a[9],
                'hora_inicio': a[10].strftime('%H:%M') if a[10] else None,
                'hora_fin': a[11].strftime('%H:%M') if a[11] else None,
                'duracion_turno': a[12],
                'turno': a[13],
                'cupos_totales': a[14],
                'fecha_desde': a[15].strftime('%d/%m/%Y') if a[15] else None,
                'fecha_hasta': a[16].strftime('%d/%m/%Y') if a[16] else None,
                'est_agenda_horario': a[17],  # Mantener nombre en respuesta para compatibilidad con frontend
                'color_agenda': a[18]
            } for a in agendas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las agendas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # ============================================
    # MÉTODOS PARA MODALES DE BÚSQUEDA
    # ============================================
    
    def getEspecialistas(self):
        """
        Obtiene lista de especialistas activos
        Endpoint: GET /api/v1/especialistas (mismo que citas)
        Estructura IDÉNTICA a CitaDao.getEspecialistas() para mantener consistencia
        Usa sintaxis PostgreSQL (|| en lugar de CONCAT)
        """
        especialistasSQL = """
            SELECT
                e.id_especialista,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                COALESCE(e.esp_matricula, '') AS esp_matricula,
                COALESCE(e.esp_color_agenda, '#3498db') AS esp_color_agenda
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            WHERE f.fun_estado = TRUE
            ORDER BY p.per_nombre, p.per_apellido
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(especialistasSQL)
            especialistas = cur.fetchall()
            
            app.logger.info(f"AgendaDao: Se encontraron {len(especialistas)} especialistas activos")
            
            # Estructura IDÉNTICA a CitaDao.getEspecialistas()
            return [{
                'id_especialista': e[0],
                'nombre_completo': e[1] if e[1] else 'Sin nombre',
                'matricula': e[2] if e[2] else '',
                'color_agenda': e[3] if e[3] else '#3498db'
            } for e in especialistas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener especialistas en AgendaDao: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def getDiasSemana(self):
        """
        Obtiene lista de días de la semana
        Endpoint: GET /api/v1/dias-semana
        """
        diasSQL = """
            SELECT
                id_dia_semana,
                des_dia_semana,
                dia_orden
            FROM dias_semana
            ORDER BY dia_orden
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(diasSQL)
            dias = cur.fetchall()
            
            return [{
                'id_dia_semana': d[0],
                'des_dia_semana': d[1],
                'dia_orden': d[2]
            } for d in dias]
            
        except Exception as e:
            app.logger.error(f"Error al obtener días de la semana: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getConsultorios(self):
        """
        Obtiene lista de consultorios
        Endpoint: GET /api/v1/consultorios
        """
        consultoriosSQL = """
            SELECT
                id_consultorio,
                des_consultorio,
                est_consultorio
            FROM consultorios
            ORDER BY des_consultorio
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(consultoriosSQL)
            consultorios = cur.fetchall()
            
            return [{
                'id_consultorio': c[0],
                'des_consultorio': c[1],
                'est_consultorio': c[2]
            } for c in consultorios]
            
        except Exception as e:
            app.logger.error(f"Error al obtener consultorios: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # ============================================
    # MÉTODOS CRUD COMPLETOS
    # ============================================
    
    def getAgendasByEspecialista(self, id_especialista):
        """Obtiene toda la agenda de un especialista específico
        Retorna estructura agrupada por día con turno_manana y turno_tarde
        INCLUYE agendas activas e inactivas para permitir activar/desactivar sin que desaparezcan"""
        agendaSQL = """
            SELECT
                ah.id_agenda_horario,
                ah.id_especialista,
                ah.id_especialidad,
                esp.des_especialidad,
                ah.id_consultorio,
                c.des_consultorio,
                ah.id_dia_semana,
                ds.des_dia_semana,
                ds.dia_orden,
                ah.agen_hora_inicio,
                ah.agen_hora_fin,
                ah.agen_duracion_turno,
                ah.agen_turno,
                ah.agen_cupos_totales,
                ah.agen_fecha_desde,
                ah.agen_fecha_hasta,
                ah.est_agenda
            FROM agenda_horarios ah
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            LEFT JOIN especialidades esp ON ah.id_especialidad = esp.id_especialidad
            JOIN consultorios c ON ah.id_consultorio = c.id_consultorio
            JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
            WHERE ah.id_especialista = %s
            ORDER BY ah.est_agenda DESC, ds.dia_orden, ah.agen_hora_inicio
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(agendaSQL, (id_especialista,))
            agendas = cur.fetchall()
            
            # Obtener todos los días de la semana
            diasSQL = "SELECT id_dia_semana, des_dia_semana, dia_orden FROM dias_semana ORDER BY dia_orden"
            cur.execute(diasSQL)
            dias = cur.fetchall()
            
            # Crear diccionario de días
            dias_dict = {}
            for dia in dias:
                dias_dict[dia[0]] = {
                    'id_dia_semana': dia[0],
                    'nombre_dia': dia[1],
                    'dia_orden': dia[2],
                    'turno_manana': None,
                    'turno_tarde': None
                }
            
            # Agrupar horarios por día y turno
            for a in agendas:
                id_dia = a[6]
                turno_raw = a[12] if a[12] else 'Mañana'
                # Normalizar turno: puede venir como 'Mañana', 'MAÑANA', 'Manana', etc.
                turno_normalizado = turno_raw.upper().replace('Ñ', 'N').replace('Á', 'A')
                
                turno_data = {
                    'id_agenda_horario': a[0],
                    'id_especialista': a[1],
                    'id_especialidad': a[2],
                    'especialidad': a[3],
                    'id_consultorio': a[4],
                    'consultorio': a[5],
                    'hora_inicio': a[9].strftime('%H:%M') if a[9] else None,
                    'hora_fin': a[10].strftime('%H:%M') if a[10] else None,
                    'duracion_turno': a[11],
                    'cupos_totales': a[13],
                    'cupos_disponibles': a[13],  # TODO: Calcular cupos disponibles reales por fecha
                    'fecha_desde': a[14].strftime('%d/%m/%Y') if a[14] else None,
                    'fecha_hasta': a[15].strftime('%d/%m/%Y') if a[15] else None,
                    'estado': a[16],  # est_agenda
                    'est_agenda_horario': a[16]  # Alias para compatibilidad con frontend
                }
                
                # Determinar si es mañana o tarde basándose en el turno o la hora
                es_manana = False
                if 'MANANA' in turno_normalizado or 'MAÑANA' in turno_normalizado.upper():
                    es_manana = True
                elif 'TARDE' in turno_normalizado:
                    es_manana = False
                else:
                    # Si no está claro, determinar por la hora
                    hora_inicio = a[9]
                    if hora_inicio:
                        hora_num = hora_inicio.hour if hasattr(hora_inicio, 'hour') else int(str(hora_inicio).split(':')[0])
                        es_manana = hora_num < 13
                    else:
                        es_manana = True  # Por defecto mañana
                
                # Si ya existe una agenda en este turno, priorizar la activa
                # Si ambas están activas o ambas inactivas, mantener la primera (ya ordenada por est_agenda DESC)
                turno_key = 'turno_manana' if es_manana else 'turno_tarde'
                if dias_dict[id_dia][turno_key] is None:
                    dias_dict[id_dia][turno_key] = turno_data
                else:
                    # Si la existente está inactiva y la nueva está activa, reemplazar
                    if not dias_dict[id_dia][turno_key]['estado'] and turno_data['estado']:
                        dias_dict[id_dia][turno_key] = turno_data
                    # Si ambas están activas o ambas inactivas, mantener la primera (ya ordenada)
            
            # Convertir a lista ordenada
            resultado = [dias_dict[dia_id] for dia_id in sorted(dias_dict.keys(), key=lambda x: dias_dict[x]['dia_orden'])]
            
            app.logger.info(f"AgendaDao: Retornando {len(resultado)} días con horarios para especialista {id_especialista}")
            return resultado
            
        except Exception as e:
            app.logger.error(f"Error al obtener agendas del especialista {id_especialista}: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()

    def getAgendaById(self, id_agenda_horario):
        """Obtiene una configuración de agenda específica por ID"""
        agendaSQL = """
            SELECT
                ah.id_agenda_horario,
                ah.id_especialista,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_especialista,
                ah.id_especialidad,
                esp.des_especialidad,
                ah.id_consultorio,
                c.des_consultorio,
                ah.id_dia_semana,
                ds.des_dia_semana,
                ah.agen_hora_inicio,
                ah.agen_hora_fin,
                ah.agen_duracion_turno,
                ah.agen_turno,
                ah.agen_cupos_totales,
                ah.agen_fecha_desde,
                ah.agen_fecha_hasta,
                ah.est_agenda,
                ah.creacion_fecha,
                ah.modificacion_fecha,
                e.esp_color_agenda
            FROM agenda_horarios ah
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN especialidades esp ON ah.id_especialidad = esp.id_especialidad
            JOIN consultorios c ON ah.id_consultorio = c.id_consultorio
            JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
            WHERE ah.id_agenda_horario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(agendaSQL, (id_agenda_horario,))
            a = cur.fetchone()
            
            if not a:
                return None
            
            return {
                'id_agenda_horario': a[0],
                'id_especialista': a[1],
                'nombre_especialista': a[2],
                'id_especialidad': a[3],
                'especialidad': a[4],
                'id_consultorio': a[5],
                'consultorio': a[6],
                'id_dia_semana': a[7],
                'dia_semana': a[8],
                'hora_inicio': a[9].strftime('%H:%M') if a[9] else None,
                'hora_fin': a[10].strftime('%H:%M') if a[10] else None,
                'duracion_turno': a[11],
                'turno': a[12],
                'cupos_totales': a[13],
                'fecha_desde': a[14].strftime('%d/%m/%Y') if a[14] else None,
                'fecha_hasta': a[15].strftime('%d/%m/%Y') if a[15] else None,
                'est_agenda_horario': a[16],
                'fecha_creacion': a[17].strftime('%d/%m/%Y') if a[17] else None,
                'fecha_modificacion': a[18].strftime('%d/%m/%Y') if a[18] else None,
                'color_agenda': a[19]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener agenda por ID {id_agenda_horario}: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getAgendaParaEditar(self, id_agenda_horario):
        """Obtiene agenda con IDs originales para edición"""
        agendaSQL = """
            SELECT
                ah.id_agenda_horario,
                ah.id_especialista,
                ah.id_especialidad,
                ah.id_consultorio,
                ah.id_dia_semana,
                ah.agen_hora_inicio,
                ah.agen_hora_fin,
                ah.agen_duracion_turno,
                ah.agen_turno,
                ah.agen_cupos_totales,
                ah.agen_fecha_desde,
                ah.agen_fecha_hasta,
                ah.est_agenda,
                esp.des_especialidad,
                c.des_consultorio,
                ds.des_dia_semana,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_especialista,
                e.esp_color_agenda
            FROM agenda_horarios ah
            LEFT JOIN especialidades esp ON ah.id_especialidad = esp.id_especialidad
            JOIN consultorios c ON ah.id_consultorio = c.id_consultorio
            JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            WHERE ah.id_agenda_horario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(agendaSQL, (id_agenda_horario,))
            a = cur.fetchone()
            
            if not a:
                return None
            
            return {
                'id_agenda_horario': a[0],
                'id_especialista': a[1],
                'id_especialidad': a[2],
                'id_consultorio': a[3],
                'id_dia_semana': a[4],
                'hora_inicio': a[5].strftime('%H:%M') if a[5] else None,
                'hora_fin': a[6].strftime('%H:%M') if a[6] else None,
                'duracion_turno': a[7],
                'turno': a[8],
                'cupos_totales': a[9],
                'fecha_desde': a[10].strftime('%Y-%m-%d') if a[10] else None,
                'fecha_hasta': a[11].strftime('%Y-%m-%d') if a[11] else None,
                'activo': a[12],
                # Descripciones para mostrar
                'especialidad': a[13],
                'consultorio': a[14],
                'dia_semana': a[15],
                'nombre_especialista': a[16],
                'color_agenda': a[17]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener agenda para editar: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getEspecialidadesByEspecialista(self, id_especialista):
        """Obtiene las especialidades asignadas a un especialista específico"""
        especialidadesSQL = """
            SELECT 
                e.id_especialidad,
                e.des_especialidad
            FROM especialidades e
            JOIN especialista_especialidades ee ON e.id_especialidad = ee.id_especialidad
            WHERE ee.id_especialista = %s
                AND e.est_especialidad = TRUE
            ORDER BY e.des_especialidad
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(especialidadesSQL, (id_especialista,))
            especialidades = cur.fetchall()
            
            return [{
                'id_especialidad': esp[0],
                'des_especialidad': esp[1]
            } for esp in especialidades]
            
        except Exception as e:
            app.logger.error(f"Error al obtener especialidades del especialista: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def validarDisponibilidadConsultorio(self, id_consultorio, id_dia_semana, hora_inicio, hora_fin, id_agenda_excluir=None):
        """Verifica que el consultorio esté disponible en el horario solicitado"""
        # Nota: Verificar el nombre exacto de la columna en la BD (puede ser 'est_agenda' o 'est_agenda_horario')
        validacionSQL = """
            SELECT COUNT(*) 
            FROM agenda_horarios
            WHERE id_consultorio = %s
                AND id_dia_semana = %s
                AND est_agenda = TRUE
                AND (
                    (agen_hora_inicio < %s AND agen_hora_fin > %s) OR
                    (agen_hora_inicio >= %s AND agen_hora_inicio < %s) OR
                    (agen_hora_fin > %s AND agen_hora_fin <= %s)
                )
        """
        
        params = [id_consultorio, id_dia_semana, hora_fin, hora_inicio, hora_inicio, hora_fin, hora_inicio, hora_fin]
        
        if id_agenda_excluir:
            validacionSQL += " AND id_agenda_horario != %s"
            params.append(id_agenda_excluir)
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(validacionSQL, params)
            count = cur.fetchone()[0]
            return count == 0
            
        except Exception as e:
            app.logger.error(f"Error al validar disponibilidad de consultorio: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def guardarAgenda(self, id_especialista, id_consultorio, id_dia_semana,
                      hora_inicio, hora_fin, duracion_turno, turno="Mañana", cupos_totales=10,
                      fecha_desde=None, fecha_hasta=None, creacion_usuario=1):
        """
        Guarda una nueva configuración de agenda - VERSIÓN CORREGIDA
        
        Nota: a partir del nuevo diseño, la agenda ya no obliga a elegir
        una especialidad. La especialidad se elige en el flujo de creación
        de la cita, por lo que este método solo define disponibilidad
        horaria del especialista en un consultorio y día.
        """
        
        if not self.validarDisponibilidadConsultorio(id_consultorio, id_dia_semana, hora_inicio, hora_fin):
            app.logger.error("El consultorio ya está ocupado en ese horario")
            return None
        
        insertAgendaSQL = """
            INSERT INTO agenda_horarios(
                id_especialista, id_consultorio, id_dia_semana,
                agen_hora_inicio, agen_hora_fin, agen_duracion_turno,
                agen_turno, agen_cupos_totales,
                agen_fecha_desde, agen_fecha_hasta, est_agenda, creacion_usuario
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_agenda_horario
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if not fecha_desde:
                fecha_desde = date.today()
            
            app.logger.info(f"Insertando agenda para especialista {id_especialista}")
            # Establecer est_agenda = TRUE por defecto para que los horarios sean visibles en citas
            cur.execute(insertAgendaSQL, (
                id_especialista, id_consultorio, id_dia_semana,
                hora_inicio, hora_fin, duracion_turno,
                turno, cupos_totales,
                fecha_desde, fecha_hasta, True, creacion_usuario
            ))
            
            agenda_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Agenda guardada exitosamente con ID: {agenda_id}")
            return agenda_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar agenda: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()

    def updateAgenda(self, id_agenda_horario, id_consultorio, id_dia_semana,
                     hora_inicio, hora_fin, duracion_turno, turno, cupos_totales,
                     fecha_desde, fecha_hasta, activo, modificacion_usuario=1):
        """Actualiza una configuración de agenda existente - VERSIÓN CORREGIDA"""
        
        if not self.validarDisponibilidadConsultorio(id_consultorio, id_dia_semana, 
                                                      hora_inicio, hora_fin, id_agenda_horario):
            app.logger.error("El consultorio ya está ocupado en ese horario")
            return False
        
        updateAgendaSQL = """
            UPDATE agenda_horarios
            SET id_consultorio = %s,
                id_dia_semana = %s,
                agen_hora_inicio = %s,
                agen_hora_fin = %s,
                agen_duracion_turno = %s,
                agen_turno = %s,
                agen_cupos_totales = %s,
                agen_fecha_desde = %s,
                agen_fecha_hasta = %s,
                est_agenda = %s,
                modificacion_fecha = CURRENT_DATE,
                modificacion_hora = CURRENT_TIME,
                modificacion_usuario = %s
            WHERE id_agenda_horario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateAgendaSQL, (
                id_consultorio, id_dia_semana,
                hora_inicio, hora_fin, duracion_turno,
                turno, cupos_totales,
                fecha_desde, fecha_hasta, activo,
                modificacion_usuario, id_agenda_horario
            ))
            
            con.commit()
            app.logger.info(f"Agenda {id_agenda_horario} actualizada exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar agenda: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    # ==========================================
    # ⭐ NUEVO MÉTODO: TOGGLE ESTADO
    # ==========================================
    def updateEstadoAgenda(self, id_agenda_horario, est_agenda_horario, modificacion_usuario=1):
        """
        Actualiza únicamente el estado (activo/inactivo) de una agenda.
        
        Args:
            id_agenda_horario (int): ID de la agenda a actualizar
            est_agenda_horario (bool): Nuevo estado (True=Activo, False=Inactivo)
            modificacion_usuario (int): ID del usuario que realiza la modificación
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        updateEstadoSQL = """
            UPDATE agenda_horarios
            SET est_agenda = %s,
                modificacion_fecha = CURRENT_DATE,
                modificacion_hora = CURRENT_TIME,
                modificacion_usuario = %s
            WHERE id_agenda_horario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateEstadoSQL, (
                est_agenda_horario,
                modificacion_usuario,
                id_agenda_horario
            ))
            
            if cur.rowcount == 0:
                app.logger.warning(f"No se encontró la agenda con ID {id_agenda_horario}")
                return False
            
            con.commit()
            estado_texto = 'activada' if est_agenda_horario else 'desactivada'
            app.logger.info(f"Agenda {id_agenda_horario} {estado_texto} exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar estado de agenda {id_agenda_horario}: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def deleteAgenda(self, id_agenda_horario):
        """Elimina FÍSICAMENTE una configuración de agenda"""
        deleteAgendaSQL = """
            DELETE FROM agenda_horarios
            WHERE id_agenda_horario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteAgendaSQL, (id_agenda_horario,))
            
            if cur.rowcount == 0:
                return False
            
            con.commit()
            app.logger.info(f"Agenda {id_agenda_horario} eliminada físicamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar agenda: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def getAgendaSemanalConsultorio(self, id_consultorio=None):
        """Obtiene una vista matriz semanal de uso de consultorios"""
        matrizSQL = """
            SELECT
                c.des_consultorio,
                ds.des_dia_semana,
                ds.dia_orden,
                ah.agen_turno,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS especialista,
                esp.des_especialidad,
                ah.agen_hora_inicio,
                ah.agen_hora_fin
            FROM agenda_horarios ah
            JOIN consultorios c ON ah.id_consultorio = c.id_consultorio
            JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN especialidades esp ON ah.id_especialidad = esp.id_especialidad
            WHERE ah.est_agenda = TRUE
        """
        
        params = []
        if id_consultorio:
            matrizSQL += " AND ah.id_consultorio = %s"
            params.append(id_consultorio)
        
        matrizSQL += " ORDER BY c.des_consultorio, ds.dia_orden, ah.agen_hora_inicio"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(matrizSQL, params if params else None)
            resultados = cur.fetchall()
            
            return [{
                'consultorio': r[0],
                'dia_semana': r[1],
                'dia_orden': r[2],
                'turno': r[3],
                'especialista': r[4],
                'especialidad': r[5],
                'hora_inicio': r[6].strftime('%H:%M') if r[6] else None,
                'hora_fin': r[7].strftime('%H:%M') if r[7] else None
            } for r in resultados]
            
        except Exception as e:
            app.logger.error(f"Error al obtener matriz semanal: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getEspecialistasConAgenda(self):
        """Obtiene lista de especialistas que tienen agenda configurada"""
        especialistasSQL = """
            SELECT DISTINCT
                e.id_especialista,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
                p.per_cedula,
                e.esp_matricula,
                COUNT(ah.id_agenda_horario) AS cantidad_horarios
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN agenda_horarios ah ON e.id_especialista = ah.id_especialista 
                AND ah.est_agenda = TRUE
            WHERE f.fun_estado = TRUE
            GROUP BY e.id_especialista, p.per_nombre, p.per_apellido, p.per_cedula, e.esp_matricula
            HAVING COUNT(ah.id_agenda_horario) > 0
            ORDER BY p.per_nombre
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(especialistasSQL)
            especialistas = cur.fetchall()
            
            return [{
                'id_especialista': e[0],
                'nombre_completo': e[1],
                'cedula': e[2],
                'matricula': e[3],
                'cantidad_horarios': e[4]
            } for e in especialistas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener especialistas con agenda: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # ==========================================
    # ⭐ NUEVO MÉTODO: TOGGLE ESTADO
    # ==========================================
    def updateEstadoAgenda(self, id_agenda_horario, est_agenda_horario, modificacion_usuario=1):
        """
        Actualiza únicamente el estado (activo/inactivo) de una agenda.
        
        Args:
            id_agenda_horario (int): ID de la agenda a actualizar
            est_agenda_horario (bool): Nuevo estado (True=Activo, False=Inactivo)
            modificacion_usuario (int): ID del usuario que realiza la modificación
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        updateEstadoSQL = """
            UPDATE agenda_horarios
            SET est_agenda = %s,
                modificacion_fecha = CURRENT_DATE,
                modificacion_hora = CURRENT_TIME,
                modificacion_usuario = %s
            WHERE id_agenda_horario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateEstadoSQL, (
                est_agenda_horario,
                modificacion_usuario,
                id_agenda_horario
            ))
            
            if cur.rowcount == 0:
                app.logger.warning(f"No se encontró la agenda con ID {id_agenda_horario}")
                return False
            
            con.commit()
            estado_texto = 'activada' if est_agenda_horario else 'desactivada'
            app.logger.info(f"Agenda {id_agenda_horario} {estado_texto} exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar estado de agenda {id_agenda_horario}: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()



        