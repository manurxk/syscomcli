from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.deposito.DepositoDao import DepositoDao

deposito_api = Blueprint('deposito_api', __name__)

@deposito_api.route('/depositos', methods=['GET'])
def getDepositos():
    deposito_dao = DepositoDao()
    try:
        depositos = deposito_dao.getDepositos()
        return jsonify({'success': True, 'data': depositos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los depósitos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@deposito_api.route('/depositos/<int:deposito_id>', methods=['GET'])
def getDeposito(deposito_id):
    deposito_dao = DepositoDao()
    try:
        deposito = deposito_dao.getDepositoById(deposito_id)
        if deposito:
            return jsonify({'success': True, 'data': deposito, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el depósito.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@deposito_api.route('/depositos', methods=['POST'])
def addDeposito():
    data = request.get_json()
    deposito_dao = DepositoDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    if 'tipo_deposito' not in data or not data['tipo_deposito']:
        return jsonify({'success': False, 'error': 'El tipo de depósito es obligatorio.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        tipo_deposito = data['tipo_deposito'].upper()
        numero_cuenta = data.get('numero_cuenta', '')
        banco = data.get('banco', '').upper() if data.get('banco') else None
        ruc_banco = data.get('ruc_banco', '')
        moneda = data.get('moneda', 'PYG').upper()
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        deposito_id = deposito_dao.guardarDeposito(
            descripcion, codigo, tipo_deposito, numero_cuenta, banco, ruc_banco, moneda, estado
        )
        if deposito_id:
            return jsonify({
                'success': True,
                'data': {'id': deposito_id, 'descripcion': descripcion, 'codigo': codigo,
                        'tipo_deposito': tipo_deposito, 'numero_cuenta': numero_cuenta,
                        'banco': banco, 'ruc_banco': ruc_banco, 'moneda': moneda, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el depósito.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@deposito_api.route('/depositos/<int:deposito_id>', methods=['PUT'])
def updateDeposito(deposito_id):
    data = request.get_json()
    deposito_dao = DepositoDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    if 'tipo_deposito' not in data or not data['tipo_deposito']:
        return jsonify({'success': False, 'error': 'El tipo de depósito es obligatorio.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        tipo_deposito = data['tipo_deposito'].upper()
        numero_cuenta = data.get('numero_cuenta', '')
        banco = data.get('banco', '').upper() if data.get('banco') else None
        ruc_banco = data.get('ruc_banco', '')
        moneda = data.get('moneda', 'PYG').upper()
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if deposito_dao.updateDeposito(
            deposito_id, descripcion, codigo, tipo_deposito, numero_cuenta, banco, ruc_banco, moneda, estado
        ):
            return jsonify({
                'success': True,
                'data': {'id': deposito_id, 'descripcion': descripcion, 'codigo': codigo,
                        'tipo_deposito': tipo_deposito, 'numero_cuenta': numero_cuenta,
                        'banco': banco, 'ruc_banco': ruc_banco, 'moneda': moneda, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el depósito.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@deposito_api.route('/depositos/<int:deposito_id>', methods=['DELETE'])
def deleteDeposito(deposito_id):
    deposito_dao = DepositoDao()
    try:
        if deposito_dao.deleteDeposito(deposito_id):
            return jsonify({'success': True, 'mensaje': f'Depósito eliminado correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el depósito.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















