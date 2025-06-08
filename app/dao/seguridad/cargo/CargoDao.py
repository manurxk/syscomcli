from flask import current_app as app
from app.conexion.Conexion import Conexion

class CargoDao:

    def getCargos(self):
        cargosSQL = """
        SELECT car_id, car_des
        FROM cargos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(cargosSQL)
            cargos = cur.fetchall()
            return [{'car_id': cargo[0], 'car_des': cargo[1]} for cargo in cargos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los cargos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCargoById(self, car_id):
        cargoSQL = """
        SELECT car_id, car_des
        FROM cargos WHERE car_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(cargoSQL, (car_id,))
            cargoEncontrado = cur.fetchone()
            if cargoEncontrado:
                return {
                    "car_id": cargoEncontrado[0],
                    "car_des": cargoEncontrado[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener cargo por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCargo(self, car_des):
        insertCargoSQL = """
        INSERT INTO cargos(car_des)
        VALUES(%s) RETURNING car_id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertCargoSQL, (car_des,))
            cargo_id = cur.fetchone()[0]
            con.commit()
            return cargo_id

        except Exception as e:
            app.logger.error(f"Error al insertar cargo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateCargo(self, car_id, car_des):
        updateCargoSQL = """
        UPDATE cargos
        SET car_des=%s
        WHERE car_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCargoSQL, (car_des, car_id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar cargo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCargo(self, car_id):
        deleteCargoSQL = """
        DELETE FROM cargos
        WHERE car_id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteCargoSQL, (car_id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar cargo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
