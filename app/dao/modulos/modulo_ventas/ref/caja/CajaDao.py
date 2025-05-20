from flask import current_app as app
from app.conexion.Conexion import Conexion

class CajaDao:

    def getCaja(self):
        cajaSQL = """
        SELECT id_caja, descripcion
        FROM cajas
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(cajaSQL)
            cajas = cur.fetchall()

            return [{'id_caja': caja[0], 'descripcion': caja[1]} for caja in cajas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las cajas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCajaById(self, id_caja):
        cajaSQL = """
        SELECT id_caja, descripcion
        FROM cajas WHERE id_caja=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(cajaSQL, (id_caja,))
            cajaEncontrada = cur.fetchone()
            if cajaEncontrada:
                return {
                    "id_caja": cajaEncontrada[0],
                    "descripcion": cajaEncontrada[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener caja: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCaja(self, descripcion):
        insertCajaSQL = """
        INSERT INTO cajas(descripcion) VALUES(%s) RETURNING id_caja
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertCajaSQL, (descripcion,))
            caja_id = cur.fetchone()[0]
            con.commit()
            return caja_id

        except Exception as e:
            app.logger.error(f"Error al insertar caja: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateCaja(self, id_caja, descripcion):
        updateCajaSQL = """
        UPDATE cajas
        SET descripcion=%s
        WHERE id_caja=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCajaSQL, (descripcion, id_caja))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar caja: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCaja(self, id_caja):
        deleteCajaSQL = """
        DELETE FROM cajas
        WHERE id_caja=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteCajaSQL, (id_caja,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar caja: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
