from flask import current_app as app
from app.conexion.Conexion import Conexion

class PacienteDao:

    def getPacientes(self):
        pacienteSQL = """
        SELECT
            pa.id_paciente
            , p.nombre
            , p.apellido
            , p.cedula
            , p.telefono_emergencia
            , pa.fecha_registro
        FROM 
            pacientes pa, personas p
        WHERE 
            pa.id_persona=p.id_persona
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pacienteSQL)
            pacientes = cur.fetchall()

            # Transformar los datos en una lista de diccionarios con los nuevos campos
            return [
                    {
                        'id_paciente': paciente[0]
                        ,'nombre': paciente[1]
                        ,'apellido': paciente[2]
                        ,'cedula': paciente[3]
                        ,'telefono_emergencia': paciente[4]
                        ,'fecha_registro': paciente[5].strftime('%d/%m/%Y')                    } 
                    for paciente in pacientes
                ]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los pacientes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPacienteById(self, id_paciente):
        pacienteSQL = """
         SELECT 
            pa.id_paciente,p.nombre, p.apellido, p.cedula, p.telefono_emergencia, pa.fecha_registro, p.id_persona
            FROM pacientes pa, personas p
            WHERE pa.id_persona=p.id_persona and pa.id_paciente = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pacienteSQL, (id_paciente,))
            pacienteEncontrado = cur.fetchone()
            if pacienteEncontrado:
                return {
                    "id_paciente": pacienteEncontrado[0],
                     "nombre": pacienteEncontrado[1],
                    "apellido": pacienteEncontrado[2],
                    "cedula": pacienteEncontrado[3],
                    "telefono_emergencia": pacienteEncontrado[4],
                    "fecha_registro": pacienteEncontrado[5],
                    "id_persona": pacienteEncontrado[6]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener paciente por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPaciente(self,id_persona,fecha_registro,):
        insertPacienteSQL = """
        INSERT INTO pacientes(fecha_registro,id_persona) 
        VALUES(%s, %s) RETURNING id_paciente 
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPacienteSQL, (fecha_registro,id_persona))
            id_paciente = cur.fetchone()[0]
            con.commit()
            return id_paciente

        except Exception as e:
            app.logger.error(f"Error al insertar paciente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updatePaciente(self,id_paciente,id_persona,fecha_registro):
        updatePacienteSQL = """
        UPDATE pacientes
        SET id_persona = %s, fecha_registro = %s
        WHERE id_paciente = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePacienteSQL, (id_persona,fecha_registro,id_paciente))
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
        DELETE FROM pacientes
        WHERE id_paciente = %s
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
