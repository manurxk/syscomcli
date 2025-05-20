from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoImpuestoDao:

    def getTipoImpuesto(self):
        tipoImpuestoSQL = """
        SELECT id_tipo_impuesto, descripcion
        FROM tipo_impuesto
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoImpuestoSQL)
            tipos_impuestos = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id_tipo_impuesto': impuesto[0], 'descripcion': impuesto[1]} for impuesto in tipos_impuestos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de impuesto: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTipoImpuestoById(self, id_tipo_impuesto):
        tipoImpuestoSQL = """
        SELECT id_tipo_impuesto, descripcion
        FROM tipo_impuesto WHERE id_tipo_impuesto=%s
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoImpuestoSQL, (id_tipo_impuesto,))
            impuestoEncontrado = cur.fetchone()  # Obtener una sola fila
            if impuestoEncontrado:
                return {
                    "id_tipo_impuesto": impuestoEncontrado[0],
                    "descripcion": impuestoEncontrado[1]
                }  # Retornar los datos del tipo de impuesto
            else:
                return None  # Retornar None si no se encuentra el tipo de impuesto
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de impuesto: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTipoImpuesto(self, descripcion):
        insertTipoImpuestoSQL = """
        INSERT INTO tipo_impuesto(descripcion) VALUES(%s) RETURNING id_tipo_impuesto
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTipoImpuestoSQL, (descripcion,))
            tipo_impuesto_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return tipo_impuesto_id

        except Exception as e:
            app.logger.error(f"Error al insertar tipo de impuesto: {str(e)}")
            con.rollback()  # Revertir si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateTipoImpuesto(self, id_tipo_impuesto, descripcion):
        updateTipoImpuestoSQL = """
        UPDATE tipo_impuesto
        SET descripcion=%s
        WHERE id_tipo_impuesto=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipoImpuestoSQL, (descripcion, id_tipo_impuesto))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de impuesto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTipoImpuesto(self, id_tipo_impuesto):
        deleteTipoImpuestoSQL = """
        DELETE FROM tipo_impuesto
        WHERE id_tipo_impuesto=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTipoImpuestoSQL, (id_tipo_impuesto,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de impuesto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
