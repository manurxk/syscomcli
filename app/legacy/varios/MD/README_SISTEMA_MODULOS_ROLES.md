# Sistema de Permisos por Módulos - Implementación

## Resumen

Se ha implementado un sistema modular de permisos que permite definir qué módulos y widgets puede acceder cada rol del sistema. El sistema está diseñado para soportar usuarios con múltiples roles combinados (ej: Administrador + Especialista).

## Estructura de Roles

Los roles definidos en el sistema son:

1. **SUPERADMINISTRADOR** - Acceso total al sistema
2. **ADMINISTRADOR** - Gestión completa de la clínica
3. **ESPECIALISTA** - Gestión de pacientes y consultas (incluye derivaciones)
4. **RECEPCIONISTA** - Gestión de citas y pacientes
5. **VENTAS** - Gestión comercial y facturación

## Componentes Implementados

### 1. Servicio de Módulos (`app/services/modulos_service.py`)

Este servicio centraliza la definición de módulos y widgets por rol.

**Características principales:**
- Define módulos accesibles por cada rol
- Define widgets del dashboard por cada rol
- Soporta múltiples roles por usuario (combina módulos)
- Métodos para verificar acceso a módulos
- Métodos para obtener widgets disponibles

**Uso básico:**
```python
from app.services.modulos_service import ModulosService

modulos_service = ModulosService()

# Verificar si tiene acceso a un módulo
if modulos_service.tiene_acceso_modulo('dashboard'):
    # Mostrar módulo
    
# Obtener todos los módulos del usuario
modulos = modulos_service.obtener_modulos_usuario()

# Obtener widgets del dashboard
widgets = modulos_service.obtener_widgets_usuario()

# Verificar rol
if modulos_service.es_admin():
    # Lógica para admin
```

### 2. Template Helpers (`app/utils/template_helpers.py`)

Funciones helper actualizadas para usar el servicio de módulos:

- `es_admin()` - Verifica si es Administrador
- `es_superadmin()` - Verifica si es Superadministrador
- `es_especialista()` - Verifica si es Especialista
- `es_recepcion()` - Verifica si es Recepcionista
- `es_ventas()` - Verifica si es Ventas
- `puede_acceder_modulo(nombre_modulo)` - Verifica acceso a módulo
- `obtener_modulos_usuario()` - Obtiene módulos accesibles
- `obtener_widgets_usuario()` - Obtiene widgets del dashboard

**Uso en templates:**
```jinja2
{% if es_admin() %}
    <a href="/admin">Panel Admin</a>
{% endif %}

{% if puede_acceder_modulo('dashboard') %}
    <a href="/dashboard">Dashboard</a>
{% endif %}

{% for widget in obtener_widgets_usuario() %}
    <div class="widget-{{ widget }}">...</div>
{% endfor %}
```

### 3. Dashboard (`app/rutas/seguridad/dashboard.py`)

El dashboard ha sido actualizado para:
- Usar el servicio de módulos para verificar roles
- Pasar módulos y widgets al template
- Soportar múltiples roles combinados

**Datos disponibles en el template:**
```python
data_usuario = {
    "esAdmin": True/False,
    "esRecepcion": True/False,
    "esEspecialista": True/False,
    "esVentas": True/False,
    "esSuperadmin": True/False,
    "modulos": ["dashboard", "mi_agenda_personal", ...],
    "widgets": ["mis_proximas_citas", "pacientes_asignados", ...],
    "roles": ["ADMINISTRADOR", "ESPECIALISTA"],
    "nombre": "Nombre del usuario"
}
```

## Módulos Definidos por Rol

### SUPERADMINISTRADOR
- Gestión de clínicas/sedes
- Configuración global del sistema
- Gestión de administradores
- Reportes consolidados
- Configuración de precios y planes
- Logs y auditoría
- Respaldos y mantenimiento

### ADMINISTRADOR
- Dashboard ejecutivo
- Gestión de usuarios de la clínica
- Asignación de roles y permisos
- Reportes financieros
- Configuración de la clínica
- Gestión de especialistas y agenda
- Reportes de desempeño
- Inventario y recursos
- Configuración de precios locales

### ESPECIALISTA
- Mi agenda personal
- Mis pacientes asignados
- Historias clínicas
- Sesiones programadas
- Notas de evolución
- Planes de tratamiento
- Documentos y evaluaciones
- Reportes de mis pacientes
- Disponibilidad horaria
- **Derivaciones** (tabla de derivaciones)

### RECEPCIONISTA
- Agenda general
- Crear/modificar citas
- Gestión de pacientes
- Check-in/Check-out
- Confirmar citas
- Lista de espera
- Llamadas y recordatorios
- Consulta de disponibilidad

### VENTAS
- Registro de nuevos pacientes
- Seguimiento de prospectos
- Cotizaciones y paquetes
- Conversiones
- Gestión de pagos y cobros
- Facturación
- Reportes de ventas
- Comisiones

## Widgets del Dashboard por Rol

### SUPERADMINISTRADOR
- Métricas globales
- Usuarios del sistema
- Clínicas/sedes
- Reportes consolidados

### ADMINISTRADOR
- Métricas generales
- Usuarios activos
- Citas hoy
- Pacientes activos
- Ingresos del mes

### ESPECIALISTA
- Mis próximas citas
- Pacientes asignados
- Derivaciones pendientes
- Historias pendientes

### RECEPCIONISTA
- Citas del día
- Citas pendientes
- Pacientes hoy
- Lista de espera

### VENTAS
- Pipeline de ventas
- Facturas del mes
- Ventas hoy
- Cuentas por cobrar

## Soporte para Múltiples Roles

El sistema está diseñado para soportar usuarios con múltiples roles. Cuando un usuario tiene varios roles:

1. **Módulos combinados**: Se combinan todos los módulos de todos sus roles (UNION)
2. **Widgets combinados**: Se combinan todos los widgets de todos sus roles
3. **Verificación de roles**: Los métodos `es_admin()`, `es_especialista()`, etc. retornan `True` si el usuario tiene AL MENOS UNO de esos roles

**Ejemplo:**
- Usuario con roles: Administrador + Especialista
- Módulos accesibles: Todos los módulos de Administrador + Todos los módulos de Especialista
- Widgets: Todos los widgets de Administrador + Todos los widgets de Especialista
- `es_admin()` retorna `True`
- `es_especialista()` retorna `True`

## Próximos Pasos (Extensión Futura)

Para implementar completamente el sistema de múltiples roles, se necesitaría:

1. **Base de Datos**: Crear tabla `usuarios_roles` para almacenar múltiples roles por usuario
2. **Modificar `obtener_roles_usuario()`**: Consultar la tabla `usuarios_roles` en lugar de solo `id_grupo`
3. **Interfaz de Usuario**: Permitir asignar múltiples roles al crear/editar usuarios
4. **Validaciones**: Limitar número máximo de roles (ej: máximo 3)

El código actual está preparado para esta extensión: la estructura ya soporta múltiples roles, solo falta implementar la persistencia en BD.

## Notas Importantes

1. **Derivaciones para Especialistas**: El sistema incluye el módulo 'derivaciones' para especialistas, que permite gestionar la tabla de derivaciones entre especialistas.

2. **Compatibilidad**: El sistema mantiene compatibilidad con el código existente que usa `id_grupo` directamente, pero se recomienda usar los métodos del servicio de módulos.

3. **Fallback**: Todas las funciones tienen fallback a verificación básica por `id_grupo` en caso de error con el servicio de módulos.

4. **Performance**: El servicio de módulos es eficiente ya que las definiciones están en memoria. Para usuarios con múltiples roles, solo se combinan los conjuntos de módulos.

## Archivos Modificados/Creados

1. ✅ `app/services/modulos_service.py` - NUEVO: Servicio de módulos
2. ✅ `app/utils/template_helpers.py` - ACTUALIZADO: Helpers para templates
3. ✅ `app/rutas/seguridad/dashboard.py` - ACTUALIZADO: Dashboard con soporte de módulos
4. ✅ `README_SISTEMA_MODULOS_ROLES.md` - NUEVO: Este documento

## Ejemplo de Uso Completo

```python
# En una ruta
from app.services.modulos_service import ModulosService

@dashboard.route('/mi-ruta')
def mi_ruta():
    modulos_service = ModulosService()
    
    # Verificar acceso
    if not modulos_service.tiene_acceso_modulo('dashboard'):
        return redirect(url_for('login.login'))
    
    # Obtener módulos y widgets
    modulos = modulos_service.obtener_modulos_usuario()
    widgets = modulos_service.obtener_widgets_usuario()
    
    return render_template('mi_template.html', 
                         modulos=modulos, 
                         widgets=widgets)
```

```jinja2
{# En un template #}
{% if puede_acceder_modulo('mi_agenda_personal') %}
    <a href="/agenda">Mi Agenda</a>
{% endif %}

{% if es_especialista() %}
    <a href="/derivaciones">Derivaciones</a>
{% endif %}

{% for widget in obtener_widgets_usuario() %}
    {% include 'widgets/' + widget + '.html' %}
{% endfor %}
```

---

**Fecha de Implementación**: 2024
**Versión**: 1.0
**Estado**: ✅ Implementado y listo para uso

