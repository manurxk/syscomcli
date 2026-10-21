import re
from app.core.base_dao import BaseDAO


class MarcaTarjetaDao(BaseDAO):
    """Acceso a datos de marca de tarjeta (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getMarcasTarjeta(self):
        """Lista los registros de marca de tarjeta."""
        sql = """
            SELECT id_marca_tarjeta, des_marca_tarjeta, cod_marca_tarjeta, est_marca_tarjeta
            FROM marcas_tarjeta
            ORDER BY des_marca_tarjeta ASC
        """
        return self.execute_query(sql)

    def getMarcaTarjetaById(self, id_marca_tarjeta):
        """Devuelve el registro de marca de tarjeta por su id, o None si no existe."""
        sql = """
            SELECT id_marca_tarjeta, des_marca_tarjeta, cod_marca_tarjeta, est_marca_tarjeta
            FROM marcas_tarjeta WHERE id_marca_tarjeta = %s
        """
        return self.execute_query_one(sql, (id_marca_tarjeta,))

    def validarDescripcion(self, descripcion):
        """Indica si la descripción solo contiene caracteres permitidos."""
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def marcaTarjetaExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de marca de tarjeta con ese valor; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM marcas_tarjeta WHERE LOWER(des_marca_tarjeta)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_marca_tarjeta != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarMarcaTarjeta(self, descripcion, codigo=None, estado=True, usuario_creacion=None):
        """Inserta un registro de marca de tarjeta y devuelve el id generado."""
        sql = """
            INSERT INTO marcas_tarjeta (des_marca_tarjeta, cod_marca_tarjeta,
                                        est_marca_tarjeta, usuario_creacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_marca_tarjeta
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None, estado, usuario_creacion),
            commit=True
        )
        return fila["id_marca_tarjeta"] if fila else None

    def updateMarcaTarjeta(self, id_marca_tarjeta, descripcion, codigo=None,
                            estado=True, usuario_modificacion=None):
        """Actualiza los datos de marca de tarjeta; devuelve True si modificó una fila."""
        sql = """
            UPDATE marcas_tarjeta
            SET des_marca_tarjeta=%s, cod_marca_tarjeta=%s,
                est_marca_tarjeta=%s, usuario_modificacion=%s
            WHERE id_marca_tarjeta=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             estado, usuario_modificacion, id_marca_tarjeta),
            commit=True
        ) > 0

    def desactivarMarcaTarjeta(self, id_marca_tarjeta, usuario_modificacion=None):
        """Da de baja (lógica) el registro de marca de tarjeta; devuelve True si modificó una fila."""
        sql = "UPDATE marcas_tarjeta SET est_marca_tarjeta=FALSE, usuario_modificacion=%s WHERE id_marca_tarjeta=%s"
        return self.execute_query(sql, (usuario_modificacion, id_marca_tarjeta), commit=True) > 0
