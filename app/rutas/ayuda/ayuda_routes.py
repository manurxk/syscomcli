import io
import json
import os
import re
import unicodedata
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

# Los manuales técnicos son dos: seguridad (para el personal, el administrador y el soporte) e infraestructura
# (operación del servidor). Las plantillas de ambos están en ayuda-seguridad-secciones/. Cada capítulo es
# {'id', 'titulo', 'template'}; si la plantilla es una sección de la guía de uso (empieza con <h3>), su h3 es el título.

# Parte D del manual de seguridad: políticas y controles técnicos (también los usa el Manual del sistema).
SECCIONES_SEGURIDAD_TECNICAS = (
    {'id': 'objetivo', 'titulo': 'Objetivo, alcance y clasificación de la información', 'template': 'ayuda-seguridad-secciones/objetivo.html'},
    {'id': 'contrasenas', 'titulo': 'Contraseñas y autenticación', 'template': 'ayuda-seguridad-secciones/contrasenas.html'},
    {'id': 'roles', 'titulo': 'Roles y control de acceso', 'template': 'ayuda-seguridad-secciones/roles.html'},
    {'id': 'aplicacion', 'titulo': 'Seguridad de la aplicación', 'template': 'ayuda-seguridad-secciones/aplicacion.html'},
    {'id': 'auditoria', 'titulo': 'Auditoría y chequeo periódico', 'template': 'ayuda-seguridad-secciones/auditoria.html'},
    {'id': 'incidentes', 'titulo': 'Respuesta a incidentes', 'template': 'ayuda-seguridad-secciones/incidentes.html'},
    {'id': 'riesgos', 'titulo': 'Riesgos aceptados y normativa', 'template': 'ayuda-seguridad-secciones/riesgos.html'},
)

# Manual de seguridad: partes y capítulos, en orden. La Parte C se genera de mensajes_validacion.json
# (un capítulo por módulo). 'titulo': None = sin carátula de parte.
PARTES_SEGURIDAD = (
    {'titulo': None, 'introduccion': None, 'capitulos': (
        {'id': 'introduccion', 'titulo': 'Introducción', 'template': 'ayuda-seguridad-secciones/seg_introduccion.html'},
    )},
    {'titulo': None,
     'introduccion': 'Recepcionistas, clínicos, personal de ventas y administradores. Lea esta parte completa antes de '
                     'empezar a usar el sistema.',
     'capitulos': (
        {'id': 'acceso', 'titulo': 'Cómo ingresar de forma segura', 'template': 'ayuda-seguridad-secciones/seg_acceso.html'},
        {'id': 'contrasena', 'titulo': 'Su contraseña', 'template': 'ayuda-seguridad-secciones/seg_contrasena.html'},
        {'id': 'roles-personal', 'titulo': 'Qué puede ver cada persona', 'template': 'ayuda-seguridad-secciones/seg_roles_personal.html'},
        {'id': 'sesion', 'titulo': 'Su sesión y su computadora', 'template': 'ayuda-seguridad-secciones/seg_sesion.html'},
        {'id': 'informacion', 'titulo': 'Cómo cuidar la información', 'template': 'ayuda-seguridad-secciones/seg_informacion.html'},
        {'id': 'validacion', 'titulo': 'Validación de los datos que se cargan', 'template': 'ayuda-seguridad-secciones/seg_validacion.html'},
        {'id': 'algo-mal', 'titulo': 'Si algo no está bien', 'template': 'ayuda-seguridad-secciones/seg_algo_mal.html'},
    )},
    {'titulo': None,
     'introduccion': 'Tareas de seguridad de quien administra el sistema en la clínica: copias de respaldo, calendario e '
                     'incidentes. Usuarios, permisos, menú y auditoría se explican en el Manual de usuario del '
                     'Administrador. Las tareas técnicas del servidor las hace el soporte técnico '
                     '(Manual de infraestructura).',
     'capitulos': (
        {'id': 'respaldos', 'titulo': 'Copias de respaldo', 'template': 'ayuda-seguridad-secciones/seg_respaldos.html'},
        {'id': 'calendario', 'titulo': 'Calendario de tareas', 'template': 'ayuda-seguridad-secciones/seg_calendario.html'},
        {'id': 'incidente', 'titulo': 'Qué hacer ante un incidente', 'template': 'ayuda-seguridad-secciones/seg_incidente.html'},
    )},
    {'titulo': None,
     'introduccion': 'Las reglas de validación y los avisos que muestra el sistema en cada pantalla, por módulo.',
     'generado': 'validaciones'},
    {'titulo': None,
     'introduccion': 'Objetivo y alcance, seguridad de la aplicación, auditoría y riesgos aceptados. Es el nivel de '
                     'detalle para el soporte técnico.',
     'capitulos': tuple(s for s in SECCIONES_SEGURIDAD_TECNICAS
                        if s['id'] in ('objetivo', 'aplicacion', 'auditoria', 'riesgos'))},
)

# Anexos del manual de seguridad (se rotulan Anexo A, B, C en este orden).
ANEXOS_SEGURIDAD = (
    {'id': 'anexo-faq', 'titulo': 'Preguntas frecuentes', 'template': 'ayuda-seguridad-secciones/seg_anexo_faq.html'},
    {'id': 'anexo-glosario', 'titulo': 'Glosario', 'template': 'ayuda-seguridad-secciones/seg_anexo_glosario.html'},
    {'id': 'anexo-contactos', 'titulo': 'Contactos', 'template': 'ayuda-seguridad-secciones/seg_anexo_contactos.html'},
    {'id': 'anexo-actualizaciones', 'titulo': 'Actualizaciones', 'template': 'ayuda-seguridad-secciones/seg_anexo_actualizaciones.html'},
)

# Capítulos del manual de infraestructura, en orden.
SECCIONES_INFRAESTRUCTURA = (
    {'id': 'introduccion', 'titulo': 'Introducción', 'template': 'ayuda-seguridad-secciones/infra_introduccion.html'},
    {'id': 'componentes', 'titulo': 'Componentes del sistema (contenedores)', 'template': 'ayuda-seguridad-secciones/componentes.html'},
    {'id': 'configuracion', 'titulo': 'Configuración (.env)', 'template': 'ayuda-seguridad-secciones/configuracion.html'},
    {'id': 'contenedores', 'titulo': 'Manejo de contenedores y reactivación del sistema', 'template': 'ayuda-seguridad-secciones/contenedores.html'},
    {'id': 'base-datos', 'titulo': 'Base de datos: usuarios, contraseñas y migraciones', 'template': 'ayuda-seguridad-secciones/base_datos.html'},
    {'id': 'https', 'titulo': 'HTTPS, red y despliegue en el servidor', 'template': 'ayuda-seguridad-secciones/https.html'},
    {'id': 'backups', 'titulo': 'Backups y restauración', 'template': 'ayuda-seguridad-secciones/backups.html'},
    {'id': 'dependencias', 'titulo': 'Gestión de vulnerabilidades (dependencias)', 'template': 'ayuda-seguridad-secciones/dependencias.html'},
    {'id': 'problemas', 'titulo': 'Solución de problemas', 'template': 'ayuda-seguridad-secciones/problemas.html'},
)

# Orden de los capítulos técnicos en el Manual del sistema, que los reúne a los dos como antes de la división.
ORDEN_TECNICO_SISTEMA = (
    'objetivo', 'componentes', 'configuracion', 'contenedores', 'contrasenas', 'roles', 'base-datos', 'aplicacion',
    'https', 'backups', 'auditoria', 'dependencias', 'incidentes', 'problemas', 'riesgos',
)

# Datos de portada y de control del documento de cada manual técnico (los usan la vista previa y el Word).
MANUALES_TECNICOS = {
    'seguridad': {
        'titulo': 'Manual de seguridad',
        'subtitulo': 'Políticas, controles y validaciones del sistema',
        'destinatario': 'Todo el personal, administrador y soporte técnico (ver «Cómo está organizado»)',
        'revision': 'Cada 6 meses, o después de un incidente o un cambio de infraestructura',
        'confidencialidad': 'Las Partes B a D describen controles de administración y no se entregan a los '
                            'usuarios finales',
        'referencias': 'ISO/IEC 27002:2013; NIST SP 800-61 rev. 2 (respuesta a incidentes)',
        'archivo': 'Manual_de_seguridad_SYSCLIN',
        # Máximo 50 hojas: letra 11, capítulos seguidos, índice de capítulos y capturas de avisos de a dos por fila
        'denso': True, 'capitulos_seguidos': True,
    },
    'infraestructura': {
        'titulo': 'Manual de infraestructura',
        'subtitulo': 'Operación, despliegue y respaldo del sistema',
        'destinatario': 'Soporte técnico: quien administra el servidor',
        'revision': 'Cada 6 meses, o después de un cambio de infraestructura',
        'confidencialidad': 'No contiene contraseñas, pero describe la infraestructura: no se publica ni se '
                            'entrega a usuarios finales',
        'referencias': 'ISO/IEC 27002:2013 (A.12.1.1, procedimientos de operación documentados)',
        'archivo': 'Manual_de_infraestructura_SYSCLIN',
    },
}

# Anexo de scripts del manual de infraestructura: se leen del repositorio al generar el manual, así nunca queda
# desactualizado. Ninguno contiene secretos (las claves viven en .env, que no se incluye).
SCRIPTS_INFRAESTRUCTURA = (
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
    for ruta, descripcion in SCRIPTS_INFRAESTRUCTURA:
        try:
            with open(os.path.join(raiz, ruta), encoding='utf-8') as f:
                contenido = f.read()
        except OSError:
            contenido = None
        scripts.append({'id': 'script-' + ruta.replace('/', '-').replace('.', '-'),
                        'ruta': ruta, 'descripcion': descripcion, 'contenido': contenido})
    return scripts


# Manual del sistema: guías de uso y seguridad en un solo documento, sin repetir pantallas. Cada pantalla va una
# sola vez, en la parte del rol que la usa; las compartidas por varios roles van en la Parte I.
# 'paginas' = claves de SECCIONES_MANUAL; 'general' = Primeros pasos; 'avisos' = capítulo de avisos de validación.
PARTES_SISTEMA = (
    {'titulo': 'Parte I. Pantallas comunes',
     'introduccion': 'Primeros pasos y las pantallas que usan varios roles. Se explican una sola vez aquí; en las '
                     'partes siguientes no se repiten.',
     'general': True, 'avisos': True,
     'paginas': ('agenda_horarios.agendaHorariosIndex', 'auditoria.auditoriaIndex', 'reporte.reporteIndex')},
    {'titulo': 'Parte II. Rol Recepción',
     'introduccion': 'Pantallas propias de Recepción: pacientes, citas y lista de espera. También usa la Agenda '
                     'Médica, la Auditoría y los Reportes de la Parte I.',
     'paginas': ('paciente.pacienteIndex', 'cita.citaIndex', 'lista_espera.listaEsperaIndex')},
    {'titulo': 'Parte III. Rol Clínico',
     'introduccion': 'Pantallas propias del Clínico: su agenda, las consultas, el plan de evaluación e intervención y '
                     'las fichas médicas. También usa la Agenda Médica (solo lectura), la Auditoría y los Reportes '
                     'de la Parte I.',
     'paginas': ('mi_agenda.miAgendaIndex', 'consulta.consultaIndex', 'pei.peiIndex', 'ficha.fichaIndex')},
    {'titulo': 'Parte IV. Rol Ventas',
     'introduccion': 'Pantallas propias de Ventas: pedidos, presupuestos, caja, facturación y cobranzas. También usa '
                     'la Auditoría y los Reportes de la Parte I.',
     'paginas': ('pedido.pedidoIndex', 'presupuesto.presupuestoIndex', 'apertura_cierre_caja.cajaEstado',
                 'apertura_cierre_caja.cajaHistorial', 'arqueo_caja.arqueoIndex', 'factura.facturaIndex',
                 'remision.remisionIndex', 'nota_credito.notaCreditoIndex', 'nota_debito.notaDebitoIndex',
                 'cuenta_cobrar.cuentaCobrarIndex', 'cobranza.cobranzaIndex', 'recaudacion.recaudacionIndex',
                 'libro_ventas.libroVentasIndex')},
    {'titulo': 'Parte V. Rol Administrador',
     'introduccion': 'Pantallas propias de la administración: usuarios, funcionarios, catálogos, timbrados, permisos '
                     'y menú. El Administrador ve además todas las pantallas de las partes anteriores.',
     'paginas': ('usuario.usuarioIndex', 'funcionario.funcionarioIndex', 'referenciales.referencialesIndex',
                 'timbrado.timbradoIndex', 'punto_expedicion.puntoExpedicionIndex', 'permisos.permisosIndex',
                 'menu.menuIndex')},
    {'titulo': 'Parte VI. Seguridad y operación',
     'introduccion': 'Políticas y procedimientos para quien administra el sistema: contraseñas, roles, copias de '
                     'seguridad, HTTPS, respuesta a incidentes. Los avisos de validación están en la Parte I.',
     'seguridad': True},
)


def _sistema_partes(figura):
    """Partes del Manual del sistema con el HTML de cada capítulo ya renderizado (hace falta contexto de Flask).
    Cada capítulo es (título o None, html): sin título, el html trae su h3 (guía de uso)."""
    secciones, _ = _armar_manual('ADMINISTRADOR')  # el Administrador ve todas las pantallas
    partes = []
    for p in PARTES_SISTEMA:
        capitulos = []
        if p.get('general'):
            capitulos.append((None, render_template('ayuda-secciones/general.html')))
        for pagina in p.get('paginas', ()):
            capitulos.append((None, render_template(SECCIONES_MANUAL[pagina]['template'], figura=figura)))
        if p.get('avisos'):
            # Una captura de ejemplo por tipo de aviso alcanza: dicen lo mismo en todas las pantallas
            mensajes = [dict(m, capturas=m['capturas'][:1])
                        for m in _mensajes_validacion(secciones, ['ADMINISTRADOR', 'SUPERADMIN'])]
            capitulos.append((None, render_template('ayuda-secciones/anexo_mensajes.html', mensajes=mensajes,
                                                    figura=figura)))
        if p.get('seguridad'):
            # La introducción de infraestructura no entra: el Manual del sistema tiene la suya
            tecnicos = sorted((s for s in SECCIONES_SEGURIDAD_TECNICAS + SECCIONES_INFRAESTRUCTURA
                               if s['id'] in ORDEN_TECNICO_SISTEMA),
                              key=lambda s: ORDEN_TECNICO_SISTEMA.index(s['id']))
            for s in tecnicos:
                ruta = os.path.join(os.path.dirname(__file__), 'templates', s['template'])
                with open(ruta, encoding='utf-8') as f:
                    capitulos.append((s['titulo'], f.read()))
        partes.append({'titulo': p['titulo'], 'introduccion': p['introduccion'], 'capitulos': capitulos})
    return partes


def _rol_solicitado():
    """Rol pedido por ?rol= (manuales por rol del inicio del administrador).
    Solo lo pueden usar ADMINISTRADOR/SUPERADMIN; el de SUPERADMIN, solo un Superadministrador."""
    rol = (request.args.get("rol") or "").strip().upper()
    roles_sesion = {(r or "").strip().upper() for r in session.get("roles", [])}
    if rol not in ROLES_AYUDA + ('TODOS',) or not roles_sesion & {"ADMINISTRADOR", "SUPERADMIN"}:
        return None
    if rol == "SUPERADMIN" and "SUPERADMIN" not in roles_sesion:
        return None
    return rol


def _roles_del_manual(rol=None):
    """Roles con los que se arma el manual: el pedido por ?rol= (TODOS = todos los perfiles) o los de la sesión."""
    if rol == 'TODOS':
        return list(ROLES_AYUDA)
    return [rol] if rol else [(r or "").strip().upper() for r in session.get("roles", [])]


def _armar_manual(rol=None):
    """Secciones del manual visibles para los roles del usuario (o para el rol pedido), en el orden del menú."""
    roles = _roles_del_manual(rol)
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


NOMBRES_PERFIL = {'SUPERADMIN': 'Superadministrador', 'ADMINISTRADOR': 'Administrador', 'RECEPCION': 'Recepción',
                   'CLINICO': 'Clínico', 'VENTAS': 'Ventas', 'TODOS': 'Todos los roles'}

# Manual de usuario: un solo manual, un capítulo por módulo y cada pantalla como apartado dentro de su capítulo.
# Filtrable por rol (?rol=; TODOS = el manual completo, que es el del Administrador: ve las 29 pantallas).
# Cada capítulo: (título, endpoints de sus pantallas en el orden en que se explican).
CAPITULOS_USUARIO = (
    ('Personas', ('paciente.pacienteIndex', 'funcionario.funcionarioIndex')),
    ('Agendamiento', ('agenda_horarios.agendaHorariosIndex', 'cita.citaIndex', 'lista_espera.listaEsperaIndex')),
    ('Clínico', ('mi_agenda.miAgendaIndex', 'consulta.consultaIndex', 'pei.peiIndex', 'ficha.fichaIndex')),
    ('Facturación', ('apertura_cierre_caja.cajaEstado', 'pedido.pedidoIndex', 'presupuesto.presupuestoIndex',
                     'factura.facturaIndex', 'cuenta_cobrar.cuentaCobrarIndex', 'cobranza.cobranzaIndex',
                     'nota_credito.notaCreditoIndex', 'nota_debito.notaDebitoIndex', 'remision.remisionIndex',
                     'arqueo_caja.arqueoIndex', 'recaudacion.recaudacionIndex', 'apertura_cierre_caja.cajaHistorial',
                     'libro_ventas.libroVentasIndex')),
    ('Configuración', ('usuario.usuarioIndex', 'permisos.permisosIndex', 'menu.menuIndex', 'timbrado.timbradoIndex',
                       'punto_expedicion.puntoExpedicionIndex', 'referenciales.referencialesIndex')),
    ('Reportes y auditoría', ('reporte.reporteIndex', 'auditoria.auditoriaIndex')),
)
CAPITULO_PRIMEROS_PASOS = {'id': 'primeros-pasos', 'titulo': None, 'template': 'ayuda-secciones/primeros_pasos.html'}
CAPITULO_FAQ_USUARIO = {'id': 'preguntas-frecuentes', 'titulo': None, 'template': 'ayuda-secciones/preguntas_frecuentes.html'}
CAPITULO_ACTUALIZACIONES_USUARIO = {'id': 'actualizaciones', 'titulo': None, 'template': 'ayuda-secciones/actualizaciones.html'}
CAPITULO_VENTAS_ORDEN = {'id': 'ventas-orden', 'titulo': None, 'template': 'ayuda-secciones/ventas_orden.html'}

MANUAL_USUARIO = {
    'titulo': 'Manual de usuario',
    'subtitulo': 'Guía de uso de las pantallas del sistema',
    'revision': 'Cada vez que cambia una pantalla del sistema',
    'confidencialidad': 'Uso interno de la clínica',
    'referencias': 'IEEE Std 1063-2001, Software User Documentation; ISO/IEC 26514:2008',
    'denso': True,  # máximo 100 hojas: letra 11, interlineado simple, capturas lado a lado, índice solo de capítulos
}


def _partes_usuario(rol, figura):
    """Partes del manual de usuario ya renderizadas: Primeros pasos, un módulo por parte (con una sección por
    pantalla que el rol ve) y las preguntas frecuentes. Devuelve (partes, nombre del perfil)."""
    secciones, _ = _armar_manual(rol)
    perfil = rol or session.get('grupo')
    perfil_nombre = NOMBRES_PERFIL.get(perfil, perfil or 'Sin rol')
    por_endpoint = {s['id'].replace('-', '.', 1): _capitulo({'id': s['id'], 'titulo': None, 'template': s['template']}, figura)
                    for s in secciones}

    partes = [{'titulo': None, 'introduccion': None, 'capitulos': [_capitulo(CAPITULO_PRIMEROS_PASOS, figura)]}]
    asignadas = set()
    modulos = [(titulo, [e for e in endpoints if e in por_endpoint]) for titulo, endpoints in CAPITULOS_USUARIO]
    for titulo, endpoints in modulos:
        asignadas.update(endpoints)
    sueltas = [e for e in por_endpoint if e not in asignadas]  # pantalla nueva que todavía no está en CAPITULOS_USUARIO
    if sueltas:
        modulos.append(('Otras pantallas', sueltas))
    for titulo, endpoints in modulos:
        if not endpoints:
            continue
        capitulos = [por_endpoint[e] for e in endpoints]
        if titulo == 'Facturación':
            capitulos = [_capitulo(CAPITULO_VENTAS_ORDEN, figura)] + capitulos
        partes.append({'titulo': titulo, 'introduccion': None, 'capitulos': capitulos})
    partes.append({'titulo': None, 'introduccion': None, 'capitulos': [_capitulo(CAPITULO_FAQ_USUARIO, figura)]})
    if rol in ('TODOS', 'ADMINISTRADOR', 'SUPERADMIN'):   # solo lo que cambió para quien administra el sistema
        partes.append({'titulo': None, 'introduccion': None,
                       'capitulos': [_capitulo(CAPITULO_ACTUALIZACIONES_USUARIO, figura)]})
    return partes, perfil_nombre


def _capitulos_documento(partes):
    """Word y PDF: cada módulo es un capítulo y sus pantallas son apartados (título de nivel 2) dentro de él, sin
    carátulas de parte. La vista previa del botón ? sigue con una sección por pantalla."""
    capitulos = []
    for parte in partes:
        if not parte['titulo']:
            capitulos.extend(parte['capitulos'])
            continue
        html = ''.join(f"<h4>{escape(c['titulo'])}</h4>{c['html']}" for c in parte['capitulos'])
        capitulos.append({'id': 'modulo-' + _slug(parte['titulo']), 'titulo': parte['titulo'], 'html': html})
    return capitulos


def _manual_usuario(rol, figura, para_documento):
    """(partes, datos de portada) del manual de usuario del perfil pedido (o de los roles de la sesión)."""
    partes, perfil_nombre = _partes_usuario(rol, figura)
    if para_documento:
        partes = [{'titulo': None, 'introduccion': None, 'capitulos': _capitulos_documento(partes)}]
    datos = dict(MANUAL_USUARIO, perfil=perfil_nombre,
                 destinatario='Todo el personal de la clínica' if rol == 'TODOS' else f'Perfil {perfil_nombre}',
                 archivo=f"Manual_de_usuario_SYSCLIN_{_slug(perfil_nombre)}")
    return partes, datos


@ayudamod.route('/manual')
@role_required(*ROLES_AYUDA)
def ayudaManual():
    """Vista previa del manual (se muestra dentro del modal de ayuda de base.html)."""
    rol = _rol_solicitado()
    secciones, sin_guia = _armar_manual(rol)
    partes, datos = _manual_usuario(rol, _figura(False), False)
    return render_template('ayuda-manual.html',
                           partes=partes,
                           m=datos,
                           sin_guia=sin_guia,
                           seccion_activa=_seccion_desde(request.args.get('desde'), secciones),
                           logo_base64=AyudaService().logo_base64(),
                           es_pdf=False,
                           fecha=date.today().strftime('%d/%m/%Y'))


@ayudamod.route('/manual/pdf')
@role_required(*ROLES_AYUDA)
def ayudaManualPdf():
    """Manual de usuario en PDF con el formato Word estándar (docs/estandar): se arma el Word y se exporta."""
    partes, datos = _manual_usuario(_rol_solicitado(), _figura(True), True)
    pdf_bytes = AyudaService().manual_tecnico_pdf(partes, [], (), date.today().strftime('%d/%m/%Y'), datos)
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True,
                     download_name=f"{datos['archivo']}_{date.today().strftime('%Y%m%d')}.pdf")


@ayudamod.route('/manual/docx')
@role_required(*ROLES_AYUDA)
def ayudaManualDocx():
    """El mismo manual de usuario en Word, para revisarlo o editarlo."""
    partes, datos = _manual_usuario(_rol_solicitado(), _figura(True), True)
    docx_bytes = AyudaService().manual_tecnico_docx(partes, [], (), date.today().strftime('%d/%m/%Y'), datos)
    return send_file(io.BytesIO(docx_bytes),
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                     as_attachment=True,
                     download_name=f"{datos['archivo']}_{date.today().strftime('%Y%m%d')}.docx")


@ayudamod.route('/sistema/pdf')
@role_required(*ROLES_SEGURIDAD)
def ayudaSistemaPdf():
    """Manual del sistema (guías de uso + seguridad, por partes) en PDF: se arma el Word y se exporta."""
    pdf_bytes = AyudaService().manual_sistema_pdf(_sistema_partes(_figura(True)), SCRIPTS_INFRAESTRUCTURA,
                                                  date.today().strftime('%d/%m/%Y'))
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True,
                     download_name=f"Manual_del_sistema_SYSCLIN_{date.today().strftime('%Y%m%d')}.pdf")


@ayudamod.route('/sistema/docx')
@role_required(*ROLES_SEGURIDAD)
def ayudaSistemaDocx():
    """El mismo Manual del sistema en Word, para revisarlo o editarlo."""
    docx_bytes = AyudaService().manual_sistema_docx(_sistema_partes(_figura(True)), SCRIPTS_INFRAESTRUCTURA,
                                                    date.today().strftime('%d/%m/%Y'))
    return send_file(io.BytesIO(docx_bytes),
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                     as_attachment=True,
                     download_name=f"Manual_del_sistema_SYSCLIN_{date.today().strftime('%Y%m%d')}.docx")


def _capitulo(espec, figura, **contexto):
    """Capítulo ya renderizado: {'id', 'titulo', 'html'}. Las secciones de la guía de uso traen el título en un
    <h3> al comienzo: se saca del HTML y pasa a ser el título (salvo que la especificación ya lo indique).
    contexto = variables propias de la plantilla (por ejemplo, los avisos de validación)."""
    html = render_template(espec['template'], figura=figura, tipos=TIPOS_MENSAJE, **contexto)
    titulo = espec.get('titulo')
    m = re.match(r'\s*<h3[^>]*>(.*?)</h3>', html, re.S)
    if m:
        html = html[m.end():]
        titulo = titulo or re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return {'id': espec['id'], 'titulo': titulo, 'html': html}


def _slug(texto):
    """Identificador sin tildes ni símbolos, para los ids de los capítulos generados."""
    limpio = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', limpio.lower()).strip('-')


def _cuando(acciones):
    """Texto de la columna «Cuándo» de las validaciones: a partir de las acciones que dan el mismo aviso."""
    if {'Crear', 'Editar'} <= acciones:
        return 'Al guardar (crear y editar)'
    if 'Crear' in acciones:
        return 'Al crear'
    if 'Editar' in acciones:
        return 'Al editar'
    if 'Eliminar / dar de baja' in acciones:
        return 'Al dar de baja'
    if 'Consultar' in acciones:
        return 'Al consultar'
    return 'Regla del sistema'


def _validaciones_por_grupo(secciones):
    """Avisos de validación por pantalla, agrupados por módulo del menú (Parte C del manual de seguridad).
    Devuelve {módulo: [{'pantalla', 'filas': [{'cuando', 'mensaje', 'tipo'}]}]}, en el orden del menú. Origen:
    mensajes_validacion.json (docs/scripts/extraer_mensajes_validacion.py)."""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'mensajes_validacion.json'), encoding='utf-8') as f:
            filas = json.load(f)
    except (OSError, ValueError):
        return {}
    titulos_tipo = {t['id']: t['titulo'] for t in TIPOS_MENSAJE}
    grupos = {}
    for sec in secciones:
        endpoints = SECCIONES_MANUAL.get(sec['id'].replace('-', '.', 1), {}).get('endpoints', ())
        blueprints = sorted({e.split('.')[0] for e in endpoints})
        if len(blueprints) > 3:  # Referenciales: cada catálogo es una pantalla
            unidades = [(_nombres_catalogos().get(bp) or bp.replace('_', ' ').capitalize(), [bp])
                        for bp in blueprints]
        else:
            unidades = [(sec['titulo'], blueprints)]
        for nombre, bps in unidades:
            acciones_por_mensaje = {}
            for fila in filas:
                if fila['blueprint'] in bps:
                    acciones_por_mensaje.setdefault(fila['mensaje'], set()).add(fila['accion'])
            if not acciones_por_mensaje:
                continue
            filas_pantalla = [{'cuando': _cuando(acciones), 'mensaje': mensaje.replace('{…}', '…'),
                               'tipo': titulos_tipo.get(_tipo_de(mensaje), 'Regla propia de la pantalla')}
                              for mensaje, acciones in sorted(acciones_por_mensaje.items())]
            grupos.setdefault(sec['grupo'], []).append({'pantalla': nombre, 'filas': filas_pantalla})
    return grupos


def _resumen_validaciones(grupos):
    """Validaciones condensadas para el manual de seguridad. De cada pantalla se juntan en una fila los campos
    obligatorios, si tiene valores únicos y los caracteres que admite; el resto de los avisos (reglas propias) se
    listan una sola vez aunque salgan en varias pantallas. Devuelve [{'modulo', 'generales', 'propios'}] en el orden
    del menú; 'grupos' es lo que devuelve _validaciones_por_grupo."""
    nombres = dict(MODULOS_MENU)
    orden = [g for g, _ in MODULOS_MENU if g in grupos] + [g for g in grupos if g not in nombres]
    modulos = []
    for grupo in orden:
        generales, propios = [], {}
        for p in grupos[grupo]:
            obligatorios, unico, caracteres = set(), False, []
            for f in p['filas']:
                mensaje = f['mensaje']
                m_obl = re.fullmatch(r'El campo "([^"]+)" es obligatorio\.?', mensaje)
                m_car = re.search(r'Use solo (.+?)\.?$', mensaje)
                if m_obl:
                    obligatorios.add(m_obl.group(1))
                elif f['tipo'] == 'El dato ya existe':
                    unico = True
                elif f['tipo'] == 'Caracteres no permitidos' and m_car:
                    if m_car.group(1) not in caracteres:
                        caracteres.append(m_car.group(1))
                else:
                    propios.setdefault(mensaje, []).append(p['pantalla'])
            if obligatorios or unico or caracteres:
                generales.append({'pantalla': p['pantalla'], 'obligatorios': ', '.join(sorted(obligatorios)),
                                  'unico': unico, 'caracteres': '; '.join(caracteres)})
        lista = [{'mensaje': m, 'pantallas': ', '.join(dict.fromkeys(ps))} for m, ps in sorted(propios.items())]
        modulos.append({'modulo': nombres.get(grupo, grupo), 'generales': generales, 'propios': lista})
    return modulos


# Módulos del menú, como los guarda la base (sin tildes) y su nombre en el manual, en el orden del menú.
MODULOS_MENU = (('Personas', 'Personas'), ('Agendamiento', 'Agendamiento'), ('Clinico', 'Clínico'),
                ('Ventas', 'Ventas'), ('Configuracion', 'Configuración'), ('Reportes', 'Reportes'))


def _partes_seguridad(figura):
    """Partes del manual de seguridad con el HTML de cada capítulo ya renderizado (hace falta contexto de Flask)."""
    secciones, _ = _armar_manual('ADMINISTRADOR')  # el Administrador ve todas las pantallas
    partes = []
    for p in PARTES_SEGURIDAD:
        if p.get('generado') == 'validaciones':
            modulos = _resumen_validaciones(_validaciones_por_grupo(secciones))
            capitulos = [{'id': 'validaciones-modulos', 'titulo': 'Reglas de validación por módulo',
                          'html': render_template('ayuda-seguridad-secciones/validaciones_resumen.html',
                                                  modulos=modulos)}]
        else:
            capitulos = [_capitulo(e, figura) for e in p['capitulos']]
        partes.append({'titulo': p['titulo'], 'introduccion': p['introduccion'], 'capitulos': capitulos})
    return partes


def _manual_tecnico(clave, figura):
    """(partes, anexos, scripts del anexo, datos de portada) del manual técnico 'seguridad' o 'infraestructura'.
    Seguridad lleva los anexos A, B y C; infraestructura, el anexo de scripts."""
    if clave == 'seguridad':
        anexos = [dict(_capitulo(e, figura), letra=chr(65 + n)) for n, e in enumerate(ANEXOS_SEGURIDAD)]
        return _partes_seguridad(figura), anexos, (), MANUALES_TECNICOS[clave]
    partes = [{'titulo': None, 'introduccion': None,
               'capitulos': [_capitulo(e, figura) for e in SECCIONES_INFRAESTRUCTURA]}]
    return partes, [], SCRIPTS_INFRAESTRUCTURA, MANUALES_TECNICOS[clave]


def _vista_tecnico(clave):
    """Vista previa de un manual técnico (modal del inicio del administrador)."""
    partes, anexos, _, datos = _manual_tecnico(clave, _figura(False))
    return render_template('ayuda-manual-tecnico.html',
                           partes=partes,
                           anexos=anexos,
                           scripts=_leer_scripts() if clave == 'infraestructura' else [],
                           m=datos,
                           logo_base64=AyudaService().logo_base64(),
                           es_pdf=False,
                           fecha=date.today().strftime('%d/%m/%Y'))


def _docx_tecnico(clave):
    """Word de un manual técnico, con el formato estándar (docs/estandar), para revisarlo o editarlo."""
    partes, anexos, scripts, datos = _manual_tecnico(clave, _figura(True))
    docx_bytes = AyudaService().manual_tecnico_docx(partes, anexos, scripts, date.today().strftime('%d/%m/%Y'), datos)
    return send_file(io.BytesIO(docx_bytes),
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                     as_attachment=True,
                     download_name=f"{datos['archivo']}_{date.today().strftime('%Y%m%d')}.docx")


def _pdf_tecnico(clave):
    """PDF de un manual técnico: se arma el Word y se exporta, así los dos son iguales."""
    partes, anexos, scripts, datos = _manual_tecnico(clave, _figura(True))
    pdf_bytes = AyudaService().manual_tecnico_pdf(partes, anexos, scripts, date.today().strftime('%d/%m/%Y'), datos)
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True,
                     download_name=f"{datos['archivo']}_{date.today().strftime('%Y%m%d')}.pdf")


@ayudamod.route('/seguridad')
@role_required(*ROLES_SEGURIDAD)
def ayudaSeguridad():
    """Vista previa del manual de seguridad."""
    return _vista_tecnico('seguridad')


@ayudamod.route('/seguridad/docx')
@role_required(*ROLES_SEGURIDAD)
def ayudaSeguridadDocx():
    """El manual de seguridad en Word."""
    return _docx_tecnico('seguridad')


@ayudamod.route('/seguridad/pdf')
@role_required(*ROLES_SEGURIDAD)
def ayudaSeguridadPdf():
    """El manual de seguridad en PDF."""
    return _pdf_tecnico('seguridad')


@ayudamod.route('/infraestructura')
@role_required(*ROLES_SEGURIDAD)
def ayudaInfraestructura():
    """Vista previa del manual de infraestructura."""
    return _vista_tecnico('infraestructura')


@ayudamod.route('/infraestructura/docx')
@role_required(*ROLES_SEGURIDAD)
def ayudaInfraestructuraDocx():
    """El manual de infraestructura en Word."""
    return _docx_tecnico('infraestructura')


@ayudamod.route('/infraestructura/pdf')
@role_required(*ROLES_SEGURIDAD)
def ayudaInfraestructuraPdf():
    """El manual de infraestructura en PDF."""
    return _pdf_tecnico('infraestructura')
