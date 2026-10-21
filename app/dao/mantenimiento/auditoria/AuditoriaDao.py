from app.core.base_dao import BaseDAO


class AuditoriaDao(BaseDAO):
    """Acceso a datos de la auditoría: eventos del sistema, cambios en datos y alertas."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def registrar_evento(self, id_usuario, accion, detalle=None, ip_origen=None):
        """Inserta un evento en la auditoría del sistema y devuelve su id."""
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

    def getIntentosAcceso(self, fecha_desde=None, fecha_hasta=None, ip=None,
                           solo_fallidos=False, pagina=1, por_pagina=50, id_usuario=None):
        """Intentos de login (accesos_sistema): un registro por cada intento,
        exitoso o no, con resultado/IP/user-agent. A diferencia de getEventos()
        (auditoria_sistema, eventos generales del sistema), esta es la tabla
        detallada que también usa el rate-limiting por IP."""
        pagina = max(1, int(pagina))
        por_pagina = max(1, min(200, int(por_pagina)))
        offset = (pagina - 1) * por_pagina

        condiciones = []
        params = []

        if fecha_desde:
            condiciones.append("a.fecha_intento >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("a.fecha_intento < (%s::date + INTERVAL '1 day')")
            params.append(fecha_hasta)
        if ip:
            condiciones.append("a.ip_origen = %s::inet")
            params.append(ip)
        if solo_fallidos:
            condiciones.append("a.resultado != 'EXITOSO'")
        if id_usuario:
            condiciones.append("a.id_usuario = %s")
            params.append(id_usuario)

        where_sql = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

        total_sql = f"SELECT COUNT(*) AS total FROM accesos_sistema a {where_sql}"
        total_registros = self.execute_query_one(total_sql, tuple(params))["total"]

        datos_sql = f"""
            SELECT a.id_acceso, a.id_usuario, a.usuario_intentado, a.resultado,
                   a.ip_origen, a.user_agent, a.fecha_intento
            FROM accesos_sistema a
            {where_sql}
            ORDER BY a.fecha_intento DESC
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

    def getIpsSospechosas(self, fecha_desde=None, fecha_hasta=None, minimo_cuentas=2):
        """IPs cuyos intentos fallidos tocaron varias cuentas distintas en el
        período — patrón de fuerza bruta/credential stuffing, no el simple
        olvido de contraseña de un usuario."""
        condiciones = ["a.resultado != 'EXITOSO'"]
        params = []
        if fecha_desde:
            condiciones.append("a.fecha_intento >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("a.fecha_intento < (%s::date + INTERVAL '1 day')")
            params.append(fecha_hasta)
        where_sql = f"WHERE {' AND '.join(condiciones)}"

        sql = f"""
            SELECT a.ip_origen,
                   COUNT(DISTINCT a.usuario_intentado) AS cuentas_distintas,
                   COUNT(*) AS total_fallos,
                   MIN(a.fecha_intento) AS primer_intento,
                   MAX(a.fecha_intento) AS ultimo_intento
            FROM accesos_sistema a
            {where_sql}
            GROUP BY a.ip_origen
            HAVING COUNT(DISTINCT a.usuario_intentado) >= %s
            ORDER BY cuentas_distintas DESC, total_fallos DESC
        """
        return self.execute_query(sql, tuple(params) + (minimo_cuentas,))

    def getSolicitudesRecuperacionGlobal(self, fecha_desde=None, fecha_hasta=None, pagina=1, por_pagina=50,
                                         id_usuario=None):
        """Solicitudes de recuperación de contraseña de todos los usuarios."""
        pagina = max(1, int(pagina))
        por_pagina = max(1, min(200, int(por_pagina)))
        offset = (pagina - 1) * por_pagina

        condiciones = []
        params = []
        if fecha_desde:
            condiciones.append("t.fecha_creacion >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("t.fecha_creacion < (%s::date + INTERVAL '1 day')")
            params.append(fecha_hasta)
        if id_usuario:
            condiciones.append("t.id_usuario = %s")
            params.append(id_usuario)
        where_sql = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

        total_sql = f"SELECT COUNT(*) AS total FROM password_reset_tokens t {where_sql}"
        total_registros = self.execute_query_one(total_sql, tuple(params))["total"]

        datos_sql = f"""
            SELECT t.id_token, t.id_usuario, u.usu_nick, t.email_destino,
                   t.ip_solicitud, t.fecha_creacion, t.fecha_expiracion, t.usado, t.fecha_uso
            FROM password_reset_tokens t
            LEFT JOIN usuarios u ON u.id_usuario = t.id_usuario
            {where_sql}
            ORDER BY t.fecha_creacion DESC
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

    # ------------------------------------------------------------------
    # Cambios en datos (auditoria_transacciones, PDF 9). Qué módulos se
    # consultan lo decide la ruta según los roles de la sesión
    # (alcance_cambios en app/utils/auditoria_constantes.py).
    # ------------------------------------------------------------------

    # Un cambio es una anulación si pasa a anulada una factura (fecha_anulacion), una nota de crédito o de
    # débito o una cobranza (estado ANULADA). Lo usan el resumen y las alertas.
    SQL_ES_ANULACION = """(t.operacion = 'UPDATE' AND (
            (t.tabla = 'facturas' AND 'fecha_anulacion' = ANY(t.campos_modificados) AND t.datos_nuevos->>'fecha_anulacion' IS NOT NULL)
         OR (t.tabla = 'notas_credito' AND 'est_nota_credito' = ANY(t.campos_modificados) AND t.datos_nuevos->>'est_nota_credito' = 'ANULADA')
         OR (t.tabla = 'notas_debito' AND 'est_nota_debito' = ANY(t.campos_modificados) AND t.datos_nuevos->>'est_nota_debito' = 'ANULADA')
         OR (t.tabla = 'cobranzas' AND 'est_cobranza' = ANY(t.campos_modificados) AND t.datos_nuevos->>'est_cobranza' = 'ANULADA')))"""

    def _filtrosCambios(self, modulos, tabla=None, operacion=None, id_usuario=None,
                        fecha_desde=None, fecha_hasta=None, id_registro=None, modulos_propios=None, id_propio=None):
        """modulos: se ven todos sus cambios; modulos_propios: solo los que hizo id_propio (usuario de la sesión)."""
        condiciones = ["(t.modulo = ANY(%s) OR (t.modulo = ANY(%s) AND t.id_usuario = %s))"]
        params = [list(modulos or []), list(modulos_propios or []) if id_propio else [], id_propio]
        if tabla:
            condiciones.append("t.tabla = %s")
            params.append(tabla)
        if operacion:
            condiciones.append("t.operacion = %s")
            params.append(operacion)
        if id_usuario:
            condiciones.append("t.id_usuario = %s")
            params.append(id_usuario)
        if id_registro:
            condiciones.append("t.id_registro = %s")
            params.append(str(id_registro))
        if fecha_desde:
            condiciones.append("t.fecha_cambio >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("t.fecha_cambio < (%s::date + INTERVAL '1 day')")
            params.append(fecha_hasta)
        return "WHERE " + " AND ".join(condiciones), params

    def getCambios(self, modulos, tabla=None, operacion=None, id_usuario=None, fecha_desde=None,
                   fecha_hasta=None, id_registro=None, pagina=1, por_pagina=50, modulos_propios=None, id_propio=None):
        """Listado de cambios en datos de los módulos indicados (y, de modulos_propios, solo los de id_propio),
        sin el contenido (antes/después): ese se pide de a uno con getCambio. Sin módulos no devuelve nada."""
        pagina = max(1, int(pagina))
        por_pagina = max(1, min(500, int(por_pagina)))
        if not modulos and not (modulos_propios and id_propio):
            return {"datos": [], "total": 0, "pagina": pagina, "por_pagina": por_pagina, "total_paginas": 0}
        where_sql, params = self._filtrosCambios(modulos, tabla, operacion, id_usuario,
                                                 fecha_desde, fecha_hasta, id_registro, modulos_propios, id_propio)
        total = self.execute_query_one(f"SELECT COUNT(*) AS total FROM auditoria_transacciones t {where_sql}",
                                       tuple(params))["total"]
        datos = self.execute_query(f"""
            SELECT t.id_auditoria_transaccion, t.fecha_cambio, t.tabla, t.modulo, t.operacion, t.id_registro,
                   t.campos_modificados, t.id_usuario, u.usu_nick, t.roles, host(t.ip_origen) AS ip_origen,
                   {self.SQL_ES_ANULACION} AS es_anulacion
            FROM auditoria_transacciones t
            LEFT JOIN usuarios u ON u.id_usuario = t.id_usuario
            {where_sql}
            ORDER BY t.id_auditoria_transaccion DESC
            LIMIT %s OFFSET %s
        """, tuple(params) + (por_pagina, (pagina - 1) * por_pagina))
        return {"datos": datos, "total": total, "pagina": pagina, "por_pagina": por_pagina,
                "total_paginas": (total + por_pagina - 1) // por_pagina if total else 0}

    def getCambio(self, id_auditoria_transaccion):
        """Un cambio completo, con el dato anterior y el nuevo."""
        return self.execute_query_one("""
            SELECT t.id_auditoria_transaccion, t.fecha_cambio, t.tabla, t.modulo, t.operacion, t.id_registro,
                   t.datos_anteriores, t.datos_nuevos, t.campos_modificados, t.id_usuario, u.usu_nick,
                   t.roles, host(t.ip_origen) AS ip_origen
            FROM auditoria_transacciones t
            LEFT JOIN usuarios u ON u.id_usuario = t.id_usuario
            WHERE t.id_auditoria_transaccion = %s
        """, (id_auditoria_transaccion,))

    def getResumenCambios(self, modulos, fecha_desde=None, fecha_hasta=None, modulos_propios=None, id_propio=None):
        """Solo cantidades (sin registros ni usuarios): totales por operación, anulaciones, cambios por
        tabla y por día. Es lo único que ve un rol con nivel "resumen" (Ventas)."""
        vacio = {"totales": {"INSERT": 0, "UPDATE": 0, "DELETE": 0, "anulaciones": 0}, "por_tabla": [], "por_dia": []}
        if not modulos and not (modulos_propios and id_propio):
            return vacio
        where_sql, params = self._filtrosCambios(modulos, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
                                                 modulos_propios=modulos_propios, id_propio=id_propio)
        p = tuple(params)
        totales = self.execute_query_one(f"""
            SELECT COUNT(*) FILTER (WHERE t.operacion = 'INSERT') AS "INSERT",
                   COUNT(*) FILTER (WHERE t.operacion = 'UPDATE') AS "UPDATE",
                   COUNT(*) FILTER (WHERE t.operacion = 'DELETE') AS "DELETE",
                   COUNT(*) FILTER (WHERE {self.SQL_ES_ANULACION}) AS anulaciones
            FROM auditoria_transacciones t {where_sql}
        """, p)
        por_tabla = self.execute_query(f"""
            SELECT t.modulo, t.tabla,
                   COUNT(*) FILTER (WHERE t.operacion = 'INSERT') AS altas,
                   COUNT(*) FILTER (WHERE t.operacion = 'UPDATE') AS modificaciones,
                   COUNT(*) FILTER (WHERE t.operacion = 'DELETE') AS bajas,
                   COUNT(*) FILTER (WHERE {self.SQL_ES_ANULACION}) AS anulaciones,
                   COUNT(*) AS total
            FROM auditoria_transacciones t {where_sql}
            GROUP BY t.modulo, t.tabla
            ORDER BY total DESC, t.tabla
        """, p)
        por_dia = self.execute_query(f"""
            SELECT t.fecha_cambio::date AS dia, COUNT(*) AS total
            FROM auditoria_transacciones t {where_sql}
            GROUP BY 1 ORDER BY 1
        """, p)
        return {"totales": totales or vacio["totales"], "por_tabla": por_tabla, "por_dia": por_dia}

    # ------------------------------------------------------------------
    # Alertas por correo e informe semanal (PDF 9, paso 6)
    # ------------------------------------------------------------------

    def getMaxIdCambio(self):
        """Devuelve el mayor id de cambio registrado en la auditoría de transacciones (0 si no hay)."""
        fila = self.execute_query_one("SELECT COALESCE(MAX(id_auditoria_transaccion), 0) AS maximo FROM auditoria_transacciones")
        return fila["maximo"]

    def getUltimoIdAlertado(self):
        """Hasta qué cambio se revisó en la última alerta enviada: lo guarda el detalle del último evento
        ALERTA_ENVIADA ("... hasta el cambio #N ..."). None si nunca se envió una alerta."""
        fila = self.execute_query_one("""
            SELECT detalle FROM auditoria_sistema WHERE accion = 'ALERTA_ENVIADA'
            ORDER BY id_auditoria DESC LIMIT 1
        """)
        if not fila or not fila["detalle"] or "#" not in fila["detalle"]:
            return None
        numero = fila["detalle"].split("#", 1)[1].split()[0].rstrip(":.,;")
        return int(numero) if numero.isdigit() else None

    def getCambiosDesde(self, id_desde, limite=2000):
        """Cambios posteriores a id_desde (sin el antes/después), del más viejo al más nuevo, con la marca de anulación."""
        return self.execute_query(f"""
            SELECT t.id_auditoria_transaccion, t.fecha_cambio, t.tabla, t.modulo, t.operacion, t.id_registro,
                   t.id_usuario, u.usu_nick, t.roles, host(t.ip_origen) AS ip_origen,
                   {self.SQL_ES_ANULACION} AS es_anulacion
            FROM auditoria_transacciones t
            LEFT JOIN usuarios u ON u.id_usuario = t.id_usuario
            WHERE t.id_auditoria_transaccion > %s
            ORDER BY t.id_auditoria_transaccion
            LIMIT %s
        """, (id_desde, limite))

    def getCambiosPeriodo(self, modulos, fecha_desde, fecha_hasta):
        """Cambios de un período (sin el antes/después) de los módulos indicados, para el informe semanal."""
        if not modulos:
            return []
        where_sql, params = self._filtrosCambios(modulos, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
        return self.execute_query(f"""
            SELECT t.id_auditoria_transaccion, t.fecha_cambio, t.tabla, t.modulo, t.operacion, t.id_registro,
                   u.usu_nick, t.roles, host(t.ip_origen) AS ip_origen, {self.SQL_ES_ANULACION} AS es_anulacion
            FROM auditoria_transacciones t
            LEFT JOIN usuarios u ON u.id_usuario = t.id_usuario
            {where_sql}
            ORDER BY t.id_auditoria_transaccion
        """, tuple(params))

    def getResumenEventosSeguridad(self, fecha_desde, fecha_hasta):
        """Cantidad de eventos de seguridad de auditoria_sistema en el período, por acción."""
        return self.execute_query("""
            SELECT accion, COUNT(*) AS cantidad
            FROM auditoria_sistema
            WHERE accion IN ('LOGIN_FAILED', 'ACCOUNT_LOCKED', 'ACCOUNT_UNLOCKED', 'RATE_LIMIT', 'PASSWORD_CHANGE')
              AND fecha_evento >= %s AND fecha_evento < (%s::date + INTERVAL '1 day')
            GROUP BY accion ORDER BY cantidad DESC
        """, (fecha_desde, fecha_hasta))

    def getDestinatariosAuditoria(self):
        """Administradores y Superadministradores activos con correo, con sus roles (para filtrar qué ve cada uno)."""
        return self.execute_query("""
            SELECT u.id_usuario, u.usu_nick, u.correo, array_agg(r.cod_rol ORDER BY r.cod_rol) AS roles
            FROM usuarios u
            JOIN usuarios_roles ur ON ur.id_usuario = u.id_usuario AND ur.est_usuario_rol = TRUE
            JOIN roles r ON r.id_rol = ur.id_rol
            WHERE u.est_usuario = TRUE AND COALESCE(TRIM(u.correo), '') <> ''
            GROUP BY u.id_usuario, u.usu_nick, u.correo
            HAVING bool_or(r.cod_rol IN ('ADMINISTRADOR', 'SUPERADMIN'))
            ORDER BY u.id_usuario
        """)

    def getTablasCambios(self, modulos, modulos_propios=None, id_propio=None):
        """Tablas con cambios registrados en los módulos indicados (para el filtro de la pantalla)."""
        if not modulos and not (modulos_propios and id_propio):
            return []
        where_sql, params = self._filtrosCambios(modulos, modulos_propios=modulos_propios, id_propio=id_propio)
        return self.execute_query(f"""
            SELECT DISTINCT t.tabla, t.modulo FROM auditoria_transacciones t
            {where_sql} ORDER BY t.modulo, t.tabla
        """, tuple(params))
