import re
from app.core.base_dao import BaseDAO


class ItemServicioDao(BaseDAO):
    """Acceso a datos de ítem de servicio (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getItemsServicios(self):
        """Lista los registros de ítem de servicio."""
        sql = """
            SELECT i.id_item_servicio, i.des_item_servicio, i.cod_item_servicio,
                   i.id_tipo_item, ti.des_tipo_item, i.item_precio_unitario,
                   i.id_moneda, m.des_moneda, i.aplica_impuesto,
                   i.id_tipo_impuesto, imp.des_tipo_impuesto, i.est_item_servicio
            FROM items_servicios i
            JOIN tipos_items ti ON i.id_tipo_item = ti.id_tipo_item
            LEFT JOIN monedas m ON i.id_moneda = m.id_moneda
            LEFT JOIN tipos_impuestos imp ON i.id_tipo_impuesto = imp.id_tipo_impuesto
            ORDER BY i.des_item_servicio ASC
        """
        return self.execute_query(sql)

    def getItemServicioById(self, id_item_servicio):
        """Devuelve el registro de ítem de servicio por su id, o None si no existe."""
        sql = """
            SELECT id_item_servicio, des_item_servicio, cod_item_servicio,
                   id_tipo_item, item_precio_unitario, id_moneda,
                   aplica_impuesto, id_tipo_impuesto, est_item_servicio
            FROM items_servicios WHERE id_item_servicio = %s
        """
        return self.execute_query_one(sql, (id_item_servicio,))

    def validarDescripcion(self, descripcion):
        """Indica si la descripción solo contiene caracteres permitidos."""
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .\-]+$", descripcion))

    def itemServicioExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de ítem de servicio con ese valor; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM items_servicios WHERE UPPER(des_item_servicio) = UPPER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_item_servicio != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarItemServicio(self, descripcion, id_tipo_item, codigo=None, precio_unitario=0,
                            id_moneda=None, aplica_impuesto=False, id_tipo_impuesto=None,
                            estado=True, usuario_creacion=None):
        """Inserta un registro de ítem de servicio y devuelve el id generado."""
        sql = """
            INSERT INTO items_servicios (des_item_servicio, cod_item_servicio, id_tipo_item,
                                         item_precio_unitario, id_moneda, aplica_impuesto,
                                         id_tipo_impuesto, est_item_servicio, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_item_servicio
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo, id_tipo_item, precio_unitario, id_moneda,
             aplica_impuesto, id_tipo_impuesto if aplica_impuesto else None, estado, usuario_creacion),
            commit=True
        )
        return fila["id_item_servicio"] if fila else None

    def updateItemServicio(self, id_item_servicio, descripcion, id_tipo_item, codigo=None,
                           precio_unitario=0, id_moneda=None, aplica_impuesto=False,
                           id_tipo_impuesto=None, estado=True, usuario_modificacion=None):
        """Actualiza los datos de ítem de servicio; devuelve True si modificó una fila."""
        sql = """
            UPDATE items_servicios
            SET des_item_servicio=%s, cod_item_servicio=%s, id_tipo_item=%s,
                item_precio_unitario=%s, id_moneda=%s, aplica_impuesto=%s,
                id_tipo_impuesto=%s, est_item_servicio=%s, usuario_modificacion=%s
            WHERE id_item_servicio=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo, id_tipo_item, precio_unitario, id_moneda,
             aplica_impuesto, id_tipo_impuesto if aplica_impuesto else None, estado,
             usuario_modificacion, id_item_servicio),
            commit=True
        ) > 0

    def desactivarItemServicio(self, id_item_servicio, usuario_modificacion=None):
        """Da de baja (lógica) el registro de ítem de servicio; devuelve True si modificó una fila."""
        sql = "UPDATE items_servicios SET est_item_servicio=FALSE, usuario_modificacion=%s WHERE id_item_servicio=%s"
        return self.execute_query(sql, (usuario_modificacion, id_item_servicio), commit=True) > 0
