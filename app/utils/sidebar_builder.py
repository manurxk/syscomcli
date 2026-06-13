from app.utils.template_helpers import (
    es_admin_o_superadmin, es_superadmin, es_recepcion, es_ventas, 
    es_especialista, es_caja, puede_acceder_modulo, tiene_permiso
)

def _get_sales_groups():
    groups = []
    
    # Grupo: Caja y Tesorería
    groups.append({
        'heading': 'Caja y Tesorería',
        'items': [
            {'title': 'Apertura/Cierre de Caja', 'icon': 'unlock', 'endpoint': 'apertura_cierre_caja.aperturaCierreIndex'},
            {'title': 'Arqueo de Caja', 'icon': 'monitor', 'endpoint': 'arqueo_caja.arqueoCajaIndex'},
            {'title': 'Recaudaciones', 'icon': 'trending-up', 'endpoint': 'recaudacion.recaudacionIndex'},
            {'title': 'Cobranzas', 'icon': 'credit-card', 'endpoint': 'cobranza.cobranzaIndex'},
            {'title': 'Cuentas a Cobrar', 'icon': 'list', 'endpoint': 'cuenta_cobrar.cuentaCobrarIndex'},
        ]
    })
    
    # Grupo: Facturación y Ventas
    groups.append({
        'heading': 'Facturación y Ventas',
        'items': [
            {'title': 'Presupuestos de Venta', 'icon': 'clipboard', 'endpoint': 'registrarpresupuesto.presupuestoIndex'},
            {'title': 'Registrar Pedido', 'icon': 'shopping-cart', 'endpoint': 'pedido.pedidoIndex'},
            {'title': 'Registrar Factura', 'icon': 'file-text', 'endpoint': 'factura.facturaIndex'},
            {'title': 'Insumos de Venta', 'icon': 'package', 'endpoint': 'registrarinsumo.insumoIndex'},
            {'title': 'Notas de Crédito', 'icon': 'minus-circle', 'endpoint': 'nota_credito.notaCreditoIndex'},
            {'title': 'Notas de Débito', 'icon': 'plus-circle', 'endpoint': 'nota_debito.notaDebitoIndex'},
            {'title': 'Libro de Ventas', 'icon': 'book-open', 'endpoint': 'libro_ventas.libroVentasIndex'},
        ]
    })
    
    # Grupo: Configuración Comercial
    if es_admin_o_superadmin():
        groups.append({
            'heading': 'Configuración Comercial',
            'items': [
                {'title': 'Timbrados', 'icon': 'hash', 'endpoint': 'timbrado.timbradoIndex'},
                {'title': 'Establecimientos', 'icon': 'home', 'endpoint': 'establecimiento.establecimientoIndex'},
                {'title': 'Puntos de Expedición', 'icon': 'map-pin', 'endpoint': 'puntoexpedicion.puntoExpedicionIndex'},
            ]
        })
        
    return groups

def build_sidebar():
    """Builds the sidebar structure based on current user's permissions."""
    sidebar = []
    is_super = es_superadmin()
    
    # ---------------------------------------------------------
    # 1. GESTIÓN DEL SISTEMA
    # ---------------------------------------------------------
    if es_admin_o_superadmin():
        if is_super:
            # Dropdown style for Superadmin
            sidebar.append({
                'is_flat': False,
                'heading': 'GESTIÓN DEL SISTEMA',
                'menus': [
                    {
                        'id': 'collapseDatosMaestros',
                        'title': 'Datos Maestros',
                        'icon': 'users',
                        'links': [
                            {'title': 'Pacientes', 'endpoint': 'paciente.pacienteIndex'},
                            {'title': 'Funcionarios', 'endpoint': 'funcionario.funcionarioIndex'},
                            {'title': 'Usuarios', 'endpoint': 'usuario.usuarioIndex'}
                        ]
                    },
                    {
                        'id': 'collapseConfigClinica',
                        'title': 'Configuración Clínica',
                        'icon': 'settings',
                        'links': [
                            {'title': 'Especialidades', 'endpoint': 'especialidad.especialidadIndex'},
                            {'title': 'Consultorios', 'endpoint': 'consultorio.consultorioIndex'},
                            {'title': 'Días Laborables', 'endpoint': 'dia.diaIndex'},
                            {'title': 'Feriados', 'endpoint': 'feriados.feriadoIndex'},
                            {'title': 'Sedes (Sucursales)', 'endpoint': 'sede.sedeIndex'},
                            {'title': 'Datos de la Clínica', 'endpoint': 'empresa.empresaIndex'}
                        ]
                    },
                    {
                        'id': 'collapseSeguridad',
                        'title': 'Seguridad y Sistema',
                        'icon': 'shield',
                        'links': [
                            {'title': 'Grupos y Permisos', 'endpoint': 'grupo.grupoIndex'},
                            {'title': 'Módulos', 'endpoint': 'modulo.moduloIndex'},
                            {'title': 'Cargos', 'endpoint': 'cargo.cargoIndex'}
                        ]
                    }
                ]
            })
        else:
            # Original flat style
            system_groups = []
            system_groups.append({
                'heading': 'Datos Maestros',
                'items': [
                    {'title': 'Pacientes', 'icon': 'users', 'endpoint': 'paciente.pacienteIndex'},
                    {'title': 'Funcionarios', 'icon': 'user-check', 'endpoint': 'funcionario.funcionarioIndex'},
                ]
            })
            system_groups.append({
                'heading': 'Configuración Clínica',
                'items': [
                    {'title': 'Especialidades', 'icon': 'star', 'endpoint': 'especialidad.especialidadIndex'},
                    {'title': 'Consultorios', 'icon': 'home', 'endpoint': 'consultorio.consultorioIndex'},
                    {'title': 'Días Laborables', 'icon': 'calendar', 'endpoint': 'dia.diaIndex'},
                    {'title': 'Feriados', 'icon': 'flag', 'endpoint': 'feriados.feriadoIndex'},
                    {'title': 'Sedes (Sucursales)', 'icon': 'map-pin', 'endpoint': 'sede.sedeIndex'},
                    {'title': 'Datos de la Clínica', 'icon': 'settings', 'endpoint': 'empresa.empresaIndex'},
                ]
            })
            sidebar.append({'is_flat': True, 'groups': system_groups})

    # ---------------------------------------------------------
    # 2. ATENCIÓN AL PACIENTE
    # ---------------------------------------------------------
    if is_super:
         # Consistent dropdown style for Superadmin
         sidebar.append({
             'is_flat': False,
             'heading': 'ATENCIÓN AL PACIENTE',
             'menus': [
                 {
                     'id': 'collapseMiTrabajo',
                     'title': 'Mi Trabajo',
                     'icon': 'user',
                     'links': [
                         {'title': 'Mi Agenda', 'endpoint': 'miagenda.miAgendaIndex'},
                         {'title': 'Próximas Citas', 'endpoint': 'cita.citaIndex'}
                     ]
                 },
                 {
                     'id': 'collapseConsultas',
                     'title': 'Consultas y Clínica',
                     'icon': 'activity',
                     'links': [
                         {'title': 'Registrar Consulta', 'endpoint': 'registrarconsulta.consultaIndex'},
                         {'title': 'Diagnósticos', 'endpoint': 'registrar_diagnostico.diagnosticoIndex'},
                         {'title': 'Tratamientos', 'endpoint': 'registrartratamiento.tratamientoIndex'},
                         {'title': 'Procedimientos', 'endpoint': 'registrarprocedimiento.procedimientoIndex'},
                         {'title': 'Anamnesis', 'endpoint': 'anamnesis.anamnesisIndex'}
                     ]
                 },
                 {
                     'id': 'collapseAgendamiento',
                     'title': 'Agendamiento y Recepción',
                     'icon': 'calendar',
                     'links': [
                         {'title': 'Agenda Médica', 'endpoint': 'agenda.agendaIndex'},
                         {'title': 'Citas Médicas', 'endpoint': 'cita.citaIndex'},
                         {'title': 'Calendario', 'endpoint': 'cita.calendario'},
                         {'title': 'Fichas Médicas', 'endpoint': 'fichamedica.fichaMedicaIndex'}
                     ]
                 }
             ]
         })
    else:
        patient_groups = []
        if es_especialista():
            patient_groups.append({'heading': 'Mi Trabajo', 'items': [{'title': 'Mi Agenda', 'icon': 'calendar', 'endpoint': 'miagenda.miAgendaIndex'}, {'title': 'Próximas Citas', 'icon': 'clock', 'endpoint': 'cita.citaIndex'}]})
        if es_especialista() or es_admin_o_superadmin():
            patient_groups.append({'heading': 'Consultas y Clínica', 'items': [{'title': 'Registrar Consulta', 'icon': 'activity', 'endpoint': 'registrarconsulta.consultaIndex'}, {'title': 'Diagnósticos', 'icon': 'file-text', 'endpoint': 'registrar_diagnostico.diagnosticoIndex'}, {'title': 'Tratamientos', 'icon': 'heart', 'endpoint': 'registrartratamiento.tratamientoIndex'}, {'title': 'Procedimientos', 'icon': 'check-square', 'endpoint': 'registrarprocedimiento.procedimientoIndex'}, {'title': 'Anamnesis', 'icon': 'clipboard', 'endpoint': 'anamnesis.anamnesisIndex'}]})
        if es_recepcion() or es_admin_o_superadmin():
            items = [{'title': 'Agenda Médica', 'icon': 'calendar', 'endpoint': 'agenda.agendaIndex'}, {'title': 'Citas Médicas', 'icon': 'clock', 'endpoint': 'cita.citaIndex'}, {'title': 'Calendario', 'icon': 'calendar-check', 'endpoint': 'cita.calendario'}, {'title': 'Fichas Médicas', 'icon': 'users', 'endpoint': 'fichamedica.fichaMedicaIndex'}]
            if not es_admin_o_superadmin(): items.append({'title': 'Pacientes', 'icon': 'user-plus', 'endpoint': 'paciente.pacienteIndex'})
            patient_groups.append({'heading': 'Agendamiento y Recepción', 'items': items})
        if patient_groups:
            sidebar.append({'is_flat': True, 'groups': patient_groups})

    # ---------------------------------------------------------
    # 3. VENTAS Y CAJA
    # ---------------------------------------------------------
    if is_super:
        sales_groups = _get_sales_groups()
        sidebar.append({
            'is_flat': False,
            'heading': 'VENTAS Y CAJA',
            'menus': [
                {
                    'id': 'collapseCaja',
                    'title': 'Caja y Tesorería',
                    'icon': 'dollar-sign',
                    'links': sales_groups[0]['items']
                },
                {
                    'id': 'collapseFactura',
                    'title': 'Facturación',
                    'icon': 'file-text',
                    'links': sales_groups[1]['items']
                },
                {
                    'id': 'collapseComercial',
                    'title': 'Configuración Comercial',
                    'icon': 'settings',
                    'links': sales_groups[2]['items']
                }
            ]
        })
    else:
        # User is not Superadmin, show flat sales menu if they have permission
        if es_ventas() or es_caja() or es_admin_o_superadmin():
            sidebar.append({
                'is_flat': True,
                'groups': _get_sales_groups()
            })
        
    # ---------------------------------------------------------
    # 4. REPORTES
    # ---------------------------------------------------------
    if any([es_admin_o_superadmin(), es_ventas(), es_recepcion(), es_especialista(), es_caja()]):
        reportes_groups = [{
            'heading': 'Módulo de Reportes',
            'items': [
                {'title': 'Dashboard Reportes', 'icon': 'bar-chart-2', 'endpoint': 'reporte.reportes_index'},
                {'title': 'Reporte de Ventas', 'icon': 'trending-up', 'endpoint': 'reporte.reporte_ventas'},
                {'title': 'Reporte Agendamiento', 'icon': 'calendar', 'endpoint': 'reporte.reporte_agendamiento'},
                {'title': 'Reporte Consultorio', 'icon': 'activity', 'endpoint': 'reporte.reporte_consultorio'}
            ]
        }]
        
        if is_super:
            sidebar.append({
                'is_flat': False,
                'heading': 'REPORTES DEL SISTEMA',
                'menus': [
                    {
                        'id': 'collapseReportes',
                        'title': 'Análisis y Reportes',
                        'icon': 'bar-chart-2',
                        'links': reportes_groups[0]['items']
                    }
                ]
            })
        else:
            sidebar.append({
                'is_flat': True,
                'groups': reportes_groups
            })

    return sidebar

# Auxiliares
def _get_specialist_patient_items():
    items = []
    if tiene_permiso('/modulos/fichamedica/fichamedica-index') or puede_acceder_modulo('Agendamiento'):
        items.append({'title': 'Fichas Médicas', 'icon': 'users', 'endpoint': 'fichamedica.fichaMedicaIndex'})
        
    items.extend([
        {'title': 'Presupuestos', 'icon': 'dollar-sign', 'endpoint': 'registrarpresupuesto.presupuestoIndex'},
        {'title': 'Recetas Médicas', 'icon': 'file-plus', 'endpoint': 'registrarreceta.recetaIndex'},
        {'title': 'Órdenes de Estudios', 'icon': 'microscope', 'endpoint': 'registrarordenestudio.ordenEstudioIndex'},
        {'title': 'Certificados Médicos', 'icon': 'award', 'endpoint': 'registrarcertificadomedico.certificadoMedicoIndex'},
        {'title': 'Insumos Médicos', 'icon': 'package', 'endpoint': 'registrarinsumo.insumoIndex'},
    ])
    return items

