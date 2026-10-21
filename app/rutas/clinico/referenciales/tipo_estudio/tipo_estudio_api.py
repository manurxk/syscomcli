from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.tipo_estudio.TipoEstudioDao import TipoEstudioDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_caracteres, msg_existe, msg_obligatorio

tipoestudioapi = Blueprint('tipoestudioapi', __name__)


@tipoestudioapi.route('/tipos-estudios', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getTiposEstudios():
    """GET: lista los registros de tipo de estudio."""
    try:
        data = TipoEstudioDao().getTiposEstudios()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipos de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoestudioapi.route('/tipos-estudios/<int:tipo_estudio_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getTipoEstudio(tipo_estudio_id):
    """GET: registro de tipo de estudio por su id; 404 si no existe."""
    try:
        registro = TipoEstudioDao().getTipoEstudioById(tipo_estudio_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tipo de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoestudioapi.route('/tipos-estudios', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addTipoEstudio():
    """POST: valida los datos y crea un registro de tipo de estudio; devuelve el id nuevo (201)."""
    data = request.get_json() or {}
    dao = TipoEstudioDao()

    descripcion = (data.get('des_tipo_estudio') or '').strip().upper()
    estado = bool(data.get('est_tipo_estudio', True))

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios y puntos')}), 400
    if dao.tipoEstudioExiste(descripcion):
        return jsonify({'success': False, 'error': msg_existe('un tipo de estudio', descripcion)}), 400

    try:
        nuevo_id = dao.guardarTipoEstudio(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_estudio': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tipo de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoestudioapi.route('/tipos-estudios/<int:tipo_estudio_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateTipoEstudio(tipo_estudio_id):
    """PUT: valida y actualiza el registro de tipo de estudio; 404 si no existe."""
    data = request.get_json() or {}
    dao = TipoEstudioDao()

    if not dao.getTipoEstudioById(tipo_estudio_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_tipo_estudio') or '').strip().upper()
    estado = bool(data.get('est_tipo_estudio', True))

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios y puntos')}), 400
    if dao.tipoEstudioExiste(descripcion, excluir_id=tipo_estudio_id):
        return jsonify({'success': False, 'error': msg_existe('un tipo de estudio', descripcion)}), 400

    try:
        dao.updateTipoEstudio(tipo_estudio_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tipo_estudio': tipo_estudio_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tipoestudioapi.route('/tipos-estudios/<int:tipo_estudio_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarTipoEstudio(tipo_estudio_id):
    """DELETE: baja lógica del registro de tipo de estudio; 404 si no existe."""
    dao = TipoEstudioDao()

    if not dao.getTipoEstudioById(tipo_estudio_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarTipoEstudio(tipo_estudio_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {tipo_estudio_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar tipo de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
