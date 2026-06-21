# Análisis de Requisitos: Integración de UltraMsg para Notificaciones WhatsApp

**Fecha:** 2026-01-22  
**Sistema:** Sysclin - Sistema de Gestión Médica  
**Objetivo:** Integrar UltraMsg para envío de notificaciones y recordatorios de citas por WhatsApp

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Descripción de UltraMsg](#descripción-de-ultramsg)
3. [Requisitos Funcionales](#requisitos-funcionales)
4. [Requisitos Técnicos](#requisitos-técnicos)
5. [Análisis de Complejidad](#análisis-de-complejidad)
6. [Cambios Necesarios en el Código](#cambios-necesarios-en-el-código)
7. [Estructura de Archivos](#estructura-de-archivos)
8. [Costos Estimados](#costos-estimados)
9. [Plan de Implementación](#plan-de-implementación)
10. [Comparación con Alternativas](#comparación-con-alternativas)
11. [Riesgos y Consideraciones](#riesgos-y-consideraciones)
12. [Recomendaciones](#recomendaciones)

---

## 🎯 Resumen Ejecutivo

### Objetivo
Integrar UltraMsg como servicio de notificaciones para enviar recordatorios de citas médicas y notificaciones por WhatsApp, reemplazando la funcionalidad que anteriormente estaba implementada con Twilio.

### Complejidad Estimada
- **Nivel:** BAJA a MEDIA
- **Tiempo de Desarrollo:** 6-8 horas
- **Esfuerzo:** 1 desarrollador

### Ventajas Clave
- ✅ API más simple y directa que Twilio
- ✅ Costos generalmente más bajos
- ✅ Específicamente diseñado para WhatsApp
- ✅ No requiere sandbox para desarrollo
- ✅ Mejor soporte para medios (imágenes, documentos)

### Desventajas
- ❌ Solo soporta WhatsApp (no SMS, voz, email)
- ❌ Requiere número de WhatsApp Business verificado
- ❌ Menos documentación que Twilio

---

## 📱 Descripción de UltraMsg

### ¿Qué es UltraMsg?
UltraMsg es una plataforma de API para WhatsApp Business que permite enviar y recibir mensajes de WhatsApp mediante API REST. Es una alternativa más económica y simple que Twilio para casos de uso específicos de WhatsApp.

### Características Principales
- **Envío de mensajes de texto**
- **Envío de medios** (imágenes, documentos, videos, audio)
- **Envío de ubicaciones**
- **Envío de contactos**
- **Plantillas de mensajes** (mensajes aprobados por WhatsApp)
- **Webhooks** para recibir mensajes entrantes
- **API REST simple** con autenticación por token

### Requisitos Previos
1. **Cuenta en UltraMsg** (https://ultramsg.com)
2. **Número de WhatsApp Business** verificado
3. **Token de API** proporcionado por UltraMsg
4. **Instance ID** de la instancia configurada

---

## 🎯 Requisitos Funcionales

### RF-01: Envío de Recordatorios de Citas
- **Descripción:** El sistema debe poder enviar recordatorios de citas médicas por WhatsApp
- **Prioridad:** ALTA
- **Casos de Uso:**
  - Recordatorio 24 horas antes de la cita
  - Recordatorio 12 horas antes de la cita
  - Recordatorio personalizado con información de la cita

### RF-02: Notificaciones de Confirmación
- **Descripción:** El sistema debe poder enviar notificaciones de confirmación de citas
- **Prioridad:** MEDIA
- **Casos de Uso:**
  - Confirmación de cita creada
  - Confirmación de cita modificada
  - Confirmación de cita cancelada

### RF-03: Manejo de Errores
- **Descripción:** El sistema debe manejar errores de envío y reintentar automáticamente
- **Prioridad:** ALTA
- **Casos de Uso:**
  - Número inválido
  - Número no registrado en WhatsApp
  - Límite de rate alcanzado
  - Error de conectividad

### RF-04: Logging y Tracking
- **Descripción:** El sistema debe registrar todos los envíos y sus estados
- **Prioridad:** MEDIA
- **Casos de Uso:**
  - Guardar ID del mensaje enviado
  - Registrar estado del mensaje (enviado, entregado, leído)
  - Mantener historial de intentos

### RF-05: Recepción de Respuestas (Opcional)
- **Descripción:** El sistema debe poder recibir confirmaciones de pacientes
- **Prioridad:** BAJA
- **Casos de Uso:**
  - Confirmación de asistencia
  - Cancelación de cita
  - Solicitud de reprogramación

---

## 🔧 Requisitos Técnicos

### RT-01: Dependencias
```python
# Nuevas dependencias necesarias
requests>=2.32.5  # Ya existe en requirements.txt
# No se requiere SDK específico, se usa API REST directa
```

### RT-02: Variables de Entorno
```bash
# Configuración necesaria
ULTRAMSG_INSTANCE_ID="tu_instance_id"
ULTRAMSG_TOKEN="tu_token_api"
ULTRAMSG_API_URL="https://api.ultramsg.com"  # URL base de la API
```

### RT-03: Base de Datos
- **Columna adicional opcional:** `recordatorio_ultramsg_id` (VARCHAR) para tracking
- **Estructura actual:** La tabla `recordatorios` ya tiene la estructura necesaria

### RT-04: Formato de Números
- **Formato requerido:** Números en formato internacional (ej: +595981123456)
- **Validación:** El sistema debe validar y formatear números antes de enviar

### RT-05: Rate Limiting
- **Límites de UltraMsg:** Generalmente 1000 mensajes/día en planes básicos
- **Implementación:** El sistema debe respetar los límites y hacer cola de mensajes

---

## 📊 Análisis de Complejidad

### Componentes a Desarrollar

| Componente | Complejidad | Tiempo Estimado | Prioridad |
|-----------|-------------|-----------------|-----------|
| UltraMsgService.py | BAJA | 2-3 horas | ALTA |
| Integración en recordatorio_tasks.py | BAJA | 1 hora | ALTA |
| Actualización de recordatorio_api.py | BAJA | 1 hora | ALTA |
| Actualización de RecordatorioDao.py | BAJA | 30 min | MEDIA |
| Configuración de variables de entorno | BAJA | 15 min | ALTA |
| Pruebas y validación | MEDIA | 2 horas | ALTA |
| Documentación | BAJA | 30 min | MEDIA |

**Total Estimado:** 6-8 horas

### Factores de Complejidad

#### ✅ Factores que REDUCEN la complejidad:
- La estructura del sistema de recordatorios ya existe
- El patrón de servicio ya estaba implementado (TwilioService)
- La base de datos ya tiene la estructura necesaria
- El scheduler ya está configurado

#### ⚠️ Factores que AUMENTAN la complejidad:
- Necesidad de formatear números telefónicos correctamente
- Manejo de diferentes tipos de mensajes (texto, medios)
- Implementación de webhooks para respuestas (opcional)
- Manejo de rate limiting

---

## 💻 Cambios Necesarios en el Código

### 1. Crear UltraMsgService

**Archivo:** `app/services/UltraMsgService.py`

```python
# Estructura básica del servicio
class UltraMsgService:
    def __init__(self):
        # Inicializar con credenciales desde app.config
        
    def enviar_recordatorio_cita(self, telefono, nombre_paciente, ...):
        # Enviar mensaje de recordatorio
        
    def _formatear_telefono(self, telefono):
        # Formatear número al formato internacional
        
    def _construir_mensaje_recordatorio(self, ...):
        # Construir mensaje personalizado
        
    def verificar_estado_mensaje(self, message_id):
        # Verificar estado del mensaje (opcional)
```

**Funcionalidades principales:**
- Envío de mensajes de texto
- Formateo de números telefónicos
- Construcción de mensajes personalizados
- Manejo de errores y reintentos
- Logging de operaciones

### 2. Actualizar recordatorio_tasks.py

**Cambios necesarios:**
```python
# Reemplazar
from app.services.TwilioService import TwilioService
# Por
from app.services.UltraMsgService import UltraMsgService

# Actualizar inicialización
ultramsg_service = UltraMsgService()

# Actualizar llamadas al servicio
success, message_id, error = ultramsg_service.enviar_recordatorio_cita(...)
```

### 3. Actualizar recordatorio_api.py

**Cambios necesarios:**
```python
# Reemplazar importación
from app.services.UltraMsgService import UltraMsgService

# Actualizar función de reenvío
ultramsg_service = UltraMsgService()
```

### 4. Actualizar RecordatorioDao.py

**Cambios necesarios:**
- Actualizar método `marcarEnviado()` para aceptar `ultramsg_id` en lugar de `twilio_sid`
- Mantener compatibilidad con estructura existente

### 5. Actualizar Configuración

**Archivo:** `app/__init__.py` o archivo de configuración

```python
# Agregar configuración
app.config['ULTRAMSG_INSTANCE_ID'] = os.getenv('ULTRAMSG_INSTANCE_ID')
app.config['ULTRAMSG_TOKEN'] = os.getenv('ULTRAMSG_TOKEN')
app.config['ULTRAMSG_API_URL'] = os.getenv('ULTRAMSG_API_URL', 'https://api.ultramsg.com')
```

### 6. Actualizar Base de Datos (Opcional)

**Script SQL:** `app/varios/SQL/add_ultramsg_column.sql`

```sql
-- Agregar columna para tracking (opcional)
ALTER TABLE recordatorios 
ADD COLUMN IF NOT EXISTS recordatorio_ultramsg_id VARCHAR(100);
```

---

## 📁 Estructura de Archivos

### Archivos Nuevos a Crear

```
app/
├── services/
│   └── UltraMsgService.py          # Servicio principal de UltraMsg
│
app/varios/SQL/
└── add_ultramsg_column.sql          # Script SQL opcional para columna de tracking

docs/
└── CONFIGURACION_ULTRAMSG.md        # Guía de configuración
```

### Archivos a Modificar

```
app/
├── __init__.py                      # Agregar configuración
├── tasks/
│   └── recordatorio_tasks.py        # Integrar UltraMsgService
├── rutas/
│   └── modulos/
│       └── recordatorio/
│           └── recordatorio_api.py # Actualizar importaciones
└── dao/
    └── modulos/
        └── recordatorio/
            └── RecordatorioDao.py  # Actualizar método marcarEnviado

requirements.txt                     # Verificar dependencias (requests ya existe)
```

---

## 💰 Costos Estimados

### Costos de UltraMsg

#### Planes Disponibles (aproximados)

| Plan | Mensajes/Mes | Precio Mensual (USD) | Precio por Mensaje |
|------|--------------|----------------------|-------------------|
| Starter | 1,000 | $5-10 | $0.005-0.01 |
| Basic | 5,000 | $20-30 | $0.004-0.006 |
| Pro | 25,000 | $50-80 | $0.002-0.003 |
| Enterprise | Ilimitado | Personalizado | Negociable |

### Estimación de Uso

**Escenario:** Clínica con 100 citas/día
- Recordatorios 24h: 100 mensajes/día
- Recordatorios 12h: 100 mensajes/día
- Notificaciones varias: 50 mensajes/día
- **Total:** ~250 mensajes/día = ~7,500 mensajes/mes

**Costo Estimado:** $30-50 USD/mes (plan Basic)

### Comparación con Twilio

| Aspecto | Twilio | UltraMsg |
|---------|--------|----------|
| Costo por mensaje | $0.005-0.01 | $0.002-0.006 |
| Plan mínimo | $15-20/mes | $5-10/mes |
| Mensajes incluidos | 0 | 1,000-5,000 |
| Configuración | Compleja | Simple |

**Ahorro estimado:** 40-60% comparado con Twilio

---

## 🚀 Plan de Implementación

### Fase 1: Preparación (1 hora)
- [ ] Crear cuenta en UltraMsg
- [ ] Obtener credenciales (Instance ID y Token)
- [ ] Configurar número de WhatsApp Business
- [ ] Configurar variables de entorno

### Fase 2: Desarrollo del Servicio (2-3 horas)
- [ ] Crear `UltraMsgService.py`
- [ ] Implementar método de envío de mensajes
- [ ] Implementar formateo de números
- [ ] Implementar construcción de mensajes
- [ ] Agregar manejo de errores
- [ ] Agregar logging

### Fase 3: Integración (1-2 horas)
- [ ] Actualizar `recordatorio_tasks.py`
- [ ] Actualizar `recordatorio_api.py`
- [ ] Actualizar `RecordatorioDao.py`
- [ ] Agregar configuración en `app/__init__.py`

### Fase 4: Base de Datos (30 min)
- [ ] Ejecutar script SQL (opcional)
- [ ] Verificar estructura de tabla

### Fase 5: Pruebas (2 horas)
- [ ] Pruebas unitarias del servicio
- [ ] Pruebas de integración
- [ ] Pruebas de envío real
- [ ] Validar manejo de errores
- [ ] Validar rate limiting

### Fase 6: Documentación (30 min)
- [ ] Documentar configuración
- [ ] Documentar uso del servicio
- [ ] Actualizar README si es necesario

### Fase 7: Despliegue (1 hora)
- [ ] Configurar variables de entorno en producción
- [ ] Desplegar código
- [ ] Verificar funcionamiento
- [ ] Monitorear primeros envíos

**Tiempo Total:** 6-8 horas

---

## 🔄 Comparación con Alternativas

### UltraMsg vs Twilio

| Característica | UltraMsg | Twilio |
|----------------|----------|--------|
| **Costo** | ✅ Más económico | ❌ Más caro |
| **Simplicidad** | ✅ API más simple | ❌ Más complejo |
| **WhatsApp** | ✅ Especializado | ✅ Soporta |
| **SMS** | ❌ No soporta | ✅ Soporta |
| **Voz** | ❌ No soporta | ✅ Soporta |
| **Email** | ❌ No soporta | ✅ Soporta |
| **Documentación** | ⚠️ Menos completa | ✅ Muy completa |
| **Soporte** | ⚠️ Limitado | ✅ Excelente |
| **Sandbox** | ❌ No necesario | ✅ Disponible |

### UltraMsg vs WhatsApp Business API Oficial

| Característica | UltraMsg | WhatsApp Business API |
|----------------|----------|----------------------|
| **Costo** | ✅ Más económico | ❌ Más caro |
| **Configuración** | ✅ Simple | ❌ Compleja |
| **Aprobación** | ✅ Rápida | ❌ Lenta (semanas) |
| **Funcionalidades** | ⚠️ Limitadas | ✅ Completas |
| **Escalabilidad** | ⚠️ Limitada | ✅ Ilimitada |

### Recomendación

**Usar UltraMsg si:**
- ✅ Solo necesitas WhatsApp
- ✅ Presupuesto limitado
- ✅ Necesitas implementación rápida
- ✅ Volumen de mensajes moderado (< 25,000/mes)

**No usar UltraMsg si:**
- ❌ Necesitas múltiples canales (SMS, voz, email)
- ❌ Necesitas funcionalidades avanzadas
- ❌ Volumen muy alto de mensajes
- ❌ Requieres soporte 24/7

---

## ⚠️ Riesgos y Consideraciones

### Riesgos Técnicos

1. **Rate Limiting**
   - **Riesgo:** Límites de mensajes por día pueden ser alcanzados
   - **Mitigación:** Implementar cola de mensajes y distribución temporal

2. **Formato de Números**
   - **Riesgo:** Números mal formateados causan errores
   - **Mitigación:** Validación y formateo robusto

3. **Disponibilidad del Servicio**
   - **Riesgo:** UltraMsg puede tener downtime
   - **Mitigación:** Implementar reintentos y logging de errores

4. **Cambios en la API**
   - **Riesgo:** UltraMsg puede cambiar su API
   - **Mitigación:** Versionar el servicio y monitorear cambios

### Consideraciones de Negocio

1. **Dependencia de un Proveedor**
   - Considerar tener un plan B o servicio alternativo

2. **Cumplimiento Normativo**
   - Verificar que UltraMsg cumpla con regulaciones locales de privacidad

3. **Escalabilidad**
   - Evaluar si UltraMsg puede manejar el crecimiento futuro

4. **Soporte**
   - Considerar el nivel de soporte necesario

---

## 📝 Recomendaciones

### ✅ Recomendación Principal

**PROCEDER con la integración de UltraMsg** si:
- El presupuesto es limitado
- Solo se necesita WhatsApp
- Se requiere una implementación rápida
- El volumen de mensajes es moderado

### Implementación Recomendada

1. **Fase Inicial (MVP):**
   - Implementar envío básico de recordatorios
   - Validar funcionamiento con pruebas reales
   - Monitorear costos y rendimiento

2. **Fase de Mejora:**
   - Agregar recepción de respuestas (webhooks)
   - Implementar plantillas de mensajes
   - Agregar envío de medios si es necesario

3. **Fase de Optimización:**
   - Implementar cola de mensajes
   - Optimizar rate limiting
   - Agregar métricas y monitoreo

### Alternativa Híbrida

Considerar mantener la arquitectura flexible para poder cambiar de proveedor fácilmente:
- Crear una interfaz abstracta `NotificationService`
- Implementar `UltraMsgService` y potencialmente otros servicios
- Permitir cambiar de proveedor sin modificar el código principal

---

## 📚 Referencias y Recursos

### Documentación Oficial
- [UltraMsg API Documentation](https://ultramsg.com/docs)
- [UltraMsg Python Examples](https://ultramsg.com/docs/python)

### Recursos Adicionales
- [WhatsApp Business API Guidelines](https://developers.facebook.com/docs/whatsapp)
- [Best Practices for WhatsApp Messages](https://developers.facebook.com/docs/whatsapp/messaging-types)

### Soporte
- Email de soporte: support@ultramsg.com
- Documentación: https://ultramsg.com/docs

---

## ✅ Checklist de Implementación

### Pre-requisitos
- [ ] Cuenta creada en UltraMsg
- [ ] Credenciales obtenidas (Instance ID y Token)
- [ ] Número de WhatsApp Business verificado
- [ ] Variables de entorno configuradas

### Desarrollo
- [ ] `UltraMsgService.py` creado y probado
- [ ] Integración en `recordatorio_tasks.py` completada
- [ ] Actualización de `recordatorio_api.py` completada
- [ ] Actualización de `RecordatorioDao.py` completada
- [ ] Configuración agregada en `app/__init__.py`

### Pruebas
- [ ] Pruebas unitarias del servicio
- [ ] Pruebas de integración
- [ ] Pruebas de envío real
- [ ] Validación de manejo de errores

### Despliegue
- [ ] Variables de entorno configuradas en producción
- [ ] Código desplegado
- [ ] Funcionamiento verificado
- [ ] Monitoreo activo

---

**Documento creado:** 2026-01-22  
**Última actualización:** 2026-01-22  
**Versión:** 1.0

