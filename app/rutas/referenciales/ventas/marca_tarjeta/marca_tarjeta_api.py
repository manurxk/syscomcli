from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.marca_tarjeta.MarcaTarjetaDao import MarcaTarjetaDao

marca_tarjeta_api = Blueprint('marca_tarjeta_api', __name__)

@marca_tarjeta_api.route('/marcas_tarjeta', methods=['GET'])
def getMarcasTarjeta():
    marca_tarjeta_dao = MarcaTarjetaDao()
    try:
        marcas_tarjeta = marca_tarjeta_dao.getMarcasTarjeta()
        return jsonify({'success': True, 'data': marcas_tarjeta, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las marcas de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@marca_tarjeta_api.route('/marcas_tarjeta/<int:marca_tarjeta_id>', methods=['GET'])
def getMarcaTarjeta(marca_tarjeta_id):
    marca_tarjeta_dao = MarcaTarjetaDao()
    try:
        marca_tarjeta = marca_tarjeta_dao.getMarcaTarjetaById(marca_tarjeta_id)
        if marca_tarjeta:
            return jsonify({'success': True, 'data': marca_tarjeta, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la marca de tarjeta.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@marca_tarjeta_api.route('/marcas_tarjeta', methods=['POST'])
def addMarcaTarjeta():
    data = request.get_json()
    marca_tarjeta_dao = MarcaTarjetaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        marca_tarjeta_id = marca_tarjeta_dao.guardarMarcaTarjeta(descripcion, codigo, estado)
        if marca_tarjeta_id:
            return jsonify({
                'success': True,
                'data': {'id': marca_tarjeta_id, 'descripcion': descripcion, 'codigo': codigo, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la marca de tarjeta.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@marca_tarjeta_api.route('/marcas_tarjeta/<int:marca_tarjeta_id>', methods=['PUT'])
def updateMarcaTarjeta(marca_tarjeta_id):
    data = request.get_json()
    marca_tarjeta_dao = MarcaTarjetaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if marca_tarjeta_dao.updateMarcaTarjeta(marca_tarjeta_id, descripcion, codigo, estado):
            return jsonify({
                'success': True,
                'data': {'id': marca_tarjeta_id, 'descripcion': descripcion, 'codigo': codigo, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar la marca de tarjeta.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@marca_tarjeta_api.route('/marcas_tarjeta/<int:marca_tarjeta_id>', methods=['DELETE'])
def deleteMarcaTarjeta(marca_tarjeta_id):
    marca_tarjeta_dao = MarcaTarjetaDao()
    try:
        if marca_tarjeta_dao.deleteMarcaTarjeta(marca_tarjeta_id):
            return jsonify({'success': True, 'mensaje': f'Marca de tarjeta eliminada correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar la marca de tarjeta.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















