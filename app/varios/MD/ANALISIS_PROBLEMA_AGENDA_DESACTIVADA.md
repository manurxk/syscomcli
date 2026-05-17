# Análisis: Problema con Agenda Médica Desactivada

## Problema Reportado

Cuando se desactiva una agenda médica:
1. ✅ La agenda desaparece correctamente de la interfaz gráfica
2. ❌ **PROBLEMA**: No se puede crear otra agenda en el mismo horario porque el sistema indica que ya está ocupado
3. ❌ Aunque la agenda está desactivada en la BD (`est_agenda = FALSE`), la restricción UNIQUE de PostgreSQL bloquea la creación

## Análisis del Código

### 1. Campo de Estado en Base de Datos

**Tabla:** `agenda_horarios`
**Campo:** `est_agenda BOOLEAN DEFAULT TRUE`

```sql
-- En 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql línea 88
est_agenda BOOLEAN DEFAULT TRUE
```

### 2. Restricción UNIQUE Problemática

**Ubicación:** `app/varios/SQL/04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql` línea 107

```sql
UNIQUE(id_consultorio, id_especialista, id_dia_semana, agen_hora_inicio)
```

**Problema:** Esta restricción NO considera el campo `est_agenda`, por lo que PostgreSQL bloquea la creación de una nueva agenda incluso si la anterior está desactivada.

### 3. Validación en Python (CORRECTA)

**Archivo:** `app/dao/modulos/agenda_medica/Agenda_MedicaDao.py`

**Método:** `validarDisponibilidadConsultorio()` (líneas 492-528)

```python
validacionSQL = """
    SELECT COUNT(*) 
    FROM agenda_horarios
    WHERE id_consultorio = %s
        AND id_dia_semana = %s
        AND est_agenda = TRUE  -- ✅ CORRECTO: Solo verifica agendas activas
        AND (
            (agen_hora_inicio < %s AND agen_hora_fin > %s) OR
            (agen_hora_inicio >= %s AND agen_hora_inicio < %s) OR
            (agen_hora_fin > %s AND agen_hora_fin <= %s)
        )
"""
```

**Conclusión:** El código Python está correcto y solo valida agendas activas.

### 4. Filtrado en Interfaz (CORRECTO)

**Método:** `getAgendasByEspecialista()` (línea 229)

```python
WHERE ah.id_especialista = %s
    AND ah.est_agenda = TRUE  -- ✅ CORRECTO: Solo muestra agendas activas
```

**Conclusión:** La interfaz solo muestra agendas activas, lo cual es correcto.

## Causa Raíz

La restricción UNIQUE en PostgreSQL se ejecuta **ANTES** de que el código Python pueda validar el estado. PostgreSQL rechaza la inserción directamente por violación de la restricción, sin permitir que el código Python verifique si la agenda existente está activa o inactiva.

## Solución Propuesta

### Opción 1: Índice Parcial (RECOMENDADA)

Modificar la restricción UNIQUE para que solo aplique a agendas activas usando un índice parcial:

```sql
-- Eliminar la restricción UNIQUE actual
ALTER TABLE agenda_horarios 
DROP CONSTRAINT IF EXISTS agenda_horarios_id_consultorio_id_especialista_id_dia_semana_agen_hora_inicio_key;

-- Crear índice único parcial solo para agendas activas
CREATE UNIQUE INDEX idx_agenda_horarios_activos_unique 
ON agenda_horarios(id_consultorio, id_especialista, id_dia_semana, agen_hora_inicio)
WHERE est_agenda = TRUE;
```

**Ventajas:**
- ✅ Permite múltiples agendas desactivadas con el mismo horario
- ✅ Solo aplica la unicidad a agendas activas
- ✅ Mantiene la integridad de datos
- ✅ No requiere cambios en el código Python

### Opción 2: Eliminar Restricción UNIQUE

Eliminar completamente la restricción y manejar la unicidad solo en la aplicación.

**Desventajas:**
- ❌ Menos protección a nivel de base de datos
- ❌ Requiere más validaciones en código

## Implementación

Se debe ejecutar un script SQL de migración para aplicar la solución recomendada.

## Cambios Adicionales Implementados

### Modificación en `getAgendasByEspecialista()`

Se modificó el método para que muestre **TANTO agendas activas como inactivas**, permitiendo:

1. ✅ Ver agendas desactivadas en la interfaz (marcadas como "Inactivo")
2. ✅ Activar/desactivar sin que desaparezcan de la vista
3. ✅ Priorizar agendas activas si hay múltiples en el mismo horario

**Cambio realizado:**
- **Antes:** `WHERE ah.id_especialista = %s AND ah.est_agenda = TRUE`
- **Ahora:** `WHERE ah.id_especialista = %s` (muestra todas)
- **Orden:** `ORDER BY ah.est_agenda DESC` (activas primero)

**Archivo modificado:** `app/dao/modulos/agenda_medica/Agenda_MedicaDao.py` línea 228-230

## Comportamiento con Diferentes Especialistas

### Escenario 1: Dos Especialistas Diferentes
- ✅ **Especialista A** puede tener agenda activa en Consultorio 1, Lunes, 13:00
- ✅ **Especialista B** puede tener agenda activa en Consultorio 1, Lunes, 13:00
- ✅ **NO hay conflicto** porque la restricción incluye `id_especialista`

### Escenario 2: Mismo Especialista
- ✅ **Especialista A** puede desactivar su agenda en Consultorio 1, Lunes, 13:00
- ✅ La agenda desactivada **sigue visible** en la interfaz (marcada como "Inactivo")
- ✅ **Especialista A** puede crear otra agenda activa en el mismo horario (después del fix SQL)
- ✅ **Especialista A** puede reactivar la agenda desactivada sin problemas
- ❌ **NO puede** tener DOS agendas ACTIVAS en el mismo horario (protegido por índice único parcial)

## Resumen de la Solución

### Script SQL a Ejecutar
`app/varios/SQL/FIX_RESTRICCION_UNIQUE_AGENDA_ACTIVA.sql`

### Cambios en Código Python
- ✅ `getAgendasByEspecialista()` ahora muestra agendas activas e inactivas
- ✅ Prioriza agendas activas cuando hay múltiples en el mismo horario
- ✅ La interfaz ya tiene el código para mostrar el estado (badge "Activo"/"Inactivo")

### Resultado Final
Después de ejecutar el script SQL y con los cambios en el código:
- ✅ Puedes activar/desactivar agendas sin que desaparezcan
- ✅ Diferentes especialistas pueden tener agendas activas en el mismo horario
- ✅ Puedes reactivar una agenda desactivada sin problemas
- ✅ El sistema protege contra duplicados solo para agendas activas

