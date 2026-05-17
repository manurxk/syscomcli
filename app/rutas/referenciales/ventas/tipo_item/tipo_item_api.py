from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.tipo_item.TipoItemDao import TipoItemDao

tipo_item_api = Blueprint('tipo_item_api', __name__)

@tipo_item_api.route('/tipos_items', methods=['GET'])
def getTiposItems():
    tipo_item_dao = TipoItemDao()
    try:
        tipos_items = tipo_item_dao.getTiposItems()
        return jsonify({'success': True, 'data': tipos_items, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los tipos de items: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_item_api.route('/tipos_items/<int:tipo_item_id>', methods=['GET'])
def getTipoItem(tipo_item_id):
    tipo_item_dao = TipoItemDao()
    try:
        tipo_item = tipo_item_dao.getTipoItemById(tipo_item_id)
        if tipo_item:
            return jsonify({'success': True, 'data': tipo_item, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el tipo de item.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de item: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_item_api.route('/tipos_items', methods=['POST'])
def addTipoItem():
    data = request.get_json()
    tipo_item_dao = TipoItemDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        categoria = data.get('categoria', '').upper() if data.get('categoria') else None
        requiere_stock = data.get('requiere_stock', False)
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        tipo_item_id = tipo_item_dao.guardarTipoItem(descripcion, codigo, categoria, requiere_stock, estado)
        if tipo_item_id:
            return jsonify({
                'success': True,
                'data': {'id': tipo_item_id, 'descripcion': descripcion, 'codigo': codigo, 
                        'categoria': categoria, 'requiere_stock': requiere_stock, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el tipo de item.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar tipo de item: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_item_api.route('/tipos_items/<int:tipo_item_id>', methods=['PUT'])
def updateTipoItem(tipo_item_id):
    data = request.get_json()
    tipo_item_dao = TipoItemDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        categoria = data.get('categoria', '').upper() if data.get('categoria') else None
        requiere_stock = data.get('requiere_stock', False)
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if tipo_item_dao.updateTipoItem(tipo_item_id, descripcion, codigo, categoria, requiere_stock, estado):
            return jsonify({
                'success': True,
                'data': {'id': tipo_item_id, 'descripcion': descripcion, 'codigo': codigo,
                        'categoria': categoria, 'requiere_stock': requiere_stock, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el tipo de item.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de item: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@tipo_item_api.route('/tipos_items/<int:tipo_item_id>', methods=['DELETE'])
def deleteTipoItem(tipo_item_id):
    tipo_item_dao = TipoItemDao()
    try:
        if tipo_item_dao.deleteTipoItem(tipo_item_id):
            return jsonify({'success': True, 'mensaje': f'Tipo de item eliminado correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el tipo de item.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar tipo de item: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















