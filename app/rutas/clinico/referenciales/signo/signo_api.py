from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.signo.SignoDao import SignoDao
from app.auth.utils.decorators import role_required

signoapi = Blueprint('signoapi', __name__)


@signoapi.route('/signos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getSignos():
    try:
        data = SignoDao().getSignos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener signos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@signoapi.route('/signos/<int:signo_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getSigno(signo_id):
    try:
        registro = SignoDao().getSignoById(signo_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener signo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@signoapi.route('/signos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addSigno():
    data = request.get_json() or {}
    dao = SignoDao()

    descripcion = (data.get('des_signo') or '').strip().upper()
    estado = bool(data.get('est_signo', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.signoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarSigno(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_signo': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar signo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@signoapi.route('/signos/<int:signo_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateSigno(signo_id):
    data = request.get_json() or {}
    dao = SignoDao()

    if not dao.getSignoById(signo_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_signo') or '').strip().upper()
    estado = bool(data.get('est_signo', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.signoExiste(descripcion, excluir_id=signo_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateSigno(signo_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_signo': signo_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar signo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@signoapi.route('/signos/<int:signo_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarSigno(signo_id):
    dao = SignoDao()

    if not dao.getSignoById(signo_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarSigno(signo_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {signo_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar signo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
