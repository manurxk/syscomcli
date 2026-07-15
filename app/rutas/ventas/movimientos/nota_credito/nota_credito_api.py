from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.nota_credito.NotaCreditoDao import NotaCreditoDao
from app.auth.utils.decorators import role_required

notacreditoapi = Blueprint('notacreditoapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@notacreditoapi.route('/notas-credito', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getNotasCredito():
    try:
        return jsonify({'success': True, 'data': NotaCreditoDao().getNotasCredito(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener notas de crédito: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notacreditoapi.route('/notas-credito/<int:id_nota_credito>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getNotaCredito(id_nota_credito):
    try:
        dao = NotaCreditoDao()
        reg = dao.getNotaCreditoById(id_nota_credito)
        if not reg:
            return jsonify({'success': False, 'error': 'No se encontró la nota de crédito.'}), 404
        reg['detalle'] = dao.getNotaCreditoDetalle(id_nota_credito)
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener nota de crédito {id_nota_credito}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notacreditoapi.route('/notas-credito', methods=['POST'])
@role_required(*ROLES_VENTAS)
def addNotaCredito():
    data = request.get_json() or {}

    for campo in ('id_factura', 'motivo'):
        if not data.get(campo):
            return jsonify({'success': False, 'error': f'El campo "{campo}" es obligatorio.'}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La nota de crédito debe tener al menos un ítem.'}), 400
    for d in detalles:
        if not d.get('item_descripcion'):
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una descripción.'}), 400

    try:
        nuevo_id = NotaCreditoDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_nota_credito': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar nota de crédito: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notacreditoapi.route('/notas-credito/<int:id_nota_credito>/anular', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def anularNotaCredito(id_nota_credito):
    dao = NotaCreditoDao()
    if not dao.getNotaCreditoById(id_nota_credito):
        return jsonify({'success': False, 'error': 'No se encontró la nota de crédito.'}), 404
    try:
        ok = dao.anular(id_nota_credito, usuario=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'La nota ya está anulada o no se pudo anular.'}), 409
        return jsonify({'success': True, 'mensaje': f'Nota de crédito {id_nota_credito} anulada.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al anular nota de crédito {id_nota_credito}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
