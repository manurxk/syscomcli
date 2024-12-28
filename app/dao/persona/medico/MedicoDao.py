# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MedicoDao:

    def getMedicos(self):
        medicoSQL = """
        SELECT
            m.id_medico,
            m.nombre,
            m.apellido,
            m.cedula,
            m.sexo,
            m.telefono,
            m.correo,
            m.matricula,
            es.descripcion AS especialidad,
            TO_CHAR(m.fecha_nacimiento, 'YYYY/MM/DD') AS fecha_nacimiento, -- Formatea la fecha
            e.descripcion AS estado_civil,
            m.direccion,
            c.descripcion AS ciudad
        FROM 
            medicos m
        INNER JOIN 
            estado_civiles e ON m.id_estado_civil = e.id_estado_civil
        INNER JOIN 
            ciudades c ON m.id_ciudad = c.id_ciudad
        INNER JOIN 
            especialidades es ON m.id_especialidad = es.id_especialidad;

        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicoSQL)
            medicos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{
                    'id_medico': medico[0], 'nombre': medico[1], 'apellido': medico[2], 'cedula': medico[3], 'sexo': medico[4],
                    'telefono': medico[5], 'correo': medico[6], 'matricula': medico[7],'especialidad': medico[8],
                    'fecha_nacimiento': medico[9], 'estado_civil': medico[10], 'direccion': medico[11], 'ciudad': medico[12]} for medico in medicos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los médicos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMedicoById(self, id):
        medicoSQL = """
        SELECT
            m.id_medico,
            m.nombre,
            m.apellido,
            m.cedula,
            m.sexo,
            m.telefono,
            m.correo,
            m.matricula,
            es.descripcion AS especialidad,
            TO_CHAR(m.fecha_nacimiento, 'YYYY/MM/DD') AS fecha_nacimiento, -- Formatea la fecha
            e.descripcion AS estado_civil,
            m.direccion,
            c.descripcion AS ciudad
        FROM 
            medicos m
        INNER JOIN 
            estado_civiles e ON m.id_estado_civil = e.id_estado_civil
        INNER JOIN 
            ciudades c ON m.id_ciudad = c.id_ciudad
        INNER JOIN 
            especialidades es ON m.id_especialidad = es.id_especialidad
        WHERE 
            m.id_medico = %s;
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicoSQL, (id,))
            medico = cur.fetchone()  # Traer un solo registro

            if medico:
                return {
                    'id_medico': medico[0],
                    'nombre': medico[1],
                    'apellido': medico[2],
                    'cedula': medico[3],
                    'sexo': medico[4],
                    'telefono': medico[5],
                    'correo': medico[6],
                    'matricula': medico[7],
                    'especialidad': medico[8],
                    'fecha_nacimiento': medico[9],
                    'estado_civil': medico[10],
                    'direccion': medico[11],
                    'ciudad': medico[12]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener médico: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarMedico(self, nombre, apellido, cedula, sexo, telefono, correo, matricula, especialidad, fecha_nacimiento, estado_civil, direccion, ciudad):
        insertMedicoSQL = """
        INSERT INTO medicos(nombre, apellido, cedula, sexo, telefono, correo, matricula, id_especialidad, fecha_nacimiento, id_estado_civil, direccion, id_ciudad) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_medico
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # Aquí no pasas 'id_medico', ya que es generado automáticamente por la base de datos
            cur.execute(insertMedicoSQL, (nombre, apellido, cedula, sexo, telefono, correo, matricula, especialidad, fecha_nacimiento, estado_civil, direccion, ciudad))
            medico_id = cur.fetchone()[0]  # Obtener el id_medico generado automáticamente
            con.commit()
            return medico_id

        except Exception as e:
            app.logger.error(f"Error al insertar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()


    def updateMedico(self, id_medico, nombre, apellido, cedula, sexo, telefono, correo, matricula, especialidad, fecha_nacimiento, estado_civil, direccion, ciudad):
        updateMedicoSQL = """
        UPDATE medicos
        SET nombre=%s, apellido=%s, cedula=%s, sexo=%s, telefono=%s, correo=%s, matricula=%s, 
            id_especialidad=%s, fecha_nacimiento=%s, id_estado_civil=%s, direccion=%s, id_ciudad=%s
        WHERE id_medico=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMedicoSQL, (nombre, apellido, cedula, sexo, telefono, correo, matricula, especialidad, fecha_nacimiento, estado_civil, direccion, ciudad, id_medico))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMedico(self, id):
        deleteMedicoSQL = """
        DELETE FROM medicos
        WHERE id_medico=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMedicoSQL, (id,))
            rows_affected = cur.rowcount  # Obtener cuántas filas fueron afectadas
            con.commit()

            return rows_affected > 0  # Retorna True si al menos una fila fue eliminada
        except Exception as e:
            app.logger.error(f"Error al eliminar médico: {str(e)}")
            con.rollback()  # En caso de error, hacer rollback
            return False  # Retorna False si ocurre un error
        finally:
            cur.close()
            con.close()