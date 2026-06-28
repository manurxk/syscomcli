import re

from app.core.base_dao import BaseDAO


class TipoTratamientoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposTratamientos(self):
        sql = "SELECT id_tipo_tratamiento, des_tipo_tratamiento, est_tipo_tratamiento FROM tipos_tratamientos ORDER BY id_tipo_tratamiento"
        return self.execute_query(sql)

    def getTipoTratamientoById(self, tipo_tratamiento_id):
        sql = "SELECT id_tipo_tratamiento, des_tipo_tratamiento, est_tipo_tratamiento FROM tipos_tratamientos WHERE id_tipo_tratamiento = %s"
        return self.execute_query_one(sql, (tipo_tratamiento_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def tipoTratamientoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM tipos_tratamientos WHERE LOWER(des_tipo_tratamiento) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_tratamiento != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoTratamiento(self, descripcion, estado, usuario_creacion=None):
        sql = """
            INSERT INTO tipos_tratamientos (des_tipo_tratamiento, est_tipo_tratamiento, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_tipo_tratamiento
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_tipo_tratamiento"] if fila else None

    def updateTipoTratamiento(self, tipo_tratamiento_id, descripcion, estado, usuario_modificacion=None):
        sql = """
            UPDATE tipos_tratamientos
            SET des_tipo_tratamiento = %s, est_tipo_tratamiento = %s, usuario_modificacion = %s
            WHERE id_tipo_tratamiento = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, tipo_tratamiento_id), commit=True) > 0

    def desactivarTipoTratamiento(self, tipo_tratamiento_id, usuario_modificacion=None):
        sql = """
            UPDATE tipos_tratamientos
            SET est_tipo_tratamiento = FALSE, usuario_modificacion = %s
            WHERE id_tipo_tratamiento = %s
        """
        return self.execute_query(sql, (usuario_modificacion, tipo_tratamiento_id), commit=True) > 0
