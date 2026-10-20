"""Alertas por correo e informe semanal de la auditoría de cambios en datos (PDF 9 + 6, paso 6).

- Qué ve cada destinatario: los módulos que su rol ve en detalle (alcance_cambios); el Superadministrador no
  recibe nada del módulo clínico.
- Alerta: un cambio es alertable si es una anulación (factura, nota de crédito/débito, cobranza) o si se hizo
  fuera del horario de atención de la empresa (empresa.horario_atencion_tramos). Las tareas automáticas
  (rol SISTEMA) no cuentan como "fuera de horario".
- Informe semanal: cantidades por módulo y tabla, anulaciones, cambios fuera de horario y eventos de seguridad,
  en PDF (mismo mecanismo que los reportes: plantilla Jinja + ReporteService._render_pdf).
"""
from datetime import date, datetime, timedelta
from html import escape

from flask import current_app

from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.services.reporte_service import ReporteService
from app.utils.auditoria_constantes import alcance_cambios, get_label

ETIQUETA_MODULO = {'CLINICO': 'Clínico', 'AGENDAMIENTO': 'Agendamiento', 'VENTAS': 'Ventas', 'SEGURIDAD': 'Seguridad'}
ETIQUETA_OPERACION = {'INSERT': 'Alta', 'UPDATE': 'Modificación', 'DELETE': 'Baja'}


def modulos_destinatario(roles):
    """Módulos que un destinatario (Administrador / Superadministrador) ve en detalle."""
    return [m for m, nivel in alcance_cambios(roles).items() if nivel == 'detalle']


def semana_anterior(hoy=None):
    """Lunes a domingo de la semana anterior a hoy."""
    hoy = hoy or date.today()
    lunes = hoy - timedelta(days=hoy.weekday() + 7)
    return lunes, lunes + timedelta(days=6)


def motivos_alerta(cambio, tramos, empresadao):
    """Por qué un cambio merece alerta: 'Anulación' y/o 'Fuera de horario' (lista vacía = no alertar)."""
    motivos = []
    if cambio.get('es_anulacion'):
        motivos.append('Anulación')
    if (cambio.get('roles') or '') != 'SISTEMA' and not empresadao.estaEnHorario(cambio['fecha_cambio'], tramos=tramos):
        motivos.append('Fuera de horario')
    return motivos


def correo_alerta(alertas):
    """Asunto, texto y HTML del correo con la lista de cambios alertados."""
    anulaciones = sum('Anulación' in a['motivos'] for a in alertas)
    fuera = sum('Fuera de horario' in a['motivos'] for a in alertas)
    asunto = f"Sysclin · Alerta de auditoría: {anulaciones} anulación(es), {fuera} cambio(s) fuera de horario"
    lineas = [f"- {a['fecha_cambio']:%d/%m/%Y %H:%M} · {', '.join(a['motivos'])} · "
              f"{ETIQUETA_MODULO.get(a['modulo'], a['modulo'])} · {a['tabla']} #{a['id_registro']} · "
              f"{ETIQUETA_OPERACION.get(a['operacion'], a['operacion'])} · {a.get('usu_nick') or a.get('roles') or 'sin usuario'} · "
              f"IP {a.get('ip_origen') or '-'}" for a in alertas]
    texto = ("Se registraron estos cambios que requieren revisión:\n\n" + "\n".join(lineas) +
             "\n\nEl detalle (dato anterior y nuevo) está en Sysclin, Auditoría → Cambios en datos.")
    filas = "".join(
        f"<tr><td>{a['fecha_cambio']:%d/%m/%Y %H:%M}</td><td><b>{escape(', '.join(a['motivos']))}</b></td>"
        f"<td>{escape(ETIQUETA_MODULO.get(a['modulo'], a['modulo']))}</td><td>{escape(a['tabla'])} #{escape(str(a['id_registro']))}</td>"
        f"<td>{escape(ETIQUETA_OPERACION.get(a['operacion'], a['operacion']))}</td>"
        f"<td>{escape(a.get('usu_nick') or a.get('roles') or 'sin usuario')}</td><td>{escape(a.get('ip_origen') or '-')}</td></tr>"
        for a in alertas)
    html = (f"<p>Se registraron estos cambios que requieren revisión:</p>"
            f"<table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse;font-family:Arial;font-size:12px'>"
            f"<tr style='background:#eee'><th>Fecha</th><th>Motivo</th><th>Módulo</th><th>Registro</th><th>Operación</th>"
            f"<th>Usuario</th><th>IP</th></tr>{filas}</table>"
            f"<p>El detalle (dato anterior y nuevo) está en Sysclin, <b>Auditoría → Cambios en datos</b>.</p>")
    return asunto, texto, html


def armar_informe(modulos, fecha_desde, fecha_hasta):
    """Datos del informe de auditoría de un período, limitados a los módulos indicados."""
    dao, empresadao = AuditoriaDao(), EmpresaDao()
    desde, hasta = str(fecha_desde), str(fecha_hasta)
    tramos = empresadao.getTramosHorario()
    cambios = dao.getCambiosPeriodo(modulos, desde, hasta)
    for c in cambios:
        c['motivos'] = motivos_alerta(c, tramos, empresadao)
    empresa = empresadao.getEmpresaPrincipal() or {}
    return {
        'empresa': empresa.get('nombre_comercial') or empresa.get('razon_social') or 'Sysclin',
        'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta,
        'generado': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'modulos': [ETIQUETA_MODULO[m] for m in modulos],
        'resumen': dao.getResumenCambios(modulos, desde, hasta),
        'anulaciones': [c for c in cambios if 'Anulación' in c['motivos']],
        'fuera_horario': [c for c in cambios if 'Fuera de horario' in c['motivos']],
        'seguridad': [dict(e, etiqueta=get_label(e['accion'])) for e in dao.getResumenEventosSeguridad(desde, hasta)],
        'ips_sospechosas': dao.getIpsSospechosas(desde, hasta),
        'etiqueta_modulo': ETIQUETA_MODULO, 'etiqueta_operacion': ETIQUETA_OPERACION,
    }


def generar_pdf_informe(datos):
    """PDF del informe (bytes), con la plantilla pdf/informe-auditoria-semanal-pdf.html.
    Se usa el motor de plantillas directo y no render_template: este último ejecuta los context processors
    (el menú lateral lee la sesión) y falla en la tarea programada, que no tiene petición web."""
    html = current_app.jinja_env.get_template('pdf/informe-auditoria-semanal-pdf.html').render(**datos)
    return ReporteService()._render_pdf(html)
