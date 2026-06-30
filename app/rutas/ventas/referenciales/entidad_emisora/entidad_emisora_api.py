from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.entidad_emisora.EntidadEmisoraDao import EntidadEmisoraDao
from app.auth.utils.decorators import role_required

entidademisoraapi = Blueprint('entidademisoraapi', __name__)


@entidademisoraapi.route('/entidades-emisoras', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getEntidadesEmisoras():
    try:
        return jsonify({'success': True, 'data': EntidadEmisoraDao().getEntidadesEmisoras(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener entidades emisoras: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidademisoraapi.route('/entidades-emisoras/<int:id_entidad_emisora>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getEntidadEmisora(id_entidad_emisora):
    try:
        registro = EntidadEmisoraDao().getEntidadEmisoraById(id_entidad_emisora)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidademisoraapi.route('/entidades-emisoras', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addEntidadEmisora():
    data = request.get_json() or {}
    dao = EntidadEmisoraDao()

    descripcion = (data.get('des_entidad_emisora') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.entidadEmisoraExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe una entidad emisora "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarEntidadEmisora(
            descripcion=descripcion,
            codigo=data.get('cod_entidad_emisora'),
            ruc=data.get('ruc_entidad'),
            telefono=data.get('telefono_entidad'),
            email=data.get('email_entidad'),
            tipo_entidad=data.get('tipo_entidad'),
            estado=bool(data.get('est_entidad_emisora', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_entidad_emisora': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidademisoraapi.route('/entidades-emisoras/<int:id_entidad_emisora>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateEntidadEmisora(id_entidad_emisora):
    data = request.get_json() or {}
    dao = EntidadEmisoraDao()

    if not dao.getEntidadEmisoraById(id_entidad_emisora):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_entidad_emisora') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.entidadEmisoraExiste(descripcion, excluir_id=id_entidad_emisora):
        return jsonify({'success': False, 'error': f'Ya existe una entidad emisora "{descripcion}".'}), 400

    try:
        dao.updateEntidadEmisora(
            id_entidad_emisora=id_entidad_emisora,
            descripcion=descripcion,
            codigo=data.get('cod_entidad_emisora'),
            ruc=data.get('ruc_entidad'),
            telefono=data.get('telefono_entidad'),
            email=data.get('email_entidad'),
            tipo_entidad=data.get('tipo_entidad'),
            estado=bool(data.get('est_entidad_emisora', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_entidad_emisora': id_entidad_emisora}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidademisoraapi.route('/entidades-emisoras/<int:id_entidad_emisora>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarEntidadEmisora(id_entidad_emisora):
    dao = EntidadEmisoraDao()
    if not dao.getEntidadEmisoraById(id_entidad_emisora):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarEntidadEmisora(id_entidad_emisora, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_entidad_emisora} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar entidad emisora: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
