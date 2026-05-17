# Análisis de Errores - Sistema de Recordatorios

**Fecha:** 22 de Enero 2026  
**Estado:** Errores identificados y soluciones propuestas

---

## 🔴 ERRORES IDENTIFICADOS

### 1. **Error de Contexto de Aplicación Flask**
**Síntoma:**
```
RuntimeError: Working outside of application context.
```

**Causa:**
- La función `procesar_recordatorios_pendientes()` se ejecuta desde APScheduler fuera del contexto de Flask
- Intenta usar `app.logger` sin tener acceso al contexto de la aplicación

**Ubicación:**
- `app/tasks/recordatorio_tasks.py:21`
- `run.py:17` (al configurar el scheduler)

**Solución:**
- Envolver el código de la función con `with app.app_context():`
- O pasar la instancia de `app` como parámetro al scheduler

---

### 2. **Error de Columna `recordatorio_activo` No Existe**
**Síntoma:**
```
ERROR: no existe la columna «recordatorio_activo»
LINE 12: AND recordatorio_activo = TRUE
```

**Causa:**
- El código asume que existe la columna `recordatorio_activo` en la tabla `recordatorios`
- La estructura real de la BD (según `04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql`) NO incluye esta columna
- Solo el esquema en `bdsysl.sql` la incluye, pero parece que la BD real usa el otro esquema

**Ubicaciones afectadas:**
- `RecordatorioDao.py:31` - INSERT usa `recordatorio_activo`
- `RecordatorioDao.py:98` - SELECT usa `recordatorio_activo = TRUE`
- `RecordatorioDao.py:278, 281` - UPDATE usa `recordatorio_activo`
- `RecordatorioDao.py:327` - SELECT usa `recordatorio_activo = TRUE`
- `recordatorio_api.py:71` - SELECT usa `recordatorio_activo = TRUE`
- `recordatorio_api.py:398` - SELECT usa `recordatorio_activo = TRUE`

**Opciones de Solución:**

**Opción A:** Agregar la columna a la BD (recomendado)
```sql
ALTER TABLE recordatorios 
ADD COLUMN IF NOT EXISTS recordatorio_activo BOOLEAN DEFAULT TRUE;
```

**Opción B:** Eliminar todas las referencias a `recordatorio_activo` del código
- Usar solo `recordatorio_estado` para filtrar (excluir 'cancelado')
- Modificar `cancelarRecordatoriosCita()` para solo cambiar el estado

**Recomendación:** Opción A, ya que permite soft-delete y es más flexible.

---

### 3. **Error 400 en Endpoint `/api/v1/recordatorios/procesar`**
**Síntoma:**
```
POST /api/v1/recordatorios/procesar HTTP/1.1" 400
```

**Causa probable:**
- La función `procesar_recordatorios_pendientes()` falla por el error de contexto
- O falla por el error de columna `recordatorio_activo`
- El endpoint retorna 400 en lugar de 500 porque la excepción se captura pero no se maneja correctamente

**Ubicación:**
- `recordatorio_api.py:432-456`

**Solución:**
- Corregir los errores 1 y 2 primero
- Mejorar el manejo de errores en el endpoint

---

## ✅ PLAN DE CORRECCIÓN

### Paso 1: Corregir Contexto de Aplicación
1. Modificar `recordatorio_tasks.py` para usar contexto de aplicación
2. Modificar `run.py` para configurar el scheduler con contexto

### Paso 2: Resolver Columna `recordatorio_activo`
1. Verificar estructura real de la tabla en BD
2. Si no existe, crear script SQL para agregarla
3. O adaptar código para no usarla

### Paso 3: Mejorar Manejo de Errores
1. Mejorar logging en endpoints
2. Retornar códigos HTTP correctos (500 para errores internos)

---

## 📋 ESTRUCTURA DE TABLA ESPERADA vs REAL

### Esquema en `bdsysl.sql` (con `recordatorio_activo`):
```sql
CREATE TABLE recordatorios (
    id_recordatorio SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    recordatorio_tipo VARCHAR(10) NOT NULL,
    recordatorio_fecha_programada TIMESTAMP NOT NULL,
    recordatorio_fecha_enviado TIMESTAMP,
    recordatorio_estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    recordatorio_intentos INTEGER DEFAULT 0,
    recordatorio_mensaje_enviado TEXT,
    recordatorio_error TEXT,
    recordatorio_twilio_sid VARCHAR(100),
    recordatorio_telefono VARCHAR(20),
    recordatorio_paciente_nombre VARCHAR(200),
    recordatorio_creacion_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recordatorio_creacion_usuario INTEGER,
    recordatorio_activo BOOLEAN DEFAULT TRUE  -- ✅ EXISTE
);
```

### Esquema en `04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql` (sin `recordatorio_activo`):
```sql
CREATE TABLE IF NOT EXISTS recordatorios (
    id_recordatorio SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    recordatorio_tipo VARCHAR(10) NOT NULL,
    recordatorio_fecha_programada TIMESTAMP NOT NULL,
    recordatorio_fecha_enviado TIMESTAMP,
    recordatorio_estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    recordatorio_intentos INTEGER DEFAULT 0,
    recordatorio_mensaje_enviado TEXT,
    recordatorio_error TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA'
    -- ❌ NO tiene recordatorio_activo
);
```

---

## 🔧 ACCIONES INMEDIATAS

1. **Verificar estructura real de BD:**
   ```sql
   \d recordatorios
   ```

2. **Si falta `recordatorio_activo`, ejecutar:**
   ```sql
   ALTER TABLE recordatorios 
   ADD COLUMN IF NOT EXISTS recordatorio_activo BOOLEAN DEFAULT TRUE;
   
   -- Actualizar registros existentes
   UPDATE recordatorios 
   SET recordatorio_activo = TRUE 
   WHERE recordatorio_activo IS NULL;
   ```

3. **Si falta `recordatorio_twilio_sid`, ejecutar:**
   ```sql
   ALTER TABLE recordatorios 
   ADD COLUMN IF NOT EXISTS recordatorio_twilio_sid VARCHAR(100);
   ```

4. **Si falta `recordatorio_telefono` o `recordatorio_paciente_nombre`, ejecutar:**
   ```sql
   ALTER TABLE recordatorios 
   ADD COLUMN IF NOT EXISTS recordatorio_telefono VARCHAR(20),
   ADD COLUMN IF NOT EXISTS recordatorio_paciente_nombre VARCHAR(200);
   ```

---

## 📝 NOTAS ADICIONALES

- El error de contexto es crítico y debe corregirse primero
- El error de columna es crítico y bloquea todas las consultas
- El error 400 es consecuencia de los anteriores
- Una vez corregidos estos errores, el sistema debería funcionar correctamente

