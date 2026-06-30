from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.moneda.MonedaDao import MonedaDao
from app.auth.utils.decorators import role_required

monedaapi = Blueprint('monedaapi', __name__)


@monedaapi.route('/monedas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getMonedas():
    try:
        return jsonify({'success': True, 'data': MonedaDao().getMonedas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener monedas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@monedaapi.route('/monedas/<int:id_moneda>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getMoneda(id_moneda):
    try:
        registro = MonedaDao().getMonedaById(id_moneda)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@monedaapi.route('/monedas', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addMoneda():
    data = request.get_json() or {}
    dao = MonedaDao()

    descripcion = (data.get('des_moneda') or '').strip().upper()
    codigo = (data.get('cod_moneda') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not codigo:
        return jsonify({'success': False, 'error': 'El código es obligatorio.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.monedaExiste(codigo):
        return jsonify({'success': False, 'error': f'Ya existe una moneda con código "{codigo}".'}), 400

    try:
        nuevo_id = dao.guardarMoneda(
            descripcion=descripcion,
            codigo=codigo,
            simbolo=data.get('simbolo_moneda'),
            decimales=int(data.get('decimales_moneda', 0)),
            es_moneda_local=bool(data.get('es_moneda_local', False)),
            tasa_cambio=float(data.get('tasa_cambio', 1.0)),
            estado=bool(data.get('est_moneda', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_moneda': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@monedaapi.route('/monedas/<int:id_moneda>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateMoneda(id_moneda):
    data = request.get_json() or {}
    dao = MonedaDao()

    if not dao.getMonedaById(id_moneda):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_moneda') or '').strip().upper()
    codigo = (data.get('cod_moneda') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not codigo:
        return jsonify({'success': False, 'error': 'El código es obligatorio.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.monedaExiste(codigo, excluir_id=id_moneda):
        return jsonify({'success': False, 'error': f'Ya existe una moneda con código "{codigo}".'}), 400

    try:
        dao.updateMoneda(
            id_moneda=id_moneda,
            descripcion=descripcion,
            codigo=codigo,
            simbolo=data.get('simbolo_moneda'),
            decimales=int(data.get('decimales_moneda', 0)),
            es_moneda_local=bool(data.get('es_moneda_local', False)),
            tasa_cambio=float(data.get('tasa_cambio', 1.0)),
            estado=bool(data.get('est_moneda', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_moneda': id_moneda}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@monedaapi.route('/monedas/<int:id_moneda>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarMoneda(id_moneda):
    dao = MonedaDao()
    if not dao.getMonedaById(id_moneda):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarMoneda(id_moneda, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Moneda {id_moneda} desactivada.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar moneda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
