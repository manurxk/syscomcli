from flask import Blueprint, request, jsonify, current_app as app, session, send_file

from app.dao.ventas.movimientos.factura.FacturaDao import FacturaDao
from app.dao.ventas.movimientos.factura.FacturaBorradorDao import FacturaBorradorDao
from app.dao.ventas.movimientos.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao
from app.services.factura_pdf_service import FacturaPDFService
from app.services.EmailService import EmailService
from app.auth.utils.decorators import role_required, permiso_requerido
from app.utils.mensajes_validacion import msg_obligatorio

facturaapi = Blueprint('facturaapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "VENTAS")


def _construir_pdf_factura(id_factura):
    """Arma el PDF de una factura. Devuelve (factura, buffer) o (None, None) si no existe."""
    dao = FacturaDao()
    factura = dao.getFacturaById(id_factura)
    if not factura:
        return None, None
    detalle = dao.getFacturaDetalle(id_factura)

    config_empresa = FacturaPDFService.config_empresa()

    factura_data = dict(factura)
    factura_data['ruc_emisor'] = config_empresa['ruc']
    factura_data['condicion_venta'] = factura.get('des_condicion_venta', 'Contado')
    factura_data['moneda'] = factura.get('cod_moneda', 'PYG')
    # Documento del receptor a mostrar en el KuDE: RUC (con DV) si el paciente lo tiene, sino cédula
    if factura.get('paciente_tipo_documento') == 'RUC' and factura.get('paciente_ruc'):
        factura_data['paciente_cedula'] = factura['paciente_ruc']

    buffer = FacturaPDFService().generar_factura_pdf(factura_data, detalle, config_empresa)
    return factura, buffer


def _enviar_factura_por_correo(id_factura):
    """Envía el PDF de la factura al correo del paciente. No lanza excepción:
    un fallo de envío no debe interrumpir el flujo de facturación/timbrado."""
    try:
        factura, buffer = _construir_pdf_factura(id_factura)
        if not factura:
            return (False, 'No se encontró la factura.')
        if not factura.get('paciente_correo'):
            app.logger.warning(f"Factura {id_factura}: no se envió por correo, el paciente no tiene correo registrado.")
            return (False, 'El paciente no tiene correo registrado.')

        success, error, _tipo_error = EmailService().enviar_factura(
            correo_destino=factura['paciente_correo'],
            numero_factura=factura['factura_numero'],
            nombre_cliente=factura['paciente_nombre'],
            monto_total=factura['factura_total_letras'] or factura['factura_total'],
            pdf_bytes=buffer.getvalue(),
        )
        return (success, error)
    except Exception as e:
        app.logger.error(f"Error al enviar factura {id_factura} por correo: {str(e)}", exc_info=True)
        return (False, 'Ocurrió un error interno al enviar el correo.')


@facturaapi.route('/facturas', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getFacturas():
    """GET: lista los registros de factura."""
    try:
        return jsonify({'success': True, 'data': FacturaDao().getFacturas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener facturas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas/<int:id_factura>', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getFactura(id_factura):
    """GET: devuelve factura por su id; 404 si no existe."""
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
@permiso_requerido("VENTAS", "LEER")
def getFacturaDetalle(id_factura):
    """GET: líneas de detalle de la factura."""
    try:
        return jsonify({'success': True, 'data': FacturaDao().getFacturaDetalle(id_factura), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener detalle de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas', methods=['POST'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def addFactura():
    """POST: valida los datos y registra factura; devuelve el id nuevo (201)."""
    data = request.get_json() or {}

    # Validaciones básicas
    obligatorios = ['id_paciente', 'id_tipo_comprobante', 'id_condicion_venta',
                    'id_timbrado', 'id_punto_expedicion', 'id_estado_factura', 'fecha_factura']
    for campo in obligatorios:
        if not data.get(campo):
            return jsonify({'success': False, 'error': msg_obligatorio(campo)}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La factura debe tener al menos un ítem en el detalle.'}), 400
    for d in detalles:
        if not d.get('item_descripcion'):
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una descripción.'}), 400
        if not d.get('item_cantidad') or int(d['item_cantidad']) <= 0:
            return jsonify({'success': False, 'error': 'La cantidad de cada ítem debe ser mayor a 0.'}), 400
        if d.get('item_precio_con_iva') is None or float(d['item_precio_con_iva']) < 0:
            return jsonify({'success': False, 'error': msg_obligatorio('Precio de cada ítem')}), 400

    # Factura al contado: se cobra en el acto, así que la caja del cobro debe estar abierta
    id_caja = (data.get('cobro') or {}).get('id_caja')
    if id_caja:
        apertura = AperturaCierreCajaDao().getAperturaActivaPorCaja(id_caja)
        if not apertura:
            return jsonify({'success': False, 'error': 'La caja elegida no está abierta. Ábrala en Estado de Caja antes de facturar al contado.'}), 400

    try:
        nuevo_id = FacturaDao().guardar(data, usuario_creacion=session.get('id_usuario'))

        # Si venía de un borrador, ya cumplió su función: se elimina
        if data.get('id_factura_borrador'):
            try:
                FacturaBorradorDao().eliminarBorrador(int(data['id_factura_borrador']))
            except Exception as e:
                app.logger.warning(f"Factura {nuevo_id} emitida, pero no se pudo eliminar el borrador {data['id_factura_borrador']}: {e}")

        envio_correo_ok, envio_correo_error = _enviar_factura_por_correo(nuevo_id)
        if not envio_correo_ok:
            app.logger.warning(f"Factura {nuevo_id} timbrada, pero no se pudo enviar por correo: {envio_correo_error}")

        return jsonify({'success': True, 'data': {'id_factura': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar factura: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ── Borradores de factura ──────────────────────────────────────────────────
@facturaapi.route('/facturas-borrador', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def getFacturasBorrador():
    """GET: lista los borradores de factura pendientes."""
    try:
        return jsonify({'success': True, 'data': FacturaBorradorDao().getBorradores(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al listar borradores de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas-borrador/<int:id_borrador>', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def getFacturaBorrador(id_borrador):
    """GET: devuelve el contenido de un borrador; 404 si no existe."""
    try:
        reg = FacturaBorradorDao().getBorradorById(id_borrador)
        if not reg:
            return jsonify({'success': False, 'error': 'No se encontró el borrador.'}), 404
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener borrador de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas-borrador', methods=['POST'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def addFacturaBorrador():
    """POST: crea un borrador (hace falta al menos el paciente); devuelve el id nuevo (201)."""
    data = request.get_json() or {}
    if not data.get('id_paciente'):
        return jsonify({'success': False, 'error': msg_obligatorio('Paciente')}), 400
    try:
        nuevo_id = FacturaBorradorDao().crearBorrador(int(data['id_paciente']), data.get('datos') or {}, session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_factura_borrador': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al crear borrador de factura: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas-borrador/<int:id_borrador>', methods=['PUT'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def updateFacturaBorrador(id_borrador):
    """PUT: guarda el avance de un borrador; 404 si ya no existe (se emitió o lo descartaron)."""
    data = request.get_json() or {}
    if not data.get('id_paciente'):
        return jsonify({'success': False, 'error': msg_obligatorio('Paciente')}), 400
    try:
        if not FacturaBorradorDao().actualizarBorrador(id_borrador, int(data['id_paciente']), data.get('datos') or {}, session.get('id_usuario')):
            return jsonify({'success': False, 'error': 'El borrador ya no existe: se emitió o lo descartaron.'}), 404
        return jsonify({'success': True, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar borrador de factura: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas-borrador/<int:id_borrador>', methods=['DELETE'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def deleteFacturaBorrador(id_borrador):
    """DELETE: descarta un borrador."""
    try:
        if not FacturaBorradorDao().eliminarBorrador(id_borrador):
            return jsonify({'success': False, 'error': 'No se encontró el borrador.'}), 404
        return jsonify({'success': True, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al descartar borrador de factura: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas/<int:id_factura>/pdf', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getFacturaPDF(id_factura):
    """GET: genera y devuelve el PDF (KuDE) de la factura."""
    try:
        factura, buffer = _construir_pdf_factura(id_factura)
        if not factura:
            return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
        nombre = f"factura_{factura['factura_numero'].replace('-', '_')}.pdf"
        return send_file(buffer, mimetype='application/pdf',
                         as_attachment=False, download_name=nombre)
    except Exception as e:
        app.logger.error(f"Error al generar PDF de factura {id_factura}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'No se pudo generar el PDF.'}), 500


@facturaapi.route('/facturas/<int:id_factura>/enviar-correo', methods=['POST'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def enviarFacturaCorreo(id_factura):
    """Reenvío manual del PDF de la factura por correo (ej. si el envío automático
    al timbrar falló, o el cliente lo pide de nuevo)."""
    success, error = _enviar_factura_por_correo(id_factura)
    if not success:
        codigo = 404 if error == 'No se encontró la factura.' else 502
        return jsonify({'success': False, 'error': error or 'No se pudo enviar el correo.'}), codigo
    return jsonify({'success': True, 'mensaje': 'Factura enviada por correo.', 'error': None}), 200


@facturaapi.route('/facturas/<int:id_factura>/anular', methods=['PUT'])
@role_required("ADMINISTRADOR")
@permiso_requerido("VENTAS", "ELIMINAR")
def anularFactura(id_factura):
    """PUT: anula la factura con motivo obligatorio (llama a sp_anular_factura); solo ADMINISTRADOR."""
    dao = FacturaDao()
    if not dao.getFacturaById(id_factura):
        return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
    motivo = ((request.get_json(silent=True) or {}).get('motivo') or '').strip()
    if len(motivo) < 3:
        return jsonify({'success': False, 'error': 'Debe indicar el motivo de la anulación.'}), 400
    try:
        ok = dao.anular(id_factura, usuario_anulacion=session.get('id_usuario'), motivo=motivo)
        if not ok:
            return jsonify({'success': False, 'error': 'La factura ya está anulada o no se pudo anular.'}), 409
        return jsonify({'success': True, 'mensaje': f'Factura {id_factura} anulada.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al anular factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
