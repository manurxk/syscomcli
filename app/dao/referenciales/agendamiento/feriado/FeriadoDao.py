# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class FeriadoDao:

    def getFeriados(self):
        sql = """
        SELECT id_feriado, fecha_feriado, des_feriado, est_feriado
        FROM feriados
        ORDER BY fecha_feriado DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            feriados = cur.fetchall()
            return [{'id': f[0], 'fecha': str(f[1]), 'descripcion': f[2], 'estado': f[3]} for f in feriados]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los feriados: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getFeriadoById(self, id_feriado):
        sql = """
        SELECT id_feriado, fecha_feriado, des_feriado, est_feriado
        FROM feriados
        WHERE id_feriado=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_feriado,))
            f = cur.fetchone()
            if f:
                return {'id': f[0], 'fecha': str(f[1]), 'descripcion': f[2], 'estado': f[3]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener feriado {id_feriado}: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def feriadoExiste(self, fecha_feriado):
        """Verifica si ya existe un feriado en esa fecha."""
        sql = "SELECT 1 FROM feriados WHERE fecha_feriado=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (fecha_feriado,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    # ============================
    # CRUD
    # ============================

    def guardarFeriado(self, fecha_feriado, descripcion, estado=True):
        if self.feriadoExiste(fecha_feriado):
            app.logger.warning("El feriado ya existe en esa fecha")
            return False

        sql = """
        INSERT INTO feriados(fecha_feriado, des_feriado, est_feriado)
        VALUES(%s, %s, %s)
        RETURNING id_feriado
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (fecha_feriado, descripcion, estado))
            id_feriado = cur.fetchone()[0]
            con.commit()
            return id_feriado
        except Exception as e:
            app.logger.error(f"Error al insertar feriado: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateFeriado(self, id_feriado, fecha_feriado, descripcion, estado=True):
        # Verificar si la nueva fecha ya existe pero en OTRO feriado
        sql_check = "SELECT id_feriado FROM feriados WHERE fecha_feriado=%s AND id_feriado != %s"
        
        sql = """
        UPDATE feriados
        SET fecha_feriado=%s, des_feriado=%s, est_feriado=%s
        WHERE id_feriado=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql_check, (fecha_feriado, id_feriado))
            if cur.fetchone():
                app.logger.warning("Ya existe otro feriado en esa fecha")
                return False

            cur.execute(sql, (fecha_feriado, descripcion, estado, id_feriado))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar feriado: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteFeriado(self, id_feriado):
        sql = "DELETE FROM feriados WHERE id_feriado=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_feriado,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar feriado: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
