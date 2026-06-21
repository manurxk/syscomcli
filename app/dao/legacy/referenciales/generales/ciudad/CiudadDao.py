# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CiudadDao:

    def getCiudades(self):
        sql = """
        SELECT id_ciudad, des_ciudad, est_ciudad
        FROM ciudades
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            ciudades = cur.fetchall()
            return [{'id': c[0], 'descripcion': c[1], 'estado': c[2]} for c in ciudades]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las ciudades: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getCiudadById(self, id_ciudad):
        sql = """
        SELECT id_ciudad, des_ciudad, est_ciudad
        FROM ciudades
        WHERE id_ciudad=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_ciudad,))
            ciudad = cur.fetchone()
            if ciudad:
                return {"id": ciudad[0], "descripcion": ciudad[1], "estado": ciudad[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener ciudad: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def ciudadExiste(self, descripcion):
        """Verifica si ya existe la ciudad con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM ciudades WHERE LOWER(des_ciudad)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validarDescripcion(self, descripcion):
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, descripcion))

    # ============================
    # CRUD
    # ============================

    def guardarCiudad(self, descripcion, estado=True):
        # Validaciones
        if not self.validarDescripcion(descripcion):
            app.logger.warning("Descripción inválida: solo letras, números y acentos")
            return False
        if self.ciudadExiste(descripcion):
            app.logger.warning("La ciudad ya existe")
            return False

        sql = """
        INSERT INTO ciudades(des_ciudad, est_ciudad)
        VALUES(%s, %s)
        RETURNING id_ciudad
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion, estado))
            id_ciudad = cur.fetchone()[0]
            con.commit()
            return id_ciudad
        except Exception as e:
            app.logger.error(f"Error al insertar ciudad: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateCiudad(self, id_ciudad, descripcion, estado=True):
        # Validaciones
        if not self.validarDescripcion(descripcion):
            app.logger.warning("Descripción inválida")
            return False

        sql = """
        UPDATE ciudades
        SET des_ciudad=%s, est_ciudad=%s
        WHERE id_ciudad=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion, estado, id_ciudad))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar ciudad: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteCiudad(self, id_ciudad):
        sql = "DELETE FROM ciudades WHERE id_ciudad=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_ciudad,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar ciudad: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
