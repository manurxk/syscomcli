from app.core.base_dao import BaseDAO


class CiudadDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCiudades(self):
        sql = "SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad FROM ciudades ORDER BY id_ciudad"
        return self.execute_query(sql)

    def getCiudadById(self, ciudad_id):
        sql = "SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad FROM ciudades WHERE id_ciudad = %s"
        return self.execute_query_one(sql, (ciudad_id,))

    def guardarCiudad(self, id_departamento, descripcion, estado):
        sql = """
            INSERT INTO ciudades (id_departamento, des_ciudad, est_ciudad)
            VALUES (%s, %s, %s)
            RETURNING id_ciudad
        """
        fila = self.execute_query_one(sql, (id_departamento, descripcion, estado), commit=True)
        return fila["id_ciudad"] if fila else None

    def updateCiudad(self, ciudad_id, id_departamento, descripcion, estado):
        sql = """
            UPDATE ciudades
            SET id_departamento = %s, des_ciudad = %s, est_ciudad = %s
            WHERE id_ciudad = %s
        """
        return self.execute_query(sql, (id_departamento, descripcion, estado, ciudad_id), commit=True) > 0

    def deleteCiudad(self, ciudad_id):
        sql = "DELETE FROM ciudades WHERE id_ciudad = %s"
        return self.execute_query(sql, (ciudad_id,), commit=True) > 0
