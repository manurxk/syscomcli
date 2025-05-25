# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class UsuarioDao:

    def getUsuarios(self):
        usuariosSQL = """
        SELECT usu_id, usu_nick, usu_clave, usu_estado
        FROM usuarios
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(usuariosSQL)
            usuarios = cur.fetchall()  # Trae datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'usu_id}': usuario[0], 'usu_nick': usuario[1], 'clave': usuario[2], 'estado': usuario[3]} for usuario in usuarios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los usuarios: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getUsuarioById(self, usu_id):
        usuarioSQL = """
        SELECT usu_id, usu_nick, clave, estado
        FROM usuarios WHERE usu_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(usuarioSQL, (usu_id,))
            usuarioEncontrado = cur.fetchone()  # Obtener una sola fila
            if usuarioEncontrado:
                return {
                    "usu_id": usuarioEncontrado[0],
                    "usu_nick": usuarioEncontrado[1],
                    "clave": usuarioEncontrado[2],
                    "estado": usuarioEncontrado[3]
                }  # Retornar los datos del usuario
            else:
                return None  # Retornar None si no se encuentra el usuario
        except Exception as e:
            app.logger.error(f"Error al obtener usuario: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarUsuario(self, usu_nick, clave, estado):
        print(usu_nick, clave, estado)
        insertUsuarioSQL = """
        INSERT INTO usuarios(usu_nick, clave, estado) 
        VALUES(%s, %s, %s) RETURNING usu_id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertUsuarioSQL, (usu_nick, clave, estado))
            usuario_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return usuario_id

        except Exception as e:
            app.logger.error(f"Error al insertar usuario: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateUsuario(self, usu_id, usu_nick, clave, estado):
        updateUsuarioSQL = """
        UPDATE usuarios
        SET usu_nick=%s, clave=%s, estado=%s
        WHERE usu_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateUsuarioSQL, (usu_nick, clave, estado, usu_id))
            filas_afectadas = cur.rowcount  # Número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteUsuario(self, usu_id):
        deleteUsuarioSQL = """
        DELETE FROM usuarios
        WHERE usu_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteUsuarioSQL, (usu_id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar usuario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
