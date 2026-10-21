import re

from app.core.base_dao import BaseDAO


class TipoAnalisisDao(BaseDAO):
    """Acceso a datos de tipo de análisis (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposAnalisis(self):
        """Lista los registros de tipo de análisis."""
        sql = "SELECT id_tipo_analisis, des_tipo_analisis, est_tipo_analisis FROM tipos_analisis ORDER BY id_tipo_analisis"
        return self.execute_query(sql)

    def getTipoAnalisisById(self, tipo_analisis_id):
        """Devuelve el registro de tipo de análisis por su id, o None si no existe."""
        sql = "SELECT id_tipo_analisis, des_tipo_analisis, est_tipo_analisis FROM tipos_analisis WHERE id_tipo_analisis = %s"
        return self.execute_query_one(sql, (tipo_analisis_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def tipoAnalisisExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de tipo de análisis con esa descripción; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM tipos_analisis WHERE LOWER(des_tipo_analisis) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_analisis != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoAnalisis(self, descripcion, estado, usuario_creacion=None):
        """Inserta un registro de tipo de análisis y devuelve el id generado."""
        sql = """
            INSERT INTO tipos_analisis (des_tipo_analisis, est_tipo_analisis, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_tipo_analisis
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_tipo_analisis"] if fila else None

    def updateTipoAnalisis(self, tipo_analisis_id, descripcion, estado, usuario_modificacion=None):
        """Actualiza los datos de tipo de análisis; devuelve True si modificó una fila."""
        sql = """
            UPDATE tipos_analisis
            SET des_tipo_analisis = %s, est_tipo_analisis = %s, usuario_modificacion = %s
            WHERE id_tipo_analisis = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, tipo_analisis_id), commit=True) > 0

    def desactivarTipoAnalisis(self, tipo_analisis_id, usuario_modificacion=None):
        """Da de baja (lógica) el registro de tipo de análisis; devuelve True si modificó una fila."""
        sql = """
            UPDATE tipos_analisis
            SET est_tipo_analisis = FALSE, usuario_modificacion = %s
            WHERE id_tipo_analisis = %s
        """
        return self.execute_query(sql, (usuario_modificacion, tipo_analisis_id), commit=True) > 0
