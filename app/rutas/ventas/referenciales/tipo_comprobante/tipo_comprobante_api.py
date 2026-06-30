from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.tipo_comprobante.TipoComprobanteDao import TipoComprobanteDao
from app.auth.utils.decorators import role_required

tipocomprobanteapi = Blueprint('tipocomprobanteapi', __name__)


@tipocomprobanteapi.route('/tipos-comprobantes', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getTiposComprobantes():
    try:
        return jsonify({'success': True, 'data': TipoComprobanteDao().getTiposComprobantes(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de comprobantes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocomprobanteapi.route('/tipos-comprobantes/<int:id_tipo_comprobante>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getTipoComprobante(id_tipo_comprobante):
    try:
        registro = TipoComprobanteDao().getTipoComprobanteById(id_tipo_comprobante)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocomprobanteapi.route('/tipos-comprobantes', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoComprobante():
    data = request.get_json() or {}
    dao = TipoComprobanteDao()

    descripcion = (data.get('des_tipo_comprobante') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.tipoComprobanteExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un tipo de comprobante "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarTipoComprobante(
            descripcion=descripcion,
            codigo=data.get('cod_tipo_comprobante'),
            codigo_sifen=data.get('codigo_sifen'),
            requiere_timbrado=bool(data.get('requiere_timbrado', True)),
            tipo_documento=data.get('tipo_documento'),
            estado=bool(data.get('est_tipo_comprobante', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_tipo_comprobante': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocomprobanteapi.route('/tipos-comprobantes/<int:id_tipo_comprobante>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoComprobante(id_tipo_comprobante):
    data = request.get_json() or {}
    dao = TipoComprobanteDao()

    if not dao.getTipoComprobanteById(id_tipo_comprobante):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_tipo_comprobante') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.tipoComprobanteExiste(descripcion, excluir_id=id_tipo_comprobante):
        return jsonify({'success': False, 'error': f'Ya existe un tipo de comprobante "{descripcion}".'}), 400

    try:
        dao.updateTipoComprobante(
            id_tipo_comprobante=id_tipo_comprobante,
            descripcion=descripcion,
            codigo=data.get('cod_tipo_comprobante'),
            codigo_sifen=data.get('codigo_sifen'),
            requiere_timbrado=bool(data.get('requiere_timbrado', True)),
            tipo_documento=data.get('tipo_documento'),
            estado=bool(data.get('est_tipo_comprobante', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_tipo_comprobante': id_tipo_comprobante}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipocomprobanteapi.route('/tipos-comprobantes/<int:id_tipo_comprobante>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoComprobante(id_tipo_comprobante):
    dao = TipoComprobanteDao()
    if not dao.getTipoComprobanteById(id_tipo_comprobante):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarTipoComprobante(id_tipo_comprobante, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_tipo_comprobante} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de comprobante: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
