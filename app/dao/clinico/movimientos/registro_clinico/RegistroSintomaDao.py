from app.core.base_dao import BaseDAO


class RegistroSintomaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT rs.id_registro_sintoma, rs.id_consulta, rs.id_sintoma,
                   rs.registro_intensidad, rs.registro_observaciones, rs.fecha_creacion,
                   s.des_sintoma
            FROM registro_sintomas rs
            JOIN sintomas s ON rs.id_sintoma = s.id_sintoma
            WHERE rs.id_consulta = %s AND rs.est_registro_sintoma = TRUE
            ORDER BY rs.id_registro_sintoma
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        sql = """
            INSERT INTO registro_sintomas (
                id_consulta, id_sintoma, registro_intensidad, registro_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING id_registro_sintoma
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_sintoma'],
            datos.get('registro_intensidad'),
            datos.get('registro_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_registro_sintoma'] if fila else None

    def desactivar(self, id_registro_sintoma, usuario_modificacion=None):
        sql = """
            UPDATE registro_sintomas SET est_registro_sintoma = FALSE, usuario_modificacion = %s
            WHERE id_registro_sintoma = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_registro_sintoma), commit=True) > 0
