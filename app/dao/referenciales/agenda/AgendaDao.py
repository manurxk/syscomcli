from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

class AgendaDao:

    def getAgendas(self):
        agendaSQL = """
        SELECT id, nombrepaciente, motivoconsulta, medico, fecha, hora
        FROM agendas
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(agendaSQL)
            agendas = cur.fetchall()  # Trae datos de la bd

            # Transformar los datos en una lista de diccionarios y convertir fecha/hora a cadena
            return [{
                'id': agenda[0],
                'nombrepaciente': agenda[1],
                'motivoconsulta': agenda[2],
                'medico': agenda[3],
                'fecha': agenda[4].strftime('%Y-%m-%d') if agenda[4] else None,  # Convertir fecha a string
                'hora': agenda[5].strftime('%H:%M:%S') if agenda[5] else None  # Convertir hora a string
            } for agenda in agendas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las agendas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getAgendaById(self, id):
        agendaSQL = """
        SELECT id, nombrepaciente, motivoconsulta, medico, fecha, hora
        FROM agendas WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(agendaSQL, (id,))
            agendaEncontrada = cur.fetchone()  # Obtener una sola fila
            if agendaEncontrada:
                return {
                    "id": agendaEncontrada[0],
                    "nombrepaciente": agendaEncontrada[1],
                    "motivoconsulta": agendaEncontrada[2],
                    "medico": agendaEncontrada[3],
                    "fecha": agendaEncontrada[4].strftime('%Y-%m-%d') if agendaEncontrada[4] else None,  # Convertir fecha
                    "hora": agendaEncontrada[5].strftime('%H:%M:%S') if agendaEncontrada[5] else None  # Convertir hora
                }  # Retornar los datos de la agenda
            else:
                return None  # Retornar None si no se encuentra la agenda
        except Exception as e:
            app.logger.error(f"Error al obtener agenda: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarAgenda(self, nombrepaciente, motivoconsulta, medico, fecha, hora):
        insertAgendaSQL = """
        INSERT INTO agendas (nombrepaciente, motivoconsulta, medico, fecha, hora) 
        VALUES (%s, %s, %s, %s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertAgendaSQL, (nombrepaciente, motivoconsulta, medico, fecha, hora))
            agenda_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return agenda_id  # Retorna el id de la nueva agenda

        except Exception as e:
            app.logger.error(f"Error al insertar agenda: {str(e)}")
            con.rollback()  # Revertir si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateAgenda(self, id, nombrepaciente, motivoconsulta, medico, fecha, hora):
        updateAgendaSQL = """
        UPDATE agendas
        SET nombrepaciente=%s, motivoconsulta=%s, medico=%s, fecha=%s, hora=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateAgendaSQL, (nombrepaciente, motivoconsulta, medico, fecha, hora, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar agenda: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteAgenda(self, id):
        deleteAgendaSQL = """
        DELETE FROM agendas
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteAgendaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar agenda: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
