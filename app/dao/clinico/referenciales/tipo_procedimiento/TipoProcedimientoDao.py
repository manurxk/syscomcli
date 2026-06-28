import re

from app.core.base_dao import BaseDAO


class TipoProcedimientoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposProcedimientos(self):
        sql = "SELECT id_tipo_procedimiento, des_tipo_procedimiento, est_tipo_procedimiento FROM tipos_procedimientos ORDER BY id_tipo_procedimiento"
        return self.execute_query(sql)

    def getTipoProcedimientoById(self, tipo_procedimiento_id):
        sql = "SELECT id_tipo_procedimiento, des_tipo_procedimiento, est_tipo_procedimiento FROM tipos_procedimientos WHERE id_tipo_procedimiento = %s"
        return self.execute_query_one(sql, (tipo_procedimiento_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def tipoProcedimientoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM tipos_procedimientos WHERE LOWER(des_tipo_procedimiento) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_procedimiento != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoProcedimiento(self, descripcion, estado, usuario_creacion=None):
        sql = """
            INSERT INTO tipos_procedimientos (des_tipo_procedimiento, est_tipo_procedimiento, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_tipo_procedimiento
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_tipo_procedimiento"] if fila else None

    def updateTipoProcedimiento(self, tipo_procedimiento_id, descripcion, estado, usuario_modificacion=None):
        sql = """
            UPDATE tipos_procedimientos
            SET des_tipo_procedimiento = %s, est_tipo_procedimiento = %s, usuario_modificacion = %s
            WHERE id_tipo_procedimiento = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, tipo_procedimiento_id), commit=True) > 0

    def desactivarTipoProcedimiento(self, tipo_procedimiento_id, usuario_modificacion=None):
        sql = """
            UPDATE tipos_procedimientos
            SET est_tipo_procedimiento = FALSE, usuario_modificacion = %s
            WHERE id_tipo_procedimiento = %s
        """
        return self.execute_query(sql, (usuario_modificacion, tipo_procedimiento_id), commit=True) > 0
