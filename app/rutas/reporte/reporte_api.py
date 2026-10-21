from flask import Blueprint, request, jsonify, send_file, session
from datetime import datetime, date
import io
from app.auth.utils.decorators import role_required
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.dao.reporte.ReporteDao import ReporteDao
from app.services.reporte_service import ReporteService
from app.utils.auditoria_constantes import AuditAccion
from app.utils.reportes_alcance import ROLES_PANTALLA_REPORTES, alcance_de_sesion

reporteapi = Blueprint('reporteapi', __name__)

# Quién puede qué lo decide alcance_de_sesion(pestana) (app/utils/reportes_alcance.py); el decorador solo deja
# pasar a los roles de la pantalla y cada ruta vuelve a comprobar su pestaña.


def _rango():
    """Fechas del filtro; por defecto, del primer día del mes a hoy."""
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    if not fecha_desde or not fecha_hasta:
        hoy = date.today()
        fecha_hasta = hoy.strftime('%Y-%m-%d')
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')
    return fecha_desde, fecha_hasta


def _sin_permiso():
    """Respuesta 403 cuando el rol no puede ver la pestaña de Reportes."""
    return jsonify({"success": False, "error": "No tiene permiso para esta pestaña de Reportes."}), 403


def _alcance(pestana):
    """Alcance de la sesión en la pestaña; el id_especialista de un Clínico sale de la sesión, nunca del parámetro."""
    return alcance_de_sesion(pestana, request.args.get('id_especialista'))


def _auditar_exportacion(reporte, fecha_desde, fecha_hasta, alcance_txt, extra=''):
    """Deja en la Auditoría quién exportó qué reporte, de qué período y con qué alcance."""
    AuditoriaDao().registrar_evento(
        id_usuario=session.get('id_usuario'),
        accion=AuditAccion.REPORT_EXPORT,
        detalle=f'Exportó a PDF el reporte de {reporte}: {fecha_desde} al {fecha_hasta}, {alcance_txt}{extra}',
        ip_origen=request.remote_addr
    )


def _alcance_texto(alcance):
    """Texto del encabezado del PDF: a quién corresponden los datos."""
    id_esp = alcance['id_especialista']
    if not id_esp:
        return 'Todos los especialistas'
    for e in FuncionarioDao().getEspecialistasActivos():
        if e['id_especialista'] == id_esp:
            return e['nombre_completo']
    return 'Un especialista'


def _kpis_agenda(datos_estado):
    """Citas por estado → KPIs. «Atendida» = COMPLETADA (criterio unificado del PDF 4)."""
    kpis = {'total': 0, 'atendidas': 0, 'canceladas': 0, 'ausentes': 0}
    for d in datos_estado:
        kpis['total'] += d['cantidad']
        if d['estado'] == 'COMPLETADA':
            kpis['atendidas'] += d['cantidad']
        elif d['estado'] == 'CANCELADA':
            kpis['canceladas'] += d['cantidad']
        elif d['estado'] == 'AUSENTE':
            kpis['ausentes'] += d['cantidad']
    total = kpis['total']
    kpis['tasa_asistencia'] = round(kpis['atendidas'] * 100.0 / total, 1) if total else 0
    kpis['tasa_ausencia'] = round(kpis['ausentes'] * 100.0 / total, 1) if total else 0
    return kpis


def _promedio_diario(cantidad, fecha_desde, fecha_hasta):
    """Promedio diario de `cantidad` en el rango de fechas (devuelve `cantidad` si el rango es inválido)."""
    try:
        dias = (datetime.strptime(fecha_hasta, '%Y-%m-%d') - datetime.strptime(fecha_desde, '%Y-%m-%d')).days + 1
        return round(cantidad / dias, 1) if dias > 0 else cantidad
    except ValueError:
        return cantidad


def _formatear(servicio, filas, campos):
    """Agrega «<campo>_formateado» a cada fila, con los decimales de su moneda."""
    for f in filas:
        dec = f.get('decimales_moneda', 0)
        for campo in campos:
            f[f'{campo}_formateado'] = servicio._formatear_moneda(f.get(campo, 0), dec)
    return filas


# ------------------------------- Resumen -------------------------------

@reporteapi.route('/reporte/resumen-data', methods=['GET'])
@role_required(*ROLES_PANTALLA_REPORTES)
def api_resumen_data():
    """GET: datos de la pestaña Resumen de Reportes."""
    if not alcance_de_sesion('resumen')['permitida']:
        return _sin_permiso()
    fecha_desde, fecha_hasta = _rango()
    dao = ReporteDao()
    servicio = ReporteService()

    ventas = dao.getVentasReport(fecha_desde, fecha_hasta)
    facturado = _formatear(servicio, servicio.calcular_totales_ventas(ventas),
                           ('cantidad_comprobantes', 'total_general'))
    saldo = _formatear(servicio, dao.getSaldoCuentasPorMoneda(), ('monto_pendiente', 'monto_vencido'))
    kpis = _kpis_agenda(dao.getAgendamientoReport(fecha_desde, fecha_hasta))

    consultorio = None
    if alcance_de_sesion('consultorio')['permitida']:   # el Superadministrador no ve datos clínicos
        consultorio = dao.getResumenConsultorio(fecha_desde, fecha_hasta)
        consultorio['promedio_diario'] = _promedio_diario(consultorio['consultas'], fecha_desde, fecha_hasta)
        consultorio['derivaciones'] = dao.getDerivaciones(fecha_desde, fecha_hasta)['total_hechas']

    return jsonify({
        "success": True,
        "facturado": facturado,
        "saldo": saldo,
        "agenda": kpis,
        "chart_data": servicio.procesar_ventas_para_grafico(ventas),
        "consultorio": consultorio
    })


# ------------------------------- Ventas -------------------------------

@reporteapi.route('/reporte/ventas-data', methods=['GET'])
@role_required(*ROLES_PANTALLA_REPORTES)
def api_ventas_data():
    """API para obtener datos del reporte de ventas para UI en formato JSON."""
    if not alcance_de_sesion('ventas')['permitida']:
        return _sin_permiso()
    fecha_desde, fecha_hasta = _rango()
    metodo_pago = request.args.get('metodo_pago', 'Todos')

    reporte_dao = ReporteDao()
    data = reporte_dao.getVentasReport(fecha_desde, fecha_hasta, metodo_pago)
    datos_detalle = reporte_dao.getVentasDetalle(fecha_desde, fecha_hasta, metodo_pago)
    datos_metodo_pago = reporte_dao.getVentasPorMetodoPago(fecha_desde, fecha_hasta)

    reporte_service = ReporteService()
    chart_data = reporte_service.procesar_ventas_para_grafico(data)
    totales = reporte_service.calcular_totales_ventas(data)  # lista: un total por moneda

    _formatear(reporte_service, datos_detalle, ('gravado', 'iva', 'total'))
    _formatear(reporte_service, totales, ('cantidad_comprobantes', 'total_gravado', 'total_iva', 'total_general'))

    return jsonify({
        "success": True,
        "data": data,
        "chart_data": chart_data,
        "totales": totales,
        "datos_detalle": datos_detalle,
        "datos_metodo_pago": datos_metodo_pago
    })


@reporteapi.route('/reporte/ventas/pdf', methods=['GET'])
@role_required(*ROLES_PANTALLA_REPORTES)
def reporte_ventas_pdf():
    """GET: genera el PDF del reporte de Ventas con los mismos filtros de la pantalla."""
    if not alcance_de_sesion('ventas')['permitida']:
        return _sin_permiso()
    fecha_desde, fecha_hasta = _rango()
    metodo_pago = request.args.get('metodo_pago', 'Todos')

    dao = ReporteDao()
    _auditar_exportacion('Ventas', fecha_desde, fecha_hasta, 'toda la clínica', f', condición {metodo_pago}')
    pdf_bytes = ReporteService().generar_pdf_ventas(
        fecha_desde, fecha_hasta, metodo_pago, 'Toda la clínica',
        detalle=dao.getVentasDetalle(fecha_desde, fecha_hasta, metodo_pago),
        por_dia=dao.getVentasReport(fecha_desde, fecha_hasta, metodo_pago),
        por_condicion=dao.getVentasPorMetodoPago(fecha_desde, fecha_hasta),
        cobrado=dao.getCobradoPorMoneda(fecha_desde, fecha_hasta),
        saldos=dao.getSaldoCuentasPorMoneda())

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Reporte_Ventas_{fecha_desde}_al_{fecha_hasta}.pdf'
    )


# ----------------------------- Agendamiento -----------------------------

@reporteapi.route('/reporte/agendamiento-data', methods=['GET'])
@role_required(*ROLES_PANTALLA_REPORTES)
def api_agendamiento_data():
    """GET: datos de la pestaña Agendamiento de Reportes."""
    alcance = _alcance('agendamiento')
    if not alcance['permitida']:
        return _sin_permiso()
    fecha_desde, fecha_hasta = _rango()
    id_esp = alcance['id_especialista']

    dao = ReporteDao()
    datos_diarios = dao.getAgendamientoPorDia(fecha_desde, fecha_hasta, id_esp)

    return jsonify({
        "success": True,
        "totales": _kpis_agenda(dao.getAgendamientoReport(fecha_desde, fecha_hasta, id_esp)),
        "pacientes": dao.getAgendamientoPacientes(fecha_desde, fecha_hasta, id_esp),
        "chart_data": ReporteService().procesar_agendamiento_para_grafico(datos_diarios),
        "por_especialista": [] if alcance['propio'] else dao.getAgendamientoPorEspecialista(fecha_desde, fecha_hasta, id_esp),
        "ausentes": dao.getPacientesAusentes(fecha_desde, fecha_hasta, id_esp),
        "reiteradas": dao.getAusenciasReiteradas(fecha_desde, fecha_hasta, id_esp),
        "canceladas": dao.getCitasCanceladas(fecha_desde, fecha_hasta, id_esp)
    })


@reporteapi.route('/reporte/agendamiento/pdf', methods=['GET'])
@role_required(*ROLES_PANTALLA_REPORTES)
def reporte_agendamiento_pdf():
    """GET: genera el PDF del reporte de Agendamiento con los mismos filtros de la pantalla."""
    alcance = _alcance('agendamiento')
    if not alcance['permitida']:
        return _sin_permiso()
    fecha_desde, fecha_hasta = _rango()
    id_esp = alcance['id_especialista']

    dao = ReporteDao()
    datos = {
        'totales': _kpis_agenda(dao.getAgendamientoReport(fecha_desde, fecha_hasta, id_esp)),
        'pacientes': dao.getAgendamientoPacientes(fecha_desde, fecha_hasta, id_esp),
        'por_especialista': [] if alcance['propio'] else dao.getAgendamientoPorEspecialista(fecha_desde, fecha_hasta, id_esp),
        'diarios': dao.getAgendamientoPorDia(fecha_desde, fecha_hasta, id_esp),
        'ausentes': dao.getPacientesAusentes(fecha_desde, fecha_hasta, id_esp),
        'reiteradas': dao.getAusenciasReiteradas(fecha_desde, fecha_hasta, id_esp),
        'canceladas': dao.getCitasCanceladas(fecha_desde, fecha_hasta, id_esp),
        'detalle': dao.getDetalleCitas(fecha_desde, fecha_hasta, id_esp),
    }
    alcance_txt = _alcance_texto(alcance)
    _auditar_exportacion('Agendamiento', fecha_desde, fecha_hasta, alcance_txt.lower() if not alcance['id_especialista'] else alcance_txt)
    pdf_bytes = ReporteService().generar_pdf_agendamiento(fecha_desde, fecha_hasta, alcance_txt, datos)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Reporte_Agendamiento_{fecha_desde}_al_{fecha_hasta}.pdf'
    )


# ------------------------------ Consultorio ------------------------------

@reporteapi.route('/reporte/consultorio-data', methods=['GET'])
@role_required(*ROLES_PANTALLA_REPORTES)
def api_consultorio_data():
    """GET: datos de la pestaña Consultorio de Reportes (el Clínico ve solo lo propio)."""
    alcance = _alcance('consultorio')
    if not alcance['permitida']:
        return _sin_permiso()
    fecha_desde, fecha_hasta = _rango()
    id_esp = alcance['id_especialista']

    dao = ReporteDao()
    resumen = dao.getResumenConsultorio(fecha_desde, fecha_hasta, id_esp)
    resumen['promedio_diario'] = _promedio_diario(resumen['consultas'], fecha_desde, fecha_hasta)
    top_diagnosticos = dao.getTopDiagnosticos(fecha_desde, fecha_hasta, id_esp)

    return jsonify({
        "success": True,
        "totales": resumen,
        "top_diagnosticos": top_diagnosticos,
        "especialidades": dao.getConsultasPorEspecialidad(fecha_desde, fecha_hasta, id_esp),
        "por_especialista": [] if alcance['propio'] else dao.getConsultasPorEspecialista(fecha_desde, fecha_hasta, id_esp),
        "derivaciones": dao.getDerivaciones(fecha_desde, fecha_hasta, id_esp)
    })


@reporteapi.route('/reporte/consultorio/pdf', methods=['GET'])
@role_required(*ROLES_PANTALLA_REPORTES)
def reporte_consultorio_pdf():
    """GET: genera el PDF del reporte de Consultorio con los mismos filtros de la pantalla."""
    alcance = _alcance('consultorio')
    if not alcance['permitida']:
        return _sin_permiso()
    fecha_desde, fecha_hasta = _rango()
    id_esp = alcance['id_especialista']

    dao = ReporteDao()
    totales = dao.getResumenConsultorio(fecha_desde, fecha_hasta, id_esp)
    totales['promedio_diario'] = _promedio_diario(totales['consultas'], fecha_desde, fecha_hasta)
    datos = {
        'totales': totales,
        'derivaciones': dao.getDerivaciones(fecha_desde, fecha_hasta, id_esp),
        'por_especialista': [] if alcance['propio'] else dao.getConsultasPorEspecialista(fecha_desde, fecha_hasta, id_esp),
        'especialidades': dao.getConsultasPorEspecialidad(fecha_desde, fecha_hasta, id_esp),
        'top_diagnosticos': dao.getTopDiagnosticos(fecha_desde, fecha_hasta, id_esp),
        'por_dia': dao.getConsultasPorDia(fecha_desde, fecha_hasta, id_esp),
    }
    alcance_txt = _alcance_texto(alcance)
    _auditar_exportacion('Consultorio', fecha_desde, fecha_hasta, alcance_txt.lower() if not id_esp else alcance_txt)
    # Las derivaciones recibidas solo se cuentan para un especialista (propio o elegido en el filtro)
    pdf_bytes = ReporteService().generar_pdf_consultorio(fecha_desde, fecha_hasta, alcance_txt, datos,
                                                         con_recibidas=bool(id_esp))

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Reporte_Consultorio_{fecha_desde}_al_{fecha_hasta}.pdf'
    )
