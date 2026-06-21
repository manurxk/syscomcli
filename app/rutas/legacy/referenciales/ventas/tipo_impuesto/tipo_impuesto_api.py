from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.tipo_impuesto.TipoImpuestoDao import TipoImpuestoDao

tipo_impuesto_api = Blueprint('tipo_impuesto_api', __name__)

@tipo_impuesto_api.route('/tipos_impuestos', methods=['GET'])
def getTiposImpuestos():
    tipo_impuesto_dao = TipoImpuestoDao()
    try:
        tipos_impuestos = tipo_impuesto_dao.getTiposImpuestos()
        return jsonify({'success': True, 'data': tipos_impuestos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los tipos de impuestos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_impuesto_api.route('/tipos_impuestos/<int:tipo_impuesto_id>', methods=['GET'])
def getTipoImpuesto(tipo_impuesto_id):
    tipo_impuesto_dao = TipoImpuestoDao()
    try:
        tipo_impuesto = tipo_impuesto_dao.getTipoImpuestoById(tipo_impuesto_id)
        if tipo_impuesto:
            return jsonify({'success': True, 'data': tipo_impuesto, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el tipo de impuesto.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_impuesto_api.route('/tipos_impuestos', methods=['POST'])
def addTipoImpuesto():
    data = request.get_json()
    tipo_impuesto_dao = TipoImpuestoDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        porcentaje = float(data.get('porcentaje', 0))
        tipo_calculo = data.get('tipo_calculo', 'PORCENTAJE')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        tipo_impuesto_id = tipo_impuesto_dao.guardarTipoImpuesto(descripcion, codigo, porcentaje, tipo_calculo, estado)
        if tipo_impuesto_id:
            return jsonify({
                'success': True,
                'data': {'id': tipo_impuesto_id, 'descripcion': descripcion, 'codigo': codigo,
                        'porcentaje': porcentaje, 'tipo_calculo': tipo_calculo, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el tipo de impuesto.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_impuesto_api.route('/tipos_impuestos/<int:tipo_impuesto_id>', methods=['PUT'])
def updateTipoImpuesto(tipo_impuesto_id):
    data = request.get_json()
    tipo_impuesto_dao = TipoImpuestoDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        porcentaje = float(data.get('porcentaje', 0))
        tipo_calculo = data.get('tipo_calculo', 'PORCENTAJE')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if tipo_impuesto_dao.updateTipoImpuesto(tipo_impuesto_id, descripcion, codigo, porcentaje, tipo_calculo, estado):
            return jsonify({
                'success': True,
                'data': {'id': tipo_impuesto_id, 'descripcion': descripcion, 'codigo': codigo,
                        'porcentaje': porcentaje, 'tipo_calculo': tipo_calculo, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el tipo de impuesto.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_impuesto_api.route('/tipos_impuestos/<int:tipo_impuesto_id>', methods=['DELETE'])
def deleteTipoImpuesto(tipo_impuesto_id):
    tipo_impuesto_dao = TipoImpuestoDao()
    try:
        if tipo_impuesto_dao.deleteTipoImpuesto(tipo_impuesto_id):
            return jsonify({'success': True, 'mensaje': f'Tipo de impuesto eliminado correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el tipo de impuesto.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















