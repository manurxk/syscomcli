from flask import Blueprint, request, jsonify, current_app as app, session

from app.core.moneda import get_moneda, redondear
from app.dao.ventas.movimientos.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao
from app.auth.utils.decorators import role_required, permiso_requerido
from app.utils.mensajes_validacion import msg_obligatorio

aperturacierrecajaapi = Blueprint('aperturacierrecajaapi', __name__)

ROLES_CAJA = ("ADMINISTRADOR", "VENTAS")


@aperturacierrecajaapi.route('/cajas-estado', methods=['GET'])
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "LEER")
def getCajasEstado():
    """GET: estado actual de cada caja (abierta o cerrada)."""
    try:
        return jsonify({'success': True, 'data': AperturaCierreCajaDao().getEstadoCajas(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener estado de cajas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/aperturas-cierres', methods=['GET'])
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "LEER")
def getAperturasCierres():
    """GET: lista los registros de apertura/cierre de caja."""
    try:
        return jsonify({'success': True, 'data': AperturaCierreCajaDao().getAperturasCierres(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener aperturas/cierres: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/aperturas-cierres/<int:id_apertura_cierre>', methods=['GET'])
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "LEER")
def getAperturaCierre(id_apertura_cierre):
    """GET: devuelve apertura/cierre de caja por su id; 404 si no existe."""
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
@permiso_requerido("VENTAS", "LEER")
def getAperturaActiva(id_caja):
    """GET: apertura vigente de la caja indicada, o vacío si está cerrada."""
    try:
        apertura = AperturaCierreCajaDao().getAperturaActivaPorCaja(id_caja)
        return jsonify({'success': True, 'data': apertura, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener apertura activa de caja {id_caja}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@aperturacierrecajaapi.route('/cajas/<int:id_caja>/saldo-esperado', methods=['GET'])
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "LEER")
def getSaldoEsperado(id_caja):
    """GET: saldo que debería haber en la caja según los cobros de la apertura vigente."""
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
@permiso_requerido("VENTAS", "LEER")
def getHistorialCaja(id_caja):
    """GET: historial de aperturas y cierres de la caja; admite filtro de fechas por query string."""
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
@permiso_requerido("VENTAS", "CREAR")
def abrirCaja():
    """POST: abre la caja con saldo inicial; la moneda queda fijada por la apertura."""
    data = request.get_json() or {}
    id_caja = data.get('id_caja')
    id_usuario = data.get('id_usuario') or session.get('id_usuario')

    if not id_caja:
        return jsonify({'success': False, 'error': msg_obligatorio('Caja')}), 400
    if not id_usuario:
        return jsonify({'success': False, 'error': msg_obligatorio('Usuario')}), 400

    observaciones = data.get('observaciones')

    try:
        moneda = get_moneda(data.get('id_moneda'))
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    saldo_inicial = redondear(data.get('saldo_inicial', 0), moneda['decimales_moneda'])

    try:
        nuevo_id = AperturaCierreCajaDao().guardarApertura(
            id_caja=id_caja,
            id_usuario=id_usuario,
            saldo_inicial=saldo_inicial,
            observaciones=observaciones,
            usuario_creacion=session.get('id_usuario'),
            id_moneda=moneda['id_moneda'],
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
@permiso_requerido("VENTAS", "EDITAR")
def cerrarCaja():
    """POST: cierra la caja con el saldo contado (llama al procedimiento sp_cerrar_caja)."""
    data = request.get_json() or {}
    id_caja = data.get('id_caja')
    id_usuario = data.get('id_usuario') or session.get('id_usuario')

    if not id_caja:
        return jsonify({'success': False, 'error': msg_obligatorio('Caja')}), 400
    if not id_usuario:
        return jsonify({'success': False, 'error': msg_obligatorio('Usuario')}), 400

    try:
        cierre = AperturaCierreCajaDao().guardarCierre(
            id_caja=id_caja,
            id_usuario=id_usuario,
            saldo_final=None,  # es la suma de los montos contados: la calcula guardarCierre
            monto_efectivo=data.get('monto_efectivo', 0),
            monto_cheques=data.get('monto_cheques', 0),
            monto_tarjetas=data.get('monto_tarjetas', 0),
            monto_transferencias=data.get('monto_transferencias', 0),
            observaciones=data.get('observaciones'),
            usuario_creacion=session.get('id_usuario'),
        )
        if cierre is None:
            return jsonify({'success': False, 'error': 'No se pudo registrar el cierre.'}), 500
        return jsonify({'success': True, 'data': cierre, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al cerrar caja {id_caja}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
