from flask import current_app as app
from app.conexion.Conexion import Conexion

class EntidadAdheridaDao:

    def getEntidadAdherida(self):
        entidadSQL = """
        SELECT id_entidad_adherida, descripcion
        FROM entidades_adheridas
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(entidadSQL)
            entidades = cur.fetchall()

            return [{'id_entidad_adherida': entidad[0], 'descripcion': entidad[1]} for entidad in entidades]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las entidades adheridas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEntidadAdheridaById(self, id_entidad_adherida):
        entidadSQL = """
        SELECT id_entidad_adherida, descripcion
        FROM entidades_adheridas WHERE id_entidad_adherida=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(entidadSQL, (id_entidad_adherida,))
            entidadEncontrada = cur.fetchone()
            if entidadEncontrada:
                return {
                    "id_entidad_adherida": entidadEncontrada[0],
                    "descripcion": entidadEncontrada[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener entidad adherida: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEntidadAdherida(self, descripcion):
        insertSQL = """
        INSERT INTO entidades_adheridas(descripcion) VALUES(%s) RETURNING id_entidad_adherida
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertSQL, (descripcion,))
            entidad_id = cur.fetchone()[0]
            con.commit()
            return entidad_id

        except Exception as e:
            app.logger.error(f"Error al insertar entidad adherida: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateEntidadAdherida(self, id_entidad_adherida, descripcion):
        updateSQL = """
        UPDATE entidades_adheridas
        SET descripcion=%s
        WHERE id_entidad_adherida=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateSQL, (descripcion, id_entidad_adherida))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar entidad adherida: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEntidadAdherida(self, id_entidad_adherida):
        deleteSQL = """
        DELETE FROM entidades_adheridas
        WHERE id_entidad_adherida=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteSQL, (id_entidad_adherida,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar entidad adherida: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
