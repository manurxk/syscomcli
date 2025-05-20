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
            , pa.fecha_nacimiento
            , pa.peso
            , pa.altura
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
                        ,'fecha_nacimiento': paciente[5].strftime('%d/%m/%Y')
                        ,'peso': paciente[6]
                        ,'altura': paciente[7]
                    } 
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
            pa.id_paciente,p.nombre, p.apellido, p.cedula, p.telefono_emergencia, pa.fecha_nacimiento, pa.peso, pa.altura, p.id_persona
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
                    "fecha_nacimiento": pacienteEncontrado[5],
                    "peso": pacienteEncontrado[6],
                    "altura": pacienteEncontrado[7],
                    "id_persona": pacienteEncontrado[8]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener paciente por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPaciente(self,id_persona,fecha_nacimiento,peso,altura,):
        insertPacienteSQL = """
        INSERT INTO pacientes(fecha_nacimiento,peso,altura,id_persona) 
        VALUES(%s, %s, %s, %s) RETURNING id_paciente 
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPacienteSQL, (fecha_nacimiento, peso,altura,id_persona))
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

    def updatePaciente(self,id_paciente,id_persona,fecha_nacimiento,peso,altura):
        updatePacienteSQL = """
        UPDATE pacientes
        SET id_persona = %s, fecha_nacimiento = %s, peso = %s, altura = %s
        WHERE id_paciente = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePacienteSQL, (id_persona,fecha_nacimiento,peso,altura,id_paciente))
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
