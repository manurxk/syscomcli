from flask import current_app as app
from app.conexion.Conexion import Conexion

class UbicacionDao:

    def getUbicaciones(self):

        ubicacionSQL = """
        SELECT id_ubicacion, descripcion
        FROM ubicaciones
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ubicacionSQL)
            ubicaciones = cur.fetchall()

            return [{'id_ubicacion': ubicacion[0], 'descripcion': ubicacion[1]} for ubicacion in ubicaciones]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las ubicaciones: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getUbicacionById(self, id_ubicacion):

        ubicacionSQL = """
        SELECT id_ubicacion, descripcion
        FROM ubicaciones WHERE id_ubicacion=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ubicacionSQL, (id_ubicacion,))
            ubicacionEncontrada = cur.fetchone()
            if ubicacionEncontrada:
                return {
                    "id_ubicacion": ubicacionEncontrada[0],
                    "descripcion": ubicacionEncontrada[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener ubicacion: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarUbicacion(self, descripcion):

        insertUbicacionSQL = """
        INSERT INTO ubicaciones(descripcion) VALUES(%s) RETURNING id_ubicacion
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertUbicacionSQL, (descripcion,))
            ubicacion_id = cur.fetchone()[0]
            con.commit()
            return ubicacion_id

        except Exception as e:
            app.logger.error(f"Error al insertar ubicacion: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateUbicacion(self, id_ubicacion, descripcion):

        updateUbicacionSQL = """
        UPDATE ubicaciones
        SET descripcion=%s
        WHERE id_ubicacion=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateUbicacionSQL, (descripcion, id_ubicacion))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar ubicacion: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteUbicacion(self, id_ubicacion):

        deleteUbicacionSQL = """
        DELETE FROM ubicaciones
        WHERE id_ubicacion=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteUbicacionSQL, (id_ubicacion,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar ubicacion: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
