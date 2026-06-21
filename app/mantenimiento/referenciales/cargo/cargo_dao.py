# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion


class CargoDao:

    def get_todos(self) -> list[dict]:
        sql = """
        SELECT id_cargo, des_cargo, est_cargo
        FROM cargos
        ORDER BY des_cargo
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            cargos = cur.fetchall()
            return [{'id': c[0], 'descripcion': c[1], 'estado': c[2]} for c in cargos]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los cargos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_cargos_permitidos(self, excluir_administrador: bool = False) -> list[dict]:
        """
        Obtiene cargos activos. Si excluir_administrador es True, excluye
        los cargos 'ADMINISTRADOR' y 'SUPERADMINISTRADOR'.
        """
        if excluir_administrador:
            sql = """
            SELECT id_cargo, des_cargo, est_cargo
            FROM cargos
            WHERE LOWER(des_cargo) NOT IN ('administrador', 'superadministrador')
            AND est_cargo = TRUE
            ORDER BY des_cargo
            """
        else:
            sql = """
            SELECT id_cargo, des_cargo, est_cargo
            FROM cargos
            WHERE est_cargo = TRUE
            ORDER BY des_cargo
            """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            cargos = cur.fetchall()
            return [{'id': c[0], 'descripcion': c[1], 'estado': c[2]} for c in cargos]
        except Exception as e:
            app.logger.error(f"Error al obtener cargos permitidos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_id(self, id_cargo: int) -> dict | None:
        sql = """
        SELECT id_cargo, des_cargo, est_cargo
        FROM cargos
        WHERE id_cargo=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_cargo,))
            cargo = cur.fetchone()
            if cargo:
                return {"id": cargo[0], "descripcion": cargo[1], "estado": cargo[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener cargo: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def existe(self, des_cargo: str) -> bool:
        """Verifica si ya existe el cargo con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM cargos WHERE LOWER(des_cargo)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_cargo,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validar_descripcion(self, des_cargo: str) -> bool:
        """Permite solo letras, números, acentos y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, des_cargo))

    def es_cargo_reservado(self, des_cargo: str) -> bool:
        """Los cargos 'ADMINISTRADOR' y 'SUPERADMINISTRADOR' están reservados y no se pueden crear/editar."""
        descripcion_lower = des_cargo.lower().strip()
        cargos_reservados = ['administrador', 'superadministrador']
        return descripcion_lower in cargos_reservados

    # ============================
    # CRUD
    # ============================

    def guardar(self, des_cargo: str, usuario_creacion: int) -> int | bool:
        if not self.validar_descripcion(des_cargo):
            app.logger.warning("Descripción inválida: solo letras, números y acentos")
            return False
        if self.es_cargo_reservado(des_cargo):
            app.logger.warning(f"El cargo '{des_cargo}' está reservado y no se puede crear")
            return False
        if self.existe(des_cargo):
            app.logger.warning("El cargo ya existe")
            return False

        sql = """
        INSERT INTO cargos(des_cargo, usuario_creacion)
        VALUES(%s, %s)
        RETURNING id_cargo
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_cargo, usuario_creacion))
            id_cargo = cur.fetchone()[0]
            con.commit()
            return id_cargo
        except Exception as e:
            app.logger.error(f"Error al insertar cargo: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def actualizar(self, id_cargo: int, des_cargo: str, est_cargo: bool, usuario_modificacion: int) -> bool:
        if not self.validar_descripcion(des_cargo):
            app.logger.warning("Descripción inválida")
            return False
        if self.es_cargo_reservado(des_cargo):
            app.logger.warning(f"El cargo '{des_cargo}' está reservado y no se puede usar")
            return False

        sql = """
        UPDATE cargos
        SET des_cargo=%s, est_cargo=%s, usuario_modificacion=%s
        WHERE id_cargo=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (des_cargo, est_cargo, usuario_modificacion, id_cargo))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar cargo: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
