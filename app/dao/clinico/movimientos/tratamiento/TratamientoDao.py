from app.core.base_dao import BaseDAO


class TratamientoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT t.id_tratamiento, t.id_consulta, t.id_tipo_tratamiento,
                   t.des_tratamiento, t.tratamiento_objetivos, t.numero_sesiones,
                   t.frecuencia_sesiones, t.duracion_sesion,
                   t.tratamiento_fecha_inicio, t.tratamiento_fecha_fin,
                   t.tratamiento_estado, t.tratamiento_observaciones, t.fecha_creacion,
                   tt.des_tipo_tratamiento
            FROM tratamientos t
            JOIN tipos_tratamientos tt ON t.id_tipo_tratamiento = tt.id_tipo_tratamiento
            WHERE t.id_consulta = %s AND t.est_tratamiento = TRUE
            ORDER BY t.id_tratamiento
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['tratamiento_fecha_inicio'] = f['tratamiento_fecha_inicio'].strftime('%Y-%m-%d') if f['tratamiento_fecha_inicio'] else None
            f['tratamiento_fecha_fin'] = f['tratamiento_fecha_fin'].strftime('%Y-%m-%d') if f['tratamiento_fecha_fin'] else None
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        sql = """
            INSERT INTO tratamientos (
                id_consulta, id_tipo_tratamiento, des_tratamiento, tratamiento_objetivos,
                numero_sesiones, frecuencia_sesiones, duracion_sesion,
                tratamiento_fecha_inicio, tratamiento_observaciones, usuario_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_tratamiento
        """
        fila = self.execute_query_one(sql, (
            id_consulta,
            datos['id_tipo_tratamiento'],
            datos['des_tratamiento'],
            datos.get('tratamiento_objetivos'),
            datos.get('numero_sesiones'),
            datos.get('frecuencia_sesiones'),
            datos.get('duracion_sesion'),
            datos['tratamiento_fecha_inicio'],
            datos.get('tratamiento_observaciones'),
            usuario_creacion,
        ), commit=True)
        return fila['id_tratamiento'] if fila else None

    def desactivar(self, id_tratamiento, usuario_modificacion=None):
        sql = """
            UPDATE tratamientos SET est_tratamiento = FALSE, usuario_modificacion = %s
            WHERE id_tratamiento = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_tratamiento), commit=True) > 0
