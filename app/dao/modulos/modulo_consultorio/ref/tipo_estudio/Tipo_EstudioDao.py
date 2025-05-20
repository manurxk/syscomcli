# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoEstudioDao:

    def getTiposEstudios(self):

        tipoEstudioSQL = """
        SELECT id, descripcion
        FROM tipos_estudios
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoEstudioSQL)
            tipos_estudios = cur.fetchall()

            return [{'id': tipo[0], 'descripcion': tipo[1]} for tipo in tipos_estudios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de estudio: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTipoEstudioById(self, id):

        tipoEstudioSQL = """
        SELECT id, descripcion
        FROM tipos_estudios WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoEstudioSQL, (id,))
            tipo_estudio_encontrado = cur.fetchone()
            if tipo_estudio_encontrado:
                return {
                    "id": tipo_estudio_encontrado[0],
                    "descripcion": tipo_estudio_encontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de estudio: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTipoEstudio(self, descripcion):

        insertTipoEstudioSQL = """
        INSERT INTO tipos_estudios(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTipoEstudioSQL, (descripcion,))
            tipo_estudio_id = cur.fetchone()[0]
            con.commit()
            return tipo_estudio_id

        except Exception as e:
            app.logger.error(f"Error al insertar tipo de estudio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateTipoEstudio(self, id, descripcion):

        updateTipoEstudioSQL = """
        UPDATE tipos_estudios
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipoEstudioSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de estudio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTipoEstudio(self, id):

        deleteTipoEstudioSQL = """
        DELETE FROM tipos_estudios
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTipoEstudioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de estudio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
