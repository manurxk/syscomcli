from app.core.base_dao import BaseDAO
from datetime import date


class OrdenDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT o.id_orden, o.id_consulta, o.orden_numero, o.orden_fecha,
                   o.orden_estado, o.orden_observaciones, o.orden_indicaciones, o.fecha_creacion
            FROM ordenes o
            WHERE o.id_consulta = %s AND o.est_orden = TRUE
            ORDER BY o.id_orden
        """
        ordenes = self.execute_query(sql, (id_consulta,))
        if not ordenes:
            return []

        ids = tuple(o['id_orden'] for o in ordenes)
        detSql = """
            SELECT od.id_orden, od.id_orden_detalle, od.tipo_orden,
                   te.des_tipo_estudio, ta.des_tipo_analisis, od.observaciones
            FROM orden_detalle od
            LEFT JOIN tipos_estudios te ON od.id_tipo_estudio = te.id_tipo_estudio
            LEFT JOIN tipos_analisis ta ON od.id_tipo_analisis = ta.id_tipo_analisis
            WHERE od.id_orden IN %s AND od.est_orden_detalle = TRUE
            ORDER BY od.id_orden_detalle
        """
        detalles = self.execute_query(detSql, (ids,))
        por_orden = {}
        for d in detalles:
            por_orden.setdefault(d['id_orden'], []).append({
                'id_orden_detalle': d['id_orden_detalle'],
                'tipo_orden': d['tipo_orden'],
                'descripcion': d['des_tipo_estudio'] or d['des_tipo_analisis'],
                'observaciones': d['observaciones'],
            })

        for o in ordenes:
            o['orden_fecha'] = o['orden_fecha'].strftime('%Y-%m-%d') if o['orden_fecha'] else None
            o['fecha_creacion'] = o['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if o['fecha_creacion'] else None
            o['detalles'] = por_orden.get(o['id_orden'], [])
        return ordenes

    def guardar(self, id_consulta, id_paciente, id_especialista, datos, usuario_creacion=None):
        detalles = datos.get('detalles') or []
        if not detalles:
            raise ValueError('La orden debe tener al menos un ítem de estudio o análisis.')

        def _crear(cur):
            anio = date.today().year
            cur.execute(
                "SELECT MAX(CAST(SUBSTRING(orden_numero FROM '[0-9]+$') AS INTEGER)) FROM ordenes WHERE orden_numero LIKE %s",
                (f'ORD-{anio}-%',)
            )
            siguiente = (cur.fetchone()[0] or 0) + 1
            numero = f'ORD-{anio}-{siguiente:04d}'

            cur.execute(
                """
                INSERT INTO ordenes(
                    id_consulta, id_paciente, id_especialista, orden_numero, orden_fecha,
                    orden_observaciones, orden_indicaciones, usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_orden
                """,
                (id_consulta, id_paciente, id_especialista, numero, datos['orden_fecha'],
                 datos.get('orden_observaciones'), datos.get('orden_indicaciones'), usuario_creacion)
            )
            id_orden = cur.fetchone()[0]

            for d in detalles:
                tipo_orden = d['tipo_orden']
                cur.execute(
                    """
                    INSERT INTO orden_detalle(
                        id_orden, tipo_orden, id_tipo_estudio, id_tipo_analisis,
                        observaciones, usuario_creacion
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (id_orden, tipo_orden,
                     d.get('id_tipo_estudio') if tipo_orden == 'ESTUDIO' else None,
                     d.get('id_tipo_analisis') if tipo_orden == 'ANALISIS' else None,
                     d.get('observaciones'), usuario_creacion)
                )
            return id_orden

        return self.execute_transaction(_crear)

    def desactivar(self, id_orden, usuario_modificacion=None):
        sql = "UPDATE ordenes SET est_orden = FALSE, usuario_modificacion = %s WHERE id_orden = %s"
        return self.execute_query(sql, (usuario_modificacion, id_orden), commit=True) > 0
