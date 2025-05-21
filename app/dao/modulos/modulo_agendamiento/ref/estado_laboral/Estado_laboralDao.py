# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class Estado_laboralDao:

    def getEstado_laborales(self):

        estado_laboralSQL = """
        SELECT id_estado_laboral, descripcion
        FROM estado_laborales
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estado_laboralSQL)
            estado_laborales = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id_estado_laboral': estado_laboral[0], 'descripcion': estado_laboral[1]} for estado_laboral in estado_laborales]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los estado_laborales: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEstado_laboralById(self, id_estado_laboral):

        estado_laboralSQL = """
        SELECT id_estado_laboral, descripcion
        FROM estado_laborales WHERE id_estado_laboral=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estado_laboralSQL, (id_estado_laboral,))
            estado_laboralEncontrado = cur.fetchone()  # Obtener una sola fila
            if estado_laboralEncontrado:
                return {
                        "id_estado_laboral": estado_laboralEncontrado[0],
                        "descripcion": estado_laboralEncontrado[1]
                    }  # Retornar los datos del estado laboral
            else:
                return None  # Retornar None si no se encuentra el estado laboral
        except Exception as e:
            app.logger.error(f"Error al obtener estado_laboral: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEstado_laboral(self, descripcion):

        insertEstado_laboralSQL = """
        INSERT INTO estado_laborales(descripcion) VALUES(%s) RETURNING id_estado_laboral        
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEstado_laboralSQL, (descripcion,))
            estado_laboral = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return estado_laboral

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar estado_laboral: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEstado_laboral(self, id_estado_laboral, descripcion):

        updateEstado_laboralSQL = """
        UPDATE estado_laborales
        SET descripcion=%s
        WHERE id_estado_laboral=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEstado_laboralSQL, (descripcion, id_estado_laboral,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar estado_laboral: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEstado_laboral(self, id_estado_laboral):

        deleteEstado_laboralSQL = """
        DELETE FROM estado_laborales
        WHERE id_estado_laboral=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(deleteEstado_laboralSQL, (id_estado_laboral,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila        
        except Exception as e:
            app.logger.error(f"Error al eliminar estado_laboral: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
