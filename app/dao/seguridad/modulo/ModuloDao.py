from flask import current_app as app
from app.conexion.Conexion import Conexion

class ModuloDao:

    def getModulos(self):
        modulosSQL = """
        SELECT mod_id, mod_des
        FROM modulos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(modulosSQL)
            modulos = cur.fetchall()
            return [{'mod_id': modulo[0], 'mod_des': modulo[1]} for modulo in modulos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los módulos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getModuloById(self, mod_id):
        moduloSQL = """
        SELECT mod_id, mod_des
        FROM modulos WHERE mod_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(moduloSQL, (mod_id,))
            moduloEncontrado = cur.fetchone()
            if moduloEncontrado:
                return {
                    "mod_id": moduloEncontrado[0],
                    "mod_des": moduloEncontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener módulo por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarModulo(self, mod_des):
        insertModuloSQL = """
        INSERT INTO modulos(mod_des)
        VALUES(%s) RETURNING mod_id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertModuloSQL, (mod_des,))
            modulo_id = cur.fetchone()[0]
            con.commit()
            return modulo_id

        except Exception as e:
            app.logger.error(f"Error al insertar módulo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateModulo(self, mod_id, mod_des):
        updateModuloSQL = """
        UPDATE modulos
        SET mod_des=%s
        WHERE mod_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateModuloSQL, (mod_des, mod_id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar módulo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteModulo(self, mod_id):
        deleteModuloSQL = """
        DELETE FROM modulos
        WHERE mod_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteModuloSQL, (mod_id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar módulo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
