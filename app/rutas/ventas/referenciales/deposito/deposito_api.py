from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.deposito.DepositoDao import DepositoDao
from app.auth.utils.decorators import role_required

depositoapi = Blueprint('depositoapi', __name__)


@depositoapi.route('/depositos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getDepositos():
    try:
        return jsonify({'success': True, 'data': DepositoDao().getDepositos(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depósitos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@depositoapi.route('/depositos/<int:id_deposito>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getDeposito(id_deposito):
    try:
        registro = DepositoDao().getDepositoById(id_deposito)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@depositoapi.route('/depositos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addDeposito():
    data = request.get_json() or {}
    dao = DepositoDao()

    descripcion = (data.get('des_deposito') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.depositoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un depósito "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarDeposito(
            descripcion=descripcion,
            codigo=data.get('cod_deposito'),
            tipo_deposito=data.get('tipo_deposito', 'BANCO'),
            numero_cuenta=data.get('numero_cuenta'),
            banco=data.get('banco_deposito'),
            ruc_banco=data.get('ruc_banco'),
            moneda=data.get('moneda_deposito', 'PYG'),
            estado=bool(data.get('est_deposito', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_deposito': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@depositoapi.route('/depositos/<int:id_deposito>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateDeposito(id_deposito):
    data = request.get_json() or {}
    dao = DepositoDao()

    if not dao.getDepositoById(id_deposito):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_deposito') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.depositoExiste(descripcion, excluir_id=id_deposito):
        return jsonify({'success': False, 'error': f'Ya existe un depósito "{descripcion}".'}), 400

    try:
        dao.updateDeposito(
            id_deposito=id_deposito,
            descripcion=descripcion,
            codigo=data.get('cod_deposito'),
            tipo_deposito=data.get('tipo_deposito', 'BANCO'),
            numero_cuenta=data.get('numero_cuenta'),
            banco=data.get('banco_deposito'),
            ruc_banco=data.get('ruc_banco'),
            moneda=data.get('moneda_deposito', 'PYG'),
            estado=bool(data.get('est_deposito', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_deposito': id_deposito}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@depositoapi.route('/depositos/<int:id_deposito>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarDeposito(id_deposito):
    dao = DepositoDao()
    if not dao.getDepositoById(id_deposito):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarDeposito(id_deposito, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Depósito {id_deposito} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
