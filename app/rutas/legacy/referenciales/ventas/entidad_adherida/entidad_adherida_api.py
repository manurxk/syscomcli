from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.entidad_adherida.EntidadAdheridaDao import EntidadAdheridaDao

entidad_adherida_api = Blueprint('entidad_adherida_api', __name__)

@entidad_adherida_api.route('/entidades_adheridas', methods=['GET'])
def getEntidadesAdheridas():
    entidad_adherida_dao = EntidadAdheridaDao()
    try:
        entidades_adheridas = entidad_adherida_dao.getEntidadesAdheridas()
        return jsonify({'success': True, 'data': entidades_adheridas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las entidades adheridas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_adherida_api.route('/entidades_adheridas/<int:entidad_adherida_id>', methods=['GET'])
def getEntidadAdherida(entidad_adherida_id):
    entidad_adherida_dao = EntidadAdheridaDao()
    try:
        entidad_adherida = entidad_adherida_dao.getEntidadAdheridaById(entidad_adherida_id)
        if entidad_adherida:
            return jsonify({'success': True, 'data': entidad_adherida, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la entidad adherida.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_adherida_api.route('/entidades_adheridas', methods=['POST'])
def addEntidadAdherida():
    data = request.get_json()
    entidad_adherida_dao = EntidadAdheridaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        ruc = data.get('ruc', '')
        telefono = data.get('telefono', '')
        email = data.get('email', '')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        entidad_adherida_id = entidad_adherida_dao.guardarEntidadAdherida(
            descripcion, codigo, ruc, telefono, email, estado
        )
        if entidad_adherida_id:
            return jsonify({
                'success': True,
                'data': {'id': entidad_adherida_id, 'descripcion': descripcion, 'codigo': codigo,
                        'ruc': ruc, 'telefono': telefono, 'email': email, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la entidad adherida.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_adherida_api.route('/entidades_adheridas/<int:entidad_adherida_id>', methods=['PUT'])
def updateEntidadAdherida(entidad_adherida_id):
    data = request.get_json()
    entidad_adherida_dao = EntidadAdheridaDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        ruc = data.get('ruc', '')
        telefono = data.get('telefono', '')
        email = data.get('email', '')
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if entidad_adherida_dao.updateEntidadAdherida(
            entidad_adherida_id, descripcion, codigo, ruc, telefono, email, estado
        ):
            return jsonify({
                'success': True,
                'data': {'id': entidad_adherida_id, 'descripcion': descripcion, 'codigo': codigo,
                        'ruc': ruc, 'telefono': telefono, 'email': email, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar la entidad adherida.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_adherida_api.route('/entidades_adheridas/<int:entidad_adherida_id>', methods=['DELETE'])
def deleteEntidadAdherida(entidad_adherida_id):
    entidad_adherida_dao = EntidadAdheridaDao()
    try:
        if entidad_adherida_dao.deleteEntidadAdherida(entidad_adherida_id):
            return jsonify({'success': True, 'mensaje': f'Entidad adherida eliminada correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar la entidad adherida.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















