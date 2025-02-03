# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EspecialistaDao:

    def getEspecialistas(self):
        especialistaSQL = """
        SELECT
            e.id_especialista,
            e.nombre,
            e.apellido,
            e.cedula,
            e.sexo,
            e.fecha_nacimiento,
            e.telefono,
            e.correo,
            e.matricula,
            es.descripcion AS especialidad,
            es.descripcion AS estado_civil,
            e.direccion,
            c.descripcion AS ciudad
        FROM 
            especialistas e
         INNER JOIN 
            estado_civiles et ON e.id_estado_civil = et.id_estado_civil
        INNER JOIN 
            especialidades es ON e.id_especialidad = es.id_especialidad
        INNER JOIN 
            ciudades c ON e.id_ciudad = c.id_ciudad;
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(especialistaSQL)
            especialistas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{
                    'id_especialista': especialista[0], 'nombre': especialista[1], 'apellido': especialista[2], 'cedula': especialista[3], 'sexo': especialista[4],
                    'fecha_nacimiento': especialista[5], 'telefono': especialista[6], 'correo': especialista[7], 'matricula': especialista[8],'especialidad': especialista[9],
                    'estado_civil': especialista[10], 'direccion': especialista[11], 'ciudad': especialista[12]} for especialista in especialistas]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los especialistas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEspecialistaById(self, id_especialista):
        especialistaSQL = """
        SELECT
            e.id_especialista,
            e.nombre,
            e.apellido,
            e.cedula,
            e.sexo,
            e.fecha_nacimiento,
            e.telefono,
            e.correo,
            e.matricula,
            es.descripcion AS especialidad,
            es.descripcion AS especialidad,
            e.direccion,
            c.descripcion AS ciudad
            FROM 
            especialistas e, 
            especialidades es, 
            ciudades c
            WHERE 
            e.id_especialidad = es.id_especialidad 
            AND e.id_ciudad = c.id_ciudad
            AND e.id_especialista = %s;
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(especialistaSQL, (id_especialista,))
            especialistaEncontrada = cur.fetchone()  # Traer un solo registro

            if especialistaEncontrada:
                return {
                    'id_especialista': especialistaEncontrada[0],
                    'nombre': especialistaEncontrada[1],
                    'apellido': especialistaEncontrada[2],
                    'cedula': especialistaEncontrada[3],
                    'sexo': especialistaEncontrada[4],
                    'fecha_nacimiento': especialistaEncontrada[5],
                    'telefono': especialistaEncontrada[6],
                    'correo': especialistaEncontrada[7],
                    'matricula': especialistaEncontrada[8],
                    'especialidad': especialistaEncontrada[9],
                    'especialidad': especialistaEncontrada[10],
                    'direccion': especialistaEncontrada[11],
                    'ciudad': especialistaEncontrada[12]
             
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener especialista: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()


    def guardarEspecialista(self, nombre, apellido, cedula, sexo, fecha_nacimiento, telefono, correo, matricula, especialidad, estado_civil, direccion, ciudad):
        insertEspecialistaSQL = """
        INSERT INTO especialistas(nombre, apellido, cedula, sexo, fecha_nacimiento, telefono, correo, matricula, id_especialidad, id_estado_civil, direccion, id_ciudad) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_especialista 
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertEspecialistaSQL, (nombre, apellido, cedula, sexo, fecha_nacimiento, telefono, correo, matricula, especialidad, estado_civil, direccion, ciudad))
            especialista_id = cur.fetchone()[0] 
            con.commit()
            return especialista_id

        except Exception as e:
            app.logger.error(f"Error al insertar especialista: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    

    def updateEspecialista(self, id_especialista, nombre, apellido, cedula, sexo, fecha_nacimiento, telefono, correo, matricula, especialidad, estado_civil, direccion, ciudad):
        updateEspecialistaSQL = """
        UPDATE especialistas
        SET nombre=%s, apellido=%s, cedula=%s, sexo=%s, fecha_nacimiento=%s, telefono=%s, correo=%s, matricula=%s, 
            id_especialidad=%s,  id_estado_civil=%s, direccion=%s, id_ciudad=%s
        WHERE id_especialista=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEspecialistaSQL, (nombre, apellido, cedula, sexo, fecha_nacimiento, telefono, correo, matricula, especialidad, estado_civil, direccion, ciudad, id_especialista))
            filas_afectadas = cur.rowcount  
            con.commit()
            return filas_afectadas > 0  

        except Exception as e:
            app.logger.error(f"Error al actualizar especialista: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEspecialista(self, id_especialista):
        deleteEspecialistaSQL = """
        DELETE FROM especialistas
        WHERE id_especialista=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteEspecialistaSQL, (id_especialista,))
            rows_affected = cur.rowcount  
            con.commit()

            return rows_affected > 0  
        except Exception as e:
            app.logger.error(f"Error al eliminar especialista: {str(e)}")
            con.rollback() 
            return False 
        finally:
            cur.close()
            con.close()
