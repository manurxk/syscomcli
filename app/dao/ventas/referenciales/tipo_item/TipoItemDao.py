import re
from app.core.base_dao import BaseDAO


class TipoItemDao(BaseDAO):
    """Acceso a datos de tipo de ítem (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getTiposItems(self):
        """Lista los registros de tipo de ítem."""
        sql = """
            SELECT id_tipo_item, des_tipo_item, cod_tipo_item,
                   tipo_item_categoria, requiere_stock, est_tipo_item
            FROM tipos_items
            ORDER BY des_tipo_item ASC
        """
        return self.execute_query(sql)

    def getTipoItemById(self, id_tipo_item):
        """Devuelve el registro de tipo de ítem por su id, o None si no existe."""
        sql = """
            SELECT id_tipo_item, des_tipo_item, cod_tipo_item,
                   tipo_item_categoria, requiere_stock, est_tipo_item
            FROM tipos_items WHERE id_tipo_item = %s
        """
        return self.execute_query_one(sql, (id_tipo_item,))

    def validarDescripcion(self, descripcion):
        """Indica si la descripción solo contiene caracteres permitidos."""
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def tipoItemExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de tipo de ítem con ese valor; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM tipos_items WHERE LOWER(des_tipo_item)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_tipo_item != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarTipoItem(self, descripcion, codigo=None, categoria=None,
                        requiere_stock=False, estado=True, usuario_creacion=None):
        """Inserta un registro de tipo de ítem y devuelve el id generado."""
        sql = """
            INSERT INTO tipos_items (des_tipo_item, cod_tipo_item, tipo_item_categoria,
                                     requiere_stock, est_tipo_item, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_tipo_item
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             categoria.upper() if categoria else None,
             requiere_stock, estado, usuario_creacion),
            commit=True
        )
        return fila["id_tipo_item"] if fila else None

    def updateTipoItem(self, id_tipo_item, descripcion, codigo=None, categoria=None,
                       requiere_stock=False, estado=True, usuario_modificacion=None):
        """Actualiza los datos de tipo de ítem; devuelve True si modificó una fila."""
        sql = """
            UPDATE tipos_items
            SET des_tipo_item=%s, cod_tipo_item=%s, tipo_item_categoria=%s,
                requiere_stock=%s, est_tipo_item=%s, usuario_modificacion=%s
            WHERE id_tipo_item=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             categoria.upper() if categoria else None,
             requiere_stock, estado, usuario_modificacion, id_tipo_item),
            commit=True
        ) > 0

    def desactivarTipoItem(self, id_tipo_item, usuario_modificacion=None):
        """Da de baja (lógica) el registro de tipo de ítem; devuelve True si modificó una fila."""
        sql = "UPDATE tipos_items SET est_tipo_item=FALSE, usuario_modificacion=%s WHERE id_tipo_item=%s"
        return self.execute_query(sql, (usuario_modificacion, id_tipo_item), commit=True) > 0
