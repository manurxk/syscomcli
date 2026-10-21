from datetime import datetime

from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.agendamiento.referenciales.dia_semana.DiaSemanaDao import DiaSemanaDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.utils.auditoria_constantes import AuditAccion
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_obligatorio

agendahorariosapi = Blueprint('agendahorariosapi', __name__)

DURACIONES_VALIDAS = (10, 15, 20, 30, 45, 60, 90)
MODALIDADES_VALIDAS = ('PRESENCIAL', 'TELEMEDICINA', 'DOMICILIO')
ROLES_GESTION_AGENDA = ("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")


def _soloAgendaPropia():
    """True si el usuario es CLINICO sin rol de gestión: solo puede ver su propia agenda."""
    roles = {(r or '').upper() for r in session.get('roles', [])}
    return not roles.intersection(ROLES_GESTION_AGENDA)


def _especialistaPropio():
    """id_especialista del usuario logueado (resuelto desde session['id_funcionario'])."""
    id_funcionario = session.get('id_funcionario')
    return CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None


def _calcularCuposTotales(hora_inicio, hora_fin, duracion_turno_min):
    """Calcula la cantidad de turnos del horario dividiendo la duración entre `duracion_turno_min` (mínimo 1)."""
    h1, m1 = (int(p) for p in hora_inicio.split(':')[:2])
    h2, m2 = (int(p) for p in hora_fin.split(':')[:2])
    minutos_totales = (h2 * 60 + m2) - (h1 * 60 + m1)
    return max(1, minutos_totales // duracion_turno_min)


def _validarDatos(data):
    """Valida los datos del horario de agenda; devuelve el mensaje de error o None si son válidos."""
    campos_obligatorios = ('id_especialista', 'id_sede', 'id_consultorio', 'id_dia_semana',
                            'hora_inicio', 'hora_fin', 'duracion_turno_min', 'fec_desde')
    for campo in campos_obligatorios:
        if not data.get(campo):
            return msg_obligatorio(campo)

    try:
        datetime.strptime(data['hora_inicio'], '%H:%M')
        datetime.strptime(data['hora_fin'], '%H:%M')
    except ValueError:
        return 'Las horas deben tener formato HH:MM.'

    if data['hora_inicio'] >= data['hora_fin']:
        return 'La hora de inicio debe ser menor que la hora de fin.'

    if int(data['duracion_turno_min']) not in DURACIONES_VALIDAS:
        return f'Duración de turno inválida. Valores permitidos: {DURACIONES_VALIDAS}.'

    modalidad = data.get('modalidad_default', 'PRESENCIAL')
    if modalidad not in MODALIDADES_VALIDAS:
        return f'Modalidad inválida. Valores permitidos: {MODALIDADES_VALIDAS}.'

    fec_hasta = data.get('fec_hasta')
    if fec_hasta and fec_hasta < data['fec_desde']:
        return 'La fecha hasta debe ser mayor o igual que la fecha desde.'

    try:
        porcentaje = int(data.get('porcentaje_overbooking') or 0)
    except (TypeError, ValueError):
        return 'El % de sobreturnos debe ser un número entre 0 y 100.'
    if not 0 <= porcentaje <= 100:
        return 'El % de sobreturnos debe ser un número entre 0 y 100.'

    return None


def _advertenciaHorarioClinica(id_dia_semana, hora_inicio, hora_fin):
    """Aviso (no bloquea) si la agenda queda fuera del horario de atención de la empresa. Sin horario cargado, nada."""
    tramos = EmpresaDao().getTramosHorario()
    if not tramos:
        return None
    del_dia = tramos.get(str(id_dia_semana), [])
    if not del_dia:
        return 'Ese día la clínica no atiende según su horario de atención (Referenciales → Empresa).'
    if not any(desde <= hora_inicio and hora_fin <= hasta for desde, hasta in del_dia):
        horario = ', '.join(f'{desde}-{hasta}' for desde, hasta in del_dia)
        return f'El horario {hora_inicio}-{hora_fin} queda fuera del horario de atención de la clínica ese día ({horario}).'
    return None


@agendahorariosapi.route('/especialistas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getEspecialistas():
    """GET: lista los especialistas."""
    try:
        data = FuncionarioDao().getEspecialistasActivos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/dias-semana', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getDiasSemana():
    """GET: lista los días de la semana."""
    try:
        data = DiaSemanaDao().getDiasSemana()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener días de la semana: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios', methods=['GET'])
@role_required(*ROLES_GESTION_AGENDA, "CLINICO")
def getAgendaHorarios():
    """GET: lista los horarios de agenda; admite filtro por especialista."""
    try:
        if _soloAgendaPropia():
            id_especialista = _especialistaPropio()
            if not id_especialista:
                return jsonify({'success': True, 'data': [], 'sin_especialista': True, 'error': None}), 200
        else:
            id_especialista = request.args.get('id_especialista', type=int)
        data = AgendaHorariosDao().getAgendaHorarios(id_especialista)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener agenda de horarios: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>', methods=['GET'])
@role_required(*ROLES_GESTION_AGENDA, "CLINICO")
def getAgendaHorario(id_agenda_horario):
    """GET: horario de agenda por su id; 404 si no existe."""
    try:
        agendadao = AgendaHorariosDao()
        agenda = agendadao.getAgendaHorarioById(id_agenda_horario)
        if not agenda or (_soloAgendaPropia() and agenda['id_especialista'] != _especialistaPropio()):
            return jsonify({'success': False, 'error': 'No se encontró el horario con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': agenda, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>/slots', methods=['GET'])
@role_required(*ROLES_GESTION_AGENDA, "CLINICO")
def getSlotsAgendaHorario(id_agenda_horario):
    """GET: turnos (slots) generados para el horario de agenda."""
    try:
        agendadao = AgendaHorariosDao()
        agenda = agendadao.getAgendaHorarioById(id_agenda_horario)
        if not agenda or (_soloAgendaPropia() and agenda['id_especialista'] != _especialistaPropio()):
            return jsonify({'success': False, 'error': 'No se encontró el horario con el ID proporcionado.'}), 404
        data = agendadao.getSlotsByAgendaHorario(id_agenda_horario)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener slots del horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def addAgendaHorario():
    """POST: valida y crea el horario de agenda."""
    data = request.get_json() or {}

    error = _validarDatos(data)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    agendadao = AgendaHorariosDao()
    if agendadao.validarConflictoHorario(
        data['id_especialista'], data['id_consultorio'], data['id_dia_semana'],
        data['hora_inicio'], data['hora_fin'], data['fec_desde'], data.get('fec_hasta')
    ):
        return jsonify({'success': False, 'error': 'Ya existe un horario que se superpone para ese especialista o consultorio en ese día.'}), 400

    try:
        datos = {
            'id_especialista': data['id_especialista'],
            'id_sede': data['id_sede'],
            'id_consultorio': data['id_consultorio'],
            'id_dia_semana': data['id_dia_semana'],
            'hora_inicio': data['hora_inicio'],
            'hora_fin': data['hora_fin'],
            'duracion_turno_min': int(data['duracion_turno_min']),
            'cupos_totales': _calcularCuposTotales(data['hora_inicio'], data['hora_fin'], int(data['duracion_turno_min'])),
            'modalidad_default': data.get('modalidad_default', 'PRESENCIAL'),
            'porcentaje_overbooking': int(data.get('porcentaje_overbooking') or 0),
            'fec_desde': data['fec_desde'],
            'fec_hasta': data.get('fec_hasta'),
        }
        id_agenda_horario = agendadao.crearAgendaHorario(datos, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_agenda_horario': id_agenda_horario},
                        'advertencia': _advertenciaHorarioClinica(data['id_dia_semana'], data['hora_inicio'], data['hora_fin']),
                        'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def updateAgendaHorario(id_agenda_horario):
    """PUT: valida y actualiza el horario de agenda; 404 si no existe."""
    data = request.get_json() or {}
    agendadao = AgendaHorariosDao()

    if not agendadao.getAgendaHorarioById(id_agenda_horario):
        return jsonify({'success': False, 'error': 'No se encontró el horario con el ID proporcionado.'}), 404

    error = _validarDatos(data)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    if agendadao.validarConflictoHorario(
        data['id_especialista'], data['id_consultorio'], data['id_dia_semana'],
        data['hora_inicio'], data['hora_fin'], data['fec_desde'], data.get('fec_hasta'),
        excluir_id=id_agenda_horario
    ):
        return jsonify({'success': False, 'error': 'Ya existe un horario que se superpone para ese especialista o consultorio en ese día.'}), 400

    try:
        datos = {
            'id_sede': data['id_sede'],
            'id_consultorio': data['id_consultorio'],
            'id_dia_semana': data['id_dia_semana'],
            'hora_inicio': data['hora_inicio'],
            'hora_fin': data['hora_fin'],
            'duracion_turno_min': int(data['duracion_turno_min']),
            'cupos_totales': _calcularCuposTotales(data['hora_inicio'], data['hora_fin'], int(data['duracion_turno_min'])),
            'modalidad_default': data.get('modalidad_default', 'PRESENCIAL'),
            'porcentaje_overbooking': int(data.get('porcentaje_overbooking') or 0),
            'fec_desde': data['fec_desde'],
            'fec_hasta': data.get('fec_hasta'),
        }
        agendadao.actualizarAgendaHorario(id_agenda_horario, datos, usuario_modificacion=session.get('id_usuario'))
        # Citas reservadas que quedaron fuera del horario nuevo: se listan para reprogramarlas
        return jsonify({'success': True, 'data': {'id_agenda_horario': id_agenda_horario},
                        'citas_afectadas': agendadao.getCitasFueraDeAgenda(id_agenda_horario),
                        'advertencia': _advertenciaHorarioClinica(data['id_dia_semana'], data['hora_inicio'], data['hora_fin']),
                        'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>/estado', methods=['PATCH'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def cambiarEstadoAgendaHorario(id_agenda_horario):
    """PATCH: activa o desactiva el horario de agenda."""
    data = request.get_json() or {}
    agendadao = AgendaHorariosDao()

    if not agendadao.getAgendaHorarioById(id_agenda_horario):
        return jsonify({'success': False, 'error': 'No se encontró el horario con el ID proporcionado.'}), 404

    estado = bool(data.get('est_agenda_horario', True))

    try:
        agendadao.cambiarEstadoAgendaHorario(id_agenda_horario, estado, usuario_modificacion=session.get('id_usuario'))
        accion = 'activado' if estado else 'desactivado'
        # Al desactivar, las citas que tenía siguen reservadas: se listan para reprogramarlas o cancelarlas
        citas = [] if estado else agendadao.getCitasFueraDeAgenda(id_agenda_horario, todas=True)
        return jsonify({'success': True, 'mensaje': f'Horario {accion} correctamente.', 'citas_afectadas': citas,
                        'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al cambiar estado del horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ---------------------------------------------------------------------------
# Bloqueos (ausencias, feriados) y sobreturnos — casos especiales de agenda (2026-10-19)
# ---------------------------------------------------------------------------

def _fecha_hora(valor):
    """'YYYY-MM-DDTHH:MM' (input datetime-local) o 'YYYY-MM-DD HH:MM' → datetime."""
    return datetime.strptime((valor or '').replace('T', ' ')[:16], '%Y-%m-%d %H:%M')


@agendahorariosapi.route('/agenda-horarios/bloqueos', methods=['GET'])
@role_required(*ROLES_GESTION_AGENDA)
def getBloqueosAgenda():
    """GET: lista los bloqueos de agenda; admite filtro por especialista."""
    try:
        data = AgendaHorariosDao().getBloqueos(request.args.get('id_especialista', None, type=int))
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener bloqueos de agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/bloqueos', methods=['POST'])
@role_required(*ROLES_GESTION_AGENDA)
def addBloqueoAgenda():
    """Bloquea un rango de un especialista en todas sus agendas. Devuelve las citas que caen en el rango."""
    data = request.get_json() or {}
    motivo = (data.get('motivo') or '').strip()
    try:
        desde, hasta = _fecha_hora(data.get('desde')), _fecha_hora(data.get('hasta'))
    except ValueError:
        return jsonify({'success': False, 'error': 'Indique la fecha y hora de inicio y de fin del bloqueo.'}), 400
    if not data.get('id_especialista'):
        return jsonify({'success': False, 'error': 'Seleccione el especialista.'}), 400
    if hasta <= desde:
        return jsonify({'success': False, 'error': 'El fin del bloqueo debe ser posterior al inicio.'}), 400
    if not motivo:
        return jsonify({'success': False, 'error': msg_obligatorio('Motivo del bloqueo')}), 400
    if hasta < datetime.now():
        return jsonify({'success': False, 'error': 'El bloqueo tiene que terminar en el futuro.'}), 400
    try:
        id_bloqueo, citas = AgendaHorariosDao().bloquearEspecialista(
            int(data['id_especialista']), desde, hasta, motivo[:200], session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_bloqueo': id_bloqueo}, 'citas_afectadas': citas, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al bloquear agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/bloqueos/<id_bloqueo>', methods=['DELETE'])
@role_required(*ROLES_GESTION_AGENDA)
def deleteBloqueoAgenda(id_bloqueo):
    """DELETE: levanta el bloqueo y libera los turnos; 404 si no existe."""
    try:
        if not AgendaHorariosDao().levantarBloqueo(id_bloqueo, session.get('id_usuario')):
            return jsonify({'success': False, 'error': 'No se encontró el bloqueo.'}), 404
        return jsonify({'success': True, 'mensaje': 'Bloqueo levantado: los turnos vuelven a estar disponibles.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al levantar bloqueo de agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>/sobreturnos', methods=['POST'])
@role_required(*ROLES_GESTION_AGENDA)
def addSobreturno(id_agenda_horario):
    """Crea un turno extra en la agenda (fecha y hora); después se reserva como cualquier turno en Citas."""
    data = request.get_json() or {}
    try:
        inicio = _fecha_hora(data.get('inicio'))
    except ValueError:
        return jsonify({'success': False, 'error': 'Indique la fecha y la hora del sobreturno.'}), 400
    try:
        id_slot = AgendaHorariosDao().crearSobreturno(id_agenda_horario, inicio, session.get('id_usuario'))
        # slots_agenda no está auditada (la genera el sistema): el sobreturno queda como evento
        AuditoriaDao().registrar_evento(
            session.get('id_usuario'), AuditAccion.RECORD_CREATE,
            f"Sobreturno #{id_slot} en la agenda {id_agenda_horario}: {inicio:%d/%m/%Y %H:%M}", request.remote_addr)
        return jsonify({'success': True, 'data': {'id_slot_agenda': id_slot}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al crear sobreturno: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
