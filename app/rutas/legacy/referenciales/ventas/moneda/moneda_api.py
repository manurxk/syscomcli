from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.moneda.MonedaDao import MonedaDao

moneda_api = Blueprint('moneda_api', __name__)

@moneda_api.route('/monedas', methods=['GET'])
def getMonedas():
    moneda_dao = MonedaDao()
    try:
        monedas = moneda_dao.getMonedas()
        return jsonify({'success': True, 'data': monedas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las monedas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@moneda_api.route('/monedas/<int:moneda_id>', methods=['GET'])
def getMoneda(moneda_id):
    moneda_dao = MonedaDao()
    try:
        moneda = moneda_dao.getMonedaById(moneda_id)
        if moneda:
            return jsonify({'success': True, 'data': moneda, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la moneda.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@moneda_api.route('/monedas', methods=['POST'])
def addMoneda():
    data = request.get_json()
    moneda_dao = MonedaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    if 'codigo' not in data or not data['codigo']:
        return jsonify({'success': False, 'error': 'El código es obligatorio.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data['codigo'].upper()
        simbolo = data.get('simbolo', '')
        decimales = int(data.get('decimales', 0))
        es_moneda_local = data.get('es_moneda_local', False)
        tasa_cambio = float(data.get('tasa_cambio', 1.0))
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        moneda_id = moneda_dao.guardarMoneda(
            descripcion, codigo, simbolo, decimales, es_moneda_local, tasa_cambio, estado
        )
        if moneda_id:
            return jsonify({
                'success': True,
                'data': {'id': moneda_id, 'descripcion': descripcion, 'codigo': codigo,
                        'simbolo': simbolo, 'decimales': decimales, 'es_moneda_local': es_moneda_local,
                        'tasa_cambio': tasa_cambio, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la moneda (código duplicado).'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@moneda_api.route('/monedas/<int:moneda_id>', methods=['PUT'])
def updateMoneda(moneda_id):
    data = request.get_json()
    moneda_dao = MonedaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    if 'codigo' not in data or not data['codigo']:
        return jsonify({'success': False, 'error': 'El código es obligatorio.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data['codigo'].upper()
        simbolo = data.get('simbolo', '')
        decimales = int(data.get('decimales', 0))
        es_moneda_local = data.get('es_moneda_local', False)
        tasa_cambio = float(data.get('tasa_cambio', 1.0))
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if moneda_dao.updateMoneda(
            moneda_id, descripcion, codigo, simbolo, decimales, es_moneda_local, tasa_cambio, estado
        ):
            return jsonify({
                'success': True,
                'data': {'id': moneda_id, 'descripcion': descripcion, 'codigo': codigo,
                        'simbolo': simbolo, 'decimales': decimales, 'es_moneda_local': es_moneda_local,
                        'tasa_cambio': tasa_cambio, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar la moneda.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@moneda_api.route('/monedas/<int:moneda_id>', methods=['DELETE'])
def deleteMoneda(moneda_id):
    moneda_dao = MonedaDao()
    try:
        if moneda_dao.deleteMoneda(moneda_id):
            return jsonify({'success': True, 'mensaje': f'Moneda eliminada correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar la moneda.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















