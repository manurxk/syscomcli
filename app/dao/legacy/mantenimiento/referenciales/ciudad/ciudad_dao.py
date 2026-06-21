# Data access object - DAO
import re
from app.core.base_dao import BaseDAO


class CiudadDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad
        FROM ciudades
        ORDER BY des_ciudad
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_ciudad'], 'id_departamento': f['id_departamento'], 'descripcion': f['des_ciudad'], 'estado': f['est_ciudad']} for f in filas]

    def get_por_departamento(self, id_departamento: int) -> list[dict]:
        sql = """
        SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad
        FROM ciudades
        WHERE id_departamento=%s
        ORDER BY des_ciudad
        """
        filas = self.execute_query(sql, (id_departamento,))
        return [{'id': f['id_ciudad'], 'id_departamento': f['id_departamento'], 'descripcion': f['des_ciudad'], 'estado': f['est_ciudad']} for f in filas]

    def get_por_id(self, id_ciudad: int) -> dict | None:
        sql = """
        SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad
        FROM ciudades
        WHERE id_ciudad=%s
        """
        f = self.execute_query_one(sql, (id_ciudad,))
        if not f:
            return None
        return {"id": f['id_ciudad'], "id_departamento": f['id_departamento'], "descripcion": f['des_ciudad'], "estado": f['est_ciudad']}

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, id_departamento: int, des_ciudad: str) -> bool:
        """Verifica si ya existe la ciudad con el mismo nombre dentro del departamento (case-insensitive)."""
        sql = "SELECT 1 FROM ciudades WHERE id_departamento=%s AND LOWER(des_ciudad)=LOWER(%s)"
        return self.execute_query_one(sql, (id_departamento, des_ciudad)) is not None

    def validar_descripcion(self, des_ciudad: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_ciudad))

    # ============================
    # CRUD
    # ============================

    def guardar(self, id_departamento: int, des_ciudad: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_ciudad):
            return False
        if self.existe(id_departamento, des_ciudad):
            return False

        sql = """
        INSERT INTO ciudades(id_departamento, des_ciudad, usuario_creacion)
        VALUES(%s, %s, %s)
        RETURNING id_ciudad
        """
        fila = self.execute_query_one(sql, (id_departamento, des_ciudad, usuario_creacion), commit=True)
        return fila[0] if fila else False

    def actualizar(self, id_ciudad: int, id_departamento: int, des_ciudad: str, est_ciudad: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_ciudad):
            return False

        sql = """
        UPDATE ciudades
        SET id_departamento=%s, des_ciudad=%s, est_ciudad=%s, usuario_modificacion=%s
        WHERE id_ciudad=%s
        """
        filas = self.execute_query(sql, (id_departamento, des_ciudad, est_ciudad, usuario_modificacion, id_ciudad), commit=True)
        return filas > 0
