import re

from app.core.base_dao import BaseDAO


class InsumoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def validarDescripcion(self, descripcion):
        """Misma regla que las otras 8 entidades del módulo: letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def getInsumos(self):
        sql = """
            SELECT id_insumo, des_insumo, insumo_unidad_medida, stock_actual,
                   stock_minimo, insumo_precio_unitario, est_insumo
            FROM insumos
            ORDER BY des_insumo
        """
        return self.execute_query(sql)

    def getInsumoById(self, insumo_id):
        sql = """
            SELECT id_insumo, des_insumo, insumo_unidad_medida, stock_actual,
                   stock_minimo, insumo_precio_unitario, est_insumo
            FROM insumos
            WHERE id_insumo = %s
        """
        return self.execute_query_one(sql, (insumo_id,))

    def insumoExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM insumos WHERE LOWER(des_insumo) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_insumo != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarInsumo(self, des_insumo, insumo_unidad_medida, stock_actual, stock_minimo,
                       insumo_precio_unitario, estado, usuario_creacion=None):
        sql = """
            INSERT INTO insumos (
                des_insumo, insumo_unidad_medida, stock_actual, stock_minimo,
                insumo_precio_unitario, est_insumo, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_insumo
        """
        fila = self.execute_query_one(sql, (
            des_insumo, insumo_unidad_medida, stock_actual, stock_minimo,
            insumo_precio_unitario, estado, usuario_creacion,
        ), commit=True)
        return fila["id_insumo"] if fila else None

    def updateInsumo(self, insumo_id, des_insumo, insumo_unidad_medida, stock_actual, stock_minimo,
                      insumo_precio_unitario, estado, usuario_modificacion=None):
        sql = """
            UPDATE insumos SET
                des_insumo = %s, insumo_unidad_medida = %s, stock_actual = %s,
                stock_minimo = %s, insumo_precio_unitario = %s, est_insumo = %s,
                usuario_modificacion = %s
            WHERE id_insumo = %s
        """
        return self.execute_query(sql, (
            des_insumo, insumo_unidad_medida, stock_actual, stock_minimo,
            insumo_precio_unitario, estado, usuario_modificacion, insumo_id,
        ), commit=True) > 0

    def desactivarInsumo(self, insumo_id, usuario_modificacion=None):
        sql = """
            UPDATE insumos SET est_insumo = FALSE, usuario_modificacion = %s
            WHERE id_insumo = %s
        """
        return self.execute_query(sql, (usuario_modificacion, insumo_id), commit=True) > 0
