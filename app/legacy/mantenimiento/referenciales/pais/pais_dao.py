# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion


class PaisDao:

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_pais, des_pais, cod_pais, est_pais
        FROM paises
        ORDER BY des_pais
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            paises = cur.fetchall()
            return [{'id': p[0], 'descripcion': p[1], 'codigo': p[2], 'estado': p[3]} for p in paises]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los paises: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_activos(self) -> list[dict]:
        sql = """
        SELECT id_pais, des_pais, cod_pais, est_pais
        FROM paises
        WHERE est_pais = TRUE
        ORDER BY des_pais
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            paises = cur.fetchall()
            return [{'id': p[0], 'descripcion': p[1], 'codigo': p[2], 'estado': p[3]} for p in paises]
        except Exception as e:
            app.logger.error(f"Error al obtener paises activos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_id(self, id_pais: int) -> dict | None:
        sql = """
        SELECT id_pais, des_pais, cod_pais, est_pais
        FROM paises
        WHERE id_pais=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_pais,))
            pais = cur.fetchone()
            if pais:
                return {"id": pais[0], "descripcion": pais[1], "codigo": pais[2], "estado": pais[3]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener pais: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_pais: str) -> bool:
        """Verifica si ya existe el pais con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM paises WHERE LOWER(des_pais)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_pais,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validar_descripcion(self, des_pais: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_pais))

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_pais: str, cod_pais: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_pais):
            app.logger.warning("Descripción inválida: solo letras, números y acentos")
            return False
        if self.existe(des_pais):
            app.logger.warning("El pais ya existe")
            return False

        sql = """
        INSERT INTO paises(des_pais, cod_pais, usuario_creacion)
        VALUES(%s, %s, %s)
        RETURNING id_pais
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_pais, cod_pais, usuario_creacion))
            id_pais = cur.fetchone()[0]
            con.commit()
            return id_pais
        except Exception as e:
            app.logger.error(f"Error al insertar pais: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def actualizar(self, id_pais: int, des_pais: str, cod_pais: str, est_pais: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_pais):
            app.logger.warning("Descripción inválida")
            return False

        sql = """
        UPDATE paises
        SET des_pais=%s, cod_pais=%s, est_pais=%s, usuario_modificacion=%s
        WHERE id_pais=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_pais, cod_pais, est_pais, usuario_modificacion, id_pais))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar pais: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
