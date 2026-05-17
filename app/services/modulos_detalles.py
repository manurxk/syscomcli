"""
Servicio para obtener detalles completos de módulos (descripciones, iconos, rutas, colores)
Compatible con el sistema de módulos por rol
"""
from typing import Dict, List, Optional
from flask import url_for

# Mapeo de módulos a sus detalles (descripción, icono, color, ruta)
MODULOS_DETALLES = {
    # SUPERADMINISTRADOR
    'gestion_clinicas': {
        'titulo': 'Gestión de Clínicas/Sedes',
        'descripcion': 'Administrar clínicas, sedes y su configuración',
        'icono': 'fas fa-building',
        'color': 'purple',
        'ruta': None  # TODO: Agregar ruta cuando esté disponible
    },
    'configuracion_global': {
        'titulo': 'Configuración Global',
        'descripcion': 'Configuración general del sistema',
        'icono': 'fas fa-cog',
        'color': 'indigo',
        'ruta': None
    },
    'gestion_administradores': {
        'titulo': 'Gestión de Administradores',
        'descripcion': 'Crear y gestionar administradores del sistema',
        'icono': 'fas fa-user-shield',
        'color': 'purple',
        'ruta': None
    },
    'reportes_consolidados': {
        'titulo': 'Reportes Consolidados',
        'descripcion': 'Reportes de todas las clínicas',
        'icono': 'fas fa-chart-bar',
        'color': 'blue',
        'ruta': None
    },
    'configuracion_precios_planes': {
        'titulo': 'Configuración de Precios y Planes',
        'descripcion': 'Gestionar precios y planes del sistema',
        'icono': 'fas fa-dollar-sign',
        'color': 'green',
        'ruta': None
    },
    'logs_auditoria': {
        'titulo': 'Logs y Auditoría',
        'descripcion': 'Registros y auditoría del sistema',
        'icono': 'fas fa-file-alt',
        'color': 'gray',
        'ruta': None
    },
    'respaldos_mantenimiento': {
        'titulo': 'Respaldos y Mantenimiento',
        'descripcion': 'Gestionar respaldos y mantenimiento',
        'icono': 'fas fa-database',
        'color': 'gray',
        'ruta': None
    },
    
    # ADMINISTRADOR
    'dashboard_admin': {
        'titulo': 'Dashboard Ejecutivo',
        'descripcion': 'Métricas generales y resumen ejecutivo',
        'icono': 'fas fa-tachometer-alt',
        'color': 'blue',
        'ruta': '/dashboard'
    },
    'gestion_usuarios_clinica': {
        'titulo': 'Gestión de Usuarios',
        'descripcion': 'Gestionar usuarios de la clínica',
        'icono': 'fas fa-users',
        'color': 'blue',
        'ruta': None  # url_for('usuario.usuarioIndex')
    },
    'asignacion_roles_permisos': {
        'titulo': 'Roles y Permisos',
        'descripcion': 'Asignar roles y permisos a usuarios',
        'icono': 'fas fa-user-cog',
        'color': 'blue',
        'ruta': None
    },
    'reportes_financieros': {
        'titulo': 'Reportes Financieros',
        'descripcion': 'Reportes financieros completos',
        'icono': 'fas fa-chart-line',
        'color': 'green',
        'ruta': None
    },
    'configuracion_clinica': {
        'titulo': 'Configuración de la Clínica',
        'descripcion': 'Horarios, salas y configuración',
        'icono': 'fas fa-hospital',
        'color': 'blue',
        'ruta': None
    },
    'gestion_especialistas_agenda': {
        'titulo': 'Gestión de Especialistas',
        'descripcion': 'Gestionar especialistas y agenda general',
        'icono': 'fas fa-user-md',
        'color': 'blue',
        'ruta': None
    },
    'reportes_desempeno': {
        'titulo': 'Reportes de Desempeño',
        'descripcion': 'Análisis de desempeño y estadísticas',
        'icono': 'fas fa-chart-pie',
        'color': 'blue',
        'ruta': None
    },
    'inventario_recursos': {
        'titulo': 'Inventario y Recursos',
        'descripcion': 'Gestionar inventario y recursos',
        'icono': 'fas fa-boxes',
        'color': 'orange',
        'ruta': None
    },
    'configuracion_precios_locales': {
        'titulo': 'Configuración de Precios Locales',
        'descripcion': 'Gestionar precios locales de la clínica',
        'icono': 'fas fa-tags',
        'color': 'green',
        'ruta': None
    },
    
    # ESPECIALISTA
    'mi_agenda_personal': {
        'titulo': 'Mi Agenda Personal',
        'descripcion': 'Ver y gestionar mi agenda personal',
        'icono': 'fas fa-calendar-alt',
        'color': 'purple',
        'ruta': None  # url_for('agenda.agendaIndex')
    },
    'mis_pacientes_asignados': {
        'titulo': 'Mis Pacientes Asignados',
        'descripcion': 'Ver mis pacientes asignados',
        'icono': 'fas fa-user-injured',
        'color': 'purple',
        'ruta': None
    },
    'historias_clinicas': {
        'titulo': 'Historias Clínicas',
        'descripcion': 'Crear, editar y consultar historias clínicas',
        'icono': 'fas fa-notes-medical',
        'color': 'purple',
        'ruta': None  # url_for('registrarconsulta.consultaIndex')
    },
    'sesiones_programadas': {
        'titulo': 'Sesiones Programadas',
        'descripcion': 'Ver y gestionar sesiones programadas',
        'icono': 'fas fa-calendar-check',
        'color': 'purple',
        'ruta': None
    },
    'notas_evolucion': {
        'titulo': 'Notas de Evolución',
        'descripcion': 'Registrar notas de evolución de pacientes',
        'icono': 'fas fa-file-medical',
        'color': 'purple',
        'ruta': None
    },
    'planes_tratamiento': {
        'titulo': 'Planes de Tratamiento',
        'descripcion': 'Crear y gestionar planes de tratamiento',
        'icono': 'fas fa-clipboard-list',
        'color': 'purple',
        'ruta': None
    },
    'documentos_evaluaciones': {
        'titulo': 'Documentos y Evaluaciones',
        'descripcion': 'Gestionar documentos y evaluaciones',
        'icono': 'fas fa-folder-open',
        'color': 'purple',
        'ruta': None
    },
    'reportes_mis_pacientes': {
        'titulo': 'Reportes de Mis Pacientes',
        'descripcion': 'Reportes y estadísticas de mis pacientes',
        'icono': 'fas fa-chart-bar',
        'color': 'purple',
        'ruta': None
    },
    'disponibilidad_horaria': {
        'titulo': 'Disponibilidad Horaria',
        'descripcion': 'Gestionar mi disponibilidad horaria',
        'icono': 'fas fa-clock',
        'color': 'purple',
        'ruta': None
    },
    'derivaciones': {
        'titulo': 'Derivaciones',
        'descripcion': 'Gestionar derivaciones de pacientes',
        'icono': 'fas fa-exchange-alt',
        'color': 'purple',
        'ruta': None  # url_for('derivacion.derivacionIndex')
    },
    
    # RECEPCIONISTA
    'agenda_general': {
        'titulo': 'Agenda General',
        'descripcion': 'Vista de todos los especialistas',
        'icono': 'fas fa-calendar',
        'color': 'blue',
        'ruta': None  # url_for('cita.citaIndex')
    },
    'crear_modificar_citas': {
        'titulo': 'Crear/Modificar Citas',
        'descripcion': 'Crear y modificar citas',
        'icono': 'fas fa-calendar-plus',
        'color': 'blue',
        'ruta': None  # url_for('cita.citaIndex')
    },
    'gestion_pacientes': {
        'titulo': 'Gestión de Pacientes',
        'descripcion': 'Registro y datos básicos de pacientes',
        'icono': 'fas fa-users',
        'color': 'blue',
        'ruta': None
    },
    'checkin_checkout': {
        'titulo': 'Check-in/Check-out',
        'descripcion': 'Registrar entrada y salida de pacientes',
        'icono': 'fas fa-sign-in-alt',
        'color': 'green',
        'ruta': None
    },
    'confirmar_citas': {
        'titulo': 'Confirmar Citas',
        'descripcion': 'Confirmar citas programadas',
        'icono': 'fas fa-check-circle',
        'color': 'green',
        'ruta': None
    },
    'lista_espera': {
        'titulo': 'Lista de Espera',
        'descripcion': 'Gestionar lista de espera',
        'icono': 'fas fa-list-ol',
        'color': 'orange',
        'ruta': None
    },
    'llamadas_recordatorios': {
        'titulo': 'Llamadas y Recordatorios',
        'descripcion': 'Gestionar llamadas y recordatorios',
        'icono': 'fas fa-phone',
        'color': 'blue',
        'ruta': None
    },
    'consulta_disponibilidad': {
        'titulo': 'Consulta de Disponibilidad',
        'descripcion': 'Consultar disponibilidad de especialistas',
        'icono': 'fas fa-search',
        'color': 'blue',
        'ruta': None
    },
    
    # VENTAS
    'registro_nuevos_pacientes': {
        'titulo': 'Registro de Nuevos Pacientes',
        'descripcion': 'Registrar nuevos pacientes (leads)',
        'icono': 'fas fa-user-plus',
        'color': 'green',
        'ruta': None
    },
    'seguimiento_prospectos': {
        'titulo': 'Seguimiento de Prospectos',
        'descripcion': 'Seguimiento de clientes potenciales',
        'icono': 'fas fa-user-clock',
        'color': 'green',
        'ruta': None
    },
    'cotizaciones_paquetes': {
        'titulo': 'Cotizaciones y Paquetes',
        'descripcion': 'Crear cotizaciones y paquetes',
        'icono': 'fas fa-file-invoice',
        'color': 'green',
        'ruta': None
    },
    'conversiones': {
        'titulo': 'Conversiones',
        'descripcion': 'Gestionar conversiones de prospectos',
        'icono': 'fas fa-exchange-alt',
        'color': 'green',
        'ruta': None
    },
    'gestion_pagos_cobros': {
        'titulo': 'Gestión de Pagos y Cobros',
        'descripcion': 'Gestionar pagos y cobros',
        'icono': 'fas fa-money-bill-wave',
        'color': 'green',
        'ruta': None
    },
    'facturacion': {
        'titulo': 'Facturación',
        'descripcion': 'Gestionar facturación',
        'icono': 'fas fa-file-invoice-dollar',
        'color': 'green',
        'ruta': None  # url_for('factura.facturaIndex')
    },
    'reportes_ventas': {
        'titulo': 'Reportes de Ventas',
        'descripcion': 'Reportes y análisis de ventas',
        'icono': 'fas fa-chart-line',
        'color': 'green',
        'ruta': None
    },
    'comisiones': {
        'titulo': 'Comisiones',
        'descripcion': 'Gestionar comisiones (si aplica)',
        'icono': 'fas fa-percent',
        'color': 'green',
        'ruta': None
    },
}

# Mapeo de colores Tailwind
COLORES_TAILWIND = {
    'purple': {
        'bg': 'bg-purple-500',
        'hover': 'hover:bg-purple-600',
        'text': 'text-purple-600',
        'border': 'border-purple-500',
        'gradient_from': 'from-purple-500',
        'gradient_to': 'to-purple-600',
    },
    'blue': {
        'bg': 'bg-blue-500',
        'hover': 'hover:bg-blue-600',
        'text': 'text-blue-600',
        'border': 'border-blue-500',
        'gradient_from': 'from-blue-500',
        'gradient_to': 'to-blue-600',
    },
    'green': {
        'bg': 'bg-green-500',
        'hover': 'hover:bg-green-600',
        'text': 'text-green-600',
        'border': 'border-green-500',
        'gradient_from': 'from-green-500',
        'gradient_to': 'to-green-600',
    },
    'orange': {
        'bg': 'bg-orange-500',
        'hover': 'hover:bg-orange-600',
        'text': 'text-orange-600',
        'border': 'border-orange-500',
        'gradient_from': 'from-orange-500',
        'gradient_to': 'to-orange-600',
    },
    'indigo': {
        'bg': 'bg-indigo-500',
        'hover': 'hover:bg-indigo-600',
        'text': 'text-indigo-600',
        'border': 'border-indigo-500',
        'gradient_from': 'from-indigo-500',
        'gradient_to': 'to-indigo-600',
    },
    'gray': {
        'bg': 'bg-gray-500',
        'hover': 'hover:bg-gray-600',
        'text': 'text-gray-600',
        'border': 'border-gray-500',
        'gradient_from': 'from-gray-500',
        'gradient_to': 'to-gray-600',
    },
}


def obtener_detalle_modulo(nombre_modulo: str) -> Optional[Dict]:
    """
    Obtiene los detalles de un módulo específico
    
    Args:
        nombre_modulo: Nombre del módulo
        
    Returns:
        Dict con detalles del módulo o None si no existe
    """
    return MODULOS_DETALLES.get(nombre_modulo)


def obtener_color_tailwind(color: str) -> Dict:
    """
    Obtiene las clases Tailwind para un color
    
    Args:
        color: Nombre del color
        
    Returns:
        Dict con clases Tailwind
    """
    return COLORES_TAILWIND.get(color, COLORES_TAILWIND['blue'])


def obtener_modulos_con_detalles(modulos: List[str]) -> List[Dict]:
    """
    Obtiene los módulos con sus detalles completos
    
    Args:
        modulos: Lista de nombres de módulos
        
    Returns:
        Lista de diccionarios con detalles de cada módulo
    """
    resultado = []
    for modulo in modulos:
        if modulo == 'dashboard':
            continue  # Saltar dashboard ya que es la página principal
        
        detalle = obtener_detalle_modulo(modulo)
        if detalle:
            detalle['nombre_modulo'] = modulo
            resultado.append(detalle)
        else:
            # Si no hay detalle, crear uno básico
            resultado.append({
                'nombre_modulo': modulo,
                'titulo': modulo.replace('_', ' ').title(),
                'descripcion': f'Módulo {modulo}',
                'icono': 'fas fa-th',
                'color': 'blue',
                'ruta': None
            })
    
    return resultado

