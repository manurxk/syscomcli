import re

from app.core.base_dao import BaseDAO


class DiagnosticoDao(BaseDAO):
    """Acceso a datos de diagnóstico (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getDiagnosticos(self):
        """Lista los registros de diagnóstico."""
        sql = "SELECT id_diagnostico, cod_cie10, des_diagnostico, est_diagnostico FROM diagnosticos ORDER BY id_diagnostico"
        return self.execute_query(sql)

    def getDiagnosticoById(self, diagnostico_id):
        """Devuelve el registro de diagnóstico por su id, o None si no existe."""
        sql = "SELECT id_diagnostico, cod_cie10, des_diagnostico, est_diagnostico FROM diagnosticos WHERE id_diagnostico = %s"
        return self.execute_query_one(sql, (diagnostico_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def validarCodigoCie10(self, codigo_cie10):
        """Misma regla que el legacy: letra + 2 dígitos + opcional .dígito(s), ej. F32 o F32.1."""
        patron = r"^[A-Z]{1}[0-9]{2}(\.[0-9]{1,2})?$"
        return bool(re.match(patron, codigo_cie10.upper()))

    def diagnosticoExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de diagnóstico con esa descripción; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM diagnosticos WHERE LOWER(des_diagnostico) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_diagnostico != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def codigoCie10Existe(self, codigo_cie10, excluir_id=None):
        """Indica si ya existe un diagnóstico con ese código CIE-10; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM diagnosticos WHERE LOWER(cod_cie10) = LOWER(%s)"
        params = [codigo_cie10]
        if excluir_id:
            sql += " AND id_diagnostico != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarDiagnostico(self, descripcion, cod_cie10, estado, usuario_creacion=None):
        """Inserta un registro de diagnóstico y devuelve el id generado."""
        sql = """
            INSERT INTO diagnosticos (des_diagnostico, cod_cie10, est_diagnostico, usuario_creacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_diagnostico
        """
        fila = self.execute_query_one(sql, (descripcion, cod_cie10, estado, usuario_creacion), commit=True)
        return fila["id_diagnostico"] if fila else None

    def updateDiagnostico(self, diagnostico_id, descripcion, cod_cie10, estado, usuario_modificacion=None):
        """Actualiza los datos de diagnóstico; devuelve True si modificó una fila."""
        sql = """
            UPDATE diagnosticos
            SET des_diagnostico = %s, cod_cie10 = %s, est_diagnostico = %s, usuario_modificacion = %s
            WHERE id_diagnostico = %s
        """
        return self.execute_query(sql, (descripcion, cod_cie10, estado, usuario_modificacion, diagnostico_id), commit=True) > 0

    def desactivarDiagnostico(self, diagnostico_id, usuario_modificacion=None):
        """Da de baja (lógica) el registro de diagnóstico; devuelve True si modificó una fila."""
        sql = """
            UPDATE diagnosticos
            SET est_diagnostico = FALSE, usuario_modificacion = %s
            WHERE id_diagnostico = %s
        """
        return self.execute_query(sql, (usuario_modificacion, diagnostico_id), commit=True) > 0
