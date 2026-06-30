from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.insumo.InsumoDao import InsumoDao
from app.auth.utils.decorators import role_required

insumoapi = Blueprint('insumoapi', __name__)


@insumoapi.route('/insumos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getInsumos():
    try:
        data = InsumoDao().getInsumos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener insumos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos/<int:insumo_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getInsumo(insumo_id):
    try:
        registro = InsumoDao().getInsumoById(insumo_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addInsumo():
    data = request.get_json() or {}
    dao = InsumoDao()

    descripcion = (data.get('des_insumo') or '').strip()
    unidad_medida = (data.get('insumo_unidad_medida') or 'UNIDAD').strip().upper()
    stock_actual = data.get('stock_actual', 0)
    stock_minimo = data.get('stock_minimo', 0)
    precio_unitario = data.get('insumo_precio_unitario')
    estado = bool(data.get('est_insumo', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if dao.insumoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un insumo "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarInsumo(
            descripcion, unidad_medida, stock_actual, stock_minimo, precio_unitario,
            estado, usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_insumo': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos/<int:insumo_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateInsumo(insumo_id):
    data = request.get_json() or {}
    dao = InsumoDao()

    if not dao.getInsumoById(insumo_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_insumo') or '').strip()
    unidad_medida = (data.get('insumo_unidad_medida') or 'UNIDAD').strip().upper()
    stock_actual = data.get('stock_actual', 0)
    stock_minimo = data.get('stock_minimo', 0)
    precio_unitario = data.get('insumo_precio_unitario')
    estado = bool(data.get('est_insumo', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if dao.insumoExiste(descripcion, excluir_id=insumo_id):
        return jsonify({'success': False, 'error': f'Ya existe un insumo "{descripcion}".'}), 400

    try:
        dao.updateInsumo(
            insumo_id, descripcion, unidad_medida, stock_actual, stock_minimo, precio_unitario,
            estado, usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_insumo': insumo_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos/<int:insumo_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarInsumo(insumo_id):
    dao = InsumoDao()

    if not dao.getInsumoById(insumo_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarInsumo(insumo_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Insumo {insumo_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
