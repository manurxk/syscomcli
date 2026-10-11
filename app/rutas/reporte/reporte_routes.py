from flask import Blueprint, render_template, session, request
from datetime import date
from app.auth.utils.decorators import role_required
from app.dao.reporte.ReporteDao import ReporteDao
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion

reportemod = Blueprint('reporte', __name__, template_folder='templates')

# Roles autorizados por reporte (ver docs_reestructuracion/sql_nueva_bd/seeds/04_seed_roles.sql)
ROLES_DASHBOARD = ('ADMINISTRADOR', 'SUPERADMIN')
ROLES_VENTAS = ('ADMINISTRADOR', 'SUPERADMIN', 'VENTAS')
ROLES_AGENDAMIENTO = ('ADMINISTRADOR', 'SUPERADMIN', 'RECEPCION')
ROLES_CONSULTORIO = ('ADMINISTRADOR', 'SUPERADMIN', 'CLINICO')

@reportemod.route('/index')
@role_required(*ROLES_DASHBOARD)
def reporteIndex():
    """Ruta index del módulo de reportes."""
    reporte_dao = ReporteDao()
    metricas = reporte_dao.getMetricasDashboard()

    # Registro de auditoría
    AuditoriaDao().registrar_evento(
        id_usuario=session.get('id_usuario'),
        accion=AuditAccion.REPORT_VIEW,
        detalle='Visita al dashboard central de reportes',
        ip_origen=request.remote_addr
    )

    return render_template('reportes-index.html', metricas=metricas)

@reportemod.route('/ventas')
@role_required(*ROLES_VENTAS)
def reporteVentas():
    """Ruta de vista del reporte de ventas."""
    hoy = date.today()
    primer_dia = hoy.replace(day=1).strftime('%Y-%m-%d')

    return render_template('reporte-ventas.html',
                         fecha_desde=primer_dia,
                         fecha_hasta=hoy.strftime('%Y-%m-%d'))

@reportemod.route('/agendamiento')
@role_required(*ROLES_AGENDAMIENTO)
def reporteAgendamiento():
    """Vista de reporte de Agendamiento."""
    hoy = date.today()
    primer_dia = hoy.replace(day=1).strftime('%Y-%m-%d')
    return render_template('reporte-agendamiento.html',
                           fecha_desde=primer_dia,
                           fecha_hasta=hoy.strftime('%Y-%m-%d'))

@reportemod.route('/consultorio')
@role_required(*ROLES_CONSULTORIO)
def reporteConsultorio():
    """Vista de reporte de Consultorio."""
    hoy = date.today()
    primer_dia = hoy.replace(day=1).strftime('%Y-%m-%d')
    return render_template('reporte-consultorio.html',
                           fecha_desde=primer_dia,
                           fecha_hasta=hoy.strftime('%Y-%m-%d'))
