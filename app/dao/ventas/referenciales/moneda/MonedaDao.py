import re
from app.core.base_dao import BaseDAO


class MonedaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getMonedas(self):
        sql = """
            SELECT id_moneda, des_moneda, cod_moneda, simbolo_moneda,
                   decimales_moneda, es_moneda_local, tasa_cambio, est_moneda
            FROM monedas
            ORDER BY es_moneda_local DESC, des_moneda ASC
        """
        return self.execute_query(sql)

    def getMonedaById(self, id_moneda):
        sql = """
            SELECT id_moneda, des_moneda, cod_moneda, simbolo_moneda,
                   decimales_moneda, es_moneda_local, tasa_cambio, est_moneda
            FROM monedas WHERE id_moneda = %s
        """
        return self.execute_query_one(sql, (id_moneda,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def monedaExiste(self, codigo, excluir_id=None):
        sql = "SELECT 1 FROM monedas WHERE UPPER(cod_moneda) = UPPER(%s)"
        params = [codigo]
        if excluir_id:
            sql += " AND id_moneda != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarMoneda(self, descripcion, codigo, simbolo=None, decimales=0,
                      es_moneda_local=False, tasa_cambio=1.0, estado=True,
                      usuario_creacion=None):
        sql = """
            INSERT INTO monedas (des_moneda, cod_moneda, simbolo_moneda, decimales_moneda,
                                 es_moneda_local, tasa_cambio, est_moneda, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_moneda
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper(), simbolo, decimales,
             es_moneda_local, tasa_cambio, estado, usuario_creacion),
            commit=True
        )
        return fila["id_moneda"] if fila else None

    def updateMoneda(self, id_moneda, descripcion, codigo, simbolo=None, decimales=0,
                     es_moneda_local=False, tasa_cambio=1.0, estado=True,
                     usuario_modificacion=None):
        sql = """
            UPDATE monedas
            SET des_moneda=%s, cod_moneda=%s, simbolo_moneda=%s, decimales_moneda=%s,
                es_moneda_local=%s, tasa_cambio=%s, est_moneda=%s, usuario_modificacion=%s
            WHERE id_moneda=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper(), simbolo, decimales,
             es_moneda_local, tasa_cambio, estado, usuario_modificacion, id_moneda),
            commit=True
        ) > 0

    def desactivarMoneda(self, id_moneda, usuario_modificacion=None):
        sql = "UPDATE monedas SET est_moneda=FALSE, usuario_modificacion=%s WHERE id_moneda=%s"
        return self.execute_query(sql, (usuario_modificacion, id_moneda), commit=True) > 0
