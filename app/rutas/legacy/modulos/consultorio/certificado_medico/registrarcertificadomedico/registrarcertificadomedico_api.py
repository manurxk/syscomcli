from flask import Blueprint, request, jsonify, current_app as app, send_file
from app.dao.modulos.consultorio.certificado_medico.CertificadoMedicoDao import CertificadoMedicoDao
from app.dao.referenciales.ventas.empresa.EmpresaDao import EmpresaDao
from app.services.pdf_service import CertificadoPDFService
from datetime import datetime

certificadomedicoapi = Blueprint('certificadomedicoapi', __name__)

@certificadomedicoapi.route('/certificados-medicos/<int:id_certificado>/pdf', methods=['GET'])
def downloadCertificadoPDF(id_certificado):
    """Genera y descarga el PDF de un certificado médico"""
    dao = CertificadoMedicoDao()
    empresadao = EmpresaDao()
    pdf_service = CertificadoPDFService()
    
    try:
        # 1. Obtener datos del certificado
        certificado = dao.getCertificadoMedicoById(id_certificado)
        if not certificado:
            return jsonify({'success': False, 'error': 'Certificado no encontrado'}), 404
            
        # 2. Obtener datos de la clínica para branding
        config_empresa = empresadao.getEmpresaPrincipal()
        
        # 3. Preparar datos para el PDF
        # El DAO devuelve un diccionario con los campos de la BD. Mapeamos a lo que espera el service.
        pdf_data = {
            'paciente_nombre': certificado.get('paciente_nombre'),
            'paciente_cedula': certificado.get('paciente_cedula'),
            'profesional_nombre': certificado.get('profesional_nombre'),
            'profesional_registro': certificado.get('profesional_matricula'),
            'fecha_emision': certificado.get('certificado_fecha'),
            'diagnostico': certificado.get('certificado_diagnostico'),
            'descripcion': certificado.get('certificado_motivo'),
            'recomendaciones': certificado.get('certificado_recomendaciones')
        }
        
        # 4. Generar PDF
        buffer = pdf_service.generar_pdf(pdf_data, config_empresa)
        
        nombre_archivo = f"Certificado_{certificado.get('paciente_nombre','documento').replace(' ','_')}_{id_certificado}.pdf"
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )
        
    except Exception as e:
        app.logger.error(f"Error generando PDF de certificado: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================
# CRUD BÁSICO DE CERTIFICADOS MÉDICOS
# ============================================

@certificadomedicoapi.route('/certificados-medicos', methods=['GET'])
def getAllCertificadosMedicos():
    """Obtiene la lista completa de certificados médicos activos"""
    dao = CertificadoMedicoDao()
    
    try:
        certificados = dao.getAllCertificadosMedicos()
        return jsonify({'success': True, 'data': certificados, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los certificados médicos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@certificadomedicoapi.route('/certificados-medicos/<int:id_certificado>', methods=['GET'])
def getCertificadoMedico(id_certificado):
    """Obtiene un certificado médico específico por su ID"""
    dao = CertificadoMedicoDao()
    
    try:
        certificado = dao.getCertificadoMedicoById(id_certificado)
        
        if certificado:
            return jsonify({'success': True, 'data': certificado, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el certificado médico.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@certificadomedicoapi.route('/certificados-medicos', methods=['POST'])
def addCertificadoMedico():
    """Crea un nuevo certificado médico"""
    data = request.get_json()
    dao = CertificadoMedicoDao()
    
    # Validar campos obligatorios
    campos_requeridos = ['id_paciente', 'id_profesional', 'certificado_fecha', 'id_tipo_certificado', 'certificado_motivo']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400
    
    try:
        certificado_id = dao.guardarCertificadoMedico(
            id_paciente=data['id_paciente'],
            id_profesional=data['id_profesional'],
            certificado_fecha=data['certificado_fecha'],
            id_tipo_certificado=data['id_tipo_certificado'],
            certificado_motivo=data['certificado_motivo'],
            id_consulta=data.get('id_consulta'),
            certificado_dias_reposo=data.get('certificado_dias_reposo'),
            certificado_desde_fecha=data.get('certificado_desde_fecha'),
            certificado_hasta_fecha=data.get('certificado_hasta_fecha'),
            certificado_diagnostico=data.get('certificado_diagnostico'),
            certificado_recomendaciones=data.get('certificado_recomendaciones'),
            certificado_estado=data.get('certificado_estado', 'VIGENTE'),
            usuario_creacion=data.get('usuario_creacion', 'ADMIN')
        )
        
        if certificado_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_certificado': certificado_id,
                    'mensaje': 'Certificado médico creado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el certificado médico.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@certificadomedicoapi.route('/certificados-medicos/<int:id_certificado>', methods=['PUT'])
def updateCertificadoMedico(id_certificado):
    """Actualiza un certificado médico existente"""
    data = request.get_json()
    dao = CertificadoMedicoDao()
    
    # Validar que existe el certificado
    certificado_existente = dao.getCertificadoMedicoById(id_certificado)
    if not certificado_existente:
        return jsonify({'success': False, 'error': 'No se encontró el certificado médico.'}), 404
    
    try:
        resultado = dao.updateCertificadoMedico(
            id_certificado=id_certificado,
            id_tipo_certificado=data.get('id_tipo_certificado'),
            certificado_dias_reposo=data.get('certificado_dias_reposo'),
            certificado_desde_fecha=data.get('certificado_desde_fecha'),
            certificado_hasta_fecha=data.get('certificado_hasta_fecha'),
            certificado_motivo=data.get('certificado_motivo'),
            certificado_diagnostico=data.get('certificado_diagnostico'),
            certificado_recomendaciones=data.get('certificado_recomendaciones'),
            certificado_estado=data.get('certificado_estado'),
            usuario_modificacion=data.get('usuario_modificacion', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {'id_certificado': id_certificado, 'mensaje': 'Certificado médico actualizado exitosamente'},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el certificado médico.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@certificadomedicoapi.route('/certificados-medicos/<int:id_certificado>', methods=['DELETE'])
def deleteCertificadoMedico(id_certificado):
    """Elimina lógicamente un certificado médico"""
    dao = CertificadoMedicoDao()
    
    try:
        if dao.deleteCertificadoMedico(id_certificado):
            return jsonify({
                'success': True,
                'mensaje': f'Certificado médico con ID {id_certificado} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el certificado médico o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar certificado médico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

