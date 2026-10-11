import logging

from flask import session, url_for
from werkzeug.routing import BuildError

from app.dao.mantenimiento.seguridad.menu.MenuDao import MenuDao

logger = logging.getLogger(__name__)

# Ícono (Feather) por grupo_menu, mostrado en el encabezado del submenú colapsable.
ICONOS_GRUPO = {
    "Personas": "users",
    "Agendamiento": "calendar",
    "Clinico": "activity",
    "Ventas": "shopping-cart",
    "Configuracion": "settings",
    "Reportes": "bar-chart-2",
}
ICONO_GRUPO_DEFECTO = "folder"


def _resolver_url(fila):
    """Resuelve el endpoint de una página a una URL concreta.

    Si la página cambió de nombre o se eliminó del código (endpoint ya no
    registrado en Flask), url_for() explota con BuildError. Como el sidebar
    se arma en un context processor global, dejar que ese error se propague
    tumba la carga de TODO el sistema para ese rol, no solo ese ítem.
    """
    try:
        return url_for(fila["endpoint"])
    except BuildError:
        logger.warning(
            "Sidebar: endpoint '%s' de la página '%s' (id_pagina=%s) ya no existe. "
            "Se omite el ítem del menú.",
            fila["endpoint"], fila["title"], fila["id_pagina"]
        )
        return None


def build_sidebar():
    """Construye el sidebar a partir del menú dinámico (tablas paginas/roles_paginas).

    Cada grupo_menu (Personas/Agendamiento/Clinico/Ventas/Configuracion/Reportes)
    se agrupa en un submenú colapsable, en vez de listar todas las páginas sueltas.
    La visibilidad de cada página se sigue administrando desde Mantener Menu.
    """
    roles = [(r or "").strip().upper() for r in session.get("roles", [])]
    if not roles:
        return []

    filas = MenuDao().getMenuParaRoles(roles)
    if not filas:
        return []

    links_por_grupo = {}
    orden_grupos = []
    for fila in filas:
        url = _resolver_url(fila)
        if url is None:
            continue
        heading = fila["grupo_menu"] or "General"
        if heading not in links_por_grupo:
            links_por_grupo[heading] = []
            orden_grupos.append(heading)
        links_por_grupo[heading].append({
            "title": fila["title"],
            "url": url,
            "html_icon": f'<i data-feather="{fila["icono"]}"></i>' if fila["icono"] else ""
        })

    menus = [{
        "title": heading,
        "icon": ICONOS_GRUPO.get(heading, ICONO_GRUPO_DEFECTO),
        "links": links_por_grupo[heading]
    } for heading in orden_grupos]

    return [{
        "is_flat": False,
        "heading": "Menú principal",
        "menus": menus
    }]
