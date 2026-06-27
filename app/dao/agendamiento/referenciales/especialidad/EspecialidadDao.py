import re

from app.core.base_dao import BaseDAO


class EspecialidadDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEspecialidades(self):
        sql = "SELECT id_especialidad, des_especialidad, est_especialidad FROM especialidades ORDER BY id_especialidad"
        return self.execute_query(sql)

    def getEspecialidadById(self, especialidad_id):
        sql = "SELECT id_especialidad, des_especialidad, est_especialidad FROM especialidades WHERE id_especialidad = %s"
        return self.execute_query_one(sql, (especialidad_id,))

    def validarDescripcion(self, descripcion):
        """Misma regla que el check constraint chk_especialidades_des: letras, números y espacios."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$"
        return bool(re.match(patron, descripcion))

    def especialidadExiste(self, descripcion, excluir_id=None):
        sql = "SELECT 1 FROM especialidades WHERE LOWER(des_especialidad) = LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_especialidad != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarEspecialidad(self, descripcion, estado, usuario_creacion=None):
        sql = """
            INSERT INTO especialidades (des_especialidad, est_especialidad, usuario_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_especialidad
        """
        fila = self.execute_query_one(sql, (descripcion, estado, usuario_creacion), commit=True)
        return fila["id_especialidad"] if fila else None

    def updateEspecialidad(self, especialidad_id, descripcion, estado, usuario_modificacion=None):
        sql = """
            UPDATE especialidades
            SET des_especialidad = %s, est_especialidad = %s, usuario_modificacion = %s
            WHERE id_especialidad = %s
        """
        return self.execute_query(sql, (descripcion, estado, usuario_modificacion, especialidad_id), commit=True) > 0

    def desactivarEspecialidad(self, especialidad_id, usuario_modificacion=None):
        sql = """
            UPDATE especialidades
            SET est_especialidad = FALSE, usuario_modificacion = %s
            WHERE id_especialidad = %s
        """
        return self.execute_query(sql, (usuario_modificacion, especialidad_id), commit=True) > 0
