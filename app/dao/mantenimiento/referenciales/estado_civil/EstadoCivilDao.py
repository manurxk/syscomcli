from app.core.base_dao import BaseDAO


class EstadoCivilDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEstadosCiviles(self):
        sql = "SELECT id_estado_civil, des_estado_civil, est_estado_civil FROM estados_civiles ORDER BY id_estado_civil"
        return self.execute_query(sql)

    def getEstadoCivilById(self, estado_civil_id):
        sql = "SELECT id_estado_civil, des_estado_civil, est_estado_civil FROM estados_civiles WHERE id_estado_civil = %s"
        return self.execute_query_one(sql, (estado_civil_id,))

    def guardarEstadoCivil(self, descripcion, estado):
        sql = """
            INSERT INTO estados_civiles (des_estado_civil, est_estado_civil)
            VALUES (%s, %s)
            RETURNING id_estado_civil
        """
        fila = self.execute_query_one(sql, (descripcion, estado), commit=True)
        return fila["id_estado_civil"] if fila else None

    def updateEstadoCivil(self, estado_civil_id, descripcion, estado):
        sql = """
            UPDATE estados_civiles
            SET des_estado_civil = %s, est_estado_civil = %s
            WHERE id_estado_civil = %s
        """
        return self.execute_query(sql, (descripcion, estado, estado_civil_id), commit=True) > 0

    def deleteEstadoCivil(self, estado_civil_id):
        sql = "DELETE FROM estados_civiles WHERE id_estado_civil = %s"
        return self.execute_query(sql, (estado_civil_id,), commit=True) > 0
