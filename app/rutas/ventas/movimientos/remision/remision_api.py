from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.remision.RemisionDao import RemisionDao
from app.auth.utils.decorators import role_required

remisionapi = Blueprint('remisionapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@remisionapi.route('/remisiones', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getRemisiones():
    try:
        return jsonify({'success': True, 'data': RemisionDao().getRemisiones(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener remisiones: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@remisionapi.route('/remisiones/<int:id_remision>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getRemision(id_remision):
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
def addRemision():
    data = request.get_json() or {}

    for campo in ['id_paciente', 'fecha_remision']:
        if not data.get(campo):
            return jsonify({'success': False, 'error': f'El campo "{campo}" es obligatorio.'}), 400

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
def entregarRemision(id_remision):
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
@role_required("ADMINISTRADOR", "SUPERADMIN")
def anularRemision(id_remision):
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
