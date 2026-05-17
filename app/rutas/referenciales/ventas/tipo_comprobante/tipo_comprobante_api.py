from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.tipo_comprobante.TipoComprobanteDao import TipoComprobanteDao

tipo_comprobante_api = Blueprint('tipo_comprobante_api', __name__)

@tipo_comprobante_api.route('/tipos_comprobantes', methods=['GET'])
def getTiposComprobantes():
    tipo_comprobante_dao = TipoComprobanteDao()
    try:
        tipos_comprobantes = tipo_comprobante_dao.getTiposComprobantes()
        return jsonify({'success': True, 'data': tipos_comprobantes, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los tipos de comprobantes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_comprobante_api.route('/tipos_comprobantes/<int:tipo_comprobante_id>', methods=['GET'])
def getTipoComprobante(tipo_comprobante_id):
    tipo_comprobante_dao = TipoComprobanteDao()
    try:
        tipo_comprobante = tipo_comprobante_dao.getTipoComprobanteById(tipo_comprobante_id)
        if tipo_comprobante:
            return jsonify({'success': True, 'data': tipo_comprobante, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el tipo de comprobante.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_comprobante_api.route('/tipos_comprobantes', methods=['POST'])
def addTipoComprobante():
    data = request.get_json()
    tipo_comprobante_dao = TipoComprobanteDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        codigo_sifen = data.get('codigo_sifen', '')
        requiere_timbrado = data.get('requiere_timbrado', True)
        tipo_documento = data.get('tipo_documento', '').upper() if data.get('tipo_documento') else None
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        tipo_comprobante_id = tipo_comprobante_dao.guardarTipoComprobante(
            descripcion, codigo, codigo_sifen, requiere_timbrado, tipo_documento, estado
        )
        if tipo_comprobante_id:
            return jsonify({
                'success': True,
                'data': {'id': tipo_comprobante_id, 'descripcion': descripcion, 'codigo': codigo,
                        'codigo_sifen': codigo_sifen, 'requiere_timbrado': requiere_timbrado,
                        'tipo_documento': tipo_documento, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el tipo de comprobante.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_comprobante_api.route('/tipos_comprobantes/<int:tipo_comprobante_id>', methods=['PUT'])
def updateTipoComprobante(tipo_comprobante_id):
    data = request.get_json()
    tipo_comprobante_dao = TipoComprobanteDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        codigo_sifen = data.get('codigo_sifen', '')
        requiere_timbrado = data.get('requiere_timbrado', True)
        tipo_documento = data.get('tipo_documento', '').upper() if data.get('tipo_documento') else None
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if tipo_comprobante_dao.updateTipoComprobante(
            tipo_comprobante_id, descripcion, codigo, codigo_sifen, requiere_timbrado, tipo_documento, estado
        ):
            return jsonify({
                'success': True,
                'data': {'id': tipo_comprobante_id, 'descripcion': descripcion, 'codigo': codigo,
                        'codigo_sifen': codigo_sifen, 'requiere_timbrado': requiere_timbrado,
                        'tipo_documento': tipo_documento, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el tipo de comprobante.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_comprobante_api.route('/tipos_comprobantes/<int:tipo_comprobante_id>', methods=['DELETE'])
def deleteTipoComprobante(tipo_comprobante_id):
    tipo_comprobante_dao = TipoComprobanteDao()
    try:
        if tipo_comprobante_dao.deleteTipoComprobante(tipo_comprobante_id):
            return jsonify({'success': True, 'mensaje': f'Tipo de comprobante eliminado correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el tipo de comprobante.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















