import re

from app.core.base_dao import BaseDAO


class EmpresaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEmpresaPrincipal(self):
        sql = """
            SELECT id_empresa, ruc_nit, digito_verificador, razon_social, nombre_comercial,
                   tipo_contribuyente, id_ciudad, direccion, numero_casa, codigo_postal,
                   telefono, celular, email, sitio_web, actividad_economica_principal,
                   horario_atencion, es_principal, est_empresa
            FROM empresa
            ORDER BY id_empresa
            LIMIT 1
        """
        return self.execute_query_one(sql)

    def validarRuc(self, ruc_nit):
        """Misma regla que el check constraint chk_empresa_ruc_len: solo dígitos, 6 a 20 caracteres."""
        return bool(re.match(r"^[0-9]{6,20}$", ruc_nit or ""))

    def validarEmail(self, email):
        """Misma regla que el check constraint chk_empresa_email."""
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.match(patron, email or "", re.IGNORECASE))

    def rucExiste(self, ruc_nit, excluir_id=None):
        sql = "SELECT 1 FROM empresa WHERE ruc_nit = %s"
        params = [ruc_nit]
        if excluir_id:
            sql += " AND id_empresa != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarEmpresa(self, ruc_nit, digito_verificador, razon_social, tipo_contribuyente,
                        direccion, telefono, celular, email, nombre_comercial=None, id_ciudad=None,
                        numero_casa=None, codigo_postal=None, sitio_web=None,
                        actividad_economica_principal=None, horario_atencion=None, usuario_creacion=None):
        """Solo permitido si todavía no existe ninguna empresa (single-tenant)."""
        if self.getEmpresaPrincipal() is not None:
            raise ValueError("Ya existe una empresa configurada")

        sql = """
            INSERT INTO empresa (ruc_nit, digito_verificador, razon_social, nombre_comercial,
                                  tipo_contribuyente, id_ciudad, direccion, numero_casa, codigo_postal,
                                  telefono, celular, email, sitio_web, actividad_economica_principal,
                                  horario_atencion, es_principal, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s)
            RETURNING id_empresa
        """
        fila = self.execute_query_one(sql, (
            ruc_nit, digito_verificador, razon_social, nombre_comercial, tipo_contribuyente,
            id_ciudad, direccion, numero_casa, codigo_postal, telefono, celular, email, sitio_web,
            actividad_economica_principal, horario_atencion, usuario_creacion
        ), commit=True)
        return fila["id_empresa"] if fila else None

    def updateEmpresa(self, id_empresa, ruc_nit, digito_verificador, razon_social, tipo_contribuyente,
                       direccion, telefono, celular, email, nombre_comercial=None, id_ciudad=None,
                       numero_casa=None, codigo_postal=None, sitio_web=None,
                       actividad_economica_principal=None, horario_atencion=None, usuario_modificacion=None):
        sql = """
            UPDATE empresa
            SET ruc_nit = %s, digito_verificador = %s, razon_social = %s, nombre_comercial = %s,
                tipo_contribuyente = %s, id_ciudad = %s, direccion = %s, numero_casa = %s,
                codigo_postal = %s, telefono = %s, celular = %s, email = %s, sitio_web = %s,
                actividad_economica_principal = %s, horario_atencion = %s, usuario_modificacion = %s
            WHERE id_empresa = %s
        """
        return self.execute_query(sql, (
            ruc_nit, digito_verificador, razon_social, nombre_comercial, tipo_contribuyente,
            id_ciudad, direccion, numero_casa, codigo_postal, telefono, celular, email, sitio_web,
            actividad_economica_principal, horario_atencion, usuario_modificacion, id_empresa
        ), commit=True) > 0
