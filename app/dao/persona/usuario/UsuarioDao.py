from flask import current_app as app
from app.conexion.Conexion import Conexion
from psycopg2 import sql  # Asegúrate de tener este módulo si usas PostgreSQL

class UsuarioDao:

    def guardarUsuario(self, nombre_usuario, contrasena):
        """
        Inserta un nuevo usuario en la base de datos.
        """
        insertUsuarioSQL = """
        INSERT INTO usuarios(nombre_usuario, contrasena)
        VALUES (%s, %s)
        RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertUsuarioSQL, (nombre_usuario, contrasena))
            usuario_id = cur.fetchone()[0]
            con.commit()
            return usuario_id

        except Exception as e:
            app.logger.error(f"Error al insertar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def getUsuarioByNombre(self, nombre_usuario):
        """
        Obtiene un usuario por su nombre de usuario.
        """
        getUsuarioSQL = """
        SELECT id, nombre_usuario, contrasena
        FROM usuarios
        WHERE nombre_usuario = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(getUsuarioSQL, (nombre_usuario,))
            usuario = cur.fetchone()

            if usuario:
                return {
                    "id": usuario[0],
                    "nombre_usuario": usuario[1],
                    "contrasena": usuario[2]
                }
            else:
                return None

        except Exception as e:
            app.logger.error(f"Error al obtener usuario por nombre: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def getUsuarioById(self, usuario_id):
        """
        Obtiene un usuario por su ID.
        """
        getUsuarioSQL = """
        SELECT id, nombre_usuario, contrasena
        FROM usuarios
        WHERE id = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(getUsuarioSQL, (usuario_id,))
            usuario = cur.fetchone()

            if usuario:
                return {
                    "id": usuario[0],
                    "nombre_usuario": usuario[1],
                    "contrasena": usuario[2]
                }
            else:
                return None

        except Exception as e:
            app.logger.error(f"Error al obtener usuario por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def updateUsuario(self, usuario_id, nombre_usuario):
        """
        Actualiza el nombre de usuario de un usuario existente.
        """
        updateUsuarioSQL = """
        UPDATE usuarios
        SET nombre_usuario = %s
        WHERE id = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateUsuarioSQL, (nombre_usuario, usuario_id))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteUsuario(self, usuario_id):
        """
        Elimina un usuario por su ID.
        """
        deleteUsuarioSQL = """
        DELETE FROM usuarios
        WHERE id = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteUsuarioSQL, (usuario_id,))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
