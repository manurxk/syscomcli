# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoAnalisisDao:

    def getTiposAnalisis(self):

        tipoAnalisisSQL = """
        SELECT id, descripcion
        FROM tipos_analisis
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoAnalisisSQL)
            tipos_analisis = cur.fetchall()

            return [{'id': tipo[0], 'descripcion': tipo[1]} for tipo in tipos_analisis]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de análisis: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTipoAnalisisById(self, id):

        tipoAnalisisSQL = """
        SELECT id, descripcion
        FROM tipos_analisis WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoAnalisisSQL, (id,))
            tipo_analisis_encontrado = cur.fetchone()
            if tipo_analisis_encontrado:
                return {
                    "id": tipo_analisis_encontrado[0],
                    "descripcion": tipo_analisis_encontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de análisis: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTipoAnalisis(self, descripcion):

        insertTipoAnalisisSQL = """
        INSERT INTO tipos_analisis(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTipoAnalisisSQL, (descripcion,))
            tipo_analisis_id = cur.fetchone()[0]
            con.commit()
            return tipo_analisis_id

        except Exception as e:
            app.logger.error(f"Error al insertar tipo de análisis: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateTipoAnalisis(self, id, descripcion):

        updateTipoAnalisisSQL = """
        UPDATE tipos_analisis
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipoAnalisisSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de análisis: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTipoAnalisis(self, id):

        deleteTipoAnalisisSQL = """
        DELETE FROM tipos_analisis
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTipoAnalisisSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de análisis: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
