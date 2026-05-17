# Vistas Faltantes para Gestión de Recordatorios

## 📋 Análisis de Vistas Necesarias

### ✅ Estado Actual
- ✅ Backend implementado (DAO, Tasks, API)
- ❌ **Faltan vistas HTML para gestión**
- ❌ **Faltan endpoints API para consultas**
- ❌ **Faltan rutas Flask para las vistas**

---

## 🎯 Vistas a Crear

### 1. **Vista Principal: Listado de Recordatorios** ⭐ PRIORITARIO

**Ruta:** `/recordatorio/recordatorio-index`

**Funcionalidad:**
- Ver todos los recordatorios del sistema
- Filtrar por estado (pendiente, enviado, fallido, cancelado)
- Filtrar por fecha
- Ver detalles de cada recordatorio
- Reenviar recordatorios fallidos manualmente

**Campos a mostrar:**
- ID Recordatorio
- Cita (fecha, hora, paciente)
- Tipo (24h, 12h)
- Fecha Programada
- Fecha Enviado
- Estado
- Intentos
- Teléfono
- Acciones (ver detalles, reenviar)

**Archivos a crear:**
- `app/rutas/modulos/recordatorio/recordatorio_routes.py`
- `app/rutas/modulos/recordatorio/recordatorio_api.py`
- `app/rutas/modulos/recordatorio/templates/recordatorio-index.html`

---

### 2. **Vista: Recordatorios por Cita** ⭐ PRIORITARIO

**Ruta:** `/cita/<id>/recordatorios` (modal o sección en detalle de cita)

**Funcionalidad:**
- Ver todos los recordatorios de una cita específica
- Ver estado de cada recordatorio
- Reenviar recordatorios manualmente
- Ver mensaje enviado

**Campos a mostrar:**
- Tipo de recordatorio
- Fecha programada
- Fecha enviado
- Estado
- Intentos
- Mensaje enviado
- Twilio SID
- Error (si falló)

**Archivos a modificar:**
- Agregar sección en `cita-index.html` o crear modal
- Agregar endpoint en `cita_api.py`

---

### 3. **Vista: Estadísticas de Recordatorios** (Opcional)

**Ruta:** `/recordatorio/estadisticas`

**Funcionalidad:**
- Ver estadísticas generales:
  - Total enviados hoy/semana/mes
  - Tasa de éxito
  - Recordatorios pendientes
  - Recordatorios fallidos
  - Gráficos de rendimiento

**Archivos a crear:**
- `app/rutas/modulos/recordatorio/templates/recordatorio-estadisticas.html`
- Endpoint en `recordatorio_api.py`

---

### 4. **Integración en Vista de Citas** ⭐ IMPORTANTE

**Modificar:** `app/rutas/modulos/cita/templates/cita-index.html`

**Agregar:**
- Columna "Recordatorios" en la tabla de citas
- Badge mostrando estado (✅ Enviados, ⏳ Pendientes, ❌ Fallidos)
- Botón para ver detalles de recordatorios
- Modal para ver/reenviar recordatorios

---

## 📁 Estructura de Archivos a Crear

```
app/rutas/modulos/recordatorio/
├── __init__.py
├── recordatorio_routes.py          # Rutas Flask para vistas
├── recordatorio_api.py              # Endpoints API
└── templates/
    └── recordatorio-index.html      # Vista principal
```

---

## 🔌 Endpoints API Necesarios

### 1. GET `/api/v1/recordatorios`
Obtener listado de recordatorios con filtros

**Query params:**
- `estado`: pendiente, enviado, fallido, cancelado
- `fecha_desde`: fecha inicio
- `fecha_hasta`: fecha fin
- `id_cita`: filtrar por cita específica
- `page`: número de página
- `per_page`: registros por página

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id_recordatorio": 1,
      "id_cita": 123,
      "tipo": "24h",
      "fecha_programada": "2025-01-15 10:00:00",
      "fecha_enviado": "2025-01-15 10:01:23",
      "estado": "enviado",
      "intentos": 1,
      "telefono": "+595981123456",
      "paciente_nombre": "Juan Pérez",
      "cita_fecha": "2025-01-16",
      "cita_hora": "10:00",
      "especialista": "Dr. Carlos González",
      "twilio_sid": "SMxxxxx"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 50
}
```

### 2. GET `/api/v1/recordatorios/<id_recordatorio>`
Obtener detalles de un recordatorio específico

### 3. GET `/api/v1/citas/<id_cita>/recordatorios`
Obtener todos los recordatorios de una cita

### 4. POST `/api/v1/recordatorios/<id_recordatorio>/reenviar`
Reenviar un recordatorio manualmente

### 5. GET `/api/v1/recordatorios/estadisticas`
Obtener estadísticas de recordatorios

---

## 🎨 Diseño de Vistas

### Vista Principal (recordatorio-index.html)

**Estructura:**
- Header con título y botones de filtro
- Tabla con DataTables (similar a otras vistas del sistema)
- Filtros:
  - Estado (dropdown)
  - Rango de fechas
  - Búsqueda por paciente/cita
- Acciones por fila:
  - Ver detalles
  - Reenviar (si falló)
  - Ver mensaje enviado

### Modal de Detalles

**Mostrar:**
- Información completa del recordatorio
- Información de la cita asociada
- Historial de intentos
- Mensaje enviado completo
- Estado en Twilio (si está disponible)

---

## 📝 Prioridades de Implementación

### Fase 1: Básico (Esencial) ⭐
1. ✅ Crear estructura de archivos
2. ✅ Crear endpoint API: GET `/api/v1/recordatorios`
3. ✅ Crear endpoint API: GET `/api/v1/citas/<id>/recordatorios`
4. ✅ Crear vista principal: `recordatorio-index.html`
5. ✅ Agregar ruta: `/recordatorio/recordatorio-index`

### Fase 2: Funcionalidades Adicionales
6. ✅ Endpoint: POST `/api/v1/recordatorios/<id>/reenviar`
7. ✅ Integrar en vista de citas (columna recordatorios)
8. ✅ Modal de detalles de recordatorios

### Fase 3: Estadísticas (Opcional)
9. ✅ Vista de estadísticas
10. ✅ Endpoint de estadísticas
11. ✅ Gráficos de rendimiento

---

## 🔗 Integración con Vista de Citas

### Modificaciones en `cita-index.html`

**Agregar columna en tabla:**
```html
<th>Recordatorios</th>
```

**Mostrar badge:**
```html
<td>
  <span class="badge badge-success" title="2 enviados">✅ 2</span>
  <span class="badge badge-warning" title="1 pendiente">⏳ 1</span>
  <button class="btn btn-sm btn-info" onclick="verRecordatorios({{cita.id_cita}})">
    Ver
  </button>
</td>
```

**Agregar modal:**
```html
<!-- Modal Recordatorios -->
<div class="modal fade" id="modalRecordatorios">
  <!-- Contenido del modal -->
</div>
```

---

## 📊 Ejemplo de Datos a Mostrar

### Tabla Principal

| ID | Cita | Paciente | Tipo | Fecha Programada | Estado | Intentos | Acciones |
|----|------|----------|------|------------------|--------|----------|----------|
| 1 | 16/01 10:00 | Juan Pérez | 24h | 15/01 10:00 | ✅ Enviado | 1 | Ver |
| 2 | 16/01 10:00 | Juan Pérez | 12h | 15/01 22:00 | ⏳ Pendiente | 0 | Ver |
| 3 | 17/01 14:00 | María García | 24h | 16/01 14:00 | ❌ Fallido | 3 | Reenviar |

---

## 🚀 Siguiente Paso

**Implementar Fase 1:**
1. Crear archivos de rutas y API
2. Crear vista HTML básica
3. Probar con datos reales

¿Procedo a crear estos archivos?

