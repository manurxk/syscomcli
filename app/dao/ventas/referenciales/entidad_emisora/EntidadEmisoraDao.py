import re
from app.core.base_dao import BaseDAO


class EntidadEmisoraDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEntidadesEmisoras(self):
        sql = """
            SELECT id_entidad_emisora, des_entidad_emisora, cod_entidad_emisora,
                   ruc_entidad, telefono_entidad, email_entidad, tipo_entidad, est_entidad_emisora
            FROM entidades_emisoras
            ORDER BY des_entidad_emisora ASC
        """
        return self.execute_query(sql)

    def getEntidadEmisoraById(self, id_entidad_emisora):
        sql = """
            SELECT id_entidad_emisora, des_entidad_emisora, cod_entidad_emisora,
                   ruc_entidad, telefono_entidad, email_entidad, tipo_entidad, est_entidad_emisora
            FROM entidades_emisoras WHERE id_entidad_emisora = %s
        """
        return self.execute_query_one(sql, (id_entidad_emisora,))

    def validarDescripcion(self, descripcion):
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .\-]+$", descripcion))

    def entidadEmisoraExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM entidades_emisoras WHERE LOWER(des_entidad_emisora)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_entidad_emisora != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarEntidadEmisora(self, descripcion, codigo=None, ruc=None, telefono=None,
                               email=None, tipo_entidad=None, estado=True,
                               usuario_creacion=None):
        sql = """
            INSERT INTO entidades_emisoras (des_entidad_emisora, cod_entidad_emisora,
                                            ruc_entidad, telefono_entidad, email_entidad,
                                            tipo_entidad, est_entidad_emisora, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_entidad_emisora
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             ruc, telefono, email,
             tipo_entidad.upper() if tipo_entidad else None,
             estado, usuario_creacion),
            commit=True
        )
        return fila["id_entidad_emisora"] if fila else None

    def updateEntidadEmisora(self, id_entidad_emisora, descripcion, codigo=None,
                              ruc=None, telefono=None, email=None, tipo_entidad=None,
                              estado=True, usuario_modificacion=None):
        sql = """
            UPDATE entidades_emisoras
            SET des_entidad_emisora=%s, cod_entidad_emisora=%s, ruc_entidad=%s,
                telefono_entidad=%s, email_entidad=%s, tipo_entidad=%s,
                est_entidad_emisora=%s, usuario_modificacion=%s
            WHERE id_entidad_emisora=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             ruc, telefono, email,
             tipo_entidad.upper() if tipo_entidad else None,
             estado, usuario_modificacion, id_entidad_emisora),
            commit=True
        ) > 0

    def desactivarEntidadEmisora(self, id_entidad_emisora, usuario_modificacion=None):
        sql = "UPDATE entidades_emisoras SET est_entidad_emisora=FALSE, usuario_modificacion=%s WHERE id_entidad_emisora=%s"
        return self.execute_query(sql, (usuario_modificacion, id_entidad_emisora), commit=True) > 0
