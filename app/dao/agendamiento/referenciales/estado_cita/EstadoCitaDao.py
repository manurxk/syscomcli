from app.core.base_dao import BaseDAO


class EstadoCitaDao(BaseDAO):
    """Acceso a datos de los estados de cita (catálogo de solo lectura)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEstadosCitas(self):
        """Lista los estados posibles de una cita."""
        sql = """
            SELECT id_estado_cita, cod_estado_cita, des_estado_cita, orden, es_final, est_estado_cita
            FROM estados_citas
            ORDER BY orden
        """
        return self.execute_query(sql)

    def getEstadoCitaById(self, id_estado_cita):
        """Devuelve el registro de estado de cita por su id, o None si no existe."""
        sql = """
            SELECT id_estado_cita, cod_estado_cita, des_estado_cita, orden, es_final, est_estado_cita
            FROM estados_citas
            WHERE id_estado_cita = %s
        """
        return self.execute_query_one(sql, (id_estado_cita,))

    def getEstadoCitaByCodigo(self, cod_estado_cita):
        """Devuelve el estado de cita por su código, o None si no existe."""
        sql = """
            SELECT id_estado_cita, cod_estado_cita, des_estado_cita, orden, es_final, est_estado_cita
            FROM estados_citas
            WHERE cod_estado_cita = %s
        """
        return self.execute_query_one(sql, (cod_estado_cita,))
