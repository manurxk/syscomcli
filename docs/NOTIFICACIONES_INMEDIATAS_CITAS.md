# Notificaciones Inmediatas de Citas - Implementación Completada

**Fecha:** 2026-01-22  
**Sistema:** Sysclin - Sistema de Gestión Médica  
**Funcionalidad:** Envío de notificaciones WhatsApp inmediatas al crear/editar citas

---

## 📋 Resumen

Se ha implementado la funcionalidad para enviar notificaciones inmediatas por WhatsApp cuando se crea o edita una cita médica. El usuario puede activar/desactivar esta funcionalidad mediante un checkbox en el formulario.

---

## ✅ Funcionalidades Implementadas

### 1. Checkbox en Formulario de Citas

**Ubicación:** `app/rutas/modulos/cita/templates/cita-agregar.html`

- ✅ Checkbox "Enviar notificación inmediata al paciente"
- ✅ Activado por defecto
- ✅ Texto dinámico que cambia entre "creada" y "actualizada" según el modo
- ✅ Información sobre recordatorios automáticos (24h y 12h)

**Características:**
- El checkbox está marcado por defecto
- Se puede desmarcar si no se desea enviar la notificación
- Muestra información sobre los recordatorios automáticos

### 2. Integración en API de Citas

**Archivo:** `app/rutas/modulos/cita/cita_api.py`

#### Endpoint: `POST /api/v1/citas` (Crear Cita)
- ✅ Verifica si `enviar_notificacion` está marcado
- ✅ Obtiene datos completos de la cita y paciente
- ✅ Envía notificación inmediata si está habilitado
- ✅ Retorna información sobre el envío de notificación

#### Endpoint: `PUT /api/v1/citas/<id>` (Editar Cita)
- ✅ Verifica si `enviar_notificacion` está marcado
- ✅ Obtiene datos actualizados de la cita y paciente
- ✅ Envía notificación inmediata si está habilitado
- ✅ Retorna información sobre el envío de notificación

### 3. Nuevo Método en UltraMsgService

**Archivo:** `app/services/UltraMsgService.py`

**Método:** `enviar_notificacion_cita_creada_editada()`

**Parámetros:**
- `telefono`: Número del paciente
- `nombre_paciente`: Nombre del paciente
- `cita_fecha`: Fecha de la cita
- `cita_hora`: Hora de la cita
- `especialista`: Nombre del especialista
- `especialidad`: Nombre de la especialidad
- `nombre_clinica`: Nombre de la clínica (configurable)
- `es_edicion`: True si es edición, False si es creación

**Características:**
- ✅ Incluye reintentos automáticos (Fase 2)
- ✅ Rate limiting (Fase 2)
- ✅ Manejo de errores robusto
- ✅ Mensaje personalizado según si es creación o edición

### 4. Mensaje de Notificación

**Formato del mensaje:**

```
✅ Su Cita ha sido CREADA

Hola [Nombre del Paciente],

Su cita médica ha sido creada con los siguientes detalles:

📅 Fecha: [DD/MM/YYYY]
🕐 Hora: [HH:MM]
👨‍⚕️ Profesional: [Nombre del Especialista]
🩺 Especialidad: [Nombre de la Especialidad]
🏥 Clínica: [Nombre de la Clínica]

Recuerde que recibirá recordatorios automáticos 24 horas y 12 horas antes de su cita.

¡Gracias por confiar en nosotros!
```

**Para edición:**
- El emoji cambia a ✏️
- El texto dice "actualizada" en lugar de "creada"

### 5. Configuración de Nombre de Clínica

**Archivo:** `app/__init__.py`

Se agregó configuración para el nombre de la clínica:

```python
app.config['NOMBRE_CLINICA'] = os.getenv('NOMBRE_CLINICA', 'Sysclin')
```

**Configuración:**
- Variable de entorno: `NOMBRE_CLINICA`
- Valor por defecto: `"Sysclin"`
- Se puede cambiar en variables de entorno o directamente en el código

---

## 🔄 Flujo Completo

### Al Crear una Cita:

1. Usuario completa el formulario de cita
2. Usuario puede marcar/desmarcar "Enviar notificación inmediata"
3. Usuario hace clic en "Guardar Cita"
4. Sistema guarda la cita en la base de datos
5. **Si está marcado el checkbox:**
   - Sistema obtiene teléfono del paciente
   - Sistema construye mensaje de notificación
   - Sistema envía mensaje vía UltraMsg
   - Sistema registra resultado (éxito o error)
6. Sistema retorna respuesta con información de notificación
7. **Además:** Sistema crea recordatorios automáticos (24h y 12h antes)

### Al Editar una Cita:

1. Usuario edita los datos de la cita
2. Usuario puede marcar/desmarcar "Enviar notificación inmediata"
3. Usuario hace clic en "Actualizar Cita"
4. Sistema actualiza la cita en la base de datos
5. **Si está marcado el checkbox:**
   - Sistema obtiene teléfono del paciente
   - Sistema construye mensaje de notificación (con texto "actualizada")
   - Sistema envía mensaje vía UltraMsg
   - Sistema registra resultado
6. Sistema retorna respuesta con información de notificación
7. **Los recordatorios automáticos se mantienen** (se actualizan si cambia la fecha/hora)

---

## 📱 Ejemplo de Mensaje Enviado

**Cuando se crea una cita:**
```
✅ Su Cita ha sido CREADA

Hola Juan Pérez,

Su cita médica ha sido creada con los siguientes detalles:

📅 Fecha: 25/01/2026
🕐 Hora: 10:00
👨‍⚕️ Profesional: Dr. Carlos González
🩺 Especialidad: Cardiología
🏥 Clínica: Sysclin

Recuerde que recibirá recordatorios automáticos 24 horas y 12 horas antes de su cita.

¡Gracias por confiar en nosotros!
```

**Cuando se edita una cita:**
```
✏️ Su Cita ha sido ACTUALIZADA

Hola Juan Pérez,

Su cita médica ha sido actualizada con los siguientes detalles:

📅 Fecha: 26/01/2026
🕐 Hora: 14:00
👨‍⚕️ Profesional: Dr. Carlos González
🩺 Especialidad: Cardiología
🏥 Clínica: Sysclin

Recuerde que recibirá recordatorios automáticos 24 horas y 12 horas antes de su cita.

¡Gracias por confiar en nosotros!
```

---

## ⚙️ Configuración

### 1. Nombre de la Clínica

**Opción A: Variable de entorno**
```bash
export NOMBRE_CLINICA="Tu Nombre de Clínica"
```

**Opción B: Editar directamente en `app/__init__.py`**
```python
app.config['NOMBRE_CLINICA'] = 'Tu Nombre de Clínica'
```

### 2. Habilitar/Deshabilitar por Defecto

Para cambiar el estado por defecto del checkbox, editar `cita-agregar.html`:

```html
<!-- Marcado por defecto -->
<input class="form-check-input" type="checkbox" id="chkEnviarNotificacion" checked>

<!-- Desmarcado por defecto -->
<input class="form-check-input" type="checkbox" id="chkEnviarNotificacion">
```

---

## 🔍 Validaciones y Manejo de Errores

### Validaciones Implementadas:

1. **Teléfono del paciente:**
   - Si el paciente no tiene teléfono registrado, no se envía notificación
   - Se registra un warning en los logs
   - La cita se guarda normalmente

2. **Configuración de UltraMsg:**
   - Si UltraMsg no está configurado, no se envía notificación
   - Se registra un error en los logs
   - La cita se guarda normalmente

3. **Errores de envío:**
   - Si falla el envío, se registra el error
   - La cita se guarda normalmente
   - El usuario recibe información sobre el error en la respuesta

### Respuestas de la API:

**Éxito con notificación:**
```json
{
  "success": true,
  "data": {
    "id_cita": 123,
    "mensaje": "Cita creada exitosamente. Notificación enviada al paciente.",
    "notificacion_enviada": true
  }
}
```

**Éxito sin notificación (checkbox desmarcado):**
```json
{
  "success": true,
  "data": {
    "id_cita": 123,
    "mensaje": "Cita creada exitosamente",
    "notificacion_enviada": false
  }
}
```

**Éxito pero notificación falló:**
```json
{
  "success": true,
  "data": {
    "id_cita": 123,
    "mensaje": "Cita creada exitosamente. Notificación no enviada: [error]",
    "notificacion_enviada": false
  }
}
```

---

## 📊 Integración con Recordatorios Automáticos

### Recordatorios Automáticos (24h y 12h)

Los recordatorios automáticos **se mantienen independientes** de las notificaciones inmediatas:

- ✅ Se crean automáticamente al crear una cita
- ✅ Se actualizan automáticamente si se edita la fecha/hora de la cita
- ✅ Se envían 24 horas antes de la cita
- ✅ Se envían 12 horas antes de la cita
- ✅ Funcionan independientemente del checkbox de notificación inmediata

### Flujo Completo de Notificaciones:

```
┌─────────────────────────────────────────────────────────┐
│  Cita Creada/Editada                                    │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────────┐  ┌──────────────────────┐
│ Notificación     │  │ Recordatorios       │
│ Inmediata        │  │ Automáticos          │
│ (Si checkbox     │  │ (Siempre activos)    │
│  marcado)        │  │                      │
└──────────────────┘  └──────────────────────┘
        │                     │
        │                     ├─── 24h antes
        │                     │
        │                     └─── 12h antes
        │
        ▼
   WhatsApp del
      Paciente
```

---

## 🧪 Pruebas

### Probar Notificación Inmediata:

1. **Crear una cita:**
   - Ir a "Registrar Nueva Cita"
   - Completar todos los campos
   - Asegurarse de que el checkbox "Enviar notificación inmediata" esté marcado
   - Seleccionar un paciente que tenga teléfono registrado
   - Guardar la cita
   - Verificar que el paciente reciba el mensaje en WhatsApp

2. **Editar una cita:**
   - Ir a editar una cita existente
   - Modificar algún campo (fecha, hora, etc.)
   - Asegurarse de que el checkbox esté marcado
   - Guardar cambios
   - Verificar que el paciente reciba el mensaje de actualización

3. **Desactivar notificación:**
   - Desmarcar el checkbox
   - Guardar la cita
   - Verificar que NO se envíe notificación
   - Verificar que los recordatorios automáticos se mantengan

---

## 📝 Archivos Modificados

1. **`app/rutas/modulos/cita/templates/cita-agregar.html`**
   - Agregado checkbox de notificación
   - Agregado campo `enviar_notificacion` en datos del formulario
   - Agregada lógica para cambiar texto según modo (crear/editar)

2. **`app/rutas/modulos/cita/cita_api.py`**
   - Modificado `addCita()` para enviar notificación
   - Modificado `updateCita()` para enviar notificación
   - Agregada importación de `UltraMsgService`

3. **`app/services/UltraMsgService.py`**
   - Agregado método `enviar_notificacion_cita_creada_editada()`
   - Agregado método `_construir_mensaje_cita_creada_editada()`

4. **`app/__init__.py`**
   - Agregada configuración `NOMBRE_CLINICA`

---

## ✅ Checklist de Funcionalidad

- [x] Checkbox agregado en formulario de citas
- [x] Checkbox marcado por defecto
- [x] Texto dinámico (creada/actualizada)
- [x] Campo `enviar_notificacion` enviado en request
- [x] API verifica checkbox antes de enviar
- [x] Obtención de teléfono del paciente
- [x] Construcción de mensaje personalizado
- [x] Envío vía UltraMsg con reintentos
- [x] Manejo de errores robusto
- [x] Logging de operaciones
- [x] Respuesta incluye información de notificación
- [x] Recordatorios automáticos se mantienen independientes
- [x] Configuración de nombre de clínica

---

## 🎯 Beneficios

1. **Comunicación Inmediata:**
   - El paciente recibe confirmación instantánea
   - Reduce llamadas de confirmación
   - Mejora la experiencia del paciente

2. **Flexibilidad:**
   - El usuario puede decidir si enviar o no
   - Útil para citas de prueba o internas
   - No interfiere con el flujo normal

3. **Información Completa:**
   - El paciente recibe todos los detalles de la cita
   - Incluye recordatorio de recordatorios automáticos
   - Mensaje profesional y claro

4. **Integración Perfecta:**
   - Funciona junto con recordatorios automáticos
   - Usa la misma infraestructura de UltraMsg
   - Aprovecha todas las mejoras de Fase 2 (reintentos, rate limiting, etc.)

---

## 📚 Referencias

- [Documentación UltraMsg](../GUIA_CONFIGURACION_ULTRAMSG_PASO_A_PASO.md)
- [Fase 2: Mejoras y Optimizaciones](../FASE2_MEJORAS_COMPLETADAS.md)
- [Sistema de Recordatorios](../ANALISIS_REQUISITOS_ULTRAMSG.md)

---

**Documento creado:** 2026-01-22  
**Última actualización:** 2026-01-22  
**Versión:** 1.0

