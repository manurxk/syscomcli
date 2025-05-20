# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class Sala_atencionDao:

    def getSala_atenciones(self):
        sala_atencionSQL = """
        SELECT id_sala_atencion, nombre
        FROM sala_atenciones
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sala_atencionSQL)
            sala_atenciones = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id_sala_atencion': sala[0], 'nombre': sala[1]} for sala in sala_atenciones]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las sala_atenciones: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getSala_atencionById(self, id):
        sala_atencionSQL = """
        SELECT id_sala_atencion, nombre
        FROM sala_atenciones WHERE id_sala_atencion=%s
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sala_atencionSQL, (id,))
            sala_atencionEncontrada = cur.fetchone()  # Obtener una sola fila
            if sala_atencionEncontrada:
                return {
                    "id_sala_atencion": sala_atencionEncontrada[0],
                    "nombre": sala_atencionEncontrada[1]
                }  # Retornar los datos de la sala de atención
            else:
                return None  # Retornar None si no se encuentra la sala
        except Exception as e:
            app.logger.error(f"Error al obtener sala_atencion: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarSala_atencion(self, nombre):
        insertSala_atencionSQL = """
        INSERT INTO sala_atenciones(nombre) VALUES(%s) RETURNING id_sala_atencion        
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecución exitosa
        try:
            cur.execute(insertSala_atencionSQL, (nombre,))
            sala_atencion = cur.fetchone()[0]
            con.commit()  # Se confirma la inserción
            return sala_atencion
        
        # Si algo falló entra aquí
        except Exception as e:
            app.logger.error(f"Error al insertar sala_atencion: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        # Siempre se va a ejecutar
        finally:
            cur.close()
            con.close()

    def updateSala_atencion(self, id, nombre):
        updateSala_atencionSQL = """
        UPDATE sala_atenciones
        SET nombre=%s
        WHERE id_sala_atencion=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateSala_atencionSQL, (nombre, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
        
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar sala_atencion: {str(e)}")
            con.rollback()
            return False 
               
        finally:
            cur.close()
            con.close()

    def deleteSala_atencion(self, id):
        deleteSala_atencionSQL = """
        DELETE FROM sala_atenciones
        WHERE id_sala_atencion=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecución exitosa
        try:
            cur.execute(deleteSala_atencionSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila        
        except Exception as e:
            app.logger.error(f"Error al eliminar sala_atencion: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
