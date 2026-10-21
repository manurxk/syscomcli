import psycopg2.errors

from app.core.base_dao import BaseDAO
from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao


class CitaDao(BaseDAO):

    # Los cambios de estado los valida sp_cambiar_estado_cita (con fn_transicion_cita_valida):
    # mapa de transiciones, correcciones del mismo día y regla del día de la cita.

    # Una cita es "de un día anterior" cuando terminó el día asignado (hora de Asunción)
    """Acceso a datos de las citas y su historial de estados."""

    SQL_ES_PASADA = "c.cita_inicio::date < (now() AT TIME ZONE 'America/Asuncion')::date"
    SQL_ES_FUTURA = "c.cita_inicio::date > (now() AT TIME ZONE 'America/Asuncion')::date"

    # Mismo margen que getSlotsDisponibles: un turno que empezó hace más de 10 minutos ya no se reserva
    SQL_TURNO_VENCIDO = "slot_inicio < (now() AT TIME ZONE 'America/Asuncion') - INTERVAL '10 minutes'"

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def _reservarTurnoDeCita(self, cur, id_cita):
        """Vuelve a reservar el turno de una cita cancelada (al cancelar se liberó y la cita
        quedó sin id_slot_agenda). Falla si el turno ya lo tomó otra cita."""
        cur.execute(
            """
            SELECT sa.id_slot_agenda
            FROM citas c
            JOIN slots_agenda sa ON sa.id_especialista = c.id_especialista AND sa.slot_inicio = c.cita_inicio
            WHERE c.id_cita = %s AND sa.estado_slot = 'DISPONIBLE'
            FOR UPDATE OF sa
            """,
            (id_cita,),
        )
        fila = cur.fetchone()
        if fila is None:
            raise ValueError(
                "El turno de esta cita ya no está libre (lo tomó otra cita o se quitó de la agenda). "
                "Agende una cita nueva."
            )
        cur.execute("UPDATE slots_agenda SET estado_slot = 'RESERVADO' WHERE id_slot_agenda = %s", (fila[0],))
        cur.execute("UPDATE citas SET id_slot_agenda = %s WHERE id_cita = %s", (fila[0], id_cita))

    def _llamarCambioEstado(self, cur, id_cita, cod_estado_nuevo, usuario_modificacion, motivo):
        """CALL sp_cambiar_estado_cita: devuelve (estado anterior, estado nuevo). Los errores de
        regla de la base llegan como ValueError con su mensaje."""
        try:
            cur.execute(
                """
                CALL sp_cambiar_estado_cita(
                    p_id_cita => %s, p_cod_estado_nuevo => %s, p_usuario_modificacion => %s,
                    o_cod_estado_anterior => NULL, o_cod_estado_nuevo => NULL, p_motivo => %s)
                """,
                (id_cita, cod_estado_nuevo, usuario_modificacion, motivo),
            )
        except psycopg2.errors.RaiseException as e:
            raise ValueError(e.diag.message_primary) from e
        return cur.fetchone()

    def validarCambioEstado(self, id_cita, cod_estado_nuevo):
        """Valida sin cambiar nada (ej. antes de crear la consulta en "Iniciar consulta"):
        llama al procedimiento y revierte."""
        con = self._get_conexion()
        cur = con.cursor()
        try:
            self._llamarCambioEstado(cur, id_cita, cod_estado_nuevo, None, None)
        finally:
            con.rollback()
            cur.close()
            con.close()

    def getEspecialistaPorFuncionario(self, id_funcionario):
        """Resuelve el id_especialista del usuario logueado a partir de session['id_funcionario'].
        Reemplaza al helper legacy especialista_helper.py (usaba Conexion() vieja y
        session['id_grupo'], que no existe en el modelo de roles nuevo)."""
        sql = "SELECT id_especialista FROM especialistas WHERE id_funcionario = %s AND est_especialista = TRUE"
        fila = self.execute_query_one(sql, (id_funcionario,))
        return fila['id_especialista'] if fila else None

    def getCitasHoyByEspecialista(self, id_especialista):
        """Citas del día actual para un especialista — usada por la vista 'Mi Agenda'."""
        sql = """
            SELECT c.id_cita, c.id_paciente, pp.per_nombre AS paciente_nombre,
                   pp.per_apellido AS paciente_apellido, pp.per_telefono AS paciente_telefono,
                   p.pac_historia_clinica,
                   TO_CHAR(c.cita_inicio, 'HH24:MI') AS cita_hora_inicio,
                   TO_CHAR(c.cita_fin, 'HH24:MI') AS cita_hora_fin,
                   c.cita_es_primera_vez, c.cita_numero_sesion, c.motivo AS cita_motivo,
                   c.id_estado_cita, ec.cod_estado_cita, ec.des_estado_cita
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.id_especialista = %s AND c.est_cita = TRUE
              AND c.cita_inicio >= CURRENT_DATE AND c.cita_inicio < CURRENT_DATE + INTERVAL '1 day'
            ORDER BY c.cita_inicio
        """
        return self.execute_query(sql, (id_especialista,))

    def getEstadosCitas(self):
        """Lista los estados posibles de una cita."""
        sql = """
            SELECT id_estado_cita, cod_estado_cita, des_estado_cita, orden, es_final
            FROM estados_citas
            WHERE est_estado_cita = TRUE
            ORDER BY orden
        """
        return self.execute_query(sql)

    def getSlotsDisponibles(self, id_especialista=None, id_especialidad=None, desde=None, hasta=None):
        # Solo turnos de agendas activas (una agenda desactivada no ofrece turnos) y marca de sobreturno
        """Lista los turnos libres, filtrados por especialista, especialidad y rango de fechas."""
        sql = f"""
            SELECT sa.id_slot_agenda, sa.id_especialista, sa.id_sede, sa.id_consultorio,
                   TO_CHAR(sa.slot_inicio, 'YYYY-MM-DD HH24:MI') AS slot_inicio,
                   TO_CHAR(sa.slot_fin, 'YYYY-MM-DD HH24:MI') AS slot_fin,
                   {AgendaHorariosDao.SQL_ES_SOBRETURNO} AS es_sobreturno
            FROM slots_agenda sa
            JOIN agenda_horarios ah ON ah.id_agenda_horario = sa.id_agenda_horario AND ah.est_agenda_horario = TRUE
            WHERE sa.estado_slot = 'DISPONIBLE'
              AND sa.slot_inicio >= (now() AT TIME ZONE 'America/Asuncion') - INTERVAL '10 minutes'
              AND (%(id_especialista)s IS NULL OR sa.id_especialista = %(id_especialista)s)
              AND (%(desde)s IS NULL OR sa.slot_inicio >= %(desde)s::DATE)
              AND (%(hasta)s IS NULL OR sa.slot_inicio < (%(hasta)s::DATE + INTERVAL '1 day'))
              AND (
                    %(id_especialidad)s IS NULL
                    OR EXISTS (
                        SELECT 1 FROM especialista_especialidades ee
                        WHERE ee.id_especialista = sa.id_especialista
                          AND ee.id_especialidad = %(id_especialidad)s
                          AND ee.est_especialista_especialidad = TRUE
                    )
                  )
            ORDER BY sa.slot_inicio
        """
        params = {
            "id_especialista": id_especialista,
            "id_especialidad": id_especialidad,
            "desde": desde,
            "hasta": hasta,
        }
        return self.execute_query(sql, params)

    def getCitas(self, id_especialista=None, id_paciente=None, desde=None, hasta=None):
        """Lista las citas, con filtros opcionales por especialista, paciente y rango de fechas."""
        sql = f"""
            SELECT c.id_cita, c.id_paciente, pp.per_nombre AS paciente_nombre,
                   pp.per_apellido AS paciente_apellido, p.pac_historia_clinica,
                   c.id_especialista, pe.per_nombre AS especialista_nombre,
                   pe.per_apellido AS especialista_apellido,
                   c.id_especialidad, esp.des_especialidad,
                   c.id_sede, s.des_sede, c.id_consultorio, co.des_consultorio,
                   TO_CHAR(c.cita_inicio, 'YYYY-MM-DD HH24:MI') AS cita_inicio,
                   TO_CHAR(c.cita_fin, 'YYYY-MM-DD HH24:MI') AS cita_fin,
                   c.modalidad, c.cita_es_primera_vez, c.cita_numero_sesion,
                   c.motivo, c.observaciones,
                   c.id_estado_cita, ec.cod_estado_cita, ec.des_estado_cita,
                   {self.SQL_ES_PASADA} AS es_pasada, {self.SQL_ES_FUTURA} AS es_futura,
                   (SELECT COUNT(*) FROM recordatorios r WHERE r.id_cita = c.id_cita) AS recordatorios_total,
                   (SELECT COUNT(*) FROM recordatorios r WHERE r.id_cita = c.id_cita AND r.est_recordatorio = TRUE) AS recordatorios_pendientes
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            LEFT JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN sedes s ON c.id_sede = s.id_sede
            JOIN consultorios co ON c.id_consultorio = co.id_consultorio
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.est_cita = TRUE
              AND (%(id_especialista)s IS NULL OR c.id_especialista = %(id_especialista)s)
              AND (%(id_paciente)s IS NULL OR c.id_paciente = %(id_paciente)s)
              AND (%(desde)s IS NULL OR c.cita_inicio >= %(desde)s)
              AND (%(hasta)s IS NULL OR c.cita_inicio <= %(hasta)s)
            ORDER BY c.cita_inicio
        """
        params = {
            "id_especialista": id_especialista,
            "id_paciente": id_paciente,
            "desde": desde,
            "hasta": hasta,
        }
        return self.execute_query(sql, params)

    def getCitaById(self, id_cita):
        """Devuelve la cita por su id, o None si no existe."""
        sql = """
            SELECT c.id_cita, c.id_paciente, pp.per_nombre AS paciente_nombre,
                   pp.per_apellido AS paciente_apellido, p.pac_historia_clinica,
                   c.id_especialista, pe.per_nombre AS especialista_nombre,
                   pe.per_apellido AS especialista_apellido,
                   c.id_especialidad, esp.des_especialidad,
                   c.id_sede, s.des_sede, c.id_consultorio, co.des_consultorio,
                   c.id_slot_agenda,
                   TO_CHAR(c.cita_inicio, 'YYYY-MM-DD HH24:MI') AS cita_inicio,
                   TO_CHAR(c.cita_fin, 'YYYY-MM-DD HH24:MI') AS cita_fin,
                   c.modalidad, c.cita_es_primera_vez, c.cita_numero_sesion,
                   c.motivo, c.observaciones, c.motivo_cancelacion,
                   c.id_estado_cita, ec.cod_estado_cita, ec.des_estado_cita
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            LEFT JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN sedes s ON c.id_sede = s.id_sede
            JOIN consultorios co ON c.id_consultorio = co.id_consultorio
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.id_cita = %s
        """
        return self.execute_query_one(sql, (id_cita,))

    def crearCita(self, datos, usuario_creacion):
        """Reserva un slot disponible y crea la cita en una sola transacción.

        El slot ya determina especialista/sede/consultorio/horario; usa
        SELECT...FOR UPDATE para evitar que dos solicitudes reserven el mismo
        slot en una carrera (mismo criterio que el comentario de slots_agenda).
        """

        def _crear(cur):
            cur.execute(
                f"""
                SELECT id_slot_agenda, id_sede, id_consultorio, id_especialista,
                       slot_inicio, slot_fin, estado_slot, {self.SQL_TURNO_VENCIDO} AS vencido
                FROM slots_agenda
                WHERE id_slot_agenda = %s
                FOR UPDATE
                """,
                (datos["id_slot_agenda"],),
            )
            slot = cur.fetchone()
            if slot is None:
                raise ValueError("El slot indicado no existe")

            (id_slot_agenda, id_sede, id_consultorio, id_especialista,
             slot_inicio, slot_fin, estado_slot, vencido) = slot

            if estado_slot != "DISPONIBLE":
                raise ValueError("El slot ya no está disponible")
            if vencido:
                raise ValueError("El turno seleccionado ya pasó; elija un turno futuro")

            id_especialidad = datos.get("id_especialidad")
            if id_especialidad:
                cur.execute(
                    """
                    SELECT 1 FROM especialista_especialidades
                    WHERE id_especialista = %s AND id_especialidad = %s
                      AND est_especialista_especialidad = TRUE
                    """,
                    (id_especialista, id_especialidad),
                )
                if cur.fetchone() is None:
                    raise ValueError("El especialista no tiene esa especialidad")

            cur.execute(
                "SELECT id_estado_cita FROM estados_citas WHERE cod_estado_cita = 'AGENDADA'"
            )
            id_estado_inicial = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO citas (
                    id_paciente, id_especialista, id_especialidad, id_sede, id_consultorio,
                    id_slot_agenda, id_estado_cita, cita_inicio, cita_fin, modalidad,
                    cita_es_primera_vez, cita_numero_sesion, motivo, observaciones,
                    usuario_creacion
                )
                VALUES (
                    %(id_paciente)s, %(id_especialista)s, %(id_especialidad)s, %(id_sede)s,
                    %(id_consultorio)s, %(id_slot_agenda)s, %(id_estado_inicial)s,
                    %(cita_inicio)s, %(cita_fin)s, %(modalidad)s, %(cita_es_primera_vez)s,
                    %(cita_numero_sesion)s, %(motivo)s, %(observaciones)s, %(usuario_creacion)s
                )
                RETURNING id_cita
                """,
                {
                    "id_paciente": datos["id_paciente"],
                    "id_especialista": id_especialista,
                    "id_especialidad": id_especialidad,
                    "id_sede": id_sede,
                    "id_consultorio": id_consultorio,
                    "id_slot_agenda": id_slot_agenda,
                    "id_estado_inicial": id_estado_inicial,
                    "cita_inicio": slot_inicio,
                    "cita_fin": slot_fin,
                    "modalidad": datos.get("modalidad", "PRESENCIAL"),
                    "cita_es_primera_vez": datos.get("cita_es_primera_vez", True),
                    "cita_numero_sesion": datos.get("cita_numero_sesion"),
                    "motivo": datos.get("motivo"),
                    "observaciones": datos.get("observaciones"),
                    "usuario_creacion": usuario_creacion,
                },
            )
            id_cita = cur.fetchone()[0]

            cur.execute(
                "UPDATE slots_agenda SET estado_slot = 'RESERVADO' WHERE id_slot_agenda = %s",
                (id_slot_agenda,),
            )

            cur.execute(
                """
                INSERT INTO citas_log_estados
                    (id_cita, id_estado_anterior, id_estado_nuevo, motivo_cambio, usuario_cambio)
                VALUES (%s, NULL, %s, 'Creación de cita', %s)
                """,
                (id_cita, id_estado_inicial, usuario_creacion),
            )

            return id_cita

        return self.execute_transaction(_crear)

    def getLogEstados(self, id_cita):
        """Devuelve el historial de cambios de estado de la cita."""
        sql = """
            SELECT l.id_cita_log_estado,
                   ea.des_estado_cita AS estado_anterior,
                   en.des_estado_cita AS estado_nuevo,
                   l.motivo_cambio,
                   u.usu_nick AS usuario,
                   TO_CHAR(l.fecha_cambio, 'DD/MM/YYYY HH24:MI') AS fecha_cambio
            FROM citas_log_estados l
            LEFT JOIN estados_citas ea ON l.id_estado_anterior = ea.id_estado_cita
            JOIN estados_citas en ON l.id_estado_nuevo = en.id_estado_cita
            LEFT JOIN usuarios u ON l.usuario_cambio = u.id_usuario
            WHERE l.id_cita = %s
            ORDER BY l.fecha_cambio
        """
        return self.execute_query(sql, (id_cita,))

    def actualizarCita(self, id_cita, datos, usuario_modificacion):
        """Edita una cita existente. Paciente y especialista quedan fijos (decisión de
        diseño documentada en el COMMENT ON TABLE citas de 07_agenda_citas.sql); si
        datos['id_slot_agenda'] difiere del slot actual, reprograma: libera el slot
        viejo y reserva el nuevo dentro de la misma transacción."""

        def _actualizar(cur):
            cur.execute(
                """
                SELECT c.id_estado_cita, c.id_slot_agenda, c.id_especialista,
                       ec.cod_estado_cita, ec.es_final
                FROM citas c
                JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                WHERE c.id_cita = %s
                FOR UPDATE OF c
                """,
                (id_cita,),
            )
            fila = cur.fetchone()
            if fila is None:
                raise ValueError("La cita indicada no existe")
            id_estado_actual, id_slot_actual, id_especialista, cod_estado_actual, es_final = fila

            if es_final:
                raise ValueError(f"No se puede editar una cita en estado '{cod_estado_actual}'")

            id_slot_nuevo = datos.get("id_slot_agenda")
            reprogramada = bool(id_slot_nuevo) and id_slot_nuevo != id_slot_actual

            if reprogramada:
                cur.execute(
                    f"""
                    SELECT id_slot_agenda, id_sede, id_consultorio, id_especialista,
                           slot_inicio, slot_fin, estado_slot, {self.SQL_TURNO_VENCIDO} AS vencido
                    FROM slots_agenda
                    WHERE id_slot_agenda = %s
                    FOR UPDATE
                    """,
                    (id_slot_nuevo,),
                )
                slot = cur.fetchone()
                if slot is None:
                    raise ValueError("El turno indicado no existe")
                (_, id_sede, id_consultorio, id_especialista_slot,
                 slot_inicio, slot_fin, estado_slot, vencido) = slot

                if estado_slot != "DISPONIBLE":
                    raise ValueError("El turno seleccionado ya no está disponible")
                if vencido:
                    raise ValueError("El turno seleccionado ya pasó; elija un turno futuro")
                if id_especialista_slot != id_especialista:
                    raise ValueError("El turno seleccionado no corresponde al especialista de la cita")

                if id_slot_actual:
                    cur.execute(
                        "UPDATE slots_agenda SET estado_slot = 'DISPONIBLE' WHERE id_slot_agenda = %s AND estado_slot = 'RESERVADO'",
                        (id_slot_actual,),
                    )
                cur.execute(
                    "UPDATE slots_agenda SET estado_slot = 'RESERVADO' WHERE id_slot_agenda = %s",
                    (id_slot_nuevo,),
                )
                cur.execute(
                    """
                    UPDATE citas
                    SET id_slot_agenda = %s, id_sede = %s, id_consultorio = %s,
                        cita_inicio = %s, cita_fin = %s
                    WHERE id_cita = %s
                    """,
                    (id_slot_nuevo, id_sede, id_consultorio, slot_inicio, slot_fin, id_cita),
                )
                cur.execute(
                    """
                    INSERT INTO citas_log_estados
                        (id_cita, id_estado_anterior, id_estado_nuevo, motivo_cambio, usuario_cambio)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_cita, id_estado_actual, id_estado_actual, "Cita reprogramada", usuario_modificacion),
                )

            cur.execute(
                """
                UPDATE citas
                SET id_especialidad = %s, modalidad = %s, cita_es_primera_vez = %s,
                    cita_numero_sesion = %s, motivo = %s, observaciones = %s,
                    usuario_modificacion = %s
                WHERE id_cita = %s
                """,
                (
                    datos.get("id_especialidad"),
                    datos.get("modalidad", "PRESENCIAL"),
                    datos.get("cita_es_primera_vez", True),
                    datos.get("cita_numero_sesion"),
                    datos.get("motivo"),
                    datos.get("observaciones"),
                    usuario_modificacion,
                    id_cita,
                ),
            )
            return True

        return self.execute_transaction(_actualizar)

    def cambiarEstadoCita(self, id_cita, cod_estado_nuevo, usuario_modificacion, motivo=None):
        """Cambia el estado de una cita con sp_cambiar_estado_cita: valida la transición, libera o
        vuelve a reservar el turno, finaliza la consulta al completar, crea los recordatorios al
        confirmar y deja el cambio en citas_log_estados, todo en la misma transacción."""
        return self.execute_transaction(
            lambda cur: bool(self._llamarCambioEstado(cur, id_cita, cod_estado_nuevo, usuario_modificacion, motivo))
        )


    CAMPOS_CORREGIBLES = ('motivo', 'observaciones', 'id_especialidad', 'modalidad')

    def corregirCita(self, id_cita, cod_estado_nuevo, datos, motivo_correccion, usuario_modificacion,
                     autorizador):
        """Corrección extraordinaria de una cita cerrada (Completada, Ausente, Cancelada) o de
        un día anterior, con autorización de un administrador (decisión del usuario 2026-10-13).

        Puede cambiar el estado sin seguir TRANSICIONES y los datos administrativos
        (CAMPOS_CORREGIBLES). NO toca el contenido clínico de la consulta. Queda en el
        historial de la cita con el motivo y quién autorizó; la auditoría la registra la ruta.
        autorizador: {'id_usuario', 'usu_nick'} (ver AuthService.verificar_autorizacion_administrador).
        """
        if not (motivo_correccion or '').strip():
            raise ValueError("El motivo de la corrección es obligatorio.")
        datos = {k: v for k, v in (datos or {}).items() if k in self.CAMPOS_CORREGIBLES and v not in (None, '')}

        def _corregir(cur):
            cur.execute(
                f"""
                SELECT c.id_estado_cita, c.id_slot_agenda, ec.cod_estado_cita, ec.es_final,
                       {self.SQL_ES_PASADA} AS es_pasada
                FROM citas c
                JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                WHERE c.id_cita = %s
                FOR UPDATE OF c
                """,
                (id_cita,),
            )
            fila = cur.fetchone()
            if fila is None:
                raise ValueError("La cita indicada no existe")
            id_estado_anterior, id_slot_agenda, cod_anterior, es_final, es_pasada = fila
            if not es_final and not es_pasada:
                raise ValueError("La cita sigue abierta: use las acciones normales (Editar o cambiar estado).")

            id_estado_nuevo = id_estado_anterior
            cambia_estado = bool(cod_estado_nuevo) and cod_estado_nuevo != cod_anterior
            if cambia_estado:
                if cod_estado_nuevo == "EN_CONSULTA":
                    raise ValueError("'En consulta' se registra con 'Iniciar consulta', no con una corrección.")
                cur.execute(
                    "SELECT id_estado_cita FROM estados_citas WHERE cod_estado_cita = %s AND est_estado_cita = TRUE",
                    (cod_estado_nuevo,),
                )
                estado_row = cur.fetchone()
                if estado_row is None:
                    raise ValueError(f"Estado '{cod_estado_nuevo}' no encontrado")
                id_estado_nuevo = estado_row[0]

                if cod_anterior == "CANCELADA":
                    self._reservarTurnoDeCita(cur, id_cita)
                if cod_estado_nuevo == "CANCELADA" and id_slot_agenda:
                    cur.execute(
                        "UPDATE slots_agenda SET estado_slot = 'DISPONIBLE' WHERE id_slot_agenda = %s AND estado_slot = 'RESERVADO'",
                        (id_slot_agenda,),
                    )
                    cur.execute("UPDATE citas SET id_slot_agenda = NULL WHERE id_cita = %s", (id_cita,))
                if cod_estado_nuevo == "COMPLETADA":
                    cur.execute(
                        """
                        UPDATE consultas SET consulta_estado = 'FINALIZADA', usuario_modificacion = %s
                        WHERE id_cita = %s AND consulta_estado != 'FINALIZADA'
                        """,
                        (usuario_modificacion, id_cita),
                    )
            elif not datos:
                raise ValueError("No hay cambios para guardar.")

            cur.execute(
                """
                UPDATE citas
                SET id_estado_cita = %s,
                    motivo = COALESCE(%s, motivo),
                    observaciones = COALESCE(%s, observaciones),
                    id_especialidad = COALESCE(%s, id_especialidad),
                    modalidad = COALESCE(%s, modalidad),
                    motivo_cancelacion = CASE WHEN %s = 'CANCELADA' THEN %s ELSE motivo_cancelacion END,
                    usuario_modificacion = %s
                WHERE id_cita = %s
                """,
                (id_estado_nuevo, datos.get('motivo'), datos.get('observaciones'), datos.get('id_especialidad'),
                 datos.get('modalidad'), cod_estado_nuevo if cambia_estado else None, motivo_correccion,
                 usuario_modificacion, id_cita),
            )

            detalle = f"Corrección autorizada por {autorizador['usu_nick']}: {motivo_correccion.strip()}"
            if datos:
                detalle += f" (datos corregidos: {', '.join(sorted(datos))})"
            cur.execute(
                """
                INSERT INTO citas_log_estados
                    (id_cita, id_estado_anterior, id_estado_nuevo, motivo_cambio, usuario_cambio)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_cita, id_estado_anterior, id_estado_nuevo, detalle, usuario_modificacion),
            )
            return {'cod_estado_anterior': cod_anterior,
                    'cod_estado_nuevo': cod_estado_nuevo if cambia_estado else cod_anterior,
                    'campos': sorted(datos), 'detalle': detalle}

        return self.execute_transaction(_corregir)
