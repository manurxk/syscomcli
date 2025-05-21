from flask import current_app as app
from app.conexion.Conexion import Conexion

class FichaDao:

    def getFichas(self):
        fichaSQL = """
        SELECT id_ficha, descripcion
        FROM fichas
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(fichaSQL)
            fichas = cur.fetchall()  # Obtener datos de la base de datos

            # Transformar los datos en una lista de diccionarios
            return [{'id_ficha': ficha[0], 'descripcion': ficha[1]} for ficha in fichas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las fichas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getFichaById(self, id_ficha):
        fichaSQL = """
        SELECT id_ficha, descripcion
        FROM fichas WHERE id_ficha=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(fichaSQL, (id_ficha,))
            fichaEncontrada = cur.fetchone()  # Obtener una sola fila
            if fichaEncontrada:
                return {
                    "id_ficha": fichaEncontrada[0],
                    "descripcion": fichaEncontrada[1]
                }  # Retornar los datos de la ficha
            else:
                return None  # Retornar None si no se encuentra la ficha

        except Exception as e:
            app.logger.error(f"Error al obtener ficha: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarFicha(self, descripcion):
        insertFichaSQL = """
        INSERT INTO fichas(descripcion) VALUES(%s) RETURNING id_ficha
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertFichaSQL, (descripcion,))
            ficha_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return ficha_id

        except Exception as e:
            app.logger.error(f"Error al insertar ficha: {str(e)}")
            con.rollback()  # Revertir si hubo un error
            return False

        finally:
            cur.close()
            con.close()

    def updateFicha(self, id_ficha, descripcion):
        updateFichaSQL = """
        UPDATE fichas
        SET descripcion=%s
        WHERE id_ficha=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateFichaSQL, (descripcion, id_ficha))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar ficha: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteFicha(self, id_ficha):
        deleteFichaSQL = """
        DELETE FROM fichas
        WHERE id_ficha=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteFichaSQL, (id_ficha,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar ficha: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
