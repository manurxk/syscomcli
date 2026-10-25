"""Alcance de la pantalla única de Reportes (PDF 4, paso 3).

Lo fija el servidor según los roles de la sesión; nunca un parámetro del navegador:
- qué pestañas puede abrir cada rol,
- de qué pestañas ve a todos los especialistas y de cuáles solo lo propio (el Clínico),
- el id_especialista con el que se filtran las consultas de ReporteDao.

Mismo criterio que alcance_cambios() de la Auditoría: con varios roles gana el más amplio.
"""
from flask import session

PESTANAS = ('resumen', 'agendamiento', 'consultorio', 'ventas')

# Pestañas que abre cada rol
PESTANAS_POR_ROL = {
    'ADMINISTRADOR': ('resumen', 'agendamiento', 'consultorio', 'ventas'),
    'SUPERADMIN': ('resumen',),      # soporte: solo el resumen, sin datos de pacientes ni de ventas
    'RECEPCION': ('agendamiento',),
    'VENTAS': ('ventas',),
    'CLINICO': ('agendamiento', 'consultorio'),
}

# Roles que ven a todos los especialistas en cada pestaña; los demás roles con acceso ven solo lo propio
ROLES_VEN_TODOS = {
    'resumen': ('ADMINISTRADOR', 'SUPERADMIN'),
    'agendamiento': ('ADMINISTRADOR', 'RECEPCION'),
    'consultorio': ('ADMINISTRADOR',),
    'ventas': ('ADMINISTRADOR', 'VENTAS'),
}

ROLES_PANTALLA_REPORTES = tuple(PESTANAS_POR_ROL)

# id_especialista que no existe: con el filtro de ReporteDao no devuelve ninguna fila. Se usa cuando un
# Clínico no tiene registro de especialista, porque None significaría «todos» y le mostraría toda la clínica.
SIN_ESPECIALISTA = -1


def _roles(roles):
    return {(r or '').strip().upper() for r in roles or []}


def pestanas_permitidas(roles):
    """Pestañas que abre la sesión, en el orden de la pantalla (con varios roles, la unión)."""
    permitidas = set()
    for rol in _roles(roles):
        permitidas.update(PESTANAS_POR_ROL.get(rol, ()))
    return [p for p in PESTANAS if p in permitidas]


def alcance_reportes(roles, pestana, id_funcionario=None, especialista_param=None):
    """Alcance de una pestaña para los roles dados.

    Devuelve un dict:
      permitida        la sesión puede abrir la pestaña
      propio           ve solo lo suyo (Clínico)
      puede_filtrar    puede elegir un especialista (Administrador y Recepción)
      sin_especialista es Clínico pero su usuario no está registrado como especialista
      id_especialista  el valor para ReporteDao: None = todos, un id = ese especialista
    `especialista_param` es el filtro opcional del navegador: solo se usa si puede_filtrar.
    """
    from app.dao.agendamiento.cita.CitaDao import CitaDao

    roles = _roles(roles)
    alcance = {'pestana': pestana, 'permitida': False, 'propio': False, 'puede_filtrar': False,
               'sin_especialista': False, 'id_especialista': None}
    if pestana not in pestanas_permitidas(roles):
        return alcance
    alcance['permitida'] = True
    if roles & set(ROLES_VEN_TODOS[pestana]):
        # Solo las pestañas por especialista aceptan el filtro; Resumen y Ventas no tienen especialista
        if pestana in ('agendamiento', 'consultorio'):
            alcance['puede_filtrar'] = True
            try:
                alcance['id_especialista'] = int(especialista_param) if especialista_param else None
            except (TypeError, ValueError):
                alcance['id_especialista'] = None
        return alcance
    # Solo ve lo propio: el id sale de la sesión
    alcance['propio'] = True
    id_especialista = CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None
    if id_especialista:
        alcance['id_especialista'] = id_especialista
    else:
        alcance['sin_especialista'] = True
        alcance['id_especialista'] = SIN_ESPECIALISTA
    return alcance


def alcance_de_sesion(pestana, especialista_param=None):
    """alcance_reportes() con los roles y el funcionario de la sesión actual."""
    return alcance_reportes(session.get('roles', []), pestana,
                            id_funcionario=session.get('id_funcionario'),
                            especialista_param=especialista_param)
