from app.core.base_dao import BaseDAO


class DerivacionDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT d.id_derivacion, d.id_consulta, d.id_especialidad_destino,
                   e.des_especialidad, d.motivo_derivacion, d.derivacion_observaciones,
                   d.fecha_creacion
            FROM derivaciones d
            JOIN especialidades e ON d.id_especialidad_destino = e.id_especialidad
            WHERE d.id_consulta = %s AND d.est_derivacion = TRUE
            ORDER BY d.id_derivacion
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        sql = """
            INSERT INTO derivaciones (
                id_consulta, id_especialidad_destino, motivo_derivacion,
                derivacion_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING id_derivacion
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_especialidad_destino'],
            datos['motivo_derivacion'],
            datos.get('derivacion_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_derivacion'] if fila else None

    def desactivar(self, id_derivacion, usuario_modificacion=None):
        sql = """
            UPDATE derivaciones SET est_derivacion = FALSE, usuario_modificacion = %s
            WHERE id_derivacion = %s AND est_derivacion = TRUE
        """
        return self.execute_query(sql, (usuario_modificacion, id_derivacion), commit=True) > 0
