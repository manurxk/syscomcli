# Data access object - DAO
import re
from app.core.base_dao import BaseDAO


class CargoDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_cargo, des_cargo, est_cargo
        FROM cargos
        ORDER BY des_cargo
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_cargo'], 'descripcion': f['des_cargo'], 'estado': f['est_cargo']} for f in filas]

    def get_cargos_permitidos(self, excluir_administrador: bool = False) -> list[dict]:
        """
        Obtiene cargos activos. Si excluir_administrador es True, excluye
        los cargos 'ADMINISTRADOR' y 'SUPERADMINISTRADOR'.
        """
        if excluir_administrador:
            sql = """
            SELECT id_cargo, des_cargo, est_cargo
            FROM cargos
            WHERE LOWER(des_cargo) NOT IN ('administrador', 'superadministrador')
            AND est_cargo = TRUE
            ORDER BY des_cargo
            """
        else:
            sql = """
            SELECT id_cargo, des_cargo, est_cargo
            FROM cargos
            WHERE est_cargo = TRUE
            ORDER BY des_cargo
            """
        filas = self.execute_query(sql)
        return [{'id': f['id_cargo'], 'descripcion': f['des_cargo'], 'estado': f['est_cargo']} for f in filas]

    def get_por_id(self, id_cargo: int) -> dict | None:
        sql = """
        SELECT id_cargo, des_cargo, est_cargo
        FROM cargos
        WHERE id_cargo=%s
        """
        f = self.execute_query_one(sql, (id_cargo,))
        if not f:
            return None
        return {"id": f['id_cargo'], "descripcion": f['des_cargo'], "estado": f['est_cargo']}

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_cargo: str) -> bool:
        """Verifica si ya existe el cargo con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM cargos WHERE LOWER(des_cargo)=LOWER(%s)"
        return self.execute_query_one(sql, (des_cargo,)) is not None

    def validar_descripcion(self, des_cargo: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_cargo))

    def es_cargo_reservado(self, des_cargo: str) -> bool:
        """Los cargos 'ADMINISTRADOR' y 'SUPERADMINISTRADOR' están reservados y no se pueden crear/editar."""
        descripcion_lower = des_cargo.lower().strip()
        cargos_reservados = ['administrador', 'superadministrador']
        return descripcion_lower in cargos_reservados

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_cargo: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_cargo):
            return False
        if self.es_cargo_reservado(des_cargo):
            return False
        if self.existe(des_cargo):
            return False

        sql = """
        INSERT INTO cargos(des_cargo, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_cargo
        """
        fila = self.execute_query_one(sql, (des_cargo, usuario_creacion), commit=True)
        return fila[0] if fila else False

    def actualizar(self, id_cargo: int, des_cargo: str, est_cargo: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_cargo):
            return False
        if self.es_cargo_reservado(des_cargo):
            return False

        sql = """
        UPDATE cargos
        SET des_cargo=%s, est_cargo=%s, usuario_modificacion=%s
        WHERE id_cargo=%s
        """
        filas = self.execute_query(sql, (des_cargo, est_cargo, usuario_modificacion, id_cargo), commit=True)
        return filas > 0
