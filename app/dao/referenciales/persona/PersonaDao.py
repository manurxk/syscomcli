from flask import current_app as app
from app.conexion.Conexion import Conexion
import psycopg2
from datetime import datetime

class PersonaDao:

    def getPersonas(self):
        personaSQL = """
        SELECT id_persona, nombres, apellidos, ci, to_char(fechanac, 'DD/MM/YYYY HH24:MI:SS') AS fechanac, sexo
        FROM personas
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL)
            lista_personas = cur.fetchall()
            lista_ordenada = []
            for item in lista_personas:
                lista_ordenada.append({
                    "id_persona": item[0],
                    "nombres": item[1],
                    "apellidos": item[2],
                    "ci": item[3],
                    "fechanac": item[4],
                    "sexo": item[5]
                })
            return lista_ordenada
        except psycopg2.DatabaseError as e:
            app.logger.error("Error al obtener personas: %s", e)
        finally:
            cur.close()
            con.close()

    def getPersonaById(self, id_persona):
        personaSQL = """
        SELECT id_persona, nombres, apellidos, ci, fechanac, sexo
        FROM personas WHERE id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL, (id_persona,))
            personaEncontrada = cur.fetchone()
            if personaEncontrada:
                return {
                    "id_persona": personaEncontrada[0],
                    "nombres": personaEncontrada[1],
                    "apellidos": personaEncontrada[2],
                    "ci": personaEncontrada[3],
                    "fechanac": personaEncontrada[4],
                    "sexo": personaEncontrada[5]
                }
            return None
        except psycopg2.DatabaseError as e:
            app.logger.error("Error al obtener persona por ID: %s", e)
        finally:
            cur.close()
            con.close()

    def guardarPersona(self, nombres, apellidos, ci, fechanac, sexo):
        # Validación de datos antes de insertar
        if not (nombres and apellidos and ci and fechanac and sexo):
            app.logger.error("Faltan datos requeridos para insertar persona.")
            return False

        insertPersonaSQL = """
        INSERT INTO public.personas(nombres, apellidos, ci, fechanac, sexo)
        VALUES (%s, %s, %s, %s, %s);
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Convertir fechanac a formato datetime
        try:
            fecha_nac = datetime.strptime(fechanac, '%d/%m/%Y')
        except ValueError as e:
            app.logger.error(f"Error en el formato de fecha: {e}")
            return False

        try:
            cur.execute(insertPersonaSQL, (nombres, apellidos, ci, fecha_nac, sexo))
            con.commit()
            return True
        except psycopg2.DatabaseError as e:
            app.logger.error("Error al insertar persona: %s", e)
        finally:
            cur.close()
            con.close()

        return False

    def updatePersona(self, id_persona, nombres, apellidos, ci, fechanac, sexo):
        # Validación de datos antes de actualizar
        if not (nombres and apellidos and ci and fechanac and sexo):
            app.logger.error("Faltan datos requeridos para actualizar persona.")
            return False

        updatePersonaSQL = """
        UPDATE personas
        SET nombres=%s, apellidos=%s, ci=%s, fechanac=%s, sexo=%s
        WHERE id_persona=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Convertir fechanac a formato datetime
        try:
            fecha_nac = datetime.strptime(fechanac, '%d/%m/%Y')
        except ValueError as e:
            app.logger.error(f"Error en el formato de fecha: {e}")
            return False

        try:
            cur.execute(updatePersonaSQL, (nombres, apellidos, ci, fecha_nac, sexo, id_persona))
            con.commit()
            app.logger.info("Persona actualizada correctamente.")
            return True
        except psycopg2.DatabaseError as e:
            app.logger.error("Error al actualizar persona: %s", e)
        finally:
            cur.close()
            con.close()

        return False

    def deletePersona(self, id_persona):
        deletePersonaSQL = """
        DELETE FROM personas
        WHERE id_persona=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePersonaSQL, (id_persona,))
            con.commit()
            app.logger.info("Persona eliminada correctamente.")
            return True
        except psycopg2.DatabaseError as e:
            app.logger.error("Error al eliminar persona: %s", e)
        finally:
            cur.close()
            con.close()

        return False
