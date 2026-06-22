from app.core.base_dao import BaseDAO


class ProfesionDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getProfesiones(self):
        sql = "SELECT id_profesion, des_profesion, est_profesion FROM profesiones ORDER BY id_profesion"
        return self.execute_query(sql)

    def getProfesionById(self, profesion_id):
        sql = "SELECT id_profesion, des_profesion, est_profesion FROM profesiones WHERE id_profesion = %s"
        return self.execute_query_one(sql, (profesion_id,))

    def guardarProfesion(self, descripcion, estado):
        sql = """
            INSERT INTO profesiones (des_profesion, est_profesion)
            VALUES (%s, %s)
            RETURNING id_profesion
        """
        fila = self.execute_query_one(sql, (descripcion, estado), commit=True)
        return fila["id_profesion"] if fila else None

    def updateProfesion(self, profesion_id, descripcion, estado):
        sql = """
            UPDATE profesiones
            SET des_profesion = %s, est_profesion = %s
            WHERE id_profesion = %s
        """
        return self.execute_query(sql, (descripcion, estado, profesion_id), commit=True) > 0

    def deleteProfesion(self, profesion_id):
        sql = "DELETE FROM profesiones WHERE id_profesion = %s"
        return self.execute_query(sql, (profesion_id,), commit=True) > 0
