from app.core.base_dao import BaseDAO


class ConsultaDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getConsultas(self, id_especialista=None, id_paciente=None, estado=None):
        """Lista de consultas con datos de paciente/especialista. Filtros opcionales por query param."""
        sql = """
            SELECT
                c.id_consulta,
                c.id_cita,
                c.id_paciente,
                c.id_especialista,
                c.consulta_fecha,
                c.consulta_motivo,
                c.consulta_estado,
                c.consulta_observaciones,
                c.est_consulta,
                pac.pac_historia_clinica,
                pp.per_nombre || ' ' || pp.per_apellido AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre,
                e.esp_matricula
            FROM consultas c
            JOIN pacientes pac ON c.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE 1 = 1
        """
        params = []
        if id_especialista:
            sql += " AND c.id_especialista = %s"
            params.append(id_especialista)
        if id_paciente:
            sql += " AND c.id_paciente = %s"
            params.append(id_paciente)
        if estado:
            sql += " AND c.consulta_estado = %s"
            params.append(estado)
        sql += " ORDER BY c.consulta_fecha DESC, c.id_consulta DESC"

        filas = self.execute_query(sql, tuple(params))
        return [{
            'id_consulta': f['id_consulta'],
            'id_cita': f['id_cita'],
            'id_paciente': f['id_paciente'],
            'id_especialista': f['id_especialista'],
            'consulta_fecha': f['consulta_fecha'].strftime('%d/%m/%Y %H:%M') if f['consulta_fecha'] else None,
            'consulta_motivo': f['consulta_motivo'],
            'consulta_estado': f['consulta_estado'],
            'consulta_observaciones': f['consulta_observaciones'],
            'activo': f['est_consulta'],
            'historia_clinica': f['pac_historia_clinica'],
            'paciente_nombre': f['paciente_nombre'],
            'paciente_cedula': f['paciente_cedula'],
            'especialista_nombre': f['especialista_nombre'],
            'esp_matricula': f['esp_matricula'],
        } for f in filas]

    def getConsultaById(self, id_consulta):
        """Detalle completo de una consulta para visualización."""
        sql = """
            SELECT
                c.id_consulta,
                c.id_cita,
                c.id_paciente,
                c.id_especialista,
                c.consulta_fecha,
                c.consulta_motivo,
                c.consulta_estado,
                c.des_consulta,
                c.consulta_observaciones,
                c.est_consulta,
                pac.pac_historia_clinica,
                pp.per_nombre AS paciente_nombre,
                pp.per_apellido AS paciente_apellido,
                pp.per_cedula AS paciente_cedula,
                pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre,
                e.esp_matricula
            FROM consultas c
            JOIN pacientes pac ON c.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_consulta = %s
        """
        f = self.execute_query_one(sql, (id_consulta,))
        if not f:
            return None
        return {
            'id_consulta': f['id_consulta'],
            'id_cita': f['id_cita'],
            'id_paciente': f['id_paciente'],
            'id_especialista': f['id_especialista'],
            'consulta_fecha': f['consulta_fecha'].strftime('%d/%m/%Y %H:%M') if f['consulta_fecha'] else None,
            'consulta_motivo': f['consulta_motivo'],
            'consulta_estado': f['consulta_estado'],
            'des_consulta': f['des_consulta'],
            'consulta_observaciones': f['consulta_observaciones'],
            'activo': f['est_consulta'],
            'pac_historia_clinica': f['pac_historia_clinica'],
            'paciente_nombre': f['paciente_nombre'],
            'paciente_apellido': f['paciente_apellido'],
            'paciente_cedula': f['paciente_cedula'],
            'especialista_nombre': f['especialista_nombre'],
            'esp_matricula': f['esp_matricula'],
        }

    def getConsultaParaEditar(self, id_consulta):
        """Detalle con campos crudos (sin formatear) para precargar el formulario de edición."""
        sql = """
            SELECT id_consulta, id_cita, id_paciente, id_especialista, consulta_fecha,
                   consulta_motivo, consulta_estado, des_consulta, consulta_observaciones, est_consulta
            FROM consultas
            WHERE id_consulta = %s
        """
        f = self.execute_query_one(sql, (id_consulta,))
        if not f:
            return None
        f['consulta_fecha'] = f['consulta_fecha'].strftime('%Y-%m-%dT%H:%M') if f['consulta_fecha'] else None
        return f

    def getConsultasPorPaciente(self, id_paciente):
        """Historial de consultas de un paciente (para ficha/anamnesis)."""
        sql = """
            SELECT
                c.id_consulta,
                c.consulta_fecha,
                c.consulta_motivo,
                c.consulta_estado,
                pe.per_nombre || ' ' || pe.per_apellido AS especialista_nombre
            FROM consultas c
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE c.id_paciente = %s AND c.est_consulta = TRUE
            ORDER BY c.consulta_fecha DESC
        """
        filas = self.execute_query(sql, (id_paciente,))
        return [{
            'id_consulta': f['id_consulta'],
            'consulta_fecha': f['consulta_fecha'].strftime('%d/%m/%Y %H:%M') if f['consulta_fecha'] else None,
            'consulta_motivo': f['consulta_motivo'],
            'consulta_estado': f['consulta_estado'],
            'especialista_nombre': f['especialista_nombre'],
        } for f in filas]

    def getConsultaDesdeCita(self, id_cita):
        """Consulta ya registrada para una cita específica (evita duplicar consulta por cita)."""
        sql = "SELECT id_consulta FROM consultas WHERE id_cita = %s AND est_consulta = TRUE"
        f = self.execute_query_one(sql, (id_cita,))
        return self.getConsultaById(f['id_consulta']) if f else None

    def guardarConsulta(self, datos, usuario_creacion=None):
        """Crea una nueva consulta. `datos` trae las claves del formulario (ver consulta_api.py)."""
        sql = """
            INSERT INTO consultas(
                id_cita, id_paciente, id_especialista, consulta_fecha, consulta_motivo,
                consulta_estado, des_consulta, consulta_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_consulta
        """
        fila = self.execute_query_one(sql, (
            datos.get('id_cita'),
            datos['id_paciente'],
            datos['id_especialista'],
            datos['consulta_fecha'],
            datos['consulta_motivo'],
            datos.get('consulta_estado', 'PENDIENTE'),
            datos.get('des_consulta'),
            datos.get('consulta_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_consulta'] if fila else None

    def updateConsulta(self, id_consulta, datos, usuario_modificacion=None):
        """Actualiza una consulta existente. No permite cambiar paciente ni especialista."""
        sql = """
            UPDATE consultas SET
                consulta_fecha = %s,
                consulta_motivo = %s,
                consulta_estado = %s,
                des_consulta = %s,
                consulta_observaciones = %s,
                usuario_modificacion = %s
            WHERE id_consulta = %s
        """
        filas = self.execute_query(sql, (
            datos['consulta_fecha'],
            datos['consulta_motivo'],
            datos['consulta_estado'],
            datos.get('des_consulta'),
            datos.get('consulta_observaciones'),
            usuario_modificacion,
            id_consulta,
        ), commit=True)
        return filas > 0

    def desactivarConsulta(self, id_consulta, usuario_modificacion=None):
        """Soft-delete de una consulta."""
        sql = """
            UPDATE consultas SET est_consulta = FALSE, usuario_modificacion = %s
            WHERE id_consulta = %s
        """
        filas = self.execute_query(sql, (usuario_modificacion, id_consulta), commit=True)
        return filas > 0
