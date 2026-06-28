import re

from app.core.base_dao import BaseDAO


class InstrumentoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getInstrumentos(self):
        sql = "SELECT id_instrumento, des_instrumento, est_instrumento FROM instrumentos ORDER BY id_instrumento"
        return self.execute_query(sql)

    def getInstrumentoById(self, instrumento_id):
        sql = "SELECT id_instrumento, des_instrumento, est_instrumento FROM instrumentos WHERE id_instrumento = %s"
        return self.execute_query_one(sql, (instrumento_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def instrumentoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM instrumentos WHERE LOWER(des_instrumento) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_instrumento != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarInstrumento(self, descripcion, estado, usuario_creacion=None):
        sql = """
            INSERT INTO instrumentos (des_instrumento, est_instrumento, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_instrumento
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_instrumento"] if fila else None

    def updateInstrumento(self, instrumento_id, descripcion, estado, usuario_modificacion=None):
        sql = """
            UPDATE instrumentos
            SET des_instrumento = %s, est_instrumento = %s, usuario_modificacion = %s
            WHERE id_instrumento = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, instrumento_id), commit=True) > 0

    def desactivarInstrumento(self, instrumento_id, usuario_modificacion=None):
        sql = """
            UPDATE instrumentos
            SET est_instrumento = FALSE, usuario_modificacion = %s
            WHERE id_instrumento = %s
        """
        return self.execute_query(sql, (usuario_modificacion, instrumento_id), commit=True) > 0
