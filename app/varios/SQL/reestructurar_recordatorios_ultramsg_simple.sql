-- ============================================================================
-- SCRIPT: Reestructuración Simplificada de Recordatorios para UltraMsg
-- ============================================================================
-- Nueva estructura: Una fila por cita con columnas booleanas
-- ============================================================================

-- Paso 1: Crear nueva tabla con la estructura simplificada
CREATE TABLE IF NOT EXISTS recordatorios_nuevo (
    id_recordatorio SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL UNIQUE REFERENCES citas(id_cita) ON DELETE CASCADE,
    
    -- Datos de la cita (cache)
    recordatorio_cita_fecha DATE NOT NULL,
    recordatorio_cita_hora_inicio TIME NOT NULL,
    recordatorio_telefono VARCHAR(20),
    recordatorio_paciente_nombre VARCHAR(200),
    
    -- Recordatorio inmediato (creación/actualización de cita)
    recordatorio_inmediato_enviado BOOLEAN DEFAULT FALSE,
    recordatorio_inmediato_fecha_enviado TIMESTAMP,
    recordatorio_inmediato_ultramsg_id VARCHAR(100),
    recordatorio_inmediato_mensaje TEXT,
    
    -- Recordatorio 24 horas antes
    recordatorio_24h_enviado BOOLEAN DEFAULT FALSE,
    recordatorio_24h_fecha_programada TIMESTAMP,
    recordatorio_24h_fecha_enviado TIMESTAMP,
    recordatorio_24h_ultramsg_id VARCHAR(100),
    recordatorio_24h_mensaje TEXT,
    
    -- Recordatorio 12 horas antes
    recordatorio_12h_enviado BOOLEAN DEFAULT FALSE,
    recordatorio_12h_fecha_programada TIMESTAMP,
    recordatorio_12h_fecha_enviado TIMESTAMP,
    recordatorio_12h_ultramsg_id VARCHAR(100),
    recordatorio_12h_mensaje TEXT,
    
    -- Auditoría
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion INTEGER DEFAULT 1
);

-- Paso 2: Migrar datos existentes usando INSERT con subconsultas
INSERT INTO recordatorios_nuevo (
    id_cita,
    recordatorio_cita_fecha,
    recordatorio_cita_hora_inicio,
    recordatorio_telefono,
    recordatorio_paciente_nombre,
    recordatorio_inmediato_enviado,
    recordatorio_inmediato_fecha_enviado,
    recordatorio_inmediato_ultramsg_id,
    recordatorio_inmediato_mensaje,
    recordatorio_24h_enviado,
    recordatorio_24h_fecha_programada,
    recordatorio_24h_fecha_enviado,
    recordatorio_24h_ultramsg_id,
    recordatorio_24h_mensaje,
    recordatorio_12h_enviado,
    recordatorio_12h_fecha_programada,
    recordatorio_12h_fecha_enviado,
    recordatorio_12h_ultramsg_id,
    recordatorio_12h_mensaje
)
SELECT DISTINCT
    c.id_cita,
    c.cita_fecha,
    c.cita_hora_inicio,
    p.per_telefono,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido),
    -- Inmediato
    CASE WHEN EXISTS (
        SELECT 1 FROM recordatorios r 
        WHERE r.id_cita = c.id_cita 
        AND r.recordatorio_tipo = 'inmediato' 
        AND r.recordatorio_estado = 'enviado'
    ) THEN TRUE ELSE FALSE END,
    (SELECT r.recordatorio_fecha_enviado FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = 'inmediato' 
     AND r.recordatorio_estado = 'enviado' LIMIT 1),
    COALESCE(
        (SELECT r.recordatorio_ultramsg_id FROM recordatorios r 
         WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = 'inmediato' LIMIT 1),
        (SELECT r.recordatorio_twilio_sid FROM recordatorios r 
         WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = 'inmediato' LIMIT 1)
    ),
    (SELECT r.recordatorio_mensaje_enviado FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = 'inmediato' LIMIT 1),
    -- 24h
    CASE WHEN EXISTS (
        SELECT 1 FROM recordatorios r 
        WHERE r.id_cita = c.id_cita 
        AND r.recordatorio_tipo = '24h' 
        AND r.recordatorio_estado = 'enviado'
    ) THEN TRUE ELSE FALSE END,
    (SELECT r.recordatorio_fecha_programada FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '24h' LIMIT 1),
    (SELECT r.recordatorio_fecha_enviado FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '24h' 
     AND r.recordatorio_estado = 'enviado' LIMIT 1),
    COALESCE(
        (SELECT r.recordatorio_ultramsg_id FROM recordatorios r 
         WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '24h' LIMIT 1),
        (SELECT r.recordatorio_twilio_sid FROM recordatorios r 
         WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '24h' LIMIT 1)
    ),
    (SELECT r.recordatorio_mensaje_enviado FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '24h' LIMIT 1),
    -- 12h
    CASE WHEN EXISTS (
        SELECT 1 FROM recordatorios r 
        WHERE r.id_cita = c.id_cita 
        AND r.recordatorio_tipo = '12h' 
        AND r.recordatorio_estado = 'enviado'
    ) THEN TRUE ELSE FALSE END,
    (SELECT r.recordatorio_fecha_programada FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '12h' LIMIT 1),
    (SELECT r.recordatorio_fecha_enviado FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '12h' 
     AND r.recordatorio_estado = 'enviado' LIMIT 1),
    COALESCE(
        (SELECT r.recordatorio_ultramsg_id FROM recordatorios r 
         WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '12h' LIMIT 1),
        (SELECT r.recordatorio_twilio_sid FROM recordatorios r 
         WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '12h' LIMIT 1)
    ),
    (SELECT r.recordatorio_mensaje_enviado FROM recordatorios r 
     WHERE r.id_cita = c.id_cita AND r.recordatorio_tipo = '12h' LIMIT 1)
FROM citas c
JOIN pacientes pa ON c.id_paciente = pa.id_paciente
JOIN personas pp ON pa.id_persona = pp.id_persona
JOIN personas p ON pp.id_persona = p.id_persona
WHERE EXISTS (
    SELECT 1 FROM recordatorios r WHERE r.id_cita = c.id_cita
)
ON CONFLICT (id_cita) DO NOTHING;

-- Paso 3: Crear índices para optimización
CREATE INDEX IF NOT EXISTS idx_recordatorios_nuevo_cita ON recordatorios_nuevo(id_cita);
CREATE INDEX IF NOT EXISTS idx_recordatorios_nuevo_24h_pendiente 
    ON recordatorios_nuevo(recordatorio_24h_fecha_programada) 
    WHERE recordatorio_24h_enviado = FALSE;
CREATE INDEX IF NOT EXISTS idx_recordatorios_nuevo_12h_pendiente 
    ON recordatorios_nuevo(recordatorio_12h_fecha_programada) 
    WHERE recordatorio_12h_enviado = FALSE;

-- Paso 4: Verificar migración
SELECT 
    'Total citas con recordatorios antiguos' as descripcion,
    COUNT(DISTINCT id_cita) as cantidad
FROM recordatorios
UNION ALL
SELECT 
    'Total citas en nueva tabla' as descripcion,
    COUNT(*) as cantidad
FROM recordatorios_nuevo;

-- Mensaje final
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Reestructuración completada';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Tabla nueva: recordatorios_nuevo';
    RAISE NOTICE 'Tabla antigua: recordatorios (mantener como backup)';
    RAISE NOTICE '';
    RAISE NOTICE 'PRÓXIMOS PASOS:';
    RAISE NOTICE '1. Verificar que los datos se migraron correctamente';
    RAISE NOTICE '2. Probar el nuevo código con RecordatorioDaoNuevo';
    RAISE NOTICE '3. Si todo funciona, renombrar tablas:';
    RAISE NOTICE '   ALTER TABLE recordatorios RENAME TO recordatorios_backup;';
    RAISE NOTICE '   ALTER TABLE recordatorios_nuevo RENAME TO recordatorios;';
    RAISE NOTICE '========================================';
END $$;

