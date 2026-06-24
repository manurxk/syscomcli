from datetime import datetime

from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao
from app.dao.agendamiento.referenciales.dia_semana.DiaSemanaDao import DiaSemanaDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.auth.utils.decorators import role_required

agendahorariosapi = Blueprint('agendahorariosapi', __name__)

DURACIONES_VALIDAS = (10, 15, 20, 30, 45, 60, 90)
MODALIDADES_VALIDAS = ('PRESENCIAL', 'TELEMEDICINA', 'DOMICILIO')


def _calcularCuposTotales(hora_inicio, hora_fin, duracion_turno_min):
    h1, m1 = (int(p) for p in hora_inicio.split(':')[:2])
    h2, m2 = (int(p) for p in hora_fin.split(':')[:2])
    minutos_totales = (h2 * 60 + m2) - (h1 * 60 + m1)
    return max(1, minutos_totales // duracion_turno_min)


def _validarDatos(data):
    campos_obligatorios = ('id_especialista', 'id_sede', 'id_consultorio', 'id_dia_semana',
                            'hora_inicio', 'hora_fin', 'duracion_turno_min', 'fec_desde')
    for campo in campos_obligatorios:
        if not data.get(campo):
            return f'El campo "{campo}" es obligatorio.'

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

    return None


@agendahorariosapi.route('/especialistas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getEspecialistas():
    try:
        data = FuncionarioDao().getEspecialistasActivos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/dias-semana', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getDiasSemana():
    try:
        data = DiaSemanaDao().getDiasSemana()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener días de la semana: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getAgendaHorarios():
    try:
        id_especialista = request.args.get('id_especialista', type=int)
        data = AgendaHorariosDao().getAgendaHorarios(id_especialista)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener agenda de horarios: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getAgendaHorario(id_agenda_horario):
    try:
        agendadao = AgendaHorariosDao()
        agenda = agendadao.getAgendaHorarioById(id_agenda_horario)
        if not agenda:
            return jsonify({'success': False, 'error': 'No se encontró el horario con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': agenda, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>/slots', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getSlotsAgendaHorario(id_agenda_horario):
    try:
        agendadao = AgendaHorariosDao()
        if not agendadao.getAgendaHorarioById(id_agenda_horario):
            return jsonify({'success': False, 'error': 'No se encontró el horario con el ID proporcionado.'}), 404
        data = agendadao.getSlotsByAgendaHorario(id_agenda_horario)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener slots del horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addAgendaHorario():
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
            'fec_desde': data['fec_desde'],
            'fec_hasta': data.get('fec_hasta'),
        }
        id_agenda_horario = agendadao.crearAgendaHorario(datos, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_agenda_horario': id_agenda_horario}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateAgendaHorario(id_agenda_horario):
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
            'fec_desde': data['fec_desde'],
            'fec_hasta': data.get('fec_hasta'),
        }
        agendadao.actualizarAgendaHorario(id_agenda_horario, datos, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_agenda_horario': id_agenda_horario}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendahorariosapi.route('/agenda-horarios/<int:id_agenda_horario>/estado', methods=['PATCH'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def cambiarEstadoAgendaHorario(id_agenda_horario):
    data = request.get_json() or {}
    agendadao = AgendaHorariosDao()

    if not agendadao.getAgendaHorarioById(id_agenda_horario):
        return jsonify({'success': False, 'error': 'No se encontró el horario con el ID proporcionado.'}), 404

    estado = bool(data.get('est_agenda_horario', True))

    try:
        agendadao.cambiarEstadoAgendaHorario(id_agenda_horario, estado, usuario_modificacion=session.get('id_usuario'))
        accion = 'activado' if estado else 'desactivado'
        return jsonify({'success': True, 'mensaje': f'Horario {accion} correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al cambiar estado del horario: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
