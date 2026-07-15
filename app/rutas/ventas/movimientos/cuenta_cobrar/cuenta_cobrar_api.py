from flask import Blueprint, jsonify, current_app as app

from app.dao.ventas.movimientos.cuenta_cobrar.CuentaCobrarDao import CuentaCobrarDao
from app.dao.ventas.movimientos.cobranza.CobranzaDao import CobranzaDao
from app.auth.utils.decorators import role_required

cuentacobrarapi = Blueprint('cuentacobrarapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@cuentacobrarapi.route('/cuentas-cobrar', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getCuentasCobrar():
    try:
        return jsonify({'success': True, 'data': CuentaCobrarDao().getCuentasCobrar(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cuentas a cobrar: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cuentacobrarapi.route('/cuentas-cobrar/pendientes', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getCuentasCobrarPendientes():
    try:
        return jsonify({'success': True, 'data': CuentaCobrarDao().getCuentasCobrarPendientes(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cuentas a cobrar pendientes: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cuentacobrarapi.route('/cuentas-cobrar/<int:id_cuenta_cobrar>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getCuentaCobrar(id_cuenta_cobrar):
    try:
        dao = CuentaCobrarDao()
        reg = dao.getCuentaCobrarById(id_cuenta_cobrar)
        if not reg:
            return jsonify({'success': False, 'error': 'Cuenta a cobrar no encontrada.'}), 404
        reg['cobranzas'] = CobranzaDao().getCobranzasPorCuenta(id_cuenta_cobrar)
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cuenta a cobrar {id_cuenta_cobrar}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
