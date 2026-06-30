from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.tipo_procedimiento.TipoProcedimientoDao import TipoProcedimientoDao
from app.auth.utils.decorators import role_required

tipoprocedimientoapi = Blueprint('tipoprocedimientoapi', __name__)


@tipoprocedimientoapi.route('/tipos-procedimientos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getTiposProcedimientos():
    try:
        data = TipoProcedimientoDao().getTiposProcedimientos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de procedimiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoprocedimientoapi.route('/tipos-procedimientos/<int:tipo_procedimiento_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getTipoProcedimiento(tipo_procedimiento_id):
    try:
        registro = TipoProcedimientoDao().getTipoProcedimientoById(tipo_procedimiento_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de procedimiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoprocedimientoapi.route('/tipos-procedimientos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoProcedimiento():
    data = request.get_json() or {}
    dao = TipoProcedimientoDao()

    descripcion = (data.get('des_tipo_procedimiento') or '').strip().upper()
    estado = bool(data.get('est_tipo_procedimiento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoProcedimientoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarTipoProcedimiento(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_procedimiento': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de procedimiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoprocedimientoapi.route('/tipos-procedimientos/<int:tipo_procedimiento_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoProcedimiento(tipo_procedimiento_id):
    data = request.get_json() or {}
    dao = TipoProcedimientoDao()

    if not dao.getTipoProcedimientoById(tipo_procedimiento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_tipo_procedimiento') or '').strip().upper()
    estado = bool(data.get('est_tipo_procedimiento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoProcedimientoExiste(descripcion, excluir_id=tipo_procedimiento_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateTipoProcedimiento(tipo_procedimiento_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_procedimiento': tipo_procedimiento_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de procedimiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoprocedimientoapi.route('/tipos-procedimientos/<int:tipo_procedimiento_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoProcedimiento(tipo_procedimiento_id):
    dao = TipoProcedimientoDao()

    if not dao.getTipoProcedimientoById(tipo_procedimiento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarTipoProcedimiento(tipo_procedimiento_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {tipo_procedimiento_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de procedimiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
