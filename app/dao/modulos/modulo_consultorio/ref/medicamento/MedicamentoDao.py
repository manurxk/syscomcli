# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MedicamentoDao:

    def getMedicamentos(self):

        medicamentoSQL = """
        SELECT id, descripcion
        FROM medicamentos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicamentoSQL)
            medicamentos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': medicamento[0], 'descripcion': medicamento[1]} for medicamento in medicamentos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los medicamentos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMedicamentoById(self, id):

        medicamentoSQL = """
        SELECT id, descripcion
        FROM medicamentos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicamentoSQL, (id,))
            medicamentoEncontrado = cur.fetchone()  # Obtener una sola fila
            if medicamentoEncontrado:
                return {
                    "id": medicamentoEncontrado[0],
                    "descripcion": medicamentoEncontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener medicamento: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMedicamento(self, descripcion):

        insertMedicamentoSQL = """
        INSERT INTO medicamentos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertMedicamentoSQL, (descripcion,))
            medicamento_id = cur.fetchone()[0]
            con.commit()
            return medicamento_id

        except Exception as e:
            app.logger.error(f"Error al insertar medicamento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateMedicamento(self, id, descripcion):

        updateMedicamentoSQL = """
        UPDATE medicamentos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMedicamentoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar medicamento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMedicamento(self, id):

        deleteMedicamentoSQL = """
        DELETE FROM medicamentos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMedicamentoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar medicamento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
