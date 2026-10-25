from datetime import datetime

from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.auth.utils.decorators import role_required
from app.services.UltraMsgService import UltraMsgService
from app.auth.services.auth_service import AuthService
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion
from app.utils.mensajes_validacion import msg_obligatorio

citaapi = Blueprint('citaapi', __name__)

ROLES_CITAS = ("ADMINISTRADOR", "RECEPCION")
TIPOS_CITA = ("PRIMERA_VEZ", "SEGUIMIENTO", "TRATAMIENTO")


def _campos_tipo_cita(data):
    """tipo_cita y cita_es_primera_vez de una cita. El tipo manda: cita_es_primera_vez siempre es
    (tipo == PRIMERA_VEZ). Si el cliente solo manda cita_es_primera_vez (formato anterior), se deriva el tipo de ahí."""
    tipo = data.get('tipo_cita')
    if not tipo:
        tipo = 'PRIMERA_VEZ' if data.get('cita_es_primera_vez', True) else 'SEGUIMIENTO'
    if tipo not in TIPOS_CITA:
        raise ValueError('El tipo de cita debe ser Primera vez, Seguimiento o Tratamiento.')
    return {'tipo_cita': tipo, 'cita_es_primera_vez': tipo == 'PRIMERA_VEZ'}


def _validar_primera_cita(id_paciente, tipo_cita, excluir_id_cita=None):
    """Un paciente sin citas anteriores (válidas) solo puede agendar una cita de Primera vez."""
    if tipo_cita != 'PRIMERA_VEZ' and CitaDao().contarCitasPrevias(id_paciente, excluir_id_cita) == 0:
        raise ValueError('El paciente no tiene citas anteriores: su primera cita debe ser de Primera vez.')

ESTADOS_VALIDOS = ('AGENDADA', 'CONFIRMADA', 'EN_CONSULTA', 'COMPLETADA', 'AUSENTE', 'CANCELADA')


@citaapi.route('/citas/numero-sesion', methods=['GET'])
@role_required(*ROLES_CITAS)
def getNumeroSesion():
    """GET: número de sesión que le corresponde a una cita de Seguimiento o Tratamiento del paciente.
    `inicio` (AAAA-MM-DD HH:MM) cuenta solo las citas anteriores a esa fecha; sin ella, es el de la próxima cita.
    `excluir_id_cita` deja afuera la cita que se está editando."""
    id_paciente = request.args.get('id_paciente', type=int)
    tipo_cita = request.args.get('tipo_cita', '')
    if not id_paciente:
        return jsonify({'success': False, 'error': msg_obligatorio('id_paciente')}), 400
    if tipo_cita not in TIPOS_CITA:
        return jsonify({'success': False, 'error': 'El tipo de cita debe ser Primera vez, Seguimiento o Tratamiento.'}), 400
    inicio = request.args.get('inicio') or None
    if inicio:
        try:
            datetime.strptime(inicio, '%Y-%m-%d %H:%M')
        except ValueError:
            return jsonify({'success': False, 'error': 'La fecha de inicio debe tener el formato AAAA-MM-DD HH:MM.'}), 400
    try:
        numero = CitaDao().calcularNumeroSesion(id_paciente, tipo_cita, inicio, request.args.get('excluir_id_cita', type=int))
        return jsonify({'success': True, 'data': {'numero': numero}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al calcular el número de sesión: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/especialistas', methods=['GET'])
@role_required(*ROLES_CITAS)
def getEspecialistasParaCitas():
    """GET: especialistas disponibles para agendar citas."""
    try:
        data = FuncionarioDao().getEspecialistasActivos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/slots-disponibles', methods=['GET'])
@role_required(*ROLES_CITAS)
def getSlotsDisponibles():
    """GET: turnos libres, con filtros de especialista, especialidad y fechas."""
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
    """GET: lista las citas, con filtros por especialista, paciente y fechas."""
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
    """GET: cita por su id; 404 si no existe."""
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
    """POST: valida y registra una cita en un turno libre."""
    data = request.get_json() or {}

    if not data.get('id_paciente'):
        return jsonify({'success': False, 'error': msg_obligatorio('id_paciente')}), 400
    if not data.get('id_slot_agenda'):
        return jsonify({'success': False, 'error': msg_obligatorio('id_slot_agenda')}), 400

    try:
        datos = {
            'id_paciente': data['id_paciente'],
            'id_slot_agenda': data['id_slot_agenda'],
            'id_especialidad': data.get('id_especialidad'),
            'modalidad': data.get('modalidad', 'PRESENCIAL'),
            **_campos_tipo_cita(data),
            'cita_numero_sesion': data.get('cita_numero_sesion'),
            'motivo': data.get('motivo'),
            'observaciones': data.get('observaciones'),
        }
        _validar_primera_cita(datos['id_paciente'], datos['tipo_cita'])
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
        return jsonify({'success': False, 'error': msg_obligatorio('id_slot_agenda')}), 400
    if not data.get('motivo'):
        return jsonify({'success': False, 'error': msg_obligatorio('motivo')}), 400

    try:
        datos = {
            'id_slot_agenda': data['id_slot_agenda'],
            'id_especialidad': data.get('id_especialidad'),
            'modalidad': data.get('modalidad', 'PRESENCIAL'),
            **_campos_tipo_cita(data),
            'cita_numero_sesion': data.get('cita_numero_sesion'),
            'motivo': data.get('motivo'),
            'observaciones': data.get('observaciones'),
        }
        cita_actual = CitaDao().getCitaById(id_cita)
        if cita_actual:
            _validar_primera_cita(cita_actual['id_paciente'], datos['tipo_cita'], excluir_id_cita=id_cita)
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
    """GET: historial de cambios de estado de la cita."""
    try:
        data = CitaDao().getLogEstados(id_cita)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener historial de la cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>/recordatorios', methods=['GET'])
@role_required(*ROLES_CITAS)
def getRecordatoriosCita(id_cita):
    """GET: recordatorios de la cita."""
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
    """PATCH: cambia el estado de la cita (las transiciones se validan en el servidor)."""
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



@citaapi.route('/citas/<int:id_cita>/correccion', methods=['POST'])
@role_required(*ROLES_CITAS)
def corregirCita(id_cita):
    """Corrige una cita cerrada o de un día anterior (CitaDao.corregirCita). Si quien la pide
    no es Administrador, un administrador presente escribe su usuario y contraseña
    (AuthService.verificar_autorizacion_administrador). Queda en el historial y en Auditoría."""
    data = request.get_json() or {}
    cod_estado_nuevo = data.get('cod_estado_nuevo') or None
    if cod_estado_nuevo and cod_estado_nuevo not in ESTADOS_VALIDOS:
        return jsonify({'success': False, 'error': f'Estado inválido. Valores permitidos: {ESTADOS_VALIDOS}.'}), 400
    if not (data.get('motivo_correccion') or '').strip():
        return jsonify({'success': False, 'error': msg_obligatorio('Motivo de la corrección')}), 400

    try:
        roles = {(r or '').upper() for r in session.get('roles', [])}
        if roles.intersection(AuthService.ROLES_AUTORIZAN_CORRECCION):
            autorizador = {'id_usuario': session.get('id_usuario'), 'usu_nick': session.get('usu_nick')}
        else:
            autorizador = AuthService.verificar_autorizacion_administrador(
                data.get('autorizador_usuario'), data.get('autorizador_clave')
            )

        resultado = CitaDao().corregirCita(
            id_cita, cod_estado_nuevo, data.get('datos'), data['motivo_correccion'],
            usuario_modificacion=session.get('id_usuario'), autorizador=autorizador,
        )
        AuditoriaDao().registrar_evento(
            id_usuario=session.get('id_usuario'), accion=AuditAccion.RECORD_UPDATE,
            detalle=(f"Corrección de cita #{id_cita} ({resultado['cod_estado_anterior']} -> "
                     f"{resultado['cod_estado_nuevo']}) pedida por {session.get('usu_nick')}. {resultado['detalle']}"),
            ip_origen=AuthService.obtener_ip_cliente(),
        )
        return jsonify({'success': True, 'mensaje': 'Cita corregida correctamente.', 'data': resultado, 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al corregir cita {id_cita}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
