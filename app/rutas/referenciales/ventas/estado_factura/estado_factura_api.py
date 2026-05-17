from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.estado_factura.EstadoFacturaDao import EstadoFacturaDao

estado_factura_api = Blueprint('estado_factura_api', __name__)

@estado_factura_api.route('/estados_factura', methods=['GET'])
def getEstadosFactura():
    estado_factura_dao = EstadoFacturaDao()
    try:
        estados_factura = estado_factura_dao.getEstadosFactura()
        return jsonify({'success': True, 'data': estados_factura, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los estados de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@estado_factura_api.route('/estados_factura/<int:estado_factura_id>', methods=['GET'])
def getEstadoFactura(estado_factura_id):
    estado_factura_dao = EstadoFacturaDao()
    try:
        estado_factura = estado_factura_dao.getEstadoFacturaById(estado_factura_id)
        if estado_factura:
            return jsonify({'success': True, 'data': estado_factura, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el estado de factura.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@estado_factura_api.route('/estados_factura', methods=['POST'])
def addEstadoFactura():
    data = request.get_json()
    estado_factura_dao = EstadoFacturaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        permite_modificacion = data.get('permite_modificacion', True)
        permite_anulacion = data.get('permite_anulacion', True)
        color = data.get('color', 'secondary')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        estado_factura_id = estado_factura_dao.guardarEstadoFactura(
            descripcion, codigo, permite_modificacion, permite_anulacion, color, estado
        )
        if estado_factura_id:
            return jsonify({
                'success': True,
                'data': {'id': estado_factura_id, 'descripcion': descripcion, 'codigo': codigo,
                        'permite_modificacion': permite_modificacion, 'permite_anulacion': permite_anulacion,
                        'color': color, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el estado de factura.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@estado_factura_api.route('/estados_factura/<int:estado_factura_id>', methods=['PUT'])
def updateEstadoFactura(estado_factura_id):
    data = request.get_json()
    estado_factura_dao = EstadoFacturaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        permite_modificacion = data.get('permite_modificacion', True)
        permite_anulacion = data.get('permite_anulacion', True)
        color = data.get('color', 'secondary')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if estado_factura_dao.updateEstadoFactura(
            estado_factura_id, descripcion, codigo, permite_modificacion, permite_anulacion, color, estado
        ):
            return jsonify({
                'success': True,
                'data': {'id': estado_factura_id, 'descripcion': descripcion, 'codigo': codigo,
                        'permite_modificacion': permite_modificacion, 'permite_anulacion': permite_anulacion,
                        'color': color, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el estado de factura.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@estado_factura_api.route('/estados_factura/<int:estado_factura_id>', methods=['DELETE'])
def deleteEstadoFactura(estado_factura_id):
    estado_factura_dao = EstadoFacturaDao()
    try:
        if estado_factura_dao.deleteEstadoFactura(estado_factura_id):
            return jsonify({'success': True, 'mensaje': f'Estado de factura eliminado correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el estado de factura.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















