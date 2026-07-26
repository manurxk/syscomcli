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


@auditoriaapi.route('/auditoria/acciones', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getAccionesAuditoria():
    try:
        acciones = [{'accion': a, 'label': get_label(a)} for a in sorted(AuditAccion._ALL)]
        return jsonify({'success': True, 'data': acciones, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener acciones de auditoría: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
