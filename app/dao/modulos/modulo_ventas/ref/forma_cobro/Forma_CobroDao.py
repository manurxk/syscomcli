from flask import current_app as app
from app.conexion.Conexion import Conexion

class FormaCobroDao:

    def getFormaCobro(self):
        formaCobroSQL = """
        SELECT id_forma_cobro, descripcion
        FROM formas_cobro
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(formaCobroSQL)
            formas_cobro = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id_forma_cobro': forma[0], 'descripcion': forma[1]} for forma in formas_cobro]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las formas de cobro: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getFormaCobroById(self, id_forma_cobro):
        formaCobroSQL = """
        SELECT id_forma_cobro, descripcion
        FROM formas_cobro WHERE id_forma_cobro=%s
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(formaCobroSQL, (id_forma_cobro,))
            formaEncontrada = cur.fetchone()  # Obtener una sola fila
            if formaEncontrada:
                return {
                    "id_forma_cobro": formaEncontrada[0],
                    "descripcion": formaEncontrada[1]
                }  # Retornar los datos de la forma de cobro
            else:
                return None  # Retornar None si no se encuentra la forma de cobro
        except Exception as e:
            app.logger.error(f"Error al obtener forma de cobro: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarFormaCobro(self, descripcion):
        insertFormaCobroSQL = """
        INSERT INTO formas_cobro(descripcion) VALUES(%s) RETURNING id_forma_cobro
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertFormaCobroSQL, (descripcion,))
            forma_cobro_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return forma_cobro_id

        except Exception as e:
            app.logger.error(f"Error al insertar forma de cobro: {str(e)}")
            con.rollback()  # Revertir si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateFormaCobro(self, id_forma_cobro, descripcion):
        updateFormaCobroSQL = """
        UPDATE formas_cobro
        SET descripcion=%s
        WHERE id_forma_cobro=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateFormaCobroSQL, (descripcion, id_forma_cobro))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar forma de cobro: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteFormaCobro(self, id_forma_cobro):
        deleteFormaCobroSQL = """
        DELETE FROM formas_cobro
        WHERE id_forma_cobro=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteFormaCobroSQL, (id_forma_cobro,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar forma de cobro: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
