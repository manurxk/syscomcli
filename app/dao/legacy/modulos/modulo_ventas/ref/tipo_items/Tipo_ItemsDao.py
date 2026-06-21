from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoItemsDao:

    def getTipoItems(self):
        tipoItemsSQL = """
        SELECT id_tipo_item, descripcion
        FROM tipo_items
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoItemsSQL)
            tipos_items = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id_tipo_item': tipo[0], 'descripcion': tipo[1]} for tipo in tipos_items]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de items: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTipoItemsById(self, id_tipo_item):
        tipoItemsSQL = """
        SELECT id_tipo_item, descripcion
        FROM tipo_items WHERE id_tipo_item=%s
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoItemsSQL, (id_tipo_item,))
            tipoEncontrado = cur.fetchone()  # Obtener una sola fila
            if tipoEncontrado:
                return {
                    "id_tipo_item": tipoEncontrado[0],
                    "descripcion": tipoEncontrado[1]
                }  # Retornar los datos del tipo de item
            else:
                return None  # Retornar None si no se encuentra el tipo de item
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de item: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTipoItems(self, descripcion):
        insertTipoItemsSQL = """
        INSERT INTO tipo_items(descripcion) VALUES(%s) RETURNING id_tipo_item
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTipoItemsSQL, (descripcion,))
            tipo_item_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return tipo_item_id

        except Exception as e:
            app.logger.error(f"Error al insertar tipo de item: {str(e)}")
            con.rollback()  # Revertir si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateTipoItems(self, id_tipo_item, descripcion):
        updateTipoItemsSQL = """
        UPDATE tipo_items
        SET descripcion=%s
        WHERE id_tipo_item=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipoItemsSQL, (descripcion, id_tipo_item))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de item: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTipoItems(self, id_tipo_item):
        deleteTipoItemsSQL = """
        DELETE FROM tipo_items
        WHERE id_tipo_item=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTipoItemsSQL, (id_tipo_item,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de item: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
