# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CiudadDao:

    def getCiudades(self):

        ciudadSQL = """
        SELECT id_ciudad, descripcion
        FROM ciudades
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ciudadSQL)
            ciudades = cur.fetchall()  # Traer datos de la base de datos

            # Transformar los datos en una lista de diccionarios
            return [{'id_ciudad': ciudad[0], 'descripcion': ciudad[1]} for ciudad in ciudades]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las ciudades: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCiudadById(self, id_ciudad):

        ciudadSQL = """
        SELECT id_ciudad, descripcion
        FROM ciudades WHERE id_ciudad=%s
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ciudadSQL, (id_ciudad,))
            ciudadEncontrada = cur.fetchone()  # Obtener una sola fila
            if ciudadEncontrada:
                return {
                    "id_ciudad": ciudadEncontrada[0],
                    "descripcion": ciudadEncontrada[1]
                }  # Retornar los datos de la ciudad
            else:
                return None  # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener ciudad: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCiudad(self, descripcion):

        insertCiudadSQL = """
        INSERT INTO ciudades(descripcion) VALUES(%s) RETURNING id_ciudad
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertCiudadSQL, (descripcion,))
            ciudad_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return ciudad_id

        except Exception as e:
            app.logger.error(f"Error al insertar ciudad: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateCiudad(self, id_ciudad, descripcion):

        updateCiudadSQL = """
        UPDATE ciudades
        SET descripcion=%s
        WHERE id_ciudad=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCiudadSQL, (descripcion, id_ciudad))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar ciudad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCiudad(self, id_ciudad):

        deleteCiudadSQL = """
        DELETE FROM ciudades
        WHERE id_ciudad=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteCiudadSQL, (id_ciudad,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila
        except Exception as e:
            app.logger.error(f"Error al eliminar ciudad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
