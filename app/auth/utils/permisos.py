"""Permisos por acción (LEER/CREAR/EDITAR/ELIMINAR) de cada rol sobre cada módulo, según la matriz «Permisos»."""

from flask import session

from app.dao.mantenimiento.referenciales.permisos.PermisoDao import PermisoDao

# Estos roles pasan siempre: la matriz no los limita.
ROLES_SIEMPRE_PERMITIDOS = {"ADMINISTRADOR", "SUPERADMIN"}


def tiene_permiso_accion(modulo, accion):
    """True si algún rol del usuario tiene `accion` sobre `modulo` (ej.: tiene_permiso_accion('VENTAS', 'CREAR'))."""
    roles = {(r or "").strip().upper() for r in session.get("roles", [])}
    if not roles:
        return False
    if roles & ROLES_SIEMPRE_PERMITIDOS:
        return True
    try:
        permisos = PermisoDao().getPermisosParaRoles(sorted(roles))
    except Exception:
        return False  # ante un error de base, se niega (no se muestra ni se permite)
    return (modulo.strip().upper(), accion.strip().upper()) in permisos
