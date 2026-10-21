from flask import Blueprint, request, jsonify, current_app as app, session, send_file

from app.dao.clinico.movimientos.certificado_medico.CertificadoMedicoDao import CertificadoMedicoDao
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.auth.utils.decorators import role_required
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.services.documento_clinico_pdf_service import DocumentoClinicoPdfService
from app.utils.mensajes_validacion import msg_obligatorio

certificadomedicoapi = Blueprint('certificadomedicoapi', __name__)

ROLES_CERTIFICADO = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@certificadomedicoapi.route('/consultas/<int:id_consulta>/certificados', methods=['GET'])
@role_required(*ROLES_CERTIFICADO)
def getCertificados(id_consulta):
    """GET: lista los certificados médicos de la consulta."""
    try:
        data = CertificadoMedicoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener certificados de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@certificadomedicoapi.route('/consultas/<int:id_consulta>/certificados', methods=['POST'])
@role_required(*ROLES_CERTIFICADO)
def addCertificado(id_consulta):
    """POST: valida y registra certificado médico en la consulta (201)."""
    data = request.get_json() or {}
    if not data.get('id_tipo_certificado_medico'):
        return jsonify({'success': False, 'error': msg_obligatorio('Tipo de certificado')}), 400
    if not data.get('certificado_fecha'):
        return jsonify({'success': False, 'error': msg_obligatorio('Fecha del certificado')}), 400
    if not (data.get('certificado_motivo') or '').strip():
        return jsonify({'success': False, 'error': msg_obligatorio('Motivo del certificado')}), 400

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
    """DELETE: baja lógica de certificado médico; 404 si no existe."""
    try:
        if CertificadoMedicoDao().desactivar(id_certificado, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar certificado de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@certificadomedicoapi.route('/certificados/<int:id_certificado>/pdf', methods=['GET'])
@role_required(*ROLES_CERTIFICADO)
def getCertificadoPdf(id_certificado):
    """PDF imprimible (CERTIFICADO.html). Lo firma el especialista de la consulta, que es quien lo emitió."""
    try:
        cert = CertificadoMedicoDao().getParaImprimir(id_certificado)
        if not cert:
            return jsonify({'success': False, 'error': 'No se encontró el documento.'}), 404
        ficha = FichaDao()
        buffer = DocumentoClinicoPdfService().generar_certificado_pdf(
            cert, ficha.getDatosPaciente(cert['id_paciente']) or {},
            ficha.getDatosGenerador(cert['id_especialista']) or {},
            DocumentoClinicoPdfService.config_empresa(),
        )
        return send_file(buffer, mimetype='application/pdf', as_attachment=False,
                         download_name=f"certificado_{cert['certificado_numero']}.pdf")
    except Exception as e:
        app.logger.error(f"Error al generar PDF de certificado {id_certificado}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
