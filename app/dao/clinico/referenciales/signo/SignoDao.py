import re

from app.core.base_dao import BaseDAO


class SignoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getSignos(self):
        sql = "SELECT id_signo, des_signo, est_signo FROM signos ORDER BY id_signo"
        return self.execute_query(sql)

    def getSignoById(self, signo_id):
        sql = "SELECT id_signo, des_signo, est_signo FROM signos WHERE id_signo = %s"
        return self.execute_query_one(sql, (signo_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def signoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM signos WHERE LOWER(des_signo) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_signo != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarSigno(self, descripcion, estado, usuario_creacion=None):
        sql = """
            INSERT INTO signos (des_signo, est_signo, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_signo
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_signo"] if fila else None

    def updateSigno(self, signo_id, descripcion, estado, usuario_modificacion=None):
        sql = """
            UPDATE signos
            SET des_signo = %s, est_signo = %s, usuario_modificacion = %s
            WHERE id_signo = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, signo_id), commit=True) > 0

    def desactivarSigno(self, signo_id, usuario_modificacion=None):
        sql = """
            UPDATE signos
            SET est_signo = FALSE, usuario_modificacion = %s
            WHERE id_signo = %s
        """
        return self.execute_query(sql, (usuario_modificacion, signo_id), commit=True) > 0
