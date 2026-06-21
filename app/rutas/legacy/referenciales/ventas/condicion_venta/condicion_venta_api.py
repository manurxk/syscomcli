from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.condicion_venta.CondicionVentaDao import CondicionVentaDao

condicion_venta_api = Blueprint('condicion_venta_api', __name__)

@condicion_venta_api.route('/condiciones_venta', methods=['GET'])
def getCondicionesVenta():
    condicion_venta_dao = CondicionVentaDao()
    try:
        condiciones_venta = condicion_venta_dao.getCondicionesVenta()
        return jsonify({'success': True, 'data': condiciones_venta, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las condiciones de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@condicion_venta_api.route('/condiciones_venta/<int:condicion_venta_id>', methods=['GET'])
def getCondicionVenta(condicion_venta_id):
    condicion_venta_dao = CondicionVentaDao()
    try:
        condicion_venta = condicion_venta_dao.getCondicionVentaById(condicion_venta_id)
        if condicion_venta:
            return jsonify({'success': True, 'data': condicion_venta, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la condición de venta.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@condicion_venta_api.route('/condiciones_venta', methods=['POST'])
def addCondicionVenta():
    data = request.get_json()
    condicion_venta_dao = CondicionVentaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        dias_credito = int(data.get('dias_credito', 0))
        permite_cuotas = data.get('permite_cuotas', False)
        numero_cuotas_max = int(data.get('numero_cuotas_max', 1))
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        condicion_venta_id = condicion_venta_dao.guardarCondicionVenta(
            descripcion, codigo, dias_credito, permite_cuotas, numero_cuotas_max, estado
        )
        if condicion_venta_id:
            return jsonify({
                'success': True,
                'data': {'id': condicion_venta_id, 'descripcion': descripcion, 'codigo': codigo,
                        'dias_credito': dias_credito, 'permite_cuotas': permite_cuotas,
                        'numero_cuotas_max': numero_cuotas_max, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la condición de venta.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@condicion_venta_api.route('/condiciones_venta/<int:condicion_venta_id>', methods=['PUT'])
def updateCondicionVenta(condicion_venta_id):
    data = request.get_json()
    condicion_venta_dao = CondicionVentaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        dias_credito = int(data.get('dias_credito', 0))
        permite_cuotas = data.get('permite_cuotas', False)
        numero_cuotas_max = int(data.get('numero_cuotas_max', 1))
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if condicion_venta_dao.updateCondicionVenta(
            condicion_venta_id, descripcion, codigo, dias_credito, permite_cuotas, numero_cuotas_max, estado
        ):
            return jsonify({
                'success': True,
                'data': {'id': condicion_venta_id, 'descripcion': descripcion, 'codigo': codigo,
                        'dias_credito': dias_credito, 'permite_cuotas': permite_cuotas,
                        'numero_cuotas_max': numero_cuotas_max, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar la condición de venta.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@condicion_venta_api.route('/condiciones_venta/<int:condicion_venta_id>', methods=['DELETE'])
def deleteCondicionVenta(condicion_venta_id):
    condicion_venta_dao = CondicionVentaDao()
    try:
        if condicion_venta_dao.deleteCondicionVenta(condicion_venta_id):
            return jsonify({'success': True, 'mensaje': f'Condición de venta eliminada correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar la condición de venta.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















