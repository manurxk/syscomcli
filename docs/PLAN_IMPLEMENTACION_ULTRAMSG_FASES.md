# Plan de Implementación: UltraMsg por Fases

**Fecha:** 2026-01-22  
**Sistema:** Angasys - Sistema de Gestión Médica  
**Objetivo:** Implementar UltraMsg para notificaciones WhatsApp en fases incrementales

---

## 📋 Resumen de Fases

| Fase | Descripción | Tiempo | Prioridad | Estado |
|------|-------------|--------|-----------|--------|
| **Fase 1** | MVP - Envío básico de recordatorios | 6-8 horas | ALTA | 🟢 En progreso |
| **Fase 2** | Mejoras y optimizaciones | 3-4 horas | MEDIA | ⚪ Pendiente |
| **Fase 3** | Recepción de respuestas (Webhooks) | 4-6 horas | BAJA | ⚪ Pendiente |
| **Fase 4** | Plantillas y medios | 2-3 horas | BAJA | ⚪ Pendiente |

**Tiempo Total Estimado:** 15-21 horas

---

## 🚀 FASE 1: MVP - Envío Básico de Recordatorios

### Objetivo
Implementar funcionalidad básica para enviar recordatorios de citas por WhatsApp usando UltraMsg.

### Componentes a Implementar

#### 1.1 Crear UltraMsgService
- ✅ Servicio principal con métodos básicos
- ✅ Envío de mensajes de texto
- ✅ Formateo de números telefónicos
- ✅ Construcción de mensajes personalizados
- ✅ Manejo básico de errores

#### 1.2 Configuración
- ✅ Variables de entorno
- ✅ Configuración en app/__init__.py

#### 1.3 Integración
- ✅ Integrar en recordatorio_tasks.py
- ✅ Actualizar recordatorio_api.py
- ✅ Actualizar RecordatorioDao.py

#### 1.4 Base de Datos (Opcional)
- ✅ Script SQL para columna de tracking

#### 1.5 Documentación
- ✅ Guía de configuración

### Entregables
- [x] `app/services/UltraMsgService.py`
- [ ] Configuración actualizada
- [ ] Integración completa
- [ ] Script SQL opcional
- [ ] Documentación de configuración

### Criterios de Éxito
- ✅ Envío de recordatorios funciona correctamente
- ✅ Manejo de errores básico implementado
- ✅ Logging de operaciones funcionando
- ✅ Sistema puede procesar recordatorios pendientes

---

## 🔧 FASE 2: Mejoras y Optimizaciones

### Objetivo
Mejorar la robustez del sistema, agregar reintentos automáticos y optimizar el manejo de errores.

### Componentes a Implementar

#### 2.1 Reintentos Automáticos
- Sistema de reintentos con backoff exponencial
- Límite máximo de reintentos configurable
- Diferentes estrategias según tipo de error

#### 2.2 Rate Limiting
- Respeto de límites de UltraMsg
- Cola de mensajes para distribución temporal
- Priorización de mensajes urgentes

#### 2.3 Mejoras en Manejo de Errores
- Categorización de errores (temporal, permanente, rate limit)
- Mensajes de error más descriptivos
- Alertas para errores críticos

#### 2.4 Métricas y Monitoreo
- Contador de mensajes enviados
- Tasa de éxito/fallo
- Tiempo promedio de envío
- Logging mejorado

### Entregables
- Sistema de reintentos
- Rate limiting implementado
- Métricas básicas
- Mejoras en logging

### Criterios de Éxito
- Sistema maneja errores temporales automáticamente
- Rate limiting funciona correctamente
- Métricas disponibles para monitoreo

---

## 📨 FASE 3: Recepción de Respuestas (Webhooks)

### Objetivo
Implementar recepción de mensajes entrantes para confirmaciones de pacientes.

### Componentes a Implementar

#### 3.1 Endpoint de Webhook
- Endpoint para recibir webhooks de UltraMsg
- Validación de seguridad
- Procesamiento de mensajes entrantes

#### 3.2 Procesamiento de Respuestas
- Reconocimiento de confirmaciones (SÍ/NO)
- Actualización de estado de citas
- Respuestas automáticas

#### 3.3 Integración con Sistema de Citas
- Actualizar estado de cita según respuesta
- Notificar a especialistas de cancelaciones
- Registrar interacciones

### Entregables
- Endpoint de webhook
- Procesamiento de respuestas
- Integración con sistema de citas

### Criterios de Éxito
- Sistema recibe y procesa mensajes entrantes
- Confirmaciones actualizan estado de citas
- Respuestas automáticas funcionan

---

## 🎨 FASE 4: Plantillas y Medios

### Objetivo
Agregar soporte para plantillas de mensajes y envío de medios (imágenes, documentos).

### Componentes a Implementar

#### 4.1 Plantillas de Mensajes
- Sistema de plantillas personalizables
- Variables dinámicas en plantillas
- Plantillas pre-aprobadas por WhatsApp

#### 4.2 Envío de Medios
- Envío de imágenes (QR codes, logos)
- Envío de documentos (recetas, certificados)
- Envío de ubicaciones (dirección de clínica)

#### 4.3 Mejoras en Mensajes
- Mensajes más ricos y visuales
- Botones interactivos (cuando esté disponible)
- Formato mejorado de mensajes

### Entregables
- Sistema de plantillas
- Envío de medios funcionando
- Mensajes mejorados

### Criterios de Éxito
- Plantillas funcionan correctamente
- Medios se envían sin errores
- Mensajes son más atractivos

---

## 📝 Checklist de Implementación por Fase

### Fase 1: MVP ✅
- [x] Crear UltraMsgService.py
- [ ] Configurar variables de entorno
- [ ] Integrar en recordatorio_tasks.py
- [ ] Actualizar recordatorio_api.py
- [ ] Actualizar RecordatorioDao.py
- [ ] Crear script SQL opcional
- [ ] Crear documentación de configuración
- [ ] Pruebas básicas

### Fase 2: Mejoras
- [ ] Implementar sistema de reintentos
- [ ] Implementar rate limiting
- [ ] Agregar métricas
- [ ] Mejorar logging
- [ ] Pruebas de robustez

### Fase 3: Webhooks
- [ ] Crear endpoint de webhook
- [ ] Implementar validación de seguridad
- [ ] Procesar mensajes entrantes
- [ ] Integrar con sistema de citas
- [ ] Pruebas de recepción

### Fase 4: Plantillas y Medios
- [ ] Sistema de plantillas
- [ ] Envío de imágenes
- [ ] Envío de documentos
- [ ] Envío de ubicaciones
- [ ] Pruebas de medios

---

## 🎯 Recomendaciones de Implementación

### Orden Recomendado
1. **Fase 1 (MVP)** - Implementar primero para tener funcionalidad básica
2. **Fase 2 (Mejoras)** - Mejorar robustez antes de agregar funcionalidades
3. **Fase 3 (Webhooks)** - Agregar cuando se necesite interactividad
4. **Fase 4 (Plantillas)** - Agregar cuando se necesite mejorar UX

### Entre Fases
- Realizar pruebas exhaustivas después de cada fase
- Monitorear uso y rendimiento
- Recopilar feedback de usuarios
- Ajustar plan según necesidades

### Consideraciones
- No avanzar a la siguiente fase hasta que la actual esté estable
- Documentar cada fase antes de continuar
- Mantener código limpio y bien estructurado
- Considerar rollback si hay problemas críticos

---

**Documento creado:** 2026-01-22  
**Última actualización:** 2026-01-22  
**Versión:** 1.0

