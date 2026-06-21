"""
DashboardDao.py
===============
DAO para las estadísticas del dashboard del sistema Sysclin.

Proporciona métricas reales desde la BD, reemplazando completamente
los valores simulados (multiplicadores por 150000, capacidades fijas, etc.)

Esquema verificado contra clausys_dev (PostgreSQL 17):
  - facturas      : id_factura, fecha_factura, factura_total, ...
  - citas         : id_cita, cita_fecha, id_especialidad, id_estado_cita, cita_activo, ...
  - especialidades: id_especialidad, des_especialidad, ...
  - estados_citas : id_estado_cita, est_cita_nombre, ...
  - pacientes     : id_paciente, id_persona, ...
  - personas      : id_persona, fecha_creacion, ...
  - auditoria_sistema: accion, fecha_evento, ...
"""

from __future__ import annotations

import logging
from typing import Optional

from app.conexion.Conexion import Conexion

logger = logging.getLogger(__name__)


class DashboardDao:
    """DAO para métricas del dashboard.

    Todos los métodos:
    - Abren y cierran su propia conexión
    - Capturan excepciones sin propagarlas al caller
    - Retornan un valor seguro (0, 0.0 o []) en caso de error
    """

    # ------------------------------------------------------------------
    # MÉTODO 1 — Ingresos del mes actual
    # ------------------------------------------------------------------

    def get_ingresos_mes_actual(self) -> float:
        """Retorna la suma de factura_total del mes en curso.

        Note:
            No filtra por estado de factura porque la columna ``factura_estado``
            no existe en el esquema actual.  Suma todo lo registrado en el mes.

        Returns:
            Total facturado (float). Retorna ``0.0`` si no hay registros o
            si ocurre cualquier error.
        """
        sql = """
            SELECT COALESCE(SUM(factura_total), 0.0)
            FROM facturas
            WHERE DATE_TRUNC('month', fecha_factura) = DATE_TRUNC('month', NOW())
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                cur.execute(sql)
                resultado = cur.fetchone()[0]
                return float(resultado) if resultado is not None else 0.0
            except Exception as exc:
                logger.error("Error en get_ingresos_mes_actual: %s", exc, exc_info=True)
                return 0.0
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            logger.error("Conexión fallida en get_ingresos_mes_actual: %s", exc, exc_info=True)
            return 0.0

    # ------------------------------------------------------------------
    # MÉTODO 2 — Pacientes nuevos este mes
    # ------------------------------------------------------------------

    def get_pacientes_nuevos_mes(self) -> int:
        """Retorna el conteo de pacientes registrados en el mes actual.

        Utiliza ``personas.fecha_creacion`` porque ``pacientes`` no tiene
        columna propia de fecha de alta (el registro de persona es el punto
        de creación real).

        Returns:
            Número de pacientes nuevos (int). Retorna ``0`` en caso de error.
        """
        sql = """
            SELECT COUNT(*)
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
            WHERE DATE_TRUNC('month', p.fecha_creacion) = DATE_TRUNC('month', NOW())
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                cur.execute(sql)
                return int(cur.fetchone()[0])
            except Exception as exc:
                logger.error("Error en get_pacientes_nuevos_mes: %s", exc, exc_info=True)
                return 0
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            logger.error("Conexión fallida en get_pacientes_nuevos_mes: %s", exc, exc_info=True)
            return 0

    # ------------------------------------------------------------------
    # MÉTODO 3 — Tasa de ocupación semanal
    # ------------------------------------------------------------------

    def get_tasa_ocupacion(self) -> float:
        """Calcula la tasa de ocupación de la semana actual (%).

        Fórmula::

            tasa = (citas_COMPLETADAS_o_ATENDIDAS / total_citas_activas) × 100

        Semana actual: Monday 00:00 → Sunday 23:59 (DATE_TRUNC 'week' en PG).

        Returns:
            Porcentaje con 1 decimal (float). Retorna ``0.0`` si no hay
            citas activas esta semana o si ocurre cualquier error.
        """
        sql = """
            SELECT
                COUNT(*) FILTER (
                    WHERE ec.est_cita_nombre IN ('COMPLETADA', 'ATENDIDA')
                ) AS realizadas,
                COUNT(*) AS total
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha >= DATE_TRUNC('week', NOW())::DATE
              AND c.cita_fecha <  (DATE_TRUNC('week', NOW()) + INTERVAL '7 days')::DATE
              AND c.cita_activo = TRUE
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                cur.execute(sql)
                fila = cur.fetchone()
                realizadas, total = fila[0], fila[1]
                if not total:
                    return 0.0
                return round((realizadas / total) * 100, 1)
            except Exception as exc:
                logger.error("Error en get_tasa_ocupacion: %s", exc, exc_info=True)
                return 0.0
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            logger.error("Conexión fallida en get_tasa_ocupacion: %s", exc, exc_info=True)
            return 0.0

    # ------------------------------------------------------------------
    # MÉTODO 4 — Citas por especialidad (mes actual)
    # ------------------------------------------------------------------

    def get_conteo_citas_por_especialidad(self) -> list[dict]:
        """Agrupa las citas del mes actual por especialidad.

        Columnas verificadas:
          - ``citas.id_especialidad`` / ``citas.cita_fecha`` / ``citas.cita_activo``
          - ``especialidades.id_especialidad`` / ``especialidades.des_especialidad``

        Returns:
            Lista de dicts ``[{"especialidad": str, "total": int}, ...]``
            ordenada por total descendente.  Retorna ``[]`` en caso de error.
        """
        sql = """
            SELECT
                e.des_especialidad  AS especialidad,
                COUNT(c.id_cita)    AS total
            FROM citas c
            JOIN especialidades e ON c.id_especialidad = e.id_especialidad
            WHERE DATE_TRUNC('month', c.cita_fecha) = DATE_TRUNC('month', NOW())
              AND c.cita_activo = TRUE
            GROUP BY e.des_especialidad
            ORDER BY total DESC
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                cur.execute(sql)
                filas = cur.fetchall()
                return [{"especialidad": fila[0], "total": int(fila[1])} for fila in filas]
            except Exception as exc:
                logger.error("Error en get_conteo_citas_por_especialidad: %s", exc, exc_info=True)
                return []
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            logger.error("Conexión fallida en get_conteo_citas_por_especialidad: %s", exc, exc_info=True)
            return []

    # ------------------------------------------------------------------
    # MÉTODO 5 — Alertas de seguridad
    # ------------------------------------------------------------------

    def get_alertas_seguridad(self) -> int:
        """Evalúa criterios de seguridad y retorna cuántos están activos (0-4).

        Cada criterio aporta 1 al total si supera su umbral:

        +---+----------------------------------------------+----------+
        | # | Criterio                                     | Umbral   |
        +===+==============================================+==========+
        | 1 | Logins fallidos en últimas 24h               | > 0      |
        +---+----------------------------------------------+----------+
        | 2 | Accesos fuera de horario 07–22 (hoy)         | > 0      |
        +---+----------------------------------------------+----------+
        | 3 | Usuarios con >2 cambios de contraseña hoy    | > 0      |
        +---+----------------------------------------------+----------+
        | 4 | Eliminaciones masivas en la última hora       | > 10     |
        +---+----------------------------------------------+----------+

        Note:
            Si ``auditoria_sistema`` no registra la acción ``LOGIN_FAIL``
            aún, el criterio 1 retornará 0 sin error.

        Returns:
            Entero entre 0 y 4. Retorna ``0`` en caso de error de BD.
        """
        criterios_sql = [
            # 1. Logins fallidos últimas 24h
            ("""
                SELECT COUNT(*)
                FROM auditoria_sistema
                WHERE accion = 'LOGIN_FAILED'
                  AND fecha_evento > NOW() - INTERVAL '24 hours'
             """, 0),           # umbral: > 0

            # 2. Accesos fuera de horario laboral (07:00–22:00 Asunción)
            ("""
                SELECT COUNT(*)
                FROM auditoria_sistema
                WHERE accion = 'LOGIN'
                  AND fecha_evento::date = CURRENT_DATE
                  AND EXTRACT(hour FROM fecha_evento AT TIME ZONE 'America/Asuncion')
                      NOT BETWEEN 7 AND 22
             """, 0),           # umbral: > 0

            # 3. Usuarios con >2 cambios de contraseña hoy
            ("""
                SELECT COUNT(*) FROM (
                    SELECT id_usuario
                    FROM auditoria_sistema
                    WHERE accion = 'PASSWORD_CHANGE'
                      AND fecha_evento::date = CURRENT_DATE
                    GROUP BY id_usuario
                    HAVING COUNT(*) > 2
                ) sub
             """, 0),           # umbral: > 0

            # 4. Eliminaciones masivas en la última hora (umbral > 10)
            ("""
                SELECT COUNT(*)
                FROM auditoria_sistema
                WHERE accion = 'RECORD_DELETE'
                  AND fecha_evento > NOW() - INTERVAL '1 hour'
             """, 10),          # umbral: > 10
        ]

        total_alertas = 0
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                for sql, umbral in criterios_sql:
                    try:
                        cur.execute(sql)
                        count = cur.fetchone()[0]
                        if count > umbral:
                            total_alertas += 1
                    except Exception as exc_inner:
                        logger.warning("Error en criterio de alerta: %s", exc_inner)
                        # Un criterio fallido no descarta los demás
                return total_alertas
            except Exception as exc:
                logger.error("Error en get_alertas_seguridad: %s", exc, exc_info=True)
                return 0
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            logger.error("Conexión fallida en get_alertas_seguridad: %s", exc, exc_info=True)
            return 0
