from flask import Blueprint, request, jsonify, session, current_app as app, send_file
from datetime import datetime, date
import io
from app.auth.utils.decorators import role_required
from app.dao.modulos.reporte.ReporteDao import ReporteDao
from app.services.ReporteService import ReporteService
from app.dao.AuditoriaDao import AuditoriaDao

reporte_api = Blueprint('reporte_api', __name__)

# Lista de roles autorizados
ROLES_REPORTES = ['SUPERADMINISTRADOR', 'ADMINISTRADOR', 'ADMIN', 'VENTAS', 'RECEPCIONISTA', 'ESPECIALISTA', 'CAJA']

@reporte_api.route('/reporte/ventas-data', methods=['GET'])
@role_required(*ROLES_REPORTES)
def api_ventas_data():
    """API para obtener datos del reporte de ventas para UI en formato JSON."""
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    metodo_pago = request.args.get('metodo_pago', 'Todos')
    
    if not fecha_desde or not fecha_hasta:
        hoy = date.today()
        fecha_hasta = hoy.strftime('%Y-%m-%d')
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')
        
    reporte_dao = ReporteDao()
    data = reporte_dao.getVentasReport(fecha_desde, fecha_hasta, metodo_pago)
    datos_detalle = reporte_dao.getVentasDetalle(fecha_desde, fecha_hasta, metodo_pago)
    datos_metodo_pago = reporte_dao.getVentasPorMetodoPago(fecha_desde, fecha_hasta)
    
    reporte_service = ReporteService()
    chart_data = reporte_service.procesar_ventas_para_grafico(data)
    totales = reporte_service.calcular_totales_ventas(data)
    
    for d in datos_detalle:
        d['gravado_formateado'] = reporte_service._formatear_moneda(d.get('gravado', 0))
        d['iva_formateado'] = reporte_service._formatear_moneda(d.get('iva', 0))
        d['total_formateado'] = reporte_service._formatear_moneda(d.get('total', 0))
        
    for kpi in list(totales.keys()):
        totales[f'{kpi}_formateado'] = reporte_service._formatear_moneda(totales[kpi])
    
    AuditoriaDao().registrar_evento(
        session.get('usuario_id', 0), 
        'REPORT_VIEW', 'reporte_ventas', None, 
        f'Generación reporte ventas {fecha_desde} - {fecha_hasta} (Pago: {metodo_pago})'
    )
    
    return jsonify({
        "success": True,
        "data": data,
        "chart_data": chart_data,
        "totales": totales,
        "datos_detalle": datos_detalle,
        "datos_metodo_pago": datos_metodo_pago
    })

@reporte_api.route('/reporte/ventas/pdf', methods=['GET'])
@role_required(*ROLES_REPORTES)
def reporte_ventas_pdf():
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    metodo_pago = request.args.get('metodo_pago', 'Todos')
    
    if not fecha_desde or not fecha_hasta:
        hoy = date.today()
        fecha_hasta = hoy.strftime('%Y-%m-%d')
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')
        
    reporte_dao = ReporteDao()
    datos_detalle = reporte_dao.getVentasDetalle(fecha_desde, fecha_hasta, metodo_pago)
    datos_agrupados = reporte_dao.getVentasReport(fecha_desde, fecha_hasta, metodo_pago)
    reporte_service = ReporteService()
    totales = reporte_service.calcular_totales_ventas(datos_agrupados)
    
    pdf_bytes = reporte_service.generar_pdf_ventas(fecha_desde, fecha_hasta, metodo_pago, datos_detalle, totales)
    
    AuditoriaDao().registrar_evento(
        session.get('usuario_id', 0), 
        'REPORT_DOWNLOAD', 'reporte_ventas_pdf', None, 
        f'Descarga PDF reporte ventas {fecha_desde} a {fecha_hasta} (Pago: {metodo_pago})'
    )
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Reporte_Ventas_{fecha_desde}_al_{fecha_hasta}.pdf'
    )

@reporte_api.route('/reporte/agendamiento-data', methods=['GET'])
@role_required(*ROLES_REPORTES)
def api_agendamiento_data():
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    if not fecha_desde or not fecha_hasta:
        hoy = date.today()
        fecha_hasta = hoy.strftime('%Y-%m-%d')
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')
        
    reporte_dao = ReporteDao()
    datos_estado = reporte_dao.getAgendamientoReport(fecha_desde, fecha_hasta)
    datos_diarios = reporte_dao.getAgendamientoPorDia(fecha_desde, fecha_hasta)
    
    reporte_service = ReporteService()
    chart_data = reporte_service.procesar_agendamiento_para_grafico(datos_diarios)
    
    kpis = {'total': 0, 'atendidas': 0, 'canceladas': 0, 'ausentes': 0}
    for d in datos_estado:
        kpis['total'] += d['cantidad']
        if d['estado'] in ('ATENDIDA', 'COMPLETADA'):
            kpis['atendidas'] += d['cantidad']
        elif d['estado'] == 'CANCELADA':
            kpis['canceladas'] += d['cantidad']
        elif d['estado'] == 'AUSENTE':
            kpis['ausentes'] += d['cantidad']
            
    AuditoriaDao().registrar_evento(
        session.get('usuario_id', 0), 
        'REPORT_VIEW', 'reporte_agendamiento', None, 
        f'Generación reporte agendamiento {fecha_desde} - {fecha_hasta}'
    )
            
    return jsonify({
        "success": True,
        "totales": kpis,
        "chart_data": chart_data,
        "datos_diarios": datos_diarios
    })

@reporte_api.route('/reporte/agendamiento/pdf', methods=['GET'])
@role_required(*ROLES_REPORTES)
def reporte_agendamiento_pdf():
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    if not fecha_desde or not fecha_hasta:
        hoy = date.today()
        fecha_hasta = hoy.strftime('%Y-%m-%d')
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')
        
    reporte_dao = ReporteDao()
    datos_estado = reporte_dao.getAgendamientoReport(fecha_desde, fecha_hasta)
    datos_diarios = reporte_dao.getAgendamientoPorDia(fecha_desde, fecha_hasta)
    
    kpis = {'total': 0, 'atendidas': 0, 'canceladas': 0, 'ausentes': 0}
    for d in datos_estado:
        kpis['total'] += d['cantidad']
        if d['estado'] in ('ATENDIDA', 'COMPLETADA'):
            kpis['atendidas'] += d['cantidad']
        elif d['estado'] == 'CANCELADA':
            kpis['canceladas'] += d['cantidad']
        elif d['estado'] == 'AUSENTE':
            kpis['ausentes'] += d['cantidad']
            
    reporte_service = ReporteService()
    pdf_bytes = reporte_service.generar_pdf_agendamiento(fecha_desde, fecha_hasta, datos_diarios, kpis)
    
    AuditoriaDao().registrar_evento(
        session.get('usuario_id', 0), 
        'REPORT_DOWNLOAD', 'reporte_agendamiento_pdf', None, 
        f'Descarga PDF reporte agendamiento {fecha_desde} a {fecha_hasta}'
    )
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Reporte_Agendamiento_{fecha_desde}_al_{fecha_hasta}.pdf'
    )

@reporte_api.route('/reporte/consultorio-data', methods=['GET'])
@role_required(*ROLES_REPORTES)
def api_consultorio_data():
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    if not fecha_desde or not fecha_hasta:
        hoy = date.today()
        fecha_hasta = hoy.strftime('%Y-%m-%d')
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')
        
    reporte_dao = ReporteDao()
    especialidades = reporte_dao.getConsultasPorEspecialidad(fecha_desde, fecha_hasta)
    top_diagnosticos = reporte_dao.getTopDiagnosticos(fecha_desde, fecha_hasta)
    
    reporte_service = ReporteService()
    chart_data = reporte_service.procesar_consultorio_para_grafico(especialidades)
    
    total_consultas = sum(e['cantidad'] for e in especialidades)
    
    try:
        f_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
        f_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        dias = (f_hasta - f_desde).days + 1
        promedio = round(total_consultas / dias, 1) if dias > 0 else total_consultas
    except:
        promedio = total_consultas
        
    kpis = {'total_consultas': total_consultas, 'promedio_diario': promedio}
    
    AuditoriaDao().registrar_evento(
        session.get('usuario_id', 0), 
        'REPORT_VIEW', 'reporte_consultorio', None, 
        f'Generación reporte consultorio {fecha_desde} - {fecha_hasta}'
    )
            
    return jsonify({
        "success": True,
        "totales": kpis,
        "chart_data": chart_data,
        "especialidades": especialidades,
        "top_diagnosticos": top_diagnosticos
    })

@reporte_api.route('/reporte/consultorio/pdf', methods=['GET'])
@role_required(*ROLES_REPORTES)
def reporte_consultorio_pdf():
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    if not fecha_desde or not fecha_hasta:
        hoy = date.today()
        fecha_hasta = hoy.strftime('%Y-%m-%d')
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')
        
    reporte_dao = ReporteDao()
    especialidades = reporte_dao.getConsultasPorEspecialidad(fecha_desde, fecha_hasta)
    total_consultas = sum(e['cantidad'] for e in especialidades)
    
    try:
        f_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
        f_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        dias = (f_hasta - f_desde).days + 1
        promedio = round(total_consultas / dias, 1) if dias > 0 else total_consultas
    except:
        promedio = total_consultas
        
    kpis = {'total_consultas': total_consultas, 'promedio_diario': promedio}
    
    reporte_service = ReporteService()
    pdf_bytes = reporte_service.generar_pdf_consultorio(fecha_desde, fecha_hasta, especialidades, kpis)
    
    AuditoriaDao().registrar_evento(
        session.get('usuario_id', 0), 
        'REPORT_DOWNLOAD', 'reporte_consultorio_pdf', None, 
        f'Descarga PDF reporte consultorio {fecha_desde} a {fecha_hasta}'
    )
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Reporte_Consultorio_{fecha_desde}_al_{fecha_hasta}.pdf'
    )
