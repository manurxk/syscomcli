import io
from datetime import date

from flask import Blueprint, render_template, session, request, send_file
from app.auth.utils.decorators import role_required
from app.dao.mantenimiento.seguridad.menu.MenuDao import MenuDao
from app.services.ayuda_service import AyudaService

ayudamod = Blueprint('ayuda', __name__, template_folder='templates')

# El manual es para cualquier usuario logueado; qué secciones ve lo decide roles_paginas.
ROLES_AYUDA = ('SUPERADMIN', 'ADMINISTRADOR', 'RECEPCION', 'CLINICO', 'VENTAS')

# Sección del manual por página del menú (clave = paginas.pag_direccion).
# 'endpoints': pantallas desde las que el botón de ayuda abre directo esa sección.
SECCIONES_MANUAL = {
    'paciente.pacienteIndex': {
        'template': 'ayuda-secciones/pacientes.html',
        'endpoints': ('paciente.pacienteIndex', 'paciente.pacienteAgregar'),
    },
    'agenda_horarios.agendaHorariosIndex': {
        'template': 'ayuda-secciones/agenda_medica.html',
        'endpoints': ('agenda_horarios.agendaHorariosIndex',),
    },
    'cita.citaIndex': {
        'template': 'ayuda-secciones/citas.html',
        'endpoints': ('cita.citaIndex', 'cita.citaAgregar'),
    },
    'lista_espera.listaEsperaIndex': {
        'template': 'ayuda-secciones/lista_espera.html',
        'endpoints': ('lista_espera.listaEsperaIndex',),
    },
    'reporte.reporteAgendamiento': {
        'template': 'ayuda-secciones/reporte_agendamiento.html',
        'endpoints': ('reporte.reporteAgendamiento',),
    },
    'mi_agenda.miAgendaIndex': {
        'template': 'ayuda-secciones/mi_agenda.html',
        'endpoints': ('mi_agenda.miAgendaIndex',),
    },
    'consulta.consultaIndex': {
        'template': 'ayuda-secciones/consultas.html',
        'endpoints': ('consulta.consultaIndex', 'consulta.consultaAgregar'),
    },
    'pei.peiIndex': {
        'template': 'ayuda-secciones/pei.html',
        'endpoints': ('pei.peiIndex', 'pei.peiAgregarNuevo', 'pei.peiAgregar'),
    },
    'ficha.fichaIndex': {
        'template': 'ayuda-secciones/fichas_medicas.html',
        'endpoints': ('ficha.fichaIndex', 'ficha.fichaPaciente'),
    },
    'reporte.reporteConsultorio': {
        'template': 'ayuda-secciones/reporte_consultorio.html',
        'endpoints': ('reporte.reporteConsultorio',),
    },
    'timbrado.timbradoIndex': {
        'template': 'ayuda-secciones/timbrados.html',
        'endpoints': ('timbrado.timbradoIndex',),
    },
    'punto_expedicion.puntoExpedicionIndex': {
        'template': 'ayuda-secciones/puntos_expedicion.html',
        'endpoints': ('punto_expedicion.puntoExpedicionIndex',),
    },
    'pedido.pedidoIndex': {
        'template': 'ayuda-secciones/pedidos.html',
        'endpoints': ('pedido.pedidoIndex', 'pedido.pedidoAgregar'),
    },
    'presupuesto.presupuestoIndex': {
        'template': 'ayuda-secciones/presupuestos.html',
        'endpoints': ('presupuesto.presupuestoIndex', 'presupuesto.presupuestoAgregar'),
    },
    'apertura_cierre_caja.cajaEstado': {
        'template': 'ayuda-secciones/caja_estado.html',
        'endpoints': ('apertura_cierre_caja.cajaEstado',),
    },
    'apertura_cierre_caja.cajaHistorial': {
        'template': 'ayuda-secciones/caja_historial.html',
        'endpoints': ('apertura_cierre_caja.cajaHistorial',),
    },
    'arqueo_caja.arqueoIndex': {
        'template': 'ayuda-secciones/arqueos.html',
        'endpoints': ('arqueo_caja.arqueoIndex', 'arqueo_caja.arqueoAgregar'),
    },
    'factura.facturaIndex': {
        'template': 'ayuda-secciones/facturas.html',
        'endpoints': ('factura.facturaIndex', 'factura.facturaAgregar'),
    },
    'remision.remisionIndex': {
        'template': 'ayuda-secciones/remisiones.html',
        'endpoints': ('remision.remisionIndex', 'remision.remisionAgregar'),
    },
    'nota_credito.notaCreditoIndex': {
        'template': 'ayuda-secciones/notas_credito.html',
        'endpoints': ('nota_credito.notaCreditoIndex', 'nota_credito.notaCreditoAgregar'),
    },
    'nota_debito.notaDebitoIndex': {
        'template': 'ayuda-secciones/notas_debito.html',
        'endpoints': ('nota_debito.notaDebitoIndex', 'nota_debito.notaDebitoAgregar'),
    },
    'cuenta_cobrar.cuentaCobrarIndex': {
        'template': 'ayuda-secciones/cuentas_cobrar.html',
        'endpoints': ('cuenta_cobrar.cuentaCobrarIndex',),
    },
    'cobranza.cobranzaIndex': {
        'template': 'ayuda-secciones/cobranzas.html',
        'endpoints': ('cobranza.cobranzaIndex', 'cobranza.cobranzaAgregar'),
    },
    'recaudacion.recaudacionIndex': {
        'template': 'ayuda-secciones/recaudaciones.html',
        'endpoints': ('recaudacion.recaudacionIndex', 'recaudacion.recaudacionAgregar'),
    },
    'libro_ventas.libroVentasIndex': {
        'template': 'ayuda-secciones/libro_ventas.html',
        'endpoints': ('libro_ventas.libroVentasIndex',),
    },
    'reporte.reporteVentas': {
        'template': 'ayuda-secciones/reporte_ventas.html',
        'endpoints': ('reporte.reporteVentas',),
    },
}


def _armar_manual():
    """Secciones del manual visibles para los roles del usuario, en el orden del menú."""
    roles = [(r or "").strip().upper() for r in session.get("roles", [])]
    paginas = MenuDao().getMenuParaRoles(roles) or []

    secciones = []
    sin_guia = []
    for pagina in paginas:
        seccion = SECCIONES_MANUAL.get(pagina["endpoint"])
        if seccion:
            secciones.append({
                "id": pagina["endpoint"].replace(".", "-"),
                "titulo": pagina["title"],
                "grupo": pagina["grupo_menu"] or "General",
                "template": seccion["template"],
            })
        else:
            sin_guia.append(pagina["title"])

    return secciones, sin_guia


def _seccion_desde(endpoint, secciones):
    """Id de la sección de la pantalla desde donde se pidió ayuda, si el rol la ve."""
    visibles = {s["id"] for s in secciones}
    for pagina, seccion in SECCIONES_MANUAL.items():
        if endpoint in seccion["endpoints"] and pagina.replace(".", "-") in visibles:
            return pagina.replace(".", "-")
    return None


@ayudamod.route('/manual')
@role_required(*ROLES_AYUDA)
def ayudaManual():
    """Vista previa del manual (se muestra dentro del modal de ayuda de base.html)."""
    secciones, sin_guia = _armar_manual()
    return render_template('ayuda-manual.html',
                           secciones=secciones,
                           sin_guia=sin_guia,
                           seccion_activa=_seccion_desde(request.args.get('desde'), secciones),
                           es_pdf=False,
                           fecha=date.today().strftime('%d/%m/%Y'))


@ayudamod.route('/manual/pdf')
@role_required(*ROLES_AYUDA)
def ayudaManualPdf():
    """Mismo manual que la vista previa, descargado como PDF."""
    secciones, sin_guia = _armar_manual()
    html_renderizado = render_template('ayuda-manual.html',
                                       secciones=secciones,
                                       sin_guia=sin_guia,
                                       seccion_activa=None,
                                       es_pdf=True,
                                       fecha=date.today().strftime('%d/%m/%Y'))
    pdf_bytes = AyudaService().generar_pdf_manual(html_renderizado)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Guia_de_uso_{session.get('grupo', 'SYSCLIN')}.pdf"
    )
