"""Quién puede abrir la ficha clínica de un paciente, y el registro de cada apertura en la auditoría.

Regla (2026-10-25): el Administrador abre cualquier ficha; un clínico abre la ficha de los pacientes con los que tiene
vínculo (cita o consulta con él, o una derivación del paciente que él aceptó). Cada apertura, descarga en PDF e intento
rechazado queda en la auditoría con quién, cuándo y de qué paciente."""
from flask import current_app, request, session

from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion

MENSAJE_SIN_ACCESO = ('No tenés acceso a la ficha de este paciente: solo se abre la de los pacientes con los que tenés citas, '
                      'consultas o una derivación aceptada.')


def _roles():
    return {(r or '').upper() for r in session.get('roles', [])}


def id_especialista_de_sesion():
    """id_especialista del usuario logueado, o None si no es especialista."""
    id_funcionario = session.get('id_funcionario')
    return CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None


def es_administrador():
    return 'ADMINISTRADOR' in _roles()


def puede_ver_ficha(id_paciente):
    """True si el usuario de la sesión puede abrir la ficha de ese paciente."""
    if es_administrador():
        return True
    yo = id_especialista_de_sesion()
    return bool(yo) and FichaDao().tieneVinculo(yo, id_paciente)


def registrar(id_paciente, que, accion=AuditAccion.REPORT_VIEW):
    """Deja en la auditoría quién hizo qué con la ficha de ese paciente: `que` es la frase que antecede al paciente
    («Abrió la ficha clínica de», «Descargó el PDF de la ficha clínica de»…). Un fallo al registrar no impide mostrar la ficha."""
    try:
        etiqueta = FichaDao().getEtiquetaPaciente(id_paciente) or f'paciente {id_paciente}'
        AuditoriaDao().registrar_evento(
            id_usuario=session.get('id_usuario'), accion=accion,
            detalle=f'{que} {etiqueta}', ip_origen=request.remote_addr)
    except Exception as e:
        current_app.logger.warning(f'No se pudo registrar en la auditoría el acceso a la ficha {id_paciente}: {e}')
