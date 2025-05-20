from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:

    def getDeposito(self):
        depositoSQL = """
        SELECT id_deposito, descripcion
        FROM depositos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(depositoSQL)
            depositos = cur.fetchall()

            return [{'id_deposito': deposito[0], 'descripcion': deposito[1]} for deposito in depositos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los depósitos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDepositoById(self, id_deposito):
        depositoSQL = """
        SELECT id_deposito, descripcion
        FROM depositos WHERE id_deposito=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(depositoSQL, (id_deposito,))
            depositoEncontrado = cur.fetchone()
            if depositoEncontrado:
                return {
                    "id_deposito": depositoEncontrado[0],
                    "descripcion": depositoEncontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener depósito: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDeposito(self, descripcion):
        insertDepositoSQL = """
        INSERT INTO depositos(descripcion) VALUES(%s) RETURNING id_deposito
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertDepositoSQL, (descripcion,))
            deposito_id = cur.fetchone()[0]
            con.commit()
            return deposito_id

        except Exception as e:
            app.logger.error(f"Error al insertar depósito: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateDeposito(self, id_deposito, descripcion):
        updateDepositoSQL = """
        UPDATE depositos
        SET descripcion=%s
        WHERE id_deposito=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDepositoSQL, (descripcion, id_deposito))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar depósito: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDeposito(self, id_deposito):
        deleteDepositoSQL = """
        DELETE FROM depositos
        WHERE id_deposito=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteDepositoSQL, (id_deposito,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar depósito: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
