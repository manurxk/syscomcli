from app.core.base_dao import BaseDAO


class RegistroProcedimientoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT rp.id_registro_procedimiento, rp.id_consulta, rp.id_tipo_procedimiento,
                   rp.des_registro_procedimiento, rp.registro_duracion, rp.registro_resultado,
                   rp.registro_observaciones, rp.fecha_creacion,
                   tp.des_tipo_procedimiento
            FROM registro_procedimientos rp
            JOIN tipos_procedimientos tp ON rp.id_tipo_procedimiento = tp.id_tipo_procedimiento
            WHERE rp.id_consulta = %s AND rp.est_registro_procedimiento = TRUE
            ORDER BY rp.id_registro_procedimiento
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        sql = """
            INSERT INTO registro_procedimientos (
                id_consulta, id_tipo_procedimiento, des_registro_procedimiento,
                registro_duracion, registro_resultado, registro_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_registro_procedimiento
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_tipo_procedimiento'],
            datos.get('des_registro_procedimiento'),
            datos.get('registro_duracion'),
            datos.get('registro_resultado'),
            datos.get('registro_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_registro_procedimiento'] if fila else None

    def desactivar(self, id_registro_procedimiento, usuario_modificacion=None):
        sql = """
            UPDATE registro_procedimientos SET est_registro_procedimiento = FALSE, usuario_modificacion = %s
            WHERE id_registro_procedimiento = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_registro_procedimiento), commit=True) > 0
