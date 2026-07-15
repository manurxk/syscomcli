from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.cobranza.CobranzaDao import CobranzaDao
from app.auth.utils.decorators import role_required

cobranzaapi = Blueprint('cobranzaapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@cobranzaapi.route('/cobranzas', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getCobranzas():
    try:
        return jsonify({'success': True, 'data': CobranzaDao().getCobranzas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cobranzas: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cobranzaapi.route('/cobranzas/<int:id_cobranza>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getCobranza(id_cobranza):
    try:
        dao = CobranzaDao()
        reg = dao.getCobranzaById(id_cobranza)
        if not reg:
            return jsonify({'success': False, 'error': 'Cobranza no encontrada.'}), 404
        reg['detalle'] = dao.getCobranzaDetalle(id_cobranza)
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cobranza {id_cobranza}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cobranzaapi.route('/cobranzas', methods=['POST'])
@role_required(*ROLES_VENTAS)
def addCobranza():
    data = request.get_json() or {}

    for campo in ('id_cuenta_cobrar', 'id_factura', 'id_caja'):
        if not data.get(campo):
            return jsonify({'success': False, 'error': f'El campo "{campo}" es obligatorio.'}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'Debe agregar al menos una forma de cobro.'}), 400
    for d in detalles:
        if not d.get('id_forma_cobro'):
            return jsonify({'success': False, 'error': 'Cada línea de detalle requiere una forma de cobro.'}), 400
        if not d.get('monto_cobrado') or int(d['monto_cobrado']) <= 0:
            return jsonify({'success': False, 'error': 'El monto de cada forma de cobro debe ser mayor a 0.'}), 400

    try:
        nuevo_id = CobranzaDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_cobranza': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar cobranza: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cobranzaapi.route('/cobranzas/<int:id_cobranza>/anular', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def anularCobranza(id_cobranza):
    try:
        ok = CobranzaDao().anular(id_cobranza, usuario=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'La cobranza ya está anulada o no se encontró.'}), 409
        return jsonify({'success': True, 'mensaje': f'Cobranza {id_cobranza} anulada.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al anular cobranza {id_cobranza}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
