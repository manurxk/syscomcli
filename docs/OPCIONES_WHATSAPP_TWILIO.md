# Opciones para Enviar WhatsApp con Twilio

## 📱 Opciones Disponibles

### 1. **Twilio Sandbox (Actual - Solo Pruebas)** ⚠️

**Características:**
- ✅ Gratis durante período de prueba
- ✅ Fácil de configurar
- ❌ Solo puedes enviar a números que hayas unido al Sandbox
- ❌ Número fijo de Twilio: `+14155238886` (no puedes usar tu número)
- ❌ Limitado a pruebas

**Cuándo usar:** Solo para desarrollo y pruebas iniciales

---

### 2. **Twilio WhatsApp API con Número Propio (Producción)** ✅ RECOMENDADO

**Características:**
- ✅ Puedes usar tu propio número de teléfono
- ✅ Enviar a cualquier número de WhatsApp
- ✅ Sin límites de números verificados
- ⚠️ Requiere verificación de número con Meta (Facebook)
- ⚠️ Tiene costo: ~$0.005 USD por mensaje

**Proceso de Configuración:**

#### Paso 1: Obtener Número de Twilio
1. En Twilio Console, ir a **Phone Numbers > Buy a number**
2. Comprar un número (costo: ~$1 USD/mes)
3. O usar un número que ya tengas

#### Paso 2: Solicitar Acceso a WhatsApp Business API
1. En Twilio Console, ir a **Messaging > Settings > WhatsApp Senders**
2. Click en **"Request WhatsApp Access"**
3. Completar formulario:
   - Nombre de negocio
   - Descripción del uso
   - Tipo de mensajes que enviarás
   - Volumen estimado
4. Twilio revisará tu solicitud (puede tardar días/semanas)

#### Paso 3: Verificar Número con Meta
1. Una vez aprobado, Twilio te guiará para verificar tu número
2. Necesitarás:
   - Cuenta de Meta Business
   - Verificar el número con Meta
   - Conectar con Twilio

#### Paso 4: Configurar en la Aplicación
```python
# Usar tu número verificado en lugar del Sandbox
TWILIO_FROM_NUMBER="whatsapp:+595981123456"  # Tu número verificado
```

**Tiempo estimado:** 1-2 semanas para aprobación

---

### 3. **WhatsApp Business API Directo (Meta)** 🏆 MEJOR OPCIÓN

**Características:**
- ✅ Precios más competitivos (~$0.005-0.01 USD/mensaje)
- ✅ Integración nativa con WhatsApp
- ✅ Mejor experiencia de usuario
- ✅ Sin intermediarios
- ⚠️ Requiere proceso de verificación más complejo
- ⚠️ Necesita Meta Business Account

**Proceso de Configuración:**

#### Paso 1: Crear Meta Business Account
1. Ir a [business.facebook.com](https://business.facebook.com)
2. Crear cuenta de negocio
3. Verificar identidad del negocio

#### Paso 2: Configurar WhatsApp Business API
1. En Meta Business Manager, ir a **WhatsApp > API Setup**
2. Seguir el proceso de configuración
3. Obtener:
   - Access Token
   - Phone Number ID
   - Business Account ID

#### Paso 3: Verificar Número
1. Verificar tu número de teléfono con Meta
2. Conectar con WhatsApp Business API

#### Paso 4: Implementar en la Aplicación
Necesitarías crear un `WhatsAppService` similar a `TwilioService`:

```python
# app/services/WhatsAppService.py
import requests

class WhatsAppService:
    def __init__(self):
        self.access_token = app.config.get('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = app.config.get('WHATSAPP_PHONE_NUMBER_ID')
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
    
    def enviar_recordatorio_cita(self, telefono, nombre_paciente, ...):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': telefono,
            'type': 'text',
            'text': {'body': mensaje}
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        return response.json()
```

**Tiempo estimado:** 1-3 semanas para aprobación completa

---

## 🔄 Comparación de Opciones

| Característica | Twilio Sandbox | Twilio WhatsApp API | WhatsApp Business API |
|----------------|----------------|---------------------|----------------------|
| **Costo** | Gratis (pruebas) | ~$0.005/mensaje | ~$0.005-0.01/mensaje |
| **Tu número** | ❌ No | ✅ Sí | ✅ Sí |
| **Límite destinatarios** | Solo verificados | Sin límite | Sin límite |
| **Tiempo setup** | 5 minutos | 1-2 semanas | 1-3 semanas |
| **Complejidad** | Muy fácil | Media | Media-Alta |
| **Para producción** | ❌ No | ✅ Sí | ✅ Sí |

---

## 💡 Recomendación

### Para AHORA (Desarrollo/Pruebas):
✅ **Usar Twilio Sandbox**
- Configuración rápida
- Gratis
- Suficiente para probar la funcionalidad

### Para PRODUCCIÓN (Futuro):
✅ **Migrar a WhatsApp Business API directo**
- Mejor precio
- Mejor experiencia
- Más control

### Alternativa Intermedia:
✅ **Twilio WhatsApp API con número propio**
- Si ya tienes cuenta Twilio
- Proceso más simple que Meta directo
- Buena opción intermedia

---

## 🚀 Plan de Migración Sugerido

### Fase 1: Ahora (Semana 1)
- ✅ Usar Twilio Sandbox para pruebas
- ✅ Verificar que todo funciona
- ✅ Probar con números de prueba

### Fase 2: Solicitar Acceso (Semana 2-3)
- 📝 Solicitar acceso a WhatsApp Business API (Meta)
- 📝 Mientras tanto, seguir usando Sandbox

### Fase 3: Migración (Semana 4)
- 🔄 Implementar `WhatsAppService`
- 🔄 Crear abstracción para cambiar entre servicios
- 🔄 Migrar gradualmente

---

## 📝 Código para Abstracción (Futuro)

Para facilitar la migración, podrías crear una interfaz:

```python
# app/services/notification_service.py
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def enviar_recordatorio_cita(self, telefono, nombre_paciente, ...):
        pass

# app/services/TwilioService.py
class TwilioService(NotificationService):
    def enviar_recordatorio_cita(self, ...):
        # Implementación actual

# app/services/WhatsAppService.py  
class WhatsAppService(NotificationService):
    def enviar_recordatorio_cita(self, ...):
        # Implementación nueva

# app/tasks/recordatorio_tasks.py
# Usar la interfaz en lugar de TwilioService directamente
service = TwilioService() if config.get('USE_TWILIO') else WhatsAppService()
```

---

## ⚠️ Importante

**NO puedes usar tu número personal de WhatsApp directamente con Twilio Sandbox.**

Para usar tu número necesitas:
1. **Twilio WhatsApp API**: Solicitar acceso y verificar número
2. **WhatsApp Business API**: Configurar cuenta de negocio y verificar

Ambas opciones requieren proceso de aprobación y verificación.

---

## 📚 Recursos

- [Twilio WhatsApp Setup](https://www.twilio.com/docs/whatsapp)
- [Meta WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Twilio WhatsApp Pricing](https://www.twilio.com/whatsapp/pricing)

---

**Recomendación Final:**
1. **Ahora**: Usa Twilio Sandbox para probar
2. **Próximas semanas**: Solicita acceso a WhatsApp Business API
3. **Producción**: Migra a WhatsApp Business API directo

