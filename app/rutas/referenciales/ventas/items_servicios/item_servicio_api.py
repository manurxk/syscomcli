from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.items_servicios.ItemServicioDao import ItemServicioDao

itemapi = Blueprint('itemapi', __name__)


@itemapi.route('/items_servicios', methods=['GET'])
def get_items():
    """Obtiene todos los items/servicios."""
    dao = ItemServicioDao()
    try:
        data = dao.getItems()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener items_servicios: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemapi.route('/items_servicios/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Obtiene un item/servicio por ID."""
    dao = ItemServicioDao()
    try:
        item = dao.getItemById(item_id)
        if item:
            return jsonify({'success': True, 'data': item, 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el item/servicio.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener item_servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemapi.route('/items_servicios', methods=['POST'])
def add_item():
    """Agrega un nuevo item/servicio al catálogo."""
    dao = ItemServicioDao()
    data = request.get_json() or {}

    if 'descripcion' not in data or not str(data['descripcion'] or '').strip():
        return jsonify({'success': False, 'error': 'El campo descripcion es obligatorio.'}), 400

    try:
        item_id = dao.guardarItem(
            descripcion=data.get('descripcion', ''),
            codigo=data.get('codigo'),
            id_tipo_item=data.get('id_tipo_item'),
            unidad_medida=data.get('unidad_medida', 'SERVICIO'),
            precio_referencial=data.get('precio_referencial', 0),
            id_tipo_impuesto=data.get('id_tipo_impuesto'),
            porcentaje_impuesto=data.get('porcentaje_impuesto', 0),
            estado='A' if data.get('estado', True) else 'I',
        )
        if not item_id:
            return jsonify({'success': False, 'error': 'No se pudo guardar el item/servicio.'}), 400

        item = dao.getItemById(item_id)
        return jsonify({'success': True, 'data': item, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al agregar item_servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemapi.route('/items_servicios/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Actualiza un item/servicio existente."""
    dao = ItemServicioDao()
    data = request.get_json() or {}

    if 'descripcion' not in data or not str(data['descripcion'] or '').strip():
        return jsonify({'success': False, 'error': 'El campo descripcion es obligatorio.'}), 400

    try:
        ok = dao.updateItem(
            id_item=item_id,
            descripcion=data.get('descripcion', ''),
            codigo=data.get('codigo'),
            id_tipo_item=data.get('id_tipo_item'),
            unidad_medida=data.get('unidad_medida', 'SERVICIO'),
            precio_referencial=data.get('precio_referencial', 0),
            id_tipo_impuesto=data.get('id_tipo_impuesto'),
            porcentaje_impuesto=data.get('porcentaje_impuesto', 0),
            estado='A' if data.get('estado', True) else 'I',
        )
        if not ok:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el item/servicio.'}), 400

        item = dao.getItemById(item_id)
        return jsonify({'success': True, 'data': item, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar item_servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemapi.route('/items_servicios/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Elimina un item/servicio del catálogo."""
    dao = ItemServicioDao()
    try:
        ok = dao.deleteItem(item_id)
        if not ok:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el item/servicio.'}), 404
        return jsonify({'success': True, 'mensaje': 'Item/servicio eliminado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al eliminar item_servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500




