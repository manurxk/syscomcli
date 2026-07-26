import re
from datetime import date
from flask import current_app as app
from app.core.base_dao import BaseDAO


class TimbradoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def validarNumeroTimbrado(self, numero):
        """Formato real de timbrado SET: 8 dígitos numéricos."""
        return bool(re.match(r"^[0-9]{8}$", numero))

    def validarCodigoEstablecimiento(self, codigo):
        """Mismo criterio que SedeDao.validarCodigoEstablecimiento: 3 dígitos numéricos."""
        return bool(re.match(r"^[0-9]{3}$", codigo))

    def getTimbrados(self):
        sql = """
            SELECT id_timbrado, numero_timbrado, codigo_establecimiento,
                   fecha_inicio, fecha_vencimiento, observaciones, est_timbrado
            FROM timbrados
            ORDER BY est_timbrado DESC, fecha_vencimiento DESC
        """
        return self.execute_query(sql)

    def getTimbradoById(self, id_timbrado):
        sql = """
            SELECT id_timbrado, numero_timbrado, codigo_establecimiento,
                   fecha_inicio, fecha_vencimiento, observaciones, est_timbrado
            FROM timbrados
            WHERE id_timbrado = %s
        """
        return self.execute_query_one(sql, (id_timbrado,))

    def getTimbradosVigentes(self):
        sql = """
            SELECT id_timbrado, numero_timbrado, codigo_establecimiento,
                   fecha_inicio, fecha_vencimiento
            FROM timbrados
            WHERE est_timbrado = TRUE
              AND fecha_inicio <= CURRENT_DATE
              AND fecha_vencimiento >= CURRENT_DATE
            ORDER BY fecha_vencimiento DESC
        """
        return self.execute_query(sql)

    def timbradoExiste(self, numero_timbrado, excluir_id=None):
        sql = "SELECT 1 FROM timbrados WHERE numero_timbrado = %s"
        params = [numero_timbrado]
        if excluir_id:
            sql += " AND id_timbrado != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardar(self, numero_timbrado, codigo_establecimiento, fecha_inicio,
                fecha_vencimiento, observaciones=None, est_timbrado=True,
                usuario_creacion=None):
        sql = """
            INSERT INTO timbrados(
                numero_timbrado, codigo_establecimiento,
                fecha_inicio, fecha_vencimiento, observaciones,
                est_timbrado, usuario_creacion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_timbrado
        """
        fila = self.execute_query_one(
            sql,
            (numero_timbrado, codigo_establecimiento, fecha_inicio,
             fecha_vencimiento, observaciones, est_timbrado, usuario_creacion),
            commit=True
        )
        return fila['id_timbrado'] if fila else None

    def update(self, id_timbrado, numero_timbrado, codigo_establecimiento,
               fecha_inicio, fecha_vencimiento, observaciones=None,
               est_timbrado=True, usuario_modificacion=None):
        sql = """
            UPDATE timbrados
            SET numero_timbrado=%s, codigo_establecimiento=%s,
                fecha_inicio=%s, fecha_vencimiento=%s, observaciones=%s,
                est_timbrado=%s, usuario_modificacion=%s
            WHERE id_timbrado=%s
        """
        return self.execute_query(
            sql,
            (numero_timbrado, codigo_establecimiento, fecha_inicio,
             fecha_vencimiento, observaciones, est_timbrado,
             usuario_modificacion, id_timbrado),
            commit=True
        ) > 0

    def desactivar(self, id_timbrado, usuario_modificacion=None):
        sql = """
            UPDATE timbrados SET est_timbrado=FALSE, usuario_modificacion=%s
            WHERE id_timbrado=%s
        """
        return self.execute_query(sql, (usuario_modificacion, id_timbrado), commit=True) > 0

    def tieneFacturas(self, id_timbrado):
        sql = "SELECT 1 FROM facturas WHERE id_timbrado=%s LIMIT 1"
        return self.execute_query_one(sql, (id_timbrado,)) is not None
