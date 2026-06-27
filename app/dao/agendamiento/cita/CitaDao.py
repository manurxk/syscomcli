from app.core.base_dao import BaseDAO


class CitaDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEstadosCitas(self):
        sql = """
            SELECT id_estado_cita, cod_estado_cita, des_estado_cita, orden, es_final
            FROM estados_citas
            WHERE est_estado_cita = TRUE
            ORDER BY orden
        """
        return self.execute_query(sql)

    def getSlotsDisponibles(self, id_especialista=None, id_especialidad=None, desde=None, hasta=None):
        sql = """
            SELECT sa.id_slot_agenda, sa.id_especialista, sa.id_sede, sa.id_consultorio,
                   TO_CHAR(sa.slot_inicio, 'YYYY-MM-DD HH24:MI') AS slot_inicio,
                   TO_CHAR(sa.slot_fin, 'YYYY-MM-DD HH24:MI') AS slot_fin
            FROM slots_agenda sa
            WHERE sa.estado_slot = 'DISPONIBLE'
              AND sa.slot_inicio >= now()
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
        sql = """
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
                """
                SELECT id_slot_agenda, id_sede, id_consultorio, id_especialista,
                       slot_inicio, slot_fin, estado_slot
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
             slot_inicio, slot_fin, estado_slot) = slot

            if estado_slot != "DISPONIBLE":
                raise ValueError("El slot ya no está disponible")

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
                    """
                    SELECT id_slot_agenda, id_sede, id_consultorio, id_especialista,
                           slot_inicio, slot_fin, estado_slot
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
                 slot_inicio, slot_fin, estado_slot) = slot

                if estado_slot != "DISPONIBLE":
                    raise ValueError("El turno seleccionado ya no está disponible")
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
        """Cambia el estado de una cita. Si el nuevo estado es CANCELADA, libera
        el slot reservado para que vuelva a estar disponible."""

        def _cambiar(cur):
            cur.execute(
                "SELECT id_estado_cita, id_slot_agenda FROM citas WHERE id_cita = %s FOR UPDATE",
                (id_cita,),
            )
            fila = cur.fetchone()
            if fila is None:
                raise ValueError("La cita indicada no existe")
            id_estado_anterior, id_slot_agenda = fila

            cur.execute(
                "SELECT id_estado_cita FROM estados_citas WHERE cod_estado_cita = %s AND est_estado_cita = TRUE",
                (cod_estado_nuevo,),
            )
            estado_row = cur.fetchone()
            if estado_row is None:
                raise ValueError(f"Estado '{cod_estado_nuevo}' no encontrado")
            id_estado_nuevo = estado_row[0]

            cur.execute(
                """
                UPDATE citas
                SET id_estado_cita = %s, usuario_modificacion = %s,
                    motivo_cancelacion = CASE WHEN %s = 'CANCELADA' THEN %s ELSE motivo_cancelacion END
                WHERE id_cita = %s
                """,
                (id_estado_nuevo, usuario_modificacion, cod_estado_nuevo, motivo, id_cita),
            )

            if cod_estado_nuevo == "CANCELADA" and id_slot_agenda:
                cur.execute(
                    "UPDATE slots_agenda SET estado_slot = 'DISPONIBLE' WHERE id_slot_agenda = %s AND estado_slot = 'RESERVADO'",
                    (id_slot_agenda,),
                )
                cur.execute(
                    "UPDATE citas SET id_slot_agenda = NULL WHERE id_cita = %s",
                    (id_cita,),
                )

            if cod_estado_nuevo == "CONFIRMADA":
                cur.execute(
                    """
                    INSERT INTO recordatorios (id_cita, canal, minutos_antes, usuario_creacion)
                    VALUES (%(id_cita)s, 'WHATSAPP', 1440, %(usuario)s),
                           (%(id_cita)s, 'WHATSAPP', 120, %(usuario)s)
                    ON CONFLICT (id_cita, canal, minutos_antes) DO NOTHING
                    """,
                    {"id_cita": id_cita, "usuario": usuario_modificacion},
                )

            cur.execute(
                """
                INSERT INTO citas_log_estados
                    (id_cita, id_estado_anterior, id_estado_nuevo, motivo_cambio, usuario_cambio)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_cita, id_estado_anterior, id_estado_nuevo, motivo, usuario_modificacion),
            )

            return True

        return self.execute_transaction(_cambiar)
