import re

from app.core.base_dao import BaseDAO
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao


class SedeDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getSedes(self):
        sql = """
            SELECT id_sede, id_empresa, des_sede, codigo_sede, cod_establecimiento_sifen,
                   id_ciudad, direccion, telefono, email, es_principal, est_sede
            FROM sedes
            ORDER BY id_sede
        """
        return self.execute_query(sql)

    def getSedeById(self, sede_id):
        sql = """
            SELECT id_sede, id_empresa, des_sede, codigo_sede, cod_establecimiento_sifen,
                   id_ciudad, direccion, codigo_postal, latitud, longitud, telefono, email,
                   horario_atencion, es_principal, est_sede
            FROM sedes
            WHERE id_sede = %s
        """
        return self.execute_query_one(sql, (sede_id,))

    def validarCodigoEstablecimiento(self, codigo):
        """Misma regla que el check constraint chk_sedes_cod_establecimiento."""
        if not codigo:
            return True
        return bool(re.match(r"^[0-9]{3}$", codigo))

    def codigoEstablecimientoExiste(self, codigo, id_empresa, excluir_id=None):
        """Misma restricción que uq_sedes_cod_establecimiento (id_empresa, cod_establecimiento_sifen)."""
        if not codigo:
            return False
        sql = "SELECT 1 FROM sedes WHERE id_empresa = %s AND cod_establecimiento_sifen = %s"
        params = [id_empresa, codigo]
        if excluir_id:
            sql += " AND id_sede != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarSede(self, descripcion, codigo_sede=None, cod_establecimiento_sifen=None, id_ciudad=None,
                     direccion=None, codigo_postal=None, latitud=None, longitud=None, telefono=None,
                     email=None, horario_atencion=None, estado=True, usuario_creacion=None):
        empresa = EmpresaDao().getEmpresaPrincipal()
        if not empresa:
            raise ValueError("No hay una empresa configurada. Configure los datos de la empresa antes de crear sedes.")

        sql = """
            INSERT INTO sedes (id_empresa, des_sede, codigo_sede, cod_establecimiento_sifen, id_ciudad,
                                direccion, codigo_postal, latitud, longitud, telefono, email,
                                horario_atencion, est_sede, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_sede
        """
        fila = self.execute_query_one(sql, (
            empresa["id_empresa"], descripcion, codigo_sede, cod_establecimiento_sifen, id_ciudad,
            direccion, codigo_postal, latitud, longitud, telefono, email,
            horario_atencion, estado, usuario_creacion
        ), commit=True)
        return fila["id_sede"] if fila else None

    def updateSede(self, sede_id, descripcion, codigo_sede=None, cod_establecimiento_sifen=None, id_ciudad=None,
                    direccion=None, codigo_postal=None, latitud=None, longitud=None, telefono=None,
                    email=None, horario_atencion=None, estado=True, usuario_modificacion=None):
        sql = """
            UPDATE sedes
            SET des_sede = %s, codigo_sede = %s, cod_establecimiento_sifen = %s, id_ciudad = %s,
                direccion = %s, codigo_postal = %s, latitud = %s, longitud = %s, telefono = %s,
                email = %s, horario_atencion = %s, est_sede = %s, usuario_modificacion = %s
            WHERE id_sede = %s
        """
        return self.execute_query(sql, (
            descripcion, codigo_sede, cod_establecimiento_sifen, id_ciudad,
            direccion, codigo_postal, latitud, longitud, telefono,
            email, horario_atencion, estado, usuario_modificacion, sede_id
        ), commit=True) > 0

    def desactivarSede(self, sede_id, usuario_modificacion=None):
        sql = """
            UPDATE sedes
            SET est_sede = FALSE, usuario_modificacion = %s
            WHERE id_sede = %s
        """
        return self.execute_query(sql, (usuario_modificacion, sede_id), commit=True) > 0
