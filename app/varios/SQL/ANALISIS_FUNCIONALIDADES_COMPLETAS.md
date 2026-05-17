# Análisis Completo de Funcionalidades en las Fases SQL

## ✅ Funcionalidades Verificadas y Incluidas

### 1. **Generación de Cupos** ✅
**Ubicación:** FASE 4 (04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql)

- **Tabla:** `agenda_horarios`
  - Campo `agen_cupos_totales` - Calculado automáticamente
  - Campo `agen_duracion_turno` - Duración en minutos (30, 45, 60)
  - Campo `agen_turno` - Calculado automáticamente (MAÑANA, TARDE, NOCHE)

- **Funciones:**
  - `obtener_cupos_por_especialista()` - Retorna cupos disponibles y ocupados por especialista
  - `obtener_cupos_por_especialidad()` - Retorna cupos disponibles y ocupados por especialidad
  - Genera bloques de tiempo según duración configurada
  - Respeta citas canceladas (no cuenta como ocupado)

- **Triggers:**
  - `validar_cupo_disponible()` - Valida cupos antes de crear/modificar citas
  - Se ejecuta automáticamente en INSERT/UPDATE de citas

### 2. **Vinculación Paciente-Especialista** ✅
**Ubicación:** FASE 16 (16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql) ⭐ NUEVO

- **Tabla:** `paciente_profesional`
  - Relación M:M entre pacientes y especialistas
  - Campo `tipo_relacion`: ASIGNADO, DERIVADO, TEMPORAL
  - Campo `activo`: TRUE/FALSE para relaciones activas
  - Índice único parcial: Un paciente solo puede estar activo con un especialista a la vez
  - Migración automática desde citas y consultas existentes

- **Vista:** `v_pacientes_por_especialista`
  - Muestra pacientes activos por especialista
  - Incluye información completa de paciente y especialista

### 3. **Agenda Horarios** ✅
**Ubicación:** FASE 4 (04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql)

- **Tabla:** `agenda_horarios`
  - Configuración de horarios por especialista, consultorio, día y especialidad
  - Vigencia desde-hasta (NULL = indefinida)
  - Cupos totales calculados automáticamente
  - Duración de turno configurable (30, 45, 60 minutos)
  - Turno calculado automáticamente (MAÑANA, TARDE, NOCHE)
  - Índice único parcial para evitar duplicados en agendas activas

- **Tabla:** `citas`
  - Vinculada a `agenda_horarios` (id_agenda_horario)
  - Vinculada a paciente (id_paciente)
  - Vinculada a especialista (id_especialista)
  - Estados: AGENDADA, CONFIRMADA, COMPLETADA, CANCELADA, INASISTENCIA, REPROGRAMADA
  - Validación automática de cupos disponibles

### 4. **Sistema de Derivaciones** ✅
**Ubicación:** FASE 16 (16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql) ⭐ NUEVO

- **Tabla:** `derivaciones`
  - Derivar pacientes entre especialistas
  - Soporte para especialistas externos (no en el sistema)
  - Estados: PENDIENTE, ACEPTADA, RECHAZADA, CANCELADA
  - Niveles de urgencia: BAJA, NORMAL, ALTA, URGENTE
  - Fechas de derivación, respuesta y aceptación
  - Motivo de rechazo (si aplica)

- **Funciones:**
  - `crear_derivacion()` - Crea derivación y notificación automática
  - `aceptar_derivacion()` - Acepta derivación y crea relación paciente-profesional
  - `rechazar_derivacion()` - Rechaza derivación y notifica al origen

- **Vista:** `v_derivaciones_pendientes`
  - Derivaciones pendientes ordenadas por urgencia y fecha
  - Incluye información de paciente y especialistas (origen y destino)

### 5. **Sistema de Notificaciones** ✅
**Ubicación:** FASE 16 (16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql) ⭐ NUEVO

- **Tabla:** `notificaciones`
  - Notificaciones para usuarios del sistema
  - Vinculada a derivaciones (opcional)
  - Tipos: DERIVACION_RECIBIDA, DERIVACION_ACEPTADA, DERIVACION_RECHAZADA, OTRA
  - Estado: leida (TRUE/FALSE)
  - Fecha de lectura

- **Funcionalidad:**
  - Creación automática al crear derivación
  - Notificación al especialista destino cuando recibe derivación
  - Notificación al especialista origen cuando se acepta/rechaza

### 6. **Soporte para Especialistas Externos** ✅
**Ubicación:** FASE 16 (16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql) ⭐ NUEVO

- **Tabla:** `derivaciones`
  - Campo `es_externo`: TRUE/FALSE
  - Campos para datos de especialista externo:
    - `especialista_externo_nombre`
    - `especialista_externo_apellido`
    - `especialista_externo_telefono`
    - `especialista_externo_matricula`
  - Constraint: Si es externo, `id_especialista_destino` puede ser NULL

## 📋 Resumen de Fases Actualizadas

### Fases Principales (01-14):
- ✅ FASE 1: Referenciales Básicas
- ✅ FASE 2: Seguridad y Usuarios (con Superadministrador)
- ✅ FASE 3: Personas y Pacientes
- ✅ FASE 4: Especialistas y Agendamiento (con generación de cupos)
- ✅ FASE 5: Consultorio
- ✅ FASE 6: Referenciales Ventas
- ✅ FASE 7: Principales Ventas
- ✅ FASE 8: Tablas Nuevas
- ✅ FASE 9: Triggers y Auditoría
- ✅ FASE 10: Datos Iniciales
- ✅ FASE 11: Migraciones Unificadas
- ✅ FASE 12: Usuarios de Ejemplo (opcional)
- ✅ FASE 13: Otros (opcional)
- ✅ FASE 14: Empresa, Sede y SIFEN

### Fases de Datos:
- ✅ FASE 15: Inserts de Todos los Datos

### Fases de Funcionalidades Avanzadas:
- ✅ FASE 16: Paciente-Profesional y Derivaciones ⭐ NUEVO

## 🔍 Funcionalidades Verificadas

### ✅ Generación de Cupos
- [x] Tabla `agenda_horarios` con campo `agen_cupos_totales`
- [x] Función `obtener_cupos_por_especialista()`
- [x] Función `obtener_cupos_por_especialidad()`
- [x] Trigger `validar_cupo_disponible()`
- [x] Cálculo automático de cupos según duración de turno
- [x] Generación de bloques de tiempo (30, 45, 60 minutos)

### ✅ Vinculación Paciente-Especialista
- [x] Tabla `paciente_profesional` (M:M)
- [x] Tipos de relación: ASIGNADO, DERIVADO, TEMPORAL
- [x] Control de relaciones activas (un paciente activo con un especialista a la vez)
- [x] Migración automática desde citas y consultas
- [x] Vista `v_pacientes_por_especialista`

### ✅ Agenda Horarios
- [x] Tabla `agenda_horarios` completa
- [x] Configuración por especialista, consultorio, día, especialidad
- [x] Vigencia desde-hasta
- [x] Cálculo automático de turno y cupos
- [x] Índice único parcial para evitar duplicados

### ✅ Sistema de Derivaciones
- [x] Tabla `derivaciones`
- [x] Funciones: crear_derivacion, aceptar_derivacion, rechazar_derivacion
- [x] Soporte para especialistas externos
- [x] Vista `v_derivaciones_pendientes`
- [x] Integración con notificaciones

### ✅ Sistema de Notificaciones
- [x] Tabla `notificaciones`
- [x] Tipos de notificación
- [x] Estado de lectura
- [x] Creación automática desde derivaciones

## 📝 Notas Importantes

1. **FASE 16 es nueva** y debe ejecutarse después de FASE 4 (requiere especialistas y pacientes)

2. **Orden de ejecución recomendado:**
   - Fases 01-14 (estructura básica)
   - FASE 16 (funcionalidades avanzadas)
   - FASE 15 (todos los datos)

3. **Migración de datos:**
   - La FASE 16 migra automáticamente relaciones paciente-especialista desde citas y consultas existentes
   - Usa `ON CONFLICT DO NOTHING` para evitar duplicados

4. **Funciones de cupos:**
   - Las funciones de cupos en FASE 4 generan bloques de tiempo según la duración configurada
   - Respeta citas canceladas (no cuenta como ocupado)
   - Considera solo agendas activas (est_agenda = TRUE)

5. **Relaciones paciente-especialista:**
   - Un paciente puede tener múltiples especialistas (histórico)
   - Solo uno puede estar activo a la vez (índice único parcial)
   - Las derivaciones crean automáticamente relaciones tipo DERIVADO

## 🚀 Próximos Pasos

1. Ejecutar todas las fases en orden (01-14, 16, 15)
2. Verificar que las funciones de cupos funcionen correctamente
3. Probar el sistema de derivaciones
4. Verificar que las notificaciones se creen automáticamente

