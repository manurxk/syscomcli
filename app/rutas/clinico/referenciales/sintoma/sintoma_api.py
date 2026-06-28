from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.sintoma.SintomaDao import SintomaDao
from app.auth.utils.decorators import role_required

sintomaapi = Blueprint('sintomaapi', __name__)


@sintomaapi.route('/sintomas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getSintomas():
    try:
        data = SintomaDao().getSintomas()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener síntomas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sintomaapi.route('/sintomas/<int:sintoma_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getSintoma(sintoma_id):
    try:
        registro = SintomaDao().getSintomaById(sintoma_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener síntoma: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sintomaapi.route('/sintomas', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addSintoma():
    data = request.get_json() or {}
    dao = SintomaDao()

    descripcion = (data.get('des_sintoma') or '').strip().upper()
    estado = bool(data.get('est_sintoma', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.sintomaExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarSintoma(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_sintoma': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar síntoma: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sintomaapi.route('/sintomas/<int:sintoma_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateSintoma(sintoma_id):
    data = request.get_json() or {}
    dao = SintomaDao()

    if not dao.getSintomaById(sintoma_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_sintoma') or '').strip().upper()
    estado = bool(data.get('est_sintoma', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.sintomaExiste(descripcion, excluir_id=sintoma_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateSintoma(sintoma_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_sintoma': sintoma_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar síntoma: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sintomaapi.route('/sintomas/<int:sintoma_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarSintoma(sintoma_id):
    dao = SintomaDao()

    if not dao.getSintomaById(sintoma_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarSintoma(sintoma_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {sintoma_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar síntoma: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
