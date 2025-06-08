from flask import current_app as app
from app.conexion.Conexion import Conexion

class GrupoDao:

    def getGrupos(self):
        gruposSQL = """
        SELECT gru_id, gru_des
        FROM grupos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(gruposSQL)
            grupos = cur.fetchall()
            return [{'gru_id': grupo[0], 'gru_des': grupo[1]} for grupo in grupos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los grupos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getGrupoById(self, gru_id):
        grupoSQL = """
        SELECT gru_id, gru_des
        FROM grupos WHERE gru_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(grupoSQL, (gru_id,))
            grupoEncontrado = cur.fetchone()
            if grupoEncontrado:
                return {
                    "gru_id": grupoEncontrado[0],
                    "gru_des": grupoEncontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener grupo por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarGrupo(self, gru_des):
        insertGrupoSQL = """
        INSERT INTO grupos(gru_des)
        VALUES(%s) RETURNING gru_id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertGrupoSQL, (gru_des,))
            grupo_id = cur.fetchone()[0]
            con.commit()
            return grupo_id

        except Exception as e:
            app.logger.error(f"Error al insertar grupo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateGrupo(self, gru_id, gru_des):
        updateGrupoSQL = """
        UPDATE grupos
        SET gru_des=%s
        WHERE gru_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateGrupoSQL, (gru_des, gru_id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar grupo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteGrupo(self, gru_id):
        deleteGrupoSQL = """
        DELETE FROM grupos
        WHERE gru_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteGrupoSQL, (gru_id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar grupo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
