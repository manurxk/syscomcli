from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.recaudacion.RecaudacionDao import RecaudacionDao
from app.auth.utils.decorators import role_required, permiso_requerido
from app.utils.mensajes_validacion import msg_obligatorio

recaudacionapi = Blueprint('recaudacionapi', __name__)

ROLES_VENTAS  = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
ROLES_ADMIN   = ("ADMINISTRADOR", "SUPERADMIN")


@recaudacionapi.route('/recaudaciones', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getRecaudaciones():
    """GET: lista los registros de recaudación."""
    try:
        return jsonify({'success': True, 'data': RecaudacionDao().getRecaudaciones(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recaudaciones: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacionapi.route('/recaudaciones/pendientes', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getRecaudacionesPendientes():
    """GET: lista los registros de recaudación."""
    try:
        return jsonify({'success': True, 'data': RecaudacionDao().getRecaudacionesPendientes(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recaudaciones pendientes: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacionapi.route('/recaudaciones/<int:id_recaudacion>', methods=['GET'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def getRecaudacion(id_recaudacion):
    """GET: devuelve recaudación por su id; 404 si no existe."""
    try:
        reg = RecaudacionDao().getRecaudacionById(id_recaudacion)
        if not reg:
            return jsonify({'success': False, 'error': 'Recaudación no encontrada.'}), 404
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recaudación {id_recaudacion}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacionapi.route('/recaudaciones', methods=['POST'])
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def addRecaudacion():
    """POST: valida los datos y registra recaudación; devuelve el id nuevo (201)."""
    data = request.get_json() or {}

    for campo in ('id_caja', 'id_deposito'):
        if not data.get(campo):
            return jsonify({'success': False, 'error': msg_obligatorio(campo)}), 400

    monto_total = (float(data.get('monto_efectivo') or 0) +
                   float(data.get('monto_cheques')  or 0) +
                   float(data.get('monto_tarjetas') or 0))
    if monto_total <= 0:
        return jsonify({'success': False, 'error': 'El monto total debe ser mayor a cero.'}), 400

    try:
        nuevo_id = RecaudacionDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_recaudacion': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar recaudación: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacionapi.route('/recaudaciones/<int:id_recaudacion>/depositar', methods=['PUT'])
@role_required(*ROLES_ADMIN)
@permiso_requerido("VENTAS", "EDITAR")
def depositarRecaudacion(id_recaudacion):
    """PUT: marca la recaudación como depositada."""
    data          = request.get_json() or {}
    fecha_deposito = data.get('fecha_deposito')
    if not fecha_deposito:
        return jsonify({'success': False, 'error': msg_obligatorio('Fecha de depósito')}), 400
    try:
        ok = RecaudacionDao().marcarDepositada(
            id_recaudacion, fecha_deposito, usuario=session.get('id_usuario')
        )
        if not ok:
            return jsonify({'success': False, 'error': 'No se pudo marcar como depositada.'}), 409
        return jsonify({'success': True, 'mensaje': f'Recaudación {id_recaudacion} depositada.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al depositar recaudación {id_recaudacion}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacionapi.route('/recaudaciones/<int:id_recaudacion>/anular', methods=['PUT'])
@role_required(*ROLES_ADMIN)
@permiso_requerido("VENTAS", "ELIMINAR")
def anularRecaudacion(id_recaudacion):
    """PUT: anula la recaudación."""
    try:
        ok = RecaudacionDao().anular(id_recaudacion, usuario=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'La recaudación ya está anulada o no se encontró.'}), 409
        return jsonify({'success': True, 'mensaje': f'Recaudación {id_recaudacion} anulada.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al anular recaudación {id_recaudacion}: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
