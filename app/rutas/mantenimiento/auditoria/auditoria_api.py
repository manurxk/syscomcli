from flask import Blueprint, request, jsonify, current_app as app

from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion, get_label
from app.auth.utils.decorators import role_required

auditoriaapi = Blueprint('auditoriaapi', __name__)


@auditoriaapi.route('/auditoria', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getEventosAuditoria():
    auditoriadao = AuditoriaDao()

    try:
        id_usuario = request.args.get('id_usuario', None, type=int)
        fecha_desde = request.args.get('fecha_desde', None)
        fecha_hasta = request.args.get('fecha_hasta', None)
        accion = request.args.get('accion', None)
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 50, type=int)

        resultado = auditoriadao.getEventos(
            id_usuario=id_usuario,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            accion=accion,
            pagina=pagina,
            por_pagina=por_pagina,
        )

        for evento in resultado['datos']:
            evento['accion_label'] = get_label(evento['accion'])

        return jsonify({'success': True, 'data': resultado, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener eventos de auditoría: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/intentos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getIntentosAcceso():
    try:
        resultado = AuditoriaDao().getIntentosAcceso(
            fecha_desde=request.args.get('fecha_desde'),
            fecha_hasta=request.args.get('fecha_hasta'),
            ip=request.args.get('ip'),
            solo_fallidos=request.args.get('solo_fallidos') == 'true',
            pagina=request.args.get('pagina', 1, type=int),
            por_pagina=request.args.get('por_pagina', 50, type=int),
        )
        return jsonify({'success': True, 'data': resultado, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener intentos de acceso: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/intentos/sospechosos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getIpsSospechosas():
    try:
        data = AuditoriaDao().getIpsSospechosas(
            fecha_desde=request.args.get('fecha_desde'),
            fecha_hasta=request.args.get('fecha_hasta'),
            minimo_cuentas=request.args.get('minimo_cuentas', 2, type=int),
        )
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener IPs sospechosas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/recuperaciones', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getSolicitudesRecuperacionGlobal():
    try:
        resultado = AuditoriaDao().getSolicitudesRecuperacionGlobal(
            fecha_desde=request.args.get('fecha_desde'),
            fecha_hasta=request.args.get('fecha_hasta'),
            pagina=request.args.get('pagina', 1, type=int),
            por_pagina=request.args.get('por_pagina', 50, type=int),
        )
        return jsonify({'success': True, 'data': resultado, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener solicitudes de recuperación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/acciones', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getAccionesAuditoria():
    try:
        acciones = [{'accion': a, 'label': get_label(a)} for a in sorted(AuditAccion._ALL)]
        return jsonify({'success': True, 'data': acciones, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener acciones de auditoría: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
