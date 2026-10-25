from flask import Blueprint, request, jsonify, current_app as app, session, send_file

from app.dao.ventas.movimientos.remision.RemisionDao import RemisionDao
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.services.documento_ventas_pdf_service import DocumentoVentasPdfService
from app.auth.utils.decorators import role_required, permiso_requerido
from app.utils.mensajes_validacion import msg_obligatorio

remisionapi = Blueprint('remisionapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "VENTAS")


@remisionapi.route('/remisiones', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getRemisiones():
    """GET: lista los registros de remisión."""
    try:
        return jsonify({'success': True, 'data': RemisionDao().getRemisiones(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener remisiones: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@remisionapi.route('/remisiones/<int:id_remision>', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getRemision(id_remision):
    """GET: devuelve remisión por su id; 404 si no existe."""
    try:
        dao = RemisionDao()
        reg = dao.getRemisionById(id_remision)
        if not reg:
            return jsonify({'success': False, 'error': 'No se encontró la remisión.'}), 404
        reg['detalle'] = dao.getRemisionDetalle(id_remision)
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener remisión: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@remisionapi.route('/remisiones', methods=['POST'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def addRemision():
    """POST: valida los datos y registra remisión; devuelve el id nuevo (201)."""
    data = request.get_json() or {}

    for campo in ['id_paciente', 'fecha_remision']:
        if not data.get(campo):
            return jsonify({'success': False, 'error': msg_obligatorio(campo)}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La remisión debe tener al menos un ítem en el detalle.'}), 400
    for d in detalles:
        if not d.get('item_descripcion'):
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una descripción.'}), 400
        cant = d.get('item_cantidad')
        if cant is None or float(cant) <= 0:
            return jsonify({'success': False, 'error': 'La cantidad de cada ítem debe ser mayor a 0.'}), 400

    try:
        nuevo_id = RemisionDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_remision': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar remisión: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@remisionapi.route('/remisiones/<int:id_remision>/entregar', methods=['PUT'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "EDITAR")
def entregarRemision(id_remision):
    """PUT: marca la remisión como entregada."""
    dao = RemisionDao()
    if not dao.getRemisionById(id_remision):
        return jsonify({'success': False, 'error': 'No se encontró la remisión.'}), 404
    try:
        ok = dao.marcarEntregada(id_remision, usuario=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'La remisión ya fue entregada o no se puede cambiar su estado.'}), 409
        return jsonify({'success': True, 'mensaje': f'Remisión {id_remision} marcada como ENTREGADA.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al entregar remisión: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@remisionapi.route('/remisiones/<int:id_remision>/anular', methods=['PUT'])
@role_required("ADMINISTRADOR")
@permiso_requerido("VENTAS", "ELIMINAR")
def anularRemision(id_remision):
    """PUT: anula la remisión."""
    dao = RemisionDao()
    if not dao.getRemisionById(id_remision):
        return jsonify({'success': False, 'error': 'No se encontró la remisión.'}), 404
    try:
        ok = dao.anular(id_remision, usuario=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'La remisión ya está anulada.'}), 409
        return jsonify({'success': True, 'mensaje': f'Remisión {id_remision} anulada.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al anular remisión: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@remisionapi.route('/remisiones/<int:id_remision>/pdf', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getRemisionPdf(id_remision):
    """PDF imprimible (REMISION.html), con firmas de quien entrega y quien recibe."""
    try:
        dao = RemisionDao()
        remision = dao.getRemisionById(id_remision)
        if not remision:
            return jsonify({'success': False, 'error': 'No se encontró la remisión.'}), 404
        buffer = DocumentoVentasPdfService().generar_remision_pdf(
            remision, dao.getRemisionDetalle(id_remision),
            FichaDao().getDatosPaciente(remision['id_paciente']) or {},
            DocumentoVentasPdfService.config_empresa(),
        )
        return send_file(buffer, mimetype='application/pdf', as_attachment=False,
                         download_name=f"remision_{remision['remision_numero']}.pdf")
    except Exception as e:
        app.logger.error(f"Error al generar PDF de remisión {id_remision}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
