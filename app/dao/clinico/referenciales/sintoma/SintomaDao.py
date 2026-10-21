import re

from app.core.base_dao import BaseDAO


class SintomaDao(BaseDAO):
    """Acceso a datos de síntoma (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getSintomas(self):
        """Lista los registros de síntoma."""
        sql = "SELECT id_sintoma, des_sintoma, est_sintoma FROM sintomas ORDER BY id_sintoma"
        return self.execute_query(sql)

    def getSintomaById(self, sintoma_id):
        """Devuelve el registro de síntoma por su id, o None si no existe."""
        sql = "SELECT id_sintoma, des_sintoma, est_sintoma FROM sintomas WHERE id_sintoma = %s"
        return self.execute_query_one(sql, (sintoma_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def sintomaExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de síntoma con esa descripción; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM sintomas WHERE LOWER(des_sintoma) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_sintoma != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarSintoma(self, descripcion, estado, usuario_creacion=None):
        """Inserta un registro de síntoma y devuelve el id generado."""
        sql = """
            INSERT INTO sintomas (des_sintoma, est_sintoma, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_sintoma
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_sintoma"] if fila else None

    def updateSintoma(self, sintoma_id, descripcion, estado, usuario_modificacion=None):
        """Actualiza los datos de síntoma; devuelve True si modificó una fila."""
        sql = """
            UPDATE sintomas
            SET des_sintoma = %s, est_sintoma = %s, usuario_modificacion = %s
            WHERE id_sintoma = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, sintoma_id), commit=True) > 0

    def desactivarSintoma(self, sintoma_id, usuario_modificacion=None):
        """Da de baja (lógica) el registro de síntoma; devuelve True si modificó una fila."""
        sql = """
            UPDATE sintomas
            SET est_sintoma = FALSE, usuario_modificacion = %s
            WHERE id_sintoma = %s
        """
        return self.execute_query(sql, (usuario_modificacion, sintoma_id), commit=True) > 0
