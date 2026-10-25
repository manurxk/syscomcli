from datetime import date, timedelta

from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.dao.clinico.movimientos.tratamiento.TratamientoDao import TratamientoDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_obligatorio

consultaapi = Blueprint('consultaapi', __name__)

ROLES_CONSULTA = ("ADMINISTRADOR", "CLINICO")


@consultaapi.route('/consultas/especialistas', methods=['GET'])
@role_required(*ROLES_CONSULTA)
def getEspecialistasParaConsultas():
    """Mismo combo que usa agendamiento, expuesto también para el rol CLINICO."""
    try:
        data = FuncionarioDao().getEspecialistasActivos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas', methods=['GET'])
@role_required(*ROLES_CONSULTA)
def getConsultas():
    """GET: lista las consultas; admite filtros id_especialista, id_paciente y estado por query string."""
    try:
        id_especialista = request.args.get('id_especialista', type=int)
        id_paciente = request.args.get('id_paciente', type=int)
        estado = request.args.get('estado')

        data = ConsultaDao().getConsultas(id_especialista, id_paciente, estado)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consultas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/<int:id_consulta>', methods=['GET'])
@role_required(*ROLES_CONSULTA)
def getConsulta(id_consulta):
    """GET: consulta por su id; 404 si no existe."""
    try:
        consulta = ConsultaDao().getConsultaById(id_consulta)
        if not consulta:
            return jsonify({'success': False, 'error': 'No se encontró la consulta con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': consulta, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/<int:id_consulta>/editar', methods=['GET'])
@role_required(*ROLES_CONSULTA)
def getConsultaParaEditar(id_consulta):
    """GET: consulta con los datos necesarios para el formulario de edición; 404 si no existe."""
    try:
        consulta = ConsultaDao().getConsultaParaEditar(id_consulta)
        if not consulta:
            return jsonify({'success': False, 'error': 'No se encontró la consulta.'}), 404
        return jsonify({'success': True, 'data': consulta, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consulta para editar: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/paciente/<int:id_paciente>', methods=['GET'])
@role_required(*ROLES_CONSULTA)
def getConsultasPorPaciente(id_paciente):
    """GET: consultas del paciente."""
    try:
        data = ConsultaDao().getConsultasPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consultas del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/cita/<int:id_cita>', methods=['GET'])
@role_required(*ROLES_CONSULTA)
def getConsultaDesdeCita(id_cita):
    """GET: consulta vinculada a la cita, o vacío si aún no se inició."""
    try:
        consulta = ConsultaDao().getConsultaDesdeCita(id_cita)
        return jsonify({'success': True, 'data': consulta, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consulta desde cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/citas/<int:id_cita>/iniciar-consulta', methods=['POST'])
@role_required("ADMINISTRADOR", "CLINICO", "RECEPCION")
def iniciarConsultaDesdeCita(id_cita):
    """Crea (o recupera, si ya existe) la consulta vinculada a la cita y la pasa a
    EN_CONSULTA. Toda consulta nace de una cita — no hay alta manual suelta.

    RECEPCION incluido a propósito: el botón "Iniciar consulta" ya era accesible
    para ese rol desde citas-index (antes solo cambiaba el estado de la cita); se
    mantiene el mismo alcance de acceso aunque ahora también cree la consulta."""
    try:
        cita = CitaDao().getCitaById(id_cita)
        if not cita:
            return jsonify({'success': False, 'error': 'No se encontró la cita indicada.'}), 404

        cod_estado = cita['cod_estado_cita']
        if cod_estado in ('CANCELADA', 'AUSENTE'):
            return jsonify({'success': False, 'error': f'No se puede iniciar una consulta para una cita en estado "{cod_estado}".'}), 400

        # Validar antes de crear la consulta (ej. cita de un día anterior): si no, quedaría
        # una consulta creada para una cita que no puede pasar a EN_CONSULTA
        if cod_estado not in ('EN_CONSULTA', 'COMPLETADA'):
            CitaDao().validarCambioEstado(id_cita, 'EN_CONSULTA')

        usuario = session.get('id_usuario')
        id_consulta = ConsultaDao().getOrCrearDesdeCita(cita, usuario_creacion=usuario)
        if id_consulta is None:
            return jsonify({'success': False, 'error': 'No se pudo iniciar la consulta.'}), 500

        if cod_estado not in ('EN_CONSULTA', 'COMPLETADA'):
            CitaDao().cambiarEstadoCita(id_cita, 'EN_CONSULTA', usuario_modificacion=usuario)

        return jsonify({'success': True, 'data': {'id_consulta': id_consulta}, 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al iniciar consulta desde cita: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/<int:id_consulta>', methods=['PUT'])
@role_required(*ROLES_CONSULTA)
def updateConsulta(id_consulta):
    """PUT: valida y actualiza fecha, motivo y estado de la consulta; 404 si no existe."""
    data = request.get_json() or {}
    dao = ConsultaDao()

    consulta = dao.getConsultaById(id_consulta)
    if not consulta:
        return jsonify({'success': False, 'error': 'No se encontró la consulta con el ID proporcionado.'}), 404

    campos_requeridos = ['consulta_fecha', 'consulta_motivo', 'consulta_estado']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({'success': False, 'error': msg_obligatorio(campo)}), 400

    # Una consulta finalizada ya quedó guardada: guardarla otra vez no hace nada nuevo
    if consulta['consulta_estado'] == 'FINALIZADA' and data['consulta_estado'] == 'FINALIZADA':
        return jsonify({'success': False, 'ya_finalizada': True,
                        'error': 'Esta consulta ya fue finalizada y guardada.'}), 409

    try:
        usuario = session.get('id_usuario')
        dao.updateConsulta(id_consulta, data, usuario_modificacion=usuario)

        # Finalizar la consulta completa la cita de origen (el inverso ya existe en
        # CitaDao.cambiarEstadoCita: completar la cita finaliza la consulta).
        if data['consulta_estado'] == 'FINALIZADA':
            cita = CitaDao().getCitaById(consulta['id_cita'])
            if cita and cita['cod_estado_cita'] not in ('COMPLETADA', 'CANCELADA', 'AUSENTE'):
                CitaDao().cambiarEstadoCita(consulta['id_cita'], 'COMPLETADA', usuario_modificacion=usuario,
                                            motivo='Consulta finalizada')

        return jsonify({'success': True, 'data': {'id_consulta': id_consulta}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/<int:id_consulta>', methods=['DELETE'])
@role_required(*ROLES_CONSULTA)
def deleteConsulta(id_consulta):
    """DELETE: baja lógica de la consulta; 404 si no existe."""
    try:
        if ConsultaDao().desactivarConsulta(id_consulta, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Consulta desactivada correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró la consulta con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al desactivar consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ----------------------------------------------------------------------
# Próximo control: el especialista agenda en su propia agenda una cita de Seguimiento del paciente de la consulta.
# Recepción la ve como cualquier otra cita (Citas, calendario, recordatorio). Reusa CitaDao.crearCita.
# ----------------------------------------------------------------------

def _consultaPropia(id_consulta):
    """(consulta, error): la consulta es del especialista logueado."""
    id_funcionario = session.get('id_funcionario')
    id_especialista = CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None
    consulta = TratamientoDao().getContextoConsulta(id_consulta)
    if not consulta or not id_especialista or consulta['id_especialista'] != id_especialista:
        return None, ('No se encontró la consulta con el ID proporcionado.', 404)
    return consulta, None


@consultaapi.route('/consultas/<int:id_consulta>/proximo-control/turnos', methods=['GET'])
@role_required("CLINICO")
def getTurnosProximoControl(id_consulta):
    """GET: turnos libres del especialista de la consulta, de hoy hasta donde hay turnos generados."""
    try:
        consulta, error = _consultaPropia(id_consulta)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        hoy = date.today()
        hasta = hoy + timedelta(days=AgendaHorariosDao.HORIZONTE_DIAS_DEFAULT)
        turnos = CitaDao().getSlotsDisponibles(consulta['id_especialista'], None, hoy.isoformat(), hasta.isoformat())
        return jsonify({'success': True, 'data': turnos, 'id_especialista': consulta['id_especialista'], 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener los turnos del próximo control: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/<int:id_consulta>/proximo-control', methods=['POST'])
@role_required("CLINICO")
def addProximoControl(id_consulta):
    """POST: crea la cita de Seguimiento (201) en un turno libre del propio especialista. Recibe id_slot_agenda y motivo."""
    data = request.get_json() or {}
    id_slot = data.get('id_slot_agenda')
    if not isinstance(id_slot, int):
        return jsonify({'success': False, 'error': msg_obligatorio('Turno')}), 400
    try:
        consulta, error = _consultaPropia(id_consulta)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        if TratamientoDao().getEspecialistaDeSlots([id_slot]).get(id_slot) != consulta['id_especialista']:
            return jsonify({'success': False, 'error': 'El turno debe ser de tu propia agenda.'}), 400
        id_cita = CitaDao().crearCita({
            'id_paciente': consulta['id_paciente'], 'id_slot_agenda': id_slot, 'modalidad': 'PRESENCIAL',
            'tipo_cita': 'SEGUIMIENTO', 'cita_es_primera_vez': False,
            'motivo': (data.get('motivo') or '').strip() or 'Control',
        }, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_cita': id_cita}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al agendar el próximo control: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
