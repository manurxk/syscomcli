import re

from app.core.base_dao import BaseDAO


class TipoEstudioDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposEstudios(self):
        sql = "SELECT id_tipo_estudio, des_tipo_estudio, est_tipo_estudio FROM tipos_estudios ORDER BY id_tipo_estudio"
        return self.execute_query(sql)

    def getTipoEstudioById(self, tipo_estudio_id):
        sql = "SELECT id_tipo_estudio, des_tipo_estudio, est_tipo_estudio FROM tipos_estudios WHERE id_tipo_estudio = %s"
        return self.execute_query_one(sql, (tipo_estudio_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def tipoEstudioExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM tipos_estudios WHERE LOWER(des_tipo_estudio) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_estudio != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoEstudio(self, descripcion, estado, usuario_creacion=None):
        sql = """
            INSERT INTO tipos_estudios (des_tipo_estudio, est_tipo_estudio, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_tipo_estudio
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_tipo_estudio"] if fila else None

    def updateTipoEstudio(self, tipo_estudio_id, descripcion, estado, usuario_modificacion=None):
        sql = """
            UPDATE tipos_estudios
            SET des_tipo_estudio = %s, est_tipo_estudio = %s, usuario_modificacion = %s
            WHERE id_tipo_estudio = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, tipo_estudio_id), commit=True) > 0

    def desactivarTipoEstudio(self, tipo_estudio_id, usuario_modificacion=None):
        sql = """
            UPDATE tipos_estudios
            SET est_tipo_estudio = FALSE, usuario_modificacion = %s
            WHERE id_tipo_estudio = %s
        """
        return self.execute_query(sql, (usuario_modificacion, tipo_estudio_id), commit=True) > 0
