"""
AuditoriaDao.py
===============
DAO para el sistema de auditoría del sistema Sysclin.

Centraliza todas las operaciones de base de datos relacionadas con la tabla
``auditoria_sistema``.  Sigue el patrón estándar del proyecto:
``Conexion()`` + ``try / except / finally`` con cierre explícito de cursor
y conexión.

Principio de diseño clave
--------------------------
``registrar_evento`` NUNCA propaga excepciones al caller.  Una falla de
auditoría no debe interrumpir el flujo principal de la aplicación.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from app.conexion.Conexion import Conexion
from app.utils.auditoria_constantes import get_icono, get_label

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers privados
# ---------------------------------------------------------------------------

def _tiempo_relativo(fecha_evento: datetime) -> str:
    """Convierte un datetime (con o sin tz) a texto relativo en español.

    Args:
        fecha_evento: Timestamp del evento.  Puede ser aware o naive.

    Returns:
        Cadena legible como ``"hace 5 minutos"``, ``"hace 3 horas"``,
        ``"hace 2 días"`` o ``"hace un momento"``.
    """
    ahora = datetime.now(tz=timezone.utc)

    # Normalizar a aware UTC para poder restar
    if fecha_evento.tzinfo is None:
        fecha_evento = fecha_evento.replace(tzinfo=timezone.utc)

    delta_seg = int((ahora - fecha_evento).total_seconds())

    if delta_seg < 60:
        return "hace un momento"
    if delta_seg < 3600:
        minutos = delta_seg // 60
        return f"hace {minutos} minuto{'s' if minutos != 1 else ''}"
    if delta_seg < 86400:
        horas = delta_seg // 3600
        return f"hace {horas} hora{'s' if horas != 1 else ''}"

    dias = delta_seg // 86400
    return f"hace {dias} día{'s' if dias != 1 else ''}"


# ---------------------------------------------------------------------------
# DAO principal
# ---------------------------------------------------------------------------

class AuditoriaDao:
    """DAO para la tabla ``auditoria_sistema``.

    Todos los métodos abren y cierran su propia conexión (patrón del
    proyecto).  ``registrar_evento`` suprime las excepciones para no
    interferir con el flujo principal.
    """

    # ------------------------------------------------------------------
    # a) Registrar evento
    # ------------------------------------------------------------------

    def registrar_evento(
        self,
        id_usuario: int,
        accion: str,
        tabla_afectada: str | None = None,
        id_registro: int | None = None,
        detalle: str | None = None,
        ip_origen: str | None = None,
    ) -> bool:
        """Inserta un evento de auditoría en ``auditoria_sistema``.

        Este método **nunca** propaga excepciones al caller.  Si ocurre
        cualquier error (BD no disponible, violación de constraint, etc.)
        solo se registra en el logger de la aplicación.

        Args:
            id_usuario:      ID del usuario que genera el evento.
            accion:          Código de acción (usar constantes de
                             :class:`~app.utils.auditoria_constantes.AuditAccion`).
            tabla_afectada:  Nombre de la tabla afectada (``None`` para
                             eventos de sesión como LOGIN/LOGOUT).
            id_registro:     PK del registro afectado (``None`` si no aplica).
            detalle:         Descripción textual libre del evento.
            ip_origen:       IP del cliente (IPv4 o IPv6).

        Returns:
            ``True`` si el INSERT fue exitoso; ``False`` en caso de error.
        """
        insertSQL = """
            INSERT INTO auditoria_sistema (
                id_usuario,
                accion,
                tabla_afectada,
                id_registro_afectado,
                detalle,
                ip_origen
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                cur.execute(insertSQL, (
                    id_usuario,
                    accion,
                    tabla_afectada,
                    id_registro,
                    detalle,
                    ip_origen,
                ))
                con.commit()
                logger.debug(
                    "Auditoría registrada: usuario=%s accion=%s tabla=%s id_registro=%s",
                    id_usuario, accion, tabla_afectada, id_registro,
                )
                return True
            except Exception as exc:
                con.rollback()
                logger.error(
                    "Error al registrar evento de auditoría (usuario=%s accion=%s): %s",
                    id_usuario, accion, exc, exc_info=True,
                )
                return False
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            # Error al abrir la conexión — igual no propagar
            logger.error(
                "No se pudo abrir conexión para auditoría (usuario=%s accion=%s): %s",
                id_usuario, accion, exc, exc_info=True,
            )
            return False

    # ------------------------------------------------------------------
    # b) Actividad reciente de un usuario
    # ------------------------------------------------------------------

    def obtener_actividad_reciente(
        self,
        id_usuario: int,
        limite: int = 10,
    ) -> list[dict]:
        """Retorna los últimos N eventos de auditoría de un usuario.

        Args:
            id_usuario: ID del usuario cuyos eventos se consultan.
            limite:     Número máximo de filas a retornar (default: 10).

        Returns:
            Lista de dicts con las claves:

            - ``id_auditoria`` (int)
            - ``accion`` (str) — código interno
            - ``label`` (str) — etiqueta en español
            - ``tabla_afectada`` (str | None)
            - ``id_registro_afectado`` (int | None)
            - ``detalle`` (str | None)
            - ``fecha_evento`` (str) — texto relativo, ej. "hace 5 minutos"
            - ``icono`` (str) — clase CSS de Font Awesome 6

            Retorna ``[]`` ante cualquier error.
        """
        selectSQL = """
            SELECT
                id_auditoria,
                accion,
                tabla_afectada,
                id_registro_afectado,
                detalle,
                fecha_evento
            FROM auditoria_sistema
            WHERE id_usuario = %s
            ORDER BY fecha_evento DESC
            LIMIT %s
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                cur.execute(selectSQL, (id_usuario, limite))
                filas = cur.fetchall()
                return [
                    {
                        "id_auditoria":         fila[0],
                        "accion":               fila[1],
                        "label":                get_label(fila[1]),
                        "tabla_afectada":       fila[2],
                        "id_registro_afectado": fila[3],
                        "detalle":              fila[4],
                        "fecha_evento":         _tiempo_relativo(fila[5]),
                        "icono":                get_icono(fila[1]),
                    }
                    for fila in filas
                ]
            except Exception as exc:
                logger.error(
                    "Error al obtener actividad reciente (usuario=%s): %s",
                    id_usuario, exc, exc_info=True,
                )
                return []
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            logger.error(
                "No se pudo abrir conexión para actividad reciente (usuario=%s): %s",
                id_usuario, exc, exc_info=True,
            )
            return []

    # ------------------------------------------------------------------
    # c) Actividad global del sistema
    # ------------------------------------------------------------------

    def obtener_actividad_sistema(self, limite: int = 50) -> list[dict]:
        """Retorna los últimos N eventos de auditoría de todos los usuarios.

        Incluye el nombre del usuario mediante JOIN con la tabla ``usuarios``.

        Args:
            limite: Número máximo de filas a retornar (default: 50).

        Returns:
            Lista de dicts con las claves:

            - ``id_auditoria`` (int)
            - ``id_usuario`` (int | None) — None si el usuario fue eliminado
            - ``nombre_usuario`` (str) — nombre de usuario o ``"[eliminado]"``
            - ``accion`` (str) — código interno
            - ``label`` (str) — etiqueta en español
            - ``tabla_afectada`` (str | None)
            - ``id_registro_afectado`` (int | None)
            - ``detalle`` (str | None)
            - ``ip_origen`` (str | None)
            - ``fecha_evento`` (str) — texto relativo
            - ``icono`` (str) — clase CSS de Font Awesome 6

            Retorna ``[]`` ante cualquier error.

        Raises:
            No lanza excepciones; los errores se registran en el logger.
        """
        selectSQL = """
            SELECT
                a.id_auditoria,
                a.id_usuario,
                COALESCE(u.usu_nick, '[eliminado]') AS nombre_usuario,
                a.accion,
                a.tabla_afectada,
                a.id_registro_afectado,
                a.detalle,
                a.ip_origen,
                a.fecha_evento
            FROM auditoria_sistema a
            LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario
            ORDER BY a.fecha_evento DESC
            LIMIT %s
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            try:
                cur.execute(selectSQL, (limite,))
                filas = cur.fetchall()
                return [
                    {
                        "id_auditoria":         fila[0],
                        "id_usuario":           fila[1],
                        "nombre_usuario":       fila[2],
                        "accion":               fila[3],
                        "label":                get_label(fila[3]),
                        "tabla_afectada":       fila[4],
                        "id_registro_afectado": fila[5],
                        "detalle":              fila[6],
                        "ip_origen":            fila[7],
                        "fecha_evento":         _tiempo_relativo(fila[8]),
                        "icono":                get_icono(fila[3]),
                    }
                    for fila in filas
                ]
            except Exception as exc:
                logger.error(
                    "Error al obtener actividad del sistema: %s",
                    exc, exc_info=True,
                )
                return []
            finally:
                cur.close()
                con.close()
        except Exception as exc:
            logger.error(
                "No se pudo abrir conexión para actividad del sistema: %s",
                exc, exc_info=True,
            )
            return []
