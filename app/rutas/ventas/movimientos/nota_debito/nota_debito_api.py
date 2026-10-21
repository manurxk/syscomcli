from flask import Blueprint, request, jsonify, current_app as app, session, send_file

from app.dao.ventas.movimientos.nota_debito.NotaDebitoDao import NotaDebitoDao
from app.dao.ventas.movimientos.factura.FacturaDao import FacturaDao
from app.services.factura_pdf_service import FacturaPDFService
from app.auth.utils.decorators import role_required, permiso_requerido
from app.utils.mensajes_validacion import msg_obligatorio

notadebitoapi = Blueprint('notadebitoapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@notadebitoapi.route('/notas-debito', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getNotasDebito():
    """GET: lista los registros de nota de débito."""
    try:
        return jsonify({'success': True, 'data': NotaDebitoDao().getNotasDebito(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener notas de débito: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notadebitoapi.route('/notas-debito/<int:id_nota_debito>', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getNotaDebito(id_nota_debito):
    """GET: devuelve nota de débito por su id; 404 si no existe."""
    try:
        dao = NotaDebitoDao()
        reg = dao.getNotaDebitoById(id_nota_debito)
        if not reg:
            return jsonify({'success': False, 'error': 'No se encontró la nota de débito.'}), 404
        reg['detalle'] = dao.getNotaDebitoDetalle(id_nota_debito)
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener nota de débito {id_nota_debito}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notadebitoapi.route('/notas-debito', methods=['POST'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def addNotaDebito():
    """POST: valida los datos y registra nota de débito; devuelve el id nuevo (201)."""
    data = request.get_json() or {}

    for campo in ('id_factura', 'motivo'):
        if not data.get(campo):
            return jsonify({'success': False, 'error': msg_obligatorio(campo)}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La nota de débito debe tener al menos un ítem.'}), 400
    for d in detalles:
        if not d.get('item_descripcion'):
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una descripción.'}), 400

    try:
        nuevo_id = NotaDebitoDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_nota_debito': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar nota de débito: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notadebitoapi.route('/notas-debito/<int:id_nota_debito>/anular', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
@permiso_requerido("VENTAS", "ELIMINAR")
def anularNotaDebito(id_nota_debito):
    """PUT: anula la nota de débito."""
    dao = NotaDebitoDao()
    if not dao.getNotaDebitoById(id_nota_debito):
        return jsonify({'success': False, 'error': 'No se encontró la nota de débito.'}), 404
    try:
        ok = dao.anular(id_nota_debito, usuario=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'La nota ya está anulada o no se pudo anular.'}), 409
        return jsonify({'success': True, 'mensaje': f'Nota de débito {id_nota_debito} anulada.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al anular nota de débito {id_nota_debito}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notadebitoapi.route('/notas-debito/<int:id_nota_debito>/pdf', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getNotaDebitoPDF(id_nota_debito):
    """KuDE de la nota (FE.html, misma plantilla que la factura asociada)."""
    try:
        dao = NotaDebitoDao()
        nota = dao.getNotaDebitoById(id_nota_debito)
        if not nota:
            return jsonify({'success': False, 'error': 'No se encontró la nota de débito.'}), 404
        fdao = FacturaDao()
        buffer = FacturaPDFService().generar_nota_pdf(
            'ND', nota, dao.getNotaDebitoDetalle(id_nota_debito),
            fdao.getFacturaById(nota['id_factura']) or {}, fdao.getFacturaDetalle(nota['id_factura']),
        )
        nombre = f"nota_debito_{nota['nota_debito_numero'].replace('-', '_')}.pdf"
        return send_file(buffer, mimetype='application/pdf', as_attachment=False, download_name=nombre)
    except Exception as e:
        app.logger.error(f"Error al generar PDF de nota de débito {id_nota_debito}: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'No se pudo generar el PDF.'}), 500
