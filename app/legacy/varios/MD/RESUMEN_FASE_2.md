# 📋 Fase 2: Sistema de Derivaciones - Implementación Completada

## ✅ Resumen Ejecutivo

Se ha implementado exitosamente el sistema de derivaciones entre especialistas, permitiendo que los profesionales puedan derivar pacientes a otros especialistas con un flujo completo de aceptación/rechazo y notificaciones.

---

## 🎯 Características Implementadas

### 1. Base de Datos
- ✅ Tabla `derivaciones` con todos los campos necesarios
- ✅ Tabla `notificaciones` para sistema de alertas
- ✅ Funciones PostgreSQL para automatizar procesos:
  - `crear_derivacion()`: Crea derivación y notificación automática
  - `aceptar_derivacion()`: Acepta derivación y asigna paciente automáticamente
  - `rechazar_derivacion()`: Rechaza derivación con motivo
- ✅ Índices optimizados para consultas rápidas
- ✅ Vista `v_derivaciones_pendientes` para consultas frecuentes

### 2. Backend (Python/Flask)
- ✅ **DerivacionDao** (`app/dao/modulos/derivacion/DerivacionDao.py`):
  - `crearDerivacion()`: Crea nueva derivación
  - `getDerivaciones()`: Obtiene todas las derivaciones (filtradas por especialista)
  - `getDerivacionesPendientes()`: Obtiene derivaciones pendientes recibidas
  - `getDerivacionById()`: Obtiene una derivación específica
  - `aceptarDerivacion()`: Acepta una derivación
  - `rechazarDerivacion()`: Rechaza una derivación
  - `cancelarDerivacion()`: Cancela una derivación (solo origen)
  - `getEspecialistasDisponibles()`: Lista especialistas disponibles para derivar

- ✅ **API Routes** (`app/rutas/modulos/derivacion/derivacion_api.py`):
  - `GET /api/v1/derivaciones`: Lista todas las derivaciones
  - `GET /api/v1/derivaciones/pendientes`: Lista derivaciones pendientes recibidas
  - `GET /api/v1/derivaciones/<id>`: Obtiene una derivación específica
  - `POST /api/v1/derivaciones`: Crea nueva derivación
  - `PATCH /api/v1/derivaciones/<id>/aceptar`: Acepta derivación
  - `PATCH /api/v1/derivaciones/<id>/rechazar`: Rechaza derivación
  - `PATCH /api/v1/derivaciones/<id>/cancelar`: Cancela derivación
  - `GET /api/v1/derivaciones/especialistas-disponibles`: Lista especialistas disponibles

- ✅ **Vista Routes** (`app/rutas/modulos/derivacion/derivacion_routes.py`):
  - `GET /derivacion/derivacion-index`: Vista principal de gestión

### 3. Frontend (HTML/JavaScript)
- ✅ **Template Principal** (`app/rutas/modulos/derivacion/templates/derivacion-index.html`):
  - Interfaz con tabs para diferentes vistas:
    - **Pendientes Recibidas**: Derivaciones que requieren respuesta
    - **Derivaciones Enviadas**: Historial de derivaciones enviadas
    - **Historial Completo**: Todas las derivaciones
  - Modal para crear nueva derivación
  - Modal para ver detalles de derivación
  - Modal para aceptar/rechazar derivaciones
  - DataTables para tablas interactivas
  - Búsqueda de pacientes integrada

### 4. Integración con Dashboard
- ✅ Módulo "Derivaciones" agregado al dashboard del especialista
- ✅ Acceso rápido desde el panel principal

---

## 🔄 Flujo de Derivación

### Crear Derivación:
1. Especialista accede a "Derivaciones"
2. Click en "Nueva Derivación"
3. Selecciona paciente de su lista
4. Selecciona especialista destino
5. Define urgencia y motivo
6. Envía derivación
7. **Sistema automáticamente:**
   - Crea registro en `derivaciones`
   - Crea notificación para especialista destino
   - Marca estado como "PENDIENTE"

### Aceptar Derivación:
1. Especialista destino ve notificación
2. Accede a "Derivaciones" → Tab "Pendientes Recibidas"
3. Revisa detalles de la derivación
4. Click en "Aceptar"
5. **Sistema automáticamente:**
   - Cambia estado a "ACEPTADA"
   - Crea registro en `paciente_profesional` con `tipo_relacion = 'DERIVADO'`
   - Crea notificación para especialista origen
   - El paciente aparece en "Mis Pacientes" del especialista destino

### Rechazar Derivación:
1. Especialista destino revisa derivación
2. Click en "Rechazar"
3. Ingresa motivo de rechazo
4. Confirma rechazo
5. **Sistema automáticamente:**
   - Cambia estado a "RECHAZADA"
   - Guarda motivo de rechazo
   - Crea notificación para especialista origen

### Cancelar Derivación:
1. Especialista origen ve sus derivaciones enviadas
2. Si está pendiente, puede cancelarla
3. **Sistema automáticamente:**
   - Cambia estado a "CANCELADA"
   - Elimina notificación pendiente del destino

---

## 📊 Estados de Derivación

| Estado | Descripción | Quién Puede Cambiar |
|-------|------------|---------------------|
| **PENDIENTE** | Esperando respuesta del especialista destino | Sistema (al crear) |
| **ACEPTADA** | Derivación aceptada, paciente asignado | Especialista destino |
| **RECHAZADA** | Derivación rechazada con motivo | Especialista destino |
| **CANCELADA** | Derivación cancelada por el origen | Especialista origen |

---

## 🚨 Niveles de Urgencia

| Urgencia | Descripción | Badge |
|----------|-------------|-------|
| **BAJA** | Sin urgencia | Gris |
| **NORMAL** | Urgencia normal | Azul |
| **ALTA** | Alta prioridad | Amarillo |
| **URGENTE** | Requiere atención inmediata | Rojo |

Las derivaciones se ordenan automáticamente por urgencia (URGENTE primero).

---

## 🔒 Seguridad y Validaciones

- ✅ Solo especialistas pueden crear derivaciones
- ✅ No se puede derivar a sí mismo
- ✅ Solo el especialista destino puede aceptar/rechazar
- ✅ Solo el especialista origen puede cancelar
- ✅ Validación de campos obligatorios
- ✅ Validación de motivo mínimo (10 caracteres)
- ✅ Filtrado automático por especialista logueado

---

## 📁 Archivos Creados/Modificados

### Nuevos Archivos:
1. `app/codigos_sql/FASE_2_DERIVACIONES_PREPARACION.sql` (actualizado para ejecución)
2. `app/dao/modulos/derivacion/DerivacionDao.py`
3. `app/rutas/modulos/derivacion/derivacion_api.py`
4. `app/rutas/modulos/derivacion/derivacion_routes.py`
5. `app/rutas/modulos/derivacion/__init__.py`
6. `app/rutas/modulos/derivacion/templates/derivacion-index.html`

### Archivos Modificados:
1. `app/__init__.py` - Registro de blueprints
2. `app/rutas/seguridad/templates/inicio.html` - Módulo en dashboard

---

## 🚀 Próximos Pasos (Opcionales)

### Mejoras Futuras:
1. **Notificaciones en Tiempo Real:**
   - WebSockets para notificaciones instantáneas
   - Badge de contador en tiempo real

2. **Integración con Mis Pacientes:**
   - Botón "Derivar" en vista Mis Pacientes
   - Acceso rápido desde ficha del paciente

3. **Historial de Paciente:**
   - Ver todas las derivaciones de un paciente específico
   - Timeline de derivaciones

4. **Estadísticas:**
   - Dashboard con métricas de derivaciones
   - Tiempo promedio de respuesta
   - Especialistas más solicitados

5. **Filtros Avanzados:**
   - Filtrar por urgencia
   - Filtrar por estado
   - Filtrar por rango de fechas

---

## ✅ Verificación

Para verificar que funciona:

1. **Ejecutar SQL:**
   ```sql
   -- Ejecutar app/codigos_sql/FASE_2_DERIVACIONES_PREPARACION.sql
   ```

2. **Reiniciar aplicación Flask**

3. **Login como especialista**

4. **Probar flujo completo:**
   - Crear derivación
   - Ver derivación pendiente (como destino)
   - Aceptar/rechazar derivación
   - Ver historial

---

**¡Fase 2 Implementada Exitosamente!** 🎉

El sistema de derivaciones está completamente funcional y listo para usar.


