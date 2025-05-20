# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class SintomaDao:

    def getSintomas(self):

        sintomaSQL = """
        SELECT id, descripcion
        FROM sintomas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sintomaSQL)
            sintomas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': sintoma[0], 'descripcion': sintoma[1]} for sintoma in sintomas]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los sintomas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getSintomaById(self, id):

        sintomaSQL = """
        SELECT id, descripcion
        FROM sintomas WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sintomaSQL, (id,))
            sintomaEncontrado = cur.fetchone()  # Obtener una sola fila
            if sintomaEncontrado:
                return {
                    "id": sintomaEncontrado[0],
                    "descripcion": sintomaEncontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener sintoma: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarSintoma(self, descripcion):

        insertSintomaSQL = """
        INSERT INTO sintomas(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertSintomaSQL, (descripcion,))
            sintoma_id = cur.fetchone()[0]
            con.commit()
            return sintoma_id

        except Exception as e:
            app.logger.error(f"Error al insertar sintoma: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateSintoma(self, id, descripcion):

        updateSintomaSQL = """
        UPDATE sintomas
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateSintomaSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar sintoma: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteSintoma(self, id):

        deleteSintomaSQL = """
        DELETE FROM sintomas
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteSintomaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar sintoma: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
