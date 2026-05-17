from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.entidad_emisora.EntidadEmisoraDao import EntidadEmisoraDao

entidad_emisora_api = Blueprint('entidad_emisora_api', __name__)

@entidad_emisora_api.route('/entidades_emisoras', methods=['GET'])
def getEntidadesEmisoras():
    entidad_emisora_dao = EntidadEmisoraDao()
    try:
        entidades_emisoras = entidad_emisora_dao.getEntidadesEmisoras()
        return jsonify({'success': True, 'data': entidades_emisoras, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las entidades emisoras: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_emisora_api.route('/entidades_emisoras/<int:entidad_emisora_id>', methods=['GET'])
def getEntidadEmisora(entidad_emisora_id):
    entidad_emisora_dao = EntidadEmisoraDao()
    try:
        entidad_emisora = entidad_emisora_dao.getEntidadEmisoraById(entidad_emisora_id)
        if entidad_emisora:
            return jsonify({'success': True, 'data': entidad_emisora, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la entidad emisora.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_emisora_api.route('/entidades_emisoras', methods=['POST'])
def addEntidadEmisora():
    data = request.get_json()
    entidad_emisora_dao = EntidadEmisoraDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        ruc = data.get('ruc', '')
        telefono = data.get('telefono', '')
        email = data.get('email', '')
        tipo_entidad = data.get('tipo_entidad', '').upper() if data.get('tipo_entidad') else None
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        entidad_emisora_id = entidad_emisora_dao.guardarEntidadEmisora(
            descripcion, codigo, ruc, telefono, email, tipo_entidad, estado
        )
        if entidad_emisora_id:
            return jsonify({
                'success': True,
                'data': {'id': entidad_emisora_id, 'descripcion': descripcion, 'codigo': codigo,
                        'ruc': ruc, 'telefono': telefono, 'email': email, 'tipo_entidad': tipo_entidad, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la entidad emisora.'}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_emisora_api.route('/entidades_emisoras/<int:entidad_emisora_id>', methods=['PUT'])
def updateEntidadEmisora(entidad_emisora_id):
    data = request.get_json()
    entidad_emisora_dao = EntidadEmisoraDao()
    
    if 'descripcion' not in data or not data['descripcion']:
        return jsonify({'success': False, 'error': 'La descripción es obligatoria.'}), 400
    
    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        ruc = data.get('ruc', '')
        telefono = data.get('telefono', '')
        email = data.get('email', '')
        tipo_entidad = data.get('tipo_entidad', '').upper() if data.get('tipo_entidad') else None
        estado = data.get('estado', 'A')
        
        if estado not in ['A', 'I']:
            return jsonify({'success': False, 'error': 'El estado debe ser "A" o "I".'}), 400
        
        if entidad_emisora_dao.updateEntidadEmisora(
            entidad_emisora_id, descripcion, codigo, ruc, telefono, email, tipo_entidad, estado
        ):
            return jsonify({
                'success': True,
                'data': {'id': entidad_emisora_id, 'descripcion': descripcion, 'codigo': codigo,
                        'ruc': ruc, 'telefono': telefono, 'email': email, 'tipo_entidad': tipo_entidad, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar la entidad emisora.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@entidad_emisora_api.route('/entidades_emisoras/<int:entidad_emisora_id>', methods=['DELETE'])
def deleteEntidadEmisora(entidad_emisora_id):
    entidad_emisora_dao = EntidadEmisoraDao()
    try:
        if entidad_emisora_dao.deleteEntidadEmisora(entidad_emisora_id):
            return jsonify({'success': True, 'mensaje': f'Entidad emisora eliminada correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar la entidad emisora.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















