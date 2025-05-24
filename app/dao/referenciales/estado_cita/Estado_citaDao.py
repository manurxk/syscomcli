# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class Estado_citaDao:

    def getEstado_citas(self):

        estado_citaSQL = """
        SELECT id_estado_cita, descripcion
        FROM estado_citas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estado_citaSQL)
            estado_citas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id_estado_cita': estado_cita[0], 'descripcion': estado_cita[1]} for estado_cita in estado_citas]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los estado_citas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEstado_citaById(self, id_estado_cita):

        estado_citaSQL = """
        SELECT id_estado_cita, descripcion
        FROM estado_citas WHERE id_estado_cita=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estado_citaSQL, (id_estado_cita,))
            estado_citaEncontrada = cur.fetchone()  # Obtener una sola fila
            if estado_citaEncontrada:
                return {
                    "id_estado_cita": estado_citaEncontrada[0],
                    "descripcion": estado_citaEncontrada[1]
                }  # Retornar los datos de la estado_cita
            else:
                return None  # Retornar None si no se encuentra la estado_cita
        except Exception as e:
            app.logger.error(f"Error al obtener estado_cita: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEstado_cita(self, descripcion):

        insertEstado_citaSQL = """
        INSERT INTO estado_citas(descripcion) VALUES(%s) RETURNING id_estado_cita        
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEstado_citaSQL, (descripcion,))
            estado_cita = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return estado_cita

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar estado_cita: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEstado_cita(self, id_estado_cita, descripcion):

        updateEstado_citaSQL = """
        UPDATE estado_citas
        SET descripcion=%s
        WHERE id_estado_cita=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEstado_citaSQL, (descripcion, id_estado_cita,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar estado_cita: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEstado_cita(self, id_estado_cita):

        deleteEstado_citaSQL = """
        DELETE FROM estado_citas
        WHERE id_estado_cita=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(deleteEstado_citaSQL, (id_estado_cita,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila
        except Exception as e:
            app.logger.error(f"Error al eliminar estado_cita: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
