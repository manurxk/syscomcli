from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
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


@consultaapi.route('/consultas', methods=['POST'])
@role_required(*ROLES_CONSULTA)
def addConsulta():
    data = request.get_json() or {}

    campos_requeridos = ['id_paciente', 'id_especialista', 'consulta_fecha', 'consulta_motivo']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({'success': False, 'error': f'El campo "{campo}" es obligatorio.'}), 400

    try:
        id_consulta = ConsultaDao().guardarConsulta(data, usuario_creacion=session.get('id_usuario'))
        if id_consulta is None:
            return jsonify({'success': False, 'error': 'No se pudo guardar la consulta.'}), 500
        return jsonify({'success': True, 'data': {'id_consulta': id_consulta}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar consulta: {str(e)}", exc_info=True)
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
