from app.core.base_dao import BaseDAO


class RegistroSignoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT rs.id_registro_signo, rs.id_consulta, rs.id_signo,
                   rs.registro_intensidad, rs.registro_observaciones, rs.fecha_creacion,
                   s.des_signo
            FROM registro_signos rs
            JOIN signos s ON rs.id_signo = s.id_signo
            WHERE rs.id_consulta = %s AND rs.est_registro_signo = TRUE
            ORDER BY rs.id_registro_signo
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        sql = """
            INSERT INTO registro_signos (
                id_consulta, id_signo, registro_intensidad, registro_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING id_registro_signo
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_signo'],
            datos.get('registro_intensidad'),
            datos.get('registro_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_registro_signo'] if fila else None

    def desactivar(self, id_registro_signo, usuario_modificacion=None):
        sql = """
            UPDATE registro_signos SET est_registro_signo = FALSE, usuario_modificacion = %s
            WHERE id_registro_signo = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_registro_signo), commit=True) > 0
