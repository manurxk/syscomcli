from flask import session

from app.dao.mantenimiento.seguridad.menu.MenuDao import MenuDao


def build_sidebar():
    """Construye el sidebar a partir del menú dinámico (tablas paginas/roles_paginas).

    Reemplaza el hardcode por rol que existía antes (ver m17_menu_dinamico.sql):
    ahora la visibilidad de cada página se administra desde Mantener Menu.
    """
    roles = [(r or "").strip().upper() for r in session.get("roles", [])]
    if not roles:
        return []

    filas = MenuDao().getMenuParaRoles(roles)
    if not filas:
        return []

    groups_por_nombre = {}
    orden_grupos = []
    for fila in filas:
        heading = fila["grupo_menu"] or "General"
        if heading not in groups_por_nombre:
            groups_por_nombre[heading] = []
            orden_grupos.append(heading)
        groups_por_nombre[heading].append({
            "title": fila["title"],
            "endpoint": fila["endpoint"],
            "html_icon": f'<i data-feather="{fila["icono"]}"></i>' if fila["icono"] else ""
        })

    groups = [{"heading": heading, "items": groups_por_nombre[heading]} for heading in orden_grupos]

    return [{
        "is_flat": True,
        "groups": groups
    }]
