import re

from app.core.base_dao import BaseDAO


class MedicamentoDao(BaseDAO):
    """Acceso a datos de medicamento (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getMedicamentos(self):
        """Lista los registros de medicamento."""
        sql = "SELECT id_medicamento, des_medicamento, est_medicamento FROM medicamentos ORDER BY id_medicamento"
        return self.execute_query(sql)

    def getMedicamentoById(self, medicamento_id):
        """Devuelve el registro de medicamento por su id, o None si no existe."""
        sql = "SELECT id_medicamento, des_medicamento, est_medicamento FROM medicamentos WHERE id_medicamento = %s"
        return self.execute_query_one(sql, (medicamento_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def medicamentoExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de medicamento con esa descripción; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM medicamentos WHERE LOWER(des_medicamento) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_medicamento != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarMedicamento(self, descripcion, estado, usuario_creacion=None):
        """Inserta un registro de medicamento y devuelve el id generado."""
        sql = """
            INSERT INTO medicamentos (des_medicamento, est_medicamento, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_medicamento
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_medicamento"] if fila else None

    def updateMedicamento(self, medicamento_id, descripcion, estado, usuario_modificacion=None):
        """Actualiza los datos de medicamento; devuelve True si modificó una fila."""
        sql = """
            UPDATE medicamentos
            SET des_medicamento = %s, est_medicamento = %s, usuario_modificacion = %s
            WHERE id_medicamento = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, medicamento_id), commit=True) > 0

    def desactivarMedicamento(self, medicamento_id, usuario_modificacion=None):
        """Da de baja (lógica) el registro de medicamento; devuelve True si modificó una fila."""
        sql = """
            UPDATE medicamentos
            SET est_medicamento = FALSE, usuario_modificacion = %s
            WHERE id_medicamento = %s
        """
        return self.execute_query(sql, (usuario_modificacion, medicamento_id), commit=True) > 0
