import re
from app.core.base_dao import BaseDAO


class EstadoFacturaDao(BaseDAO):
    """Acceso a datos de estado de factura (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEstadosFactura(self):
        """Lista los registros de estado de factura."""
        sql = """
            SELECT id_estado_factura, des_estado_factura, cod_estado_factura,
                   permite_modificacion, permite_anulacion, color_estado, est_estado_factura
            FROM estados_factura
            ORDER BY des_estado_factura ASC
        """
        return self.execute_query(sql)

    def getEstadoFacturaById(self, id_estado_factura):
        """Devuelve el registro de estado de factura por su id, o None si no existe."""
        sql = """
            SELECT id_estado_factura, des_estado_factura, cod_estado_factura,
                   permite_modificacion, permite_anulacion, color_estado, est_estado_factura
            FROM estados_factura WHERE id_estado_factura = %s
        """
        return self.execute_query_one(sql, (id_estado_factura,))

    def validarDescripcion(self, descripcion):
        """Indica si la descripción solo contiene caracteres permitidos."""
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$", descripcion))

    def estadoFacturaExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de estado de factura con ese valor; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM estados_factura WHERE LOWER(des_estado_factura)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_estado_factura != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarEstadoFactura(self, descripcion, codigo=None, permite_modificacion=True,
                              permite_anulacion=True, color='secondary',
                              estado=True, usuario_creacion=None):
        """Inserta un registro de estado de factura y devuelve el id generado."""
        sql = """
            INSERT INTO estados_factura (des_estado_factura, cod_estado_factura,
                                         permite_modificacion, permite_anulacion,
                                         color_estado, est_estado_factura, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_estado_factura
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             permite_modificacion, permite_anulacion, color, estado, usuario_creacion),
            commit=True
        )
        return fila["id_estado_factura"] if fila else None

    def updateEstadoFactura(self, id_estado_factura, descripcion, codigo=None,
                             permite_modificacion=True, permite_anulacion=True,
                             color='secondary', estado=True, usuario_modificacion=None):
        """Actualiza los datos de estado de factura; devuelve True si modificó una fila."""
        sql = """
            UPDATE estados_factura
            SET des_estado_factura=%s, cod_estado_factura=%s, permite_modificacion=%s,
                permite_anulacion=%s, color_estado=%s, est_estado_factura=%s,
                usuario_modificacion=%s
            WHERE id_estado_factura=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             permite_modificacion, permite_anulacion, color,
             estado, usuario_modificacion, id_estado_factura),
            commit=True
        ) > 0

    def desactivarEstadoFactura(self, id_estado_factura, usuario_modificacion=None):
        """Da de baja (lógica) el registro de estado de factura; devuelve True si modificó una fila."""
        sql = "UPDATE estados_factura SET est_estado_factura=FALSE, usuario_modificacion=%s WHERE id_estado_factura=%s"
        return self.execute_query(sql, (usuario_modificacion, id_estado_factura), commit=True) > 0
