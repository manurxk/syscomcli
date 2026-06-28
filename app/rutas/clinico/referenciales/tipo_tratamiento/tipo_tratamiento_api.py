from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.tipo_tratamiento.TipoTratamientoDao import TipoTratamientoDao
from app.auth.utils.decorators import role_required

tipotratamientoapi = Blueprint('tipotratamientoapi', __name__)


@tipotratamientoapi.route('/tipos-tratamientos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getTiposTratamientos():
    try:
        data = TipoTratamientoDao().getTiposTratamientos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de tratamiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipotratamientoapi.route('/tipos-tratamientos/<int:tipo_tratamiento_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getTipoTratamiento(tipo_tratamiento_id):
    try:
        registro = TipoTratamientoDao().getTipoTratamientoById(tipo_tratamiento_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de tratamiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipotratamientoapi.route('/tipos-tratamientos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoTratamiento():
    data = request.get_json() or {}
    dao = TipoTratamientoDao()

    descripcion = (data.get('des_tipo_tratamiento') or '').strip().upper()
    estado = bool(data.get('est_tipo_tratamiento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoTratamientoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarTipoTratamiento(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_tratamiento': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de tratamiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipotratamientoapi.route('/tipos-tratamientos/<int:tipo_tratamiento_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoTratamiento(tipo_tratamiento_id):
    data = request.get_json() or {}
    dao = TipoTratamientoDao()

    if not dao.getTipoTratamientoById(tipo_tratamiento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_tipo_tratamiento') or '').strip().upper()
    estado = bool(data.get('est_tipo_tratamiento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.tipoTratamientoExiste(descripcion, excluir_id=tipo_tratamiento_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateTipoTratamiento(tipo_tratamiento_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_tratamiento': tipo_tratamiento_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de tratamiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipotratamientoapi.route('/tipos-tratamientos/<int:tipo_tratamiento_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoTratamiento(tipo_tratamiento_id):
    dao = TipoTratamientoDao()

    if not dao.getTipoTratamientoById(tipo_tratamiento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarTipoTratamiento(tipo_tratamiento_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {tipo_tratamiento_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de tratamiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
