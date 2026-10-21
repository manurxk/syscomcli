from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.pedido.PedidoDao import PedidoDao
from app.auth.utils.decorators import role_required, permiso_requerido
from app.utils.mensajes_validacion import msg_obligatorio

pedidoapi = Blueprint('pedidoapi', __name__)

ROLES_PEDIDO = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@pedidoapi.route('/pedidos', methods=['GET'])
@role_required(*ROLES_PEDIDO)
@permiso_requerido("VENTAS", "LEER")
def getPedidos():
    """GET: lista los registros de pedido."""
    try:
        return jsonify({'success': True, 'data': PedidoDao().getPedidos(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener pedidos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>', methods=['GET'])
@role_required(*ROLES_PEDIDO)
@permiso_requerido("VENTAS", "LEER")
def getPedido(id_pedido):
    """GET: devuelve pedido por su id; 404 si no existe."""
    try:
        registro = PedidoDao().getPedidoById(id_pedido)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el pedido.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener pedido: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@pedidoapi.route('/pedidos', methods=['POST'])
@role_required(*ROLES_PEDIDO)
@permiso_requerido("VENTAS", "CREAR")
def addPedido():
    """POST: valida los datos y registra pedido; devuelve el id nuevo (201)."""
    data = request.get_json() or {}

    if not data.get('id_paciente'):
        return jsonify({'success': False, 'error': msg_obligatorio('Paciente')}), 400
    if not data.get('fecha_pedido'):
        return jsonify({'success': False, 'error': msg_obligatorio('Fecha del pedido')}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'El pedido debe tener al menos un ítem.'}), 400
    for d in detalles:
        if not d.get('item_descripcion'):
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una descripción.'}), 400
        if not d.get('item_cantidad') or float(d['item_cantidad']) <= 0:
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una cantidad mayor a 0.'}), 400

    try:
        nuevo_id = PedidoDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_pedido': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar pedido: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>/estado', methods=['PUT'])
@role_required(*ROLES_PEDIDO)
@permiso_requerido("VENTAS", "EDITAR")
def updateEstadoPedido(id_pedido):
    """PUT: cambia el estado del pedido."""
    data = request.get_json() or {}
    nuevo_estado = data.get('pedido_estado')
    if nuevo_estado not in ('PENDIENTE', 'CONFIRMADO', 'FACTURADO', 'CANCELADO'):
        return jsonify({'success': False, 'error': 'Estado inválido.'}), 400

    dao = PedidoDao()
    if not dao.getPedidoById(id_pedido):
        return jsonify({'success': False, 'error': 'No se encontró el pedido.'}), 404

    try:
        dao.actualizarEstado(id_pedido, nuevo_estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_pedido': id_pedido}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar estado del pedido: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@pedidoapi.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
@role_required(*ROLES_PEDIDO)
@permiso_requerido("VENTAS", "ELIMINAR")
def deletePedido(id_pedido):
    """DELETE: da de baja el pedido."""
    dao = PedidoDao()
    if not dao.getPedidoById(id_pedido):
        return jsonify({'success': False, 'error': 'No se encontró el pedido.'}), 404
    try:
        dao.desactivar(id_pedido, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Pedido {id_pedido} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar pedido: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
