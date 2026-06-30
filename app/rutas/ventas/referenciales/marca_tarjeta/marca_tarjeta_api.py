from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.marca_tarjeta.MarcaTarjetaDao import MarcaTarjetaDao
from app.auth.utils.decorators import role_required

marcatarjetaapi = Blueprint('marcatarjetaapi', __name__)


@marcatarjetaapi.route('/marcas-tarjeta', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getMarcasTarjeta():
    try:
        return jsonify({'success': True, 'data': MarcaTarjetaDao().getMarcasTarjeta(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener marcas de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@marcatarjetaapi.route('/marcas-tarjeta/<int:id_marca_tarjeta>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getMarcaTarjeta(id_marca_tarjeta):
    try:
        registro = MarcaTarjetaDao().getMarcaTarjetaById(id_marca_tarjeta)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@marcatarjetaapi.route('/marcas-tarjeta', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addMarcaTarjeta():
    data = request.get_json() or {}
    dao = MarcaTarjetaDao()

    descripcion = (data.get('des_marca_tarjeta') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.marcaTarjetaExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe una marca de tarjeta "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarMarcaTarjeta(
            descripcion=descripcion,
            codigo=data.get('cod_marca_tarjeta'),
            estado=bool(data.get('est_marca_tarjeta', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_marca_tarjeta': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@marcatarjetaapi.route('/marcas-tarjeta/<int:id_marca_tarjeta>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateMarcaTarjeta(id_marca_tarjeta):
    data = request.get_json() or {}
    dao = MarcaTarjetaDao()

    if not dao.getMarcaTarjetaById(id_marca_tarjeta):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_marca_tarjeta') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.marcaTarjetaExiste(descripcion, excluir_id=id_marca_tarjeta):
        return jsonify({'success': False, 'error': f'Ya existe una marca de tarjeta "{descripcion}".'}), 400

    try:
        dao.updateMarcaTarjeta(
            id_marca_tarjeta=id_marca_tarjeta,
            descripcion=descripcion,
            codigo=data.get('cod_marca_tarjeta'),
            estado=bool(data.get('est_marca_tarjeta', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_marca_tarjeta': id_marca_tarjeta}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@marcatarjetaapi.route('/marcas-tarjeta/<int:id_marca_tarjeta>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarMarcaTarjeta(id_marca_tarjeta):
    dao = MarcaTarjetaDao()
    if not dao.getMarcaTarjetaById(id_marca_tarjeta):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarMarcaTarjeta(id_marca_tarjeta, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_marca_tarjeta} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar marca de tarjeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
