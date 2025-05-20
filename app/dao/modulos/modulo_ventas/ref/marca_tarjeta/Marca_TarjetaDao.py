from flask import current_app as app
from app.conexion.Conexion import Conexion

class MarcaTarjetaDao:

    def getMarcaTarjeta(self):
        marcaTarjetaSQL = """
        SELECT id_marca_tarjeta, descripcion
        FROM marca_tarjeta
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(marcaTarjetaSQL)
            marcas_tarjeta = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id_marca_tarjeta': marca[0], 'descripcion': marca[1]} for marca in marcas_tarjeta]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las marcas de tarjeta: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMarcaTarjetaById(self, id_marca_tarjeta):
        marcaTarjetaSQL = """
        SELECT id_marca_tarjeta, descripcion
        FROM marca_tarjeta WHERE id_marca_tarjeta=%s
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(marcaTarjetaSQL, (id_marca_tarjeta,))
            marcaEncontrada = cur.fetchone()  # Obtener una sola fila
            if marcaEncontrada:
                return {
                    "id_marca_tarjeta": marcaEncontrada[0],
                    "descripcion": marcaEncontrada[1]
                }  # Retornar los datos de la marca de tarjeta
            else:
                return None  # Retornar None si no se encuentra la marca de tarjeta
        except Exception as e:
            app.logger.error(f"Error al obtener marca de tarjeta: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMarcaTarjeta(self, descripcion):
        insertMarcaTarjetaSQL = """
        INSERT INTO marca_tarjeta(descripcion) VALUES(%s) RETURNING id_marca_tarjeta
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertMarcaTarjetaSQL, (descripcion,))
            marca_tarjeta_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return marca_tarjeta_id

        except Exception as e:
            app.logger.error(f"Error al insertar marca de tarjeta: {str(e)}")
            con.rollback()  # Revertir si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateMarcaTarjeta(self, id_marca_tarjeta, descripcion):
        updateMarcaTarjetaSQL = """
        UPDATE marca_tarjeta
        SET descripcion=%s
        WHERE id_marca_tarjeta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMarcaTarjetaSQL, (descripcion, id_marca_tarjeta))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar marca de tarjeta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMarcaTarjeta(self, id_marca_tarjeta):
        deleteMarcaTarjetaSQL = """
        DELETE FROM marca_tarjeta
        WHERE id_marca_tarjeta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMarcaTarjetaSQL, (id_marca_tarjeta,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar marca de tarjeta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
