# Data access object - DAO
import re
from app.core.base_dao import BaseDAO


class GeneroDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_genero, des_genero, est_genero
        FROM generos
        ORDER BY des_genero
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_genero'], 'descripcion': f['des_genero'], 'estado': f['est_genero']} for f in filas]

    def get_por_id(self, id_genero: int) -> dict | None:
        sql = """
        SELECT id_genero, des_genero, est_genero
        FROM generos
        WHERE id_genero=%s
        """
        f = self.execute_query_one(sql, (id_genero,))
        if not f:
            return None
        return {"id": f['id_genero'], "descripcion": f['des_genero'], "estado": f['est_genero']}

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_genero: str) -> bool:
        """Verifica si ya existe el género con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM generos WHERE LOWER(des_genero)=LOWER(%s)"
        return self.execute_query_one(sql, (des_genero,)) is not None

    def validar_descripcion(self, des_genero: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_genero))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_genero: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_genero):
            return False
        if self.existe(des_genero):
            return False

        sql = """
        INSERT INTO generos(des_genero, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_genero
        """
        fila = self.execute_query_one(sql, (des_genero, usuario_creacion), commit=True)
        return fila[0] if fila else False

    def actualizar(self, id_genero: int, des_genero: str, est_genero: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_genero):
            return False

        sql = """
        UPDATE generos
        SET des_genero=%s, est_genero=%s, usuario_modificacion=%s
        WHERE id_genero=%s
        """
        filas = self.execute_query(sql, (des_genero, est_genero, usuario_modificacion, id_genero), commit=True)
        return filas > 0
