import re

from app.core.base_dao import BaseDAO


class TipoEstudioDao(BaseDAO):
    """Acceso a datos de tipo de estudio (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposEstudios(self):
        """Lista los registros de tipo de estudio."""
        sql = "SELECT id_tipo_estudio, des_tipo_estudio, est_tipo_estudio FROM tipos_estudios ORDER BY id_tipo_estudio"
        return self.execute_query(sql)

    def getTipoEstudioById(self, tipo_estudio_id):
        """Devuelve el registro de tipo de estudio por su id, o None si no existe."""
        sql = "SELECT id_tipo_estudio, des_tipo_estudio, est_tipo_estudio FROM tipos_estudios WHERE id_tipo_estudio = %s"
        return self.execute_query_one(sql, (tipo_estudio_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def tipoEstudioExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de tipo de estudio con esa descripción; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM tipos_estudios WHERE LOWER(des_tipo_estudio) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_estudio != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoEstudio(self, descripcion, estado, usuario_creacion=None):
        """Inserta un registro de tipo de estudio y devuelve el id generado."""
        sql = """
            INSERT INTO tipos_estudios (des_tipo_estudio, est_tipo_estudio, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_tipo_estudio
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_tipo_estudio"] if fila else None

    def updateTipoEstudio(self, tipo_estudio_id, descripcion, estado, usuario_modificacion=None):
        """Actualiza los datos de tipo de estudio; devuelve True si modificó una fila."""
        sql = """
            UPDATE tipos_estudios
            SET des_tipo_estudio = %s, est_tipo_estudio = %s, usuario_modificacion = %s
            WHERE id_tipo_estudio = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, tipo_estudio_id), commit=True) > 0

    def desactivarTipoEstudio(self, tipo_estudio_id, usuario_modificacion=None):
        """Da de baja (lógica) el registro de tipo de estudio; devuelve True si modificó una fila."""
        sql = """
            UPDATE tipos_estudios
            SET est_tipo_estudio = FALSE, usuario_modificacion = %s
            WHERE id_tipo_estudio = %s
        """
        return self.execute_query(sql, (usuario_modificacion, tipo_estudio_id), commit=True) > 0
