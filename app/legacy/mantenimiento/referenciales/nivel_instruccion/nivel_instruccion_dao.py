# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion


class NivelInstruccionDao:

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_nivel_instruccion, des_nivel_instruccion, est_nivel_instruccion
        FROM niveles_instruccion
        ORDER BY id_nivel_instruccion
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            niveles = cur.fetchall()
            return [{'id': n[0], 'descripcion': n[1], 'estado': n[2]} for n in niveles]
        except Exception as e:
            app.logger.error(f"Error al obtener niveles de instrucción: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_id(self, id_nivel_instruccion: int) -> dict | None:
        sql = """
        SELECT id_nivel_instruccion, des_nivel_instruccion, est_nivel_instruccion
        FROM niveles_instruccion
        WHERE id_nivel_instruccion=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_nivel_instruccion,))
            nivel = cur.fetchone()
            if nivel:
                return {"id": nivel[0], "descripcion": nivel[1], "estado": nivel[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener nivel de instrucción: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_nivel_instruccion: str) -> bool:
        """Verifica si ya existe el nivel con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM niveles_instruccion WHERE LOWER(des_nivel_instruccion)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_nivel_instruccion,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validar_descripcion(self, des_nivel_instruccion: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_nivel_instruccion))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_nivel_instruccion: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_nivel_instruccion):
            app.logger.warning("Descripción inválida: solo letras, números y acentos")
            return False
        if self.existe(des_nivel_instruccion):
            app.logger.warning("El nivel de instrucción ya existe")
            return False

        sql = """
        INSERT INTO niveles_instruccion(des_nivel_instruccion, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_nivel_instruccion
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_nivel_instruccion, usuario_creacion))
            id_nivel = cur.fetchone()[0]
            con.commit()
            return id_nivel
        except Exception as e:
            app.logger.error(f"Error al insertar nivel de instrucción: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def actualizar(self, id_nivel_instruccion: int, des_nivel_instruccion: str, est_nivel_instruccion: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_nivel_instruccion):
            app.logger.warning("Descripción inválida")
            return False

        sql = """
        UPDATE niveles_instruccion
        SET des_nivel_instruccion=%s, est_nivel_instruccion=%s, usuario_modificacion=%s
        WHERE id_nivel_instruccion=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_nivel_instruccion, est_nivel_instruccion, usuario_modificacion, id_nivel_instruccion))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar nivel de instrucción: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
