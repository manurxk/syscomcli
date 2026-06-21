# Análisis de Implementación: Recordatorios de Citas vía Twilio y WhatsApp Business API

## 📋 Resumen Ejecutivo

Este documento analiza el impacto, costos y plan de implementación para agregar recordatorios automáticos de citas médicas usando **Twilio** (fase de pruebas) y posterior migración a **WhatsApp Business API** (producción).

**Estado Actual:**
- ✅ Tabla `recordatorios` existe en BD (estructura completa)
- ✅ `TwilioService.py` existe con funcionalidad básica
- ✅ Sistema de tareas programadas (APScheduler) implementado
- ❌ No hay implementación de recordatorios automáticos
- ❌ No hay integración con creación/modificación de citas

---

## 1. Análisis del Código Actual

### 1.1 Sistema de Agenda y Citas

#### Estructura de Datos

**Tabla `citas`:**
```sql
- id_cita (PK)
- id_paciente, id_especialista, id_especialidad
- cita_fecha, cita_hora_inicio, cita_hora_fin
- cita_motivo, cita_observaciones
- id_estado_cita (AGENDADA, CONFIRMADA, CANCELADA, etc.)
- cita_activo (boolean)
```

**Tabla `recordatorios` (existente):**
```sql
- id_recordatorio (PK)
- id_cita (FK)
- recordatorio_tipo ('12h', '24h')
- recordatorio_fecha_programada (TIMESTAMP)
- recordatorio_fecha_enviado (TIMESTAMP, nullable)
- recordatorio_estado ('pendiente', 'enviado', 'fallido', 'cancelado')
- recordatorio_intentos (INTEGER)
- recordatorio_mensaje_enviado (TEXT)
- recordatorio_error (TEXT)
- recordatorio_twilio_sid (VARCHAR) -- Para tracking
- recordatorio_telefono (VARCHAR) -- Cache
- recordatorio_paciente_nombre (VARCHAR) -- Cache
```

#### Código Relevante

**`app/dao/modulos/cita/CitaDao.py`:**
- `guardarCita()`: Crea nuevas citas (línea 635-859)
- `updateCita()`: Actualiza citas existentes (línea 861-983)
- `cancelarCita()`: Cancela citas (línea 1069-1088)
- `getCitaById()`: Obtiene datos completos de cita (línea 453-527)

**`app/services/TwilioService.py`:**
- ✅ `enviar_recordatorio_cita()`: Método básico implementado
- ✅ `_formatear_telefono()`: Formatea números paraguayos (+595)
- ✅ `_construir_mensaje_recordatorio()`: Genera mensaje personalizado
- ✅ Fallback automático WhatsApp → SMS
- ⚠️ **Falta**: Manejo de errores robusto, reintentos, logging detallado

**`app/auth/tasks/auth_tasks.py`:**
- ✅ Sistema de tareas programadas con APScheduler
- ✅ Ejemplos de configuración de scheduler
- ⚠️ **Falta**: Tarea específica para recordatorios

### 1.2 Puntos de Integración Identificados

1. **Al crear cita** (`CitaDao.guardarCita()`):
   - Crear registros en `recordatorios` para 24h y 12h antes
   - Calcular `recordatorio_fecha_programada` basado en `cita_fecha` y `cita_hora_inicio`

2. **Al actualizar cita** (`CitaDao.updateCita()`):
   - Actualizar o cancelar recordatorios existentes
   - Recrear si la fecha/hora cambió

3. **Al cancelar cita** (`CitaDao.cancelarCita()`):
   - Cancelar todos los recordatorios pendientes

4. **Tarea programada** (nueva):
   - Ejecutar cada 5-10 minutos
   - Buscar recordatorios con `estado='pendiente'` y `fecha_programada <= NOW()`
   - Enviar vía TwilioService
   - Actualizar estado en BD

---

## 2. Impacto de la Implementación

### 2.1 Cambios en Backend

#### Archivos a Modificar/Crear

1. **`app/dao/modulos/cita/CitaDao.py`** (MODIFICAR)
   - Agregar método `crearRecordatoriosParaCita(id_cita)`
   - Agregar método `cancelarRecordatoriosCita(id_cita)`
   - Modificar `guardarCita()` para crear recordatorios
   - Modificar `updateCita()` para actualizar recordatorios
   - Modificar `cancelarCita()` para cancelar recordatorios

2. **`app/dao/modulos/recordatorio/RecordatorioDao.py`** (CREAR NUEVO)
   - `getRecordatoriosPendientes()`: Obtiene recordatorios listos para enviar
   - `marcarEnviado(id_recordatorio, twilio_sid)`
   - `marcarFallido(id_recordatorio, error)`
   - `incrementarIntentos(id_recordatorio)`

3. **`app/tasks/recordatorio_tasks.py`** (CREAR NUEVO)
   - `procesar_recordatorios_pendientes()`: Tarea principal del scheduler
   - Lógica de reintentos (máx 3 intentos)
   - Manejo de errores y logging

4. **`app/services/TwilioService.py`** (MEJORAR)
   - Mejorar manejo de errores
   - Agregar logging detallado
   - Agregar método para verificar estado de mensaje

5. **`run.py` o `app/__init__.py`** (MODIFICAR)
   - Configurar scheduler con tarea de recordatorios
   - Inicializar APScheduler al arrancar la app

#### Estimación de Líneas de Código

- **RecordatorioDao.py**: ~200 líneas
- **recordatorio_tasks.py**: ~150 líneas
- **Modificaciones CitaDao.py**: ~100 líneas
- **Mejoras TwilioService.py**: ~50 líneas
- **Configuración scheduler**: ~30 líneas

**Total: ~530 líneas de código nuevo/modificado**

### 2.2 Cambios en Base de Datos

✅ **No requiere cambios** - La tabla `recordatorios` ya existe con toda la estructura necesaria.

**Índices existentes:**
- `idx_recordatorios_pendientes`: Optimizado para queries del scheduler
- `idx_recordatorios_cita`: Para búsquedas por cita

### 2.3 Cambios en Frontend

**Impacto mínimo:**
- Opcional: Mostrar estado de recordatorios en detalle de cita
- Opcional: Permitir reenvío manual de recordatorios
- Opcional: Configuración de tipos de recordatorio (12h/24h)

**Estimación:** Si se implementa UI, ~100-200 líneas adicionales (opcional).

### 2.4 Dependencias

✅ **Ya instaladas:**
- `twilio==9.8.8` (requirements.txt línea 44)
- `APScheduler==3.11.1` (requirements.txt línea 5)

✅ **No requiere nuevas dependencias**

---

## 3. Análisis de Costos

### 3.1 Twilio (Fase de Pruebas)

#### Precios Twilio (Paraguay, 2025)

**WhatsApp (Sandbox - Pruebas):**
- ✅ **GRATIS** durante período de prueba (hasta 1,000 conversaciones/mes)
- Después: $0.005 USD por conversación iniciada
- Período de gracia: 24 horas (mensajes dentro de 24h son gratis)

**SMS (Fallback):**
- Paraguay: ~$0.05-0.08 USD por SMS
- Usar solo como fallback si WhatsApp falla

#### Estimación de Costos Mensuales (Twilio)

**Escenario Conservador:**
- 100 citas/mes
- 2 recordatorios por cita (24h y 12h antes)
- 200 mensajes/mes
- **Costo: $0 USD** (dentro del período de prueba)

**Escenario Realista:**
- 500 citas/mes
- 2 recordatorios por cita
- 1,000 mensajes/mes
- **Costo: $5 USD/mes** (después del período de prueba)

**Escenario Alto Volumen:**
- 2,000 citas/mes
- 2 recordatorios por cita
- 4,000 mensajes/mes
- **Costo: $20 USD/mes**

#### Costos Adicionales Twilio

- **Número de teléfono:** $1 USD/mes (si se requiere número dedicado)
- **API calls:** Incluidos en el precio por mensaje
- **Webhooks:** Gratis

**Total estimado (producción): $5-25 USD/mes** según volumen

### 3.2 WhatsApp Business API (Producción)

#### Precios WhatsApp Business API (Meta, 2025)

**Modelo de Conversación:**
- **Conversación iniciada por usuario:** $0.005-0.09 USD (según país)
- **Conversación iniciada por empresa:** $0.005-0.09 USD
- Paraguay: ~$0.005-0.01 USD por conversación

**Ventana de 24 horas:**
- Todos los mensajes dentro de 24h de la última respuesta del usuario son **gratis**

**Costo por Template Message:**
- $0.005-0.01 USD por mensaje (Paraguay)

#### Estimación de Costos Mensuales (WhatsApp Business API)

**Escenario Conservador (100 citas/mes):**
- 200 recordatorios/mes
- **Costo: $1-2 USD/mes**

**Escenario Realista (500 citas/mes):**
- 1,000 recordatorios/mes
- **Costo: $5-10 USD/mes**

**Escenario Alto Volumen (2,000 citas/mes):**
- 4,000 recordatorios/mes
- **Costo: $20-40 USD/mes**

#### Costos Adicionales WhatsApp Business API

- **Meta Business Account:** Gratis
- **Número verificado:** Gratis (si ya tienes número)
- **API calls:** Incluidos
- **Soporte:** Incluido en planes básicos

**Total estimado (producción): $5-40 USD/mes** según volumen

### 3.3 Comparación de Costos

| Volumen Mensual | Twilio (Pruebas) | Twilio (Prod) | WhatsApp API |
|----------------|------------------|---------------|--------------|
| 100 citas | **$0** | $5 | $1-2 |
| 500 citas | **$0** | $5 | $5-10 |
| 2,000 citas | **$0** | $20 | $20-40 |

**Recomendación:**
- **Fase 1 (Pruebas):** Usar Twilio Sandbox (gratis)
- **Fase 2 (Producción):** Migrar a WhatsApp Business API (mejor precio y experiencia)

### 3.4 Costos de Desarrollo

**Tiempo estimado de implementación:**
- Desarrollo backend: 8-12 horas
- Testing: 4-6 horas
- Documentación: 2 horas

**Total: 14-20 horas de desarrollo**

---

## 4. Plan de Implementación

### 4.1 Fase 1: Implementación con Twilio (Pruebas)

#### Paso 1: Crear RecordatorioDao
- [ ] Crear `app/dao/modulos/recordatorio/RecordatorioDao.py`
- [ ] Implementar métodos CRUD básicos
- [ ] Implementar `getRecordatoriosPendientes()`

#### Paso 2: Integrar con CitaDao
- [ ] Agregar `crearRecordatoriosParaCita()` en CitaDao
- [ ] Modificar `guardarCita()` para crear recordatorios
- [ ] Modificar `updateCita()` para actualizar/cancelar recordatorios
- [ ] Modificar `cancelarCita()` para cancelar recordatorios

#### Paso 3: Mejorar TwilioService
- [ ] Agregar manejo robusto de errores
- [ ] Agregar logging detallado
- [ ] Agregar método de verificación de estado

#### Paso 4: Crear Tarea Programada
- [ ] Crear `app/tasks/recordatorio_tasks.py`
- [ ] Implementar `procesar_recordatorios_pendientes()`
- [ ] Agregar lógica de reintentos (máx 3)
- [ ] Configurar scheduler en `run.py`

#### Paso 5: Testing
- [ ] Crear citas de prueba
- [ ] Verificar creación de recordatorios
- [ ] Verificar envío automático
- [ ] Verificar actualización de estado
- [ ] Probar cancelación de citas

#### Paso 6: Configuración
- [ ] Agregar variables de entorno para Twilio
- [ ] Configurar webhook de Twilio (opcional)
- [ ] Documentar configuración

**Tiempo estimado: 2-3 días de desarrollo**

### 4.2 Fase 2: Migración a WhatsApp Business API

#### Paso 1: Crear WhatsAppService
- [ ] Crear `app/services/WhatsAppService.py`
- [ ] Implementar métodos similares a TwilioService
- [ ] Integrar con Meta Graph API

#### Paso 2: Refactorizar para Abstracción
- [ ] Crear interfaz `NotificationService` (abstracta)
- [ ] Hacer que TwilioService y WhatsAppService implementen la interfaz
- [ ] Modificar recordatorio_tasks para usar la interfaz

#### Paso 3: Configuración
- [ ] Obtener credenciales de Meta Business
- [ ] Verificar número de teléfono
- [ ] Configurar webhooks de Meta

#### Paso 4: Testing y Migración
- [ ] Probar en ambiente de staging
- [ ] Migrar gradualmente (feature flag)
- [ ] Monitorear costos y rendimiento

**Tiempo estimado: 3-5 días de desarrollo**

---

## 5. Consideraciones Técnicas

### 5.1 Manejo de Errores

**Errores comunes:**
- Número de teléfono inválido
- Número no tiene WhatsApp
- Límite de rate de Twilio/Meta
- Fallo de red

**Estrategia:**
- Reintentos automáticos (máx 3 intentos, con backoff exponencial)
- Logging detallado de errores
- Notificación a administradores si falla > 5% de mensajes

### 5.2 Performance

**Optimizaciones:**
- Query optimizada con índice `idx_recordatorios_pendientes`
- Procesar en lotes (batch) de 50-100 recordatorios
- Ejecutar tarea cada 5-10 minutos (no cada minuto)

### 5.3 Seguridad

- ✅ Credenciales de Twilio/Meta en variables de entorno
- ✅ Validación de números de teléfono
- ✅ Logging sin exponer datos sensibles
- ✅ Rate limiting para evitar abuso

### 5.4 Escalabilidad

**Si el volumen crece:**
- Considerar cola de mensajes (Redis/RabbitMQ)
- Procesar recordatorios de forma asíncrona
- Distribuir carga en múltiples workers

---

## 6. Riesgos y Mitigaciones

### 6.1 Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Twilio bloquea cuenta por spam | Baja | Alto | Validar números, respetar rate limits |
| Costos superan presupuesto | Media | Medio | Monitorear costos, alertas automáticas |
| Fallos en envío masivo | Media | Medio | Reintentos automáticos, logging |
| Migración a WhatsApp API compleja | Baja | Medio | Abstracción desde el inicio |

### 6.2 Monitoreo Recomendado

- **Métricas clave:**
  - Tasa de éxito de envío (%)
  - Costo por mensaje
  - Tiempo de procesamiento
  - Errores por tipo

- **Alertas:**
  - Tasa de éxito < 90%
  - Costo mensual > umbral configurado
  - Errores consecutivos > 10

---

## 7. Recomendaciones Finales

### 7.1 Implementación Inmediata (Twilio)

✅ **Ventajas:**
- Rápido de implementar (2-3 días)
- Gratis durante pruebas
- Código reutilizable para WhatsApp API
- Bajo riesgo

✅ **Recomendación: IMPLEMENTAR**

### 7.2 Migración a WhatsApp Business API

✅ **Ventajas:**
- Mejor experiencia de usuario
- Precios competitivos
- Integración nativa con WhatsApp
- Mejor para producción

✅ **Recomendación: MIGRAR después de 1-2 meses de pruebas**

### 7.3 Próximos Pasos

1. **Aprobar implementación con Twilio**
2. **Asignar desarrollador (14-20 horas)**
3. **Configurar cuenta Twilio Sandbox**
4. **Desarrollar e implementar**
5. **Probar en ambiente de staging**
6. **Desplegar a producción**
7. **Monitorear costos y rendimiento**
8. **Planificar migración a WhatsApp API**

---

## 8. Conclusión

**Impacto Técnico:** MEDIO (530 líneas de código, cambios en 4-5 archivos)
**Impacto en BD:** NINGUNO (tabla ya existe)
**Impacto en Frontend:** MÍNIMO (opcional)
**Costo Mensual:** $0-25 USD según volumen
**Tiempo de Desarrollo:** 2-3 días (Fase 1)

**Recomendación Final:**
✅ **PROCEDER con la implementación**. El sistema ya tiene la infraestructura necesaria (tabla, TwilioService, scheduler). Solo falta conectar los componentes y crear la tarea programada.

**ROI Esperado:**
- Reducción de inasistencias: 20-30%
- Mejora en experiencia del paciente
- Ahorro de tiempo del personal (no llamar manualmente)

---

## Anexos

### A. Estructura de Archivos Propuesta

```
app/
├── dao/
│   └── modulos/
│       └── recordatorio/
│           ├── __init__.py
│           └── RecordatorioDao.py (NUEVO)
├── services/
│   ├── TwilioService.py (MEJORAR)
│   └── WhatsAppService.py (FUTURO)
├── tasks/
│   ├── __init__.py
│   ├── auth_tasks.py (EXISTE)
│   └── recordatorio_tasks.py (NUEVO)
└── dao/modulos/cita/
    └── CitaDao.py (MODIFICAR)
```

### B. Ejemplo de Mensaje de Recordatorio

```
🏥 *Recordatorio de Cita Médica*

Hola Juan Pérez,

Le recordamos su cita:
📅 Fecha: 15/01/2025
🕐 Hora: 10:00
👨‍⚕️ Profesional: Dr. Carlos González
🩺 Especialidad: Cardiología
📋 Motivo: Control de presión arterial

Por favor confirme su asistencia respondiendo:
✅ SI - para confirmar
❌ NO - para cancelar

¡Gracias!
```

### C. Variables de Entorno Necesarias

```bash
# Twilio (Fase 1)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_FROM_NUMBER=whatsapp:+14155238886

# WhatsApp Business API (Fase 2)
WHATSAPP_ACCESS_TOKEN=xxxxx
WHATSAPP_PHONE_NUMBER_ID=xxxxx
WHATSAPP_BUSINESS_ACCOUNT_ID=xxxxx
```

---

**Documento creado:** 2025-01-XX
**Última actualización:** 2025-01-XX
**Autor:** Análisis Técnico - Sistema Sysclin

