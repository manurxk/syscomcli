from app.core.base_dao import BaseDAO


class RegistroDiagnosticoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT rd.id_registro_diagnostico, rd.id_consulta, rd.id_diagnostico,
                   rd.registro_tipo, rd.registro_gravedad, rd.des_registro_diagnostico,
                   rd.registro_observaciones, rd.fecha_creacion,
                   d.des_diagnostico, d.cod_cie10
            FROM registro_diagnosticos rd
            JOIN diagnosticos d ON rd.id_diagnostico = d.id_diagnostico
            WHERE rd.id_consulta = %s AND rd.est_registro_diagnostico = TRUE
            ORDER BY rd.id_registro_diagnostico
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        sql = """
            INSERT INTO registro_diagnosticos (
                id_consulta, id_diagnostico, registro_tipo, registro_gravedad,
                des_registro_diagnostico, registro_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_registro_diagnostico
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_diagnostico'],
            datos.get('registro_tipo', 'PRESUNTIVO'),
            datos.get('registro_gravedad'),
            datos.get('des_registro_diagnostico'),
            datos.get('registro_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_registro_diagnostico'] if fila else None

    def desactivar(self, id_registro_diagnostico, usuario_modificacion=None):
        sql = """
            UPDATE registro_diagnosticos SET est_registro_diagnostico = FALSE, usuario_modificacion = %s
            WHERE id_registro_diagnostico = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_registro_diagnostico), commit=True) > 0
