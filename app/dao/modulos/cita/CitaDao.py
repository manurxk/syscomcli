from flask import current_app as app, session
from app.conexion.Conexion import Conexion
from datetime import datetime, date, timedelta
from app.dao.gestionar_personas.paciente.PacienteDao import PacienteDao
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes
    

class CitaDao:
    
    # =====================================================
    # MÉTODOS PARA MODALES DE BÚSQUEDA
    # =====================================================
    
    def getPacientes(self):
        """
        Obtiene lista de pacientes para el modal de búsqueda
        Endpoint: GET /api/v1/pacientes
        Si el usuario es especialista, solo devuelve sus pacientes asignados.
        """
        # Verificar si debe filtrar por especialista
        id_especialista = None
        puede_ver_todos = puede_ver_todos_pacientes()
        app.logger.info(f"DEBUG CitaDao.getPacientes: puede_ver_todos={puede_ver_todos}")
        
        if not puede_ver_todos:
            id_especialista = obtener_id_especialista_usuario()
            app.logger.info(f"DEBUG CitaDao.getPacientes: id_especialista={id_especialista}")
        
        # Construir query base
        pacientesSQL = """
            SELECT DISTINCT
                p.id_paciente,
                p.pac_historia_clinica,
                CONCAT(per.per_nombre, ' ', per.per_apellido) AS nombre_completo,
                per.per_cedula,
                per.per_telefono,
                per.per_fecha_nacimiento
            FROM pacientes p
            JOIN personas per ON p.id_persona = per.id_persona
        """
        
        # Agregar filtro por especialista si aplica
        if id_especialista:
            pacientesSQL += """
                INNER JOIN paciente_profesional pp ON p.id_paciente = pp.id_paciente
                WHERE pp.id_especialista = %s AND pp.activo = TRUE
            """
        else:
            # Para Admin/Recepcionista, no filtrar (o usar pac_estado si existe)
            pacientesSQL += " WHERE 1=1"
        
        pacientesSQL += " ORDER BY per.per_nombre"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if id_especialista:
                cur.execute(pacientesSQL, (id_especialista,))
            else:
                cur.execute(pacientesSQL)
            pacientes = cur.fetchall()
            
            return [{
                'id_paciente': p[0],
                'historia_clinica': p[1],
                'nombre_completo': p[2],
                'cedula': p[3],
                'telefono': p[4],
                'fecha_nacimiento': p[5].strftime('%d/%m/%Y') if p[5] else None
            } for p in pacientes]
            
        except Exception as e:
            app.logger.error(f"Error al obtener pacientes: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getEspecialistas(self, id_especialidad=None):
        """
        Obtiene lista de especialistas activos
        Si se proporciona id_especialidad, filtra solo los especialistas vinculados a esa especialidad
        Endpoint: GET /api/v1/especialistas?id_especialidad=X
        Usa sintaxis PostgreSQL compatible (|| en lugar de CONCAT)
        """
        if id_especialidad:
            especialistasSQL = """
                SELECT DISTINCT
                    e.id_especialista,
                    p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                    COALESCE(e.esp_matricula, '') AS esp_matricula,
                    COALESCE(e.esp_color_agenda, '#3498db') AS esp_color_agenda
                FROM especialistas e
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas p ON f.id_persona = p.id_persona
                JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista
                JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad
                WHERE f.fun_estado = TRUE
                  AND ee.id_especialidad = %s
                  AND esp.est_especialidad = TRUE
                ORDER BY nombre_completo
            """
        else:
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
            if id_especialidad:
                # Convertir a int para asegurar el tipo correcto
                id_especialidad = int(id_especialidad)
                app.logger.info(f"CitaDao: Filtrando especialistas por especialidad {id_especialidad} (tipo: {type(id_especialidad).__name__})")
                cur.execute(especialistasSQL, (id_especialidad,))
                app.logger.debug(f"CitaDao: SQL ejecutado con parámetro id_especialidad={id_especialidad}")
            else:
                app.logger.info("CitaDao: Obteniendo todos los especialistas (sin filtro)")
                cur.execute(especialistasSQL)
            
            especialistas = cur.fetchall()
            app.logger.info(f"CitaDao: Se encontraron {len(especialistas)} especialistas activos" + 
                          (f" para la especialidad {id_especialidad}" if id_especialidad else ""))
            
            # Si no se encontraron especialistas con filtro, hacer una consulta de diagnóstico
            if id_especialidad and len(especialistas) == 0:
                app.logger.warning(f"CitaDao: No se encontraron especialistas para especialidad {id_especialidad}")
                # Consulta de diagnóstico para verificar si la especialidad existe y tiene especialistas vinculados
                diagnosticoSQL = """
                    SELECT 
                        COUNT(*) as total_vinculos,
                        COUNT(DISTINCT ee.id_especialista) as especialistas_vinculados,
                        COUNT(DISTINCT CASE WHEN f.fun_estado = TRUE THEN ee.id_especialista END) as especialistas_activos
                    FROM especialista_especialidades ee
                    JOIN especialistas e ON ee.id_especialista = e.id_especialista
                    JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                    JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad
                    WHERE ee.id_especialidad = %s
                """
                cur.execute(diagnosticoSQL, (id_especialidad,))
                diagnostico = cur.fetchone()
                app.logger.info(f"CitaDao: Diagnóstico para especialidad {id_especialidad}: "
                              f"Total vínculos={diagnostico[0]}, "
                              f"Especialistas vinculados={diagnostico[1]}, "
                              f"Especialistas activos={diagnostico[2]}")
            
            return [{
                'id_especialista': e[0],
                'nombre_completo': e[1] if e[1] else 'Sin nombre',
                'matricula': e[2] if e[2] else '',
                'color_agenda': e[3] if e[3] else '#3498db'
            } for e in especialistas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener especialistas en CitaDao: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def getEspecialidades(self):
        """
        Obtiene lista de especialidades activas
        Endpoint: GET /api/v1/especialidades
        """
        especialidadesSQL = """
            SELECT
                id_especialidad,
                des_especialidad
            FROM especialidades
            WHERE est_especialidad = TRUE
            ORDER BY des_especialidad
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(especialidadesSQL)
            especialidades = cur.fetchall()
            
            return [{
                'id_especialidad': e[0],
                'des_especialidad': e[1]
            } for e in especialidades]
            
        except Exception as e:
            app.logger.error(f"Error al obtener especialidades: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getEstadosCitas(self):
        """
        Obtiene lista de estados de citas
        Endpoint: GET /api/v1/estados-citas
        """
        estadosSQL = """
            SELECT
                id_estado_cita,
                est_cita_nombre,
                est_cita_descripcion,
                est_cita_color
            FROM estados_citas
            WHERE est_cita_activo = TRUE
            ORDER BY id_estado_cita
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(estadosSQL)
            estados = cur.fetchall()
            
            return [{
                'id_estado_cita': e[0],
                'nombre': e[1],
                'descripcion': e[2],
                'color': e[3]
            } for e in estados]
            
        except Exception as e:
            app.logger.error(f"Error al obtener estados de citas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # =====================================================
    # CONSULTA DE CUPOS DISPONIBLES
    # =====================================================
    
    def getCuposDisponiblesPorEspecialidad(self, id_especialidad, fecha_inicio, fecha_fin):
        """
        Obtiene cupos disponibles para una especialidad en un rango de fechas
        Usa la función de PostgreSQL obtener_cupos_por_especialidad
        """
        # Convertir fechas a DATE explícitamente para evitar problemas de tipos
        cuposSQL = """
            SELECT * FROM obtener_cupos_por_especialidad(%s, %s::DATE, %s::DATE)
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(cuposSQL, (id_especialidad, fecha_inicio, fecha_fin))
            cupos = cur.fetchall()
            
            return [{
                'id_especialista': c[0],
                'especialista_nombre': c[1],
                'especialista_color': c[2],
                'dia_semana': c[3],
                'fecha_especifica': c[4].strftime('%Y-%m-%d') if c[4] else None,
                'hora_inicio': str(c[5]),
                'hora_fin': str(c[6]),
                'turno': c[7],
                'cupos_totales': c[8],
                'cupos_ocupados': c[9],
                'cupos_disponibles': c[10],
                'id_agenda_horario': c[11]
            } for c in cupos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener cupos por especialidad: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCuposDisponiblesPorEspecialista(self, id_especialista, fecha_inicio, fecha_fin):
        """
        Obtiene cupos disponibles para un especialista en un rango de fechas
        Usa la función de PostgreSQL obtener_cupos_por_especialista
        """
        # Convertir fechas a DATE explícitamente para evitar problemas de tipos
        cuposSQL = """
            SELECT * FROM obtener_cupos_por_especialista(%s, %s::DATE, %s::DATE)
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"CitaDao: Consultando cupos para especialista {id_especialista} desde {fecha_inicio} hasta {fecha_fin}")
            cur.execute(cuposSQL, (id_especialista, fecha_inicio, fecha_fin))
            cupos = cur.fetchall()
            
            app.logger.info(f"CitaDao: Se obtuvieron {len(cupos)} cupos de la función SQL")
            
            resultado = []
            for c in cupos:
                # La función ahora retorna 9 campos (agregado duracion_minutos)
                cupo = {
                    'dia_semana': c[0],
                    'fecha_especifica': c[1].strftime('%Y-%m-%d') if c[1] else None,
                    'hora_inicio': str(c[2]),
                    'hora_fin': str(c[3]),
                    'turno': c[4],
                    'cupos_totales': int(c[5]) if c[5] is not None else 0,
                    'cupos_ocupados': int(c[6]) if c[6] is not None else 0,
                    'cupos_disponibles': int(c[7]) if c[7] is not None else 0,
                    'id_agenda_horario': int(c[8]) if c[8] is not None else None,
                    'duracion_minutos': int(c[9]) if len(c) > 9 and c[9] is not None else 60
                }
                resultado.append(cupo)
                
                # Debug: Log detallado para cupos ocupados
                if cupo['cupos_disponibles'] <= 0 or cupo['cupos_ocupados'] > 0:
                    app.logger.debug(f"CitaDao: Cupo ocupado detectado - Fecha: {cupo['fecha_especifica']}, Hora: {cupo['hora_inicio']}, "
                                   f"Ocupados: {cupo['cupos_ocupados']}, Disponibles: {cupo['cupos_disponibles']}, Totales: {cupo['cupos_totales']}")
            
            # Debug: Log para cupos ocupados
            cuposOcupados = [c for c in resultado if c['cupos_disponibles'] <= 0]
            if cuposOcupados:
                app.logger.info(f"CitaDao: Se encontraron {len(cuposOcupados)} cupos ocupados de {len(resultado)} totales")
                app.logger.debug(f"CitaDao: Ejemplos de cupos ocupados: {cuposOcupados[:3]}")
            else:
                app.logger.warning(f"CitaDao: NO se encontraron cupos ocupados. Esto puede indicar un problema con la función SQL.")
            
            return resultado
            
        except Exception as e:
            app.logger.error(f"Error al obtener cupos por especialista: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # =====================================================
    # MÉTODOS CRUD COMPLETOS
    # =====================================================
    
    def getAllCitas(self):
        """
        Obtiene todas las citas activas CON id_profesional para consultas.
        Si el usuario es especialista, solo devuelve sus citas.
        """
        # Verificar si debe filtrar por especialista
        id_especialista = None
        puede_ver_todos = puede_ver_todos_pacientes()
        app.logger.info(f"DEBUG CitaDao.getAllCitas: puede_ver_todos={puede_ver_todos}")
        
        if not puede_ver_todos:
            id_especialista = obtener_id_especialista_usuario()
            app.logger.info(f"DEBUG CitaDao.getAllCitas: id_especialista={id_especialista}")
        
        citasSQL = """
            SELECT
                c.id_cita,
                c.id_paciente,
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_telefono,
                c.id_especialista,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                e.esp_color_agenda,
                c.id_especialidad,
                esp.des_especialidad,
                c.cita_fecha,
                c.cita_hora_inicio,
                c.cita_hora_fin,
                c.cita_es_primera_vez,
                c.cita_motivo,
                c.cita_observaciones,
                c.cita_numero_sesion,
                c.id_estado_cita,
                ec.est_cita_nombre,
                ec.est_cita_color,
                c.cita_fecha_confirmacion,
                c.cita_creacion_fecha
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_activo = TRUE
        """
        
        # Agregar filtro por especialista si aplica
        if id_especialista:
            citasSQL += " AND c.id_especialista = %s"
        
        citasSQL += " ORDER BY c.cita_fecha DESC, c.cita_hora_inicio DESC"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if id_especialista:
                cur.execute(citasSQL, (id_especialista,))
            else:
                cur.execute(citasSQL)
            citas = cur.fetchall()
            
            return [{
                'id_cita': c[0],
                'id_paciente': c[1],
                'historia_clinica': c[2],
                'paciente_nombre': c[3],
                'paciente_telefono': c[4],
                'id_profesional': c[5],  # ✅ IMPORTANTE: id_especialista mapeado como id_profesional
                'id_especialista': c[5],  # Mantener ambos por compatibilidad
                'especialista_nombre': c[6],
                'especialista_color': c[7],
                'id_especialidad': c[8],
                'especialidad': c[9],
                'cita_fecha': c[10].strftime('%d/%m/%Y') if c[10] else None,
                'cita_hora_inicio': c[11].strftime('%H:%M') if c[11] else None,
                'cita_hora_fin': c[12].strftime('%H:%M') if c[12] else None,
                'cita_tipo': 'PRIMERA_VEZ' if c[13] else 'SEGUIMIENTO',  # ✅ Convertir boolean a string
                'cita_motivo': c[14],
                'cita_observaciones': c[15],
                'cita_numero_sesion': c[16],
                'id_estado_cita': c[17],
                'estado_nombre': c[18],
                'estado_color': c[19],
                'fecha_confirmacion': c[20].strftime('%d/%m/%Y %H:%M') if c[20] else None,
                'fecha_creacion': c[21].strftime('%d/%m/%Y') if c[21] else None
            } for c in citas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las citas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCitaById(self, id_cita):
        """Obtiene una cita específica por ID"""
        citaSQL = """
            SELECT
                c.id_cita,
                c.id_paciente,
                c.id_especialista,
                c.id_especialidad,
                c.id_agenda_horario,
                c.cita_fecha,
                c.cita_hora_inicio,
                c.cita_hora_fin,
                c.cita_es_primera_vez,
                c.cita_motivo,
                c.cita_observaciones,
                c.cita_numero_sesion,
                c.id_estado_cita,
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                esp.des_especialidad,
                ec.est_cita_nombre,
                ec.est_cita_color,
                c.cita_fecha_confirmacion
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.id_cita = %s AND c.cita_activo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(citaSQL, (id_cita,))
            c = cur.fetchone()
            
            if not c:
                return None
            
            return {
                'id_cita': c[0],
                'id_paciente': c[1],
                'id_especialista': c[2],
                'id_especialidad': c[3],
                'id_agenda_horario': c[4],
                'cita_fecha': c[5].strftime('%Y-%m-%d') if c[5] else None,
                'cita_hora_inicio': c[6].strftime('%H:%M') if c[6] else None,
                'cita_hora_fin': c[7].strftime('%H:%M') if c[7] else None,
                'cita_tipo': 'PRIMERA_VEZ' if c[8] else 'SEGUIMIENTO',  # ✅ Convertir boolean a string
                'cita_motivo': c[9],
                'cita_observaciones': c[10],
                'cita_numero_sesion': c[11],
                'id_estado_cita': c[12],
                'historia_clinica': c[13],
                'paciente_nombre': c[14],
                'especialista_nombre': c[15],
                'especialidad': c[16],
                'estado_nombre': c[17],
                'estado_color': c[18],
                'fecha_confirmacion': c[19].strftime('%d/%m/%Y %H:%M') if c[19] else None
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener cita por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getCitaParaEditar(self, id_cita):
        """Obtiene cita con IDs originales para edición"""
        citaSQL = """
            SELECT
                c.id_cita,
                c.id_paciente,
                c.id_especialista,
                c.id_especialidad,
                c.id_agenda_horario,
                c.cita_fecha,
                c.cita_hora_inicio,
                c.cita_hora_fin,
                c.cita_es_primera_vez,
                c.cita_motivo,
                c.cita_observaciones,
                c.cita_numero_sesion,
                c.id_estado_cita,
                -- Descripciones para mostrar
                p.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                esp.des_especialidad,
                ec.est_cita_nombre
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.id_cita = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(citaSQL, (id_cita,))
            c = cur.fetchone()
            
            if not c:
                return None
            
            return {
                'id_cita': c[0],
                'id_paciente': c[1],
                'id_especialista': c[2],
                'id_especialidad': c[3],
                'id_agenda_horario': c[4],
                'cita_fecha': c[5].strftime('%Y-%m-%d') if c[5] else None,
                'cita_hora_inicio': c[6].strftime('%H:%M') if c[6] else None,
                'cita_hora_fin': c[7].strftime('%H:%M') if c[7] else None,
                'cita_tipo': 'PRIMERA_VEZ' if c[8] else 'SEGUIMIENTO',  # ✅ Convertir boolean a string
                'cita_motivo': c[9],
                'cita_observaciones': c[10],
                'cita_numero_sesion': c[11],
                'id_estado_cita': c[12],
                # Descripciones
                'historia_clinica': c[13],
                'paciente_nombre': c[14],
                'especialista_nombre': c[15],
                'especialidad': c[16],
                'estado_nombre': c[17]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener cita para editar: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()


    def registrarPacienteRapido(self, nombre, apellido, cedula, fecha_nacimiento):
        """
        Registro rápido de paciente desde módulo de citas
        Solo con datos básicos: nombre, apellido, cédula, fecha nacimiento
        """
        paciente_dao = PacienteDao()
        
        try:
            # Usar el método guardarPaciente existente con valores mínimos
            paciente_id = paciente_dao.guardarPaciente(
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                fecha_nacimiento=fecha_nacimiento,
                telefono=None,  # Opcional
                id_genero=None,
                id_estado_civil=None
            )
            
            if paciente_id:
                # Obtener datos completos del paciente recién creado
                paciente = paciente_dao.getPacienteById(paciente_id)
                return paciente
            
            return None
            
        except Exception as e:
            app.logger.error(f"Error en registro rápido de paciente: {str(e)}")
            return None


    def guardarCita(self, id_paciente, id_agenda_horario, id_especialista, id_especialidad,
                    cita_fecha, cita_hora_inicio, cita_hora_fin, cita_tipo, cita_motivo,
                    cita_creacion_usuario, id_estado_cita=1, cita_observaciones=None,
                    cita_numero_sesion=None):
        """Guarda una nueva cita"""
        
        # ✅ Convertir cita_tipo (string) a cita_es_primera_vez (boolean)
        # El frontend envía: 'PRIMERA_VEZ' o 'SEGUIMIENTO'
        # La BD espera: TRUE o FALSE
        cita_es_primera_vez = (cita_tipo == 'PRIMERA_VEZ' or cita_tipo == 'PRIMERA VEZ')
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # ✅ VALIDACIÓN: Verificar que la fecha de la cita coincida con el día de la semana de la agenda
            validarAgendaSQL = """
                SELECT 
                    ah.id_dia_semana,
                    ds.des_dia_semana,
                    CASE 
                        WHEN EXTRACT(DOW FROM %s::DATE) = 0 THEN 7
                        ELSE EXTRACT(DOW FROM %s::DATE)
                    END as dia_semana_cita
                FROM agenda_horarios ah
                JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
                WHERE ah.id_agenda_horario = %s
                    AND ah.est_agenda = TRUE
            """
            
            cur.execute(validarAgendaSQL, (cita_fecha, cita_fecha, id_agenda_horario))
            agenda_data = cur.fetchone()
            
            if not agenda_data:
                app.logger.error(f"Agenda horario {id_agenda_horario} no encontrada o inactiva")
                return None
            
            id_dia_semana_agenda = agenda_data[0]
            nombre_dia_agenda = agenda_data[1]
            dia_semana_cita = agenda_data[2]
            
            if id_dia_semana_agenda != dia_semana_cita:
                app.logger.warning(
                    f"Intento de crear cita en día que no coincide con la agenda. "
                    f"Agenda configurada para: {nombre_dia_agenda} (id={id_dia_semana_agenda}), "
                    f"Fecha de cita: {cita_fecha} (día={dia_semana_cita})"
                )
                # Retornar None para indicar error, el API manejará el mensaje
                return None
            
            # ✅ VALIDACIÓN: Verificar que la hora de inicio coincida con un bloque de la agenda
            validarHoraSQL = """
                SELECT COUNT(*) > 0
                FROM agenda_horarios ah
                CROSS JOIN LATERAL (
                    SELECT 
                        ((('2000-01-01'::DATE + ah.agen_hora_inicio)::TIMESTAMP + 
                          (n * (COALESCE(ah.agen_duracion_turno, 60) || ' minutes')::INTERVAL))::TIME) as hora_inicio_bloque
                    FROM generate_series(
                        0, 
                        CASE 
                            WHEN COALESCE(ah.agen_duracion_turno, 60) = 30 THEN (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 1800)::INTEGER - 1
                            WHEN COALESCE(ah.agen_duracion_turno, 60) = 45 THEN (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 2700)::INTEGER - 1
                            ELSE (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 3600)::INTEGER - 1
                        END
                    ) n
                    WHERE ((('2000-01-01'::DATE + ah.agen_hora_inicio)::TIMESTAMP + 
                            (n * (COALESCE(ah.agen_duracion_turno, 60) || ' minutes')::INTERVAL))::TIME) < ah.agen_hora_fin
                ) bloque
                WHERE ah.id_agenda_horario = %s
                    AND ah.est_agenda = TRUE
                    AND bloque.hora_inicio_bloque = %s::TIME
            """
            
            cur.execute(validarHoraSQL, (id_agenda_horario, cita_hora_inicio))
            hora_valida = cur.fetchone()[0]
            
            if not hora_valida:
                app.logger.warning(
                    f"La hora {cita_hora_inicio} no coincide con ningún bloque de la agenda {id_agenda_horario}"
                )
                return None
            
            # ✅ VALIDACIÓN: Verificar que no haya solapamiento con otra cita del mismo especialista
            validarSolapamientoEspecialistaSQL = """
                SELECT COUNT(*) 
                FROM citas
                WHERE id_especialista = %s
                    AND cita_fecha = %s
                    AND cita_activo = TRUE
                    AND id_estado_cita != (SELECT id_estado_cita FROM estados_citas WHERE est_cita_nombre = 'CANCELADA')
                    AND (
                        (cita_hora_inicio < %s AND cita_hora_fin > %s) OR
                        (cita_hora_inicio >= %s AND cita_hora_inicio < %s) OR
                        (cita_hora_fin > %s AND cita_hora_fin <= %s)
                    )
            """
            
            cur.execute(validarSolapamientoEspecialistaSQL, (
                id_especialista, cita_fecha,
                cita_hora_inicio, cita_hora_fin,  # Para el primer caso: solapamiento parcial
                cita_hora_inicio, cita_hora_fin,   # Para el segundo caso: inicio dentro del rango
                cita_hora_inicio, cita_hora_fin    # Para el tercer caso: fin dentro del rango
            ))
            solapamiento_especialista = cur.fetchone()[0]
            
            if solapamiento_especialista > 0:
                app.logger.warning(
                    f"Intento de crear cita con solapamiento para especialista {id_especialista} "
                    f"en fecha {cita_fecha} entre {cita_hora_inicio} y {cita_hora_fin}"
                )
                return None
            
            # ✅ VALIDACIÓN: Verificar que el paciente no tenga otra cita en el mismo horario
            validarSolapamientoPacienteSQL = """
                SELECT COUNT(*) 
                FROM citas
                WHERE id_paciente = %s
                    AND cita_fecha = %s
                    AND cita_activo = TRUE
                    AND id_estado_cita != (SELECT id_estado_cita FROM estados_citas WHERE est_cita_nombre = 'CANCELADA')
                    AND (
                        (cita_hora_inicio < %s AND cita_hora_fin > %s) OR
                        (cita_hora_inicio >= %s AND cita_hora_inicio < %s) OR
                        (cita_hora_fin > %s AND cita_hora_fin <= %s)
                    )
            """
            
            cur.execute(validarSolapamientoPacienteSQL, (
                id_paciente, cita_fecha,
                cita_hora_inicio, cita_hora_fin,  # Para el primer caso: solapamiento parcial
                cita_hora_inicio, cita_hora_fin,   # Para el segundo caso: inicio dentro del rango
                cita_hora_inicio, cita_hora_fin    # Para el tercer caso: fin dentro del rango
            ))
            solapamiento_paciente = cur.fetchone()[0]
            
            if solapamiento_paciente > 0:
                app.logger.warning(
                    f"Intento de crear cita con solapamiento para paciente {id_paciente} "
                    f"en fecha {cita_fecha} entre {cita_hora_inicio} y {cita_hora_fin}"
                )
                return None
            
            app.logger.info(f"Guardando cita tipo {cita_tipo} (es_primera_vez={cita_es_primera_vez}) para paciente ID: {id_paciente}")
            
            insertCitaSQL = """
                INSERT INTO citas(
                    id_paciente, id_agenda_horario, id_especialista, id_especialidad,
                    cita_fecha, cita_hora_inicio, cita_hora_fin, cita_es_primera_vez,
                    cita_motivo, cita_observaciones, cita_numero_sesion,
                    id_estado_cita, cita_creacion_usuario
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_cita
            """
            
            cur.execute(insertCitaSQL, (
                id_paciente, id_agenda_horario, id_especialista, id_especialidad,
                cita_fecha, cita_hora_inicio, cita_hora_fin, cita_es_primera_vez,
                cita_motivo, cita_observaciones, cita_numero_sesion,
                id_estado_cita, cita_creacion_usuario
            ))
            
            cita_id = cur.fetchone()[0]
            
            # ✅ CREAR RELACIÓN PACIENTE_PROFESIONAL si no existe
            # Esto asegura que el paciente aparezca en "Mis Pacientes" del especialista
            # Convertir usuario_creacion a string (VARCHAR) si es necesario
            usuario_creacion_str = str(cita_creacion_usuario) if cita_creacion_usuario else 'SISTEMA'
            
            verificarRelacionSQL = """
                SELECT id_paciente_profesional, activo
                FROM paciente_profesional
                WHERE id_paciente = %s AND id_especialista = %s
                ORDER BY fecha_asignacion DESC
                LIMIT 1
            """
            cur.execute(verificarRelacionSQL, (id_paciente, id_especialista))
            relacion_existente = cur.fetchone()
            
            if relacion_existente:
                id_relacion, activo = relacion_existente
                if not activo:
                    # Si existe pero está inactiva, reactivarla
                    reactivarRelacionSQL = """
                        UPDATE paciente_profesional
                        SET activo = TRUE,
                            fecha_asignacion = CURRENT_TIMESTAMP,
                            fecha_finalizacion = NULL,
                            usuario_modificacion = %s,
                            fecha_modificacion = CURRENT_TIMESTAMP
                        WHERE id_paciente_profesional = %s
                    """
                    cur.execute(reactivarRelacionSQL, (usuario_creacion_str, id_relacion))
                    app.logger.info(f"Relación paciente_profesional reactivada (ID: {id_relacion}) para paciente {id_paciente} y especialista {id_especialista}")
                else:
                    app.logger.info(f"Relación paciente_profesional ya existe y está activa (ID: {id_relacion})")
            else:
                # Crear nueva relación
                insertRelacionSQL = """
                    INSERT INTO paciente_profesional (
                        id_paciente, id_especialista, tipo_relacion, 
                        fecha_asignacion, activo, usuario_creacion
                    )
                    VALUES (%s, %s, 'ASIGNADO', CURRENT_TIMESTAMP, TRUE, %s)
                    RETURNING id_paciente_profesional
                """
                cur.execute(insertRelacionSQL, (id_paciente, id_especialista, usuario_creacion_str))
                id_relacion = cur.fetchone()[0]
                app.logger.info(f"Nueva relación paciente_profesional creada (ID: {id_relacion}) para paciente {id_paciente} y especialista {id_especialista}")
            
            con.commit()
            
            app.logger.info(f"Cita guardada exitosamente con ID: {cita_id}")
            
            # ✅ CREAR RECORDATORIOS AUTOMÁTICOS
            try:
                self.crearRecordatoriosParaCita(cita_id, cita_fecha, cita_hora_inicio, cita_creacion_usuario)
            except Exception as e:
                # No fallar la creación de la cita si falla la creación de recordatorios
                app.logger.warning(f"Error al crear recordatorios para cita {cita_id}: {str(e)}")
            
            return cita_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar cita: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def updateCita(self, id_cita, cita_fecha, cita_hora_inicio, cita_hora_fin,
                   cita_tipo, cita_motivo, cita_observaciones, cita_numero_sesion,
                   id_estado_cita, modificacion_usuario=1):
        """Actualiza una cita existente"""
        
        # ✅ Convertir cita_tipo (string) a cita_es_primera_vez (boolean)
        cita_es_primera_vez = (cita_tipo == 'PRIMERA_VEZ' or cita_tipo == 'PRIMERA VEZ')
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Obtener datos de la cita actual para validaciones
            obtenerCitaSQL = """
                SELECT id_especialista, id_paciente
                FROM citas
                WHERE id_cita = %s
            """
            cur.execute(obtenerCitaSQL, (id_cita,))
            cita_actual = cur.fetchone()
            
            if not cita_actual:
                app.logger.error(f"Cita {id_cita} no encontrada")
                return False
            
            id_especialista = cita_actual[0]
            id_paciente = cita_actual[1]
            
            # ✅ VALIDACIÓN: Verificar que no haya solapamiento con otra cita del mismo especialista
            validarSolapamientoEspecialistaSQL = """
                SELECT COUNT(*) 
                FROM citas
                WHERE id_especialista = %s
                    AND cita_fecha = %s
                    AND cita_activo = TRUE
                    AND id_cita != %s
                    AND id_estado_cita != (SELECT id_estado_cita FROM estados_citas WHERE est_cita_nombre = 'CANCELADA')
                    AND (
                        (cita_hora_inicio < %s AND cita_hora_fin > %s) OR
                        (cita_hora_inicio >= %s AND cita_hora_inicio < %s) OR
                        (cita_hora_fin > %s AND cita_hora_fin <= %s)
                    )
            """
            
            cur.execute(validarSolapamientoEspecialistaSQL, (
                id_especialista, cita_fecha, id_cita,
                cita_hora_inicio, cita_hora_fin,  # Para el primer caso: solapamiento parcial
                cita_hora_inicio, cita_hora_fin,   # Para el segundo caso: inicio dentro del rango
                cita_hora_inicio, cita_hora_fin    # Para el tercer caso: fin dentro del rango
            ))
            solapamiento_especialista = cur.fetchone()[0]
            
            if solapamiento_especialista > 0:
                app.logger.warning(
                    f"Intento de actualizar cita {id_cita} con solapamiento para especialista {id_especialista} "
                    f"en fecha {cita_fecha} entre {cita_hora_inicio} y {cita_hora_fin}"
                )
                return False
            
            # ✅ VALIDACIÓN: Verificar que el paciente no tenga otra cita en el mismo horario
            validarSolapamientoPacienteSQL = """
                SELECT COUNT(*) 
                FROM citas
                WHERE id_paciente = %s
                    AND cita_fecha = %s
                    AND cita_activo = TRUE
                    AND id_cita != %s
                    AND id_estado_cita != (SELECT id_estado_cita FROM estados_citas WHERE est_cita_nombre = 'CANCELADA')
                    AND (
                        (cita_hora_inicio < %s AND cita_hora_fin > %s) OR
                        (cita_hora_inicio >= %s AND cita_hora_inicio < %s) OR
                        (cita_hora_fin > %s AND cita_hora_fin <= %s)
                    )
            """
            
            cur.execute(validarSolapamientoPacienteSQL, (
                id_paciente, cita_fecha, id_cita,
                cita_hora_inicio, cita_hora_fin,  # Para el primer caso: solapamiento parcial
                cita_hora_inicio, cita_hora_fin,   # Para el segundo caso: inicio dentro del rango
                cita_hora_inicio, cita_hora_fin    # Para el tercer caso: fin dentro del rango
            ))
            solapamiento_paciente = cur.fetchone()[0]
            
            if solapamiento_paciente > 0:
                app.logger.warning(
                    f"Intento de actualizar cita {id_cita} con solapamiento para paciente {id_paciente} "
                    f"en fecha {cita_fecha} entre {cita_hora_inicio} y {cita_hora_fin}"
                )
                return False
            
            updateCitaSQL = """
                UPDATE citas
                SET cita_fecha = %s,
                    cita_hora_inicio = %s,
                    cita_hora_fin = %s,
                    cita_es_primera_vez = %s,
                    cita_motivo = %s,
                    cita_observaciones = %s,
                    cita_numero_sesion = %s,
                    id_estado_cita = %s,
                    cita_modificacion_fecha = CURRENT_TIMESTAMP,
                    cita_modificacion_usuario = %s
                WHERE id_cita = %s
            """
            
            cur.execute(updateCitaSQL, (
                cita_fecha, cita_hora_inicio, cita_hora_fin,
                cita_es_primera_vez, cita_motivo, cita_observaciones, cita_numero_sesion,
                id_estado_cita, modificacion_usuario, id_cita
            ))
            
            con.commit()
            app.logger.info(f"Cita {id_cita} actualizada exitosamente")
            
            # ✅ ACTUALIZAR RECORDATORIOS (cancelar los antiguos y crear nuevos)
            try:
                # Obtener datos actualizados de la cita
                cita_actualizada = self.getCitaById(id_cita)
                if cita_actualizada:
                    # Cancelar recordatorios antiguos
                    from app.dao.modulos.recordatorio.RecordatorioDao import RecordatorioDao
                    recordatorio_dao = RecordatorioDao()
                    recordatorio_dao.cancelarRecordatoriosCita(id_cita)
                    
                    # Crear nuevos recordatorios con la fecha/hora actualizada
                    fecha_cita = datetime.strptime(cita_actualizada['cita_fecha'], '%Y-%m-%d').date()
                    hora_cita = datetime.strptime(cita_actualizada['cita_hora_inicio'], '%H:%M').time()
                    self.crearRecordatoriosParaCita(id_cita, fecha_cita, hora_cita, modificacion_usuario)
            except Exception as e:
                # No fallar la actualización si falla la actualización de recordatorios
                app.logger.warning(f"Error al actualizar recordatorios para cita {id_cita}: {str(e)}")
            
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar cita: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteCita(self, id_cita):
        """Elimina lógicamente una cita"""
        deleteCitaSQL = """
            UPDATE citas
            SET cita_activo = FALSE,
                cita_modificacion_fecha = CURRENT_TIMESTAMP
            WHERE id_cita = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteCitaSQL, (id_cita,))
            
            if cur.rowcount == 0:
                return False
            
            con.commit()
            app.logger.info(f"Cita {id_cita} eliminada exitosamente")
            
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar cita: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    # =====================================================
    # MÉTODOS DE CAMBIO DE ESTADO
    # =====================================================
    
    def cambiarEstadoCita(self, id_cita, id_estado_cita, usuario_id=1):
        """Cambia el estado de una cita"""
        updateSQL = """
            UPDATE citas
            SET id_estado_cita = %s,
                cita_modificacion_fecha = CURRENT_TIMESTAMP,
                cita_modificacion_usuario = %s
            WHERE id_cita = %s AND cita_activo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, (id_estado_cita, usuario_id, id_cita))
            con.commit()
            
            app.logger.info(f"Estado de cita {id_cita} cambiado a {id_estado_cita}")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al cambiar estado de cita: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def confirmarCita(self, id_cita, usuario_id=1):
        """Confirma una cita (estado CONFIRMADA)"""
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("SELECT id_estado_cita FROM estados_citas WHERE est_cita_nombre = 'CONFIRMADA'")
            estado = cur.fetchone()
            if estado:
                return self.cambiarEstadoCita(id_cita, estado[0], usuario_id)
            return False
        except Exception as e:
            app.logger.error(f"Error al confirmar cita: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def cancelarCita(self, id_cita, usuario_id=1):
        """Cancela una cita (estado CANCELADA)"""
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("SELECT id_estado_cita FROM estados_citas WHERE est_cita_nombre = 'CANCELADA'")
            estado = cur.fetchone()
            if estado:
                resultado = self.cambiarEstadoCita(id_cita, estado[0], usuario_id)
                
                # ✅ CANCELAR RECORDATORIOS PENDIENTES
                if resultado:
                    try:
                        from app.dao.modulos.recordatorio.RecordatorioDao import RecordatorioDao
                        recordatorio_dao = RecordatorioDao()
                        recordatorio_dao.cancelarRecordatoriosCita(id_cita)
                        app.logger.info(f"Recordatorios cancelados para cita {id_cita}")
                    except Exception as e:
                        app.logger.warning(f"Error al cancelar recordatorios para cita {id_cita}: {str(e)}")
                
                return resultado
            return False
        except Exception as e:
            app.logger.error(f"Error al cancelar cita: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    # =====================================================
    # MÉTODOS DE RECORDATORIOS
    # =====================================================
    
    def crearRecordatoriosParaCita(self, id_cita, cita_fecha, cita_hora_inicio, usuario_creacion=1):
        """
        Crea recordatorios automáticos para una cita (24h y 12h antes)
        
        Args:
            id_cita: ID de la cita
            cita_fecha: Fecha de la cita (date)
            cita_hora_inicio: Hora de inicio de la cita (time o string 'HH:MM')
            usuario_creacion: ID del usuario que crea los recordatorios
            
        Returns:
            bool: True si se crearon correctamente, False en caso contrario
        """
        try:
            from app.dao.modulos.recordatorio.RecordatorioDao import RecordatorioDao
            recordatorio_dao = RecordatorioDao()
            
            # Obtener datos del paciente y cita para cache
            cita_data = self.getCitaById(id_cita)
            if not cita_data:
                app.logger.warning(f"No se pudo obtener datos de la cita {id_cita} para crear recordatorios")
                return False
            
            # Obtener teléfono del paciente
            paciente_dao = PacienteDao()
            paciente = paciente_dao.getPacienteById(cita_data['id_paciente'])
            
            if not paciente:
                app.logger.warning(f"No se pudo obtener datos del paciente {cita_data['id_paciente']} para crear recordatorios")
                return False
            
            telefono = paciente.get('telefono')
            # Si el teléfono es 'Sin teléfono' o None, usar None
            if telefono == 'Sin teléfono' or not telefono:
                telefono = None
            
            paciente_nombre = cita_data.get('paciente_nombre') or paciente.get('nombre_completo') or 'Paciente'
            
            app.logger.info(f"Creando recordatorios para cita {id_cita} - Paciente: {paciente_nombre}, Teléfono: {telefono or 'No disponible'}")
            
            # Crear recordatorios aunque no tenga teléfono (se puede agregar después)
            # El sistema intentará enviar cuando haya teléfono disponible
            
            # Calcular fechas de envío
            # Combinar fecha y hora para crear datetime
            if isinstance(cita_fecha, date):
                if isinstance(cita_hora_inicio, str):
                    # Manejar diferentes formatos de hora
                    if ':' in cita_hora_inicio:
                        try:
                            hora_time = datetime.strptime(cita_hora_inicio, '%H:%M:%S').time()
                        except:
                            hora_time = datetime.strptime(cita_hora_inicio, '%H:%M').time()
                    else:
                        hora_time = datetime.strptime(cita_hora_inicio, '%H:%M').time()
                else:
                    hora_time = cita_hora_inicio
                cita_datetime = datetime.combine(cita_fecha, hora_time)
            elif isinstance(cita_fecha, datetime):
                cita_datetime = cita_fecha
            elif isinstance(cita_fecha, str):
                # Si es string, parsearlo
                try:
                    cita_datetime = datetime.strptime(cita_fecha, '%Y-%m-%d')
                    if isinstance(cita_hora_inicio, str):
                        if ':' in cita_hora_inicio:
                            try:
                                hora_time = datetime.strptime(cita_hora_inicio, '%H:%M:%S').time()
                            except:
                                hora_time = datetime.strptime(cita_hora_inicio, '%H:%M').time()
                        else:
                            hora_time = datetime.strptime(cita_hora_inicio, '%H:%M').time()
                    else:
                        hora_time = cita_hora_inicio
                    cita_datetime = datetime.combine(cita_datetime.date(), hora_time)
                except Exception as e:
                    app.logger.error(f"Error al parsear fecha/hora: {str(e)}", exc_info=True)
                    return False
            else:
                app.logger.error(f"Tipo de fecha no soportado: {type(cita_fecha)}")
                return False
            
            # Asegurar que cita_datetime es un datetime
            if not isinstance(cita_datetime, datetime):
                app.logger.error(f"cita_datetime no es datetime: {type(cita_datetime)}")
                return False
            
            # Calcular fechas programadas para recordatorios
            # Recordatorio 24 horas antes
            fecha_24h = cita_datetime - timedelta(hours=24)
            # Recordatorio 12 horas antes
            fecha_12h = cita_datetime - timedelta(hours=12)
            
            # Solo programar recordatorios si la fecha programada es en el futuro
            ahora = datetime.now()
            fecha_24h_programada = fecha_24h if fecha_24h > ahora else None
            fecha_12h_programada = fecha_12h if fecha_12h > ahora else None
            
            # Crear o actualizar recordatorio (una sola fila por cita)
            try:
                # Convertir fecha a date si es datetime
                cita_fecha_date = cita_fecha if isinstance(cita_fecha, date) else cita_datetime.date()
                # Convertir hora a time si es datetime
                cita_hora_time = cita_hora_inicio if isinstance(cita_hora_inicio, (time, str)) else cita_datetime.time()
                
                if isinstance(cita_hora_time, str):
                    cita_hora_time = datetime.strptime(cita_hora_time, '%H:%M:%S').time()
                
                resultado = recordatorio_dao.crearOActualizarRecordatorio(
                    id_cita=id_cita,
                    cita_fecha=cita_fecha_date,
                    cita_hora_inicio=cita_hora_time,
                    telefono=telefono,
                    paciente_nombre=paciente_nombre,
                    fecha_24h=fecha_24h_programada,
                    fecha_12h=fecha_12h_programada,
                    usuario_creacion=usuario_creacion
                )
                
                if resultado:
                    recordatorios_info = []
                    if fecha_24h_programada:
                        recordatorios_info.append(f"24h programado para {fecha_24h_programada}")
                    else:
                        recordatorios_info.append("24h no programado (fecha ya pasó)")
                    
                    if fecha_12h_programada:
                        recordatorios_info.append(f"12h programado para {fecha_12h_programada}")
                    else:
                        recordatorios_info.append("12h no programado (fecha ya pasó)")
                    
                    app.logger.info(
                        f"✅ Recordatorios creados/actualizados para cita {id_cita}: {', '.join(recordatorios_info)}"
                    )
                    return True
                else:
                    app.logger.warning(f"⚠️ No se pudo crear/actualizar recordatorios para cita {id_cita}")
                    return False
            except Exception as e:
                app.logger.error(f"Error al crear/actualizar recordatorios: {str(e)}", exc_info=True)
                return False
            
        except Exception as e:
            app.logger.error(f"Error al crear recordatorios para cita {id_cita}: {str(e)}", exc_info=True)
            return False

    # =====================================================
    # FILTROS ADICIONALES
    # =====================================================
    
    def getCitasByPaciente(self, id_paciente):
        """Obtiene todas las citas de un paciente"""
        citasSQL = """
            SELECT
                c.id_cita,
                c.cita_fecha,
                c.cita_hora_inicio,
                c.cita_es_primera_vez,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                esp.des_especialidad,
                ec.est_cita_nombre,
                ec.est_cita_color
            FROM citas c
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.id_paciente = %s AND c.cita_activo = TRUE
            ORDER BY c.cita_fecha DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(citasSQL, (id_paciente,))
            citas = cur.fetchall()
            
            return [{
                'id_cita': c[0],
                'fecha': c[1].strftime('%d/%m/%Y') if c[1] else None,
                'hora': c[2].strftime('%H:%M') if c[2] else None,
                'tipo': 'PRIMERA_VEZ' if c[3] else 'SEGUIMIENTO',  # ✅ Convertir boolean a string
                'especialista': c[4],
                'especialidad': c[5],
                'estado': c[6],
                'estado_color': c[7]
            } for c in citas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener citas del paciente: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCitasByEspecialista(self, id_especialista):
        """Obtiene todas las citas de un especialista"""
        citasSQL = """
            SELECT
                c.id_cita,
                c.cita_fecha,
                c.cita_hora_inicio,
                c.cita_es_primera_vez,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                p.pac_historia_clinica,
                ec.est_cita_nombre,
                ec.est_cita_color
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.id_especialista = %s AND c.cita_activo = TRUE
            ORDER BY c.cita_fecha DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(citasSQL, (id_especialista,))
            citas = cur.fetchall()
            
            return [{
                'id_cita': c[0],
                'fecha': c[1].strftime('%d/%m/%Y') if c[1] else None,
                'hora': c[2].strftime('%H:%M') if c[2] else None,
                'tipo': 'PRIMERA_VEZ' if c[3] else 'SEGUIMIENTO',  # ✅ Convertir boolean a string
                'paciente': c[4],
                'historia_clinica': c[5],
                'estado': c[6],
                'estado_color': c[7]
            } for c in citas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener citas del especialista: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCitasByFecha(self, fecha_inicio, fecha_fin):
        """Obtiene citas en un rango de fechas"""
        citasSQL = """
            SELECT
                c.id_cita,
                c.cita_fecha,
                c.cita_hora_inicio,
                c.cita_es_primera_vez,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                esp.des_especialidad,
                ec.est_cita_nombre,
                ec.est_cita_color
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha BETWEEN %s AND %s
                AND c.cita_activo = TRUE
            ORDER BY c.cita_fecha, c.cita_hora_inicio
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(citasSQL, (fecha_inicio, fecha_fin))
            citas = cur.fetchall()
            
            return [{
                'id_cita': c[0],
                'fecha': c[1].strftime('%d/%m/%Y') if c[1] else None,
                'hora': c[2].strftime('%H:%M') if c[2] else None,
                'tipo': 'PRIMERA_VEZ' if c[3] else 'SEGUIMIENTO',  # ✅ Convertir boolean a string
                'paciente': c[4],
                'especialista': c[5],
                'especialidad': c[6],
                'estado': c[7],
                'estado_color': c[8]
            } for c in citas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener citas por fecha: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()




























