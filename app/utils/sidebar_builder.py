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
            "endpoint": "funcionario.funcionarioIndex"
        })

    if not items:
        return []

    return [{
        "is_flat": True,
        "groups": [{
            "heading": "Mantenimiento",
            "items": items
        }]
    }]
