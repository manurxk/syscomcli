# Data access object - DAO
import re
from app.core.base_dao import BaseDAO


class EstadoCivilDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_estado_civil, des_estado_civil, est_estado_civil
        FROM estados_civiles
        ORDER BY des_estado_civil
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_estado_civil'], 'descripcion': f['des_estado_civil'], 'estado': f['est_estado_civil']} for f in filas]

    def get_por_id(self, id_estado_civil: int) -> dict | None:
        sql = """
        SELECT id_estado_civil, des_estado_civil, est_estado_civil
        FROM estados_civiles
        WHERE id_estado_civil=%s
        """
        f = self.execute_query_one(sql, (id_estado_civil,))
        if not f:
            return None
        return {"id": f['id_estado_civil'], "descripcion": f['des_estado_civil'], "estado": f['est_estado_civil']}

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_estado_civil: str) -> bool:
        """Verifica si ya existe un estado civil con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM estados_civiles WHERE LOWER(des_estado_civil)=LOWER(%s)"
        return self.execute_query_one(sql, (des_estado_civil,)) is not None

    def validar_descripcion(self, des_estado_civil: str) -> bool:
        """Permite solo letras con acentos y espacios (sin números ni símbolos)."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
        return bool(re.match(patron, des_estado_civil))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_estado_civil: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_estado_civil):
            return False
        if self.existe(des_estado_civil):
            return False

        sql = """
        INSERT INTO estados_civiles(des_estado_civil, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_estado_civil
        """
        fila = self.execute_query_one(sql, (des_estado_civil, usuario_creacion), commit=True)
        return fila[0] if fila else False

    def actualizar(self, id_estado_civil: int, des_estado_civil: str, est_estado_civil: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_estado_civil):
            return False

        sql = """
        UPDATE estados_civiles
        SET des_estado_civil=%s, est_estado_civil=%s, usuario_modificacion=%s
        WHERE id_estado_civil=%s
        """
        filas = self.execute_query(sql, (des_estado_civil, est_estado_civil, usuario_modificacion, id_estado_civil), commit=True)
        return filas > 0
