# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion


class ProfesionDao:

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_profesion, des_profesion, est_profesion
        FROM profesiones
        ORDER BY des_profesion
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            profesiones = cur.fetchall()
            return [{'id': p[0], 'descripcion': p[1], 'estado': p[2]} for p in profesiones]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las profesiones: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_id(self, id_profesion: int) -> dict | None:
        sql = """
        SELECT id_profesion, des_profesion, est_profesion
        FROM profesiones
        WHERE id_profesion=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_profesion,))
            profesion = cur.fetchone()
            if profesion:
                return {"id": profesion[0], "descripcion": profesion[1], "estado": profesion[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener profesión: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_profesion: str) -> bool:
        """Verifica si ya existe la profesión (case-insensitive)."""
        sql = "SELECT 1 FROM profesiones WHERE LOWER(des_profesion)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_profesion,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validar_descripcion(self, des_profesion: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_profesion))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_profesion: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_profesion):
            app.logger.warning("Descripción inválida: solo letras, números y acentos")
            return False
        if self.existe(des_profesion):
            app.logger.warning("La profesión ya existe")
            return False

        sql = """
        INSERT INTO profesiones(des_profesion, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_profesion
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_profesion, usuario_creacion))
            id_profesion = cur.fetchone()[0]
            con.commit()
            return id_profesion
        except Exception as e:
            app.logger.error(f"Error al insertar profesión: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def actualizar(self, id_profesion: int, des_profesion: str, est_profesion: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_profesion):
            app.logger.warning("Descripción inválida")
            return False

        sql = """
        UPDATE profesiones
        SET des_profesion=%s, est_profesion=%s, usuario_modificacion=%s
        WHERE id_profesion=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_profesion, est_profesion, usuario_modificacion, id_profesion))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar profesión: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
