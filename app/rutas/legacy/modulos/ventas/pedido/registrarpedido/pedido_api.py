from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.pedido.PedidoDao import PedidoDao
from datetime import datetime

pedidoapi = Blueprint('pedidoapi', __name__)

@pedidoapi.route('/pedidos', methods=['GET'])
def getAllPedidos():
    """Obtiene todos los pedidos"""
    dao = PedidoDao()
    
    try:
        pedidos = dao.getPedidos()
        return jsonify({'success': True, 'data': pedidos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los pedidos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>', methods=['GET'])
def getPedido(id_pedido):
    """Obtiene un pedido específico por su ID con su detalle"""
    dao = PedidoDao()
    
    try:
        pedido = dao.getPedidoById(id_pedido)
        
        if pedido:
            # Obtener detalle
            detalle = dao.getPedidoDetalle(id_pedido)
            pedido['detalle'] = detalle
            
            return jsonify({'success': True, 'data': pedido, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el pedido.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el pedido: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@pedidoapi.route('/pedidos', methods=['POST'])
def addPedido():
    """Crea un nuevo pedido"""
    data = request.get_json()
    dao = PedidoDao()
    
    campos_requeridos = ['id_paciente', 'fecha_pedido']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        pedido_id = dao.guardarPedido(
            id_paciente=data['id_paciente'],
            fecha_pedido=data['fecha_pedido'],
            fecha_entrega=data.get('fecha_entrega'),
            id_profesional=data.get('id_profesional'),
            pedido_subtotal=data.get('pedido_subtotal', 0),
            pedido_descuento=data.get('pedido_descuento', 0),
            pedido_total=data.get('pedido_total', 0),
            observaciones=data.get('observaciones'),
            est_pedido=data.get('est_pedido', 'PENDIENTE'),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if pedido_id:
            return jsonify({
                'success': True,
                'data': {'id_pedido': pedido_id, 'mensaje': 'Pedido creado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear el pedido.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear pedido: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>/detalle', methods=['POST'])
def addPedidoDetalle(id_pedido):
    """Agrega un item al detalle de un pedido"""
    data = request.get_json()
    dao = PedidoDao()
    
    campos_requeridos = ['item_descripcion', 'item_precio_unitario']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarPedidoDetalle(
            id_pedido=id_pedido,
            item_descripcion=data['item_descripcion'],
            item_precio_unitario=int(data['item_precio_unitario']),  # Convertir a entero (guaraníes)
            item_cantidad=data.get('item_cantidad', 1),
            item_descuento=int(data.get('item_descuento', 0)),
            id_tipo_item=data.get('id_tipo_item'),
            id_consulta=data.get('id_consulta'),
            observaciones=data.get('observaciones')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_pedido_detalle': detalle_id, 'mensaje': 'Item agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el item al pedido.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de pedido: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>/detalle/<int:id_detalle>', methods=['PUT'])
def updatePedidoDetalle(id_pedido, id_detalle):
    """Actualiza un item del detalle de pedido"""
    data = request.get_json()
    dao = PedidoDao()
    
    try:
        resultado = dao.updatePedidoDetalle(
            id_pedido_detalle=id_detalle,
            item_descripcion=data.get('item_descripcion'),
            item_cantidad=data.get('item_cantidad'),
            item_precio_unitario=int(data['item_precio_unitario']) if data.get('item_precio_unitario') else None,
            item_descuento=int(data.get('item_descuento', 0)) if data.get('item_descuento') is not None else None,
            id_tipo_item=data.get('id_tipo_item'),
            id_consulta=data.get('id_consulta'),
            observaciones=data.get('observaciones')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Item actualizado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el item.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar detalle de pedido: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>/detalle/<int:id_detalle>', methods=['DELETE'])
def deletePedidoDetalle(id_pedido, id_detalle):
    """Elimina un item del detalle de pedido"""
    dao = PedidoDao()
    
    try:
        resultado = dao.deletePedidoDetalle(id_detalle)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Item eliminado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el item.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al eliminar detalle de pedido: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>', methods=['PUT'])
def updatePedido(id_pedido):
    """Actualiza un pedido existente"""
    data = request.get_json()
    dao = PedidoDao()
    
    try:
        resultado = dao.updatePedido(
            id_pedido=id_pedido,
            fecha_pedido=data.get('fecha_pedido'),
            fecha_entrega=data.get('fecha_entrega'),
            id_profesional=data.get('id_profesional'),
            pedido_descuento=int(data.get('pedido_descuento', 0)) if data.get('pedido_descuento') is not None else None,
            observaciones=data.get('observaciones'),
            est_pedido=data.get('est_pedido'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Pedido actualizado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el pedido.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar pedido: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
def deletePedido(id_pedido):
    """Elimina un pedido y su detalle"""
    dao = PedidoDao()
    
    try:
        resultado = dao.deletePedido(id_pedido)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Pedido eliminado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el pedido.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al eliminar pedido: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ENDPOINTS DE FILTRADO
# ============================================

@pedidoapi.route('/pedidos/paciente/<int:id_paciente>', methods=['GET'])
def getPedidosPorPaciente(id_paciente):
    """Obtiene todos los pedidos de un paciente"""
    dao = PedidoDao()
    
    try:
        pedidos = dao.getPedidosPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': pedidos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener pedidos del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















