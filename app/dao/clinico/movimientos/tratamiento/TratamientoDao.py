from app.core.base_dao import BaseDAO
from app.dao.agendamiento.cita.CitaDao import sql_numero_sesion


class TratamientoDao(BaseDAO):
    """Acceso a datos de los tratamientos indicados en una consulta."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        """Lista los tratamientos de la consulta."""
        sql = """
            SELECT t.id_tratamiento, t.id_consulta, t.id_tipo_tratamiento,
                   t.des_tratamiento, t.tratamiento_objetivos, t.numero_sesiones,
                   t.frecuencia_sesiones, t.duracion_sesion,
                   t.tratamiento_fecha_inicio, t.tratamiento_fecha_fin,
                   t.tratamiento_estado, t.tratamiento_observaciones, t.fecha_creacion,
                   tt.des_tipo_tratamiento,
                   (SELECT COUNT(*) FROM citas c
                    JOIN estados_citas ec ON ec.id_estado_cita = c.id_estado_cita
                    WHERE c.id_tratamiento = t.id_tratamiento AND c.est_cita = TRUE
                      AND ec.cod_estado_cita NOT IN ('CANCELADA', 'AUSENTE')) AS sesiones_agendadas
            FROM tratamientos t
            JOIN tipos_tratamientos tt ON t.id_tipo_tratamiento = tt.id_tipo_tratamiento
            WHERE t.id_consulta = %s AND t.est_tratamiento = TRUE
            ORDER BY t.id_tratamiento
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['tratamiento_fecha_inicio'] = f['tratamiento_fecha_inicio'].strftime('%Y-%m-%d') if f['tratamiento_fecha_inicio'] else None
            f['tratamiento_fecha_fin'] = f['tratamiento_fecha_fin'].strftime('%Y-%m-%d') if f['tratamiento_fecha_fin'] else None
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        """Inserta un tratamiento en la consulta y devuelve su id."""
        sql = """
            INSERT INTO tratamientos (
                id_consulta, id_tipo_tratamiento, des_tratamiento, tratamiento_objetivos,
                numero_sesiones, frecuencia_sesiones, duracion_sesion,
                tratamiento_fecha_inicio, tratamiento_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_tratamiento
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_tipo_tratamiento'],
            datos['des_tratamiento'],
            datos.get('tratamiento_objetivos'),
            datos.get('numero_sesiones'),
            datos.get('frecuencia_sesiones'),
            datos.get('duracion_sesion'),
            datos['tratamiento_fecha_inicio'],
            datos.get('tratamiento_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_tratamiento'] if fila else None

    def desactivar(self, id_tratamiento, usuario_modificacion=None):
        """Da de baja (lógica) el tratamiento; devuelve True si modificó una fila."""
        sql = """
            UPDATE tratamientos SET est_tratamiento = FALSE, usuario_modificacion = %s
            WHERE id_tratamiento = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_tratamiento), commit=True) > 0

    # ------------------------------------------------------------------
    # Plan de sesiones: las citas de tipo TRATAMIENTO ligadas al tratamiento (citas.id_tratamiento)
    # ------------------------------------------------------------------

    def getContextoPlan(self, id_tratamiento):
        """Tratamiento activo con su paciente y el especialista que lo indicó (el de la consulta); None si no existe."""
        sql = """
            SELECT t.id_tratamiento, t.numero_sesiones, t.frecuencia_sesiones, t.duracion_sesion,
                   t.des_tratamiento, t.tratamiento_estado, t.id_consulta,
                   tt.des_tipo_tratamiento,
                   co.id_paciente, co.id_especialista,
                   pe.per_nombre AS paciente_nombre, pe.per_apellido AS paciente_apellido
            FROM tratamientos t
            JOIN tipos_tratamientos tt ON tt.id_tipo_tratamiento = t.id_tipo_tratamiento
            JOIN consultas co ON co.id_consulta = t.id_consulta
            JOIN pacientes pa ON pa.id_paciente = co.id_paciente
            JOIN personas pe ON pe.id_persona = pa.id_persona
            WHERE t.id_tratamiento = %s AND t.est_tratamiento = TRUE
        """
        return self.execute_query_one(sql, (id_tratamiento,))

    def getSesionesPlan(self, id_tratamiento):
        """Citas del plan, por fecha. `valida` es False en las canceladas y ausentes (no cuentan en el avance)."""
        sql = f"""
            SELECT c.id_cita, c.id_slot_agenda,
                   TO_CHAR(c.cita_inicio, 'YYYY-MM-DD HH24:MI') AS cita_inicio,
                   TO_CHAR(c.cita_fin, 'YYYY-MM-DD HH24:MI') AS cita_fin,
                   ec.cod_estado_cita, ec.des_estado_cita,
                   {sql_numero_sesion('c')} AS cita_numero_sesion,
                   (ec.cod_estado_cita NOT IN ('CANCELADA', 'AUSENTE')) AS valida
            FROM citas c
            JOIN estados_citas ec ON ec.id_estado_cita = c.id_estado_cita
            WHERE c.id_tratamiento = %s AND c.est_cita = TRUE
            ORDER BY c.cita_inicio
        """
        return self.execute_query(sql, (id_tratamiento,))

    def getSlotsPlan(self, id_especialista, desde, hasta):
        """Turnos del especialista entre dos fechas (con cualquier estado), para validar una tanda propuesta.
        `vencido` usa el mismo margen que CitaDao.crearCita: un turno que empezó hace más de 10 minutos ya no se reserva."""
        sql = """
            SELECT sa.id_slot_agenda, sa.estado_slot,
                   TO_CHAR(sa.slot_inicio, 'YYYY-MM-DD HH24:MI') AS slot_inicio,
                   TO_CHAR(sa.slot_fin, 'YYYY-MM-DD HH24:MI') AS slot_fin,
                   (sa.slot_inicio < (now() AT TIME ZONE 'America/Asuncion') - INTERVAL '10 minutes') AS vencido
            FROM slots_agenda sa
            JOIN agenda_horarios ah ON ah.id_agenda_horario = sa.id_agenda_horario AND ah.est_agenda_horario = TRUE
            WHERE sa.id_especialista = %s
              AND sa.slot_inicio >= %s::date AND sa.slot_inicio < (%s::date + INTERVAL '1 day')
            ORDER BY sa.slot_inicio
        """
        return self.execute_query(sql, (id_especialista, desde, hasta))

    def getEspecialistaDeSlots(self, ids_slots):
        """{id_slot_agenda: id_especialista} de los turnos indicados (los que no existen no aparecen)."""
        if not ids_slots:
            return {}
        filas = self.execute_query(
            "SELECT id_slot_agenda, id_especialista FROM slots_agenda WHERE id_slot_agenda = ANY(%s)", (list(ids_slots),))
        return {f['id_slot_agenda']: f['id_especialista'] for f in filas}

    def getContextoConsulta(self, id_consulta):
        """Paciente y especialista de la consulta, para abrir el plan de un tratamiento nuevo; None si no existe."""
        sql = """
            SELECT co.id_consulta, co.id_especialista, co.id_paciente,
                   pe.per_nombre AS paciente_nombre, pe.per_apellido AS paciente_apellido
            FROM consultas co
            JOIN pacientes pa ON pa.id_paciente = co.id_paciente
            JOIN personas pe ON pe.id_persona = pa.id_persona
            WHERE co.id_consulta = %s AND co.est_consulta = TRUE
        """
        return self.execute_query_one(sql, (id_consulta,))

    def getSesionesFuturas(self, id_tratamiento):
        """Citas del plan que todavía no ocurrieron y siguen abiertas (Agendada o Confirmada)."""
        sql = """
            SELECT c.id_cita, TO_CHAR(c.cita_inicio, 'YYYY-MM-DD HH24:MI') AS cita_inicio
            FROM citas c
            JOIN estados_citas ec ON ec.id_estado_cita = c.id_estado_cita
            WHERE c.id_tratamiento = %s AND c.est_cita = TRUE
              AND ec.cod_estado_cita IN ('AGENDADA', 'CONFIRMADA')
              AND c.cita_inicio > (now() AT TIME ZONE 'America/Asuncion')
            ORDER BY c.cita_inicio
        """
        return self.execute_query(sql, (id_tratamiento,))

    def cambiarEstado(self, id_tratamiento, estado, usuario_modificacion=None):
        """Cambia el estado del tratamiento. Al finalizarlo guarda la fecha de fin (hoy, hora de Asunción);
        al suspenderlo o reactivarlo la deja vacía."""
        sql = """
            UPDATE tratamientos
            SET tratamiento_estado = %s,
                tratamiento_fecha_fin = CASE WHEN %s = 'FINALIZADO' THEN (now() AT TIME ZONE 'America/Asuncion')::date ELSE NULL END,
                usuario_modificacion = %s
            WHERE id_tratamiento = %s
        """
        return self.execute_query(sql, (estado, estado, usuario_modificacion, id_tratamiento), commit=True) > 0
