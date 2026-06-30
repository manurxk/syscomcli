import re
from app.core.base_dao import BaseDAO


class CondicionVentaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCondicionesVenta(self):
        sql = """
            SELECT id_condicion_venta, des_condicion_venta, cod_condicion_venta,
                   dias_credito, permite_cuotas, numero_cuotas_max, est_condicion_venta
            FROM condiciones_venta
            ORDER BY dias_credito ASC, des_condicion_venta ASC
        """
        return self.execute_query(sql)

    def getCondicionVentaById(self, id_condicion_venta):
        sql = """
            SELECT id_condicion_venta, des_condicion_venta, cod_condicion_venta,
                   dias_credito, permite_cuotas, numero_cuotas_max, est_condicion_venta
            FROM condiciones_venta WHERE id_condicion_venta = %s
        """
        return self.execute_query_one(sql, (id_condicion_venta,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def condicionVentaExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM condiciones_venta WHERE LOWER(des_condicion_venta)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_condicion_venta != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarCondicionVenta(self, descripcion, codigo=None, dias_credito=0,
                               permite_cuotas=False, numero_cuotas_max=1,
                               estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO condiciones_venta (des_condicion_venta, cod_condicion_venta,
                                           dias_credito, permite_cuotas, numero_cuotas_max,
                                           est_condicion_venta, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_condicion_venta
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             dias_credito, permite_cuotas, numero_cuotas_max, estado, usuario_creacion),
            commit=True
        )
        return fila["id_condicion_venta"] if fila else None

    def updateCondicionVenta(self, id_condicion_venta, descripcion, codigo=None,
                              dias_credito=0, permite_cuotas=False, numero_cuotas_max=1,
                              estado=True, usuario_modificacion=None):
        sql = """
            UPDATE condiciones_venta
            SET des_condicion_venta=%s, cod_condicion_venta=%s, dias_credito=%s,
                permite_cuotas=%s, numero_cuotas_max=%s, est_condicion_venta=%s,
                usuario_modificacion=%s
            WHERE id_condicion_venta=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             dias_credito, permite_cuotas, numero_cuotas_max,
             estado, usuario_modificacion, id_condicion_venta),
            commit=True
        ) > 0

    def desactivarCondicionVenta(self, id_condicion_venta, usuario_modificacion=None):
        sql = "UPDATE condiciones_venta SET est_condicion_venta=FALSE, usuario_modificacion=%s WHERE id_condicion_venta=%s"
        return self.execute_query(sql, (usuario_modificacion, id_condicion_venta), commit=True) > 0
