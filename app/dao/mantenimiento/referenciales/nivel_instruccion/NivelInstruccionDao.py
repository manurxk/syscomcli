from app.core.base_dao import BaseDAO


class NivelInstruccionDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getNivelesInstruccion(self):
        sql = "SELECT id_nivel_instruccion, des_nivel_instruccion, est_nivel_instruccion FROM niveles_instruccion ORDER BY id_nivel_instruccion"
        return self.execute_query(sql)

    def getNivelInstruccionById(self, nivel_instruccion_id):
        sql = "SELECT id_nivel_instruccion, des_nivel_instruccion, est_nivel_instruccion FROM niveles_instruccion WHERE id_nivel_instruccion = %s"
        return self.execute_query_one(sql, (nivel_instruccion_id,))

    def guardarNivelInstruccion(self, descripcion, estado):
        sql = """
            INSERT INTO niveles_instruccion (des_nivel_instruccion, est_nivel_instruccion)
            VALUES (%s, %s)
            RETURNING id_nivel_instruccion
        """
        fila = self.execute_query_one(sql, (descripcion, estado), commit=True)
        return fila["id_nivel_instruccion"] if fila else None

    def updateNivelInstruccion(self, nivel_instruccion_id, descripcion, estado):
        sql = """
            UPDATE niveles_instruccion
            SET des_nivel_instruccion = %s, est_nivel_instruccion = %s
            WHERE id_nivel_instruccion = %s
        """
        return self.execute_query(sql, (descripcion, estado, nivel_instruccion_id), commit=True) > 0

    def deleteNivelInstruccion(self, nivel_instruccion_id):
        sql = "DELETE FROM niveles_instruccion WHERE id_nivel_instruccion = %s"
        return self.execute_query(sql, (nivel_instruccion_id,), commit=True) > 0
