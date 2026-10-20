import io
from datetime import date

from flask import Blueprint, request, jsonify, session, send_file, current_app as app

from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.services.informe_auditoria_service import (armar_informe, generar_pdf_informe, modulos_destinatario,
                                                    semana_anterior)
from app.utils.auditoria_constantes import (AuditAccion, get_label, alcance_cambios,
                                            ROLES_PANTALLA_AUDITORIA, ROLES_AUDITORIA_COMPLETA)
from app.auth.utils.decorators import role_required

auditoriaapi = Blueprint('auditoriaapi', __name__)


def _alcance_sesion():
    """Lo que la sesión puede ver de auditoria_transacciones, por nivel (ver alcance_cambios):
    detalle (todos los cambios del módulo), propios (solo los del usuario de la sesión) y resumen."""
    alcance = alcance_cambios(session.get('roles', []))
    por_nivel = {n: [m for m, v in alcance.items() if v == n] for n in ('detalle', 'propios', 'resumen')}
    return por_nivel, session.get('id_usuario')


@auditoriaapi.route('/auditoria/cambios', methods=['GET'])
@role_required(*ROLES_PANTALLA_AUDITORIA)
def getCambiosDatos():
    """Listado de cambios en datos: módulos en detalle completos y, en los "propios", solo los del usuario."""
    nivel, id_propio = _alcance_sesion()
    detalle, propios = nivel['detalle'], nivel['propios']
    if not detalle and not propios:
        return jsonify({'success': False, 'error': 'No tiene permiso para ver el detalle de los cambios.'}), 403
    modulo = request.args.get('modulo')
    if modulo:
        detalle = [m for m in detalle if m == modulo]
        propios = [m for m in propios if m == modulo]
    try:
        resultado = AuditoriaDao().getCambios(
            detalle,
            tabla=request.args.get('tabla') or None,
            operacion=request.args.get('operacion') or None,
            id_usuario=request.args.get('id_usuario', None, type=int),
            fecha_desde=request.args.get('fecha_desde') or None,
            fecha_hasta=request.args.get('fecha_hasta') or None,
            id_registro=request.args.get('id_registro') or None,
            pagina=request.args.get('pagina', 1, type=int),
            por_pagina=request.args.get('por_pagina', 50, type=int),
            modulos_propios=propios, id_propio=id_propio,
        )
        return jsonify({'success': True, 'data': resultado, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cambios en datos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/cambios/<int:id_cambio>', methods=['GET'])
@role_required(*ROLES_PANTALLA_AUDITORIA)
def getCambioDatos(id_cambio):
    """Un cambio con el dato anterior y el nuevo; 403 si la sesión no lo puede ver (o no existe)."""
    try:
        nivel, id_propio = _alcance_sesion()
        cambio = AuditoriaDao().getCambio(id_cambio)
        permitido = cambio and (cambio['modulo'] in nivel['detalle'] or
                                (cambio['modulo'] in nivel['propios'] and id_propio and cambio['id_usuario'] == id_propio))
        if not permitido:
            return jsonify({'success': False, 'error': 'No tiene permiso para ver este cambio.'}), 403
        return jsonify({'success': True, 'data': cambio, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener el cambio {id_cambio}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/cambios/resumen', methods=['GET'])
@role_required(*ROLES_PANTALLA_AUDITORIA)
def getResumenCambiosDatos():
    """Solo cantidades: módulos en detalle o resumen completos y, en los "propios", solo los del usuario."""
    try:
        nivel, id_propio = _alcance_sesion()
        data = AuditoriaDao().getResumenCambios(
            nivel['detalle'] + nivel['resumen'],
            fecha_desde=request.args.get('fecha_desde') or None,
            fecha_hasta=request.args.get('fecha_hasta') or None,
            modulos_propios=nivel['propios'], id_propio=id_propio,
        )
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener el resumen de cambios: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/cambios/tablas', methods=['GET'])
@role_required(*ROLES_PANTALLA_AUDITORIA)
def getTablasCambiosDatos():
    try:
        nivel, id_propio = _alcance_sesion()
        data = AuditoriaDao().getTablasCambios(nivel['detalle'], modulos_propios=nivel['propios'], id_propio=id_propio)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener las tablas auditadas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@auditoriaapi.route('/auditoria/informe-semanal/pdf', methods=['GET'])
@role_required(*ROLES_AUDITORIA_COMPLETA)
def getInformeSemanalPdf():
    """Informe de auditoría en PDF (por defecto, la semana anterior), con los módulos que ve la sesión.
    Es el mismo que llega por correo los lunes."""
    try:
        desde, hasta = semana_anterior()
        if request.args.get('fecha_desde') and request.args.get('fecha_hasta'):
            desde = date.fromisoformat(request.args['fecha_desde'])
            hasta = date.fromisoformat(request.args['fecha_hasta'])
        modulos = modulos_destinatario(session.get('roles', []))
        pdf = generar_pdf_informe(armar_informe(modulos, desde, hasta))
        return send_file(io.BytesIO(pdf), mimetype='application/pdf', as_attachment=True,
                         download_name=f'Informe_auditoria_{desde}_al_{hasta}.pdf')
    except ValueError:
        return jsonify({'success': False, 'error': 'Las fechas no tienen un formato válido.'}), 400
    except Exception as e:
        app.logger.error(f"Error al generar el informe de auditoría: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


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
            id_usuario=request.args.get('id_usuario', None, type=int),
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
            id_usuario=request.args.get('id_usuario', None, type=int),
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
