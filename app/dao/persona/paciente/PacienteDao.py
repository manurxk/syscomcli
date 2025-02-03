from flask import current_app as app
from app.conexion.Conexion import Conexion

class PacienteDao:

    def getPacientes(self):
        pacienteSQL = """
        SELECT
            p.id_persona,
            p.nombre, 
            p.apellido, 
            p.cedula, 
            g.descripcion, 
            e.descripcion, 
            p.telefono_emergencia, 
            c.descripcion 
        FROM personas p, generos g, estado_civiles e, ciudades c
            where p.id_genero=g.id_genero and p.id_estado_civil=e.id_estado_civil and p.id_ciudad=c.id_ciudad
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pacienteSQL)
            pacientes = cur.fetchall()

            return [{
                'id': paciente[0], 'nombre': paciente[1], 'apellido': paciente[2], 
                'cedula': paciente[3], 'genero': paciente[4], 'estado_civil': paciente[5], 
                'telefono_emergencia': paciente[6],'ciudad': paciente[7]} for paciente in pacientes]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los pacientes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPacienteById(self, id_paciente):
        pacienteSQL = """
         SELECT
            p.id_persona, p.nombre, p.apellido, p.cedula, g.descripcion, e.descripcion, 
            p.telefono_emergencia, c.descripcion, g.id_genero, e.id_estado_civil, c.id_ciudad 
            FROM personas p, generos g, estado_civiles e, ciudades c
            where p.id_genero=g.id_genero and p.id_estado_civil=e.id_estado_civil 
            and p.id_ciudad=c.id_ciudad and p.id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pacienteSQL, (id_paciente,))
            pacienteEncontrado = cur.fetchone()
            if pacienteEncontrado:
                return {
                    "id": pacienteEncontrado[0],
                    "nombre": pacienteEncontrado[1],
                    "apellido": pacienteEncontrado[2],
                    "cedula": pacienteEncontrado[3],
                    "genero": pacienteEncontrado[4],
                    "estado_civil": pacienteEncontrado[5],
                    "telefono_emergencia": pacienteEncontrado[6],
                    "ciudad": pacienteEncontrado[7],
                    "id_genero": pacienteEncontrado[8],
                    "id_estado_civil": pacienteEncontrado[9],
                     "id_ciudad": pacienteEncontrado[10]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener paciente por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPaciente(self, nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad):
        insertPacienteSQL = """
        INSERT INTO personas(nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad) 
        VALUES(%s, %s, %s,%s, %s, %s, %s) RETURNING id_persona
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPacienteSQL, (nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad))
            paciente_id = cur.fetchone()[0]
            con.commit()
            return paciente_id

        except Exception as e:
            app.logger.error(f"Error al insertar paciente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updatePaciente(self, id_paciente, nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad):
        updatePacienteSQL = """
        UPDATE personas
        SET nombre=%s, apellido=%s, cedula=%s, id_genero=%s, id_estado_civil=%s, 
            telefono_emergencia=%s, id_ciudad=%s
        WHERE id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePacienteSQL, (nombre, apellido, cedula, id_genero, id_estado_civil, 
                                           telefono_emergencia, id_ciudad, id_paciente))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar paciente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePaciente(self, id_paciente):
        deletePacienteSQL = """
        DELETE FROM personas
        WHERE id_persona=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePacienteSQL, (id_paciente,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar paciente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()