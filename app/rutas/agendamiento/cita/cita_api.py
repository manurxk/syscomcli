from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.auth.utils.decorators import role_required
from app.services.UltraMsgService import UltraMsgService

citaapi = Blueprint('citaapi', __name__)

ROLES_CITAS = ("ADMINISTRADOR", "SUPERADMIN", "RECEPCIONISTA")

ESTADOS_VALIDOS = ('AGENDADA', 'CONFIRMADA', 'EN_CONSULTA', 'COMPLETADA', 'AUSENTE', 'CANCELADA')


@citaapi.route('/citas/especialistas', methods=['GET'])
@role_required(*ROLES_CITAS)
def getEspecialistasParaCitas():
    try:
        data = FuncionarioDao().getEspecialistasActivos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/slots-disponibles', methods=['GET'])
@role_required(*ROLES_CITAS)
def getSlotsDisponibles():
    try:
        id_especialista = request.args.get('id_especialista', type=int)
        id_especialidad = request.args.get('id_especialidad', type=int)
        desde = request.args.get('desde')
        hasta = request.args.get('hasta')
        data = CitaDao().getSlotsDisponibles(id_especialista, id_especialidad, desde, hasta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener slots disponibles: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas', methods=['GET'])
@role_required(*ROLES_CITAS)
def getCitas():
    try:
        id_especialista = request.args.get('id_especialista', type=int)
        id_paciente = request.args.get('id_paciente', type=int)
        desde = request.args.get('desde')
        hasta = request.args.get('hasta')
        data = CitaDao().getCitas(id_especialista, id_paciente, desde, hasta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener citas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>', methods=['GET'])
@role_required(*ROLES_CITAS)
def getCita(id_cita):
    try:
        cita = CitaDao().getCitaById(id_cita)
        if not cita:
            return jsonify({'success': False, 'error': 'No se encontró la cita con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': cita, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas', methods=['POST'])
@role_required(*ROLES_CITAS)
def addCita():
    data = request.get_json() or {}

    if not data.get('id_paciente'):
        return jsonify({'success': False, 'error': 'El campo "id_paciente" es obligatorio.'}), 400
    if not data.get('id_slot_agenda'):
        return jsonify({'success': False, 'error': 'El campo "id_slot_agenda" es obligatorio.'}), 400

    try:
        datos = {
            'id_paciente': data['id_paciente'],
            'id_slot_agenda': data['id_slot_agenda'],
            'id_especialidad': data.get('id_especialidad'),
            'modalidad': data.get('modalidad', 'PRESENCIAL'),
            'cita_es_primera_vez': data.get('cita_es_primera_vez', True),
            'cita_numero_sesion': data.get('cita_numero_sesion'),
            'motivo': data.get('motivo'),
            'observaciones': data.get('observaciones'),
        }
        id_cita = CitaDao().crearCita(datos, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_cita': id_cita}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>', methods=['PUT'])
@role_required(*ROLES_CITAS)
def updateCita(id_cita):
    """Edita una cita (paciente y especialista quedan fijos). Si se envía un
    id_slot_agenda distinto al actual, reprograma: libera el slot viejo y reserva
    el nuevo (CitaDao.actualizarCita)."""
    data = request.get_json() or {}

    if not data.get('id_slot_agenda'):
        return jsonify({'success': False, 'error': 'El campo "id_slot_agenda" es obligatorio.'}), 400
    if not data.get('motivo'):
        return jsonify({'success': False, 'error': 'El campo "motivo" es obligatorio.'}), 400

    try:
        datos = {
            'id_slot_agenda': data['id_slot_agenda'],
            'id_especialidad': data.get('id_especialidad'),
            'modalidad': data.get('modalidad', 'PRESENCIAL'),
            'cita_es_primera_vez': data.get('cita_es_primera_vez', True),
            'cita_numero_sesion': data.get('cita_numero_sesion'),
            'motivo': data.get('motivo'),
            'observaciones': data.get('observaciones'),
        }
        CitaDao().actualizarCita(id_cita, datos, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': 'Cita actualizada correctamente.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al actualizar cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>/logs', methods=['GET'])
@role_required(*ROLES_CITAS)
def getLogsCita(id_cita):
    try:
        data = CitaDao().getLogEstados(id_cita)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener historial de la cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>/recordatorios', methods=['GET'])
@role_required(*ROLES_CITAS)
def getRecordatoriosCita(id_cita):
    try:
        data = RecordatorioDao().getRecordatoriosByCita(id_cita)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recordatorios de la cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>/recordatorios/<int:id_recordatorio>/reenviar', methods=['POST'])
@role_required(*ROLES_CITAS)
def reenviarRecordatorio(id_cita, id_recordatorio):
    """Fuerza el envío inmediato de un recordatorio, fuera de la ventana automática
    del job (procesar_recordatorios_pendientes). Útil para reenviar a pedido del staff
    o para probar la integración con UltraMsg sin esperar la ventana de 24h/2h."""
    recordatorio_dao = RecordatorioDao()
    detalle = recordatorio_dao.getRecordatorioConDetalle(id_recordatorio)

    if not detalle or detalle['id_cita'] != id_cita:
        return jsonify({'success': False, 'error': 'No se encontró el recordatorio indicado.'}), 404
    if not detalle['paciente_telefono']:
        return jsonify({'success': False, 'error': 'El paciente no tiene teléfono registrado.'}), 400

    try:
        ultramsg_service = UltraMsgService()
        if not ultramsg_service.client_available:
            return jsonify({'success': False, 'error': 'UltraMsg no está configurado en el servidor.'}), 503

        success, _message_id, error, _tipo_error = ultramsg_service.enviar_recordatorio_cita(
            telefono=detalle['paciente_telefono'],
            nombre_paciente=detalle['paciente_nombre'],
            cita_fecha=detalle['cita_fecha'],
            cita_hora=detalle['cita_hora'],
            especialista=detalle['especialista_nombre'],
            especialidad=detalle['des_especialidad'] or 'Consulta',
            motivo=detalle['cita_motivo'],
        )

        if not success:
            return jsonify({'success': False, 'error': error or 'No se pudo enviar el mensaje.'}), 502

        recordatorio_dao.marcarEnviado(id_recordatorio)
        return jsonify({'success': True, 'mensaje': 'Recordatorio reenviado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al reenviar recordatorio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>/estado', methods=['PATCH'])
@role_required(*ROLES_CITAS)
def cambiarEstadoCita(id_cita):
    data = request.get_json() or {}
    cod_estado_nuevo = data.get('cod_estado_nuevo')

    if cod_estado_nuevo not in ESTADOS_VALIDOS:
        return jsonify({'success': False, 'error': f'Estado inválido. Valores permitidos: {ESTADOS_VALIDOS}.'}), 400

    try:
        CitaDao().cambiarEstadoCita(
            id_cita, cod_estado_nuevo,
            usuario_modificacion=session.get('id_usuario'),
            motivo=data.get('motivo'),
        )
        return jsonify({'success': True, 'mensaje': 'Estado de la cita actualizado correctamente.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al cambiar estado de cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
