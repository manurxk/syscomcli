import re
from app.core.base_dao import BaseDAO


class TipoComprobanteDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposComprobantes(self):
        sql = """
            SELECT id_tipo_comprobante, des_tipo_comprobante, cod_tipo_comprobante,
                   codigo_sifen, requiere_timbrado, tipo_documento, est_tipo_comprobante
            FROM tipos_comprobantes
            ORDER BY des_tipo_comprobante ASC
        """
        return self.execute_query(sql)

    def getTipoComprobanteById(self, id_tipo_comprobante):
        sql = """
            SELECT id_tipo_comprobante, des_tipo_comprobante, cod_tipo_comprobante,
                   codigo_sifen, requiere_timbrado, tipo_documento, est_tipo_comprobante
            FROM tipos_comprobantes WHERE id_tipo_comprobante = %s
        """
        return self.execute_query_one(sql, (id_tipo_comprobante,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def tipoComprobanteExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM tipos_comprobantes WHERE LOWER(des_tipo_comprobante)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_comprobante != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoComprobante(self, descripcion, codigo=None, codigo_sifen=None,
                                requiere_timbrado=True, tipo_documento=None,
                                estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO tipos_comprobantes (des_tipo_comprobante, cod_tipo_comprobante,
                                            codigo_sifen, requiere_timbrado, tipo_documento,
                                            est_tipo_comprobante, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_tipo_comprobante
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None, codigo_sifen,
             requiere_timbrado, tipo_documento.upper() if tipo_documento else None,
             estado, usuario_creacion),
            commit=True
        )
        return fila["id_tipo_comprobante"] if fila else None

    def updateTipoComprobante(self, id_tipo_comprobante, descripcion, codigo=None,
                               codigo_sifen=None, requiere_timbrado=True,
                               tipo_documento=None, estado=True, usuario_modificacion=None):
        sql = """
            UPDATE tipos_comprobantes
            SET des_tipo_comprobante=%s, cod_tipo_comprobante=%s, codigo_sifen=%s,
                requiere_timbrado=%s, tipo_documento=%s, est_tipo_comprobante=%s,
                usuario_modificacion=%s
            WHERE id_tipo_comprobante=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None, codigo_sifen,
             requiere_timbrado, tipo_documento.upper() if tipo_documento else None,
             estado, usuario_modificacion, id_tipo_comprobante),
            commit=True
        ) > 0

    def desactivarTipoComprobante(self, id_tipo_comprobante, usuario_modificacion=None):
        sql = "UPDATE tipos_comprobantes SET est_tipo_comprobante=FALSE, usuario_modificacion=%s WHERE id_tipo_comprobante=%s"
        return self.execute_query(sql, (usuario_modificacion, id_tipo_comprobante), commit=True) > 0
