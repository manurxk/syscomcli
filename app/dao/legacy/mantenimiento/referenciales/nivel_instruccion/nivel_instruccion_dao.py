# Data access object - DAO
import re
from app.core.base_dao import BaseDAO


class NivelInstruccionDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_nivel_instruccion, des_nivel_instruccion, est_nivel_instruccion
        FROM niveles_instruccion
        ORDER BY id_nivel_instruccion
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_nivel_instruccion'], 'descripcion': f['des_nivel_instruccion'], 'estado': f['est_nivel_instruccion']} for f in filas]

    def get_por_id(self, id_nivel_instruccion: int) -> dict | None:
        sql = """
        SELECT id_nivel_instruccion, des_nivel_instruccion, est_nivel_instruccion
        FROM niveles_instruccion
        WHERE id_nivel_instruccion=%s
        """
        f = self.execute_query_one(sql, (id_nivel_instruccion,))
        if not f:
            return None
        return {"id": f['id_nivel_instruccion'], "descripcion": f['des_nivel_instruccion'], "estado": f['est_nivel_instruccion']}

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_nivel_instruccion: str) -> bool:
        """Verifica si ya existe el nivel con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM niveles_instruccion WHERE LOWER(des_nivel_instruccion)=LOWER(%s)"
        return self.execute_query_one(sql, (des_nivel_instruccion,)) is not None

    def validar_descripcion(self, des_nivel_instruccion: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_nivel_instruccion))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_nivel_instruccion: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_nivel_instruccion):
            return False
        if self.existe(des_nivel_instruccion):
            return False

        sql = """
        INSERT INTO niveles_instruccion(des_nivel_instruccion, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_nivel_instruccion
        """
        fila = self.execute_query_one(sql, (des_nivel_instruccion, usuario_creacion), commit=True)
        return fila[0] if fila else False

    def actualizar(self, id_nivel_instruccion: int, des_nivel_instruccion: str, est_nivel_instruccion: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_nivel_instruccion):
            return False

        sql = """
        UPDATE niveles_instruccion
        SET des_nivel_instruccion=%s, est_nivel_instruccion=%s, usuario_modificacion=%s
        WHERE id_nivel_instruccion=%s
        """
        filas = self.execute_query(sql, (des_nivel_instruccion, est_nivel_instruccion, usuario_modificacion, id_nivel_instruccion), commit=True)
        return filas > 0
