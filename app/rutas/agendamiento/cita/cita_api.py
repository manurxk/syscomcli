from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.auth.utils.decorators import role_required

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


@citaapi.route('/citas/<int:id_cita>/logs', methods=['GET'])
@role_required(*ROLES_CITAS)
def getLogsCita(id_cita):
    try:
        data = CitaDao().getLogEstados(id_cita)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener historial de la cita: {str(e)}")
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
