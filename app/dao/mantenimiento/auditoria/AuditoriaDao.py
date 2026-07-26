from app.core.base_dao import BaseDAO


class AuditoriaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def registrar_evento(self, id_usuario, accion, detalle=None, ip_origen=None):
        sql = """
            INSERT INTO auditoria_sistema (id_usuario, accion, detalle, ip_origen)
            VALUES (%s, %s, %s, %s)
            RETURNING id_auditoria
        """
        fila = self.execute_query_one(sql, (id_usuario or None, accion, detalle, ip_origen), commit=True)
        return fila["id_auditoria"] if fila else None

    def getEventos(self, id_usuario=None, fecha_desde=None, fecha_hasta=None, accion=None, pagina=1, por_pagina=50):
        """
        Lista eventos de auditoría con filtros opcionales y paginación.

        Args:
            id_usuario: filtra por usuario que generó el evento.
            fecha_desde / fecha_hasta: rango sobre fecha_evento (YYYY-MM-DD).
            accion: código de acción (ver AuditAccion).
            pagina / por_pagina: paginación.

        Returns:
            Diccionario con datos, total, pagina, por_pagina, total_paginas.
        """
        pagina = max(1, int(pagina))
        por_pagina = max(1, min(200, int(por_pagina)))
        offset = (pagina - 1) * por_pagina

        condiciones = []
        params = []

        if id_usuario:
            condiciones.append("a.id_usuario = %s")
            params.append(id_usuario)
        if fecha_desde:
            condiciones.append("a.fecha_evento >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("a.fecha_evento < (%s::date + INTERVAL '1 day')")
            params.append(fecha_hasta)
        if accion:
            condiciones.append("a.accion = %s")
            params.append(accion)

        where_sql = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

        total_sql = f"SELECT COUNT(*) AS total FROM auditoria_sistema a {where_sql}"
        total_registros = self.execute_query_one(total_sql, tuple(params))["total"]

        datos_sql = f"""
            SELECT
                a.id_auditoria,
                a.id_usuario,
                u.usu_nick,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, 'Sin funcionario') AS funcionario,
                a.accion,
                a.detalle,
                a.ip_origen,
                a.fecha_evento
            FROM auditoria_sistema a
            LEFT JOIN usuarios u ON u.id_usuario = a.id_usuario
            LEFT JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
            LEFT JOIN personas p ON p.id_persona = f.id_persona
            {where_sql}
            ORDER BY a.fecha_evento DESC
            LIMIT %s OFFSET %s
        """
        datos = self.execute_query(datos_sql, tuple(params) + (por_pagina, offset))

        total_paginas = (total_registros + por_pagina - 1) // por_pagina if total_registros else 0

        return {
            "datos": datos,
            "total": total_registros,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total_paginas": total_paginas,
        }
