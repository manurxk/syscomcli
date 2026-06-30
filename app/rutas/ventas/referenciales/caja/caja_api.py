from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.caja.CajaDao import CajaDao
from app.auth.utils.decorators import role_required

cajaapi = Blueprint('cajaapi', __name__)


@cajaapi.route('/cajas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getCajas():
    try:
        return jsonify({'success': True, 'data': CajaDao().getCajas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cajas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cajaapi.route('/cajas/<int:id_caja>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getCaja(id_caja):
    try:
        registro = CajaDao().getCajaById(id_caja)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cajaapi.route('/cajas', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addCaja():
    data = request.get_json() or {}
    dao = CajaDao()

    descripcion = (data.get('des_caja') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.cajaExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe una caja "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarCaja(
            descripcion=descripcion,
            codigo=data.get('cod_caja'),
            saldo_inicial=float(data.get('caja_saldo_inicial', 0)),
            estado_caja=data.get('caja_estado', 'CERRADA'),
            estado=bool(data.get('est_caja', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_caja': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cajaapi.route('/cajas/<int:id_caja>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateCaja(id_caja):
    data = request.get_json() or {}
    dao = CajaDao()

    if not dao.getCajaById(id_caja):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_caja') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.cajaExiste(descripcion, excluir_id=id_caja):
        return jsonify({'success': False, 'error': f'Ya existe una caja "{descripcion}".'}), 400

    try:
        dao.updateCaja(
            id_caja=id_caja,
            descripcion=descripcion,
            codigo=data.get('cod_caja'),
            saldo_inicial=float(data.get('caja_saldo_inicial')) if data.get('caja_saldo_inicial') is not None else None,
            estado_caja=data.get('caja_estado'),
            estado=bool(data.get('est_caja', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_caja': id_caja}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cajaapi.route('/cajas/<int:id_caja>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarCaja(id_caja):
    dao = CajaDao()
    if not dao.getCajaById(id_caja):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarCaja(id_caja, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Caja {id_caja} desactivada.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
