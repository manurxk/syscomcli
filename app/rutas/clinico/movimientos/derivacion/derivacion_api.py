from datetime import date, timedelta

from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.clinico.movimientos.derivacion.DerivacionDao import DerivacionDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_obligatorio

derivacionapi = Blueprint('derivacionapi', __name__)

ROLES_DERIVACION = ("ADMINISTRADOR", "CLINICO")


def _especialistaPropio():
    """id_especialista del usuario logueado (resuelto desde session['id_funcionario'])."""
    id_funcionario = session.get('id_funcionario')
    return CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None


@derivacionapi.route('/consultas/<int:id_consulta>/derivaciones', methods=['GET'])
@role_required(*ROLES_DERIVACION)
def getDerivaciones(id_consulta):
    """GET: lista los derivaciones de la consulta."""
    try:
        data = DerivacionDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener derivaciones de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/especialistas', methods=['GET'])
@role_required(*ROLES_DERIVACION)
def getEspecialistasDeEspecialidad():
    """GET: especialistas activos que atienden la especialidad (?id_especialidad=), para elegir a quién derivar."""
    id_especialidad = request.args.get('id_especialidad', type=int)
    if not id_especialidad:
        return jsonify({'success': False, 'error': msg_obligatorio('Especialidad de destino')}), 400
    try:
        data = DerivacionDao().getEspecialistasDeEspecialidad(id_especialidad)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas de la especialidad: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/consultas/<int:id_consulta>/derivaciones', methods=['POST'])
@role_required(*ROLES_DERIVACION)
def addDerivacion(id_consulta):
    """POST: valida y registra derivación en la consulta (201). Queda Pendiente hasta que el especialista
    de destino la acepte o la rechace desde Mi Agenda. `id_especialista_destino` es opcional."""
    data = request.get_json() or {}
    if not data.get('id_especialidad_destino'):
        return jsonify({'success': False, 'error': msg_obligatorio('Especialidad de destino')}), 400
    if not (data.get('motivo_derivacion') or '').strip():
        return jsonify({'success': False, 'error': msg_obligatorio('Motivo de derivación')}), 400

    try:
        dao = DerivacionDao()
        id_destino = data.get('id_especialista_destino') or None
        if id_destino:
            if not dao.atiendeEspecialidad(id_destino, data['id_especialidad_destino']):
                return jsonify({'success': False, 'error': 'El especialista elegido no atiende esa especialidad.'}), 400
            if id_destino == dao.getEspecialistaDeConsulta(id_consulta):
                return jsonify({'success': False, 'error': 'No se puede derivar a uno mismo.'}), 400
        nuevo_id = dao.guardar(id_consulta, {**data, 'id_especialista_destino': id_destino}, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_derivacion': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar derivación de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>', methods=['DELETE'])
@role_required(*ROLES_DERIVACION)
def deleteDerivacion(id_derivacion):
    """DELETE: baja lógica de derivación mientras siga Pendiente; 404 si no existe."""
    try:
        dao = DerivacionDao()
        actual = dao.getById(id_derivacion)
        if actual and actual['estado_derivacion'] != 'PENDIENTE':
            return jsonify({'success': False, 'error': 'La derivación ya fue respondida: no se puede eliminar.'}), 400
        if dao.desactivar(id_derivacion, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Derivación eliminada correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró la derivación con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar derivación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ----------------------------------------------------------------------
# Mi Agenda: derivaciones recibidas (aceptar / rechazar), aceptadas por agendar y respuestas a las propias
# ----------------------------------------------------------------------

@derivacionapi.route('/mi-agenda/derivaciones', methods=['GET'])
@role_required("CLINICO")
def getMisDerivaciones():
    """GET: lo que muestra la tarjeta «Derivaciones» de Mi Agenda del especialista logueado."""
    try:
        yo = _especialistaPropio()
        if not yo:
            return jsonify({'success': True, 'data': {'recibidas': [], 'sin_cita': [], 'respondidas': []}, 'error': None}), 200
        dao = DerivacionDao()
        data = {'recibidas': dao.getRecibidas(yo), 'sin_cita': dao.getAceptadasSinCita(yo),
                'respondidas': dao.getRespondidasDeMisConsultas(yo)}
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener las derivaciones de Mi Agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


def _responder(id_derivacion, aceptar):
    """Acepta o rechaza (el rechazo exige motivo). Devuelve la respuesta JSON."""
    motivo = ((request.get_json(silent=True) or {}).get('motivo') or '').strip()
    if not aceptar and not motivo:
        return jsonify({'success': False, 'error': msg_obligatorio('Motivo del rechazo')}), 400
    try:
        yo = _especialistaPropio()
        if not yo:
            return jsonify({'success': False, 'error': 'Tu usuario no tiene un perfil de especialista vinculado.'}), 400
        DerivacionDao().responder(id_derivacion, yo, session.get('id_usuario'), aceptar, motivo)
        return jsonify({'success': True, 'mensaje': 'Derivación aceptada.' if aceptar else 'Derivación rechazada.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al responder la derivación: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>/aceptar', methods=['POST'])
@role_required("CLINICO")
def aceptarDerivacion(id_derivacion):
    """POST: acepta la derivación pendiente (queda asignada al especialista que la acepta)."""
    return _responder(id_derivacion, True)


@derivacionapi.route('/derivaciones/<int:id_derivacion>/rechazar', methods=['POST'])
@role_required("CLINICO")
def rechazarDerivacion(id_derivacion):
    """POST: rechaza la derivación pendiente; `motivo` es obligatorio y lo ve quien derivó."""
    return _responder(id_derivacion, False)


# ----------------------------------------------------------------------
# Cita del paciente derivado: el que aceptó elige un turno libre de su agenda (cita de Primera vez con él)
# ----------------------------------------------------------------------

def _derivacionAceptadaPorMi(id_derivacion):
    """(derivación, error): aceptada por el especialista logueado."""
    yo = _especialistaPropio()
    d = DerivacionDao().getById(id_derivacion)
    if not d or not yo or d['id_especialista_destino'] != yo or d['estado_derivacion'] != 'ACEPTADA':
        return None, ('No se encontró la derivación aceptada.', 404)
    return d, None


@derivacionapi.route('/derivaciones/<int:id_derivacion>/cita/turnos', methods=['GET'])
@role_required("CLINICO")
def getTurnosCitaDerivacion(id_derivacion):
    """GET: turnos libres del especialista que aceptó, de hoy hasta donde hay turnos generados."""
    try:
        d, error = _derivacionAceptadaPorMi(id_derivacion)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        hoy = date.today()
        hasta = hoy + timedelta(days=AgendaHorariosDao.HORIZONTE_DIAS_DEFAULT)
        turnos = CitaDao().getSlotsDisponibles(d['id_especialista_destino'], None, hoy.isoformat(), hasta.isoformat())
        return jsonify({'success': True, 'data': turnos, 'id_especialista': d['id_especialista_destino'], 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener los turnos de la derivación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>/cita', methods=['POST'])
@role_required("CLINICO")
def addCitaDerivacion(id_derivacion):
    """POST: crea la cita de Primera vez del paciente derivado (201) en un turno libre propio. Recibe id_slot_agenda y motivo."""
    data = request.get_json() or {}
    id_slot = data.get('id_slot_agenda')
    if not isinstance(id_slot, int):
        return jsonify({'success': False, 'error': msg_obligatorio('Turno')}), 400
    try:
        d, error = _derivacionAceptadaPorMi(id_derivacion)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        from app.dao.clinico.movimientos.tratamiento.TratamientoDao import TratamientoDao
        if TratamientoDao().getEspecialistaDeSlots([id_slot]).get(id_slot) != d['id_especialista_destino']:
            return jsonify({'success': False, 'error': 'El turno debe ser de tu propia agenda.'}), 400
        id_cita = CitaDao().crearCita({
            'id_paciente': d['id_paciente'], 'id_slot_agenda': id_slot, 'modalidad': 'PRESENCIAL',
            'tipo_cita': 'PRIMERA_VEZ', 'cita_es_primera_vez': True,
            'motivo': (data.get('motivo') or '').strip() or 'Derivación',
        }, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_cita': id_cita}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al agendar la cita de la derivación: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
