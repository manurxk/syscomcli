from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.nota_debito.NotaDebitoDao import NotaDebitoDao
from app.auth.utils.decorators import role_required

notadebitoapi = Blueprint('notadebitoapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@notadebitoapi.route('/notas-debito', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getNotasDebito():
    try:
        return jsonify({'success': True, 'data': NotaDebitoDao().getNotasDebito(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener notas de débito: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@notadebitoapi.route('/notas-debito/<int:id_nota_debito>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getNotaDebito(id_nota_debito):
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
def addNotaDebito():
    data = request.get_json() or {}

    for campo in ('id_factura', 'motivo'):
        if not data.get(campo):
            return jsonify({'success': False, 'error': f'El campo "{campo}" es obligatorio.'}), 400

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
def anularNotaDebito(id_nota_debito):
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
