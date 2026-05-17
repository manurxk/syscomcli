# Próximos Pasos - Implementación de Recordatorios Twilio

## ✅ Estado Actual
- ✅ Código implementado y listo
- ⏳ Pendiente: Configuración y pruebas

---

## 📋 Paso 1: Configurar Credenciales de Twilio

### 1.1 Crear Cuenta en Twilio (si no tienes)

1. Ir a [https://www.twilio.com/](https://www.twilio.com/)
2. Crear cuenta gratuita (trial)
3. Verificar email y teléfono

### 1.2 Obtener Credenciales

1. Iniciar sesión en [Twilio Console](https://console.twilio.com/)
2. En el Dashboard, encontrar:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: Click en "show" para verlo
3. Copiar ambos valores

### 1.3 Configurar WhatsApp Sandbox (Para Pruebas)

1. En Twilio Console, ir a **Messaging > Try it out > Send a WhatsApp message**
2. Verás un número de WhatsApp Sandbox (ej: `+14155238886`)
3. Seguir instrucciones para unir tu número:
   - Enviar el código indicado al número de WhatsApp de Twilio
   - Ejemplo: Enviar `join <código>` al `+1 415 523 8886`
4. Una vez unido, podrás recibir mensajes de prueba

---

## 📋 Paso 2: Configurar Variables de Entorno

### Opción A: Variables de Entorno del Sistema (Recomendado)

```bash
# En Linux/Mac
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_FROM_NUMBER="whatsapp:+14155238886"

# En Windows (PowerShell)
$env:TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:TWILIO_AUTH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:TWILIO_FROM_NUMBER="whatsapp:+14155238886"

# En Windows (CMD)
set TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
set TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
set TWILIO_FROM_NUMBER=whatsapp:+14155238886
```

### Opción B: Archivo .env (Alternativa)

Crear archivo `.env` en la raíz del proyecto:

```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=whatsapp:+14155238886
```

Luego modificar `app/__init__.py` para cargar variables:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de .env

app.config['TWILIO_ACCOUNT_SID'] = os.getenv('TWILIO_ACCOUNT_SID')
app.config['TWILIO_AUTH_TOKEN'] = os.getenv('TWILIO_AUTH_TOKEN')
app.config['TWILIO_FROM_NUMBER'] = os.getenv('TWILIO_FROM_NUMBER', 'whatsapp:+14155238886')
```

**Nota:** Si usas `.env`, necesitarás instalar: `pip install python-dotenv`

### Opción C: Modificar app/__init__.py directamente

Agregar al inicio de `app/__init__.py`:

```python
import os

# Configuración de Twilio
app.config['TWILIO_ACCOUNT_SID'] = os.getenv('TWILIO_ACCOUNT_SID', 'TU_ACCOUNT_SID_AQUI')
app.config['TWILIO_AUTH_TOKEN'] = os.getenv('TWILIO_AUTH_TOKEN', 'TU_AUTH_TOKEN_AQUI')
app.config['TWILIO_FROM_NUMBER'] = os.getenv('TWILIO_FROM_NUMBER', 'whatsapp:+14155238886')
```

---

## 📋 Paso 3: Verificar Instalación de Dependencias

```bash
# Verificar que APScheduler esté instalado
pip show APScheduler

# Si no está instalado:
pip install APScheduler

# Verificar que Twilio esté instalado
pip show twilio

# Si no está instalado:
pip install twilio
```

---

## 📋 Paso 4: Probar la Configuración

### 4.1 Verificar que las Variables se Carguen

Ejecutar en Python (desde la raíz del proyecto):

```python
from app import app
with app.app_context():
    print("TWILIO_ACCOUNT_SID:", app.config.get('TWILIO_ACCOUNT_SID'))
    print("TWILIO_AUTH_TOKEN:", "***" if app.config.get('TWILIO_AUTH_TOKEN') else "NO CONFIGURADO")
    print("TWILIO_FROM_NUMBER:", app.config.get('TWILIO_FROM_NUMBER'))
```

### 4.2 Probar TwilioService

```python
from app import app
from app.services.TwilioService import TwilioService

with app.app_context():
    try:
        twilio = TwilioService()
        print("✅ TwilioService inicializado correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
```

---

## 📋 Paso 5: Crear Cita de Prueba

### 5.1 Crear Cita desde la Interfaz

1. Iniciar la aplicación: `python run.py`
2. Crear una cita de prueba con:
   - **Paciente**: Que tenga teléfono configurado
   - **Fecha**: Al menos 25 horas en el futuro (para que se creen ambos recordatorios)
   - **Hora**: Cualquier hora

### 5.2 Verificar que se Crearon los Recordatorios

Ejecutar en la BD:

```sql
-- Ver recordatorios creados para la cita
SELECT 
    r.id_recordatorio,
    r.recordatorio_tipo,
    r.recordatorio_fecha_programada,
    r.recordatorio_estado,
    r.recordatorio_telefono,
    c.cita_fecha,
    c.cita_hora_inicio
FROM recordatorios r
JOIN citas c ON r.id_cita = c.id_cita
WHERE c.id_cita = <ID_DE_LA_CITA>
ORDER BY r.recordatorio_tipo;
```

Deberías ver 2 recordatorios:
- Uno tipo `24h` programado para 24 horas antes
- Uno tipo `12h` programado para 12 horas antes

---

## 📋 Paso 6: Probar Envío Inmediato (Opcional)

Para probar sin esperar 24 horas, puedes:

### Opción A: Crear Cita con Fecha Cercana

Crear una cita programada para dentro de 11 horas (solo se creará el recordatorio 12h)

### Opción B: Modificar Fecha Programada en BD

```sql
-- Modificar fecha programada para que sea ahora mismo (SOLO PARA PRUEBAS)
UPDATE recordatorios
SET recordatorio_fecha_programada = NOW() - INTERVAL '1 minute'
WHERE id_cita = <ID_DE_LA_CITA>
  AND recordatorio_estado = 'pendiente';
```

### Opción C: Ejecutar Manualmente el Procesador

```python
from app import app
from app.tasks.recordatorio_tasks import procesar_recordatorios_pendientes

with app.app_context():
    resultado = procesar_recordatorios_pendientes()
    print("Resultado:", resultado)
```

---

## 📋 Paso 7: Monitorear Logs

### 7.1 Ver Logs de la Aplicación

Al ejecutar `python run.py`, deberías ver:

```
INFO: ✅ Scheduler iniciado correctamente
INFO: ✅ Tarea programada de recordatorios configurada (cada 10 minutos)
INFO: Recordatorio 24h creado para cita 123 (programado para 2025-01-15 10:00:00)
```

### 7.2 Ver Logs del Procesamiento

Cada 10 minutos, deberías ver:

```
INFO: === INICIANDO PROCESAMIENTO DE RECORDATORIOS ===
INFO: Se encontraron X recordatorios pendientes
INFO: Procesando recordatorio Y (Cita: Z, Tipo: 24h, Paciente: ...)
INFO: ✅ Recordatorio Y enviado exitosamente (SID: SM...)
INFO: === PROCESAMIENTO COMPLETADO ===
```

### 7.3 Verificar Estado en Twilio

1. Ir a [Twilio Console > Messaging > Logs](https://console.twilio.com/us1/develop/sms/logs)
2. Ver los mensajes enviados y su estado

---

## 📋 Paso 8: Verificar Funcionalidad Completa

### Checklist de Verificación

- [ ] Variables de entorno configuradas
- [ ] TwilioService se inicializa sin errores
- [ ] Scheduler se inicia correctamente
- [ ] Al crear cita, se crean recordatorios en BD
- [ ] Los recordatorios tienen fecha_programada correcta
- [ ] El scheduler procesa recordatorios pendientes
- [ ] Los mensajes se envían correctamente
- [ ] Los recordatorios se marcan como "enviado" en BD
- [ ] Al cancelar cita, se cancelan los recordatorios
- [ ] Al actualizar cita, se actualizan los recordatorios

---

## 📋 Paso 9: Ajustes y Optimización

### 9.1 Ajustar Frecuencia del Scheduler

Si quieres cambiar la frecuencia (actualmente 10 minutos), editar `app/tasks/recordatorio_tasks.py`:

```python
scheduler.add_job(
    func=procesar_recordatorios_pendientes,
    trigger='interval',
    minutes=5,  # Cambiar aquí (5, 10, 15, etc.)
    ...
)
```

### 9.2 Ajustar Tipos de Recordatorios

Para cambiar los tipos (actualmente 24h y 12h), modificar `CitaDao.crearRecordatoriosParaCita()`:

```python
# Ejemplo: Agregar recordatorio 48h antes
fecha_48h = cita_datetime - timedelta(hours=48)
if fecha_48h > ahora:
    recordatorio_dao.crearRecordatorio(
        id_cita=id_cita,
        tipo_recordatorio='48h',  # También actualizar CHECK en BD
        ...
    )
```

### 9.3 Personalizar Mensaje

Editar `TwilioService._construir_mensaje_recordatorio()` para cambiar el formato del mensaje.

---

## 🚨 Troubleshooting

### Error: "Configuración de Twilio incompleta"

**Solución:**
- Verificar que las variables de entorno estén configuradas
- Reiniciar la aplicación después de configurar variables

### Error: "WhatsApp falló"

**Solución:**
- Verificar que tu número esté unido al Sandbox
- Verificar formato del número (+595...)
- El sistema intentará SMS automáticamente

### Recordatorios no se crean

**Solución:**
- Verificar que el paciente tenga teléfono en la BD
- Verificar logs para errores específicos
- Verificar que la fecha de la cita sea futura

### Scheduler no ejecuta

**Solución:**
- Verificar logs al iniciar aplicación
- Verificar que APScheduler esté instalado
- Verificar que no haya errores en la configuración

---

## 📚 Documentación Adicional

- **Análisis Completo**: `docs/analisis_implementacion_recordatorios_twilio_whatsapp.md`
- **Guía de Configuración**: `docs/CONFIGURACION_TWILIO_RECORDATORIOS.md`
- **Documentación Twilio**: https://www.twilio.com/docs/whatsapp

---

## ✅ Siguiente Paso Inmediato

**AHORA MISMO debes:**

1. **Crear cuenta en Twilio** (si no tienes)
2. **Obtener credenciales** (Account SID y Auth Token)
3. **Configurar variables de entorno**
4. **Reiniciar la aplicación**
5. **Crear una cita de prueba**

Una vez completados estos pasos, el sistema estará funcionando y enviará recordatorios automáticamente.

---

**Última actualización:** 2025-01-XX
**Estado:** Listo para configuración y pruebas

