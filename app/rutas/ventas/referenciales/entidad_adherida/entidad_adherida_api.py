from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.entidad_adherida.EntidadAdheridaDao import EntidadAdheridaDao
from app.auth.utils.decorators import role_required

entidadadheridaapi = Blueprint('entidadadheridaapi', __name__)


@entidadadheridaapi.route('/entidades-adheridas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getEntidadesAdheridas():
    try:
        return jsonify({'success': True, 'data': EntidadAdheridaDao().getEntidadesAdheridas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener entidades adheridas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidadadheridaapi.route('/entidades-adheridas/<int:id_entidad_adherida>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getEntidadAdherida(id_entidad_adherida):
    try:
        registro = EntidadAdheridaDao().getEntidadAdheridaById(id_entidad_adherida)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidadadheridaapi.route('/entidades-adheridas', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addEntidadAdherida():
    data = request.get_json() or {}
    dao = EntidadAdheridaDao()

    descripcion = (data.get('des_entidad_adherida') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.entidadAdheridaExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe una entidad adherida "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarEntidadAdherida(
            descripcion=descripcion,
            codigo=data.get('cod_entidad_adherida'),
            ruc=data.get('ruc_entidad'),
            telefono=data.get('telefono_entidad'),
            email=data.get('email_entidad'),
            estado=bool(data.get('est_entidad_adherida', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_entidad_adherida': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidadadheridaapi.route('/entidades-adheridas/<int:id_entidad_adherida>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateEntidadAdherida(id_entidad_adherida):
    data = request.get_json() or {}
    dao = EntidadAdheridaDao()

    if not dao.getEntidadAdheridaById(id_entidad_adherida):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_entidad_adherida') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.entidadAdheridaExiste(descripcion, excluir_id=id_entidad_adherida):
        return jsonify({'success': False, 'error': f'Ya existe una entidad adherida "{descripcion}".'}), 400

    try:
        dao.updateEntidadAdherida(
            id_entidad_adherida=id_entidad_adherida,
            descripcion=descripcion,
            codigo=data.get('cod_entidad_adherida'),
            ruc=data.get('ruc_entidad'),
            telefono=data.get('telefono_entidad'),
            email=data.get('email_entidad'),
            estado=bool(data.get('est_entidad_adherida', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_entidad_adherida': id_entidad_adherida}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@entidadadheridaapi.route('/entidades-adheridas/<int:id_entidad_adherida>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarEntidadAdherida(id_entidad_adherida):
    dao = EntidadAdheridaDao()
    if not dao.getEntidadAdheridaById(id_entidad_adherida):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarEntidadAdherida(id_entidad_adherida, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_entidad_adherida} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar entidad adherida: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
