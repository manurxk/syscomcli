
# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PersonaDao:

    def getPersonas(self):
        personaSQL = """
        SELECT id_persona, nombre, apellido, fechanacimiento, cedula, sexo
        FROM persona
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL)
            personas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id_persona': persona[0], 'nombre': persona[1], 'apellido': persona[2], 'fechanacimiento': persona[3], 'cedula': persona[4], 'sexo': persona[5]} for persona in personas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las personas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPersonaById(self, id):
        personaSQL = """
        SELECT id_persona, nombre, apellido, fechanacimiento, cedula, sexo
        FROM persona WHERE id_persona=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL, (id,))
            personaEncontrada = cur.fetchone()  # Obtener una sola fila
            if personaEncontrada:
                return {
                    "id_persona": personaEncontrada[0],
                    "nombre": personaEncontrada[1],
                    "apellido": personaEncontrada[2],
                    "fechanacimiento": personaEncontrada[3],
                    "cedula": personaEncontrada[4],
                    "sexo": personaEncontrada[5]
                }  # Retornar los datos de persona
            else:
                return None  # Retornar None si no se encuentra la persona
        except Exception as e:
            app.logger.error(f"Error al obtener persona: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPersona(self, nombre, apellido, fechanacimiento, cedula, sexo):
        insertPersonaSQL = """
        INSERT INTO persona(nombre, apellido, fechanacimiento, cedula, sexo) VALUES(%s, %s, %s, %s, %s) RETURNING id_persona
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertPersonaSQL, (nombre, apellido, fechanacimiento, cedula, sexo))
            persona_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return persona_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar persona: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updatePersona(self, id, nombre, apellido, fechanacimiento, cedula, sexo):
        updatePersonaSQL = """
        UPDATE persona
        SET nombre=%s, apellido=%s, fechanacimiento=%s, cedula=%s, sexo=%s
        WHERE id_persona=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePersonaSQL, (nombre, apellido, fechanacimiento, cedula, sexo, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePersona(self, id):
        deletePersonaSQL = """
        DELETE FROM persona
        WHERE id_persona=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePersonaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()