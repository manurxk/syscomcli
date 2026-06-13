-- ============================================================================
-- CONSULTAS SIMPLES PARA VERIFICAR RECORDATORIOS
-- ============================================================================

-- CONSULTA 1: Ver todos los recordatorios (últimos 50)
SELECT 
    r.id_recordatorio,
    r.id_cita,
    r.recordatorio_tipo,
    r.recordatorio_estado,
    r.recordatorio_fecha_programada,
    r.recordatorio_fecha_enviado,
    c.cita_fecha,
    c.cita_hora_inicio,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente
FROM recordatorios r
JOIN citas c ON r.id_cita = c.id_cita
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
ORDER BY r.id_cita DESC
LIMIT 50;

-- CONSULTA 2: Ver recordatorios de citas específicas
-- Reemplaza los números con los IDs de las citas que quieres verificar
SELECT 
    r.id_recordatorio,
    r.id_cita,
    r.recordatorio_tipo,
    r.recordatorio_estado,
    r.recordatorio_fecha_programada,
    c.cita_fecha,
    c.cita_hora_inicio,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente
FROM recordatorios r
JOIN citas c ON r.id_cita = c.id_cita
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
WHERE r.id_cita IN (1, 2, 3)  -- REEMPLAZA CON LOS IDs DE TUS CITAS
ORDER BY r.id_cita, r.recordatorio_tipo;

-- CONSULTA 3: Contar recordatorios por estado (resumen general)
SELECT 
    recordatorio_estado,
    COUNT(*) as cantidad
FROM recordatorios
GROUP BY recordatorio_estado
ORDER BY cantidad DESC;

-- CONSULTA 4: Ver citas que tienen recordatorios (últimas 20)
SELECT DISTINCT
    c.id_cita,
    c.cita_fecha,
    c.cita_hora_inicio,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente,
    COUNT(r.id_recordatorio) as total_recordatorios
FROM citas c
JOIN recordatorios r ON c.id_cita = r.id_cita
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
GROUP BY c.id_cita, c.cita_fecha, c.cita_hora_inicio, pp.per_nombre, pp.per_apellido
ORDER BY c.id_cita DESC
LIMIT 20;

