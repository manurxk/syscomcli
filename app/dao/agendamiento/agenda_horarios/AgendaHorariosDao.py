import json
import math
import uuid
from datetime import date, datetime, timedelta

from app.core.base_dao import BaseDAO


class AgendaHorariosDao(BaseDAO):
    """Acceso a datos de los horarios de agenda de los especialistas, sus turnos (slots) y bloqueos."""

    HORIZONTE_DIAS_DEFAULT = 15

    # Un sobreturno es un turno creado a mano (crearSobreturno guarda quién lo creó); los que genera el sistema
    # (_generarSlots) tienen usuario_creacion vacío. No se usa "fuera de la grilla": un turno viejo que queda
    # fuera del horario después de cambiar la agenda no es un sobreturno.
    SQL_ES_SOBRETURNO = "(sa.usuario_creacion IS NOT NULL)"
    # Hora actual de Paraguay (los turnos se guardan en hora local)
    SQL_AHORA = "(now() AT TIME ZONE 'America/Asuncion')"

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getAgendaHorarios(self, id_especialista=None):
        """Lista los horarios de agenda del especialista."""
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
                ah.porcentaje_overbooking,
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
        """Devuelve el horario de agenda por su id, o None si no existe."""
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
                     cupos_totales, modalidad_default, porcentaje_overbooking, fec_desde, fec_hasta,
                     bloqueos, usuario_creacion)
                VALUES (%(id_especialista)s, %(id_sede)s, %(id_consultorio)s,
                        %(id_dia_semana)s, %(hora_inicio)s,
                        %(hora_fin)s, %(duracion_turno_min)s, %(cupos_totales)s,
                        %(modalidad_default)s, %(porcentaje_overbooking)s, %(fec_desde)s, %(fec_hasta)s,
                        %(bloqueos)s::jsonb, %(usuario_creacion)s)
                RETURNING id_agenda_horario
                """,
                {**datos, "porcentaje_overbooking": datos.get("porcentaje_overbooking", 0),
                 # una agenda nueva hereda los bloqueos vigentes de su especialista
                 "bloqueos": json.dumps(self._bloqueosDelEspecialista(cur, datos["id_especialista"])),
                 "usuario_creacion": usuario_creacion},
            )
            id_agenda_horario = cur.fetchone()[0]
            self._generarSlots(cur, id_agenda_horario)
            return id_agenda_horario

        return self.execute_transaction(_crear)

    def actualizarAgendaHorario(self, id_agenda_horario, datos, usuario_modificacion):
        """Actualiza la cabecera y regenera los turnos futuros que no tienen cita (libres, bloqueados u
        obsoletos): la generación vuelve a aplicar los bloqueos. Los turnos RESERVADO no se tocan, aunque
        queden fuera del horario nuevo: getCitasFueraDeAgenda los lista para reprogramarlos.
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
                    porcentaje_overbooking = %(porcentaje_overbooking)s,
                    fec_desde = %(fec_desde)s,
                    fec_hasta = %(fec_hasta)s,
                    usuario_modificacion = %(usuario_modificacion)s
                WHERE id_agenda_horario = %(id_agenda_horario)s
                """,
                {**datos, "porcentaje_overbooking": datos.get("porcentaje_overbooking", 0),
                 "id_agenda_horario": id_agenda_horario, "usuario_modificacion": usuario_modificacion},
            )
            cur.execute(
                f"""
                DELETE FROM slots_agenda
                WHERE id_agenda_horario = %s
                  AND estado_slot IN ('DISPONIBLE', 'BLOQUEADO', 'OBSOLETO')
                  AND slot_inicio >= {self.SQL_AHORA}
                """,
                (id_agenda_horario,),
            )
            self._generarSlots(cur, id_agenda_horario)
            return id_agenda_horario

        return self.execute_transaction(_actualizar)

    def cambiarEstadoAgendaHorario(self, id_agenda_horario, estado, usuario_modificacion):
        """Activa o desactiva la agenda. Al desactivar, sus turnos libres futuros pasan a OBSOLETO (dejan de
        ofrecerse; antes se seguían ofreciendo hasta el fin del horizonte). Al reactivar, se borran los
        OBSOLETO futuros y se regeneran (con los bloqueos vigentes). Las citas reservadas no se tocan:
        getCitasFueraDeAgenda las lista."""

        def _cambiar(cur):
            cur.execute(
                "UPDATE agenda_horarios SET est_agenda_horario = %s, usuario_modificacion = %s WHERE id_agenda_horario = %s",
                (estado, usuario_modificacion, id_agenda_horario),
            )
            if estado:
                cur.execute(
                    f"DELETE FROM slots_agenda WHERE id_agenda_horario = %s AND estado_slot = 'OBSOLETO' AND slot_inicio >= {self.SQL_AHORA}",
                    (id_agenda_horario,),
                )
                self._generarSlots(cur, id_agenda_horario)
            else:
                cur.execute(
                    f"""UPDATE slots_agenda SET estado_slot = 'OBSOLETO', usuario_modificacion = %s
                        WHERE id_agenda_horario = %s AND estado_slot IN ('DISPONIBLE', 'BLOQUEADO')
                          AND slot_inicio >= {self.SQL_AHORA}""",
                    (usuario_modificacion, id_agenda_horario),
                )
            return True

        return self.execute_transaction(_cambiar)

    def getCitasFueraDeAgenda(self, id_agenda_horario, todas=False):
        """Citas futuras (no cerradas) con turno en esta agenda que ya no encajan en ella: otro día, otra hora o
        fuera de su vigencia. Con todas=True, todas sus citas futuras (por ejemplo, al desactivarla)."""
        condicion = "TRUE" if todas else """(EXTRACT(ISODOW FROM sa.slot_inicio) <> ah.id_dia_semana
                    OR sa.slot_inicio::time < ah.hora_inicio OR sa.slot_fin::time > ah.hora_fin
                    OR sa.slot_inicio::date < ah.fec_desde OR (ah.fec_hasta IS NOT NULL AND sa.slot_inicio::date > ah.fec_hasta))"""
        return self.execute_query(f"""
            SELECT c.id_cita, TO_CHAR(sa.slot_inicio, 'DD/MM/YYYY HH24:MI') AS cita_inicio, ec.des_estado_cita,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente
            FROM slots_agenda sa
            JOIN agenda_horarios ah ON ah.id_agenda_horario = sa.id_agenda_horario
            JOIN citas c ON c.id_slot_agenda = sa.id_slot_agenda
            JOIN estados_citas ec ON ec.id_estado_cita = c.id_estado_cita
            JOIN pacientes pa ON pa.id_paciente = c.id_paciente
            JOIN personas pp ON pp.id_persona = pa.id_persona
            WHERE sa.id_agenda_horario = %s AND sa.estado_slot = 'RESERVADO'
              AND sa.slot_inicio >= {self.SQL_AHORA} AND ec.es_final = FALSE
              AND {condicion}
            ORDER BY sa.slot_inicio
        """, (id_agenda_horario,))

    def getSlotsByAgendaHorario(self, id_agenda_horario):
        """Lista los turnos (slots) generados para el horario de agenda."""
        sql = f"""
            SELECT sa.id_slot_agenda,
                   TO_CHAR(sa.slot_inicio, 'YYYY-MM-DD HH24:MI') AS slot_inicio,
                   TO_CHAR(sa.slot_fin, 'YYYY-MM-DD HH24:MI') AS slot_fin,
                   sa.estado_slot, {self.SQL_ES_SOBRETURNO} AS es_sobreturno
            FROM slots_agenda sa
            JOIN agenda_horarios ah ON ah.id_agenda_horario = sa.id_agenda_horario
            WHERE sa.id_agenda_horario = %s
            ORDER BY sa.slot_inicio
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
                   fec_desde, fec_hasta, est_agenda_horario, bloqueos
            FROM agenda_horarios
            WHERE id_agenda_horario = %s
            """,
            (id_agenda_horario,),
        )
        fila = cur.fetchone()
        if fila is None or not fila[9]:
            return 0  # una agenda desactivada no genera turnos

        (id_sede, id_consultorio, id_especialista,
         id_dia_semana, hora_inicio, hora_fin, duracion_turno_min,
         fec_desde, fec_hasta, _activa, bloqueos) = fila
        rangos = [(datetime.fromisoformat(b['desde']), datetime.fromisoformat(b['hasta'])) for b in (bloqueos or [])]

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

        insertados = 0
        for slot_inicio, slot_fin in slots:
            # Un turno que cae en un bloqueo (ausencia, feriado) se crea BLOQUEADO
            estado = 'BLOQUEADO' if any(slot_inicio < hasta and slot_fin > desde for desde, hasta in rangos) else 'DISPONIBLE'
            cur.execute(
                """
                INSERT INTO slots_agenda
                    (id_agenda_horario, id_sede, id_consultorio, id_especialista,
                     slot_inicio, slot_fin, estado_slot)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_agenda_horario, slot_inicio) DO NOTHING
                """,
                (id_agenda_horario, id_sede, id_consultorio, id_especialista,
                 slot_inicio, slot_fin, estado),
            )
            insertados += cur.rowcount
        return insertados

    def getAgendasVigentesActivas(self):
        """Horarios activos cuya vigencia no terminó: los únicos que siguen generando slots.
        Un especialista o funcionario dado de baja deja de generar; si se reactiva, vuelve a generar."""
        sql = """
            SELECT ah.id_agenda_horario
            FROM agenda_horarios ah
            JOIN especialistas e ON ah.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            WHERE ah.est_agenda_horario = TRUE
              AND (ah.fec_hasta IS NULL OR ah.fec_hasta >= CURRENT_DATE)
              AND e.est_especialista = TRUE
              AND f.est_funcionario = TRUE
            ORDER BY ah.id_agenda_horario
        """
        return self.execute_query(sql)

    def extenderSlotsAgenda(self, id_agenda_horario):
        """Completa el horizonte rodante de un horario (tarea diaria). Devuelve slots nuevos."""
        return self.execute_transaction(lambda cur: self._generarSlots(cur, id_agenda_horario))

    # ------------------------------------------------------------------
    # Bloqueos de un especialista (ausencias, feriados): agenda_horarios.bloqueos (JSONB).
    # El bloqueo se graba en todas las agendas del especialista, así la generación de turnos lo aplica
    # también a los días que todavía no se generaron (horizonte de 15 días).
    # ------------------------------------------------------------------

    def _bloqueosDelEspecialista(self, cur, id_especialista):
        """Bloqueos vigentes del especialista (para copiarlos a una agenda nueva)."""
        cur.execute(f"""
            SELECT DISTINCT b FROM agenda_horarios ah, jsonb_array_elements(ah.bloqueos) b
            WHERE ah.id_especialista = %s AND (b->>'hasta')::timestamp >= {self.SQL_AHORA}
        """, (id_especialista,))
        return [fila[0] for fila in cur.fetchall()]

    def getBloqueos(self, id_especialista=None):
        """Bloqueos vigentes o futuros, uno por fila (aunque estén copiados en varias agendas)."""
        return self.execute_query(f"""
            SELECT DISTINCT ON (b->>'id') b->>'id' AS id_bloqueo, ah.id_especialista,
                   p.per_nombre || ' ' || p.per_apellido AS especialista,
                   TO_CHAR((b->>'desde')::timestamp, 'DD/MM/YYYY HH24:MI') AS desde,
                   TO_CHAR((b->>'hasta')::timestamp, 'DD/MM/YYYY HH24:MI') AS hasta,
                   b->>'motivo' AS motivo
            FROM agenda_horarios ah
            CROSS JOIN LATERAL jsonb_array_elements(ah.bloqueos) b
            JOIN especialistas e ON e.id_especialista = ah.id_especialista
            JOIN funcionarios f ON f.id_funcionario = e.id_funcionario
            JOIN personas p ON p.id_persona = f.id_persona
            WHERE (b->>'hasta')::timestamp >= {self.SQL_AHORA}
              AND (%(id_especialista)s IS NULL OR ah.id_especialista = %(id_especialista)s)
            ORDER BY b->>'id'
        """, {"id_especialista": id_especialista})

    def getCitasEnRango(self, id_especialista, desde, hasta):
        """Citas futuras no cerradas del especialista cuyo turno cae en el rango (para reprogramar o cancelar)."""
        return self.execute_query(f"""
            SELECT c.id_cita, TO_CHAR(sa.slot_inicio, 'DD/MM/YYYY HH24:MI') AS cita_inicio, ec.des_estado_cita,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente
            FROM slots_agenda sa
            JOIN citas c ON c.id_slot_agenda = sa.id_slot_agenda
            JOIN estados_citas ec ON ec.id_estado_cita = c.id_estado_cita
            JOIN pacientes pa ON pa.id_paciente = c.id_paciente
            JOIN personas pp ON pp.id_persona = pa.id_persona
            WHERE sa.id_especialista = %s AND sa.estado_slot = 'RESERVADO' AND ec.es_final = FALSE
              AND sa.slot_inicio < %s AND sa.slot_fin > %s AND sa.slot_inicio >= {self.SQL_AHORA}
            ORDER BY sa.slot_inicio
        """, (id_especialista, hasta, desde))

    def bloquearEspecialista(self, id_especialista, desde, hasta, motivo, usuario_modificacion):
        """Bloquea un rango (datetime) en todas las agendas del especialista: lo guarda en bloqueos y pasa a
        BLOQUEADO los turnos libres ya generados del rango. Devuelve (id_bloqueo, citas reservadas en el rango)."""
        bloqueo = {"id": uuid.uuid4().hex[:12], "desde": desde.isoformat(timespec='minutes'),
                   "hasta": hasta.isoformat(timespec='minutes'), "motivo": motivo,
                   "usuario": usuario_modificacion, "fecha": datetime.now().isoformat(timespec='minutes')}

        def _bloquear(cur):
            cur.execute(
                "UPDATE agenda_horarios SET bloqueos = bloqueos || %s::jsonb, usuario_modificacion = %s WHERE id_especialista = %s",
                (json.dumps([bloqueo]), usuario_modificacion, id_especialista),
            )
            if cur.rowcount == 0:
                raise ValueError("El especialista no tiene agendas cargadas.")
            cur.execute(
                f"""UPDATE slots_agenda SET estado_slot = 'BLOQUEADO', usuario_modificacion = %s
                    WHERE id_especialista = %s AND estado_slot = 'DISPONIBLE'
                      AND slot_inicio < %s AND slot_fin > %s AND slot_inicio >= {self.SQL_AHORA}""",
                (usuario_modificacion, id_especialista, hasta, desde),
            )
            return bloqueo["id"]

        id_bloqueo = self.execute_transaction(_bloquear)
        return id_bloqueo, self.getCitasEnRango(id_especialista, desde, hasta)

    def levantarBloqueo(self, id_bloqueo, usuario_modificacion):
        """Quita el bloqueo de todas las agendas donde está y libera sus turnos futuros (salvo los que cubra
        otro bloqueo; en una agenda desactivada quedan OBSOLETO). Devuelve False si no existe."""

        def _levantar(cur):
            cur.execute("""
                SELECT ah.id_agenda_horario, ah.est_agenda_horario, b
                FROM agenda_horarios ah, jsonb_array_elements(ah.bloqueos) b WHERE b->>'id' = %s
            """, (id_bloqueo,))
            filas = cur.fetchall()
            if not filas:
                return False
            for id_agenda, activa, b in filas:
                cur.execute("""
                    UPDATE agenda_horarios
                    SET bloqueos = COALESCE((SELECT jsonb_agg(x) FROM jsonb_array_elements(bloqueos) x
                                             WHERE x->>'id' <> %s), '[]'::jsonb),
                        usuario_modificacion = %s
                    WHERE id_agenda_horario = %s
                    RETURNING bloqueos
                """, (id_bloqueo, usuario_modificacion, id_agenda))
                restantes = cur.fetchone()[0] or []
                cur.execute(
                    f"""UPDATE slots_agenda SET estado_slot = %s, usuario_modificacion = %s
                        WHERE id_agenda_horario = %s AND estado_slot = 'BLOQUEADO'
                          AND slot_inicio < %s AND slot_fin > %s AND slot_inicio >= {self.SQL_AHORA}""",
                    ('DISPONIBLE' if activa else 'OBSOLETO', usuario_modificacion, id_agenda, b['hasta'], b['desde']),
                )
                for r in restantes:  # lo que siga cubierto por otro bloqueo vuelve a BLOQUEADO
                    cur.execute(
                        f"""UPDATE slots_agenda SET estado_slot = 'BLOQUEADO'
                            WHERE id_agenda_horario = %s AND estado_slot IN ('DISPONIBLE', 'OBSOLETO')
                              AND slot_inicio < %s AND slot_fin > %s AND slot_inicio >= {self.SQL_AHORA}""",
                        (id_agenda, r['hasta'], r['desde']),
                    )
            return True

        return self.execute_transaction(_levantar)

    # ------------------------------------------------------------------
    # Sobreturnos: turno extra puntual, con cupo diario según agenda_horarios.porcentaje_overbooking
    # ------------------------------------------------------------------

    def crearSobreturno(self, id_agenda_horario, inicio, usuario_creacion):
        """Crea un turno libre extra en la agenda, el día y la hora indicados (aunque esa hora no esté en la
        grilla), con la duración de la agenda. Valida: agenda activa, día y vigencia de la agenda, hora futura,
        sin bloqueo, cupo diario (porcentaje_overbooking de los turnos del día) y sin repetir la hora de otro turno."""

        def _crear(cur):
            cur.execute("""
                SELECT id_sede, id_consultorio, id_especialista, id_dia_semana, duracion_turno_min, cupos_totales,
                       porcentaje_overbooking, fec_desde, fec_hasta, est_agenda_horario, bloqueos
                FROM agenda_horarios WHERE id_agenda_horario = %s FOR UPDATE
            """, (id_agenda_horario,))
            a = cur.fetchone()
            if a is None:
                raise ValueError("La agenda indicada no existe.")
            (id_sede, id_consultorio, id_especialista, id_dia, duracion, cupos, porcentaje,
             fec_desde, fec_hasta, activa, bloqueos) = a
            fin = inicio + timedelta(minutes=duracion)
            if not activa:
                raise ValueError("La agenda está desactivada.")
            if inicio.isoweekday() != id_dia:
                raise ValueError("Ese día el especialista no atiende en esta agenda.")
            if inicio.date() < fec_desde or (fec_hasta and inicio.date() > fec_hasta):
                raise ValueError("La fecha está fuera de la vigencia de la agenda.")
            cur.execute(f"SELECT %s::timestamp < {self.SQL_AHORA}", (inicio,))
            if cur.fetchone()[0]:
                raise ValueError("El sobreturno tiene que ser en el futuro.")
            for b in (bloqueos or []):
                if inicio < datetime.fromisoformat(b['hasta']) and fin > datetime.fromisoformat(b['desde']):
                    raise ValueError(f"Ese horario está bloqueado ({b['motivo']}).")
            maximo = math.ceil(cupos * porcentaje / 100) if porcentaje else 0
            if maximo == 0:
                raise ValueError("La agenda no permite sobreturnos: configure el % de sobreturnos en la agenda.")
            cur.execute(f"""
                SELECT COUNT(*) FROM slots_agenda sa JOIN agenda_horarios ah ON ah.id_agenda_horario = sa.id_agenda_horario
                WHERE sa.id_agenda_horario = %s AND sa.slot_inicio::date = %s AND sa.estado_slot IN ('DISPONIBLE', 'RESERVADO')
                  AND {self.SQL_ES_SOBRETURNO}
            """, (id_agenda_horario, inicio.date()))
            if cur.fetchone()[0] >= maximo:
                raise ValueError(f"Ya se usaron los {maximo} sobreturno(s) permitidos para ese día.")
            cur.execute("""
                INSERT INTO slots_agenda (id_agenda_horario, id_sede, id_consultorio, id_especialista,
                                          slot_inicio, slot_fin, usuario_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_agenda_horario, slot_inicio) DO NOTHING
                RETURNING id_slot_agenda
            """, (id_agenda_horario, id_sede, id_consultorio, id_especialista, inicio, fin, usuario_creacion))
            fila = cur.fetchone()
            if fila is None:
                raise ValueError("Ya existe un turno a esa hora en esta agenda.")
            return fila[0]

        return self.execute_transaction(_crear)
