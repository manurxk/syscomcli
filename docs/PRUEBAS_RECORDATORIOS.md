# Guía de Pruebas - Sistema de Recordatorios

## 🧪 Pasos para Probar el Sistema Completo

### Paso 1: Verificar que se Crean Recordatorios en BD

#### 1.1 Crear una Cita de Prueba

1. Acceder a `/cita/cita-index`
2. Click en "Nueva Cita"
3. Crear una cita con:
   - **Paciente**: Que tenga teléfono configurado
   - **Fecha**: Al menos 25 horas en el futuro (para que se creen ambos recordatorios: 24h y 12h)
   - **Hora**: Cualquier hora
   - Guardar la cita

#### 1.2 Verificar en la Base de Datos

Ejecutar en PostgreSQL:

```sql
-- Ver todos los recordatorios creados
SELECT 
    r.id_recordatorio,
    r.id_cita,
    r.recordatorio_tipo,
    r.recordatorio_fecha_programada,
    r.recordatorio_estado,
    r.recordatorio_telefono,
    r.recordatorio_paciente_nombre,
    c.cita_fecha,
    c.cita_hora_inicio,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre
FROM recordatorios r
JOIN citas c ON r.id_cita = c.id_cita
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
WHERE c.id_cita = <ID_DE_LA_CITA>
ORDER BY r.recordatorio_tipo;
```

**Resultado esperado:**
- Deberías ver 2 recordatorios:
  - Uno tipo `24h` programado para 24 horas antes de la cita
  - Uno tipo `12h` programado para 12 horas antes de la cita
- Ambos con estado `pendiente`

#### 1.3 Verificar desde la Interfaz

1. Acceder a `/recordatorio/recordatorio-index`
2. Click en "Verificar en BD"
3. Ingresar el ID de la cita creada
4. Verificar que muestra:
   - Total de recordatorios: 2
   - Estado: Pendientes: 2

---

### Paso 2: Probar el Botón "Procesar Ahora"

#### 2.1 Preparar Recordatorio para Envío

**Opción A: Esperar a que llegue la fecha programada**
- Esperar hasta que `recordatorio_fecha_programada <= NOW()`

**Opción B: Modificar fecha programada (SOLO PARA PRUEBAS)**

```sql
-- Modificar fecha programada para que sea ahora mismo
UPDATE recordatorios
SET recordatorio_fecha_programada = NOW() - INTERVAL '1 minute'
WHERE id_cita = <ID_DE_LA_CITA>
  AND recordatorio_estado = 'pendiente'
  AND recordatorio_activo = TRUE;
```

#### 2.2 Ejecutar Procesamiento Manual

1. Acceder a `/recordatorio/recordatorio-index`
2. Verificar que hay recordatorios pendientes en la tabla
3. Click en "Procesar Ahora"
4. Confirmar el procesamiento
5. Esperar a que termine

**Resultado esperado:**
- Mensaje de éxito con estadísticas:
  - Total procesado: X
  - Enviados: Y
  - Fallidos: Z
- La tabla se recarga automáticamente
- Los recordatorios procesados cambian de estado a "enviado" o "fallido"

#### 2.3 Verificar Estado en BD

```sql
-- Ver estado actualizado
SELECT 
    id_recordatorio,
    recordatorio_tipo,
    recordatorio_estado,
    recordatorio_fecha_enviado,
    recordatorio_twilio_sid,
    recordatorio_intentos,
    recordatorio_error
FROM recordatorios
WHERE id_cita = <ID_DE_LA_CITA>
ORDER BY recordatorio_tipo;
```

**Resultado esperado:**
- Estado cambiado a `enviado` (si Twilio está configurado) o `fallido`
- `recordatorio_fecha_enviado` con timestamp
- `recordatorio_twilio_sid` con ID del mensaje (si se envió)

---

### Paso 3: Verificar Integración con Twilio

#### 3.1 Verificar Configuración

```python
# Desde Python (en la raíz del proyecto)
from app import app
from app.services.TwilioService import TwilioService

with app.app_context():
    try:
        twilio = TwilioService()
        print("✅ TwilioService inicializado correctamente")
        print(f"Account SID: {app.config.get('TWILIO_ACCOUNT_SID', 'NO CONFIGURADO')[:10]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
```

#### 3.2 Probar Envío Manual

```python
from app import app
from app.services.TwilioService import TwilioService
from datetime import datetime, timedelta

with app.app_context():
    twilio = TwilioService()
    
    # Usar tu número de WhatsApp unido al Sandbox
    success, message_sid, error = twilio.enviar_recordatorio_cita(
        telefono="+595981123456",  # Tu número verificado
        nombre_paciente="Juan Pérez",
        cita_fecha=datetime.now() + timedelta(days=1),
        cita_hora=datetime.now().time(),
        especialista="Dr. Carlos González",
        especialidad="Cardiología",
        motivo="Control de presión"
    )
    
    if success:
        print(f"✅ Mensaje enviado. SID: {message_sid}")
    else:
        print(f"❌ Error: {error}")
```

---

### Paso 4: Verificar en Vista de Citas

#### 4.1 Ver Columna de Recordatorios

1. Acceder a `/cita/cita-index`
2. Verificar que aparece la columna "Recordatorios"
3. Esperar unos segundos a que se carguen los estados
4. Verificar que aparecen badges:
   - ✅ Verde para enviados
   - ⏳ Amarillo para pendientes
   - ❌ Rojo para fallidos

#### 4.2 Ver Recordatorios de una Cita

1. En la tabla de citas, click en "Ver" en la columna Recordatorios
2. Debería redirigir a `/recordatorio/recordatorio-index?id_cita=X`
3. Verificar que la tabla muestra solo los recordatorios de esa cita

---

## 🔍 Consultas SQL Útiles

### Ver Todos los Recordatorios

```sql
SELECT 
    r.id_recordatorio,
    r.id_cita,
    r.recordatorio_tipo,
    r.recordatorio_fecha_programada,
    r.recordatorio_fecha_enviado,
    r.recordatorio_estado,
    r.recordatorio_intentos,
    r.recordatorio_twilio_sid,
    c.cita_fecha,
    c.cita_hora_inicio,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente
FROM recordatorios r
JOIN citas c ON r.id_cita = c.id_cita
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
WHERE r.recordatorio_activo = TRUE
ORDER BY r.recordatorio_fecha_programada DESC;
```

### Ver Recordatorios Pendientes

```sql
SELECT * FROM recordatorios
WHERE recordatorio_estado = 'pendiente'
  AND recordatorio_activo = TRUE
  AND recordatorio_fecha_programada <= NOW()
ORDER BY recordatorio_fecha_programada;
```

### Ver Recordatorios por Cita

```sql
SELECT * FROM recordatorios
WHERE id_cita = <ID_CITA>
  AND recordatorio_activo = TRUE
ORDER BY recordatorio_tipo;
```

### Estadísticas de Recordatorios

```sql
SELECT 
    recordatorio_estado,
    COUNT(*) as cantidad
FROM recordatorios
WHERE recordatorio_activo = TRUE
GROUP BY recordatorio_estado;
```

---

## ✅ Checklist de Verificación

### Creación de Recordatorios
- [ ] Al crear cita, se crean 2 recordatorios en BD
- [ ] Fechas programadas son correctas (24h y 12h antes)
- [ ] Estado inicial es "pendiente"
- [ ] Teléfono y nombre del paciente están guardados

### Procesamiento Manual
- [ ] Botón "Procesar Ahora" funciona
- [ ] Muestra estadísticas correctas
- [ ] Actualiza estado en BD
- [ ] Recarga la tabla automáticamente

### Verificación en BD
- [ ] Botón "Verificar en BD" funciona
- [ ] Muestra información correcta
- [ ] Muestra resumen de estados

### Integración con Citas
- [ ] Columna de recordatorios aparece
- [ ] Se cargan los estados automáticamente
- [ ] Botón "Ver" redirige correctamente

### Twilio (si está configurado)
- [ ] Se envían mensajes correctamente
- [ ] Se guarda Twilio SID
- [ ] Fallback a SMS funciona si WhatsApp falla

---

## 🐛 Troubleshooting

### No se crean recordatorios al crear cita

**Verificar:**
1. El paciente tiene teléfono en la BD
2. La fecha de la cita es futura (más de 12 horas)
3. Revisar logs de la aplicación
4. Verificar que `crearRecordatoriosParaCita()` se ejecuta

**Query de diagnóstico:**
```sql
-- Verificar si el paciente tiene teléfono
SELECT 
    p.id_paciente,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS nombre,
    pp.per_telefono
FROM pacientes p
JOIN personas pp ON p.id_persona = pp.id_persona
WHERE p.id_paciente = <ID_PACIENTE>;
```

### Botón "Procesar Ahora" no funciona

**Verificar:**
1. Endpoint `/api/v1/recordatorios/procesar` existe
2. Permisos de usuario (ADMINISTRADOR o RECEPCIONISTA)
3. Revisar consola del navegador para errores JavaScript
4. Revisar logs del servidor

### No hay recordatorios pendientes

**Verificar:**
```sql
-- Ver si hay recordatorios pendientes
SELECT COUNT(*) 
FROM recordatorios
WHERE recordatorio_estado = 'pendiente'
  AND recordatorio_activo = TRUE
  AND recordatorio_fecha_programada <= NOW();
```

Si no hay, puede ser que:
- Todos ya fueron procesados
- Las fechas programadas son futuras
- Los recordatorios fueron cancelados

---

## 📝 Notas Importantes

1. **Fechas Programadas**: Los recordatorios solo se procesan si `fecha_programada <= NOW()`

2. **Límite de Procesamiento**: Se procesan máximo 100 recordatorios por ejecución

3. **Reintentos**: Máximo 3 intentos antes de marcar como "fallido"

4. **Twilio Sandbox**: Solo puedes enviar a números verificados en el Sandbox

5. **Logs**: Revisar logs de la aplicación para ver detalles del procesamiento

---

**Última actualización:** 2025-01-XX

