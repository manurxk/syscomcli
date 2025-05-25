# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class GeneroDao:

    def getGeneros(self):

        generoSQL = """
        SELECT id_genero, descripcion
        FROM generos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(generoSQL)
            generos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id_genero': genero[0], 'descripcion': genero[1]} for genero in generos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los generos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getGeneroById(self, id_genero):

        generoSQL = """
        SELECT id_genero, descripcion
        FROM generos WHERE id_genero=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(generoSQL, (id_genero,))
            generoEncontrada = cur.fetchone()  # Obtener una sola fila
            if generoEncontrada:
                return {
                        "id_genero": generoEncontrada[0],
                        "descripcion": generoEncontrada[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None  # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener genero: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarGenero(self, descripcion):

        insertGeneroSQL = """
        INSERT INTO generos(descripcion) VALUES(%s) RETURNING id_genero        
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertGeneroSQL, (descripcion,))
            genero_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return genero_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar genero: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateGenero(self, id_genero, descripcion):

        updateGeneroSQL = """
        UPDATE generos
        SET descripcion=%s
        WHERE id_genero=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateGeneroSQL, (descripcion, id_genero,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar genero: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteGenero(self, id_genero):

        deleteGeneroSQL = """
        DELETE FROM generos
        WHERE id_genero=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(deleteGeneroSQL, (id_genero,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila
        except Exception as e:
            app.logger.error(f"Error al eliminar genero: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
