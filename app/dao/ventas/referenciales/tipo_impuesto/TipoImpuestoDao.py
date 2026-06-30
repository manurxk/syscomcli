import re
from app.core.base_dao import BaseDAO


class TipoImpuestoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposImpuestos(self):
        sql = """
            SELECT id_tipo_impuesto, des_tipo_impuesto, cod_tipo_impuesto,
                   porcentaje_impuesto, tipo_calculo, est_tipo_impuesto
            FROM tipos_impuestos
            ORDER BY des_tipo_impuesto ASC
        """
        return self.execute_query(sql)

    def getTipoImpuestoById(self, id_tipo_impuesto):
        sql = """
            SELECT id_tipo_impuesto, des_tipo_impuesto, cod_tipo_impuesto,
                   porcentaje_impuesto, tipo_calculo, est_tipo_impuesto
            FROM tipos_impuestos WHERE id_tipo_impuesto = %s
        """
        return self.execute_query_one(sql, (id_tipo_impuesto,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .%]+$", descripcion))

    def tipoImpuestoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM tipos_impuestos WHERE LOWER(des_tipo_impuesto)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_impuesto != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoImpuesto(self, descripcion, codigo=None, porcentaje=0,
                             tipo_calculo='PORCENTAJE', estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO tipos_impuestos (des_tipo_impuesto, cod_tipo_impuesto,
                                         porcentaje_impuesto, tipo_calculo,
                                         est_tipo_impuesto, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_tipo_impuesto
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             porcentaje, tipo_calculo, estado, usuario_creacion),
            commit=True
        )
        return fila["id_tipo_impuesto"] if fila else None

    def updateTipoImpuesto(self, id_tipo_impuesto, descripcion, codigo=None,
                            porcentaje=0, tipo_calculo='PORCENTAJE',
                            estado=True, usuario_modificacion=None):
        sql = """
            UPDATE tipos_impuestos
            SET des_tipo_impuesto=%s, cod_tipo_impuesto=%s, porcentaje_impuesto=%s,
                tipo_calculo=%s, est_tipo_impuesto=%s, usuario_modificacion=%s
            WHERE id_tipo_impuesto=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             porcentaje, tipo_calculo, estado, usuario_modificacion, id_tipo_impuesto),
            commit=True
        ) > 0

    def desactivarTipoImpuesto(self, id_tipo_impuesto, usuario_modificacion=None):
        sql = "UPDATE tipos_impuestos SET est_tipo_impuesto=FALSE, usuario_modificacion=%s WHERE id_tipo_impuesto=%s"
        return self.execute_query(sql, (usuario_modificacion, id_tipo_impuesto), commit=True) > 0
