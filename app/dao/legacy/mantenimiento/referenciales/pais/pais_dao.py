# Data access object - DAO
import re
from app.core.base_dao import BaseDAO


class PaisDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_pais, des_pais, cod_pais, est_pais
        FROM paises
        ORDER BY des_pais
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_pais'], 'descripcion': f['des_pais'], 'codigo': f['cod_pais'], 'estado': f['est_pais']} for f in filas]

    def get_activos(self) -> list[dict]:
        sql = """
        SELECT id_pais, des_pais, cod_pais, est_pais
        FROM paises
        WHERE est_pais = TRUE
        ORDER BY des_pais
        """
        filas = self.execute_query(sql)
        return [{'id': f['id_pais'], 'descripcion': f['des_pais'], 'codigo': f['cod_pais'], 'estado': f['est_pais']} for f in filas]

    def get_por_id(self, id_pais: int) -> dict | None:
        sql = """
        SELECT id_pais, des_pais, cod_pais, est_pais
        FROM paises
        WHERE id_pais=%s
        """
        f = self.execute_query_one(sql, (id_pais,))
        if not f:
            return None
        return {"id": f['id_pais'], "descripcion": f['des_pais'], "codigo": f['cod_pais'], "estado": f['est_pais']}

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_pais: str) -> bool:
        """Verifica si ya existe el pais con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM paises WHERE LOWER(des_pais)=LOWER(%s)"
        return self.execute_query_one(sql, (des_pais,)) is not None

    def validar_descripcion(self, des_pais: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_pais))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_pais: str, cod_pais: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_pais):
            return False
        if self.existe(des_pais):
            return False

        sql = """
        INSERT INTO paises(des_pais, cod_pais, usuario_creacion)
        VALUES(%s, %s, %s)
        RETURNING id_pais
        """
        fila = self.execute_query_one(sql, (des_pais, cod_pais, usuario_creacion), commit=True)
        return fila[0] if fila else False

    def actualizar(self, id_pais: int, des_pais: str, cod_pais: str, est_pais: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_pais):
            return False

        sql = """
        UPDATE paises
        SET des_pais=%s, cod_pais=%s, est_pais=%s, usuario_modificacion=%s
        WHERE id_pais=%s
        """
        filas = self.execute_query(sql, (des_pais, cod_pais, est_pais, usuario_modificacion, id_pais), commit=True)
        return filas > 0
