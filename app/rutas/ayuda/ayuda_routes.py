import io
import json
import os
import re
from functools import lru_cache
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
    'reporte.reporteIndex': {
        'template': 'ayuda-secciones/reportes.html',
        'endpoints': ('reporte.reporteIndex',),
    },
    'usuario.usuarioIndex': {
        'template': 'ayuda-secciones/usuarios.html',
        'endpoints': ('usuario.usuarioIndex', 'usuario.usuarioAgregar', 'usuario.usuarioDetalle'),
    },
    # Cada catálogo abre la misma sección: todos funcionan igual (Agregar / Editar / Activo)
    'referenciales.referencialesIndex': {
        'template': 'ayuda-secciones/referenciales.html',
        'endpoints': ('referenciales.referencialesIndex',
                      'cargo.cargoIndex', 'especialidad.especialidadIndex', 'empresa.empresaIndex',
                      'sede.sedeIndex', 'consultorio.consultorioIndex', 'signo.signoIndex',
                      'sintoma.sintomaIndex', 'diagnostico.diagnosticoIndex', 'medicamento.medicamentoIndex',
                      'tipo_analisis.tipoAnalisisIndex', 'tipo_estudio.tipoEstudioIndex',
                      'tipo_procedimiento.tipoProcedimientoIndex', 'tipo_tratamiento.tipoTratamientoIndex',
                      'tipo_certificado_medico.tipoCertificadoMedicoIndex', 'instrumento.instrumentoIndex',
                      'insumo.insumoIndex', 'item_servicio.itemServicioIndex', 'moneda.monedaIndex',
                      'forma_cobro.formaCobroIndex', 'condicion_venta.condicionVentaIndex',
                      'tipo_comprobante.tipoComprobanteIndex', 'tipo_impuesto.tipoImpuestoIndex',
                      'tipo_item.tipoItemIndex', 'marca_tarjeta.marcaTarjetaIndex',
                      'entidad_adherida.entidadAdheridaIndex', 'entidad_emisora.entidadEmisoraIndex',
                      'estado_factura.estadoFacturaIndex', 'caja.cajaIndex', 'deposito.depositoIndex'),
    },
    'permisos.permisosIndex': {
        'template': 'ayuda-secciones/permisos.html',
        'endpoints': ('permisos.permisosIndex',),
    },
    'menu.menuIndex': {
        'template': 'ayuda-secciones/menu.html',
        'endpoints': ('menu.menuIndex',),
    },
    # Accesos pasó a ser la pestaña "Sesiones y usuarios" de Auditoría (PDF 9 + 6, paso 5): su ayuda está ahí
    'auditoria.auditoriaIndex': {
        'template': 'ayuda-secciones/auditoria.html',
        'endpoints': ('auditoria.auditoriaIndex', 'acceso.accesoIndex'),
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
    {'id': 'avisos', 'titulo': 'Avisos de validación del sistema', 'template': 'ayuda-seguridad-secciones/avisos_validacion.html'},
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
    ('migrations/17_rol_sysclin_app.sql', 'Rol de la aplicación con permisos mínimos'),
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


def _roles_del_manual(rol=None):
    """Roles con los que se arma el manual: el pedido por ?rol= o los de la sesión."""
    return [rol] if rol else [(r or "").strip().upper() for r in session.get("roles", [])]


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


# Tipos de aviso de validación: se reconocen por el texto del mensaje (primera coincidencia).
# 'capturas' = (archivo, pantalla de ejemplo) en static/img/ayuda/mensajes/ (las toma docs/scripts/capturas_manual.py).
TIPOS_MENSAJE = (
    {'id': 'obligatorio', 'titulo': 'Campo obligatorio', 'capturas': (('obligatorio_especialidad.jpg', 'Especialidades'), ('obligatorio_cargo.jpg', 'Cargos')),
     'patron': r'es obligatori|no puede estar vac|debe indicar|debe seleccionar|debe tener al menos|requerid',
     'significa': 'Dejó vacío un dato que el sistema necesita para guardar.',
     'ejemplo': 'El campo "Descripción" es obligatorio.',
     'hacer': 'Complete el campo que nombra el aviso y presione Guardar de nuevo.'},
    {'id': 'caracteres', 'titulo': 'Caracteres no permitidos', 'capturas': (('caracteres_especialidad.jpg', 'Especialidades'), ('caracteres_cargo.jpg', 'Cargos')),
     'patron': r'caracteres|solo puede contener|inv.lid(?!o? ?para)',
     'significa': 'El dato trae símbolos o un formato que ese campo no admite.',
     'ejemplo': 'El campo "Descripción" contiene caracteres no permitidos. Use solo letras, números y espacios.',
     'hacer': 'Quite los símbolos; el aviso indica qué sí se puede escribir en ese campo.'},
    {'id': 'existe', 'titulo': 'El dato ya existe', 'capturas': (('ya_existe_especialidad.jpg', 'Especialidades'), ('ya_existe_cargo.jpg', 'Cargos')),
     'patron': r'^ya existe|ya est. registrad|duplicad',
     'significa': 'Ese dato ya está cargado y no se puede repetir.',
     'ejemplo': 'Ya existe una especialidad "PSICOLOGÍA".',
     'hacer': 'Búsquelo en el listado y edítelo, o use otro valor.'},
    {'id': 'valor', 'titulo': 'Valor fuera de lo permitido', 'capturas': (('valor_agenda_medica.jpg', 'Agenda Médica (bloqueo de días)'),),
     'patron': r'mayor|menor|negativ|cero|rango|exced|supera|m.ximo|m.nimo|fecha|vigen|vencid|pasad|formato',
     'significa': 'El número o la fecha no cumple la condición de la operación.',
     'ejemplo': 'El fin del bloqueo debe ser posterior al inicio.',
     'hacer': 'Corrija el valor según lo que indica el aviso.'},
    {'id': 'estado', 'titulo': 'Operación no permitida en este momento', 'capturas': (('estado_citas.jpg', 'Citas (cambio de estado)'),),
     'patron': r'estado|no se puede|no puede|no es posible|no se permite|anulad|cerrad|bloquead|pendiente',
     'significa': 'El registro está en un estado que no admite esa acción (por ejemplo, ya anulado o con la caja cerrada).',
     'ejemplo': "Una cita en estado 'Confirmada' no puede pasar a 'COMPLETADA'.",
     'hacer': 'Revise el estado del registro; el aviso explica qué falta resolver antes.'},
)


@lru_cache(maxsize=1)
def _nombres_catalogos():
    """Nombre de cada catálogo como lo ve el usuario (títulos de la pantalla Referenciales), por blueprint."""
    ruta = os.path.join(os.path.dirname(__file__), '..', 'mantenimiento', 'referenciales',
                        'templates', 'referenciales-index.html')
    try:
        with open(ruta, encoding='utf-8') as f:
            html = f.read()
    except OSError:
        return {}
    return {m.group(1): m.group(2).strip() for m in
            re.finditer(r"url_for\('(\w+)\.\w+'\).*?<h6[^>]*>([^<]+)</h6>", html, re.S)}


def _tipo_de(mensaje):
    """Id del tipo de aviso al que pertenece el mensaje, o 'otro'."""
    for tipo in TIPOS_MENSAJE:
        if re.search(tipo['patron'], mensaje, re.IGNORECASE):
            return tipo['id']
    return 'otro'


def _mensajes_validacion(secciones, roles):
    """Anexo del manual: explica una vez cada tipo de aviso y en qué pantallas aparece (las visibles para
    los roles). Origen de los mensajes: mensajes_validacion.json, que se regenera con
    docs/scripts/extraer_mensajes_validacion.py --escribir."""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'mensajes_validacion.json'), encoding='utf-8') as f:
            filas = json.load(f)
    except (OSError, ValueError):
        return []
    roles = set(roles)
    pantallas = {}  # tipo -> {pantalla: {detalle}}
    for fila in filas:
        if fila['roles'] and not roles & set(fila['roles']):
            continue
        tipo = _tipo_de(fila['mensaje'])
        for sec in secciones:
            pagina = sec['id'].replace('-', '.', 1)
            endpoints = SECCIONES_MANUAL.get(pagina, {}).get('endpoints', ())
            if fila['blueprint'] in {e.split('.')[0] for e in endpoints}:
                nombre = sec['titulo']
                if len({e.split('.')[0] for e in endpoints}) > 3:  # Referenciales: el catálogo, no el índice
                    nombre = _nombres_catalogos().get(fila['blueprint']) or fila['blueprint'].replace('_', ' ').capitalize()
                m = re.search(r'El campo "([^"{]+)" es obligatorio', fila['mensaje']) if tipo == 'obligatorio'                     else re.search(r'Use solo (.+)\.$', fila['mensaje']) if tipo == 'caracteres' else None
                pantallas.setdefault(tipo, {}).setdefault(nombre, set())
                if m:
                    pantallas[tipo][nombre].add(m.group(1))

    resultado = []
    for t in TIPOS_MENSAJE:
        if t['id'] not in pantallas:
            continue
        por_pantalla = pantallas[t['id']]
        if t['id'] == 'caracteres':
            # Se agrupa por la regla: "letras, números y espacios: Cargo, Especialidad…"
            grupos = {}
            for nombre, reglas in por_pantalla.items():
                for regla in reglas:
                    grupos.setdefault(regla, []).append(nombre)
            items = [f"Solo {regla}: {', '.join(sorted(n))}." for regla, n in sorted(grupos.items())]
            # Pantallas con una regla propia que el aviso mismo explica (nombres, teléfonos, etc.)
            propias = sorted(n for n, reglas in por_pantalla.items() if not reglas)
            if propias:
                items.append(f"Con regla propia (el aviso indica qué se admite): {', '.join(propias)}.")
        elif t['id'] == 'obligatorio':
            items = [f"{n}: {', '.join(sorted(c))}." if c else f"{n}." for n, c in sorted(por_pantalla.items())]
        else:
            items = [', '.join(sorted(por_pantalla)) + '.']
        resultado.append(dict(t, lista=items))
    return resultado


def _figura(es_pdf):
    """Captura de pantalla de la guía (generadas con docs/scripts/capturas_manual.py en static/img/ayuda/).
    La vista previa la pide por URL; el PDF, por ruta de archivo. Si la imagen no existe, no muestra nada."""
    def figura(ruta, pie=''):
        archivo = os.path.join(current_app.static_folder, 'img', 'ayuda', *ruta.split('/'))
        if not os.path.isfile(archivo):
            return ''
        src = ('file://' + archivo) if es_pdf else url_for('static', filename=f'img/ayuda/{ruta}')
        pie_html = f'<figcaption>{escape(pie)}</figcaption>' if pie else ''
        # Markup seguro: ruta, pie y src pasan por escape() antes de armar el HTML
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
                           mensajes=_mensajes_validacion(secciones, _roles_del_manual(rol)),
                           sin_guia=sin_guia,
                           seccion_activa=_seccion_desde(request.args.get('desde'), secciones),
                           logo_base64=AyudaService().logo_base64(),
                           figura=_figura(False),
                           es_pdf=False,
                           perfil=rol or session.get('grupo'),
                           fecha=date.today().strftime('%d/%m/%Y'))


NOMBRES_PERFIL = {'SUPERADMIN': 'Superadministrador', 'ADMINISTRADOR': 'Administrador', 'RECEPCION': 'Recepción',
                   'CLINICO': 'Clínico', 'VENTAS': 'Ventas'}


def _guia_html(rol):
    """HTML de cada capítulo de la guía (Primeros pasos, una sección por pantalla y el anexo de avisos), ya
    renderizado, para armar el Word. Las imágenes van por ruta de archivo."""
    secciones, _ = _armar_manual(rol)
    figura = _figura(True)
    capitulos = [render_template('ayuda-secciones/general.html')]
    capitulos += [render_template(s['template'], figura=figura) for s in secciones]
    mensajes = _mensajes_validacion(secciones, _roles_del_manual(rol))
    if mensajes:
        capitulos.append(render_template('ayuda-secciones/anexo_mensajes.html', mensajes=mensajes, figura=figura))
    return capitulos


def _guia_nombre(rol):
    perfil = rol or session.get('grupo')
    return perfil, f"Guia_de_uso_{perfil or 'SYSCLIN'}"


@ayudamod.route('/manual/pdf')
@role_required(*ROLES_AYUDA)
def ayudaManualPdf():
    """Guía de uso en PDF con el formato Word estándar (docs/estandar): se arma el Word y se exporta."""
    rol = _rol_solicitado()
    perfil, nombre = _guia_nombre(rol)
    pdf_bytes = AyudaService().manual_guia_pdf(_guia_html(rol), NOMBRES_PERFIL.get(perfil, perfil or 'Sin rol'),
                                               date.today().strftime('%d/%m/%Y'))
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True,
                     download_name=f'{nombre}.pdf')


@ayudamod.route('/manual/docx')
@role_required(*ROLES_AYUDA)
def ayudaManualDocx():
    """La misma guía de uso en Word, para revisarla o editarla."""
    rol = _rol_solicitado()
    perfil, nombre = _guia_nombre(rol)
    docx_bytes = AyudaService().manual_guia_docx(_guia_html(rol), NOMBRES_PERFIL.get(perfil, perfil or 'Sin rol'),
                                                 date.today().strftime('%d/%m/%Y'))
    return send_file(io.BytesIO(docx_bytes),
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                     as_attachment=True, download_name=f'{nombre}.docx')


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
    """Manual de seguridad en PDF con el formato Word estándar (docs/estandar): se arma el Word y se exporta."""
    pdf_bytes = AyudaService().manual_seguridad_pdf(SECCIONES_SEGURIDAD, SCRIPTS_SEGURIDAD,
                                                    date.today().strftime('%d/%m/%Y'))

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Manual_de_seguridad_SYSCLIN_{date.today().strftime('%Y%m%d')}.pdf"
    )
