import re
from app.core.base_dao import BaseDAO


class FormaCobroDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getFormasCobro(self):
        sql = """
            SELECT id_forma_cobro, des_forma_cobro, cod_forma_cobro,
                   requiere_entidad, permite_cuotas, est_forma_cobro
            FROM formas_cobro
            ORDER BY des_forma_cobro ASC
        """
        return self.execute_query(sql)

    def getFormaCobroById(self, id_forma_cobro):
        sql = """
            SELECT id_forma_cobro, des_forma_cobro, cod_forma_cobro,
                   requiere_entidad, permite_cuotas, est_forma_cobro
            FROM formas_cobro WHERE id_forma_cobro = %s
        """
        return self.execute_query_one(sql, (id_forma_cobro,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def formaCobroExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM formas_cobro WHERE LOWER(des_forma_cobro)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_forma_cobro != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def codigoExiste(self, codigo, excluir_id=None):
        sql = "SELECT 1 FROM formas_cobro WHERE UPPER(cod_forma_cobro)=UPPER(%s)"
        params = [codigo]
        if excluir_id:
            sql += " AND id_forma_cobro != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarFormaCobro(self, descripcion, codigo, requiere_entidad=False,
                          permite_cuotas=False, estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO formas_cobro (des_forma_cobro, cod_forma_cobro, requiere_entidad,
                                      permite_cuotas, est_forma_cobro, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_forma_cobro
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper(), requiere_entidad,
             permite_cuotas, estado, usuario_creacion),
            commit=True
        )
        return fila["id_forma_cobro"] if fila else None

    def updateFormaCobro(self, id_forma_cobro, descripcion, codigo, requiere_entidad=False,
                         permite_cuotas=False, estado=True, usuario_modificacion=None):
        sql = """
            UPDATE formas_cobro
            SET des_forma_cobro=%s, cod_forma_cobro=%s, requiere_entidad=%s,
                permite_cuotas=%s, est_forma_cobro=%s, usuario_modificacion=%s
            WHERE id_forma_cobro=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper(), requiere_entidad,
             permite_cuotas, estado, usuario_modificacion, id_forma_cobro),
            commit=True
        ) > 0

    def desactivarFormaCobro(self, id_forma_cobro, usuario_modificacion=None):
        sql = "UPDATE formas_cobro SET est_forma_cobro=FALSE, usuario_modificacion=%s WHERE id_forma_cobro=%s"
        return self.execute_query(sql, (usuario_modificacion, id_forma_cobro), commit=True) > 0
