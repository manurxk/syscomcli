# Reestructuración del Módulo de Recordatorios para UltraMsg

**Fecha:** 2026-01-22  
**Objetivo:** Simplificar la estructura de recordatorios usando UltraMsg

---

## 📋 Nueva Estructura

### Concepto
En lugar de tener múltiples filas por cita (una por cada tipo de recordatorio), ahora tendremos **una sola fila por cita** con columnas booleanas para cada tipo de recordatorio.

### Ventajas
- ✅ Más simple: una fila = una cita
- ✅ Sin estados complejos: solo "enviado" o "no enviado"
- ✅ Consultas más rápidas: no hay JOINs complejos
- ✅ Fácil de entender y mantener
- ✅ Mejor para UltraMsg: cada tipo tiene su propio ID de mensaje

---

## 🗄️ Estructura de la Nueva Tabla

```sql
recordatorios
├── id_recordatorio (PK)
├── id_cita (UNIQUE, FK a citas)
├── recordatorio_cita_fecha (cache)
├── recordatorio_cita_hora_inicio (cache)
├── recordatorio_telefono (cache)
├── recordatorio_paciente_nombre (cache)
│
├── RECORDATORIO INMEDIATO (creación/actualización)
│   ├── recordatorio_inmediato_enviado (BOOLEAN)
│   ├── recordatorio_inmediato_fecha_enviado (TIMESTAMP)
│   ├── recordatorio_inmediato_ultramsg_id (VARCHAR)
│   └── recordatorio_inmediato_mensaje (TEXT)
│
├── RECORDATORIO 24H
│   ├── recordatorio_24h_enviado (BOOLEAN)
│   ├── recordatorio_24h_fecha_programada (TIMESTAMP)
│   ├── recordatorio_24h_fecha_enviado (TIMESTAMP)
│   ├── recordatorio_24h_ultramsg_id (VARCHAR)
│   └── recordatorio_24h_mensaje (TEXT)
│
└── RECORDATORIO 12H
    ├── recordatorio_12h_enviado (BOOLEAN)
    ├── recordatorio_12h_fecha_programada (TIMESTAMP)
    ├── recordatorio_12h_fecha_enviado (TIMESTAMP)
    ├── recordatorio_12h_ultramsg_id (VARCHAR)
    └── recordatorio_12h_mensaje (TEXT)
```

---

## 🔄 Comparación: Antes vs Ahora

### ANTES (Estructura Actual)
```
cita_id=10
├── recordatorio (tipo='24h', estado='enviado')
├── recordatorio (tipo='12h', estado='pendiente')
└── recordatorio (tipo='inmediato', estado='enviado')
```
**3 filas por cita**

### AHORA (Nueva Estructura)
```
cita_id=10
└── recordatorio
    ├── recordatorio_24h_enviado = TRUE
    ├── recordatorio_12h_enviado = FALSE
    └── recordatorio_inmediato_enviado = TRUE
```
**1 fila por cita**

---

## 📝 Cambios en el Código

### 1. RecordatorioDao - Nuevos Métodos

#### `crearOActualizarRecordatorio()`
Crea o actualiza el recordatorio de una cita (una sola fila).

#### `marcarInmediatoEnviado()`
Marca el recordatorio inmediato como enviado.

#### `marcar24hEnviado()`
Marca el recordatorio 24h como enviado.

#### `marcar12hEnviado()`
Marca el recordatorio 12h como enviado.

#### `obtenerRecordatoriosPendientes24h()`
Obtiene citas con recordatorio 24h pendiente.

#### `obtenerRecordatoriosPendientes12h()`
Obtiene citas con recordatorio 12h pendiente.

### 2. Simplificación de Consultas

**Antes:**
```sql
SELECT * FROM recordatorios 
WHERE id_cita = 10 AND recordatorio_tipo = '24h'
```

**Ahora:**
```sql
SELECT * FROM recordatorios 
WHERE id_cita = 10
-- Todo en una fila
```

### 3. Vista en la Tabla de Citas

**Antes:**
- Contar filas de recordatorios
- Filtrar por estado
- JOINs complejos

**Ahora:**
```javascript
// Simplemente verificar booleanos
if (recordatorio.recordatorio_inmediato_enviado) {
    // Mostrar badge "Inmediato enviado"
}
if (recordatorio.recordatorio_24h_enviado) {
    // Mostrar badge "24h enviado"
}
if (recordatorio.recordatorio_12h_enviado) {
    // Mostrar badge "12h enviado"
}
```

---

## 🚀 Plan de Migración

### Fase 1: Crear Nueva Tabla
1. Ejecutar script `reestructurar_recordatorios_ultramsg.sql`
2. Verificar que los datos se migraron correctamente
3. Comparar conteos entre tabla antigua y nueva

### Fase 2: Actualizar Código
1. Crear nuevo `RecordatorioDao` con métodos simplificados
2. Actualizar `recordatorio_tasks.py` para usar nueva estructura
3. Actualizar `recordatorio_api.py` para nuevas consultas
4. Actualizar vista HTML para mostrar nuevos campos

### Fase 3: Pruebas
1. Crear nueva cita y verificar recordatorio inmediato
2. Verificar que se programan 24h y 12h
3. Probar envío de recordatorios programados
4. Verificar visualización en tabla de citas

### Fase 4: Migración Final
1. Hacer backup de tabla antigua
2. Renombrar tablas (descomentar en script SQL)
3. Eliminar tabla antigua (después de verificar)

---

## 📊 Ejemplo de Uso

### Crear Recordatorio para Nueva Cita
```python
recordatorio_dao.crearOActualizarRecordatorio(
    id_cita=10,
    cita_fecha='2026-01-30',
    cita_hora='14:30',
    telefono='0991501318',
    paciente_nombre='ARMANDO RAMIREZ',
    fecha_24h='2026-01-29 14:30',
    fecha_12h='2026-01-30 02:30'
)
```

### Marcar Inmediato como Enviado
```python
recordatorio_dao.marcarInmediatoEnviado(
    id_cita=10,
    message_id='msg_123',
    mensaje='Mensaje enviado...'
)
```

### Obtener Recordatorios Pendientes 24h
```python
pendientes = recordatorio_dao.obtenerRecordatoriosPendientes24h()
# Retorna lista de citas con recordatorio_24h_enviado = FALSE
# y recordatorio_24h_fecha_programada <= NOW()
```

---

## ✅ Beneficios

1. **Simplicidad**: Una fila por cita, fácil de entender
2. **Rendimiento**: Menos JOINs, consultas más rápidas
3. **Mantenibilidad**: Código más simple y claro
4. **Escalabilidad**: Fácil agregar nuevos tipos de recordatorios
5. **Claridad**: Estado de todos los recordatorios de una cita en un vistazo

---

## ⚠️ Consideraciones

- La migración preserva los datos existentes
- Se recomienda hacer backup antes de ejecutar
- Verificar datos después de la migración
- La tabla antigua se puede mantener como backup

---

**Estado:** 📝 Plan de implementación  
**Próximo paso:** Ejecutar script SQL y actualizar código

