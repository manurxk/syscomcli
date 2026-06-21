from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date

class FichaMedicaDao:
    """
    DAO para obtener la ficha médica completa de un paciente
    Centraliza todas las consultas necesarias para la vista de historia clínica
    """
    
    # ==========================================
    # MÉTODO PRINCIPAL - FICHA COMPLETA
    # ==========================================
    
    def getFichaMedicaCompleta(self, id_paciente):
        """
        Obtiene toda la información necesaria para la ficha médica de un paciente
        Retorna un diccionario con todas las secciones incluyendo anamnesis
        """
        try:
            return {
                'paciente': self.getDatosPaciente(id_paciente),
                'anamnesis': self.getAnamnesisPaciente(id_paciente),
                'consultas_recientes': self.getConsultasRecientes(id_paciente, limite=10),
                'diagnosticos': self.getDiagnosticosPaciente(id_paciente),
                'tratamientos_activos': self.getTratamientosActivos(id_paciente),
                'procedimientos': self.getProcedimientosRecientes(id_paciente, limite=15),
                'proximas_citas': self.getProximasCitas(id_paciente, limite=5),
                'timeline': self.getTimelineEventos(id_paciente, limite=30)
            }
        except Exception as e:
            app.logger.error(f"Error al obtener ficha médica completa: {str(e)}")
            return None
    
    # ==========================================
    # DATOS DEL PACIENTE
    # ==========================================
    
    def getDatosPaciente(self, id_paciente):
        """Obtiene los datos completos del paciente"""
        pacienteSQL = """
            SELECT
                pac.id_paciente,
                pac.pac_historia_clinica,
                pac.pac_observaciones,
                CONCAT(per.per_nombre, ' ', per.per_apellido) AS nombre_completo,
                per.per_nombre,
                per.per_apellido,
                per.per_cedula,
                per.per_fecha_nacimiento,
                DATE_PART('year', AGE(per.per_fecha_nacimiento)) AS edad,
                per.per_telefono,
                per.per_correo,
                per.per_domicilio,
                g.des_genero,
                ec.des_estado_civil,
                c.des_ciudad,
                cn.des_ciudad AS ciudad_nacimiento,
                ni.des_nivel_instruccion,
                pr.des_profesion,
                CASE WHEN DATE_PART('year', AGE(per.per_fecha_nacimiento)) < 18 THEN TRUE ELSE FALSE END AS es_menor,
                pm.pam_nom_madre,
                pm.pam_tel_madre,
                pm.pam_nom_padre,
                pm.pam_tel_padre,
                pm.pam_colegio,
                per.per_fecha_inscripcion
            FROM pacientes pac
            JOIN personas per ON pac.id_persona = per.id_persona
            LEFT JOIN generos g ON per.id_genero = g.id_genero
            LEFT JOIN estados_civiles ec ON per.id_estado_civil = ec.id_estado_civil
            LEFT JOIN ciudades c ON per.id_ciudad = c.id_ciudad
            LEFT JOIN ciudades cn ON per.id_ciudad_nacimiento = cn.id_ciudad
            LEFT JOIN niveles_instruccion ni ON per.id_nivel_instruccion = ni.id_nivel_instruccion
            LEFT JOIN profesiones pr ON per.id_profesion = pr.id_profesion
            LEFT JOIN pacientes_menores pm ON pac.id_paciente = pm.id_paciente
            WHERE pac.id_paciente = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(pacienteSQL, (id_paciente,))
            p = cur.fetchone()
            
            if not p:
                return None
            
            return {
                'id_paciente': p[0],
                'historia_clinica': p[1],
                'observaciones': p[2],
                'nombre_completo': p[3],
                'nombre': p[4],
                'apellido': p[5],
                'cedula': p[6],
                'fecha_nacimiento': p[7].strftime('%d/%m/%Y') if p[7] else None,
                'edad': int(p[8]) if p[8] else None,
                'telefono': p[9],
                'correo': p[10],
                'domicilio': p[11],
                'genero': p[12],
                'estado_civil': p[13],
                'ciudad': p[14],
                'ciudad_nacimiento': p[15],
                'nivel_instruccion': p[16],
                'profesion': p[17],
                'es_menor': p[18],
                'madre_nombre': p[19],
                'madre_telefono': p[20],
                'padre_nombre': p[21],
                'padre_telefono': p[22],
                'colegio': p[23],
                'fecha_registro': p[24].strftime('%d/%m/%Y') if p[24] else None
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener datos del paciente: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # ANAMNESIS DEL PACIENTE
    # ==========================================
    
    def getAnamnesisPaciente(self, id_paciente):
        """Obtiene la anamnesis activa del paciente para la ficha médica"""
        anamnesisSQL = """
            SELECT
                a.id_anamnesis,
                a.informante,
                a.relacion_informante,
                a.motivo_consulta,
                a.fecha_elaboracion,
                a.fecha_ultima_modificacion,
                a.antecedentes_familiares_similares,
                a.antecedentes_patologicos_familiares,
                a.componentes_familiares,
                a.historia_familiar,
                a.antecedentes_patologicos_personales,
                a.historia_problema_actual,
                a.historia_desarrollo,
                a.historia_academica,
                a.historia_laboral,
                a.historia_rehabilitacion,
                a.medicacion_actual,
                a.medicacion_psiquiatrica_previa,
                a.consumo_sustancias,
                a.relaciones_interpersonales,
                a.actividad_fisica,
                a.patron_sueno,
                a.patron_alimentacion,
                a.actividad_emocional,
                a.actividad_sexual,
                a.impresion_diagnostica,
                a.plan_trabajo,
                a.eval_neuropsicologica,
                a.eval_psicologica,
                a.eval_psicopedagogica,
                a.eval_fonoaudiologica,
                a.eval_psicomotora,
                a.terapia_individual,
                a.terapia_familiar,
                a.terapia_grupal,
                a.terapia_ocupacional,
                a.otra_terapia,
                a.observaciones,
                a.indicaciones,
                a.version,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS elaborado_por_nombre
            FROM anamnesis a
            LEFT JOIN usuarios u ON a.elaborado_por = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE a.id_paciente = %s AND a.activo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(anamnesisSQL, (id_paciente,))
            a = cur.fetchone()
            
            if not a:
                return None
            
            return {
                'id_anamnesis': a[0],
                'informante': a[1],
                'relacion_informante': a[2],
                'motivo_consulta': a[3],
                'fecha_elaboracion': a[4].strftime('%d/%m/%Y %H:%M') if a[4] else None,
                'fecha_ultima_modificacion': a[5].strftime('%d/%m/%Y %H:%M') if a[5] else None,
                'antecedentes_familiares_similares': a[6],
                'antecedentes_patologicos_familiares': a[7],
                'componentes_familiares': a[8],
                'historia_familiar': a[9],
                'antecedentes_patologicos_personales': a[10],
                'historia_problema_actual': a[11],
                'historia_desarrollo': a[12],
                'historia_academica': a[13],
                'historia_laboral': a[14],
                'historia_rehabilitacion': a[15],
                'medicacion_actual': a[16],
                'medicacion_psiquiatrica_previa': a[17],
                'consumo_sustancias': a[18],
                'relaciones_interpersonales': a[19],
                'actividad_fisica': a[20],
                'patron_sueno': a[21],
                'patron_alimentacion': a[22],
                'actividad_emocional': a[23],
                'actividad_sexual': a[24],
                'impresion_diagnostica': a[25],
                'plan_trabajo': a[26],
                'eval_neuropsicologica': a[27],
                'eval_psicologica': a[28],
                'eval_psicopedagogica': a[29],
                'eval_fonoaudiologica': a[30],
                'eval_psicomotora': a[31],
                'terapia_individual': a[32],
                'terapia_familiar': a[33],
                'terapia_grupal': a[34],
                'terapia_ocupacional': a[35],
                'otra_terapia': a[36],
                'observaciones': a[37],
                'indicaciones': a[38],
                'version': a[39],
                'elaborado_por_nombre': a[40]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener anamnesis del paciente: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # CONSULTAS RECIENTES
    # ==========================================
    
    def getConsultasRecientes(self, id_paciente, limite=10):
        """Obtiene las últimas consultas del paciente"""
        consultasSQL = """
            SELECT
                c.id_consulta,
                c.consulta_fecha,
                c.consulta_motivo,
                c.consulta_estado,
                c.des_consulta,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                (SELECT COUNT(*) FROM registro_diagnosticos WHERE id_consulta = c.id_consulta AND est_registro_diagnostico = 'A') AS total_diagnosticos,
                (SELECT COUNT(*) FROM registro_procedimientos WHERE id_consulta = c.id_consulta AND est_registro_procedimiento = 'A') AS total_procedimientos
            FROM consultas c
            JOIN especialistas e ON c.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_paciente = %s AND c.est_consulta = 'A'
            ORDER BY c.consulta_fecha DESC
            LIMIT %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(consultasSQL, (id_paciente, limite))
            consultas = cur.fetchall()
            
            return [{
                'id_consulta': c[0],
                'fecha': c[1].strftime('%d/%m/%Y %H:%M') if c[1] else None,
                'motivo': c[2],
                'estado': c[3],
                'descripcion': c[4],
                'profesional': c[5],
                'matricula': c[6],
                'total_diagnosticos': c[7] or 0,
                'total_procedimientos': c[8] or 0
            } for c in consultas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener consultas recientes: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # DIAGNÓSTICOS
    # ==========================================
    
    def getDiagnosticosPaciente(self, id_paciente):
        """Obtiene todos los diagnósticos del paciente"""
        diagnosticosSQL = """
            SELECT
                rd.id_registro_diagnostico,
                rd.registro_fecha,
                rd.registro_tipo,
                rd.registro_gravedad,
                rd.des_registro_diagnostico,
                d.des_diagnostico,
                d.diagnostico_codigo_cie10,
                c.consulta_fecha,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                (SELECT COUNT(*) FROM tratamientos WHERE id_registro_diagnostico = rd.id_registro_diagnostico AND est_tratamiento = 'A') AS tiene_tratamiento
            FROM registro_diagnosticos rd
            JOIN diagnosticos d ON rd.id_diagnostico = d.id_diagnostico
            JOIN consultas c ON rd.id_consulta = c.id_consulta
            JOIN especialistas e ON c.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_paciente = %s AND rd.est_registro_diagnostico = 'A'
            ORDER BY rd.registro_fecha DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(diagnosticosSQL, (id_paciente,))
            diagnosticos = cur.fetchall()
            
            return [{
                'id_registro_diagnostico': d[0],
                'fecha': d[1].strftime('%d/%m/%Y') if d[1] else None,
                'tipo': d[2],
                'gravedad': d[3],
                'descripcion_especifica': d[4],
                'diagnostico': d[5],
                'codigo_cie10': d[6],
                'fecha_consulta': d[7].strftime('%d/%m/%Y') if d[7] else None,
                'profesional': d[8],
                'tiene_tratamiento': d[9] > 0
            } for d in diagnosticos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener diagnósticos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # TRATAMIENTOS ACTIVOS
    # ==========================================
    
    def getTratamientosActivos(self, id_paciente):
        """Obtiene los tratamientos activos del paciente"""
        tratamientosSQL = """
            SELECT
                t.id_tratamiento,
                t.des_tratamiento,
                t.tratamiento_objetivos,
                t.tratamiento_estado,
                t.numero_sesiones,
                t.frecuencia_sesiones,
                t.duracion_sesion,
                t.tratamiento_fecha_inicio,
                t.tratamiento_fecha_fin,
                tt.des_tipo_tratamiento,
                d.des_diagnostico,
                d.diagnostico_codigo_cie10,
                CURRENT_DATE - t.tratamiento_fecha_inicio AS dias_tratamiento,
                CASE 
                    WHEN t.tratamiento_fecha_fin IS NOT NULL 
                    THEN t.tratamiento_fecha_fin - CURRENT_DATE 
                    ELSE NULL 
                END AS dias_restantes
            FROM tratamientos t
            LEFT JOIN tipos_tratamientos tt ON t.id_tipo_tratamiento = tt.id_tipo_tratamiento
            LEFT JOIN registro_diagnosticos rd ON t.id_registro_diagnostico = rd.id_registro_diagnostico
            LEFT JOIN diagnosticos d ON rd.id_diagnostico = d.id_diagnostico
            WHERE t.id_paciente = %s 
              AND t.tratamiento_estado IN ('ACTIVO', 'EN_PAUSA')
              AND t.est_tratamiento = 'A'
            ORDER BY t.tratamiento_fecha_inicio DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(tratamientosSQL, (id_paciente,))
            tratamientos = cur.fetchall()
            
            return [{
                'id_tratamiento': t[0],
                'descripcion': t[1],
                'objetivos': t[2],
                'estado': t[3],
                'numero_sesiones': t[4],
                'frecuencia_sesiones': t[5],
                'duracion_sesion': t[6],
                'fecha_inicio': t[7].strftime('%d/%m/%Y') if t[7] else None,
                'fecha_fin': t[8].strftime('%d/%m/%Y') if t[8] else None,
                'tipo_tratamiento': t[9],
                'diagnostico': t[10],
                'codigo_cie10': t[11],
                'dias_tratamiento': t[12],
                'dias_restantes': t[13]
            } for t in tratamientos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener tratamientos activos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # PROCEDIMIENTOS RECIENTES
    # ==========================================
    
    def getProcedimientosRecientes(self, id_paciente, limite=15):
        """Obtiene los procedimientos recientes del paciente"""
        procedimientosSQL = """
            SELECT
                rp.id_registro_procedimiento,
                rp.registro_fecha,
                rp.des_registro_procedimiento,
                rp.registro_duracion,
                rp.registro_resultado,
                tp.des_tipo_procedimiento,
                c.consulta_fecha,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre
            FROM registro_procedimientos rp
            JOIN tipos_procedimientos tp ON rp.id_tipo_procedimiento = tp.id_tipo_procedimiento
            JOIN consultas c ON rp.id_consulta = c.id_consulta
            JOIN especialistas e ON c.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE rp.id_paciente = %s AND rp.est_registro_procedimiento = 'A'
            ORDER BY rp.registro_fecha DESC
            LIMIT %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(procedimientosSQL, (id_paciente, limite))
            procedimientos = cur.fetchall()
            
            return [{
                'id_registro_procedimiento': p[0],
                'fecha': p[1].strftime('%d/%m/%Y %H:%M') if p[1] else None,
                'descripcion': p[2],
                'duracion': p[3],
                'resultado': p[4],
                'tipo_procedimiento': p[5],
                'fecha_consulta': p[6].strftime('%d/%m/%Y') if p[6] else None,
                'profesional': p[7]
            } for p in procedimientos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener procedimientos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # PRÓXIMAS CITAS
    # ==========================================
    
    def getProximasCitas(self, id_paciente, limite=5):
        """Obtiene las próximas citas del paciente"""
        citasSQL = """
            SELECT
                cit.id_cita,
                cit.cita_fecha,
                cit.cita_hora_inicio,
                cit.cita_hora_fin,
                cit.cita_tipo,
                cit.cita_motivo,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                esp.des_especialidad,
                ec.est_cita_nombre,
                ec.est_cita_color,
                cit.cita_fecha - CURRENT_DATE AS dias_hasta_cita
            FROM citas cit
            JOIN especialistas e ON cit.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON cit.id_especialidad = esp.id_especialidad
            JOIN estados_citas ec ON cit.id_estado_cita = ec.id_estado_cita
            WHERE cit.id_paciente = %s 
              AND cit.cita_fecha >= CURRENT_DATE
              AND cit.cita_activo = TRUE
            ORDER BY cit.cita_fecha, cit.cita_hora_inicio
            LIMIT %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(citasSQL, (id_paciente, limite))
            citas = cur.fetchall()
            
            return [{
                'id_cita': c[0],
                'fecha': c[1].strftime('%d/%m/%Y') if c[1] else None,
                'hora_inicio': c[2].strftime('%H:%M') if c[2] else None,
                'hora_fin': c[3].strftime('%H:%M') if c[3] else None,
                'tipo': c[4],
                'motivo': c[5],
                'especialista': c[6],
                'especialidad': c[7],
                'estado': c[8],
                'estado_color': c[9],
                'dias_hasta_cita': c[10]
            } for c in citas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener próximas citas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # TIMELINE DE EVENTOS
    # ==========================================
    
    def getTimelineEventos(self, id_paciente, limite=30):
        """Obtiene un timeline unificado de todos los eventos médicos"""
        timelineSQL = """
            SELECT * FROM (
                -- CONSULTAS
                SELECT 
                    'CONSULTA' AS tipo_evento,
                    c.id_consulta AS id_evento,
                    c.consulta_fecha AS fecha_evento,
                    c.consulta_motivo AS descripcion,
                    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional,
                    c.consulta_estado AS detalle_adicional
                FROM consultas c
                JOIN especialistas e ON c.id_profesional = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE c.id_paciente = %s AND c.est_consulta = 'A'
                
                UNION ALL
                
                -- DIAGNÓSTICOS
                SELECT 
                    'DIAGNOSTICO' AS tipo_evento,
                    rd.id_registro_diagnostico AS id_evento,
                    rd.registro_fecha AS fecha_evento,
                    d.des_diagnostico AS descripcion,
                    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional,
                    CONCAT(d.diagnostico_codigo_cie10, ' - ', rd.registro_gravedad) AS detalle_adicional
                FROM registro_diagnosticos rd
                JOIN diagnosticos d ON rd.id_diagnostico = d.id_diagnostico
                JOIN consultas c ON rd.id_consulta = c.id_consulta
                JOIN especialistas e ON c.id_profesional = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE c.id_paciente = %s AND rd.est_registro_diagnostico = 'A'
                
                UNION ALL
                
                -- PROCEDIMIENTOS
                SELECT 
                    'PROCEDIMIENTO' AS tipo_evento,
                    rp.id_registro_procedimiento AS id_evento,
                    rp.registro_fecha AS fecha_evento,
                    tp.des_tipo_procedimiento AS descripcion,
                    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional,
                    rp.registro_resultado AS detalle_adicional
                FROM registro_procedimientos rp
                JOIN tipos_procedimientos tp ON rp.id_tipo_procedimiento = tp.id_tipo_procedimiento
                JOIN consultas c ON rp.id_consulta = c.id_consulta
                JOIN especialistas e ON c.id_profesional = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE rp.id_paciente = %s AND rp.est_registro_procedimiento = 'A'
                
                UNION ALL
                
                -- TRATAMIENTOS
                SELECT 
                    'TRATAMIENTO' AS tipo_evento,
                    t.id_tratamiento AS id_evento,
                    t.tratamiento_fecha_inicio AS fecha_evento,
                    t.des_tratamiento AS descripcion,
                    'Sistema' AS profesional,
                    t.tratamiento_estado AS detalle_adicional
                FROM tratamientos t
                WHERE t.id_paciente = %s AND t.est_tratamiento = 'A'
            ) eventos
            ORDER BY fecha_evento DESC
            LIMIT %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(timelineSQL, (id_paciente, id_paciente, id_paciente, id_paciente, limite))
            eventos = cur.fetchall()
            
            return [{
                'tipo_evento': e[0],
                'id_evento': e[1],
                'fecha': e[2].strftime('%d/%m/%Y') if e[2] else None,
                'descripcion': e[3],
                'profesional': e[4],
                'detalle': e[5]
            } for e in eventos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener timeline: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    # ==========================================
    # MÉTODO PARA EXPORTAR FICHA
    # ==========================================
    
    def getFichaMedicaParaExportar(self, id_paciente):
        """
        Obtiene la ficha médica completa con formato optimizado para exportación
        Incluye anamnesis y más detalles que la versión normal
        """
        try:
            ficha = self.getFichaMedicaCompleta(id_paciente)
            
            if not ficha:
                return None
            
            # Agregar información adicional para el reporte
            ficha['metadata'] = {
                'fecha_generacion': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'sistema': 'Sistema de Gestión Médica',
                'version': '1.0'
            }
            
            return ficha
            
        except Exception as e:
            app.logger.error(f"Error al preparar ficha para exportar: {str(e)}")
            return None