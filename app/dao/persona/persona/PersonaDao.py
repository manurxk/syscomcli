
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








from flask import current_app as app
from app.conexion.Conexion import Conexion

class PersonaDao:

    def getPersonas(self):
        personaSQL = """
        SELECT id_persona, nombre, apellido, fechanacimiento, telefono, direccion, sexo, correo_electronico, id_ciudad, id_pais, id_nacionalidad, id_estado_civil, id_ocupacion, id_barrio, fecha_registro, hora_registro
        FROM persona
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL)
            personas = cur.fetchall()

            return [{
                'id_persona': persona[0], 
                'nombre': persona[1], 
                'apellido': persona[2], 
                'fechanacimiento': persona[3],
                'telefono': persona[4],
                'direccion': persona[5],
                'sexo': persona[6],
                'correo_electronico': persona[7],
                'id_ciudad': persona[8],
                'id_pais': persona[9],
                'id_nacionalidad': persona[10],
                'id_estado_civil': persona[11],
                'id_ocupacion': persona[12],
                'id_barrio': persona[13],
                'fecha_registro': persona[14],
                'hora_registro': persona[15]
            } for persona in personas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las personas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPersonaById(self, id):
        personaSQL = """
        SELECT id_persona, nombre, apellido, fechanacimiento, telefono, direccion, sexo, correo_electronico, id_ciudad, id_pais, id_nacionalidad, id_estado_civil, id_ocupacion, id_barrio, fecha_registro, hora_registro
        FROM persona WHERE id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL, (id,))
            personaEncontrada = cur.fetchone()
            if personaEncontrada:
                return {
                    "id_persona": personaEncontrada[0],
                    "nombre": personaEncontrada[1],
                    "apellido": personaEncontrada[2],
                    "fechanacimiento": personaEncontrada[3],
                    "telefono": personaEncontrada[4],
                    "direccion": personaEncontrada[5],
                    "sexo": personaEncontrada[6],
                    "correo_electronico": personaEncontrada[7],
                    "id_ciudad": personaEncontrada[8],
                    "id_pais": personaEncontrada[9],
                    "id_nacionalidad": personaEncontrada[10],
                    "id_estado_civil": personaEncontrada[11],
                    "id_ocupacion": personaEncontrada[12],
                    "id_barrio": personaEncontrada[13],
                    "fecha_registro": personaEncontrada[14],
                    "hora_registro": personaEncontrada[15]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener persona: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPersona(self, nombre, apellido, fechanacimiento, telefono, direccion, sexo, correo_electronico, id_ciudad, id_pais, id_nacionalidad, id_estado_civil, id_ocupacion, id_barrio):
        insertPersonaSQL = """
        INSERT INTO persona(nombre, apellido, fechanacimiento, telefono, direccion, sexo, correo_electronico, id_ciudad, id_pais, id_nacionalidad, id_estado_civil, id_ocupacion, id_barrio, fecha_registro, hora_registro) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME) RETURNING id_persona
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPersonaSQL, (nombre, apellido, fechanacimiento, telefono, direccion, sexo, correo_electronico, id_ciudad, id_pais, id_nacionalidad, id_estado_civil, id_ocupacion, id_barrio))
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

    def updatePersona(self, id, nombre, apellido, fechanacimiento, telefono, direccion, sexo, correo_electronico, id_ciudad, id_pais, id_nacionalidad, id_estado_civil, id_ocupacion, id_barrio):
        updatePersonaSQL = """
        UPDATE persona
        SET nombre=%s, apellido=%s, fechanacimiento=%s, telefono=%s, direccion=%s, sexo=%s, correo_electronico=%s, id_ciudad=%s, id_pais=%s, id_nacionalidad=%s, id_estado_civil=%s, id_ocupacion=%s, id_barrio=%s
        WHERE id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePersonaSQL, (nombre, apellido, fechanacimiento, telefono, direccion, sexo, correo_electronico, id_ciudad, id_pais, id_nacionalidad, id_estado_civil, id_ocupacion, id_barrio, id))
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

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
