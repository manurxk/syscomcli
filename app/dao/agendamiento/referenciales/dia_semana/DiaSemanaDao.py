from app.core.base_dao import BaseDAO


class DiaSemanaDao(BaseDAO):
    """Acceso a datos de los días de la semana (catálogo de solo lectura)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getDiasSemana(self):
        """Lista los días de la semana."""
        sql = """
            SELECT id_dia_semana, nro_dia, des_dia, est_dia
            FROM dias_semana
            ORDER BY nro_dia
        """
        return self.execute_query(sql)

    def getDiaSemanaById(self, id_dia_semana):
        """Devuelve el registro de día de la semana por su id, o None si no existe."""
        sql = """
            SELECT id_dia_semana, nro_dia, des_dia, est_dia
            FROM dias_semana
            WHERE id_dia_semana = %s
        """
        return self.execute_query_one(sql, (id_dia_semana,))
