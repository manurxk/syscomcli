# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion


class CiudadDao:

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad
        FROM ciudades
        ORDER BY des_ciudad
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            ciudades = cur.fetchall()
            return [{'id': c[0], 'id_departamento': c[1], 'descripcion': c[2], 'estado': c[3]} for c in ciudades]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las ciudades: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_departamento(self, id_departamento: int) -> list[dict]:
        sql = """
        SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad
        FROM ciudades
        WHERE id_departamento=%s
        ORDER BY des_ciudad
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_departamento,))
            ciudades = cur.fetchall()
            return [{'id': c[0], 'id_departamento': c[1], 'descripcion': c[2], 'estado': c[3]} for c in ciudades]
        except Exception as e:
            app.logger.error(f"Error al obtener ciudades por departamento: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_id(self, id_ciudad: int) -> dict | None:
        sql = """
        SELECT id_ciudad, id_departamento, des_ciudad, est_ciudad
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
                return {"id": ciudad[0], "id_departamento": ciudad[1], "descripcion": ciudad[2], "estado": ciudad[3]}
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

    def existe(self, id_departamento: int, des_ciudad: str) -> bool:
        """Verifica si ya existe la ciudad con el mismo nombre dentro del departamento (case-insensitive)."""
        sql = "SELECT 1 FROM ciudades WHERE id_departamento=%s AND LOWER(des_ciudad)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_departamento, des_ciudad))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validar_descripcion(self, des_ciudad: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_ciudad))

    # ============================
    # CRUD
    # ============================

    def guardar(self, id_departamento: int, des_ciudad: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_ciudad):
            app.logger.warning("Descripción inválida: solo letras, números y acentos")
            return False
        if self.existe(id_departamento, des_ciudad):
            app.logger.warning("La ciudad ya existe en ese departamento")
            return False

        sql = """
        INSERT INTO ciudades(id_departamento, des_ciudad, usuario_creacion)
        VALUES(%s, %s, %s)
        RETURNING id_ciudad
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_departamento, des_ciudad, usuario_creacion))
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

    def actualizar(self, id_ciudad: int, id_departamento: int, des_ciudad: str, est_ciudad: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_ciudad):
            app.logger.warning("Descripción inválida")
            return False

        sql = """
        UPDATE ciudades
        SET id_departamento=%s, des_ciudad=%s, est_ciudad=%s, usuario_modificacion=%s
        WHERE id_ciudad=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_departamento, des_ciudad, est_ciudad, usuario_modificacion, id_ciudad))
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
