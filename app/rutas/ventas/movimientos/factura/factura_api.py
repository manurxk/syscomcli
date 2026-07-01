from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.factura.FacturaDao import FacturaDao
from app.dao.ventas.movimientos.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao
from app.auth.utils.decorators import role_required

facturaapi = Blueprint('facturaapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@facturaapi.route('/facturas', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getFacturas():
    try:
        return jsonify({'success': True, 'data': FacturaDao().getFacturas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener facturas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas/<int:id_factura>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getFactura(id_factura):
    try:
        dao = FacturaDao()
        reg = dao.getFacturaById(id_factura)
        if not reg:
            return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
        detalle = dao.getFacturaDetalle(id_factura)
        reg['detalle'] = detalle
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas/<int:id_factura>/detalle', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getFacturaDetalle(id_factura):
    try:
        return jsonify({'success': True, 'data': FacturaDao().getFacturaDetalle(id_factura), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener detalle de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas', methods=['POST'])
@role_required(*ROLES_VENTAS)
def addFactura():
    data = request.get_json() or {}

    # Validaciones básicas
    obligatorios = ['id_paciente', 'id_tipo_comprobante', 'id_condicion_venta',
                    'id_timbrado', 'id_punto_expedicion', 'id_estado_factura', 'fecha_factura']
    for campo in obligatorios:
        if not data.get(campo):
            return jsonify({'success': False, 'error': f'El campo "{campo}" es obligatorio.'}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La factura debe tener al menos un ítem en el detalle.'}), 400
    for d in detalles:
        if not d.get('item_descripcion'):
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una descripción.'}), 400
        if not d.get('item_cantidad') or int(d['item_cantidad']) <= 0:
            return jsonify({'success': False, 'error': 'La cantidad de cada ítem debe ser mayor a 0.'}), 400
        if d.get('item_precio_con_iva') is None or float(d['item_precio_con_iva']) < 0:
            return jsonify({'success': False, 'error': 'El precio de cada ítem es obligatorio.'}), 400

    # Verificar caja abierta si se provee id_caja
    id_caja = data.get('id_caja')
    if id_caja:
        apertura = AperturaCierreCajaDao().getAperturaActivaPorCaja(id_caja)
        if not apertura:
            return jsonify({'success': False, 'error': 'La caja seleccionada no tiene una apertura activa.'}), 400

    try:
        nuevo_id = FacturaDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_factura': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar factura: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas/<int:id_factura>/anular', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def anularFactura(id_factura):
    dao = FacturaDao()
    if not dao.getFacturaById(id_factura):
        return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
    try:
        ok = dao.anular(id_factura, usuario_anulacion=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'La factura ya está anulada o no se pudo anular.'}), 409
        return jsonify({'success': True, 'mensaje': f'Factura {id_factura} anulada.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al anular factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
