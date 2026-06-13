"""
auditoria_constantes.py
=======================
Módulo de constantes para el sistema de auditoría del sistema Angasys.

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
