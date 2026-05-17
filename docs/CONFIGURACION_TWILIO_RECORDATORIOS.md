# Configuración de Recordatorios con Twilio

## ✅ Implementación Completada

La integración con Twilio para recordatorios automáticos de citas ha sido implementada exitosamente.

## 📋 Componentes Implementados

1. **RecordatorioDao** (`app/dao/modulos/recordatorio/RecordatorioDao.py`)
   - Gestión completa de recordatorios en BD
   - Consulta de recordatorios pendientes
   - Marcado de estado (enviado/fallido)

2. **TwilioService Mejorado** (`app/services/TwilioService.py`)
   - Manejo robusto de errores
   - Fallback automático WhatsApp → SMS
   - Logging detallado

3. **Tarea Programada** (`app/tasks/recordatorio_tasks.py`)
   - Procesa recordatorios cada 10 minutos
   - Reintentos automáticos (máx 3 intentos)
   - Estadísticas de procesamiento

4. **Integración con Citas** (`app/dao/modulos/cita/CitaDao.py`)
   - Creación automática de recordatorios al crear cita
   - Actualización de recordatorios al modificar cita
   - Cancelación de recordatorios al cancelar cita

5. **Scheduler Configurado** (`run.py`)
   - Ejecuta tareas programadas automáticamente
   - Inicia al arrancar la aplicación

## 🔧 Configuración Requerida

### 1. Variables de Entorno

Agregar las siguientes variables de entorno o en el archivo de configuración de Flask:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=whatsapp:+14155238886  # Número de Twilio Sandbox (pruebas)
```

### 2. Obtener Credenciales de Twilio

1. Crear cuenta en [Twilio](https://www.twilio.com/)
2. Ir al [Console de Twilio](https://console.twilio.com/)
3. Obtener:
   - **Account SID**: Se encuentra en el dashboard
   - **Auth Token**: Se encuentra en el dashboard (click en "show")
   - **Número de WhatsApp**: Para pruebas, usar el número Sandbox: `whatsapp:+14155238886`

### 3. Configurar WhatsApp Sandbox (Pruebas)

1. En Twilio Console, ir a **Messaging > Try it out > Send a WhatsApp message**
2. Seguir las instrucciones para unir tu número de WhatsApp al Sandbox
3. Enviar el código de verificación al número indicado
4. Una vez unido, podrás enviar mensajes desde el Sandbox

### 4. Configurar en la Aplicación

#### Opción A: Variables de Entorno (Recomendado)

```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_FROM_NUMBER="whatsapp:+14155238886"
```

#### Opción B: Archivo de Configuración

Agregar en `app/__init__.py` o en un archivo de configuración:

```python
import os

app.config['TWILIO_ACCOUNT_SID'] = os.getenv('TWILIO_ACCOUNT_SID')
app.config['TWILIO_AUTH_TOKEN'] = os.getenv('TWILIO_AUTH_TOKEN')
app.config['TWILIO_FROM_NUMBER'] = os.getenv('TWILIO_FROM_NUMBER', 'whatsapp:+14155238886')
```

## 🚀 Funcionamiento

### Flujo Automático

1. **Al crear una cita:**
   - Se crean automáticamente 2 recordatorios:
     - Recordatorio 24h antes de la cita
     - Recordatorio 12h antes de la cita
   - Solo se crean si la fecha de envío es en el futuro

2. **Al actualizar una cita:**
   - Se cancelan los recordatorios antiguos
   - Se crean nuevos recordatorios con la fecha/hora actualizada

3. **Al cancelar una cita:**
   - Se cancelan todos los recordatorios pendientes

4. **Procesamiento automático:**
   - Cada 10 minutos, el scheduler busca recordatorios pendientes
   - Envía los mensajes vía Twilio (WhatsApp preferido, SMS como fallback)
   - Actualiza el estado en la BD
   - Reintenta hasta 3 veces si falla

### Tipos de Recordatorios

- **24h**: Se envía 24 horas antes de la cita
- **12h**: Se envía 12 horas antes de la cita

## 📊 Monitoreo

### Logs

Los logs incluyen información detallada:

```
INFO: Recordatorio 24h creado para cita 123 (programado para 2025-01-15 10:00:00)
INFO: Procesando recordatorio 456 (Cita: 123, Tipo: 24h, Paciente: Juan Pérez)
INFO: ✅ Recordatorio 456 enviado exitosamente (SID: SMxxxxxxxxxxxxx)
```

### Consultar Recordatorios en BD

```sql
-- Ver recordatorios pendientes
SELECT * FROM recordatorios 
WHERE recordatorio_estado = 'pendiente' 
  AND recordatorio_activo = TRUE
ORDER BY recordatorio_fecha_programada;

-- Ver recordatorios enviados
SELECT * FROM recordatorios 
WHERE recordatorio_estado = 'enviado'
ORDER BY recordatorio_fecha_enviado DESC;

-- Ver recordatorios fallidos
SELECT * FROM recordatorios 
WHERE recordatorio_estado = 'fallido'
ORDER BY recordatorio_fecha_programada;
```

## 🧪 Pruebas

### Probar Manualmente

1. **Crear una cita de prueba:**
   - Crear una cita con fecha/hora en el futuro (más de 24h)
   - Verificar que se crearon los recordatorios en BD

2. **Probar envío inmediato:**
   - Crear una cita con fecha/hora muy cercana (menos de 12h)
   - Verificar que solo se crea el recordatorio 12h
   - El scheduler lo procesará en la próxima ejecución (máx 10 min)

3. **Forzar procesamiento:**
   - Ejecutar manualmente desde Python:
   ```python
   from app.tasks.recordatorio_tasks import procesar_recordatorios_pendientes
   resultado = procesar_recordatorios_pendientes()
   print(resultado)
   ```

### Verificar Estado de Mensajes

```python
from app.services.TwilioService import TwilioService

twilio = TwilioService()
estado = twilio.verificar_estado_mensaje('SMxxxxxxxxxxxxx')
print(estado)
```

## ⚠️ Consideraciones Importantes

1. **Números de Teléfono:**
   - Los números deben tener código de país (+595 para Paraguay)
   - El sistema formatea automáticamente números locales (0981... → +595981...)

2. **Límites de Twilio Sandbox:**
   - Durante pruebas, solo puedes enviar a números verificados en el Sandbox
   - Para producción, necesitarás un número de Twilio verificado

3. **Costos:**
   - Sandbox: Gratis durante período de prueba
   - Producción: ~$0.005 USD por mensaje WhatsApp
   - Ver [análisis de costos](../docs/analisis_implementacion_recordatorios_twilio_whatsapp.md)

4. **Scheduler:**
   - El scheduler se ejecuta en el mismo proceso de la aplicación
   - Para producción, considerar usar un worker separado o cron

## 🔍 Troubleshooting

### Error: "Configuración de Twilio incompleta"

- Verificar que las variables de entorno estén configuradas
- Verificar que los valores sean correctos

### Error: "WhatsApp falló"

- Verificar que el número esté unido al Sandbox
- Verificar que el formato del número sea correcto (+595...)
- El sistema intentará SMS como fallback automáticamente

### Recordatorios no se crean

- Verificar que el paciente tenga teléfono en la BD
- Verificar logs para ver errores específicos
- Verificar que la fecha de la cita sea en el futuro

### Scheduler no ejecuta

- Verificar logs al iniciar la aplicación
- Verificar que APScheduler esté instalado: `pip install APScheduler`
- Verificar que no haya errores en la configuración

## 📝 Próximos Pasos

1. **Configurar variables de entorno**
2. **Probar con una cita de prueba**
3. **Monitorear logs durante las primeras horas**
4. **Ajustar frecuencia del scheduler si es necesario** (actualmente 10 minutos)
5. **Planificar migración a WhatsApp Business API** (ver análisis)

## 📚 Referencias

- [Análisis Completo de Implementación](./analisis_implementacion_recordatorios_twilio_whatsapp.md)
- [Documentación de Twilio](https://www.twilio.com/docs/whatsapp)
- [Documentación de APScheduler](https://apscheduler.readthedocs.io/)

---

**Última actualización:** 2025-01-XX
**Estado:** ✅ Implementación Completa

