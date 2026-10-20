"""
Capturas de pantalla para la Guía de uso (botón ? y su PDF).

Entra a Sysclin con un navegador automatizado (Playwright), recorre las pantallas
de la lista CAPTURAS, marca con ①②③ los botones y campos de cada paso y guarda la imagen en
app/static/img/ayuda/<seccion>/<archivo>. Las secciones de la guía las muestran solas.

Se ejecuta en un contenedor temporal, dentro de la red de Sysclin (no toca la app):
    docker run --rm --network dock_network-tesis -e CAPTURAS_PASS_LGONZALEZ -v "${PWD}:/repo" -w /repo `
      mcr.microsoft.com/playwright/python:v1.49.0-noble sh -c `
      "pip install -q --break-system-packages playwright==1.49.0 && python docs/scripts/capturas_manual.py [seccion]"

Sin argumento regenera todas; con una sección (por ejemplo "citas"), solo esa.

Notas:
- Usa cuentas de PRUEBA sin MFA (el código llega por correo y el script no lo lee).
  La contraseña sale de CAPTURAS_PASS_<USUARIO> o, solo para las cuentas del seed (recep2, cajero1),
  de su valor conocido. Sin contraseña el rol se saltea: no se prueban claves, porque cada fallo
  suma al bloqueo de la cuenta. Ej.: -e CAPTURAS_PASS_PSICOADMIN para las capturas de ADMIN.
- Sysclin permite una sola sesión por usuario: no usar una cuenta que alguien tenga abierta.
- Las capturas muestran lo que haya en la base: correrlo solo con datos de prueba.
- El script solo navega y abre formularios o modales: nunca presiona Guardar.
"""
import os
import sys

from playwright.sync_api import sync_playwright

BASE = os.getenv('CAPTURAS_BASE_URL', 'https://nginx')
SALIDA = os.path.join('app', 'static', 'img', 'ayuda')
PASS_USUARIOS_PRUEBA = 'Prueba2026!'  # la del seed (docs/scripts/seed_prueba.py)

# Cuenta de prueba por rol (sin MFA)
USUARIOS = {
    'RECEPCION': 'recep2',
    'CLINICO': 'lgonzalez',
    'VENTAS': 'cajero1',
    'ADMIN': 'psicoadmin',     # ADMINISTRADOR + CLINICO, sin MFA (Funcionarios)
}
CUENTAS_SEED = ('recep2', 'cajero1')

# Datos de prueba que usan algunas pantallas (paciente CI 9000009 y una consulta suya)
ID_CONSULTA_PRUEBA = 27
ID_CONSULTA_CON_ORDENES = 24   # consulta de lgonzalez con órdenes cargadas (impresión)


def boton(texto):
    """Botón o enlace visible por su texto."""
    return f':is(a, button):visible:has-text("{texto}")'


def campo(texto):
    """Campo de formulario por el texto de su etiqueta (marca la etiqueta y el control)."""
    return f'div:has(> label:has-text("{texto}")):visible'


def titulo(texto):
    """Título de un bloque del formulario."""
    return f':is(h5, h6, .card-header, .card-title):visible:has-text("{texto}")'


MODAL = '.modal.show .modal-content'

# Cada captura: sección de la guía, archivo, rol, pantalla, acciones previas y marcas (selector, número de paso[, 'esquina']).
# Acciones: ('click', selector), ('esperar', selector) o ('js', código que se ejecuta en la página).
# Recorte opcional: 'hasta' corta debajo de ese elemento; 'desde' empieza arriba de ese elemento;
# 'alto' limita la altura en píxeles; 'elemento' captura solo ese elemento (por ejemplo, un modal).
CAPTURAS = [
    # ---------------- Recepción ----------------
    {
        'seccion': 'pacientes', 'archivo': '01_listado.jpg', 'rol': 'RECEPCION',
        'url': '/mantenimiento/paciente/paciente-index',
        'marcas': [(boton('Nuevo Paciente'), 1)], 'hasta': boton('Nuevo Paciente'),
    },
    {
        'seccion': 'pacientes', 'archivo': '02_formulario.jpg', 'rol': 'RECEPCION',
        'url': '/mantenimiento/paciente/paciente-agregar',
        'marcas': [(titulo('Datos Personales'), 2), (titulo('Documento para Facturación'), 3),
                   (titulo('Contacto'), 4), (titulo('Notas Clínicas'), 6), (boton('Registrar Paciente'), 7, 'esquina')],
    },
    {
        'seccion': 'agenda_medica', 'archivo': '01_listado.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/agenda-horarios/agenda-horarios-index',
        'marcas': [(boton('Nuevo Horario'), 1)], 'hasta': boton('Nuevo Horario'),
    },
    {
        'seccion': 'agenda_medica', 'archivo': '02_nuevo_horario.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/agenda-horarios/agenda-horarios-index',
        # "Nuevo Horario" pide elegir antes un especialista
        'acciones': [('esperar', '#selectEspecialista option:nth-child(2)'),
                     ('js', "const s = document.getElementById('selectEspecialista'); "
                            "s.value = s.options[1].value; $(s).trigger('change');"),
                     ('click', boton('Nuevo Horario')), ('esperar', MODAL)],
        'elemento': MODAL,
        'marcas': [(campo('Sede'), 2), (campo('Día'), 3), (campo('Hora inicio'), 4), (campo('Duración'), 5),
                   (campo('Modalidad'), 6), (campo('Fecha desde'), 7), (boton('Guardar'), 8, 'esquina')],
    },
    {
        'seccion': 'citas', 'archivo': '01_listado.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/citas/citas-index',
        'marcas': [('a.btn[href$="citas-agregar"]', 1)],
        'hasta': '.card-header',  # título + botón; la tabla no aporta a este paso
    },
    {
        'seccion': 'citas', 'archivo': '02_nueva_cita.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/citas/citas-agregar',
        'marcas': [
            ('#btnBuscarPaciente', 2),
            ('#selectEspecialista', 3),
            ('#txtFechaCita', 4),
            ('.tipo-cita-card[data-tipo="primera_vez"]', 5),
            ('#selectModalidad', 6),
            ('#btnGuardarCita', 7, 'esquina'),
        ],
    },
    {
        'seccion': 'citas', 'archivo': '03_corregir_boton.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/citas/citas-index',
        'acciones': [('esperar', '#tbl tbody tr td'), ('js', "$('#tbl').DataTable().search('Completada').draw()"),
                     ('esperar', '#tbl tbody tr button[name="btn_corregir"]')],
        'marcas': [('#tbl tbody tr:first-child button[name="btn_corregir"]', 1, 'esquina')],
        'desde': '#tbl', 'alto': 430,
    },
    {
        'seccion': 'citas', 'archivo': '04_corregir.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/citas/citas-index',
        'acciones': [('esperar', '#tbl tbody tr td'), ('js', "$('#tbl').DataTable().search('Completada').draw()"),
                     ('click', '#tbl tbody tr:first-child button[name="btn_corregir"]'),
                     ('esperar', '.swal2-popup #corrMotivo'),
                     ('js', "document.getElementById('corrEstado').value = 'AUSENTE'; "
                            "document.getElementById('corrMotivo').value = 'El paciente no vino; se marcó completada por error.'")],
        'elemento': '.swal2-popup',
        'marcas': [('#corrEstado', 2), ('#corrMotivo', 3), ('#corrUsuario', 4), ('.swal2-confirm', 5, 'esquina')],
    },
    {
        'seccion': 'lista_espera', 'archivo': '01_listado.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/lista-espera/lista-espera-index',
        'marcas': [(boton('Agregar'), 1)], 'hasta': boton('Agregar'),
    },
    {
        'seccion': 'lista_espera', 'archivo': '02_agregar.jpg', 'rol': 'RECEPCION',
        'url': '/agendamiento/lista-espera/lista-espera-index',
        'acciones': [('click', boton('Agregar')), ('esperar', MODAL)],
        'elemento': MODAL,
        'marcas': [(campo('Agenda'), 2), (campo('Paciente'), 3), (campo('Prioridad'), 4),
                   (campo('Motivo'), 5), (boton('Guardar'), 6, 'esquina')],
    },
    # ---------------- Clínico ----------------
    {
        'seccion': 'mi_agenda', 'archivo': '01_citas_hoy.jpg', 'rol': 'CLINICO',
        'url': '/agendamiento/mi-agenda',
        'marcas': [(titulo('Citas de Hoy'), 1), (boton('Iniciar'), 2, 'esquina')],
        'alto': 700,
    },
    {
        'seccion': 'consultas', 'archivo': '01_atencion.jpg', 'rol': 'CLINICO',
        'url': f'/clinico/consulta/consulta-editar/{ID_CONSULTA_PRUEBA}',
        'marcas': [(campo('Motivo de Consulta'), 1), (boton('Guardar Cambios'), 2, 'esquina')],
        'hasta': boton('Guardar Cambios'),
    },
    {
        'seccion': 'consultas', 'archivo': '02_imprimir_lista.jpg', 'rol': 'CLINICO',
        'url': f'/clinico/consulta/consulta-editar/{ID_CONSULTA_CON_ORDENES}',
        'acciones': [('esperar', '#tbody-ordenes a[title="Imprimir"]')],
        'marcas': [('#tbody-ordenes a[title="Imprimir"]', 1, 'esquina')],
        'desde': titulo('Órdenes'), 'hasta': '#tbody-ordenes',
    },
    {
        'seccion': 'consultas', 'archivo': '03_imprimir_aviso.jpg', 'rol': 'CLINICO',
        'url': f'/clinico/consulta/consulta-editar/{ID_CONSULTA_CON_ORDENES}',
        # El aviso que aparece al guardar, mostrado sin guardar nada (el script nunca guarda)
        'acciones': [('esperar', '#tbody-ordenes'), ('js', "ofrecerImprimir('#', 'Orden guardada')"),
                     ('esperar', '.swal2-popup a.btn-primary')],
        'elemento': '.swal2-popup',
        'marcas': [('.swal2-popup a.btn-primary', 1)],
    },
    {
        'seccion': 'pei', 'archivo': '01_listado.jpg', 'rol': 'CLINICO',
        'url': '/clinico/pei/pei-index',
        'marcas': [(boton('Nuevo PEI'), 1)], 'hasta': boton('Nuevo PEI'),
    },
    {
        'seccion': 'pei', 'archivo': '02_nuevo.jpg', 'rol': 'CLINICO',
        'url': '/clinico/pei/pei-agregar',
        'marcas': [(campo('Paciente'), 2), (boton('Seleccionar y continuar'), 3, 'esquina')],
        'alto': 700,
    },
    {
        'seccion': 'fichas_medicas', 'archivo': '01_listado.jpg', 'rol': 'CLINICO',
        'url': '/clinico/ficha/ficha-index',
        'marcas': [('input[type="search"]:visible', 1), (boton('Ver ficha'), 2, 'esquina')],
        'alto': 620,
    },
    # ---------------- Administración ----------------
    {
        'seccion': 'funcionarios', 'archivo': '01_listado.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/funcionario/funcionario-index',
        'marcas': [(boton('Nuevo Funcionario'), 1)], 'hasta': boton('Nuevo Funcionario'),
    },
    {
        'seccion': 'funcionarios', 'archivo': '02_formulario.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/funcionario/funcionario-agregar',
        # Cargo clínico para que aparezca "Datos de Especialista" (paso 4)
        'acciones': [('esperar', '#id_cargo option:nth-child(2)'),
                     ('js', "const s = document.getElementById('id_cargo'); "
                            "const o = [...s.options].find(o => /^PSIC[OÓ]LOGO$/i.test(o.text.trim())); "
                            "if (o) { s.value = o.value; $(s).trigger('change'); }"),
                     ('esperar', '#collapseEspecialista.show')],
        'marcas': [(titulo('Datos Personales'), 2), (campo('Cargo Asignado'), 3),
                   (titulo('Datos de Especialista'), 4), ('#btnGuardar', 5, 'esquina')],
    },
    {
        'seccion': 'usuarios', 'archivo': '01_listado.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/usuario/usuario-index',
        'marcas': [(boton('Nuevo Usuario'), 1)], 'hasta': boton('Nuevo Usuario'),
    },
    {
        'seccion': 'usuarios', 'archivo': '02_formulario.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/usuario/usuario-agregar',
        'acciones': [('esperar', '#id_rol option:nth-child(2)')],
        'marcas': [(titulo('Funcionario Asociado'), 2), (campo('Username'), 3), (campo('Rol Principal'), 4),
                   (titulo('Contraseña'), 6), ('#btnGuardar', 7, 'esquina')],
    },
    {
        # Detalle de recep2 (id 5, cuenta del seed): datos y acciones (los registros de acceso están en Auditoría)
        'seccion': 'usuarios', 'archivo': '03_detalle.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/usuario/usuario-detalle/5',
        'marcas': [('a.btn[href*="auditoria-index"]', 1, 'esquina'), ('#btnResetear', 2, 'esquina'), (titulo('Sesiones activas'), 3)],
        'hasta': titulo('Sesiones activas'),
    },
    {
        'seccion': 'permisos', 'archivo': '01_matriz.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/referenciales/permisos/permisos-index',
        'acciones': [('esperar', '#selRol option:nth-child(2)'),
                     ('js', "const s = document.getElementById('selRol'); "
                            "const o = [...s.options].find(o => /RECEP/i.test(o.text)); "
                            "if (o) { s.value = o.value; $(s).trigger('change'); }"),
                     ('esperar', '#tblMatriz .chk-permiso')],
        'marcas': [('#selRol', 1, 'esquina'), ('#tblMatriz thead', 2), (boton('Guardar cambios'), 3, 'esquina')],
        'alto': 900,
    },
    {
        'seccion': 'menu', 'archivo': '01_menu.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/seguridad/menu/menu-index',
        'acciones': [('esperar', '#selRol option:nth-child(2)'),
                     ('js', "const s = document.getElementById('selRol'); "
                            "const o = [...s.options].find(o => /RECEP/i.test(o.text)); "
                            "if (o) { s.value = o.value; $(s).trigger('change'); }"),
                     ('esperar', '#tblMatriz .chk-visible')],
        'marcas': [('#selRol', 1, 'esquina'), ('#tblMatriz thead', 2), (boton('Guardar cambios'), 3, 'esquina')],
        'alto': 900,
    },
    # Auditoría: pantalla única con pestañas (PDF 9 + 6, paso 5); Accesos es la pestaña "Sesiones y usuarios"
    {
        'seccion': 'auditoria', 'archivo': '01_cambios.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/auditoria/auditoria-index?tab=cambios',
        'acciones': [('esperar', '#tblCambios tbody tr .btn-ver-cambio')],
        'marcas': [('#cFechaDesde', 1), ('#cModulo', 2), ('#cFiltrar', 3, 'esquina'),
                   ('#tblCambios tbody tr:first-child .btn-ver-cambio', 4, 'esquina')],
        'alto': 1100,
    },
    {
        'seccion': 'auditoria', 'archivo': '02_detalle_cambio.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/auditoria/auditoria-index?tab=cambios',
        'acciones': [('esperar', '#tblCambios tbody tr .btn-ver-cambio'),
                     ('click', '#tblCambios tbody tr:first-child .btn-ver-cambio'), ('esperar', MODAL)],
        'elemento': MODAL,
        'marcas': [('#cambioTodos', 1)],
    },
    {
        'seccion': 'auditoria', 'archivo': '03_eventos.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/auditoria/auditoria-index?tab=eventos',
        'acciones': [('esperar', '#tblEventos tbody tr')],
        'marcas': [('#eAccion', 1), ('#eFiltrar', 2, 'esquina')],
        'alto': 900,
    },
    {
        'seccion': 'auditoria', 'archivo': '04_accesos.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/auditoria/auditoria-index?tab=accesos',
        'acciones': [('esperar', '#tblIntentos tbody tr')],
        'marcas': [('#aSoloFallidos', 1)],
        'alto': 900,
    },
    {
        'seccion': 'auditoria', 'archivo': '05_sesiones.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/auditoria/auditoria-index?tab=sesiones',
        'acciones': [('esperar', '#tbodyAccesos .btn-ver-sesiones')],
        'marcas': [('#tbodyAccesos .btn-ver-sesiones', 1)],
        'alto': 700,
    },
    {
        'seccion': 'referenciales', 'archivo': '01_indice.jpg', 'rol': 'ADMIN',
        # Sin recorte de alto: tiene que verse también el grupo Ventas
        'url': '/mantenimiento/referenciales/referenciales-index',
    },
    {
        'seccion': 'referenciales', 'archivo': '02_cargos.jpg', 'rol': 'ADMIN',
        'url': '/mantenimiento/referenciales/cargo/cargo-index',
        'acciones': [('click', boton('Agregar')), ('esperar', MODAL)],
        'elemento': MODAL,
        'marcas': [(campo('Descripción'), 3), (boton('Guardar'), 4, 'esquina')],
    },
    {
        'seccion': 'reportes', 'archivo': '01_filtros.jpg', 'rol': 'ADMIN',
        'url': '/reporte/index',
        'marcas': [(campo('Desde'), 1), (boton('Aplicar'), 2, 'esquina'), (boton('Exportar PDF'), 3, 'esquina')],
    },
    # ---------------- Ventas ----------------
    {
        'seccion': 'timbrados', 'archivo': '01_listado.jpg', 'rol': 'ADMIN',
        'url': '/ventas/referenciales/timbrado/timbrado-index',
        'marcas': [(boton('Agregar'), 1)], 'hasta': boton('Agregar'),
    },
    {
        'seccion': 'timbrados', 'archivo': '02_agregar.jpg', 'rol': 'ADMIN',
        'url': '/ventas/referenciales/timbrado/timbrado-index',
        'acciones': [('click', boton('Agregar')), ('esperar', MODAL)],
        'elemento': MODAL,
        'marcas': [(campo('Timbrado'), 2), (campo('Fecha inicio'), 3), (boton('Guardar'), 4, 'esquina')],
    },
    {
        'seccion': 'puntos_expedicion', 'archivo': '01_listado.jpg', 'rol': 'ADMIN',
        'url': '/ventas/referenciales/punto-expedicion/punto-expedicion-index',
        'marcas': [(boton('Agregar'), 1)], 'hasta': boton('Agregar'),
    },
    {
        'seccion': 'puntos_expedicion', 'archivo': '02_agregar.jpg', 'rol': 'ADMIN',
        'url': '/ventas/referenciales/punto-expedicion/punto-expedicion-index',
        'acciones': [('click', boton('Agregar')), ('esperar', MODAL)],
        'elemento': MODAL,
        'marcas': [(campo('Timbrado'), 2), (campo('Código'), 3), (boton('Guardar'), 4, 'esquina')],
    },
    {
        'seccion': 'pedidos', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/pedido/pedido-index',
        'marcas': [(boton('Nuevo Pedido'), 1)], 'hasta': boton('Nuevo Pedido'),
    },
    {
        'seccion': 'pedidos', 'archivo': '02_nuevo.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/pedido/pedido-agregar',
        'marcas': [(boton('Seleccionar y continuar'), 2, 'esquina'), (boton('Guardar Pedido'), 6, 'esquina')],
        'alto': 760,
    },
    {
        'seccion': 'presupuestos', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/presupuesto/presupuesto-index',
        'marcas': [(boton('Nuevo Presupuesto'), 1)], 'hasta': boton('Nuevo Presupuesto'),
    },
    {
        'seccion': 'presupuestos', 'archivo': '02_nuevo.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/presupuesto/presupuesto-agregar',
        'marcas': [(boton('Seleccionar y continuar'), 2, 'esquina'), (boton('Guardar Presupuesto'), 6, 'esquina')],
        'alto': 760,
    },
    {
        'seccion': 'caja_estado', 'archivo': '01_estado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/caja/caja-estado',
        'marcas': [(boton('Abrir Caja'), 1, 'esquina')],
        'alto': 620,
    },
    {
        'seccion': 'caja_historial', 'archivo': '01_historial.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/caja/caja-historial',
        'alto': 560,
    },
    {
        'seccion': 'arqueos', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/arqueo-caja/arqueo-index',
        'marcas': [(boton('Nuevo Arqueo'), 1)], 'hasta': boton('Nuevo Arqueo'),
    },
    {
        'seccion': 'arqueos', 'archivo': '02_nuevo.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/arqueo-caja/arqueo-agregar',
        'marcas': [(campo('Caja'), 2), (boton('Cargar apertura activa'), 2, 'esquina'), (campo('Monto real'), 4),
                   (boton('Calcular diferencia'), 5, 'esquina'), (boton('Guardar Arqueo'), 6, 'esquina')],
    },
    {
        'seccion': 'facturas', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/factura/factura-index',
        'marcas': [(boton('Nueva Factura'), 1)], 'hasta': boton('Nueva Factura'),
    },
    {
        'seccion': 'facturas', 'archivo': '02_nueva.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/factura/factura-agregar',
        'marcas': [(boton('Seleccionar y continuar'), 2, 'esquina'), (titulo('Datos de la Factura'), 4),
                   (boton('Agregar Ítem'), 5, 'esquina'), (boton('Emitir Factura'), 7, 'esquina')],
    },
    {
        'seccion': 'remisiones', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/remision/remision-index',
        'marcas': [(boton('Nueva Remisión'), 1)], 'hasta': boton('Nueva Remisión'),
    },
    {
        'seccion': 'remisiones', 'archivo': '02_nueva.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/remision/remision-agregar',
        'marcas': [(boton('Seleccionar y continuar'), 2, 'esquina'), (boton('Agregar Ítem'), 5, 'esquina'),
                   (boton('Guardar Remisión'), 6, 'esquina')],
    },
    {
        'seccion': 'notas_credito', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/nota-credito/nota-credito-index',
        'marcas': [(boton('Nueva Nota de Crédito'), 1)], 'hasta': boton('Nueva Nota de Crédito'),
    },
    {
        'seccion': 'notas_credito', 'archivo': '02_nueva.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/nota-credito/nota-credito-agregar',
        'marcas': [(boton('Seleccionar y continuar'), 2, 'esquina'), (campo('Motivo'), 3),
                   (boton('Agregar Ítem'), 5, 'esquina'), (boton('Guardar Nota de Crédito'), 6, 'esquina')],
    },
    {
        'seccion': 'notas_debito', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/nota-debito/nota-debito-index',
        'marcas': [(boton('Nueva Nota de Débito'), 1)], 'hasta': boton('Nueva Nota de Débito'),
    },
    {
        'seccion': 'notas_debito', 'archivo': '02_nueva.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/nota-debito/nota-debito-agregar',
        'marcas': [(boton('Seleccionar y continuar'), 2, 'esquina'), (campo('Motivo'), 3),
                   (boton('Agregar Ítem'), 5, 'esquina'), (boton('Guardar Nota de Débito'), 6, 'esquina')],
    },
    {
        'seccion': 'cuentas_cobrar', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/cuenta-cobrar/cuenta-cobrar-index',
        'alto': 560,
    },
    {
        'seccion': 'cobranzas', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/cobranza/cobranza-index',
        'marcas': [(boton('Nueva Cobranza'), 1)], 'hasta': boton('Nueva Cobranza'),
    },
    {
        'seccion': 'cobranzas', 'archivo': '02_nueva.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/cobranza/cobranza-agregar',
        'marcas': [(boton('Seleccionar y continuar'), 2, 'esquina'), (campo('Caja'), 3),
                   (boton('Agregar forma de cobro'), 4, 'esquina'), (boton('Guardar Cobranza'), 8, 'esquina')],
    },
    {
        'seccion': 'recaudaciones', 'archivo': '01_listado.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/recaudacion/recaudacion-index',
        'marcas': [(boton('Nueva Recaudación'), 1)], 'hasta': boton('Nueva Recaudación'),
    },
    {
        'seccion': 'recaudaciones', 'archivo': '02_nueva.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/recaudacion/recaudacion-agregar',
        'marcas': [(campo('Caja'), 2), (campo('Depósito'), 2), (titulo('Desglose de Montos'), 3),
                   (boton('Guardar Recaudación'), 5, 'esquina')],
    },
    {
        'seccion': 'libro_ventas', 'archivo': '01_libro.jpg', 'rol': 'VENTAS',
        'url': '/ventas/movimientos/libro-ventas/libro-ventas-index',
        'alto': 560,
    },
]

# Marca circular violeta (paleta SYSCLIN) más un contorno. Por defecto va a la izquierda del elemento,
# centrada (no tapa la etiqueta de arriba); 'esquina' la pone arriba a la izquierda (botones con vecino al lado).
JS_MARCAR = """
(el, [numero, posicion]) => {
    el.scrollIntoView({block: 'center'});
    const r = el.getBoundingClientRect();
    el.style.outline = '3px solid #7c3aed';
    el.style.outlineOffset = '2px';
    const m = document.createElement('div');
    m.className = 'marca-captura';
    m.textContent = numero;
    m.style.cssText = 'position:absolute;z-index:99999;width:26px;height:26px;border-radius:50%;'
        + 'background:#7c3aed;color:#fff;font:bold 14px Arial,sans-serif;display:flex;align-items:center;'
        + 'justify-content:center;box-shadow:0 0 0 3px #fff;'
        + (posicion === 'esquina'
            ? 'left:' + (r.left + window.scrollX - 14) + 'px;top:' + (r.top + window.scrollY - 14) + 'px;'
            : 'left:' + (r.left + window.scrollX - 34) + 'px;top:' + (r.top + window.scrollY + r.height / 2 - 13) + 'px;');
    document.body.appendChild(m);
}
"""


def clave_de(usuario):
    """Contraseña de la cuenta, o None si no hay que intentar (un fallo suma al bloqueo)."""
    return (os.getenv(f'CAPTURAS_PASS_{usuario.upper()}')
            or (PASS_USUARIOS_PRUEBA if usuario in CUENTAS_SEED else None))


def iniciar_sesion(page, usuario):
    page.goto(f'{BASE}/login')
    page.fill('#inputUsuario', usuario)
    page.fill('#usuario_clave', clave_de(usuario))
    page.click('#btnLogin')
    page.wait_for_url(lambda url: '/login' not in url, timeout=20000)


def caja(page, selector):
    """Caja del primer elemento visible, en coordenadas de la página."""
    loc = page.locator(selector).first
    return loc.bounding_box() if loc.count() else None


def capturar(page, c):
    page.goto(BASE + c['url'])
    page.wait_for_load_state('networkidle')
    for accion, selector in c.get('acciones', []):
        if accion == 'click':
            page.locator(selector).first.click()
        elif accion == 'esperar':
            # Las <option> nunca son "visibles": para esas alcanza con que existan
            estado = 'attached' if 'option' in selector else 'visible'
            page.locator(selector).first.wait_for(state=estado, timeout=8000)
        elif accion == 'js':
            page.evaluate(f'() => {{ {selector} }}')
        page.wait_for_timeout(500)  # animación de modales

    faltantes = []
    for selector, numero, *posicion in c.get('marcas', []):
        loc = page.locator(selector).first
        if loc.count():
            loc.evaluate(JS_MARCAR, [str(numero), posicion[0] if posicion else 'izquierda'])
        else:
            faltantes.append(selector)

    destino = os.path.join(SALIDA, c['seccion'], c['archivo'])
    os.makedirs(os.path.dirname(destino), exist_ok=True)

    if c.get('elemento'):
        # Solo el elemento (un modal), con margen para que se vean las marcas de la izquierda
        page.evaluate('window.scrollTo(0, 0)')
        b = caja(page, c['elemento'])
        clip = {'x': max(b['x'] - 40, 0), 'y': max(b['y'] - 20, 0), 'width': b['width'] + 60, 'height': b['height'] + 40}
    else:
        # Solo el contenido (sin sidebar ni barra superior): la guía explica la pantalla, no el menú
        page.evaluate('window.scrollTo(0, 0)')
        main = caja(page, 'main.app-main')
        arriba, abajo = main['y'], main['y'] + main['height']
        if c.get('desde') and caja(page, c['desde']):
            arriba = max(arriba, caja(page, c['desde'])['y'] - 12)
        if c.get('hasta') and caja(page, c['hasta']):
            b = caja(page, c['hasta'])
            abajo = min(abajo, b['y'] + b['height'] + 14)
        if c.get('alto'):
            abajo = min(abajo, arriba + c['alto'])
        clip = {'x': main['x'], 'y': arriba, 'width': main['width'], 'height': abajo - arriba}

    # Un modal se fotografía en la ventana visible: con full_page el navegador se agranda al alto de toda la
    # página, el modal se reubica y el recorte (calculado antes) ya no coincide (pasaba en páginas largas, como Auditoría)
    page.screenshot(path=destino, type='jpeg', quality=82, full_page=not c.get('elemento'), clip=clip)
    aviso = f"  (sin marcar: {' | '.join(faltantes)})" if faltantes else ''
    print(f'OK  {destino}{aviso}')


def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    capturas = [c for c in CAPTURAS if not filtro or c['seccion'] == filtro]
    if not capturas:
        sys.exit(f'No hay capturas para la sección "{filtro}".')

    with sync_playwright() as p:
        # --lang define el formato de los campos de fecha (dd/mm/aaaa)
        navegador = p.chromium.launch(args=['--lang=es-ES'])
        # Agrupado por rol: una sesión por usuario
        for rol in dict.fromkeys(c['rol'] for c in capturas):
            usuario = USUARIOS[rol]
            if not clave_de(usuario):
                print(f'OMITIDO {rol}: falta CAPTURAS_PASS_{usuario.upper()}')
                continue
            ctx = navegador.new_context(ignore_https_errors=True, viewport={'width': 1366, 'height': 900},
                                        color_scheme='light', locale='es-ES')
            page = ctx.new_page()
            try:
                iniciar_sesion(page, usuario)
            except Exception as e:
                print(f'ERROR no se pudo iniciar sesión como {usuario} ({rol}): {e}')
                ctx.close()
                continue
            print(f'Sesión iniciada como {usuario} ({rol})')
            for c in (c for c in capturas if c['rol'] == rol):
                try:
                    capturar(page, c)
                except Exception as e:
                    print(f'ERROR {c["seccion"]}/{c["archivo"]}: {str(e).splitlines()[0]}')
            page.goto(f'{BASE}/logout')
            ctx.close()
        navegador.close()


if __name__ == '__main__':
    main()
