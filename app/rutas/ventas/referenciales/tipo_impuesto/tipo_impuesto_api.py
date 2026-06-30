from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.tipo_impuesto.TipoImpuestoDao import TipoImpuestoDao
from app.auth.utils.decorators import role_required

tipoimpuestoapi = Blueprint('tipoimpuestoapi', __name__)


@tipoimpuestoapi.route('/tipos-impuestos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getTiposImpuestos():
    try:
        return jsonify({'success': True, 'data': TipoImpuestoDao().getTiposImpuestos(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de impuestos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoimpuestoapi.route('/tipos-impuestos/<int:id_tipo_impuesto>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getTipoImpuesto(id_tipo_impuesto):
    try:
        registro = TipoImpuestoDao().getTipoImpuestoById(id_tipo_impuesto)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoimpuestoapi.route('/tipos-impuestos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoImpuesto():
    data = request.get_json() or {}
    dao = TipoImpuestoDao()

    descripcion = (data.get('des_tipo_impuesto') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.tipoImpuestoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un tipo de impuesto "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarTipoImpuesto(
            descripcion=descripcion,
            codigo=data.get('cod_tipo_impuesto'),
            porcentaje=float(data.get('porcentaje_impuesto', 0)),
            tipo_calculo=data.get('tipo_calculo', 'PORCENTAJE'),
            estado=bool(data.get('est_tipo_impuesto', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_tipo_impuesto': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoimpuestoapi.route('/tipos-impuestos/<int:id_tipo_impuesto>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoImpuesto(id_tipo_impuesto):
    data = request.get_json() or {}
    dao = TipoImpuestoDao()

    if not dao.getTipoImpuestoById(id_tipo_impuesto):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_tipo_impuesto') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.tipoImpuestoExiste(descripcion, excluir_id=id_tipo_impuesto):
        return jsonify({'success': False, 'error': f'Ya existe un tipo de impuesto "{descripcion}".'}), 400

    try:
        dao.updateTipoImpuesto(
            id_tipo_impuesto=id_tipo_impuesto,
            descripcion=descripcion,
            codigo=data.get('cod_tipo_impuesto'),
            porcentaje=float(data.get('porcentaje_impuesto', 0)),
            tipo_calculo=data.get('tipo_calculo', 'PORCENTAJE'),
            estado=bool(data.get('est_tipo_impuesto', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_tipo_impuesto': id_tipo_impuesto}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoimpuestoapi.route('/tipos-impuestos/<int:id_tipo_impuesto>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoImpuesto(id_tipo_impuesto):
    dao = TipoImpuestoDao()
    if not dao.getTipoImpuestoById(id_tipo_impuesto):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarTipoImpuesto(id_tipo_impuesto, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_tipo_impuesto} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de impuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
