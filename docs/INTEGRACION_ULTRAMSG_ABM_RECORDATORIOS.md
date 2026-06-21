# Integración UltraMsg en ABM de Recordatorios

**Fecha:** 2026-01-22  
**Sistema:** Sysclin - Sistema de Gestión Médica  
**Objetivo:** Documentar la integración completa de UltraMsg en el módulo de gestión de recordatorios

---

## 📋 Resumen

Se ha completado la integración de UltraMsg en el ABM (Alta, Baja, Modificación) de recordatorios, reemplazando completamente las referencias a Twilio y mejorando la visualización y gestión de los mensajes enviados.

---

## ✅ Cambios Implementados

### 1. Actualización del DAO (`RecordatorioDao.py`)

#### 1.1 Método `getRecordatoriosPorCita`
- **Antes:** Solo incluía `recordatorio_twilio_sid` si existía la columna
- **Ahora:** 
  - Verifica dinámicamente si existe `recordatorio_ultramsg_id`
  - Si existe, la incluye en la consulta
  - Retorna `ultramsg_id` y `message_id` (alias) en el resultado
  - Mantiene compatibilidad con `twilio_sid` si existe

**Código actualizado:**
```python
# Verifica qué columnas existen para tracking
tiene_ultramsg_id = self._columna_existe('recordatorio_ultramsg_id')
tiene_twilio_sid = self._columna_existe('recordatorio_twilio_sid')

# Construye SELECT dinámicamente
if tiene_ultramsg_id:
    columnas_select.append('recordatorio_ultramsg_id')
elif tiene_twilio_sid:
    columnas_select.append('recordatorio_twilio_sid')
```

#### 1.2 Método `marcarEnviado`
- Ya estaba actualizado para usar `message_id` genérico
- Guarda en `recordatorio_ultramsg_id` si existe la columna
- Mantiene compatibilidad con `recordatorio_twilio_sid` como fallback

---

### 2. Actualización de la API (`recordatorio_api.py`)

#### 2.1 Endpoint `GET /api/v1/recordatorios`
- **Antes:** Retornaba `twilio_sid: None` hardcodeado
- **Ahora:**
  - Verifica dinámicamente si existe `recordatorio_ultramsg_id`
  - Incluye la columna en la consulta SQL
  - Retorna `ultramsg_id` y `message_id` en la respuesta JSON
  - Los valores pueden ser `None` si la columna no existe o está vacía

**Cambios en SQL:**
```sql
-- Antes
NULL as recordatorio_twilio_sid

-- Ahora (dinámico)
{r.recordatorio_ultramsg_id} as recordatorio_message_id
-- o NULL si la columna no existe
```

**Cambios en respuesta JSON:**
```json
{
  "ultramsg_id": "msg_123456",
  "message_id": "msg_123456",  // Alias para compatibilidad
  // ... otros campos
}
```

#### 2.2 Endpoint `GET /api/v1/recordatorios/<id>`
- Actualizado de la misma manera que el endpoint de listado
- Incluye `ultramsg_id` y `message_id` en los detalles del recordatorio

---

### 3. Actualización de la Vista HTML (`recordatorio-index.html`)

#### 3.1 Modal de Detalles
- **Antes:** No mostraba información del servicio de mensajería
- **Ahora:** Muestra el UltraMsg ID cuando está disponible

**Código agregado:**
```javascript
${r.ultramsg_id || r.message_id ? `
<tr><td><strong>UltraMsg ID:</strong></td><td><code>${r.ultramsg_id || r.message_id || 'N/A'}</code></td></tr>
` : ''}
```

#### 3.2 Visualización
- El UltraMsg ID se muestra en una fila adicional en la tabla de información del recordatorio
- Se muestra solo si existe un valor (no se muestra si es `null` o `undefined`)
- Formato: `<code>` para mejor legibilidad

---

### 4. Funcionalidad de Reenvío

#### 4.1 Endpoint `POST /api/v1/recordatorios/<id>/reenviar`
- **Estado:** ✅ Ya estaba funcionando correctamente
- Usa `UltraMsgService.enviar_recordatorio_cita()`
- Guarda el `message_id` retornado usando `marcarEnviado()`
- Maneja errores y actualiza el estado del recordatorio

---

## 🔄 Flujo de Datos

### Creación/Actualización de Recordatorio
1. Se crea o actualiza un recordatorio en la base de datos
2. El sistema procesa el recordatorio (manual o automático)
3. `UltraMsgService` envía el mensaje y retorna un `message_id`
4. `RecordatorioDao.marcarEnviado()` guarda el `message_id` en `recordatorio_ultramsg_id`
5. El recordatorio queda marcado como "enviado" con su ID de mensaje

### Visualización en el ABM
1. El usuario accede a la lista de recordatorios
2. La API consulta incluyendo `recordatorio_ultramsg_id` (si existe)
3. El frontend muestra el UltraMsg ID en el modal de detalles
4. El usuario puede ver el estado del mensaje y reenviarlo si es necesario

---

## 📊 Estructura de Datos

### Tabla `recordatorios`
```sql
-- Columna opcional (se crea con el script SQL)
recordatorio_ultramsg_id VARCHAR(100)  -- ID del mensaje de UltraMsg
```

### Respuesta JSON de la API
```json
{
  "id_recordatorio": 123,
  "id_cita": 456,
  "tipo": "24h",
  "estado": "enviado",
  "ultramsg_id": "msg_abc123",
  "message_id": "msg_abc123",  // Alias
  "fecha_enviado": "2026-01-22 10:30:00",
  // ... otros campos
}
```

---

## 🛠️ Scripts SQL

### Crear Columna de Tracking (Opcional)
El script `app/varios/SQL/add_ultramsg_column.sql` crea la columna `recordatorio_ultramsg_id` si no existe.

**Ejecutar:**
```bash
psql -U usuario -d nombre_bd -f app/varios/SQL/add_ultramsg_column.sql
```

---

## ✅ Verificación

### Checklist de Integración
- [x] `RecordatorioDao.getRecordatoriosPorCita()` incluye `ultramsg_id`
- [x] `RecordatorioDao.marcarEnviado()` guarda `message_id` en `recordatorio_ultramsg_id`
- [x] API retorna `ultramsg_id` y `message_id` en respuestas JSON
- [x] Vista HTML muestra UltraMsg ID en modal de detalles
- [x] Funcionalidad de reenvío funciona correctamente
- [x] Compatibilidad mantenida con columnas antiguas (si existen)

### Pruebas Recomendadas
1. **Crear un recordatorio** y verificar que se guarda el `message_id`
2. **Listar recordatorios** y verificar que aparece `ultramsg_id` en la respuesta
3. **Ver detalles** de un recordatorio enviado y verificar que se muestra el UltraMsg ID
4. **Reenviar un recordatorio** y verificar que se actualiza el `message_id`

---

## 🔮 Próximos Pasos

### Fase 3: Webhooks (Próxima)
- Implementar endpoint para recibir webhooks de UltraMsg
- Actualizar estado de mensajes basado en webhooks
- Manejar estados: enviado, entregado, leído, fallido
- Mejorar tracking de mensajes en tiempo real

### Mejoras Futuras
- Agregar columna en la tabla principal para mostrar UltraMsg ID
- Implementar verificación de estado de mensajes
- Agregar filtros por estado de mensaje (enviado, entregado, leído)
- Dashboard de métricas de envío

---

## 📝 Notas Técnicas

### Compatibilidad
- El sistema mantiene compatibilidad con `recordatorio_twilio_sid` si existe
- Si no existe `recordatorio_ultramsg_id`, el sistema funciona normalmente pero no guarda el ID
- Los valores `None` se manejan correctamente en el frontend

### Rendimiento
- Las verificaciones de columnas se hacen una vez por consulta
- No hay impacto significativo en el rendimiento
- Las consultas SQL son eficientes con índices apropiados

### Seguridad
- Los IDs de mensajes no contienen información sensible
- Se validan los permisos antes de mostrar información
- Los endpoints están protegidos con `@role_required`

---

## 📚 Referencias

- [Documentación UltraMsg API](https://docs.ultramsg.com/)
- [Plan de Implementación por Fases](./PLAN_IMPLEMENTACION_ULTRAMSG_FASES.md)
- [Guía de Configuración](./GUIA_CONFIGURACION_ULTRAMSG_PASO_A_PASO.md)
- [Análisis de Requisitos](./ANALISIS_REQUISITOS_ULTRAMSG.md)

---

**Última actualización:** 2026-01-22  
**Estado:** ✅ Completado

