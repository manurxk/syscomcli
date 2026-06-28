from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.instrumento.InstrumentoDao import InstrumentoDao
from app.auth.utils.decorators import role_required

instrumentoapi = Blueprint('instrumentoapi', __name__)


@instrumentoapi.route('/instrumentos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getInstrumentos():
    try:
        data = InstrumentoDao().getInstrumentos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener instrumentos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@instrumentoapi.route('/instrumentos/<int:instrumento_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getInstrumento(instrumento_id):
    try:
        registro = InstrumentoDao().getInstrumentoById(instrumento_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener instrumento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@instrumentoapi.route('/instrumentos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addInstrumento():
    data = request.get_json() or {}
    dao = InstrumentoDao()

    descripcion = (data.get('des_instrumento') or '').strip().upper()
    estado = bool(data.get('est_instrumento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.instrumentoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarInstrumento(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_instrumento': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar instrumento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@instrumentoapi.route('/instrumentos/<int:instrumento_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateInstrumento(instrumento_id):
    data = request.get_json() or {}
    dao = InstrumentoDao()

    if not dao.getInstrumentoById(instrumento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_instrumento') or '').strip().upper()
    estado = bool(data.get('est_instrumento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.instrumentoExiste(descripcion, excluir_id=instrumento_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateInstrumento(instrumento_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_instrumento': instrumento_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar instrumento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@instrumentoapi.route('/instrumentos/<int:instrumento_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarInstrumento(instrumento_id):
    dao = InstrumentoDao()

    if not dao.getInstrumentoById(instrumento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarInstrumento(instrumento_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {instrumento_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar instrumento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
