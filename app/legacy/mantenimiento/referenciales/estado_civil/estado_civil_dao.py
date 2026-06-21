# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion


class EstadoCivilDao:

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_estado_civil, des_estado_civil, est_estado_civil
        FROM estados_civiles
        ORDER BY des_estado_civil
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            estados = cur.fetchall()
            return [{'id': e[0], 'descripcion': e[1], 'estado': e[2]} for e in estados]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los estados civiles: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_id(self, id_estado_civil: int) -> dict | None:
        sql = """
        SELECT id_estado_civil, des_estado_civil, est_estado_civil
        FROM estados_civiles
        WHERE id_estado_civil=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_estado_civil,))
            estado = cur.fetchone()
            if estado:
                return {"id": estado[0], "descripcion": estado[1], "estado": estado[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener estado civil: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_estado_civil: str) -> bool:
        """Verifica si ya existe un estado civil con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM estados_civiles WHERE LOWER(des_estado_civil)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_estado_civil,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validar_descripcion(self, des_estado_civil: str) -> bool:
        """Permite solo letras con acentos y espacios (sin números ni símbolos)."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
        return bool(re.match(patron, des_estado_civil))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_estado_civil: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_estado_civil):
            app.logger.warning("Descripción inválida: solo letras y acentos")
            return False
        if self.existe(des_estado_civil):
            app.logger.warning("El estado civil ya existe")
            return False

        sql = """
        INSERT INTO estados_civiles(des_estado_civil, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_estado_civil
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_estado_civil, usuario_creacion))
            id_estado_civil = cur.fetchone()[0]
            con.commit()
            return id_estado_civil
        except Exception as e:
            app.logger.error(f"Error al insertar estado civil: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def actualizar(self, id_estado_civil: int, des_estado_civil: str, est_estado_civil: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_estado_civil):
            app.logger.warning("Descripción inválida")
            return False

        sql = """
        UPDATE estados_civiles
        SET des_estado_civil=%s, est_estado_civil=%s, usuario_modificacion=%s
        WHERE id_estado_civil=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_estado_civil, est_estado_civil, usuario_modificacion, id_estado_civil))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar estado civil: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
