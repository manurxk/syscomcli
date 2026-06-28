import re

from app.core.base_dao import BaseDAO


class TipoCertificadoMedicoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposCertificadosMedicos(self):
        sql = "SELECT id_tipo_certificado_medico, des_tipo_certificado_medico, est_tipo_certificado_medico FROM tipos_certificados_medicos ORDER BY id_tipo_certificado_medico"
        return self.execute_query(sql)

    def getTipoCertificadoMedicoById(self, tipo_certificado_medico_id):
        sql = "SELECT id_tipo_certificado_medico, des_tipo_certificado_medico, est_tipo_certificado_medico FROM tipos_certificados_medicos WHERE id_tipo_certificado_medico = %s"
        return self.execute_query_one(sql, (tipo_certificado_medico_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el legacy: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def tipoCertificadoMedicoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM tipos_certificados_medicos WHERE LOWER(des_tipo_certificado_medico) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_certificado_medico != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoCertificadoMedico(self, descripcion, estado, usuario_creacion=None):
        sql = """
            INSERT INTO tipos_certificados_medicos (des_tipo_certificado_medico, est_tipo_certificado_medico, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_tipo_certificado_medico
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_tipo_certificado_medico"] if fila else None

    def updateTipoCertificadoMedico(self, tipo_certificado_medico_id, descripcion, estado, usuario_modificacion=None):
        sql = """
            UPDATE tipos_certificados_medicos
            SET des_tipo_certificado_medico = %s, est_tipo_certificado_medico = %s, usuario_modificacion = %s
            WHERE id_tipo_certificado_medico = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, tipo_certificado_medico_id), commit=True) > 0

    def desactivarTipoCertificadoMedico(self, tipo_certificado_medico_id, usuario_modificacion=None):
        sql = """
            UPDATE tipos_certificados_medicos
            SET est_tipo_certificado_medico = FALSE, usuario_modificacion = %s
            WHERE id_tipo_certificado_medico = %s
        """
        return self.execute_query(sql, (usuario_modificacion, tipo_certificado_medico_id), commit=True) > 0
