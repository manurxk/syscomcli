# Data access object - DAO
import re
from app.core.base_dao import BaseDAO


class ProfesionDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_profesion, des_profesion, est_profesion
        FROM profesiones
        ORDER BY des_profesion
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_profesion'], 'descripcion': f['des_profesion'], 'estado': f['est_profesion']} for f in filas]

    def get_por_id(self, id_profesion: int) -> dict | None:
        sql = """
        SELECT id_profesion, des_profesion, est_profesion
        FROM profesiones
        WHERE id_profesion=%s
        """
        f = self.execute_query_one(sql, (id_profesion,))
        if not f:
            return None
        return {"id": f['id_profesion'], "descripcion": f['des_profesion'], "estado": f['est_profesion']}

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_profesion: str) -> bool:
        """Verifica si ya existe la profesión (case-insensitive)."""
        sql = "SELECT 1 FROM profesiones WHERE LOWER(des_profesion)=LOWER(%s)"
        return self.execute_query_one(sql, (des_profesion,)) is not None

    def validar_descripcion(self, des_profesion: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_profesion))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_profesion: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_profesion):
            return False
        if self.existe(des_profesion):
            return False

        sql = """
        INSERT INTO profesiones(des_profesion, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_profesion
        """
        fila = self.execute_query_one(sql, (des_profesion, usuario_creacion), commit=True)
        return fila[0] if fila else False

    def actualizar(self, id_profesion: int, des_profesion: str, est_profesion: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_profesion):
            return False

        sql = """
        UPDATE profesiones
        SET des_profesion=%s, est_profesion=%s, usuario_modificacion=%s
        WHERE id_profesion=%s
        """
        filas = self.execute_query(sql, (des_profesion, est_profesion, usuario_modificacion, id_profesion), commit=True)
        return filas > 0
