from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.item_servicio.ItemServicioDao import ItemServicioDao
from app.auth.utils.decorators import role_required

itemservicioapi = Blueprint('itemservicioapi', __name__)


@itemservicioapi.route('/items-servicios', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getItemsServicios():
    try:
        return jsonify({'success': True, 'data': ItemServicioDao().getItemsServicios(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener items de servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemservicioapi.route('/items-servicios/<int:id_item_servicio>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getItemServicio(id_item_servicio):
    try:
        registro = ItemServicioDao().getItemServicioById(id_item_servicio)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener item de servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemservicioapi.route('/items-servicios', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addItemServicio():
    data = request.get_json() or {}
    dao = ItemServicioDao()

    descripcion = (data.get('des_item_servicio') or '').strip().upper()
    id_tipo_item = data.get('id_tipo_item')

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not id_tipo_item:
        return jsonify({'success': False, 'error': 'El tipo de ítem es obligatorio.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.itemServicioExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un ítem con descripción "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarItemServicio(
            descripcion=descripcion,
            id_tipo_item=id_tipo_item,
            codigo=(data.get('cod_item_servicio') or '').strip().upper() or None,
            precio_unitario=float(data.get('item_precio_unitario', 0)),
            id_moneda=data.get('id_moneda') or None,
            aplica_impuesto=bool(data.get('aplica_impuesto', False)),
            id_tipo_impuesto=data.get('id_tipo_impuesto') or None,
            estado=bool(data.get('est_item_servicio', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_item_servicio': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar item de servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemservicioapi.route('/items-servicios/<int:id_item_servicio>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateItemServicio(id_item_servicio):
    data = request.get_json() or {}
    dao = ItemServicioDao()

    if not dao.getItemServicioById(id_item_servicio):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_item_servicio') or '').strip().upper()
    id_tipo_item = data.get('id_tipo_item')

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not id_tipo_item:
        return jsonify({'success': False, 'error': 'El tipo de ítem es obligatorio.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.itemServicioExiste(descripcion, excluir_id=id_item_servicio):
        return jsonify({'success': False, 'error': f'Ya existe un ítem con descripción "{descripcion}".'}), 400

    try:
        dao.updateItemServicio(
            id_item_servicio=id_item_servicio,
            descripcion=descripcion,
            id_tipo_item=id_tipo_item,
            codigo=(data.get('cod_item_servicio') or '').strip().upper() or None,
            precio_unitario=float(data.get('item_precio_unitario', 0)),
            id_moneda=data.get('id_moneda') or None,
            aplica_impuesto=bool(data.get('aplica_impuesto', False)),
            id_tipo_impuesto=data.get('id_tipo_impuesto') or None,
            estado=bool(data.get('est_item_servicio', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_item_servicio': id_item_servicio}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar item de servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@itemservicioapi.route('/items-servicios/<int:id_item_servicio>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarItemServicio(id_item_servicio):
    dao = ItemServicioDao()
    if not dao.getItemServicioById(id_item_servicio):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarItemServicio(id_item_servicio, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Ítem {id_item_servicio} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar item de servicio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
