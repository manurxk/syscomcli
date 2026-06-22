from app.core.base_dao import BaseDAO


class CargoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCargos(self):
        sql = "SELECT id_cargo, des_cargo, est_cargo FROM cargos ORDER BY id_cargo"
        return self.execute_query(sql)

    def getCargoById(self, cargo_id):
        sql = "SELECT id_cargo, des_cargo, est_cargo FROM cargos WHERE id_cargo = %s"
        return self.execute_query_one(sql, (cargo_id,))

    def guardarCargo(self, descripcion, estado):
        sql = """
            INSERT INTO cargos (des_cargo, est_cargo)
            VALUES (%s, %s)
            RETURNING id_cargo
        """
        fila = self.execute_query_one(sql, (descripcion, estado), commit=True)
        return fila["id_cargo"] if fila else None

    def updateCargo(self, cargo_id, descripcion, estado):
        sql = """
            UPDATE cargos
            SET des_cargo = %s, est_cargo = %s
            WHERE id_cargo = %s
        """
        return self.execute_query(sql, (descripcion, estado, cargo_id), commit=True) > 0

    def deleteCargo(self, cargo_id):
        sql = "DELETE FROM cargos WHERE id_cargo = %s"
        return self.execute_query(sql, (cargo_id,), commit=True) > 0
