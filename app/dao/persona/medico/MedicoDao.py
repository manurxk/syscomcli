from flask import current_app as app
from app.conexion.Conexion import Conexion

class MedicoDao:

    def getMedicos(self):
        medicoSQL = """
        SELECT
            m.id, m.nombre, m.apellido, m.documento_identidad, m.registro_profesional, m.especialidad, 
            m.telefono, m.correo, m.ocupacion, m.sexo, m.estado_civil, c.descripcion AS ciudad, b.descripcion AS barrio, p.descripcion AS pais,
            m.direccion, m.fecha_nacimiento, m.fecha_registro, m.contacto_emergencia, m.numero_emergencia
        FROM medicos m
        JOIN ciudades c ON m.id_ciudad = c.id
        JOIN barrios b ON m.id_barrio = b.id
        JOIN paises p ON m.id_pais = p.id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicoSQL)
            medicos = cur.fetchall()

            # Retorna los datos en forma de lista de diccionarios
            return [{
                'id': medico[0],
                'nombre': medico[1],
                'apellido': medico[2],
                'documento_identidad': medico[3],
                'registro_profesional': medico[4],
                'especialidad': medico[5],
                'telefono': medico[6],
                'correo': medico[7],
                'ocupacion': medico[8],
                'sexo': medico[9],
                'estado_civil': medico[10],
                'ciudad': medico[11],
                'barrio': medico[12],
                'pais': medico[13],
                'direccion': medico[14],
                'fecha_nacimiento': medico[15],
                'fecha_registro': medico[16],
                'contacto_emergencia': medico[17],
                'numero_emergencia': medico[18],
            } for medico in medicos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los médicos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMedicoById(self, id_medico):
        medicoSQL = """
        SELECT
            m.id, m.nombre, m.apellido, m.documento_identidad, m.registro_profesional, m.especialidad, 
            m.telefono, m.correo, m.ocupacion, m.sexo, m.estado_civil, c.descripcion AS ciudad, b.descripcion AS barrio, p.descripcion AS pais,
            m.direccion, m.fecha_nacimiento, m.fecha_registro, m.contacto_emergencia, m.numero_emergencia
        FROM medicos m
        JOIN ciudades c ON m.id_ciudad = c.id
        JOIN barrios b ON m.id_barrio = b.id
        JOIN paises p ON m.id_pais = p.id
        WHERE m.id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicoSQL, (id_medico,))
            medico = cur.fetchone()
            if medico:
                return {
                    'id': medico[0],
                    'nombre': medico[1],
                    'apellido': medico[2],
                    'documento_identidad': medico[3],
                    'registro_profesional': medico[4],
                    'especialidad': medico[5],
                    'telefono': medico[6],
                    'correo': medico[7],
                    'ocupacion': medico[8],
                    'sexo': medico[9],
                    'estado_civil': medico[10],
                    'ciudad': medico[11],
                    'barrio': medico[12],
                    'pais': medico[13],
                    'direccion': medico[14],
                    'fecha_nacimiento': medico[15],
                    'fecha_registro': medico[16],
                    'contacto_emergencia': medico[17],
                    'numero_emergencia': medico[18],
                }
            else:
                return None

        except Exception as e:
            app.logger.error(f"Error al obtener médico por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMedico(self, nombre, apellido, documento_identidad, registro_profesional, especialidad, telefono, correo, 
                      ocupacion, sexo, estado_civil, id_ciudad, id_barrio, id_pais, direccion, fecha_nacimiento, 
                      fecha_registro, contacto_emergencia, numero_emergencia):
        insertMedicoSQL = """
        INSERT INTO medicos (nombre, apellido, documento_identidad, registro_profesional, especialidad, telefono, correo, 
                             ocupacion, sexo, estado_civil, id_ciudad, id_barrio, id_pais, direccion, fecha_nacimiento, 
                             fecha_registro, contacto_emergencia, numero_emergencia) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertMedicoSQL, (nombre, apellido, documento_identidad, registro_profesional, especialidad, telefono, 
                                          correo, ocupacion, sexo, estado_civil, id_ciudad, id_barrio, id_pais, direccion, 
                                          fecha_nacimiento, fecha_registro, contacto_emergencia, numero_emergencia))
            medico_id = cur.fetchone()[0]
            con.commit()
            return medico_id

        except Exception as e:
            app.logger.error(f"Error al insertar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateMedico(self, id_medico, **kwargs):
        campos = ", ".join([f"{key} = %s" for key in kwargs])
        updateMedicoSQL = f"""
        UPDATE medicos
        SET {campos}
        WHERE id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            valores = list(kwargs.values()) + [id_medico]
            cur.execute(updateMedicoSQL, tuple(valores))
            con.commit()
            return cur.rowcount > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMedico(self, id_medico):
        deleteMedicoSQL = """
        DELETE FROM medicos
        WHERE id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMedicoSQL, (id_medico,))
            con.commit()
            return cur.rowcount > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
