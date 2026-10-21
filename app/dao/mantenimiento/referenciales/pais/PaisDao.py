from app.core.base_dao import BaseDAO


class PaisDao(BaseDAO):
    """Acceso a datos de país (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPaises(self):
        """Lista los registros de país."""
        sql = "SELECT id_pais, des_pais, cod_pais, est_pais FROM paises ORDER BY id_pais"
        return self.execute_query(sql)

    def getPaisById(self, pais_id):
        """Devuelve el registro de país por su id, o None si no existe."""
        sql = "SELECT id_pais, des_pais, cod_pais, est_pais FROM paises WHERE id_pais = %s"
        return self.execute_query_one(sql, (pais_id,))

    def guardarPais(self, descripcion, codigo, estado):
        """Inserta un registro de país y devuelve el id generado."""
        sql = """
            INSERT INTO paises (des_pais, cod_pais, est_pais)
            VALUES (%s, %s, %s)
            RETURNING id_pais
        """
        fila = self.execute_query_one(sql, (descripcion, codigo, estado), commit=True)
        return fila["id_pais"] if fila else None

    def updatePais(self, pais_id, descripcion, codigo, estado):
        """Actualiza los datos de país; devuelve True si modificó una fila."""
        sql = """
            UPDATE paises
            SET des_pais = %s, cod_pais = %s, est_pais = %s
            WHERE id_pais = %s
        """
        return self.execute_query(sql, (descripcion, codigo, estado, pais_id), commit=True) > 0
