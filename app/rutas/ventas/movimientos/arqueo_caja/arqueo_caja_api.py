from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.arqueo_caja.ArqueoCajaDao import ArqueoCajaDao
from app.auth.utils.decorators import role_required

arqueocajaapi = Blueprint('arqueocajaapi', __name__)

ROLES_CAJA = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@arqueocajaapi.route('/arqueos', methods=['GET'])
@role_required(*ROLES_CAJA)
def getArqueos():
    try:
        return jsonify({'success': True, 'data': ArqueoCajaDao().getArqueos(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener arqueos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueocajaapi.route('/arqueos/<int:id_arqueo>', methods=['GET'])
@role_required(*ROLES_CAJA)
def getArqueo(id_arqueo):
    try:
        registro = ArqueoCajaDao().getArqueoById(id_arqueo)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el arqueo.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener arqueo {id_arqueo}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueocajaapi.route('/cajas/<int:id_caja>/arqueos', methods=['GET'])
@role_required(*ROLES_CAJA)
def getArqueosPorCaja(id_caja):
    try:
        return jsonify({'success': True, 'data': ArqueoCajaDao().getArqueosPorCaja(id_caja), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener arqueos de caja {id_caja}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueocajaapi.route('/aperturas-cierres/<int:id_apertura_cierre>/monto-esperado', methods=['GET'])
@role_required(*ROLES_CAJA)
def getMontoEsperado(id_apertura_cierre):
    id_caja = request.args.get('id_caja', type=int)
    if not id_caja:
        return jsonify({'success': False, 'error': 'id_caja es requerido.'}), 400
    try:
        monto = ArqueoCajaDao().calcularMontoEsperado(id_apertura_cierre, id_caja)
        if monto is None:
            return jsonify({'success': False, 'error': 'No se pudo calcular el monto esperado.'}), 404
        return jsonify({'success': True, 'data': {'monto_esperado': monto}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al calcular monto esperado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueocajaapi.route('/arqueos', methods=['POST'])
@role_required(*ROLES_CAJA)
def addArqueo():
    data = request.get_json() or {}

    id_apertura_cierre = data.get('id_apertura_cierre')
    id_caja = data.get('id_caja')
    monto_real = data.get('monto_real')

    if not id_apertura_cierre:
        return jsonify({'success': False, 'error': 'La apertura de caja es obligatoria.'}), 400
    if not id_caja:
        return jsonify({'success': False, 'error': 'La caja es obligatoria.'}), 400
    if monto_real is None:
        return jsonify({'success': False, 'error': 'El monto real es obligatorio.'}), 400

    try:
        nuevo_id = ArqueoCajaDao().guardarArqueo(
            id_apertura_cierre=id_apertura_cierre,
            id_caja=id_caja,
            monto_real=monto_real,
            observaciones=data.get('observaciones'),
            usuario_creacion=session.get('id_usuario'),
        )
        if nuevo_id is None:
            return jsonify({'success': False, 'error': 'No se pudo registrar el arqueo.'}), 500
        return jsonify({'success': True, 'data': {'id_arqueo': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar arqueo: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
