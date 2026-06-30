from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.auth.utils.decorators import role_required

consultaapi = Blueprint('consultaapi', __name__)

ROLES_CONSULTA = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


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
    try:
        data = ConsultaDao().getConsultasPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consultas del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/cita/<int:id_cita>', methods=['GET'])
@role_required(*ROLES_CONSULTA)
def getConsultaDesdeCita(id_cita):
    try:
        consulta = ConsultaDao().getConsultaDesdeCita(id_cita)
        return jsonify({'success': True, 'data': consulta, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consulta desde cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/citas/<int:id_cita>/iniciar-consulta', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO", "RECEPCION")
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

        usuario = session.get('id_usuario')
        id_consulta = ConsultaDao().getOrCrearDesdeCita(cita, usuario_creacion=usuario)
        if id_consulta is None:
            return jsonify({'success': False, 'error': 'No se pudo iniciar la consulta.'}), 500

        if cod_estado not in ('EN_CONSULTA', 'COMPLETADA'):
            CitaDao().cambiarEstadoCita(id_cita, 'EN_CONSULTA', usuario_modificacion=usuario)

        return jsonify({'success': True, 'data': {'id_consulta': id_consulta}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al iniciar consulta desde cita: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/<int:id_consulta>', methods=['PUT'])
@role_required(*ROLES_CONSULTA)
def updateConsulta(id_consulta):
    data = request.get_json() or {}
    dao = ConsultaDao()

    if not dao.getConsultaById(id_consulta):
        return jsonify({'success': False, 'error': 'No se encontró la consulta con el ID proporcionado.'}), 404

    campos_requeridos = ['consulta_fecha', 'consulta_motivo', 'consulta_estado']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({'success': False, 'error': f'El campo "{campo}" es obligatorio.'}), 400

    try:
        dao.updateConsulta(id_consulta, data, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_consulta': id_consulta}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultaapi.route('/consultas/<int:id_consulta>', methods=['DELETE'])
@role_required(*ROLES_CONSULTA)
def deleteConsulta(id_consulta):
    try:
        if ConsultaDao().desactivarConsulta(id_consulta, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Consulta desactivada correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró la consulta con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al desactivar consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
