# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DiaDao:

    def getDia(self):
        diaSQL = """
        SELECT id_dia, descripcion
        FROM dias
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(diaSQL)
            dias = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id_dia': dia[0], 'descripcion': dia[1]} for dia in dias]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los días: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDiaById(self, id_dia):
        diaSQL = """
        SELECT id_dia, descripcion
        FROM dias WHERE id_dia=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(diaSQL, (id_dia,))
            diaEncontrada = cur.fetchone()  # Obtener una sola fila
            if diaEncontrada:
                return {
                    "id_dia": diaEncontrada[0],
                    "descripcion": diaEncontrada[1]
                }  # Retornar los datos del día
            else:
                return None  # Retornar None si no se encuentra el día
        except Exception as e:
            app.logger.error(f"Error al obtener días: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDia(self, descripcion):
        insertDiaSQL = """
        INSERT INTO dias(descripcion) VALUES(%s) RETURNING id_dia
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertDiaSQL, (descripcion,))
            dia_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return dia_id

        except Exception as e:
            app.logger.error(f"Error al insertar día: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateDia(self, id_dia, descripcion):
        updateDiaSQL = """
        UPDATE dias
        SET descripcion=%s
        WHERE id_dia=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDiaSQL, (descripcion, id_dia,))
            filas_afectadas = cur.rowcount  # Número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar día: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDia(self, id_dia):
        deleteDiaSQL = """
        DELETE FROM dias
        WHERE id_dia=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteDiaSQL, (id_dia,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar día: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
