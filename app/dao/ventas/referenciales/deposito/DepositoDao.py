import re
from app.core.base_dao import BaseDAO


class DepositoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getDepositos(self):
        sql = """
            SELECT id_deposito, des_deposito, cod_deposito, tipo_deposito,
                   numero_cuenta, banco_deposito, ruc_banco, moneda_deposito, est_deposito
            FROM depositos
            ORDER BY des_deposito ASC
        """
        return self.execute_query(sql)

    def getDepositoById(self, id_deposito):
        sql = """
            SELECT id_deposito, des_deposito, cod_deposito, tipo_deposito,
                   numero_cuenta, banco_deposito, ruc_banco, moneda_deposito, est_deposito
            FROM depositos WHERE id_deposito = %s
        """
        return self.execute_query_one(sql, (id_deposito,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .\-]+$", descripcion))

    def depositoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM depositos WHERE LOWER(des_deposito)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_deposito != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarDeposito(self, descripcion, codigo=None, tipo_deposito='BANCO',
                        numero_cuenta=None, banco=None, ruc_banco=None,
                        moneda='PYG', estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO depositos (des_deposito, cod_deposito, tipo_deposito,
                                   numero_cuenta, banco_deposito, ruc_banco,
                                   moneda_deposito, est_deposito, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_deposito
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             tipo_deposito.upper(), numero_cuenta,
             banco.upper() if banco else None, ruc_banco,
             moneda.upper(), estado, usuario_creacion),
            commit=True
        )
        return fila["id_deposito"] if fila else None

    def updateDeposito(self, id_deposito, descripcion, codigo=None, tipo_deposito='BANCO',
                       numero_cuenta=None, banco=None, ruc_banco=None,
                       moneda='PYG', estado=True, usuario_modificacion=None):
        sql = """
            UPDATE depositos
            SET des_deposito=%s, cod_deposito=%s, tipo_deposito=%s,
                numero_cuenta=%s, banco_deposito=%s, ruc_banco=%s,
                moneda_deposito=%s, est_deposito=%s, usuario_modificacion=%s
            WHERE id_deposito=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             tipo_deposito.upper(), numero_cuenta,
             banco.upper() if banco else None, ruc_banco,
             moneda.upper(), estado, usuario_modificacion, id_deposito),
            commit=True
        ) > 0

    def desactivarDeposito(self, id_deposito, usuario_modificacion=None):
        sql = "UPDATE depositos SET est_deposito=FALSE, usuario_modificacion=%s WHERE id_deposito=%s"
        return self.execute_query(sql, (usuario_modificacion, id_deposito), commit=True) > 0
