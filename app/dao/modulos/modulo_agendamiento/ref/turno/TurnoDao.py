from flask import current_app as app
from app.conexion.Conexion import Conexion

class TurnoDao:

    def getTurno(self):
        turnoSQL = """
        SELECT id_turno, descripcion
        FROM turnos
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(turnoSQL)
            turnos = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id_turno': turno[0], 'descripcion': turno[1]} for turno in turnos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los turnos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTurnoById(self, id_turno):
        turnoSQL = """
        SELECT id_turno, descripcion
        FROM turnos WHERE id_turno=%s
        """
        # Objeto conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(turnoSQL, (id_turno,))
            turnoEncontrada = cur.fetchone()  # Obtener una sola fila
            if turnoEncontrada:
                return {
                    "id_turno": turnoEncontrada[0],
                    "descripcion": turnoEncontrada[1]
                }  # Retornar los datos del turno
            else:
                return None  # Retornar None si no se encuentra el turno
        except Exception as e:
            app.logger.error(f"Error al obtener turno: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTurno(self, descripcion):
        insertTurnoSQL = """
        INSERT INTO turnos(descripcion) VALUES(%s) RETURNING id_turno
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTurnoSQL, (descripcion,))
            turno_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return turno_id

        except Exception as e:
            app.logger.error(f"Error al insertar turno: {str(e)}")
            con.rollback()  # Revertir si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateTurno(self, id_turno, descripcion):
        updateTurnoSQL = """
        UPDATE turnos
        SET descripcion=%s
        WHERE id_turno=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTurnoSQL, (descripcion, id_turno))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar turno: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTurno(self, id_turno):
        deleteTurnoSQL = """
        DELETE FROM turnos
        WHERE id_turno=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTurnoSQL, (id_turno,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar turno: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()