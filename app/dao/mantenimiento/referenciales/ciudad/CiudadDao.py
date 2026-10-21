from app.core.base_dao import BaseDAO


class CiudadDao(BaseDAO):
    """Acceso a datos de ciudad (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCiudades(self):
        """Lista los registros de ciudad."""
        sql = "SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad FROM ciudades ORDER BY id_ciudad"
        return self.execute_query(sql)

    def getCiudadById(self, ciudad_id):
        """Devuelve el registro de ciudad por su id, o None si no existe."""
        sql = "SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad FROM ciudades WHERE id_ciudad = %s"
        return self.execute_query_one(sql, (ciudad_id,))

    def guardarCiudad(self, id_departamento, descripcion, estado):
        """Inserta un registro de ciudad y devuelve el id generado."""
        sql = """
            INSERT INTO ciudades (id_departamento, des_ciudad, est_ciudad)
            VALUES (%s, %s, %s)
            RETURNING id_ciudad
        """
        fila = self.execute_query_one(sql, (id_departamento, descripcion, estado), commit=True)
        return fila["id_ciudad"] if fila else None

    def updateCiudad(self, ciudad_id, id_departamento, descripcion, estado):
        """Actualiza los datos de ciudad; devuelve True si modificó una fila."""
        sql = """
            UPDATE ciudades
            SET id_departamento = %s, des_ciudad = %s, est_ciudad = %s
            WHERE id_ciudad = %s
        """
        return self.execute_query(sql, (id_departamento, descripcion, estado, ciudad_id), commit=True) > 0
