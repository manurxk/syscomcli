from app.core.base_dao import BaseDAO

CAMPOS_PEI = [
    'pei_objetivos', 'pei_areas_intervencion', 'pei_estrategias',
    'pei_cronograma_seguimiento', 'pei_estado',
]


class PeiDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPeiActual(self, id_paciente):
        """Versión vigente (es_version_actual=TRUE) del PEI de un paciente."""
        sql = """
            SELECT p.id_pei, p.id_paciente, p.id_especialista, p.nro_version, p.es_version_actual,
                   p.pei_objetivos, p.pei_areas_intervencion, p.pei_estrategias,
                   p.pei_cronograma_seguimiento, p.pei_estado,
                   p.fecha_creacion, p.fecha_modificacion,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente_nombre,
                   pac.pac_historia_clinica,
                   fp.per_nombre || ' ' || fp.per_apellido AS especialista_nombre
            FROM pei p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
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

    def getPeiById(self, id_pei):
        """Una versión puntual del PEI, por su ID."""
        sql = """
            SELECT id_pei, id_paciente, id_especialista, nro_version, es_version_actual,
                   pei_objetivos, pei_areas_intervencion, pei_estrategias,
                   pei_cronograma_seguimiento, pei_estado,
                   fecha_creacion, fecha_modificacion
            FROM pei
            WHERE id_pei = %s
        """
        f = self.execute_query_one(sql, (id_pei,))
        if not f:
            return None
        f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        f['fecha_modificacion'] = f['fecha_modificacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_modificacion'] else None
        return f

    def getHistorialPei(self, id_paciente):
        """Todas las versiones del PEI de un paciente, más reciente primero."""
        sql = """
            SELECT p.id_pei, p.nro_version, p.es_version_actual, p.pei_estado,
                   p.fecha_creacion, p.usuario_creacion,
                   fp.per_nombre || ' ' || fp.per_apellido AS especialista_nombre
            FROM pei p
            JOIN especialistas e ON p.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas fp ON f.id_persona = fp.id_persona
            WHERE p.id_paciente = %s
            ORDER BY p.nro_version DESC
        """
        filas = self.execute_query(sql, (id_paciente,))
        return [{
            'id_pei': f['id_pei'],
            'nro_version': f['nro_version'],
            'es_version_actual': f['es_version_actual'],
            'pei_estado': f['pei_estado'],
            'fecha_creacion': f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None,
            'usuario_creacion': f['usuario_creacion'],
            'especialista_nombre': f['especialista_nombre'],
        } for f in filas]

    def listTodosActuales(self):
        """PEI actual (es_version_actual=TRUE) de todos los pacientes que tienen PEI."""
        sql = """
            SELECT p.id_pei, p.id_paciente, p.id_especialista, p.nro_version, p.pei_estado,
                   p.fecha_creacion,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente_nombre,
                   pac.pac_historia_clinica,
                   fp.per_nombre || ' ' || fp.per_apellido AS especialista_nombre
            FROM pei p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON p.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas fp ON f.id_persona = fp.id_persona
            WHERE p.es_version_actual = TRUE
            ORDER BY pp.per_apellido, pp.per_nombre
        """
        filas = self.execute_query(sql)
        return [{
            'id_pei': f['id_pei'],
            'id_paciente': f['id_paciente'],
            'id_especialista': f['id_especialista'],
            'nro_version': f['nro_version'],
            'pei_estado': f['pei_estado'],
            'fecha_creacion': f['fecha_creacion'].strftime('%d/%m/%Y') if f['fecha_creacion'] else None,
            'paciente_nombre': f['paciente_nombre'],
            'pac_historia_clinica': f['pac_historia_clinica'],
            'especialista_nombre': f['especialista_nombre'],
        } for f in filas]

    def tienePei(self, id_paciente):
        sql = "SELECT 1 FROM pei WHERE id_paciente = %s AND es_version_actual = TRUE"
        return self.execute_query_one(sql, (id_paciente,)) is not None

    def guardarNuevaVersion(self, id_paciente, id_especialista, datos, usuario_creacion=None):
        """
        Inserta una nueva versión del PEI del paciente (nro_version = max+1) y
        desmarca la versión anterior como vigente. Insert-only: nunca se pisa
        contenido clínico ya guardado.
        """
        columnas = ', '.join(CAMPOS_PEI)
        placeholders = ', '.join(['%s'] * len(CAMPOS_PEI))
        valores = tuple(datos.get(c) for c in CAMPOS_PEI)

        def _guardar(cur):
            cur.execute(
                "SELECT COALESCE(MAX(nro_version), 0) FROM pei WHERE id_paciente = %s",
                (id_paciente,)
            )
            nro_version = cur.fetchone()[0] + 1

            cur.execute(
                "UPDATE pei SET es_version_actual = FALSE WHERE id_paciente = %s AND es_version_actual = TRUE",
                (id_paciente,)
            )

            cur.execute(
                f"""
                INSERT INTO pei(
                    id_paciente, id_especialista, nro_version, es_version_actual,
                    {columnas}, usuario_creacion
                ) VALUES (%s, %s, %s, TRUE, {placeholders}, %s)
                RETURNING id_pei
                """,
                (id_paciente, id_especialista, nro_version) + valores + (usuario_creacion,)
            )
            return cur.fetchone()[0]

        return self.execute_transaction(_guardar)
