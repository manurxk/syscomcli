import io
import os
from datetime import date

from flask import Blueprint, render_template, session, request, send_file, url_for, current_app
from markupsafe import Markup, escape
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
    'funcionario.funcionarioIndex': {
        'template': 'ayuda-secciones/funcionarios.html',
        'endpoints': ('funcionario.funcionarioIndex', 'funcionario.funcionarioAgregar'),
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


# Manual de seguridad: solo para quien administra el sistema.
ROLES_SEGURIDAD = ('SUPERADMIN', 'ADMINISTRADOR')

# Capítulos del manual de seguridad, en orden.
SECCIONES_SEGURIDAD = (
    {'id': 'objetivo', 'titulo': 'Objetivo, alcance y clasificación de la información', 'template': 'ayuda-seguridad-secciones/objetivo.html'},
    {'id': 'componentes', 'titulo': 'Componentes del sistema (contenedores)', 'template': 'ayuda-seguridad-secciones/componentes.html'},
    {'id': 'configuracion', 'titulo': 'Configuración (.env)', 'template': 'ayuda-seguridad-secciones/configuracion.html'},
    {'id': 'contenedores', 'titulo': 'Manejo de contenedores y reactivación del sistema', 'template': 'ayuda-seguridad-secciones/contenedores.html'},
    {'id': 'contrasenas', 'titulo': 'Contraseñas y autenticación', 'template': 'ayuda-seguridad-secciones/contrasenas.html'},
    {'id': 'roles', 'titulo': 'Roles y control de acceso', 'template': 'ayuda-seguridad-secciones/roles.html'},
    {'id': 'base-datos', 'titulo': 'Base de datos: usuarios, contraseñas y migraciones', 'template': 'ayuda-seguridad-secciones/base_datos.html'},
    {'id': 'aplicacion', 'titulo': 'Seguridad de la aplicación', 'template': 'ayuda-seguridad-secciones/aplicacion.html'},
    {'id': 'https', 'titulo': 'HTTPS, red y despliegue en el servidor', 'template': 'ayuda-seguridad-secciones/https.html'},
    {'id': 'backups', 'titulo': 'Backups y restauración', 'template': 'ayuda-seguridad-secciones/backups.html'},
    {'id': 'auditoria', 'titulo': 'Auditoría y chequeo periódico', 'template': 'ayuda-seguridad-secciones/auditoria.html'},
    {'id': 'dependencias', 'titulo': 'Gestión de vulnerabilidades (dependencias)', 'template': 'ayuda-seguridad-secciones/dependencias.html'},
    {'id': 'incidentes', 'titulo': 'Respuesta a incidentes', 'template': 'ayuda-seguridad-secciones/incidentes.html'},
    {'id': 'problemas', 'titulo': 'Solución de problemas', 'template': 'ayuda-seguridad-secciones/problemas.html'},
    {'id': 'riesgos', 'titulo': 'Riesgos aceptados y normativa', 'template': 'ayuda-seguridad-secciones/riesgos.html'},
)

# Anexo de scripts: se leen del repositorio al generar el manual, así nunca queda desactualizado.
# Ninguno contiene secretos (las claves viven en .env, que no se incluye).
SCRIPTS_SEGURIDAD = (
    ('dock/docker-compose.yml', 'Definición de los contenedores (desarrollo)'),
    ('dock/docker-compose.servidor.yml', 'Ajustes del servidor: puertos cerrados y HSTS'),
    ('dock/Dockerfile', 'Imagen de la aplicación y modo de arranque'),
    ('.env.example', 'Plantilla del .env, sin valores'),
    ('dock/backup/entrypoint.sh', 'Servicio de backup: ciclo cada 24 h'),
    ('dock/backup/backup.sh', 'Backup cifrado con GPG y rotación'),
    ('dock/backup/restore_test.sh', 'Prueba de restauración'),
    ('dock/nginx/conf.d/default.conf', 'Proxy HTTPS (nginx)'),
    ('dock/nginx/hsts.conf', 'HSTS (solo servidor)'),
    ('dock/nginx/generar_cert_local.sh', 'Certificado autofirmado de desarrollo'),
    ('migrations/103_rol_sysclin_app.sql', 'Rol de la aplicación con permisos mínimos'),
)


def _leer_scripts():
    """Contenido actual de los scripts del anexo; si alguno falta, se indica en lugar de fallar."""
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    scripts = []
    for ruta, descripcion in SCRIPTS_SEGURIDAD:
        try:
            with open(os.path.join(raiz, ruta), encoding='utf-8') as f:
                contenido = f.read()
        except OSError:
            contenido = None
        scripts.append({'id': 'script-' + ruta.replace('/', '-').replace('.', '-'),
                        'ruta': ruta, 'descripcion': descripcion, 'contenido': contenido})
    return scripts


def _rol_solicitado():
    """Rol pedido por ?rol= (manuales por rol del inicio del administrador).
    Solo lo pueden usar ADMINISTRADOR/SUPERADMIN; el de SUPERADMIN, solo un Superadministrador."""
    rol = (request.args.get("rol") or "").strip().upper()
    roles_sesion = {(r or "").strip().upper() for r in session.get("roles", [])}
    if rol not in ROLES_AYUDA or not roles_sesion & {"ADMINISTRADOR", "SUPERADMIN"}:
        return None
    if rol == "SUPERADMIN" and "SUPERADMIN" not in roles_sesion:
        return None
    return rol


def _armar_manual(rol=None):
    """Secciones del manual visibles para los roles del usuario (o para el rol pedido), en el orden del menú."""
    roles = [rol] if rol else [(r or "").strip().upper() for r in session.get("roles", [])]
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


def _figura(es_pdf):
    """Captura de pantalla de la guía (generadas con docs/scripts/capturas_manual.py en static/img/ayuda/).
    La vista previa la pide por URL; el PDF, por ruta de archivo. Si la imagen no existe, no muestra nada."""
    def figura(ruta, pie=''):
        archivo = os.path.join(current_app.static_folder, 'img', 'ayuda', *ruta.split('/'))
        if not os.path.isfile(archivo):
            return ''
        src = ('file://' + archivo) if es_pdf else url_for('static', filename=f'img/ayuda/{ruta}')
        pie_html = f'<figcaption>{escape(pie)}</figcaption>' if pie else ''
        return Markup(f'<figure class="captura"><img src="{escape(src)}" alt="{escape(pie)}">{pie_html}</figure>')
    return figura


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
    rol = _rol_solicitado()
    secciones, sin_guia = _armar_manual(rol)
    return render_template('ayuda-manual.html',
                           secciones=secciones,
                           sin_guia=sin_guia,
                           seccion_activa=_seccion_desde(request.args.get('desde'), secciones),
                           logo_base64=AyudaService().logo_base64(),
                           figura=_figura(False),
                           es_pdf=False,
                           perfil=rol or session.get('grupo'),
                           fecha=date.today().strftime('%d/%m/%Y'))


@ayudamod.route('/manual/pdf')
@role_required(*ROLES_AYUDA)
def ayudaManualPdf():
    """Mismo manual que la vista previa, descargado como PDF."""
    rol = _rol_solicitado()
    perfil = rol or session.get('grupo')
    secciones, sin_guia = _armar_manual(rol)
    html_renderizado = render_template('ayuda-manual.html',
                                       secciones=secciones,
                                       sin_guia=sin_guia,
                                       seccion_activa=None,
                                       logo_base64=AyudaService().logo_base64(),
                                       figura=_figura(True),
                                       es_pdf=True,
                                       perfil=perfil,
                                       fecha=date.today().strftime('%d/%m/%Y'))
    pdf_bytes = AyudaService().generar_pdf_manual(html_renderizado)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Guia_de_uso_{perfil or 'SYSCLIN'}.pdf"
    )


@ayudamod.route('/seguridad')
@role_required(*ROLES_SEGURIDAD)
def ayudaSeguridad():
    """Vista previa del manual de seguridad y operación (modal del inicio del administrador)."""
    return render_template('ayuda-seguridad.html',
                           secciones=SECCIONES_SEGURIDAD,
                           scripts=_leer_scripts(),
                           logo_base64=AyudaService().logo_base64(),
                           es_pdf=False,
                           fecha=date.today().strftime('%d/%m/%Y'))


@ayudamod.route('/seguridad/pdf')
@role_required(*ROLES_SEGURIDAD)
def ayudaSeguridadPdf():
    """Mismo manual de seguridad, descargado como PDF."""
    html_renderizado = render_template('ayuda-seguridad.html',
                                       secciones=SECCIONES_SEGURIDAD,
                                       scripts=_leer_scripts(),
                                       logo_base64=AyudaService().logo_base64(),
                                       es_pdf=True,
                                       fecha=date.today().strftime('%d/%m/%Y'))
    pdf_bytes = AyudaService().generar_pdf_manual(html_renderizado)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Manual_de_seguridad_SYSCLIN_{date.today().strftime('%Y%m%d')}.pdf"
    )
