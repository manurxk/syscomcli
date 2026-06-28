from app.core.base_dao import BaseDAO

CAMPOS_ANAMNESIS = [
    'informante', 'relacion_informante', 'motivo_consulta',
    'antecedentes_familiares_similares', 'antecedentes_patologicos_familiares',
    'componentes_familiares', 'historia_familiar',
    'antecedentes_patologicos_personales', 'historia_problema_actual', 'historia_desarrollo',
    'historia_academica', 'historia_laboral', 'historia_rehabilitacion',
    'medicacion_actual', 'medicacion_psiquiatrica_previa', 'consumo_sustancias',
    'relaciones_interpersonales', 'actividad_fisica', 'patron_sueno', 'patron_alimentacion',
    'actividad_emocional', 'actividad_sexual',
    'impresion_diagnostica', 'plan_trabajo',
    'eval_neuropsicologica', 'eval_psicologica', 'eval_psicopedagogica',
    'eval_fonoaudiologica', 'eval_psicomotora',
    'terapia_individual', 'terapia_familiar', 'terapia_grupal', 'terapia_ocupacional',
    'otra_terapia', 'observaciones', 'indicaciones',
]

CAMPOS_BOOLEANOS_ANAMNESIS = [
    'eval_neuropsicologica', 'eval_psicologica', 'eval_psicopedagogica',
    'eval_fonoaudiologica', 'eval_psicomotora',
    'terapia_individual', 'terapia_familiar', 'terapia_grupal', 'terapia_ocupacional',
]


class AnamnesisDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getAnamnesisActual(self, id_paciente):
        """Versión vigente (es_version_actual=TRUE) de la anamnesis de un paciente."""
        sql = f"""
            SELECT a.id_anamnesis, a.id_paciente, a.nro_version, a.es_version_actual,
                   {', '.join('a.' + c for c in CAMPOS_ANAMNESIS)},
                   a.fecha_creacion, a.fecha_modificacion,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente_nombre,
                   pac.pac_historia_clinica
            FROM anamnesis a
            JOIN pacientes pac ON a.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            WHERE a.id_paciente = %s AND a.es_version_actual = TRUE
        """
        f = self.execute_query_one(sql, (id_paciente,))
        if not f:
            return None
        f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        f['fecha_modificacion'] = f['fecha_modificacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_modificacion'] else None
        return f

    def getAnamnesisById(self, id_anamnesis):
        """Una versión puntual de la anamnesis, por su ID."""
        sql = f"""
            SELECT id_anamnesis, id_paciente, nro_version, es_version_actual,
                   {', '.join(CAMPOS_ANAMNESIS)}, fecha_creacion, fecha_modificacion
            FROM anamnesis
            WHERE id_anamnesis = %s
        """
        f = self.execute_query_one(sql, (id_anamnesis,))
        if not f:
            return None
        f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        f['fecha_modificacion'] = f['fecha_modificacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_modificacion'] else None
        return f

    def getHistorialAnamnesis(self, id_paciente):
        """Todas las versiones de la anamnesis de un paciente, más reciente primero."""
        sql = """
            SELECT id_anamnesis, nro_version, es_version_actual, motivo_consulta,
                   fecha_creacion, usuario_creacion
            FROM anamnesis
            WHERE id_paciente = %s
            ORDER BY nro_version DESC
        """
        filas = self.execute_query(sql, (id_paciente,))
        return [{
            'id_anamnesis': f['id_anamnesis'],
            'nro_version': f['nro_version'],
            'es_version_actual': f['es_version_actual'],
            'motivo_consulta': f['motivo_consulta'],
            'fecha_creacion': f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None,
            'usuario_creacion': f['usuario_creacion'],
        } for f in filas]

    def tieneAnamnesis(self, id_paciente):
        sql = "SELECT 1 FROM anamnesis WHERE id_paciente = %s AND es_version_actual = TRUE"
        return self.execute_query_one(sql, (id_paciente,)) is not None

    def guardarNuevaVersion(self, id_paciente, datos, usuario_creacion=None):
        """
        Inserta una nueva versión de la anamnesis del paciente (nro_version = max+1) y
        desmarca la versión anterior como vigente. Insert-only: nunca se pisa contenido
        clínico ya guardado (ver comentario de la tabla en 08_consulta_anamnesis.sql).
        """
        columnas = ', '.join(CAMPOS_ANAMNESIS)
        placeholders = ', '.join(['%s'] * len(CAMPOS_ANAMNESIS))
        valores = tuple(datos.get(c) for c in CAMPOS_ANAMNESIS)

        def _guardar(cur):
            cur.execute(
                "SELECT COALESCE(MAX(nro_version), 0) FROM anamnesis WHERE id_paciente = %s",
                (id_paciente,)
            )
            nro_version = cur.fetchone()[0] + 1

            cur.execute(
                "UPDATE anamnesis SET es_version_actual = FALSE WHERE id_paciente = %s AND es_version_actual = TRUE",
                (id_paciente,)
            )

            cur.execute(
                f"""
                INSERT INTO anamnesis(
                    id_paciente, nro_version, es_version_actual, {columnas}, usuario_creacion
                ) VALUES (%s, %s, TRUE, {placeholders}, %s)
                RETURNING id_anamnesis
                """,
                (id_paciente, nro_version) + valores + (usuario_creacion,)
            )
            return cur.fetchone()[0]

        return self.execute_transaction(_guardar)
