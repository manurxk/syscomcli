from app.core.base_dao import BaseDAO


class GeneroDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getGeneros(self):
        sql = "SELECT id_genero, des_genero, est_genero FROM generos ORDER BY id_genero"
        return self.execute_query(sql)

    def getGeneroById(self, genero_id):
        sql = "SELECT id_genero, des_genero, est_genero FROM generos WHERE id_genero = %s"
        return self.execute_query_one(sql, (genero_id,))

    def guardarGenero(self, descripcion, estado):
        sql = """
            INSERT INTO generos (des_genero, est_genero)
            VALUES (%s, %s)
            RETURNING id_genero
        """
        fila = self.execute_query_one(sql, (descripcion, estado))
        return fila["id_genero"] if fila else None

    def updateGenero(self, genero_id, descripcion, estado):
        sql = """
            UPDATE generos
            SET des_genero = %s, est_genero = %s
            WHERE id_genero = %s
        """
        return self.execute_query(sql, (descripcion, estado, genero_id), commit=True) > 0

    def deleteGenero(self, genero_id):
        sql = "DELETE FROM generos WHERE id_genero = %s"
        return self.execute_query(sql, (genero_id,), commit=True) > 0
