from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime


class DisponibilidadDao:
    def getDisponibilidad(self):
        query = """
        SELECT id, id_persona, dia_semana, hora_inicio, hora_fin, hora_almuerzo_inicio, hora_almuerzo_fin, duracion_consulta
        FROM disponibilidad_medico
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(query)
            disponibilidades = cur.fetchall()

            return [{
                'id': d[0],
                'id_persona': d[1],
                'dia_semana': d[2],
                'hora_inicio': d[3].strftime('%H:%M:%S') if d[3] else None,
                'hora_fin': d[4].strftime('%H:%M:%S') if d[4] else None,
                'hora_almuerzo_inicio': d[5].strftime('%H:%M:%S') if d[5] else None,
                'hora_almuerzo_fin': d[6].strftime('%H:%M:%S') if d[6] else None,
                'duracion_consulta': d[7]
            } for d in disponibilidades]

        except Exception as e:
            app.logger.error(f"Error al obtener disponibilidad: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDisponibilidadById(self, id):
        query = """
        SELECT id, id_persona, dia_semana, hora_inicio, hora_fin, hora_almuerzo_inicio, hora_almuerzo_fin, duracion_consulta
        FROM disponibilidad_medico WHERE id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(query, (id,))
            disponibilidad = cur.fetchone()
            if disponibilidad:
                return {
                    'id': disponibilidad[0],
                    'id_persona': disponibilidad[1],
                    'dia_semana': disponibilidad[2],
                    'hora_inicio': disponibilidad[3].strftime('%H:%M:%S') if disponibilidad[3] else None,
                    'hora_fin': disponibilidad[4].strftime('%H:%M:%S') if disponibilidad[4] else None,
                    'hora_almuerzo_inicio': disponibilidad[5].strftime('%H:%M:%S') if disponibilidad[5] else None,
                    'hora_almuerzo_fin': disponibilidad[6].strftime('%H:%M:%S') if disponibilidad[6] else None,
                    'duracion_consulta': disponibilidad[7]
                }
            return None

        except Exception as e:
            app.logger.error(f"Error al obtener disponibilidad por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDisponibilidad(self, id_persona, dia_semana, hora_inicio, hora_fin, hora_almuerzo_inicio, hora_almuerzo_fin, duracion_consulta):
        query = """
        INSERT INTO disponibilidad_medico 
        (id_persona, dia_semana, hora_inicio, hora_fin, hora_almuerzo_inicio, hora_almuerzo_fin, duracion_consulta) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(query, (id_persona, dia_semana, hora_inicio, hora_fin, hora_almuerzo_inicio, hora_almuerzo_fin, duracion_consulta))
            id_disponibilidad = cur.fetchone()[0]
            con.commit()
            return id_disponibilidad

        except Exception as e:
            app.logger.error(f"Error al guardar disponibilidad: {str(e)}")
            con.rollback()
            return None

        finally:
            cur.close()
            con.close()

    def updateDisponibilidad(self, id, id_persona, dia_semana, hora_inicio, hora_fin, hora_almuerzo_inicio, hora_almuerzo_fin, duracion_consulta):
        query = """
        UPDATE disponibilidad_medico
        SET id_persona=%s, dia_semana=%s, hora_inicio=%s, hora_fin=%s, hora_almuerzo_inicio=%s, hora_almuerzo_fin=%s, duracion_consulta=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(query, (id_persona, dia_semana, hora_inicio, hora_fin, hora_almuerzo_inicio, hora_almuerzo_fin, duracion_consulta, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar disponibilidad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDisponibilidad(self, id):
        query = """
        DELETE FROM disponibilidad_medico WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(query, (id,))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar disponibilidad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
