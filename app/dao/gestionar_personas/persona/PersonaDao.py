from flask import current_app as app
from app.conexion.Conexion import Conexion

class PersonaDao:

    def getPersonas(self):
        personaSQL = """
      SELECT
        p.id_persona, p.nombre, p.apellido, p.cedula, g.descripcion, e.descripcion, p.telefono_emergencia, c.descripcion 
            FROM personas p, generos g, estado_civiles e, ciudades c
            where p.id_genero=g.id_genero and p.id_estado_civil=e.id_estado_civil and p.id_ciudad=c.id_ciudad
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL)
            personas = cur.fetchall()

            # Transformar los datos en una lista de diccionarios con los nuevos campos
            return [{
                'id': persona[0], 'nombre': persona[1], 'apellido': persona[2], 'cedula': persona[3], 'genero': persona[4], 'estado_civil': persona[5], 'telefono_emergencia': persona[6],'ciudad': persona[7]} for persona in personas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las personas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()
    # TRANSFORMAC CON CTGP PRIMERO MANDAR LA TABLA SQL 
    def getPersonasById(self, id_persona):
        personaSQL = """
         SELECT
            p.id_persona, p.nombre, p.apellido, p.cedula, g.descripcion, e.descripcion, p.telefono_emergencia, c.descripcion, g.id_genero, e.id_estado_civil, c. id_ciudad 
            FROM personas p, generos g, estado_civiles e, ciudades c
            where p.id_genero=g.id_genero and p.id_estado_civil=e.id_estado_civil and p.id_ciudad=c.id_ciudad and p.id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL, (id_persona,))
            personaEncontrada = cur.fetchone()
            if personaEncontrada:
                return {
                    "id": personaEncontrada[0],
                    "nombre": personaEncontrada[1],
                    "apellido": personaEncontrada[2],
                    "cedula": personaEncontrada[3],
                    "genero": personaEncontrada[4],
                    "estado_civil": personaEncontrada[5],
                    "telefono_emergencia": personaEncontrada[6],
                    "ciudad": personaEncontrada[7],
                    "id_genero": personaEncontrada[8],
                    "id_estado_civil": personaEncontrada[9],
                     "id_ciudad": personaEncontrada[10]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener persona por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPersona(self, nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad):
        insertPersonaSQL = """
        INSERT INTO personas(nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad) VALUES(%s, %s, %s,%s, %s, %s, %s) RETURNING id_persona
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPersonaSQL, (nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad))
            persona_id = cur.fetchone()[0]
            con.commit()
            return persona_id

        except Exception as e:
            app.logger.error(f"Error al insertar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updatePersona(self, id_persona, nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad):
        updatePersonaSQL = """
        UPDATE personas
        SET nombre=%s, apellido=%s, cedula=%s, id_genero=%s, id_estado_civil=%s, telefono_emergencia=%s, id_ciudad=%s
        WHERE id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePersonaSQL, (nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad,id_persona))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

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
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()