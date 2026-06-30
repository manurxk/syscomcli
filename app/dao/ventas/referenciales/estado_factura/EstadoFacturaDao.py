import re
from app.core.base_dao import BaseDAO


class EstadoFacturaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEstadosFactura(self):
        sql = """
            SELECT id_estado_factura, des_estado_factura, cod_estado_factura,
                   permite_modificacion, permite_anulacion, color_estado, est_estado_factura
            FROM estados_factura
            ORDER BY des_estado_factura ASC
        """
        return self.execute_query(sql)

    def getEstadoFacturaById(self, id_estado_factura):
        sql = """
            SELECT id_estado_factura, des_estado_factura, cod_estado_factura,
                   permite_modificacion, permite_anulacion, color_estado, est_estado_factura
            FROM estados_factura WHERE id_estado_factura = %s
        """
        return self.execute_query_one(sql, (id_estado_factura,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def estadoFacturaExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM estados_factura WHERE LOWER(des_estado_factura)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_estado_factura != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarEstadoFactura(self, descripcion, codigo=None, permite_modificacion=True,
                              permite_anulacion=True, color='secondary',
                              estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO estados_factura (des_estado_factura, cod_estado_factura,
                                         permite_modificacion, permite_anulacion,
                                         color_estado, est_estado_factura, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_estado_factura
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             permite_modificacion, permite_anulacion, color, estado, usuario_creacion),
            commit=True
        )
        return fila["id_estado_factura"] if fila else None

    def updateEstadoFactura(self, id_estado_factura, descripcion, codigo=None,
                             permite_modificacion=True, permite_anulacion=True,
                             color='secondary', estado=True, usuario_modificacion=None):
        sql = """
            UPDATE estados_factura
            SET des_estado_factura=%s, cod_estado_factura=%s, permite_modificacion=%s,
                permite_anulacion=%s, color_estado=%s, est_estado_factura=%s,
                usuario_modificacion=%s
            WHERE id_estado_factura=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             permite_modificacion, permite_anulacion, color,
             estado, usuario_modificacion, id_estado_factura),
            commit=True
        ) > 0

    def desactivarEstadoFactura(self, id_estado_factura, usuario_modificacion=None):
        sql = "UPDATE estados_factura SET est_estado_factura=FALSE, usuario_modificacion=%s WHERE id_estado_factura=%s"
        return self.execute_query(sql, (usuario_modificacion, id_estado_factura), commit=True) > 0
