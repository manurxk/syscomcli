from flask import session


def build_sidebar():
    """Builds the sidebar structure based on current user's permissions.

    FASE 1 (2026-06-21): se reconstruye sub-fase por sub-fase a medida que
    cada modulo se registra en app/__init__.py
    (ver docs_reestructuracion/06_MAPEO_ENTIDADES_NUEVA_ESTRUCTURA.md).
    """
    roles = {(r or "").strip().upper() for r in session.get("roles", [])}
    items = []

    if roles & {"ADMINISTRADOR", "SUPERADMIN"}:
        items.append({
            "title": "Funcionarios",
            "endpoint": "funcionario.funcionarioIndex",
            "html_icon": '<i data-feather="briefcase"></i>'
        })

    if roles & {"ADMINISTRADOR", "SUPERADMIN", "RECEPCIONISTA"}:
        items.append({
            "title": "Pacientes",
            "endpoint": "paciente.pacienteIndex",
            "html_icon": '<i data-feather="users"></i>'
        })

    if roles & {"ADMINISTRADOR", "SUPERADMIN"}:
        items.append({
            "title": "Usuarios",
            "endpoint": "usuario.usuarioIndex",
            "html_icon": '<i data-feather="user-check"></i>'
        })

    config_items = []
    if roles & {"ADMINISTRADOR", "SUPERADMIN"}:
        config_items.append({
            "title": "Referenciales",
            "endpoint": "referenciales.referencialesIndex",
            "html_icon": '<i data-feather="sliders"></i>'
        })

    if not items and not config_items:
        return []

    groups = []
    if items:
        groups.append({"heading": "Personas", "items": items})
    if config_items:
        groups.append({"heading": "Configuración", "items": config_items})

    return [{
        "is_flat": True,
        "groups": groups
    }]
