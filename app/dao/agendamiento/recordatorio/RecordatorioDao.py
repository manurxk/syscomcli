from app.core.base_dao import BaseDAO


class RecordatorioDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getRecordatoriosByCita(self, id_cita):
        sql = """
            SELECT id_recordatorio, canal, minutos_antes, est_recordatorio
            FROM recordatorios
            WHERE id_cita = %s
            ORDER BY minutos_antes DESC
        """
        return self.execute_query(sql, (id_cita,))

    def getPendientesEnVentana(self, limite=100):
        """Recordatorios cuya ventana de envío (cita_inicio - minutos_antes) ya se
        alcanzó, de citas todavía no finalizadas. est_recordatorio se usa como flag
        pendiente/enviado (no hay columna enviado_at separada, ver avance_B_diseno_bd_06_07_agendamiento.md)."""
        sql = """
            SELECT r.id_recordatorio, r.id_cita, r.canal, r.minutos_antes,
                   TO_CHAR(c.cita_inicio, 'YYYY-MM-DD') AS cita_fecha,
                   TO_CHAR(c.cita_inicio, 'HH24:MI') AS cita_hora,
                   c.motivo AS cita_motivo,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente_nombre,
                   pp.per_telefono AS paciente_telefono,
                   pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre,
                   esp.des_especialidad
            FROM recordatorios r
            JOIN citas c ON r.id_cita = c.id_cita
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            JOIN pacientes pa ON c.id_paciente = pa.id_paciente
            JOIN personas pp ON pa.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            LEFT JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            WHERE r.est_recordatorio = TRUE
              AND ec.es_final = FALSE
              AND c.cita_inicio - (r.minutos_antes || ' minutes')::INTERVAL <= now()
              AND c.cita_inicio > now()
            ORDER BY c.cita_inicio
            LIMIT %s
        """
        return self.execute_query(sql, (limite,))

    def getRecordatorioConDetalle(self, id_recordatorio):
        """Mismos datos que getPendientesEnVentana pero sin filtro de ventana/estado —
        para el reenvío manual (forzar un envío fuera de la ventana automática)."""
        sql = """
            SELECT r.id_recordatorio, r.id_cita, r.canal, r.minutos_antes, r.est_recordatorio,
                   TO_CHAR(c.cita_inicio, 'YYYY-MM-DD') AS cita_fecha,
                   TO_CHAR(c.cita_inicio, 'HH24:MI') AS cita_hora,
                   c.motivo AS cita_motivo,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente_nombre,
                   pp.per_telefono AS paciente_telefono,
                   pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre,
                   esp.des_especialidad
            FROM recordatorios r
            JOIN citas c ON r.id_cita = c.id_cita
            JOIN pacientes pa ON c.id_paciente = pa.id_paciente
            JOIN personas pp ON pa.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            LEFT JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            WHERE r.id_recordatorio = %s
        """
        return self.execute_query_one(sql, (id_recordatorio,))

    def marcarEnviado(self, id_recordatorio):
        sql = "UPDATE recordatorios SET est_recordatorio = FALSE WHERE id_recordatorio = %s"
        return self.execute_query(sql, (id_recordatorio,), commit=True) > 0
