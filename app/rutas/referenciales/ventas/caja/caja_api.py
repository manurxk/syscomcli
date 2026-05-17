from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.caja.CajaDao import CajaDao

caja_api = Blueprint('caja_api', __name__)

@caja_api.route('/cajas', methods=['GET'])
def getCajas():
    caja_dao = CajaDao()
    try:
        cajas = caja_dao.getCajas()
        return jsonify({'success': True, 'data': cajas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las cajas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@caja_api.route('/cajas/<int:caja_id>', methods=['GET'])
def getCaja(caja_id):
    caja_dao = CajaDao()
    try:
        caja = caja_dao.getCajaById(caja_id)
        if caja:
            return jsonify({'success': True, 'data': caja, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la caja.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@caja_api.route('/cajas', methods=['POST'])
def addCaja():
    data = request.get_json()
    caja_dao = CajaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        saldo_inicial = int(data.get('saldo_inicial', 0))
        estado_caja = data.get('estado_caja', 'CERRADA')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        if estado_caja not in ['ABIERTA', 'CERRADA']:
            return jsonify({'success': False, 'error': 'El estado de caja debe ser "ABIERTA" o "CERRADA".'}), 400
        
        caja_id = caja_dao.guardarCaja(descripcion, codigo, saldo_inicial, estado_caja, estado)
        if caja_id:
            return jsonify({
                'success': True,
                'data': {'id': caja_id, 'descripcion': descripcion, 'codigo': codigo,
                        'saldo_inicial': saldo_inicial, 'saldo_actual': saldo_inicial,
                        'estado_caja': estado_caja, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la caja.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@caja_api.route('/cajas/<int:caja_id>', methods=['PUT'])
def updateCaja(caja_id):
    data = request.get_json()
    caja_dao = CajaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        saldo_inicial = data.get('saldo_inicial')
        estado_caja = data.get('estado_caja')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        if estado_caja and estado_caja not in ['ABIERTA', 'CERRADA']:
            return jsonify({'success': False, 'error': 'El estado de caja debe ser "ABIERTA" o "CERRADA".'}), 400
        
        if saldo_inicial is not None:
            saldo_inicial = int(saldo_inicial)
        
        if caja_dao.updateCaja(caja_id, descripcion, codigo, saldo_inicial, estado_caja, estado):
            return jsonify({
                'success': True,
                'data': {'id': caja_id, 'descripcion': descripcion, 'codigo': codigo,
                        'saldo_inicial': saldo_inicial, 'estado_caja': estado_caja, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar la caja.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@caja_api.route('/cajas/<int:caja_id>', methods=['DELETE'])
def deleteCaja(caja_id):
    caja_dao = CajaDao()
    try:
        if caja_dao.deleteCaja(caja_id):
            return jsonify({'success': True, 'mensaje': f'Caja eliminada correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar la caja.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















