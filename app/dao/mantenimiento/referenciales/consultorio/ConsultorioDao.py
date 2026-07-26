import re

from app.core.base_dao import BaseDAO


class ConsultorioDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def validarDescripcion(self, descripcion):
        """Misma regla que el check constraint chk_consultorios_des: letras, números y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, descripcion))

    def getConsultorios(self, id_sede=None):
        sql = """
            SELECT c.id_consultorio, c.id_sede, s.des_sede, c.des_consultorio, c.est_consultorio
            FROM consultorios c
            JOIN sedes s ON c.id_sede = s.id_sede
            WHERE (%(id_sede)s IS NULL OR c.id_sede = %(id_sede)s)
            ORDER BY s.des_sede, c.des_consultorio
        """
        return self.execute_query(sql, {"id_sede": id_sede})

    def getConsultorioById(self, id_consultorio):
        sql = """
            SELECT id_consultorio, id_sede, des_consultorio, est_consultorio
            FROM consultorios
            WHERE id_consultorio = %s
        """
        return self.execute_query_one(sql, (id_consultorio,))

    def descripcionExiste(self, id_sede, des_consultorio, excluir_id=None):
        """Misma restricción que uq_consultorios_sede_des (id_sede, des_consultorio)."""
        sql = "SELECT 1 FROM consultorios WHERE id_sede = %s AND des_consultorio = %s"
        params = [id_sede, des_consultorio]
        if excluir_id:
            sql += " AND id_consultorio != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarConsultorio(self, id_sede, des_consultorio, estado=True, usuario_creacion=None):
        sql = """
            INSERT INTO consultorios (id_sede, des_consultorio, est_consultorio, usuario_creacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_consultorio
        """
        fila = self.execute_query_one(
            sql, (id_sede, des_consultorio, estado, usuario_creacion), commit=True
        )
        return fila["id_consultorio"] if fila else None

    def updateConsultorio(self, id_consultorio, id_sede, des_consultorio, estado=True, usuario_modificacion=None):
        sql = """
            UPDATE consultorios
            SET id_sede = %s, des_consultorio = %s, est_consultorio = %s, usuario_modificacion = %s
            WHERE id_consultorio = %s
        """
        return self.execute_query(
            sql, (id_sede, des_consultorio, estado, usuario_modificacion, id_consultorio), commit=True
        ) > 0

    def desactivarConsultorio(self, id_consultorio, usuario_modificacion=None):
        sql = """
            UPDATE consultorios
            SET est_consultorio = FALSE, usuario_modificacion = %s
            WHERE id_consultorio = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_consultorio), commit=True) > 0
