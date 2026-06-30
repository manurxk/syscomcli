from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.clinico.movimientos.pei.PeiDao import PeiDao, CAMPOS_PEI
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.auth.utils.decorators import role_required

peiapi = Blueprint('peiapi', __name__)

ROLES_PEI = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


def _resolver_id_especialista(id_especialista_body=None):
    """Devuelve id_especialista: del body si viene, o del usuario logueado."""
    if id_especialista_body:
        return id_especialista_body
    id_funcionario = session.get('id_funcionario')
    if not id_funcionario:
        return None
    return CitaDao().getEspecialistaPorFuncionario(id_funcionario)


@peiapi.route('/pei', methods=['GET'])
@role_required(*ROLES_PEI)
def listPei():
    try:
        data = PeiDao().listTodosActuales()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al listar PEIs: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@peiapi.route('/pei/paciente/<int:id_paciente>', methods=['GET'])
@role_required(*ROLES_PEI)
def getPeiActual(id_paciente):
    try:
        data = PeiDao().getPeiActual(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener PEI actual (paciente {id_paciente}): {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@peiapi.route('/pei/paciente/<int:id_paciente>/historial', methods=['GET'])
@role_required(*ROLES_PEI)
def getHistorialPei(id_paciente):
    try:
        data = PeiDao().getHistorialPei(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener historial PEI (paciente {id_paciente}): {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@peiapi.route('/pei/<int:id_pei>', methods=['GET'])
@role_required(*ROLES_PEI)
def getPei(id_pei):
    try:
        data = PeiDao().getPeiById(id_pei)
        if not data:
            return jsonify({'success': False, 'error': 'PEI no encontrado.'}), 404
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener PEI {id_pei}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@peiapi.route('/pei/paciente/<int:id_paciente>', methods=['POST'])
@role_required(*ROLES_PEI)
def addVersionPei(id_paciente):
    """Crea una nueva versión del PEI del paciente (insert-only, ver PeiDao)."""
    body = request.get_json() or {}

    id_especialista = _resolver_id_especialista(body.get('id_especialista'))
    if not id_especialista:
        return jsonify({'success': False, 'error': 'No se pudo determinar el especialista. Verificá tu perfil.'}), 400

    datos = {campo: body.get(campo) for campo in CAMPOS_PEI}
    datos['pei_estado'] = datos.get('pei_estado') or 'ACTIVO'
    if datos['pei_estado'] not in ('ACTIVO', 'CERRADO'):
        return jsonify({'success': False, 'error': 'Estado inválido. Debe ser ACTIVO o CERRADO.'}), 400

    try:
        id_pei = PeiDao().guardarNuevaVersion(
            id_paciente, id_especialista, datos,
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_pei': id_pei}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar PEI (paciente {id_paciente}): {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
