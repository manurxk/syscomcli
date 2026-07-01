from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.movimientos.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao
from app.auth.utils.decorators import role_required

aperturacierrecajaapi = Blueprint('aperturacierrecajaapi', __name__)

ROLES_CAJA = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@aperturacierrecajaapi.route('/cajas-estado', methods=['GET'])
@role_required(*ROLES_CAJA)
def getCajasEstado():
    try:
        return jsonify({'success': True, 'data': AperturaCierreCajaDao().getEstadoCajas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener estado de cajas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/aperturas-cierres', methods=['GET'])
@role_required(*ROLES_CAJA)
def getAperturasCierres():
    try:
        return jsonify({'success': True, 'data': AperturaCierreCajaDao().getAperturasCierres(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener aperturas/cierres: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/aperturas-cierres/<int:id_apertura_cierre>', methods=['GET'])
@role_required(*ROLES_CAJA)
def getAperturaCierre(id_apertura_cierre):
    try:
        registro = AperturaCierreCajaDao().getAperturaCierreById(id_apertura_cierre)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener apertura/cierre {id_apertura_cierre}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/cajas/<int:id_caja>/apertura-activa', methods=['GET'])
@role_required(*ROLES_CAJA)
def getAperturaActiva(id_caja):
    try:
        apertura = AperturaCierreCajaDao().getAperturaActivaPorCaja(id_caja)
        return jsonify({'success': True, 'data': apertura, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener apertura activa de caja {id_caja}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/cajas/<int:id_caja>/saldo-esperado', methods=['GET'])
@role_required(*ROLES_CAJA)
def getSaldoEsperado(id_caja):
    try:
        saldo = AperturaCierreCajaDao().calcularSaldoEsperado(id_caja)
        if saldo is None:
            return jsonify({'success': False, 'error': 'No hay apertura activa para esta caja.'}), 404
        return jsonify({'success': True, 'data': saldo, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al calcular saldo esperado de caja {id_caja}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/cajas/<int:id_caja>/historial', methods=['GET'])
@role_required(*ROLES_CAJA)
def getHistorialCaja(id_caja):
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    try:
        data = AperturaCierreCajaDao().getHistorialPorCaja(id_caja, fecha_desde, fecha_hasta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener historial de caja {id_caja}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/apertura-caja', methods=['POST'])
@role_required(*ROLES_CAJA)
def abrirCaja():
    data = request.get_json() or {}
    id_caja = data.get('id_caja')
    id_usuario = data.get('id_usuario') or session.get('id_usuario')

    if not id_caja:
        return jsonify({'success': False, 'error': 'La caja es obligatoria.'}), 400
    if not id_usuario:
        return jsonify({'success': False, 'error': 'El usuario es obligatorio.'}), 400

    saldo_inicial = data.get('saldo_inicial', 0)
    observaciones = data.get('observaciones')

    try:
        nuevo_id = AperturaCierreCajaDao().guardarApertura(
            id_caja=id_caja,
            id_usuario=id_usuario,
            saldo_inicial=saldo_inicial,
            observaciones=observaciones,
            usuario_creacion=session.get('id_usuario'),
        )
        if nuevo_id is None:
            return jsonify({'success': False, 'error': 'No se pudo registrar la apertura.'}), 500
        return jsonify({'success': True, 'data': {'id_apertura_cierre': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al abrir caja {id_caja}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/cierre-caja', methods=['POST'])
@role_required(*ROLES_CAJA)
def cerrarCaja():
    data = request.get_json() or {}
    id_caja = data.get('id_caja')
    id_usuario = data.get('id_usuario') or session.get('id_usuario')

    if not id_caja:
        return jsonify({'success': False, 'error': 'La caja es obligatoria.'}), 400
    if not id_usuario:
        return jsonify({'success': False, 'error': 'El usuario es obligatorio.'}), 400
    if data.get('saldo_final') is None:
        return jsonify({'success': False, 'error': 'El saldo final es obligatorio.'}), 400

    try:
        nuevo_id = AperturaCierreCajaDao().guardarCierre(
            id_caja=id_caja,
            id_usuario=id_usuario,
            saldo_final=data.get('saldo_final'),
            monto_efectivo=data.get('monto_efectivo', 0),
            monto_cheques=data.get('monto_cheques', 0),
            monto_tarjetas=data.get('monto_tarjetas', 0),
            monto_transferencias=data.get('monto_transferencias', 0),
            observaciones=data.get('observaciones'),
            usuario_creacion=session.get('id_usuario'),
        )
        if nuevo_id is None:
            return jsonify({'success': False, 'error': 'No se pudo registrar el cierre.'}), 500
        return jsonify({'success': True, 'data': {'id_apertura_cierre': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al cerrar caja {id_caja}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
