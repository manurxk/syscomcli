"""El Superadministrador es una cuenta de soporte: el resto del personal no lo ve en las listas, pero sus acciones quedan
registradas en la auditoría, con la etiqueta «Soporte técnico» para quien no es Superadministrador."""
from flask import session
from app.core.base_dao import BaseDAO

ETIQUETA_SOPORTE = 'Soporte técnico'
_dao = BaseDAO(db_name_env="DB_NAME_NUEVA")


def es_superadmin_sesion():
    """Indica si el usuario en sesión tiene el rol SUPERADMIN."""
    return 'SUPERADMIN' in {(r or "").strip().upper() for r in session.get("roles", [])}


def ids_superadmin():
    """Ids de los usuarios con el rol SUPERADMIN activo."""
    filas = _dao.execute_query(
        "SELECT DISTINCT ur.id_usuario FROM usuarios_roles ur JOIN roles r ON r.id_rol = ur.id_rol "
        "WHERE r.cod_rol = 'SUPERADMIN' AND ur.est_usuario_rol = TRUE")
    return {f['id_usuario'] for f in filas}


def es_usuario_soporte(id_usuario):
    """True si ese usuario es Superadministrador (se usa para negar el acceso a quien no lo es)."""
    return id_usuario in ids_superadmin()


def ocultar_soporte(filas, campo_id='id_usuario'):
    """Quita de la lista las filas del Superadministrador, salvo que quien consulta también lo sea."""
    if es_superadmin_sesion():
        return filas
    soporte = ids_superadmin()
    return [f for f in filas if f.get(campo_id) not in soporte]


def etiquetar_soporte(filas, campo_id='id_usuario', campos_nombre=('usu_nick', 'usuario_intentado', 'usu_nombre')):
    """En la auditoría, las acciones del Superadministrador figuran como «Soporte técnico» (no se ocultan)."""
    if es_superadmin_sesion() or not filas:
        return filas
    soporte = ids_superadmin()
    for f in filas:
        if f.get(campo_id) in soporte:
            for campo in campos_nombre:
                if campo in f:
                    f[campo] = ETIQUETA_SOPORTE
            if 'roles' in f:
                f['roles'] = 'SOPORTE'
    return filas
