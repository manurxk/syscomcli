from flask import Blueprint, render_template, session
from datetime import date
from app.auth.utils.decorators import role_required
from app.dao.modulos.reporte.ReporteDao import ReporteDao
from app.dao.AuditoriaDao import AuditoriaDao

reporte_mod = Blueprint('reporte', __name__, template_folder='templates')

# Lista de roles autorizados para ver reportes
ROLES_REPORTES = ['SUPERADMINISTRADOR', 'ADMINISTRADOR', 'ADMIN', 'VENTAS', 'RECEPCIONISTA', 'ESPECIALISTA', 'CAJA']

@reporte_mod.route('/index')
@role_required(*ROLES_REPORTES)
def reportes_index():
    """Ruta index del módulo de reportes."""
    reporte_dao = ReporteDao()
    metricas = reporte_dao.getMetricasDashboard()
    
    # Registro de auditoría
    AuditoriaDao().registrar_evento(
        session.get('usuario_id', 0), 
        'REPORT_VIEW', 'reportes_index', None, 'Visita al dashboard central de reportes'
    )
    
    return render_template('reportes-index.html', metricas=metricas)

@reporte_mod.route('/ventas')
@role_required(*ROLES_REPORTES)
def reporte_ventas():
    """Ruta de vista del reporte de ventas."""
    hoy = date.today()
    primer_dia = hoy.replace(day=1).strftime('%Y-%m-%d')
    
    return render_template('reporte-ventas.html', 
                         fecha_desde=primer_dia, 
                         fecha_hasta=hoy.strftime('%Y-%m-%d'))

@reporte_mod.route('/agendamiento')
@role_required(*ROLES_REPORTES)
def reporte_agendamiento():
    """Vista de reporte de Agendamiento."""
    hoy = date.today()
    primer_dia = hoy.replace(day=1).strftime('%Y-%m-%d')
    return render_template('reporte-agendamiento.html',
                           fecha_desde=primer_dia,
                           fecha_hasta=hoy.strftime('%Y-%m-%d'))

@reporte_mod.route('/consultorio')
@role_required(*ROLES_REPORTES)
def reporte_consultorio():
    """Vista de reporte de Consultorio."""
    hoy = date.today()
    primer_dia = hoy.replace(day=1).strftime('%Y-%m-%d')
    return render_template('reporte-consultorio.html',
                           fecha_desde=primer_dia,
                           fecha_hasta=hoy.strftime('%Y-%m-%d'))
