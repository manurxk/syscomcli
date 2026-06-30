from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.tipo_item.TipoItemDao import TipoItemDao
from app.auth.utils.decorators import role_required

tipoitemapi = Blueprint('tipoitemapi', __name__)


@tipoitemapi.route('/tipos-items', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getTiposItems():
    try:
        return jsonify({'success': True, 'data': TipoItemDao().getTiposItems(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de ítems: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoitemapi.route('/tipos-items/<int:id_tipo_item>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getTipoItem(id_tipo_item):
    try:
        registro = TipoItemDao().getTipoItemById(id_tipo_item)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de ítem: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoitemapi.route('/tipos-items', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoItem():
    data = request.get_json() or {}
    dao = TipoItemDao()

    descripcion = (data.get('des_tipo_item') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.tipoItemExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un tipo de ítem "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarTipoItem(
            descripcion=descripcion,
            codigo=data.get('cod_tipo_item'),
            categoria=data.get('tipo_item_categoria'),
            requiere_stock=bool(data.get('requiere_stock', False)),
            estado=bool(data.get('est_tipo_item', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_tipo_item': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de ítem: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoitemapi.route('/tipos-items/<int:id_tipo_item>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoItem(id_tipo_item):
    data = request.get_json() or {}
    dao = TipoItemDao()

    if not dao.getTipoItemById(id_tipo_item):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_tipo_item') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.tipoItemExiste(descripcion, excluir_id=id_tipo_item):
        return jsonify({'success': False, 'error': f'Ya existe un tipo de ítem "{descripcion}".'}), 400

    try:
        dao.updateTipoItem(
            id_tipo_item=id_tipo_item,
            descripcion=descripcion,
            codigo=data.get('cod_tipo_item'),
            categoria=data.get('tipo_item_categoria'),
            requiere_stock=bool(data.get('requiere_stock', False)),
            estado=bool(data.get('est_tipo_item', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_tipo_item': id_tipo_item}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de ítem: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoitemapi.route('/tipos-items/<int:id_tipo_item>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoItem(id_tipo_item):
    dao = TipoItemDao()
    if not dao.getTipoItemById(id_tipo_item):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarTipoItem(id_tipo_item, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_tipo_item} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de ítem: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
