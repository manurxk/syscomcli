# Nota: Número de WhatsApp Business

**Fecha:** 2026-01-22  
**Sistema:** Sysclin - Sistema de Gestión Médica

---

## 📱 Número de WhatsApp Business Configurado

**Número:** `0991301397`

Este es el número de WhatsApp Business que está conectado a tu instancia de UltraMsg y desde el cual se enviarán todos los mensajes de recordatorios y notificaciones.

---

## 🔄 Flujo de Envío

```
┌─────────────────────────────────────────────────────────┐
│  Sistema Sysclin                                        │
│  (app/services/UltraMsgService.py)                     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ Envía mensaje vía API
                   ▼
┌─────────────────────────────────────────────────────────┐
│  UltraMsg API                                           │
│  (https://api.ultramsg.com)                             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ Procesa y envía
                   ▼
┌─────────────────────────────────────────────────────────┐
│  WhatsApp Business                                      │
│  Número: 0991301397                                     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ Entrega mensaje
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Paciente                                               │
│  (Número de teléfono del paciente)                      │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Ejemplo de Uso

Cuando el sistema envía un recordatorio:

1. **Origen:** `0991301397` (tu número de WhatsApp Business)
2. **Destino:** Número del paciente (ej: `0981123456`)
3. **Mensaje:** Recordatorio de cita médica

El paciente recibirá el mensaje como si viniera del número `0991301397`.

---

## ⚠️ Importante

- ✅ Este número (`0991301397`) es el que está conectado a UltraMsg
- ✅ Todos los mensajes se enviarán desde este número
- ✅ Los pacientes verán este número como remitente
- ✅ Este número debe estar activo y conectado a WhatsApp Business
- ✅ No necesitas configurar este número en el código, UltraMsg lo maneja automáticamente

---

## 🔧 Configuración

El número `0991301397` está configurado en tu instancia de UltraMsg. No necesitas hacer nada adicional en el código del sistema.

El sistema solo necesita:
- `ULTRAMSG_INSTANCE_ID`: ID de tu instancia
- `ULTRAMSG_TOKEN`: Token de autenticación
- `ULTRAMSG_API_URL`: URL de la API

El número de origen se maneja automáticamente por UltraMsg según la instancia configurada.

---

## 📞 Números de Destino

Los números de destino son los teléfonos de los pacientes registrados en el sistema. El sistema:

1. Obtiene el número del paciente desde la base de datos
2. Lo formatea automáticamente al formato internacional (ej: `0981123456` → `595981123456`)
3. Envía el mensaje desde `0991301397` hacia ese número

---

**Documento creado:** 2026-01-22  
**Última actualización:** 2026-01-22  
**Versión:** 1.0

