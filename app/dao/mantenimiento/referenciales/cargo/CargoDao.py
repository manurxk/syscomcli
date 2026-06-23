import re

from app.core.base_dao import BaseDAO


class CargoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCargos(self):
        sql = "SELECT id_cargo, des_cargo, est_cargo, es_clinico FROM cargos ORDER BY id_cargo"
        return self.execute_query(sql)

    def getCargoById(self, cargo_id):
        sql = "SELECT id_cargo, des_cargo, est_cargo, es_clinico FROM cargos WHERE id_cargo = %s"
        return self.execute_query_one(sql, (cargo_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el check constraint chk_cargos_des: letras, números y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, descripcion))

    def esCargoReservado(self, descripcion):
        return descripcion.strip().upper() in ("ADMINISTRADOR", "SUPERADMINISTRADOR")

    def cargoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM cargos WHERE LOWER(des_cargo) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_cargo != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarCargo(self, descripcion, estado, es_clinico=False, usuario_creacion=None):
        sql = """
            INSERT INTO cargos (des_cargo, est_cargo, es_clinico, usuario_creacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_cargo
        """
        fila = self.execute_query_one(sql, (descripcion, estado, es_clinico, usuario_creacion), commit=True)
        return fila["id_cargo"] if fila else None

    def updateCargo(self, cargo_id, descripcion, estado, es_clinico=False, usuario_modificacion=None):
        sql = """
            UPDATE cargos
            SET des_cargo = %s, est_cargo = %s, es_clinico = %s, usuario_modificacion = %s
            WHERE id_cargo = %s
        """
        return self.execute_query(sql, (descripcion, estado, es_clinico, usuario_modificacion, cargo_id), commit=True) > 0

    def desactivarCargo(self, cargo_id, usuario_modificacion=None):
        sql = """
            UPDATE cargos
            SET est_cargo = FALSE, usuario_modificacion = %s
            WHERE id_cargo = %s
        """
        return self.execute_query(sql, (usuario_modificacion, cargo_id), commit=True) > 0
