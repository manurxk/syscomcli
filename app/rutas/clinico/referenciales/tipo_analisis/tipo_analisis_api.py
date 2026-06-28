from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.tipo_analisis.TipoAnalisisDao import TipoAnalisisDao
from app.auth.utils.decorators import role_required

tipoanalisisapi = Blueprint('tipoanalisisapi', __name__)


@tipoanalisisapi.route('/tipos-analisis', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getTiposAnalisis():
    try:
        data = TipoAnalisisDao().getTiposAnalisis()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de análisis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoanalisisapi.route('/tipos-analisis/<int:tipo_analisis_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getTipoAnalisis(tipo_analisis_id):
    try:
        registro = TipoAnalisisDao().getTipoAnalisisById(tipo_analisis_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de análisis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoanalisisapi.route('/tipos-analisis', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoAnalisis():
    data = request.get_json() or {}
    dao = TipoAnalisisDao()

    descripcion = (data.get('des_tipo_analisis') or '').strip().upper()
    estado = bool(data.get('est_tipo_analisis', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoAnalisisExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarTipoAnalisis(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_analisis': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de análisis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoanalisisapi.route('/tipos-analisis/<int:tipo_analisis_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoAnalisis(tipo_analisis_id):
    data = request.get_json() or {}
    dao = TipoAnalisisDao()

    if not dao.getTipoAnalisisById(tipo_analisis_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_tipo_analisis') or '').strip().upper()
    estado = bool(data.get('est_tipo_analisis', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoAnalisisExiste(descripcion, excluir_id=tipo_analisis_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateTipoAnalisis(tipo_analisis_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_analisis': tipo_analisis_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de análisis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoanalisisapi.route('/tipos-analisis/<int:tipo_analisis_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoAnalisis(tipo_analisis_id):
    dao = TipoAnalisisDao()

    if not dao.getTipoAnalisisById(tipo_analisis_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarTipoAnalisis(tipo_analisis_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {tipo_analisis_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de análisis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
