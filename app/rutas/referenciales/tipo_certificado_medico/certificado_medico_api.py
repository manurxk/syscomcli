from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.tipo_certificado_medico.CertificadoMedicoDao import TipoCertificadoMedicoDao

tipo_certificado_medico_api = Blueprint('tipo_certificado_medico_api', __name__)

# ===============================
# Trae todos los tipos de certificados médicos
# ===============================
@tipo_certificado_medico_api.route('/tipos_certificados_medicos', methods=['GET'])
def getTiposCertificadosMedicos():
    tipo_certificado_medico_dao = TipoCertificadoMedicoDao()

    try:
        tipos_certificados = tipo_certificado_medico_dao.getTiposCertificadosMedicos()

        return jsonify({
            'success': True,
            'data': tipos_certificados,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los tipos de certificados médicos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae un tipo de certificado médico por ID
# ===============================
@tipo_certificado_medico_api.route('/tipos_certificados_medicos/<int:tipo_certificado_id>', methods=['GET'])
def getTipoCertificadoMedico(tipo_certificado_id):
    tipo_certificado_medico_dao = TipoCertificadoMedicoDao()

    try:
        tipo_certificado = tipo_certificado_medico_dao.getTipoCertificadoMedicoById(tipo_certificado_id)

        if tipo_certificado:
            return jsonify({
                'success': True,
                'data': tipo_certificado,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de certificado médico con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener tipo de certificado médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega un nuevo tipo de certificado médico
# ===============================
@tipo_certificado_medico_api.route('/tipos_certificados_medicos', methods=['POST'])
def addTipoCertificadoMedico():
    data = request.get_json()
    tipo_certificado_medico_dao = TipoCertificadoMedicoDao()

    campos_requeridos = ['descripcion', 'estado']

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
        if campo == 'descripcion' and (data[campo] is None or len(data[campo].strip()) == 0):
            return jsonify({
                'success': False,
                'error': 'La descripción no puede estar vacía.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        estado = data.get('estado', 'A')

        # Validar que la descripción contenga solo letras, números, espacios y puntos
        if not tipo_certificado_medico_dao.validarDescripcion(descripcion):
            return jsonify({
                'success': False,
                'error': 'La descripción solo puede contener letras, números, acentos, espacios y puntos.'
            }), 400

        # Validar estado
        if estado not in ['A', 'I']:
            return jsonify({
                'success': False,
                'error': 'El estado debe ser "A" (Activo) o "I" (Inactivo).'
            }), 400

        tipo_certificado_id = tipo_certificado_medico_dao.guardarTipoCertificadoMedico(descripcion, estado)
        if tipo_certificado_id:
            return jsonify({
                'success': True,
                'data': {
                    'id': tipo_certificado_id,
                    'descripcion': descripcion,
                    'estado': estado
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el tipo de certificado médico (duplicado o inválido).'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar tipo de certificado médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza un tipo de certificado médico
# ===============================
@tipo_certificado_medico_api.route('/tipos_certificados_medicos/<int:tipo_certificado_id>', methods=['PUT'])
def updateTipoCertificadoMedico(tipo_certificado_id):
    data = request.get_json()
    tipo_certificado_medico_dao = TipoCertificadoMedicoDao()

    campos_requeridos = ['descripcion', 'estado']

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
        if campo == 'descripcion' and (data[campo] is None or len(data[campo].strip()) == 0):
            return jsonify({
                'success': False,
                'error': 'La descripción no puede estar vacía.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        estado = data.get('estado', 'A')

        # Validar que la descripción contenga solo letras, números, espacios y puntos
        if not tipo_certificado_medico_dao.validarDescripcion(descripcion):
            return jsonify({
                'success': False,
                'error': 'La descripción solo puede contener letras, números, acentos, espacios y puntos.'
            }), 400

        # Validar estado
        if estado not in ['A', 'I']:
            return jsonify({
                'success': False,
                'error': 'El estado debe ser "A" (Activo) o "I" (Inactivo).'
            }), 400

        if tipo_certificado_medico_dao.updateTipoCertificadoMedico(tipo_certificado_id, descripcion, estado):
            return jsonify({
                'success': True,
                'data': {
                    'id': tipo_certificado_id,
                    'descripcion': descripcion,
                    'estado': estado
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de certificado médico con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de certificado médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Elimina un tipo de certificado médico
# ===============================
@tipo_certificado_medico_api.route('/tipos_certificados_medicos/<int:tipo_certificado_id>', methods=['DELETE'])
def deleteTipoCertificadoMedico(tipo_certificado_id):
    tipo_certificado_medico_dao = TipoCertificadoMedicoDao()

    try:
        resultado = tipo_certificado_medico_dao.deleteTipoCertificadoMedico(tipo_certificado_id)
        if resultado is True:
            return jsonify({
                'success': True,
                'mensaje': f'Tipo de certificado médico con ID {tipo_certificado_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el tipo de certificado médico porque está siendo usado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar tipo de certificado médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


















