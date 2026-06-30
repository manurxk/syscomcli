from app.core.base_dao import BaseDAO
from datetime import date


class RecetaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT r.id_receta, r.id_consulta, r.receta_numero, r.receta_fecha,
                   r.receta_validez_dias, r.receta_indicaciones_generales,
                   r.receta_observaciones, r.fecha_creacion
            FROM recetas r
            WHERE r.id_consulta = %s AND r.est_receta = TRUE
            ORDER BY r.id_receta
        """
        recetas = self.execute_query(sql, (id_consulta,))
        if not recetas:
            return []

        ids = tuple(r['id_receta'] for r in recetas)
        detSql = """
            SELECT rd.id_receta, rd.id_receta_detalle, rd.medicamento_dosis,
                   rd.medicamento_frecuencia, rd.medicamento_duracion,
                   rd.medicamento_cantidad, rd.medicamento_indicaciones, m.des_medicamento
            FROM receta_detalle rd
            JOIN medicamentos m ON rd.id_medicamento = m.id_medicamento
            WHERE rd.id_receta IN %s AND rd.est_receta_detalle = TRUE
            ORDER BY rd.id_receta_detalle
        """
        detalles = self.execute_query(detSql, (ids,))
        por_receta = {}
        for d in detalles:
            por_receta.setdefault(d['id_receta'], []).append(d)

        for r in recetas:
            r['receta_fecha'] = r['receta_fecha'].strftime('%Y-%m-%d') if r['receta_fecha'] else None
            r['fecha_creacion'] = r['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if r['fecha_creacion'] else None
            r['detalles'] = por_receta.get(r['id_receta'], [])
        return recetas

    def guardar(self, id_consulta, id_paciente, id_especialista, datos, usuario_creacion=None):
        detalles = datos.get('detalles') or []
        if not detalles:
            raise ValueError('La receta debe tener al menos un medicamento.')

        def _crear(cur):
            anio = date.today().year
            cur.execute(
                "SELECT MAX(CAST(SUBSTRING(receta_numero FROM '[0-9]+$') AS INTEGER)) FROM recetas WHERE receta_numero LIKE %s",
                (f'REC-{anio}-%',)
            )
            siguiente = (cur.fetchone()[0] or 0) + 1
            numero = f'REC-{anio}-{siguiente:04d}'

            cur.execute(
                """
                INSERT INTO recetas(
                    id_consulta, id_paciente, id_especialista, receta_numero, receta_fecha,
                    receta_validez_dias, receta_indicaciones_generales, receta_observaciones,
                    usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_receta
                """,
                (id_consulta, id_paciente, id_especialista, numero, datos['receta_fecha'],
                 datos.get('receta_validez_dias') or 30, datos.get('receta_indicaciones_generales'),
                 datos.get('receta_observaciones'), usuario_creacion)
            )
            id_receta = cur.fetchone()[0]

            for d in detalles:
                cur.execute(
                    """
                    INSERT INTO receta_detalle(
                        id_receta, id_medicamento, medicamento_dosis, medicamento_frecuencia,
                        medicamento_duracion, medicamento_cantidad, medicamento_indicaciones,
                        usuario_creacion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (id_receta, d['id_medicamento'], d['medicamento_dosis'], d['medicamento_frecuencia'],
                     d.get('medicamento_duracion'), d.get('medicamento_cantidad'),
                     d.get('medicamento_indicaciones'), usuario_creacion)
                )
            return id_receta

        return self.execute_transaction(_crear)

    def desactivar(self, id_receta, usuario_modificacion=None):
        sql = "UPDATE recetas SET est_receta = FALSE, usuario_modificacion = %s WHERE id_receta = %s"
        return self.execute_query(sql, (usuario_modificacion, id_receta), commit=True) > 0
