# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoProcedimientoMedicoDao:

    def getTiposProcedimientosMedicos(self):

        tipoProcedimientoSQL = """
        SELECT id, descripcion
        FROM tipos_procedimientos_medicos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoProcedimientoSQL)
            tipos_procedimientos = cur.fetchall()

            return [{'id': tipo[0], 'descripcion': tipo[1]} for tipo in tipos_procedimientos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de procedimiento médico: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTipoProcedimientoMedicoById(self, id):

        tipoProcedimientoSQL = """
        SELECT id, descripcion
        FROM tipos_procedimientos_medicos WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipoProcedimientoSQL, (id,))
            tipo_procedimiento_encontrado = cur.fetchone()
            if tipo_procedimiento_encontrado:
                return {
                    "id": tipo_procedimiento_encontrado[0],
                    "descripcion": tipo_procedimiento_encontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de procedimiento médico: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTipoProcedimientoMedico(self, descripcion):

        insertTipoProcedimientoSQL = """
        INSERT INTO tipos_procedimientos_medicos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTipoProcedimientoSQL, (descripcion,))
            tipo_procedimiento_id = cur.fetchone()[0]
            con.commit()
            return tipo_procedimiento_id

        except Exception as e:
            app.logger.error(f"Error al insertar tipo de procedimiento médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateTipoProcedimientoMedico(self, id, descripcion):

        updateTipoProcedimientoSQL = """
        UPDATE tipos_procedimientos_medicos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipoProcedimientoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de procedimiento médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTipoProcedimientoMedico(self, id):

        deleteTipoProcedimientoSQL = """
        DELETE FROM tipos_procedimientos_medicos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTipoProcedimientoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de procedimiento médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
