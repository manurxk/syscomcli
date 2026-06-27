from app.core.base_dao import BaseDAO

ESTADOS_VALIDOS = ('PENDIENTE', 'NOTIFICADO', 'ACEPTADO', 'EXPIRADO', 'CANCELADO')


class ListaEsperaDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getListaEspera(self, id_agenda_horario=None):
        sql = """
            SELECT le.id_lista_espera, le.id_agenda_horario, le.id_paciente,
                   le.estado, le.prioridad, le.motivo, le.est_lista_espera,
                   TO_CHAR(le.fecha_creacion, 'DD/MM/YYYY HH24:MI') AS fecha_creacion,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente_nombre,
                   pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre,
                   ds.des_dia,
                   TO_CHAR(ah.hora_inicio, 'HH24:MI') AS hora_inicio,
                   TO_CHAR(ah.hora_fin, 'HH24:MI') AS hora_fin
            FROM lista_espera le
            JOIN pacientes pa ON le.id_paciente = pa.id_paciente
            JOIN personas pp ON pa.id_persona = pp.id_persona
            JOIN agenda_horarios ah ON le.id_agenda_horario = ah.id_agenda_horario
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
            WHERE le.est_lista_espera = TRUE
              AND (%(id_agenda_horario)s IS NULL OR le.id_agenda_horario = %(id_agenda_horario)s)
            ORDER BY le.prioridad DESC, le.fecha_creacion
        """
        return self.execute_query(sql, {"id_agenda_horario": id_agenda_horario})

    def getListaEsperaById(self, id_lista_espera):
        sql = """
            SELECT id_lista_espera, id_agenda_horario, id_paciente, estado,
                   prioridad, motivo, est_lista_espera
            FROM lista_espera
            WHERE id_lista_espera = %s
        """
        return self.execute_query_one(sql, (id_lista_espera,))

    def agregarOReactivar(self, id_agenda_horario, id_paciente, motivo=None, prioridad=0, usuario_creacion=None):
        """Patrón 'buscar y reactivar': UNIQUE(id_agenda_horario, id_paciente) sin
        filtro de soft-delete, así que anotar de nuevo al mismo paciente en la misma
        agenda reactiva la fila existente en PENDIENTE en vez de duplicarla."""
        sql = """
            INSERT INTO lista_espera (id_agenda_horario, id_paciente, motivo, prioridad, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id_agenda_horario, id_paciente) DO UPDATE
            SET estado = 'PENDIENTE', motivo = EXCLUDED.motivo, prioridad = EXCLUDED.prioridad,
                est_lista_espera = TRUE, usuario_modificacion = EXCLUDED.usuario_creacion
            RETURNING id_lista_espera
        """
        fila = self.execute_query_one(
            sql, (id_agenda_horario, id_paciente, motivo, prioridad, usuario_creacion), commit=True
        )
        return fila["id_lista_espera"] if fila else None

    def cambiarEstado(self, id_lista_espera, nuevo_estado, usuario_modificacion=None):
        if nuevo_estado not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Valores permitidos: {ESTADOS_VALIDOS}.")
        sql = """
            UPDATE lista_espera
            SET estado = %s, usuario_modificacion = %s,
                fec_ultima_notificacion = CASE WHEN %s = 'NOTIFICADO' THEN now() ELSE fec_ultima_notificacion END
            WHERE id_lista_espera = %s
        """
        return self.execute_query(
            sql, (nuevo_estado, usuario_modificacion, nuevo_estado, id_lista_espera), commit=True
        ) > 0

    def desactivar(self, id_lista_espera, usuario_modificacion=None):
        sql = "UPDATE lista_espera SET est_lista_espera = FALSE, usuario_modificacion = %s WHERE id_lista_espera = %s"
        return self.execute_query(sql, (usuario_modificacion, id_lista_espera), commit=True) > 0
