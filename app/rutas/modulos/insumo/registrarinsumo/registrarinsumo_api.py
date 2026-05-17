from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.insumo.InsumoDao import InsumoDao

insumoapi = Blueprint('insumoapi', __name__)


# ============================================
# CRUD BÁSICO DE INSUMOS
# ============================================

@insumoapi.route('/insumos', methods=['GET'])
def getAllInsumos():
    """Obtiene la lista completa de insumos activos"""
    dao = InsumoDao()
    
    try:
        insumos = dao.getAllInsumos()
        return jsonify({'success': True, 'data': insumos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los insumos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos/<int:id_insumo>', methods=['GET'])
def getInsumo(id_insumo):
    """Obtiene un insumo específico por su ID"""
    dao = InsumoDao()
    
    try:
        insumo = dao.getInsumoById(id_insumo)
        
        if insumo:
            return jsonify({'success': True, 'data': insumo, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el insumo.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos', methods=['POST'])
def addInsumo():
    """Crea un nuevo insumo"""
    data = request.get_json()
    dao = InsumoDao()
    
    # Validar campos obligatorios
    if 'des_insumo' not in data or not data['des_insumo']:
        return jsonify({
            'success': False,
            'error': 'El campo des_insumo es obligatorio y no puede estar vacío.'
        }), 400
    
    try:
        insumo_id = dao.guardarInsumo(
            des_insumo=data['des_insumo'],
            insumo_unidad_medida=data.get('insumo_unidad_medida', 'UNIDAD'),
            insumo_stock_actual=int(data.get('insumo_stock_actual', 0)),
            insumo_stock_minimo=int(data.get('insumo_stock_minimo', 0)),
            insumo_precio_unitario=int(data['insumo_precio_unitario']) if data.get('insumo_precio_unitario') else None,
            usuario_creacion=data.get('usuario_creacion', 'ADMIN')
        )
        
        if insumo_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_insumo': insumo_id,
                    'mensaje': 'Insumo creado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el insumo. Verifique que no exista uno con el mismo nombre.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar insumo: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@insumoapi.route('/insumos/<int:id_insumo>', methods=['PUT'])
def updateInsumo(id_insumo):
    """Actualiza un insumo existente"""
    data = request.get_json()
    dao = InsumoDao()
    
    # Validar que existe el insumo
    insumo_existente = dao.getInsumoById(id_insumo)
    if not insumo_existente:
        return jsonify({'success': False, 'error': 'No se encontró el insumo.'}), 404
    
    try:
        resultado = dao.updateInsumo(
            id_insumo=id_insumo,
            des_insumo=data.get('des_insumo'),
            insumo_unidad_medida=data.get('insumo_unidad_medida'),
            insumo_stock_actual=int(data['insumo_stock_actual']) if data.get('insumo_stock_actual') is not None else None,
            insumo_stock_minimo=int(data['insumo_stock_minimo']) if data.get('insumo_stock_minimo') is not None else None,
            insumo_precio_unitario=int(data['insumo_precio_unitario']) if data.get('insumo_precio_unitario') else None,
            usuario_modificacion=data.get('usuario_modificacion', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {'id_insumo': id_insumo, 'mensaje': 'Insumo actualizado exitosamente'},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el insumo. Verifique que no exista uno con el mismo nombre.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al actualizar insumo: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@insumoapi.route('/insumos/<int:id_insumo>', methods=['DELETE'])
def deleteInsumo(id_insumo):
    """Elimina lógicamente un insumo"""
    dao = InsumoDao()
    
    try:
        if dao.deleteInsumo(id_insumo):
            return jsonify({
                'success': True,
                'mensaje': f'Insumo con ID {id_insumo} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el insumo o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ENDPOINTS ESPECIALES
# ============================================

@insumoapi.route('/insumos/<int:id_insumo>/stock', methods=['PATCH'])
def actualizarStockInsumo(id_insumo):
    """Actualiza el stock de un insumo (sumar o restar)"""
    data = request.get_json()
    dao = InsumoDao()
    
    cantidad = data.get('cantidad')
    operacion = data.get('operacion', 'SUMAR')  # SUMAR o RESTAR
    
    if cantidad is None:
        return jsonify({
            'success': False,
            'error': 'El campo cantidad es obligatorio.'
        }), 400
    
    if operacion not in ['SUMAR', 'RESTAR']:
        return jsonify({
            'success': False,
            'error': 'La operación debe ser SUMAR o RESTAR.'
        }), 400
    
    try:
        if dao.actualizarStock(id_insumo, int(cantidad), operacion):
            insumo_actualizado = dao.getInsumoById(id_insumo)
            return jsonify({
                'success': True,
                'data': insumo_actualizado,
                'mensaje': f'Stock actualizado exitosamente ({operacion})'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el stock.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar stock: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@insumoapi.route('/insumos/bajo-stock', methods=['GET'])
def getInsumosBajoStock():
    """Obtiene insumos con stock bajo"""
    dao = InsumoDao()
    
    try:
        insumos = dao.getInsumosBajoStock()
        return jsonify({'success': True, 'data': insumos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener insumos bajo stock: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















