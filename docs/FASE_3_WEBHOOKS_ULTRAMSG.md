# Fase 3: Implementación de Webhooks UltraMsg

**Fecha:** 2026-01-22  
**Sistema:** Angasys - Sistema de Gestión Médica  
**Objetivo:** Implementar recepción de webhooks de UltraMsg para actualizar estados de mensajes y recibir respuestas de pacientes

---

## 📋 Resumen

La Fase 3 implementa la recepción de webhooks de UltraMsg para:
- Actualizar el estado de los mensajes enviados (enviado, entregado, leído, fallido)
- Recibir mensajes entrantes de pacientes
- Procesar confirmaciones de citas (SÍ/NO)
- Actualizar automáticamente el estado de las citas según las respuestas

---

## 🎯 Objetivos

1. **Tracking de Mensajes:** Actualizar el estado de los mensajes en tiempo real
2. **Confirmaciones Automáticas:** Procesar respuestas de pacientes sobre sus citas
3. **Actualización de Estados:** Modificar el estado de las citas según las confirmaciones
4. **Notificaciones:** Alertar a especialistas sobre cancelaciones o cambios

---

## 📦 Componentes a Implementar

### 1. Endpoint de Webhook

#### 1.1 Crear Blueprint de Webhooks
**Archivo:** `app/rutas/modulos/recordatorio/webhook_api.py`

```python
from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.recordatorio.RecordatorioDao import RecordatorioDao
from app.dao.modulos.cita.CitaDao import CitaDao
import hmac
import hashlib

webhookapi = Blueprint('webhookapi', __name__)
```

#### 1.2 Endpoint Principal
**Ruta:** `POST /api/v1/webhooks/ultramsg`

**Funcionalidades:**
- Validar firma del webhook (seguridad)
- Procesar diferentes tipos de eventos
- Actualizar estados en la base de datos
- Responder con 200 OK a UltraMsg

**Tipos de eventos a manejar:**
- `sent`: Mensaje enviado exitosamente
- `delivered`: Mensaje entregado al destinatario
- `read`: Mensaje leído por el destinatario
- `failed`: Mensaje falló al enviar
- `message`: Mensaje entrante del paciente

---

### 2. Validación de Seguridad

#### 2.1 Verificación de Firma
UltraMsg puede enviar una firma HMAC para validar que el webhook es legítimo.

**Implementación:**
```python
def verificar_firma_webhook(payload, firma_recibida, secret_key):
    """
    Verifica la firma HMAC del webhook
    """
    firma_calculada = hmac.new(
        secret_key.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(firma_calculada, firma_recibida)
```

#### 2.2 Configuración
Agregar en `app/__init__.py`:
```python
app.config['ULTRAMSG_WEBHOOK_SECRET'] = os.getenv('ULTRAMSG_WEBHOOK_SECRET', '')
```

---

### 3. Procesamiento de Eventos

#### 3.1 Estructura de Eventos UltraMsg

**Evento: Mensaje Enviado/Entregado/Leído**
```json
{
  "event": "sent|delivered|read",
  "data": {
    "id": "msg_123456",
    "from": "595991301397",
    "to": "595991234567",
    "status": "sent|delivered|read",
    "timestamp": "2026-01-22T10:30:00Z"
  }
}
```

**Evento: Mensaje Fallido**
```json
{
  "event": "failed",
  "data": {
    "id": "msg_123456",
    "from": "595991301397",
    "to": "595991234567",
    "error": "Invalid phone number",
    "timestamp": "2026-01-22T10:30:00Z"
  }
}
```

**Evento: Mensaje Entrante**
```json
{
  "event": "message",
  "data": {
    "id": "msg_789012",
    "from": "595991234567",
    "to": "595991301397",
    "body": "SÍ, confirmo mi cita",
    "timestamp": "2026-01-22T10:30:00Z"
  }
}
```

#### 3.2 Actualización de Estados

**Método en RecordatorioDao:**
```python
def actualizarEstadoMensaje(self, message_id, nuevo_estado, error=None):
    """
    Actualiza el estado de un mensaje basado en webhook
    
    Args:
        message_id: ID del mensaje de UltraMsg
        nuevo_estado: 'sent', 'delivered', 'read', 'failed'
        error: Mensaje de error si falló
    """
    # Buscar recordatorio por message_id
    # Actualizar estado y fecha correspondiente
    # Si falló, incrementar intentos o marcar como fallido
```

---

### 4. Procesamiento de Confirmaciones

#### 4.1 Reconocimiento de Respuestas

**Patrones a reconocer:**
- Confirmación: "SÍ", "SI", "CONFIRMO", "OK", "DE ACUERDO", "ACEPTO"
- Cancelación: "NO", "CANCELO", "CANCELAR", "ANULAR", "NO PUEDO"

**Implementación:**
```python
def procesar_confirmacion_cita(mensaje_texto, id_cita):
    """
    Procesa una confirmación o cancelación de cita
    
    Returns:
        tuple: (tipo, confirmado) donde tipo es 'confirmacion'|'cancelacion'|'desconocido'
    """
    mensaje_upper = mensaje_texto.upper().strip()
    
    confirmaciones = ['SÍ', 'SI', 'CONFIRMO', 'OK', 'DE ACUERDO', 'ACEPTO', 'CONFIRMAR']
    cancelaciones = ['NO', 'CANCELO', 'CANCELAR', 'ANULAR', 'NO PUEDO', 'NO PUEDO IR']
    
    if any(conf in mensaje_upper for conf in confirmaciones):
        return ('confirmacion', True)
    elif any(canc in mensaje_upper for canc in cancelaciones):
        return ('cancelacion', False)
    else:
        return ('desconocido', None)
```

#### 4.2 Actualización de Estado de Cita

**Método en CitaDao:**
```python
def actualizarEstadoPorConfirmacion(self, id_cita, confirmado):
    """
    Actualiza el estado de una cita según confirmación del paciente
    
    Args:
        id_cita: ID de la cita
        confirmado: True si confirmó, False si canceló
    """
    if confirmado:
        # Mantener o actualizar a estado "CONFIRMADA"
        nuevo_estado = "CONFIRMADA"
    else:
        # Cambiar a estado "CANCELADA"
        nuevo_estado = "CANCELADA"
    
    # Actualizar en BD
    # Notificar a especialista si se canceló
```

---

### 5. Respuestas Automáticas

#### 5.1 Respuesta a Confirmación
```python
def enviar_respuesta_confirmacion(telefono, confirmado, cita_info):
    """
    Envía respuesta automática al paciente según su confirmación
    """
    if confirmado:
        mensaje = f"""
✅ ¡Gracias por confirmar tu cita!

📅 Fecha: {cita_info['fecha']}
🕐 Hora: {cita_info['hora']}
👨‍⚕️ Especialista: {cita_info['especialista']}

Te esperamos. Si necesitas cambiar o cancelar, avísanos con anticipación.
        """
    else:
        mensaje = f"""
✅ Hemos registrado la cancelación de tu cita.

Si deseas reagendar, por favor contáctanos.

Gracias.
        """
    
    ultramsg_service.enviar_mensaje_simple(telefono, mensaje)
```

---

## 📁 Estructura de Archivos

```
app/
├── rutas/
│   └── modulos/
│       └── recordatorio/
│           ├── webhook_api.py          # Nuevo: Endpoint de webhooks
│           ├── recordatorio_api.py      # Existente
│           └── templates/
│               └── recordatorio-index.html
├── dao/
│   └── modulos/
│       ├── recordatorio/
│       │   └── RecordatorioDao.py      # Actualizar: agregar métodos de webhook
│       └── cita/
│           └── CitaDao.py              # Actualizar: agregar método de confirmación
└── services/
    └── UltraMsgService.py              # Actualizar: agregar método de respuesta
```

---

## 🔧 Implementación Paso a Paso

### Paso 1: Crear Endpoint de Webhook

1. Crear `app/rutas/modulos/recordatorio/webhook_api.py`
2. Implementar endpoint `POST /api/v1/webhooks/ultramsg`
3. Agregar validación de seguridad básica
4. Registrar blueprint en `app/__init__.py`

### Paso 2: Actualizar RecordatorioDao

1. Agregar método `actualizarEstadoMensaje()`
2. Agregar método `buscarPorMessageId()`
3. Agregar columna `recordatorio_estado_mensaje` (opcional)

### Paso 3: Implementar Procesamiento de Eventos

1. Manejar eventos `sent`, `delivered`, `read`, `failed`
2. Actualizar estados en la base de datos
3. Logging de eventos recibidos

### Paso 4: Implementar Procesamiento de Mensajes Entrantes

1. Reconocer confirmaciones y cancelaciones
2. Actualizar estado de citas
3. Enviar respuestas automáticas

### Paso 5: Integración con Sistema de Citas

1. Actualizar `CitaDao` con método de confirmación
2. Notificar a especialistas sobre cancelaciones
3. Registrar interacciones en log

### Paso 6: Configuración en UltraMsg

1. Configurar URL del webhook en el panel de UltraMsg
2. Configurar eventos a recibir
3. Probar webhook con eventos de prueba

---

## 🔐 Seguridad

### Validación de Webhooks
- Verificar firma HMAC si UltraMsg la proporciona
- Validar origen de la petición (IP whitelist opcional)
- Rate limiting en el endpoint
- Logging de intentos sospechosos

### Protección de Datos
- No exponer información sensible en logs
- Validar formato de datos recibidos
- Manejar errores sin exponer detalles internos

---

## 📊 Base de Datos

### Columnas Opcionales a Agregar

```sql
-- Estado del mensaje (sent, delivered, read, failed)
ALTER TABLE recordatorios 
ADD COLUMN IF NOT EXISTS recordatorio_estado_mensaje VARCHAR(20);

-- Fecha de última actualización del estado
ALTER TABLE recordatorios 
ADD COLUMN IF NOT EXISTS recordatorio_estado_actualizado TIMESTAMP;

-- Fecha de lectura (si el mensaje fue leído)
ALTER TABLE recordatorios 
ADD COLUMN IF NOT EXISTS recordatorio_fecha_leido TIMESTAMP;
```

---

## 🧪 Pruebas

### Pruebas Unitarias
- Validación de firma de webhook
- Procesamiento de diferentes tipos de eventos
- Reconocimiento de confirmaciones/cancelaciones
- Actualización de estados

### Pruebas de Integración
- Enviar webhook de prueba desde UltraMsg
- Verificar actualización en base de datos
- Probar confirmación de cita
- Verificar respuesta automática

### Pruebas End-to-End
1. Crear una cita
2. Enviar recordatorio
3. Simular respuesta del paciente
4. Verificar actualización de estado
5. Verificar respuesta automática

---

## 📝 Configuración en UltraMsg

### Pasos en el Panel de UltraMsg

1. **Acceder a Configuración de Webhooks**
   - Panel de UltraMsg → Settings → Webhooks

2. **Configurar URL del Webhook**
   ```
   https://tu-dominio.com/api/v1/webhooks/ultramsg
   ```

3. **Seleccionar Eventos**
   - ✅ Message Sent
   - ✅ Message Delivered
   - ✅ Message Read
   - ✅ Message Failed
   - ✅ Incoming Message

4. **Configurar Secret Key (Opcional)**
   - Generar una clave secreta
   - Configurarla en `ULTRAMSG_WEBHOOK_SECRET`

5. **Probar Webhook**
   - Usar herramienta de prueba de UltraMsg
   - Verificar que se reciben eventos

---

## 🚀 Criterios de Éxito

- [ ] Endpoint de webhook recibe eventos correctamente
- [ ] Estados de mensajes se actualizan en tiempo real
- [ ] Confirmaciones de citas se procesan automáticamente
- [ ] Respuestas automáticas se envían correctamente
- [ ] Estados de citas se actualizan según confirmaciones
- [ ] Especialistas reciben notificaciones de cancelaciones
- [ ] Sistema maneja errores de webhook correctamente
- [ ] Logging completo de eventos recibidos

---

## 📚 Referencias

- [Documentación UltraMsg Webhooks](https://docs.ultramsg.com/api/webhooks)
- [Plan de Implementación por Fases](./PLAN_IMPLEMENTACION_ULTRAMSG_FASES.md)
- [Integración ABM Recordatorios](./INTEGRACION_ULTRAMSG_ABM_RECORDATORIOS.md)

---

## ⏱️ Estimación de Tiempo

- **Desarrollo:** 4-6 horas
- **Pruebas:** 1-2 horas
- **Configuración:** 30 minutos
- **Total:** 5.5-8.5 horas

---

**Estado:** ⚪ Pendiente  
**Prioridad:** BAJA (después de Fase 2)  
**Última actualización:** 2026-01-22

