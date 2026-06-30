from app.core.base_dao import BaseDAO


class FichaDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    # ----------------------------------------
    # FICHA COMPLETA
    # ----------------------------------------

    def getFichaCompleta(self, id_paciente):
        return {
            'paciente': self.getDatosPaciente(id_paciente),
            'anamnesis': self.getAnamnesisPaciente(id_paciente),
            'pei': self.getPeiPaciente(id_paciente),
            'consultas_recientes': self.getConsultasRecientes(id_paciente, limite=10),
            'diagnosticos': self.getDiagnosticosPaciente(id_paciente),
            'tratamientos_activos': self.getTratamientosActivos(id_paciente),
            'procedimientos': self.getProcedimientosRecientes(id_paciente, limite=15),
            'proximas_citas': self.getProximasCitas(id_paciente, limite=5),
            'notas': self.getNotasPaciente(id_paciente),
            'timeline': self.getTimeline(id_paciente, limite=30),
        }

    # ----------------------------------------
    # DATOS DEL PACIENTE
    # ----------------------------------------

    def getDatosPaciente(self, id_paciente):
        sql = """
            SELECT
                pac.id_paciente,
                pac.pac_historia_clinica,
                pac.pac_observaciones,
                per.per_nombre || ' ' || per.per_apellido AS nombre_completo,
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
                CASE WHEN DATE_PART('year', AGE(per.per_fecha_nacimiento)) < 18
                     THEN TRUE ELSE FALSE END AS es_menor,
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
        f = self.execute_query_one(sql, (id_paciente,))
        if not f:
            return None
        return {
            'id_paciente': f['id_paciente'],
            'historia_clinica': f['pac_historia_clinica'],
            'observaciones': f['pac_observaciones'],
            'nombre_completo': f['nombre_completo'],
            'nombre': f['per_nombre'],
            'apellido': f['per_apellido'],
            'cedula': f['per_cedula'],
            'fecha_nacimiento': f['per_fecha_nacimiento'].strftime('%d/%m/%Y') if f['per_fecha_nacimiento'] else None,
            'edad': int(f['edad']) if f['edad'] else None,
            'telefono': f['per_telefono'],
            'correo': f['per_correo'],
            'domicilio': f['per_domicilio'],
            'genero': f['des_genero'],
            'estado_civil': f['des_estado_civil'],
            'ciudad': f['des_ciudad'],
            'ciudad_nacimiento': f['ciudad_nacimiento'],
            'nivel_instruccion': f['des_nivel_instruccion'],
            'profesion': f['des_profesion'],
            'es_menor': f['es_menor'],
            'madre_nombre': f['pam_nom_madre'],
            'madre_telefono': f['pam_tel_madre'],
            'padre_nombre': f['pam_nom_padre'],
            'padre_telefono': f['pam_tel_padre'],
            'colegio': f['pam_colegio'],
            'fecha_registro': f['per_fecha_inscripcion'].strftime('%d/%m/%Y') if f['per_fecha_inscripcion'] else None,
        }

    # ----------------------------------------
    # ANAMNESIS (versión vigente)
    # ----------------------------------------

    def getAnamnesisPaciente(self, id_paciente):
        sql = """
            SELECT
                a.id_anamnesis, a.nro_version, a.motivo_consulta,
                a.informante, a.relacion_informante,
                a.antecedentes_familiares_similares, a.antecedentes_patologicos_familiares,
                a.historia_familiar, a.antecedentes_patologicos_personales,
                a.historia_problema_actual, a.historia_desarrollo,
                a.historia_academica, a.historia_laboral, a.historia_rehabilitacion,
                a.medicacion_actual, a.medicacion_psiquiatrica_previa,
                a.consumo_sustancias, a.relaciones_interpersonales,
                a.actividad_fisica, a.patron_sueno, a.patron_alimentacion,
                a.actividad_emocional, a.actividad_sexual,
                a.impresion_diagnostica, a.plan_trabajo,
                a.eval_neuropsicologica, a.eval_psicologica, a.eval_psicopedagogica,
                a.eval_fonoaudiologica, a.eval_psicomotora,
                a.terapia_individual, a.terapia_familiar, a.terapia_grupal,
                a.terapia_ocupacional, a.otra_terapia,
                a.observaciones, a.indicaciones,
                a.fecha_creacion, a.fecha_modificacion
            FROM anamnesis a
            WHERE a.id_paciente = %s AND a.es_version_actual = TRUE
        """
        f = self.execute_query_one(sql, (id_paciente,))
        if not f:
            return None
        f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        f['fecha_modificacion'] = f['fecha_modificacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_modificacion'] else None
        return f

    # ----------------------------------------
    # PEI (versión vigente)
    # ----------------------------------------

    def getPeiPaciente(self, id_paciente):
        sql = """
            SELECT
                p.id_pei, p.nro_version, p.pei_estado,
                p.pei_objetivos, p.pei_areas_intervencion, p.pei_estrategias,
                p.pei_cronograma_seguimiento,
                p.fecha_creacion, p.fecha_modificacion,
                fp.per_nombre || ' ' || fp.per_apellido AS especialista_nombre
            FROM pei p
            JOIN especialistas e ON p.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas fp ON f.id_persona = fp.id_persona
            WHERE p.id_paciente = %s AND p.es_version_actual = TRUE
        """
        f = self.execute_query_one(sql, (id_paciente,))
        if not f:
            return None
        f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        f['fecha_modificacion'] = f['fecha_modificacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_modificacion'] else None
        return f

    # ----------------------------------------
    # CONSULTAS RECIENTES
    # ----------------------------------------

    def getConsultasRecientes(self, id_paciente, limite=10):
        sql = """
            SELECT
                c.id_consulta,
                c.consulta_fecha,
                c.consulta_motivo,
                c.consulta_estado,
                c.des_consulta,
                pe.per_nombre || ' ' || pe.per_apellido AS profesional_nombre,
                e.esp_matricula,
                (SELECT COUNT(*) FROM registro_diagnosticos rd
                 WHERE rd.id_consulta = c.id_consulta AND rd.est_registro_diagnostico = TRUE
                ) AS total_diagnosticos,
                (SELECT COUNT(*) FROM registro_procedimientos rp
                 WHERE rp.id_consulta = c.id_consulta AND rp.est_registro_procedimiento = TRUE
                ) AS total_procedimientos
            FROM consultas c
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_paciente = %s AND c.est_consulta = TRUE
            ORDER BY c.consulta_fecha DESC
            LIMIT %s
        """
        filas = self.execute_query(sql, (id_paciente, limite))
        return [{
            'id_consulta': f['id_consulta'],
            'fecha': f['consulta_fecha'].strftime('%d/%m/%Y %H:%M') if f['consulta_fecha'] else None,
            'motivo': f['consulta_motivo'],
            'estado': f['consulta_estado'],
            'descripcion': f['des_consulta'],
            'profesional': f['profesional_nombre'],
            'matricula': f['esp_matricula'],
            'total_diagnosticos': f['total_diagnosticos'] or 0,
            'total_procedimientos': f['total_procedimientos'] or 0,
        } for f in filas]

    # ----------------------------------------
    # DIAGNÓSTICOS
    # ----------------------------------------

    def getDiagnosticosPaciente(self, id_paciente):
        sql = """
            SELECT
                rd.id_registro_diagnostico,
                rd.fecha_creacion,
                rd.registro_tipo,
                rd.registro_gravedad,
                rd.des_registro_diagnostico,
                d.des_diagnostico,
                d.cod_cie10,
                c.consulta_fecha,
                pe.per_nombre || ' ' || pe.per_apellido AS profesional_nombre
            FROM registro_diagnosticos rd
            JOIN diagnosticos d ON rd.id_diagnostico = d.id_diagnostico
            JOIN consultas c ON rd.id_consulta = c.id_consulta
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_paciente = %s AND rd.est_registro_diagnostico = TRUE
            ORDER BY rd.fecha_creacion DESC
        """
        filas = self.execute_query(sql, (id_paciente,))
        return [{
            'id_registro_diagnostico': f['id_registro_diagnostico'],
            'fecha': f['fecha_creacion'].strftime('%d/%m/%Y') if f['fecha_creacion'] else None,
            'tipo': f['registro_tipo'],
            'gravedad': f['registro_gravedad'],
            'descripcion_especifica': f['des_registro_diagnostico'],
            'diagnostico': f['des_diagnostico'],
            'cod_cie10': f['cod_cie10'],
            'fecha_consulta': f['consulta_fecha'].strftime('%d/%m/%Y') if f['consulta_fecha'] else None,
            'profesional': f['profesional_nombre'],
        } for f in filas]

    # ----------------------------------------
    # TRATAMIENTOS ACTIVOS
    # ----------------------------------------

    def getTratamientosActivos(self, id_paciente):
        sql = """
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
                t.tratamiento_observaciones,
                tt.des_tipo_tratamiento,
                c.consulta_fecha,
                pe.per_nombre || ' ' || pe.per_apellido AS profesional_nombre,
                CURRENT_DATE - t.tratamiento_fecha_inicio::DATE AS dias_tratamiento,
                CASE
                    WHEN t.tratamiento_fecha_fin IS NOT NULL
                    THEN t.tratamiento_fecha_fin::DATE - CURRENT_DATE
                    ELSE NULL
                END AS dias_restantes
            FROM tratamientos t
            JOIN tipos_tratamientos tt ON t.id_tipo_tratamiento = tt.id_tipo_tratamiento
            JOIN consultas c ON t.id_consulta = c.id_consulta
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_paciente = %s AND t.est_tratamiento = TRUE
            ORDER BY t.tratamiento_fecha_inicio DESC
        """
        filas = self.execute_query(sql, (id_paciente,))
        return [{
            'id_tratamiento': f['id_tratamiento'],
            'descripcion': f['des_tratamiento'],
            'objetivos': f['tratamiento_objetivos'],
            'estado': f['tratamiento_estado'],
            'numero_sesiones': f['numero_sesiones'],
            'frecuencia_sesiones': f['frecuencia_sesiones'],
            'duracion_sesion': f['duracion_sesion'],
            'fecha_inicio': f['tratamiento_fecha_inicio'].strftime('%d/%m/%Y') if f['tratamiento_fecha_inicio'] else None,
            'fecha_fin': f['tratamiento_fecha_fin'].strftime('%d/%m/%Y') if f['tratamiento_fecha_fin'] else None,
            'observaciones': f['tratamiento_observaciones'],
            'tipo_tratamiento': f['des_tipo_tratamiento'],
            'fecha_consulta': f['consulta_fecha'].strftime('%d/%m/%Y') if f['consulta_fecha'] else None,
            'profesional': f['profesional_nombre'],
            'dias_tratamiento': int(f['dias_tratamiento']) if f['dias_tratamiento'] is not None else None,
            'dias_restantes': int(f['dias_restantes']) if f['dias_restantes'] is not None else None,
        } for f in filas]

    # ----------------------------------------
    # PROCEDIMIENTOS RECIENTES
    # ----------------------------------------

    def getProcedimientosRecientes(self, id_paciente, limite=15):
        sql = """
            SELECT
                rp.id_registro_procedimiento,
                rp.fecha_creacion,
                rp.des_registro_procedimiento,
                rp.registro_duracion,
                rp.registro_resultado,
                tp.des_tipo_procedimiento,
                c.consulta_fecha,
                pe.per_nombre || ' ' || pe.per_apellido AS profesional_nombre
            FROM registro_procedimientos rp
            JOIN tipos_procedimientos tp ON rp.id_tipo_procedimiento = tp.id_tipo_procedimiento
            JOIN consultas c ON rp.id_consulta = c.id_consulta
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_paciente = %s AND rp.est_registro_procedimiento = TRUE
            ORDER BY rp.fecha_creacion DESC
            LIMIT %s
        """
        filas = self.execute_query(sql, (id_paciente, limite))
        return [{
            'id_registro_procedimiento': f['id_registro_procedimiento'],
            'fecha': f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None,
            'descripcion': f['des_registro_procedimiento'],
            'duracion': f['registro_duracion'],
            'resultado': f['registro_resultado'],
            'tipo_procedimiento': f['des_tipo_procedimiento'],
            'fecha_consulta': f['consulta_fecha'].strftime('%d/%m/%Y') if f['consulta_fecha'] else None,
            'profesional': f['profesional_nombre'],
        } for f in filas]

    # ----------------------------------------
    # PRÓXIMAS CITAS
    # ----------------------------------------

    def getProximasCitas(self, id_paciente, limite=5):
        sql = """
            SELECT
                cit.id_cita,
                cit.cita_inicio,
                cit.cita_fin,
                cit.motivo,
                pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre,
                esp.des_especialidad,
                ec.cod_estado_cita,
                ec.des_estado_cita,
                cit.cita_inicio::DATE - CURRENT_DATE AS dias_hasta_cita
            FROM citas cit
            JOIN especialistas e ON cit.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialista_especialidades ee ON ee.id_especialista = e.id_especialista AND ee.est_especialista_especialidad = TRUE
            JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad
            JOIN estados_citas ec ON cit.id_estado_cita = ec.id_estado_cita
            WHERE cit.id_paciente = %s
              AND cit.cita_inicio >= NOW()
              AND cit.est_cita = TRUE
            ORDER BY cit.cita_inicio
            LIMIT %s
        """
        filas = self.execute_query(sql, (id_paciente, limite))
        return [{
            'id_cita': f['id_cita'],
            'fecha': f['cita_inicio'].strftime('%d/%m/%Y') if f['cita_inicio'] else None,
            'hora_inicio': f['cita_inicio'].strftime('%H:%M') if f['cita_inicio'] else None,
            'hora_fin': f['cita_fin'].strftime('%H:%M') if f['cita_fin'] else None,
            'motivo': f['motivo'],
            'especialista': f['especialista_nombre'],
            'especialidad': f['des_especialidad'],
            'estado_cod': f['cod_estado_cita'],
            'estado': f['des_estado_cita'],
            'dias_hasta_cita': int(f['dias_hasta_cita']) if f['dias_hasta_cita'] is not None else None,
        } for f in filas]

    # ----------------------------------------
    # NOTAS CLÍNICAS
    # ----------------------------------------

    def getNotasPaciente(self, id_paciente):
        sql = """
            SELECT
                n.id_nota,
                n.nota_contenido,
                n.nota_fecha,
                pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre
            FROM notas_clinicas n
            JOIN especialistas e ON n.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE n.id_paciente = %s AND n.est_nota = TRUE
            ORDER BY n.nota_fecha DESC
        """
        filas = self.execute_query(sql, (id_paciente,))
        return [{
            'id_nota': f['id_nota'],
            'contenido': f['nota_contenido'],
            'fecha': f['nota_fecha'].strftime('%d/%m/%Y %H:%M') if f['nota_fecha'] else None,
            'especialista': f['especialista_nombre'],
        } for f in filas]

    def guardarNota(self, id_paciente, id_especialista, nota_contenido, usuario_creacion=None):
        sql = """
            INSERT INTO notas_clinicas(id_paciente, id_especialista, nota_contenido, usuario_creacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_nota
        """
        fila = self.execute_query_one(
            sql, (id_paciente, id_especialista, nota_contenido, usuario_creacion), commit=True
        )
        return fila['id_nota'] if fila else None

    def eliminarNota(self, id_nota, usuario_modificacion=None):
        sql = "UPDATE notas_clinicas SET est_nota = FALSE WHERE id_nota = %s"
        return self.execute_query(sql, (id_nota,), commit=True) > 0

    # ----------------------------------------
    # TIMELINE
    # ----------------------------------------

    def getTimeline(self, id_paciente, limite=30):
        sql = """
            SELECT * FROM (
                SELECT
                    'CONSULTA' AS tipo_evento,
                    c.id_consulta AS id_evento,
                    c.consulta_fecha AS fecha_evento,
                    c.consulta_motivo AS descripcion,
                    pe.per_nombre || ' ' || pe.per_apellido AS profesional,
                    c.consulta_estado AS detalle
                FROM consultas c
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE c.id_paciente = %s AND c.est_consulta = TRUE

                UNION ALL

                SELECT
                    'DIAGNOSTICO' AS tipo_evento,
                    rd.id_registro_diagnostico AS id_evento,
                    rd.fecha_creacion AS fecha_evento,
                    d.des_diagnostico AS descripcion,
                    pe.per_nombre || ' ' || pe.per_apellido AS profesional,
                    d.cod_cie10 AS detalle
                FROM registro_diagnosticos rd
                JOIN diagnosticos d ON rd.id_diagnostico = d.id_diagnostico
                JOIN consultas c ON rd.id_consulta = c.id_consulta
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE c.id_paciente = %s AND rd.est_registro_diagnostico = TRUE

                UNION ALL

                SELECT
                    'PROCEDIMIENTO' AS tipo_evento,
                    rp.id_registro_procedimiento AS id_evento,
                    rp.fecha_creacion AS fecha_evento,
                    tp.des_tipo_procedimiento AS descripcion,
                    pe.per_nombre || ' ' || pe.per_apellido AS profesional,
                    rp.registro_resultado AS detalle
                FROM registro_procedimientos rp
                JOIN tipos_procedimientos tp ON rp.id_tipo_procedimiento = tp.id_tipo_procedimiento
                JOIN consultas c ON rp.id_consulta = c.id_consulta
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE c.id_paciente = %s AND rp.est_registro_procedimiento = TRUE

                UNION ALL

                SELECT
                    'TRATAMIENTO' AS tipo_evento,
                    t.id_tratamiento AS id_evento,
                    t.tratamiento_fecha_inicio AS fecha_evento,
                    t.des_tratamiento AS descripcion,
                    pe.per_nombre || ' ' || pe.per_apellido AS profesional,
                    t.tratamiento_estado AS detalle
                FROM tratamientos t
                JOIN consultas c ON t.id_consulta = c.id_consulta
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE c.id_paciente = %s AND t.est_tratamiento = TRUE

                UNION ALL

                SELECT
                    'NOTA' AS tipo_evento,
                    n.id_nota AS id_evento,
                    n.nota_fecha AS fecha_evento,
                    n.nota_contenido AS descripcion,
                    pe.per_nombre || ' ' || pe.per_apellido AS profesional,
                    NULL AS detalle
                FROM notas_clinicas n
                JOIN especialistas e ON n.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                WHERE n.id_paciente = %s AND n.est_nota = TRUE
            ) ev
            ORDER BY fecha_evento DESC NULLS LAST
            LIMIT %s
        """
        filas = self.execute_query(
            sql, (id_paciente, id_paciente, id_paciente, id_paciente, id_paciente, limite)
        )
        return [{
            'tipo_evento': f['tipo_evento'],
            'id_evento': f['id_evento'],
            'fecha': f['fecha_evento'].strftime('%d/%m/%Y %H:%M') if f['fecha_evento'] else None,
            'descripcion': f['descripcion'],
            'profesional': f['profesional'],
            'detalle': f['detalle'],
        } for f in filas]
