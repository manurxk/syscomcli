from app.core.base_dao import BaseDAO


class PaisDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPaises(self):
        sql = "SELECT id_pais, des_pais, cod_pais, est_pais FROM paises ORDER BY id_pais"
        return self.execute_query(sql)

    def getPaisById(self, pais_id):
        sql = "SELECT id_pais, des_pais, cod_pais, est_pais FROM paises WHERE id_pais = %s"
        return self.execute_query_one(sql, (pais_id,))

    def guardarPais(self, descripcion, codigo, estado):
        sql = """
            INSERT INTO paises (des_pais, cod_pais, est_pais)
            VALUES (%s, %s, %s)
            RETURNING id_pais
        """
        fila = self.execute_query_one(sql, (descripcion, codigo, estado), commit=True)
        return fila["id_pais"] if fila else None

    def updatePais(self, pais_id, descripcion, codigo, estado):
        sql = """
            UPDATE paises
            SET des_pais = %s, cod_pais = %s, est_pais = %s
            WHERE id_pais = %s
        """
        return self.execute_query(sql, (descripcion, codigo, estado, pais_id), commit=True) > 0

    def deletePais(self, pais_id):
        sql = "DELETE FROM paises WHERE id_pais = %s"
        return self.execute_query(sql, (pais_id,), commit=True) > 0
