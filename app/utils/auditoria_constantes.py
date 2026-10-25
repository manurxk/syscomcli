"""
auditoria_constantes.py
=======================
Módulo de constantes para el sistema de auditoría del sistema SYSCLIN.

Centraliza las acciones auditables, sus íconos de Font Awesome 6 y sus
etiquetas en español.  No tiene dependencias externas (solo stdlib).

Uso típico::

    from app.utils.auditoria_constantes import AuditAccion, ICON_MAP, LABEL_MAP, get_icono

    accion = AuditAccion.LOGIN
    icono  = get_icono(accion)          # "fa-solid fa-right-to-bracket"
    label  = LABEL_MAP[accion]          # "Inicio de sesión"
"""

from __future__ import annotations

__all__ = [
    "AuditAccion",
    "ICON_MAP",
    "LABEL_MAP",
    "get_icono",
    "get_label",
]

# ---------------------------------------------------------------------------
# a) Constantes de acciones auditables
# ---------------------------------------------------------------------------

class AuditAccion:
    """Constantes string para cada acción auditable del sistema.

    Los valores coinciden exactamente con los permitidos por el CHECK
    constraint de la columna ``accion`` en la tabla ``auditoria_sistema``.
    """

    LOGIN:           str = "LOGIN"
    LOGOUT:          str = "LOGOUT"
    LOGIN_FAILED:    str = "LOGIN_FAILED"
    PROFILE_UPDATE:  str = "PROFILE_UPDATE"
    RECORD_CREATE:   str = "RECORD_CREATE"
    RECORD_UPDATE:   str = "RECORD_UPDATE"
    RECORD_DELETE:   str = "RECORD_DELETE"
    PASSWORD_CHANGE: str = "PASSWORD_CHANGE"
    REPORT_VIEW:     str = "REPORT_VIEW"
    REPORT_EXPORT:   str = "REPORT_EXPORT"      # exportación de un reporte a PDF (con el reporte y los filtros en el detalle)
    RATE_LIMIT:       str = "RATE_LIMIT"        # IP o recuperación frenada por exceso de intentos
    ACCOUNT_LOCKED:   str = "ACCOUNT_LOCKED"    # cuenta bloqueada por la escalada de intentos fallidos
    ACCOUNT_UNLOCKED: str = "ACCOUNT_UNLOCKED"  # cuenta desbloqueada por un administrador
    ALERTA_ENVIADA:   str = "ALERTA_ENVIADA"    # alerta de auditoría enviada por correo (marca hasta qué cambio se avisó)
    INFORME_SEMANAL:  str = "INFORME_SEMANAL"   # informe semanal de auditoría enviado por correo

    # Conjunto para validación rápida
    _ALL: frozenset[str] = frozenset({
        LOGIN,
        LOGOUT,
        LOGIN_FAILED,
        PROFILE_UPDATE,
        RECORD_CREATE,
        RECORD_UPDATE,
        RECORD_DELETE,
        PASSWORD_CHANGE,
        REPORT_VIEW,
        REPORT_EXPORT,
        RATE_LIMIT,
        ACCOUNT_LOCKED,
        ACCOUNT_UNLOCKED,
        ALERTA_ENVIADA,
        INFORME_SEMANAL,
    })

    @classmethod
    def es_valida(cls, accion: str) -> bool:
        """Retorna ``True`` si *accion* es un valor reconocido."""
        return accion in cls._ALL


# ---------------------------------------------------------------------------
# b) Mapa de íconos — Font Awesome 6 (clase CSS completa)
# ---------------------------------------------------------------------------

ICON_MAP: dict[str, str] = {
    AuditAccion.LOGIN:           "fa-solid fa-right-to-bracket",
    AuditAccion.LOGOUT:          "fa-solid fa-right-from-bracket",
    AuditAccion.LOGIN_FAILED:    "fa-solid fa-user-xmark",
    AuditAccion.PROFILE_UPDATE:  "fa-solid fa-user-pen",
    AuditAccion.RECORD_CREATE:   "fa-solid fa-plus-circle",
    AuditAccion.RECORD_UPDATE:   "fa-solid fa-pen-to-square",
    AuditAccion.RECORD_DELETE:   "fa-solid fa-trash",
    AuditAccion.PASSWORD_CHANGE: "fa-solid fa-key",
    AuditAccion.REPORT_VIEW:     "fa-solid fa-chart-bar",
    AuditAccion.REPORT_EXPORT:   "fa-solid fa-file-pdf",
    AuditAccion.RATE_LIMIT:       "fa-solid fa-gauge-high",
    AuditAccion.ACCOUNT_LOCKED:   "fa-solid fa-lock",
    AuditAccion.ACCOUNT_UNLOCKED: "fa-solid fa-lock-open",
    AuditAccion.ALERTA_ENVIADA:   "fa-solid fa-bell",
    AuditAccion.INFORME_SEMANAL:  "fa-solid fa-file-pdf",
}
"""Diccionario que mapea cada acción a su clase CSS de Font Awesome 6.

Reemplaza la necesidad de almacenar íconos en la base de datos —
la lógica de presentación vive exclusivamente en la capa Python.
"""

# ---------------------------------------------------------------------------
# c) Mapa de etiquetas en español
# ---------------------------------------------------------------------------

LABEL_MAP: dict[str, str] = {
    AuditAccion.LOGIN:           "Inicio de sesión",
    AuditAccion.LOGOUT:          "Cierre de sesión",
    AuditAccion.LOGIN_FAILED:    "Intento fallido de sesión",
    AuditAccion.PROFILE_UPDATE:  "Actualización de perfil",
    AuditAccion.RECORD_CREATE:   "Creación de registro",
    AuditAccion.RECORD_UPDATE:   "Modificación de registro",
    AuditAccion.RECORD_DELETE:   "Eliminación de registro",
    AuditAccion.PASSWORD_CHANGE: "Cambio de contraseña",
    AuditAccion.REPORT_VIEW:     "Visualización de reporte",
    AuditAccion.REPORT_EXPORT:   "Exportación de reporte a PDF",
    AuditAccion.RATE_LIMIT:       "Límite de intentos superado",
    AuditAccion.ACCOUNT_LOCKED:   "Cuenta bloqueada",
    AuditAccion.ACCOUNT_UNLOCKED: "Cuenta desbloqueada",
    AuditAccion.ALERTA_ENVIADA:   "Alerta de auditoría enviada",
    AuditAccion.INFORME_SEMANAL:  "Informe semanal de auditoría enviado",
}
"""Diccionario que mapea cada acción a su etiqueta descriptiva en español."""

# ---------------------------------------------------------------------------
# d) Funciones de utilidad
# ---------------------------------------------------------------------------

_ICONO_DEFECTO: str = "fa-solid fa-circle-question"
_LABEL_DEFECTO: str = "Acción desconocida"


def get_icono(accion: str) -> str:
    """Retorna la clase CSS de Font Awesome 6 correspondiente a *accion*.

    Args:
        accion: Código de acción (ej. ``"LOGIN"``).  No distingue mayúsculas
                ni espacios laterales.

    Returns:
        Clase CSS del ícono (ej. ``"fa-solid fa-right-to-bracket"``).
        Si la acción no está registrada devuelve
        ``"fa-solid fa-circle-question"``.
    """
    return ICON_MAP.get(accion.strip().upper(), _ICONO_DEFECTO)


def get_label(accion: str) -> str:
    """Retorna la etiqueta en español correspondiente a *accion*.

    Args:
        accion: Código de acción (ej. ``"RECORD_DELETE"``).

    Returns:
        Etiqueta legible (ej. ``"Eliminación de registro"``).
        Si la acción no está registrada devuelve ``"Acción desconocida"``.
    """
    return LABEL_MAP.get(accion.strip().upper(), _LABEL_DEFECTO)


# ---------------------------------------------------------------------------
# d) Alcance de la auditoría de cambios en datos (auditoria_transacciones) por rol
# ---------------------------------------------------------------------------
# Cada cambio auditado tiene un módulo (lo fija el trigger fn_auditar_cambios). Por módulo, un rol ve:
#   "detalle": el listado de cambios de todos los usuarios, con el dato anterior y el nuevo;
#   "propios": lo mismo, pero solo los cambios que hizo el usuario de la sesión;
#   "resumen": solo cantidades (cambios por tabla, operación y día, anulaciones), sin registros ni usuarios.
# Los datos clínicos solo los ven Clínico (los suyos) y Administrador (todos); el Superadministrador (soporte) solo ve Seguridad.
# Decisiones del usuario, 2026-10-18 y 2026-10-19 (docs/taller_programacion/09_plan_auditoria_triggers.md, paso 5).

MODULOS_AUDITORIA = ("CLINICO", "AGENDAMIENTO", "VENTAS", "SEGURIDAD")

ALCANCE_CAMBIOS_POR_ROL: dict[str, dict[str, str]] = {
    "ADMINISTRADOR": {m: "detalle" for m in MODULOS_AUDITORIA},
    "SUPERADMIN":    {"SEGURIDAD": "detalle"},   # soporte: sin datos de pacientes ni de ventas
    "RECEPCION":     {"AGENDAMIENTO": "detalle"},
    "CLINICO":       {"CLINICO": "propios"},
    "VENTAS":        {"VENTAS": "resumen"},
}
_PESO_NIVEL = {"resumen": 1, "propios": 2, "detalle": 3}

# Roles que ven además los eventos del sistema, los accesos y las sesiones (pestañas 2 a 4)
ROLES_AUDITORIA_COMPLETA = ("ADMINISTRADOR", "SUPERADMIN")
ROLES_PANTALLA_AUDITORIA = tuple(ALCANCE_CAMBIOS_POR_ROL)


def alcance_cambios(roles) -> dict[str, str]:
    """Módulos que pueden ver los roles de una sesión y con qué nivel; con varios roles gana el más amplio
    (detalle > propios > resumen)."""
    alcance: dict[str, str] = {}
    for rol in roles or []:
        for modulo, nivel in ALCANCE_CAMBIOS_POR_ROL.get((rol or "").strip().upper(), {}).items():
            if _PESO_NIVEL[nivel] > _PESO_NIVEL.get(alcance.get(modulo), 0):
                alcance[modulo] = nivel
    return alcance
