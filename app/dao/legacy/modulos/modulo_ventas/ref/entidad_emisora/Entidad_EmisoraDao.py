from flask import current_app as app
from app.conexion.Conexion import Conexion

class EntidadEmisoraDao:

    def getEntidadEmisora(self):
        entidadSQL = """
        SELECT id_entidad_emisora, descripcion
        FROM entidades_emisoras
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(entidadSQL)
            entidades = cur.fetchall()

            return [{'id_entidad_emisora': entidad[0], 'descripcion': entidad[1]} for entidad in entidades]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las entidades emisoras: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEntidadEmisoraById(self, id_entidad_emisora):
        entidadSQL = """
        SELECT id_entidad_emisora, descripcion
        FROM entidades_emisoras WHERE id_entidad_emisora=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(entidadSQL, (id_entidad_emisora,))
            entidadEncontrada = cur.fetchone()
            if entidadEncontrada:
                return {
                    "id_entidad_emisora": entidadEncontrada[0],
                    "descripcion": entidadEncontrada[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener entidad emisora: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEntidadEmisora(self, descripcion):
        insertSQL = """
        INSERT INTO entidades_emisoras(descripcion) VALUES(%s) RETURNING id_entidad_emisora
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
            app.logger.error(f"Error al insertar entidad emisora: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateEntidadEmisora(self, id_entidad_emisora, descripcion):
        updateSQL = """
        UPDATE entidades_emisoras
        SET descripcion=%s
        WHERE id_entidad_emisora=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateSQL, (descripcion, id_entidad_emisora))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar entidad emisora: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEntidadEmisora(self, id_entidad_emisora):
        deleteSQL = """
        DELETE FROM entidades_emisoras
        WHERE id_entidad_emisora=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteSQL, (id_entidad_emisora,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar entidad emisora: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
