from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.tipo_certificado_medico.TipoCertificadoMedicoDao import TipoCertificadoMedicoDao
from app.auth.utils.decorators import role_required

tipocertificadomedicoapi = Blueprint('tipocertificadomedicoapi', __name__)


@tipocertificadomedicoapi.route('/tipos-certificados-medicos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getTiposCertificadosMedicos():
    try:
        data = TipoCertificadoMedicoDao().getTiposCertificadosMedicos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocertificadomedicoapi.route('/tipos-certificados-medicos/<int:tipo_certificado_medico_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getTipoCertificadoMedico(tipo_certificado_medico_id):
    try:
        registro = TipoCertificadoMedicoDao().getTipoCertificadoMedicoById(tipo_certificado_medico_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocertificadomedicoapi.route('/tipos-certificados-medicos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoCertificadoMedico():
    data = request.get_json() or {}
    dao = TipoCertificadoMedicoDao()

    descripcion = (data.get('des_tipo_certificado_medico') or '').strip().upper()
    estado = bool(data.get('est_tipo_certificado_medico', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoCertificadoMedicoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarTipoCertificadoMedico(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_certificado_medico': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocertificadomedicoapi.route('/tipos-certificados-medicos/<int:tipo_certificado_medico_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoCertificadoMedico(tipo_certificado_medico_id):
    data = request.get_json() or {}
    dao = TipoCertificadoMedicoDao()

    if not dao.getTipoCertificadoMedicoById(tipo_certificado_medico_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_tipo_certificado_medico') or '').strip().upper()
    estado = bool(data.get('est_tipo_certificado_medico', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoCertificadoMedicoExiste(descripcion, excluir_id=tipo_certificado_medico_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateTipoCertificadoMedico(tipo_certificado_medico_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_certificado_medico': tipo_certificado_medico_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocertificadomedicoapi.route('/tipos-certificados-medicos/<int:tipo_certificado_medico_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoCertificadoMedico(tipo_certificado_medico_id):
    dao = TipoCertificadoMedicoDao()

    if not dao.getTipoCertificadoMedicoById(tipo_certificado_medico_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarTipoCertificadoMedico(tipo_certificado_medico_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {tipo_certificado_medico_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
