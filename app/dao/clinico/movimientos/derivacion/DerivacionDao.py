from app.core.base_dao import BaseDAO


class DerivacionDao(BaseDAO):
    """Acceso a datos de las derivaciones a otra especialidad hechas en una consulta, y de su respuesta
    (aceptar / rechazar) por parte del especialista que las recibe."""

    # Una derivación sin especialista la ve todo el que atienda esa especialidad; con especialista, solo él.
    # Nadie ve las que derivó él mismo.
    SQL_ES_PARA_MI = """
        co.id_especialista <> %(yo)s
        AND (d.id_especialista_destino = %(yo)s
             OR (d.id_especialista_destino IS NULL AND EXISTS (
                    SELECT 1 FROM especialista_especialidades ee
                    WHERE ee.id_especialista = %(yo)s AND ee.id_especialidad = d.id_especialidad_destino
                      AND ee.est_especialista_especialidad = TRUE)))"""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        """Lista las derivaciones de la consulta, con su estado y quién las recibió."""
        sql = """
            SELECT d.id_derivacion, d.id_consulta, d.id_especialidad_destino,
                   e.des_especialidad, d.motivo_derivacion, d.derivacion_observaciones,
                   d.estado_derivacion, d.motivo_respuesta, d.id_especialista_destino,
                   p.per_nombre || ' ' || p.per_apellido AS especialista_destino,
                   TO_CHAR(d.fecha_respuesta, 'DD/MM/YYYY HH24:MI') AS fecha_respuesta,
                   d.fecha_creacion
            FROM derivaciones d
            JOIN especialidades e ON d.id_especialidad_destino = e.id_especialidad
            LEFT JOIN especialistas ed ON ed.id_especialista = d.id_especialista_destino
            LEFT JOIN funcionarios fd ON fd.id_funcionario = ed.id_funcionario
            LEFT JOIN personas p ON p.id_persona = fd.id_persona
            WHERE d.id_consulta = %s AND d.est_derivacion = TRUE
            ORDER BY d.id_derivacion
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def getById(self, id_derivacion):
        """Derivación activa con su paciente y el especialista que la hizo; None si no existe."""
        sql = """
            SELECT d.id_derivacion, d.id_especialidad_destino, d.id_especialista_destino, d.estado_derivacion,
                   d.motivo_derivacion, co.id_consulta, co.id_paciente, co.id_especialista AS id_especialista_origen
            FROM derivaciones d
            JOIN consultas co ON co.id_consulta = d.id_consulta
            WHERE d.id_derivacion = %s AND d.est_derivacion = TRUE
        """
        return self.execute_query_one(sql, (id_derivacion,))

    def getEspecialistaDeConsulta(self, id_consulta):
        """id_especialista de la consulta (el que deriva), o None si no existe."""
        fila = self.execute_query_one("SELECT id_especialista FROM consultas WHERE id_consulta = %s", (id_consulta,))
        return fila['id_especialista'] if fila else None

    def getEspecialistasDeEspecialidad(self, id_especialidad):
        """Especialistas activos que atienden la especialidad (para elegir a quién derivar)."""
        sql = """
            SELECT e.id_especialista, p.per_nombre || ' ' || p.per_apellido AS nombre_completo
            FROM especialista_especialidades ee
            JOIN especialistas e ON e.id_especialista = ee.id_especialista AND e.est_especialista = TRUE
            JOIN funcionarios f ON f.id_funcionario = e.id_funcionario AND f.est_funcionario = TRUE
            JOIN personas p ON p.id_persona = f.id_persona
            WHERE ee.id_especialidad = %s AND ee.est_especialista_especialidad = TRUE
            ORDER BY p.per_apellido, p.per_nombre
        """
        return self.execute_query(sql, (id_especialidad,))

    def atiendeEspecialidad(self, id_especialista, id_especialidad):
        """True si el especialista está activo y atiende esa especialidad."""
        sql = """
            SELECT 1 FROM especialista_especialidades ee
            JOIN especialistas e ON e.id_especialista = ee.id_especialista AND e.est_especialista = TRUE
            WHERE ee.id_especialista = %s AND ee.id_especialidad = %s AND ee.est_especialista_especialidad = TRUE
        """
        return self.execute_query_one(sql, (id_especialista, id_especialidad)) is not None

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        """Inserta una derivación (Pendiente) en la consulta y devuelve su id."""
        sql = """
            INSERT INTO derivaciones (
                id_consulta, id_especialidad_destino, id_especialista_destino, motivo_derivacion,
                derivacion_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_derivacion
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_especialidad_destino'],
            datos.get('id_especialista_destino'),
            datos['motivo_derivacion'],
            datos.get('derivacion_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_derivacion'] if fila else None

    def desactivar(self, id_derivacion, usuario_modificacion=None):
        """Da de baja (lógica) la derivación mientras siga Pendiente; devuelve True si modificó una fila."""
        sql = """
            UPDATE derivaciones SET est_derivacion = FALSE, usuario_modificacion = %s
            WHERE id_derivacion = %s AND est_derivacion = TRUE AND estado_derivacion = 'PENDIENTE'
        """
        return self.execute_query(sql, (usuario_modificacion, id_derivacion), commit=True) > 0

    # ------------------------------------------------------------------
    # Mi Agenda: lo que recibe, lo que debe agendar y cómo le respondieron al especialista
    # ------------------------------------------------------------------

    def getRecibidas(self, id_especialista):
        """Derivaciones pendientes de respuesta que le corresponden al especialista."""
        sql = f"""
            SELECT d.id_derivacion, e.des_especialidad, d.motivo_derivacion, d.derivacion_observaciones,
                   d.id_especialista_destino IS NOT NULL AS dirigida_a_mi,
                   TO_CHAR(d.fecha_creacion, 'DD/MM/YYYY HH24:MI') AS fecha,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente,
                   po.per_nombre || ' ' || po.per_apellido AS deriva
            FROM derivaciones d
            JOIN consultas co ON co.id_consulta = d.id_consulta
            JOIN especialidades e ON e.id_especialidad = d.id_especialidad_destino
            JOIN pacientes pa ON pa.id_paciente = co.id_paciente
            JOIN personas pp ON pp.id_persona = pa.id_persona
            JOIN especialistas eo ON eo.id_especialista = co.id_especialista
            JOIN funcionarios fo ON fo.id_funcionario = eo.id_funcionario
            JOIN personas po ON po.id_persona = fo.id_persona
            WHERE d.est_derivacion = TRUE AND d.estado_derivacion = 'PENDIENTE' AND {self.SQL_ES_PARA_MI}
            ORDER BY d.fecha_creacion
        """
        return self.execute_query(sql, {'yo': id_especialista})

    def getAceptadasSinCita(self, id_especialista):
        """Derivaciones que el especialista aceptó y para las que todavía no agendó una cita del paciente
        (ninguna cita abierta o realizada con él creada desde que la aceptó)."""
        sql = """
            SELECT d.id_derivacion, e.des_especialidad, d.motivo_derivacion, co.id_paciente,
                   TO_CHAR(d.fecha_respuesta, 'DD/MM/YYYY HH24:MI') AS fecha_respuesta,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente,
                   po.per_nombre || ' ' || po.per_apellido AS deriva
            FROM derivaciones d
            JOIN consultas co ON co.id_consulta = d.id_consulta
            JOIN especialidades e ON e.id_especialidad = d.id_especialidad_destino
            JOIN pacientes pa ON pa.id_paciente = co.id_paciente
            JOIN personas pp ON pp.id_persona = pa.id_persona
            JOIN especialistas eo ON eo.id_especialista = co.id_especialista
            JOIN funcionarios fo ON fo.id_funcionario = eo.id_funcionario
            JOIN personas po ON po.id_persona = fo.id_persona
            WHERE d.est_derivacion = TRUE AND d.estado_derivacion = 'ACEPTADA' AND d.id_especialista_destino = %(yo)s
              AND NOT EXISTS (
                    SELECT 1 FROM citas c JOIN estados_citas ec ON ec.id_estado_cita = c.id_estado_cita
                    WHERE c.id_paciente = co.id_paciente AND c.id_especialista = %(yo)s AND c.est_cita = TRUE
                      AND ec.cod_estado_cita NOT IN ('CANCELADA', 'AUSENTE') AND c.fecha_creacion >= d.fecha_respuesta)
            ORDER BY d.fecha_respuesta
        """
        return self.execute_query(sql, {'yo': id_especialista})

    def getRespondidasDeMisConsultas(self, id_especialista, dias=7):
        """Derivaciones que hizo el especialista y que respondieron en los últimos días (para que lo vea)."""
        sql = """
            SELECT d.id_derivacion, e.des_especialidad, d.estado_derivacion, d.motivo_respuesta,
                   TO_CHAR(d.fecha_respuesta, 'DD/MM/YYYY HH24:MI') AS fecha_respuesta,
                   pp.per_nombre || ' ' || pp.per_apellido AS paciente,
                   pd.per_nombre || ' ' || pd.per_apellido AS responde
            FROM derivaciones d
            JOIN consultas co ON co.id_consulta = d.id_consulta
            JOIN especialidades e ON e.id_especialidad = d.id_especialidad_destino
            JOIN pacientes pa ON pa.id_paciente = co.id_paciente
            JOIN personas pp ON pp.id_persona = pa.id_persona
            LEFT JOIN usuarios u ON u.id_usuario = d.usuario_respuesta
            LEFT JOIN funcionarios fd ON fd.id_funcionario = u.id_funcionario
            LEFT JOIN personas pd ON pd.id_persona = fd.id_persona
            WHERE d.est_derivacion = TRUE AND d.estado_derivacion <> 'PENDIENTE' AND co.id_especialista = %s
              AND d.fecha_respuesta >= now() - make_interval(days => %s)
            ORDER BY d.fecha_respuesta DESC
        """
        return self.execute_query(sql, (id_especialista, dias))

    def responder(self, id_derivacion, id_especialista, usuario, aceptar, motivo=None):
        """Acepta o rechaza una derivación pendiente. Valida que sea para ese especialista y que siga pendiente
        (el primero que responde se la queda; si la rechaza, queda rechazada para todos). Al aceptar, queda asignada al que aceptó."""

        def _responder(cur):
            cur.execute(
                f"""SELECT d.estado_derivacion FROM derivaciones d
                    JOIN consultas co ON co.id_consulta = d.id_consulta
                    WHERE d.id_derivacion = %(id)s AND d.est_derivacion = TRUE AND {self.SQL_ES_PARA_MI}
                    FOR UPDATE OF d""",
                {'id': id_derivacion, 'yo': id_especialista})
            fila = cur.fetchone()
            if fila is None:
                raise ValueError("No se encontró la derivación.")
            if fila[0] != 'PENDIENTE':
                raise ValueError("Esta derivación ya fue respondida.")
            cur.execute(
                """UPDATE derivaciones
                   SET estado_derivacion = %s, id_especialista_destino = COALESCE(%s, id_especialista_destino), motivo_respuesta = %s,
                       fecha_respuesta = now(), usuario_respuesta = %s, usuario_modificacion = %s
                   WHERE id_derivacion = %s""",
                ('ACEPTADA' if aceptar else 'RECHAZADA', id_especialista if aceptar else None,
                 None if aceptar else motivo, usuario, usuario, id_derivacion))
            return True

        return self.execute_transaction(_responder)
