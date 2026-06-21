# Análisis de Errores en la Agenda

## Problemas Identificados

### 1. **Mensaje de Error Incorrecto**
- **Problema**: El mensaje muestra fechas mal formateadas (ej: "0202-12-29" en lugar de "2025-12-29")
- **Causa**: Error en el parseo de fechas en JavaScript
- **Solución**: ✅ Ya corregido en `cita-agregar.html`

### 2. **No se Encuentran Cupos para Fechas Válidas**
- **Problema**: El sistema muestra "No hay horarios disponibles" para fechas que deberían tener cupos
- **Posibles Causas**:
  1. **Fechas fuera del rango de vigencia**: La agenda tiene `agen_fecha_desde` y `agen_fecha_hasta` que limitan cuándo está activa
  2. **Día de la semana no coincide**: La fecha seleccionada no corresponde al día de la semana configurado en la agenda
  3. **Agenda inactiva**: `est_agenda = FALSE`
  4. **Problema con la función SQL**: La función `obtener_cupos_por_especialista` no está retornando resultados correctamente

### 3. **Función SQL Incompleta**
- **Problema**: La función en `04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql` no incluía `duracion_minutos` en el RETURNS TABLE
- **Solución**: ✅ Ya corregido - ahora incluye `duracion_minutos` y usa la duración configurada (30, 45, 60 minutos)

## Scripts de Diagnóstico

### Script Principal: `DIAGNOSTICO_AGENDA_CUPOS.sql`
Este script verifica:
1. Agendas activas del especialista
2. Día de la semana de fechas específicas
3. Verificación de vigencia de agendas
4. Resultado de la función `obtener_cupos_por_especialista`
5. Comparación día de semana vs agenda
6. Verificación completa de todas las condiciones

## Pasos para Diagnosticar

1. **Ejecutar el script de diagnóstico**:
   ```sql
   \i app/varios/SQL/DIAGNOSTICO_AGENDA_CUPOS.sql
   ```

2. **Verificar en la consola del navegador**:
   - Abrir las herramientas de desarrollador (F12)
   - Ir a la pestaña "Console"
   - Buscar los logs que muestran:
     - Fecha consultada
     - Especialista consultado
     - Total de cupos recibidos

3. **Verificar en los logs del servidor**:
   - Buscar mensajes que empiecen con "CitaDao:" o "API:"
   - Estos mostrarán información detallada sobre la consulta

## Soluciones Aplicadas

### ✅ Correcciones Realizadas:
1. Parseo de fechas en mensajes de error
2. Función SQL actualizada para incluir `duracion_minutos`
3. Función SQL actualizada para usar duración configurada (30, 45, 60 minutos)
4. Logging mejorado en API y DAO
5. Validación de día de semana en backend

### 🔧 Próximos Pasos:
1. Ejecutar el script de diagnóstico para identificar el problema específico
2. Verificar las fechas de vigencia de las agendas (`agen_fecha_desde` y `agen_fecha_hasta`)
3. Asegurarse de que las agendas estén activas (`est_agenda = TRUE`)
4. Verificar que el día de la semana de la fecha consultada coincida con el configurado en la agenda

## Ejemplo de Consulta para Verificar Agenda

```sql
-- Ver todas las agendas del especialista 1
SELECT 
    ah.id_agenda_horario,
    ds.des_dia_semana,
    ah.agen_hora_inicio,
    ah.agen_hora_fin,
    ah.agen_fecha_desde,
    ah.agen_fecha_hasta,
    ah.est_agenda,
    CASE 
        WHEN '2025-12-30'::DATE < ah.agen_fecha_desde THEN '❌ ANTES'
        WHEN ah.agen_fecha_hasta IS NOT NULL AND '2025-12-30'::DATE > ah.agen_fecha_hasta THEN '❌ DESPUÉS'
        ELSE '✅ DENTRO'
    END as vigencia_2025_12_30,
    CASE 
        WHEN (
            CASE 
                WHEN EXTRACT(DOW FROM '2025-12-30'::DATE) = 0 THEN 7
                ELSE EXTRACT(DOW FROM '2025-12-30'::DATE)
            END
        ) = ah.id_dia_semana THEN '✅ COINCIDE'
        ELSE '❌ NO COINCIDE'
    END as dia_semana_coincide
FROM agenda_horarios ah
JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
WHERE ah.id_especialista = 1;
```








