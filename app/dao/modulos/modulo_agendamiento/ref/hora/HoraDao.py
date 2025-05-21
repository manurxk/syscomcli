# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class HoraDao:

    def getHoras(self):

        horaSQL = """
        SELECT id, descripcion
        FROM horas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(horaSQL)
            horas = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': hora[0], 'descripcion': hora[1]} for hora in horas]

        except Exception as e:
            app.logger.error(f"Error al obtener todos las horas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getHoraById(self, id):

        horaSQL = """
        SELECT id, descripcion
        FROM horas WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(horaSQL, (id,))
            horaEncontrada = cur.fetchone() # Obtener una sola fila
            if horaEncontrada:
                return {
                        "id": horaEncontrada[0],
                        "descripcion": horaEncontrada[1]
                    }  # Retornar los datos de la medico
            else:
                return None # Retornar None si no se encuentra la medico
        except Exception as e:
            app.logger.error(f"Error al obtener horas: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarHora(self, descripcion):

        insertHoraSQL = """
   INSERT INTO horas(descripcion) VALUES(%s) RETURNING id        
   """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertHoraSQL, (descripcion,))
            hora_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return hora_id
        
        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar hora: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

          # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateHora(self, id, descripcion):

        updateHoraSQL = """
        UPDATE horas
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateHoraSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas            con.commit()
            con.commit()
        
            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar hora: {str(e)}")
            con.rollback()
            return False 
               
        finally:
            cur.close()
            con.close()

    def deleteHora(self, id):

        updateHoraSQL = """
        DELETE FROM horas
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(updateHoraSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila        
        except Exception as e:
            app.logger.error(f"Error al eliminar hora: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

