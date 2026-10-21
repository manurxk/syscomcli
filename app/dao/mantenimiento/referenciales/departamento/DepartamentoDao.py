from app.core.base_dao import BaseDAO


class DepartamentoDao(BaseDAO):
    """Acceso a datos de departamento (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getDepartamentos(self):
        """Lista los registros de departamento."""
        sql = "SELECT id_departamento, id_pais, des_departamento, est_departamento FROM departamentos ORDER BY id_departamento"
        return self.execute_query(sql)

    def getDepartamentoById(self, departamento_id):
        """Devuelve el registro de departamento por su id, o None si no existe."""
        sql = "SELECT id_departamento, id_pais, des_departamento, est_departamento FROM departamentos WHERE id_departamento = %s"
        return self.execute_query_one(sql, (departamento_id,))

    def guardarDepartamento(self, id_pais, descripcion, estado):
        """Inserta un registro de departamento y devuelve el id generado."""
        sql = """
            INSERT INTO departamentos (id_pais, des_departamento, est_departamento)
            VALUES (%s, %s, %s)
            RETURNING id_departamento
        """
        fila = self.execute_query_one(sql, (id_pais, descripcion, estado), commit=True)
        return fila["id_departamento"] if fila else None

    def updateDepartamento(self, departamento_id, id_pais, descripcion, estado):
        """Actualiza los datos de departamento; devuelve True si modificó una fila."""
        sql = """
            UPDATE departamentos
            SET id_pais = %s, des_departamento = %s, est_departamento = %s
            WHERE id_departamento = %s
        """
        return self.execute_query(sql, (id_pais, descripcion, estado, departamento_id), commit=True) > 0
