-- ============================================================================
-- SCRIPT: Verificar Recordatorios de Citas
-- ============================================================================
-- Este script ayuda a verificar si existen recordatorios para las citas
-- y su estado actual
-- ============================================================================

-- 1. Ver TODOS los recordatorios con información de la cita
SELECT 
    r.id_recordatorio,
    r.id_cita,
    r.recordatorio_tipo,
    r.recordatorio_estado,
    r.recordatorio_fecha_programada,
    r.recordatorio_fecha_enviado,
    r.recordatorio_intentos,
    r.recordatorio_telefono,
    r.recordatorio_paciente_nombre,
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'recordatorios' 
                    AND column_name = 'recordatorio_ultramsg_id') 
        THEN (SELECT recordatorio_ultramsg_id FROM recordatorios WHERE id_recordatorio = r.id_recordatorio)
        ELSE NULL
    END as ultramsg_id,
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'recordatorios' 
                    AND column_name = 'recordatorio_activo') 
        THEN (SELECT recordatorio_activo FROM recordatorios WHERE id_recordatorio = r.id_recordatorio)
        ELSE NULL
    END as activo,
    c.cita_fecha,
    c.cita_hora_inicio,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre_completo
FROM recordatorios r
JOIN citas c ON r.id_cita = c.id_cita
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
ORDER BY r.id_cita, r.recordatorio_tipo;

-- 2. Contar recordatorios por cita
SELECT 
    id_cita,
    COUNT(*) as total_recordatorios,
    COUNT(CASE WHEN recordatorio_estado = 'enviado' THEN 1 END) as enviados,
    COUNT(CASE WHEN recordatorio_estado = 'pendiente' THEN 1 END) as pendientes,
    COUNT(CASE WHEN recordatorio_estado = 'fallido' THEN 1 END) as fallidos,
    COUNT(CASE WHEN recordatorio_estado = 'cancelado' THEN 1 END) as cancelados
FROM recordatorios
GROUP BY id_cita
ORDER BY id_cita DESC
LIMIT 20;

-- 3. Ver citas SIN recordatorios (últimas 20 citas)
SELECT 
    c.id_cita,
    c.cita_fecha,
    c.cita_hora_inicio,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
    ec.est_cita_nombre AS estado_cita
FROM citas c
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
WHERE NOT EXISTS (
    SELECT 1 FROM recordatorios r WHERE r.id_cita = c.id_cita
)
AND c.cita_activo = TRUE
ORDER BY c.id_cita DESC
LIMIT 20;

-- 4. Ver recordatorios de una cita específica (REEMPLAZAR 123 con el ID de la cita)
-- SELECT * FROM recordatorios WHERE id_cita = 123;

-- 5. Verificar estructura de la tabla recordatorios
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'recordatorios'
ORDER BY ordinal_position;

