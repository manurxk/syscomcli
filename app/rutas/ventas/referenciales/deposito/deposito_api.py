from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.deposito.DepositoDao import DepositoDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_caracteres, msg_existe, msg_obligatorio

depositoapi = Blueprint('depositoapi', __name__)

TIPOS_DEPOSITO_VALIDOS = ('BANCO', 'CUENTA_CORRIENTE', 'CAJA_AHORRO', 'BILLETERA_DIGITAL')


@depositoapi.route('/depositos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getDepositos():
    """GET: lista los registros de depósito."""
    try:
        return jsonify({'success': True, 'data': DepositoDao().getDepositos(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depósitos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@depositoapi.route('/depositos/<int:id_deposito>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getDeposito(id_deposito):
    """GET: devuelve depósito por su id; 404 si no existe."""
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
    """POST: valida los datos y registra depósito; devuelve el id nuevo (201)."""
    data = request.get_json() or {}
    dao = DepositoDao()

    descripcion = (data.get('des_deposito') or '').strip().upper()
    tipo_deposito = (data.get('tipo_deposito') or 'BANCO').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios, puntos y guiones')}), 400
    if tipo_deposito not in TIPOS_DEPOSITO_VALIDOS:
        return jsonify({'success': False, 'error': f'El tipo de depósito debe ser uno de: {", ".join(TIPOS_DEPOSITO_VALIDOS)}.'}), 400
    if dao.depositoExiste(descripcion):
        return jsonify({'success': False, 'error': msg_existe('un depósito', descripcion)}), 400

    try:
        nuevo_id = dao.guardarDeposito(
            descripcion=descripcion,
            codigo=data.get('cod_deposito'),
            tipo_deposito=tipo_deposito,
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
    """PUT: valida y actualiza depósito; 404 si no existe."""
    data = request.get_json() or {}
    dao = DepositoDao()

    if not dao.getDepositoById(id_deposito):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_deposito') or '').strip().upper()
    tipo_deposito = (data.get('tipo_deposito') or 'BANCO').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios, puntos y guiones')}), 400
    if tipo_deposito not in TIPOS_DEPOSITO_VALIDOS:
        return jsonify({'success': False, 'error': f'El tipo de depósito debe ser uno de: {", ".join(TIPOS_DEPOSITO_VALIDOS)}.'}), 400
    if dao.depositoExiste(descripcion, excluir_id=id_deposito):
        return jsonify({'success': False, 'error': msg_existe('un depósito', descripcion)}), 400

    try:
        dao.updateDeposito(
            id_deposito=id_deposito,
            descripcion=descripcion,
            codigo=data.get('cod_deposito'),
            tipo_deposito=tipo_deposito,
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
    """DELETE: da de baja (lógica) depósito; 404 si no existe."""
    dao = DepositoDao()
    if not dao.getDepositoById(id_deposito):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarDeposito(id_deposito, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Depósito {id_deposito} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar depósito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
