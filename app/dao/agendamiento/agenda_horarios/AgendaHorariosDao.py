from datetime import date, datetime, timedelta

from app.core.base_dao import BaseDAO


class AgendaHorariosDao(BaseDAO):

    HORIZONTE_DIAS_DEFAULT = 15

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getAgendaHorarios(self, id_especialista=None):
        sql = """
            SELECT
                ah.id_agenda_horario,
                ah.id_especialista,
                p.per_nombre,
                p.per_apellido,
                ah.id_sede,
                s.des_sede,
                ah.id_consultorio,
                c.des_consultorio,
                ah.id_dia_semana,
                ds.des_dia,
                TO_CHAR(ah.hora_inicio, 'HH24:MI') AS hora_inicio,
                TO_CHAR(ah.hora_fin, 'HH24:MI') AS hora_fin,
                ah.duracion_turno_min,
                ah.cupos_totales,
                (SELECT COUNT(*) FROM slots_agenda sa
                 WHERE sa.id_agenda_horario = ah.id_agenda_horario
                   AND sa.estado_slot = 'DISPONIBLE') AS cupos_disponibles,
                ah.modalidad_default,
                TO_CHAR(ah.fec_desde, 'YYYY-MM-DD') AS fec_desde,
                TO_CHAR(ah.fec_hasta, 'YYYY-MM-DD') AS fec_hasta,
                ah.est_agenda_horario
            FROM agenda_horarios ah
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            JOIN sedes s ON ah.id_sede = s.id_sede
            JOIN consultorios c ON ah.id_consultorio = c.id_consultorio
            JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
            WHERE (%(id_especialista)s IS NULL OR ah.id_especialista = %(id_especialista)s)
            ORDER BY ds.nro_dia, ah.hora_inicio
        """
        return self.execute_query(sql, {"id_especialista": id_especialista})

    def getAgendaHorarioById(self, id_agenda_horario):
        sql = """
            SELECT id_agenda_horario, id_especialista, id_sede, id_consultorio,
                   id_dia_semana,
                   TO_CHAR(hora_inicio, 'HH24:MI') AS hora_inicio,
                   TO_CHAR(hora_fin, 'HH24:MI') AS hora_fin,
                   duracion_turno_min, cupos_totales, modalidad_default,
                   porcentaje_overbooking,
                   TO_CHAR(fec_desde, 'YYYY-MM-DD') AS fec_desde,
                   TO_CHAR(fec_hasta, 'YYYY-MM-DD') AS fec_hasta,
                   est_agenda_horario
            FROM agenda_horarios
            WHERE id_agenda_horario = %s
        """
        return self.execute_query_one(sql, (id_agenda_horario,))

    def validarConflictoHorario(self, id_especialista, id_consultorio, id_dia_semana,
                                 hora_inicio, hora_fin, fec_desde, fec_hasta=None,
                                 excluir_id=None):
        """Detecta solapamiento de horario para el mismo especialista o el mismo
        consultorio, en el mismo día de semana y rango de vigencia. La tabla no
        usa un EXCLUDE de BD para esto (ver comentario en agenda_horarios), se
        valida acá antes de insertar/actualizar.
        """
        sql = """
            SELECT 1
            FROM agenda_horarios
            WHERE id_dia_semana = %(id_dia_semana)s
              AND est_agenda_horario = TRUE
              AND (id_especialista = %(id_especialista)s OR id_consultorio = %(id_consultorio)s)
              AND hora_inicio < %(hora_fin)s
              AND hora_fin > %(hora_inicio)s
              AND fec_desde <= COALESCE(%(fec_hasta)s, fec_desde)
              AND (fec_hasta IS NULL OR fec_hasta >= %(fec_desde)s)
              AND (%(excluir_id)s IS NULL OR id_agenda_horario != %(excluir_id)s)
            LIMIT 1
        """
        params = {
            "id_especialista": id_especialista,
            "id_consultorio": id_consultorio,
            "id_dia_semana": id_dia_semana,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "fec_desde": fec_desde,
            "fec_hasta": fec_hasta,
            "excluir_id": excluir_id,
        }
        return self.execute_query_one(sql, params) is not None

    def crearAgendaHorario(self, datos, usuario_creacion):
        """Inserta la cabecera y genera los slots iniciales en una sola transacción."""

        def _crear(cur):
            cur.execute(
                """
                INSERT INTO agenda_horarios
                    (id_especialista, id_sede, id_consultorio,
                     id_dia_semana, hora_inicio, hora_fin, duracion_turno_min,
                     cupos_totales, modalidad_default, fec_desde, fec_hasta,
                     usuario_creacion)
                VALUES (%(id_especialista)s, %(id_sede)s, %(id_consultorio)s,
                        %(id_dia_semana)s, %(hora_inicio)s,
                        %(hora_fin)s, %(duracion_turno_min)s, %(cupos_totales)s,
                        %(modalidad_default)s, %(fec_desde)s, %(fec_hasta)s,
                        %(usuario_creacion)s)
                RETURNING id_agenda_horario
                """,
                {**datos, "usuario_creacion": usuario_creacion},
            )
            id_agenda_horario = cur.fetchone()[0]
            self._generarSlots(cur, id_agenda_horario)
            return id_agenda_horario

        return self.execute_transaction(_crear)

    def actualizarAgendaHorario(self, id_agenda_horario, datos, usuario_modificacion):
        """Actualiza la cabecera y regenera los slots futuros que sigan DISPONIBLE.
        No toca slots RESERVADO/OBSOLETO ya existentes.
        """

        def _actualizar(cur):
            cur.execute(
                """
                UPDATE agenda_horarios
                SET id_sede = %(id_sede)s,
                    id_consultorio = %(id_consultorio)s,
                    id_dia_semana = %(id_dia_semana)s,
                    hora_inicio = %(hora_inicio)s,
                    hora_fin = %(hora_fin)s,
                    duracion_turno_min = %(duracion_turno_min)s,
                    cupos_totales = %(cupos_totales)s,
                    modalidad_default = %(modalidad_default)s,
                    fec_desde = %(fec_desde)s,
                    fec_hasta = %(fec_hasta)s,
                    usuario_modificacion = %(usuario_modificacion)s
                WHERE id_agenda_horario = %(id_agenda_horario)s
                """,
                {**datos, "id_agenda_horario": id_agenda_horario,
                 "usuario_modificacion": usuario_modificacion},
            )
            cur.execute(
                """
                DELETE FROM slots_agenda
                WHERE id_agenda_horario = %s
                  AND estado_slot = 'DISPONIBLE'
                  AND slot_inicio >= (now() AT TIME ZONE 'America/Asuncion')
                """,
                (id_agenda_horario,),
            )
            self._generarSlots(cur, id_agenda_horario)
            return id_agenda_horario

        return self.execute_transaction(_actualizar)

    def cambiarEstadoAgendaHorario(self, id_agenda_horario, estado, usuario_modificacion):
        """Activa/desactiva la cabecera. No borra ni regenera slots: desactivar solo
        detiene la generación de slots futuros (ver comentario de est_agenda_horario en el DDL)."""
        sql = """
            UPDATE agenda_horarios
            SET est_agenda_horario = %s, usuario_modificacion = %s
            WHERE id_agenda_horario = %s
        """
        return self.execute_query(sql, (estado, usuario_modificacion, id_agenda_horario), commit=True)

    def getSlotsByAgendaHorario(self, id_agenda_horario):
        sql = """
            SELECT id_slot_agenda,
                   TO_CHAR(slot_inicio, 'YYYY-MM-DD HH24:MI') AS slot_inicio,
                   TO_CHAR(slot_fin, 'YYYY-MM-DD HH24:MI') AS slot_fin,
                   estado_slot
            FROM slots_agenda
            WHERE id_agenda_horario = %s
            ORDER BY slot_inicio
        """
        return self.execute_query(sql, (id_agenda_horario,))

    def _generarSlots(self, cur, id_agenda_horario, horizonte_dias=HORIZONTE_DIAS_DEFAULT):
        """Calcula y guarda los slots concretos dentro del horizonte rodante.
        Idempotente vía ON CONFLICT DO NOTHING sobre (id_agenda_horario, slot_inicio).
        Recibe el cursor de una transacción ya abierta (no abre conexión propia).
        """
        cur.execute(
            """
            SELECT id_sede, id_consultorio, id_especialista,
                   id_dia_semana, hora_inicio, hora_fin, duracion_turno_min,
                   fec_desde, fec_hasta
            FROM agenda_horarios
            WHERE id_agenda_horario = %s
            """,
            (id_agenda_horario,),
        )
        fila = cur.fetchone()
        if fila is None:
            return

        (id_sede, id_consultorio, id_especialista,
         id_dia_semana, hora_inicio, hora_fin, duracion_turno_min,
         fec_desde, fec_hasta) = fila

        hoy = date.today()
        inicio_horizonte = max(fec_desde, hoy)
        fin_horizonte = inicio_horizonte + timedelta(days=horizonte_dias)
        if fec_hasta:
            fin_horizonte = min(fin_horizonte, fec_hasta)

        slots = []
        dia = inicio_horizonte
        while dia <= fin_horizonte:
            if dia.isoweekday() == id_dia_semana:
                cursor_hora = datetime.combine(dia, hora_inicio)
                fin_dia = datetime.combine(dia, hora_fin)
                paso = timedelta(minutes=duracion_turno_min)
                while cursor_hora + paso <= fin_dia:
                    slots.append((cursor_hora, cursor_hora + paso))
                    cursor_hora += paso
            dia += timedelta(days=1)

        for slot_inicio, slot_fin in slots:
            cur.execute(
                """
                INSERT INTO slots_agenda
                    (id_agenda_horario, id_sede, id_consultorio, id_especialista,
                     slot_inicio, slot_fin)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_agenda_horario, slot_inicio) DO NOTHING
                """,
                (id_agenda_horario, id_sede, id_consultorio, id_especialista,
                 slot_inicio, slot_fin),
            )
