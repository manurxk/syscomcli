from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.movimientos.certificado_medico.CertificadoMedicoDao import CertificadoMedicoDao
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.auth.utils.decorators import role_required

certificadomedicoapi = Blueprint('certificadomedicoapi', __name__)

ROLES_CERTIFICADO = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@certificadomedicoapi.route('/consultas/<int:id_consulta>/certificados', methods=['GET'])
@role_required(*ROLES_CERTIFICADO)
def getCertificados(id_consulta):
    try:
        data = CertificadoMedicoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener certificados de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@certificadomedicoapi.route('/consultas/<int:id_consulta>/certificados', methods=['POST'])
@role_required(*ROLES_CERTIFICADO)
def addCertificado(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_tipo_certificado_medico'):
        return jsonify({'success': False, 'error': 'El tipo de certificado es obligatorio.'}), 400
    if not data.get('certificado_fecha'):
        return jsonify({'success': False, 'error': 'La fecha del certificado es obligatoria.'}), 400
    if not (data.get('certificado_motivo') or '').strip():
        return jsonify({'success': False, 'error': 'El motivo del certificado es obligatorio.'}), 400

    consulta = ConsultaDao().getConsultaParaEditar(id_consulta)
    if not consulta:
        return jsonify({'success': False, 'error': 'La consulta no existe.'}), 404

    try:
        nuevo_id = CertificadoMedicoDao().guardar(
            id_consulta, consulta['id_paciente'], consulta['id_especialista'],
            data, usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_certificado': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar certificado de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@certificadomedicoapi.route('/certificados/<int:id_certificado>', methods=['DELETE'])
@role_required(*ROLES_CERTIFICADO)
def deleteCertificado(id_certificado):
    try:
        if CertificadoMedicoDao().desactivar(id_certificado, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar certificado de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
