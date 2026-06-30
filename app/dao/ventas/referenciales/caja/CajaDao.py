import re
from app.core.base_dao import BaseDAO


class CajaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getCajas(self):
        sql = """
            SELECT id_caja, des_caja, cod_caja, caja_saldo_inicial,
                   caja_saldo_actual, caja_estado, est_caja
            FROM cajas
            ORDER BY des_caja ASC
        """
        return self.execute_query(sql)

    def getCajaById(self, id_caja):
        sql = """
            SELECT id_caja, des_caja, cod_caja, caja_saldo_inicial,
                   caja_saldo_actual, caja_estado, est_caja
            FROM cajas WHERE id_caja = %s
        """
        return self.execute_query_one(sql, (id_caja,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .\-]+$", descripcion))

    def cajaExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM cajas WHERE LOWER(des_caja)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_caja != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarCaja(self, descripcion, codigo=None, saldo_inicial=0,
                    estado_caja='CERRADA', estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO cajas (des_caja, cod_caja, caja_saldo_inicial, caja_saldo_actual,
                               caja_estado, est_caja, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_caja
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             saldo_inicial, saldo_inicial, estado_caja, estado, usuario_creacion),
            commit=True
        )
        return fila["id_caja"] if fila else None

    def updateCaja(self, id_caja, descripcion, codigo=None, saldo_inicial=None,
                   estado_caja=None, estado=True, usuario_modificacion=None):
        sql = """
            UPDATE cajas
            SET des_caja=%s, cod_caja=%s, est_caja=%s, usuario_modificacion=%s
        """
        params = [descripcion, codigo.upper() if codigo else None, estado, usuario_modificacion]

        if saldo_inicial is not None:
            sql += ", caja_saldo_inicial=%s"
            params.append(saldo_inicial)

        if estado_caja is not None:
            sql += ", caja_estado=%s"
            params.append(estado_caja)

        sql += " WHERE id_caja=%s"
        params.append(id_caja)

        return self.execute_query(sql, tuple(params), commit=True) > 0

    def desactivarCaja(self, id_caja, usuario_modificacion=None):
        sql = "UPDATE cajas SET est_caja=FALSE, usuario_modificacion=%s WHERE id_caja=%s"
        return self.execute_query(sql, (usuario_modificacion, id_caja), commit=True) > 0
