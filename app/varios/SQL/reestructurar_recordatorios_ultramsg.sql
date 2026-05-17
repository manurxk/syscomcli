-- ============================================================================
-- SCRIPT: Reestructuración de Recordatorios para UltraMsg
-- ============================================================================
-- Nueva estructura simplificada:
-- - Una sola fila por cita (no múltiples filas)
-- - Columnas booleanas para cada tipo de recordatorio
-- - Sin estados complejos, solo "enviado" o no
-- - Fechas de envío para cada tipo
-- - IDs de mensajes UltraMsg para cada tipo
-- ============================================================================

-- Paso 1: Crear nueva tabla temporal con la nueva estructura
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

-- Paso 2: Migrar datos existentes (si hay)
DO $$
DECLARE
    cita_rec RECORD;
    rec_24h RECORD;
    rec_12h RECORD;
    rec_inmediato RECORD;
BEGIN
    -- Para cada cita que tenga recordatorios
    FOR cita_rec IN 
        SELECT DISTINCT id_cita FROM recordatorios
    LOOP
        -- Obtener datos de la cita
        DECLARE
            cita_fecha DATE;
            cita_hora TIME;
            paciente_telefono VARCHAR(20);
            paciente_nombre VARCHAR(200);
        BEGIN
            SELECT c.cita_fecha, c.cita_hora_inicio
            INTO cita_fecha, cita_hora
            FROM citas c
            WHERE c.id_cita = cita_rec.id_cita;
            
            SELECT p.per_telefono, CONCAT(p.per_nombre, ' ', p.per_apellido)
            INTO paciente_telefono, paciente_nombre
            FROM citas c
            JOIN pacientes pa ON c.id_paciente = pa.id_paciente
            JOIN personas p ON pa.id_persona = p.id_persona
            WHERE c.id_cita = cita_rec.id_cita;
            
            -- Buscar recordatorio 24h
            SELECT 
                recordatorio_fecha_enviado,
                COALESCE(
                    (SELECT recordatorio_ultramsg_id FROM recordatorios 
                     WHERE id_cita = cita_rec.id_cita AND recordatorio_tipo = '24h' LIMIT 1),
                    (SELECT recordatorio_twilio_sid FROM recordatorios 
                     WHERE id_cita = cita_rec.id_cita AND recordatorio_tipo = '24h' LIMIT 1)
                ) as ultramsg_id,
                recordatorio_mensaje_enviado
            INTO rec_24h
            FROM recordatorios
            WHERE id_cita = cita_rec.id_cita 
                AND recordatorio_tipo = '24h'
                AND recordatorio_estado = 'enviado'
            LIMIT 1;
            
            -- Buscar recordatorio 12h
            SELECT 
                recordatorio_fecha_programada,
                recordatorio_fecha_enviado,
                COALESCE(
                    (SELECT recordatorio_ultramsg_id FROM recordatorios 
                     WHERE id_cita = cita_rec.id_cita AND recordatorio_tipo = '12h' LIMIT 1),
                    (SELECT recordatorio_twilio_sid FROM recordatorios 
                     WHERE id_cita = cita_rec.id_cita AND recordatorio_tipo = '12h' LIMIT 1)
                ) as ultramsg_id,
                recordatorio_mensaje_enviado
            INTO rec_12h
            FROM recordatorios
            WHERE id_cita = cita_rec.id_cita 
                AND recordatorio_tipo = '12h'
                AND recordatorio_estado = 'enviado'
            LIMIT 1;
            
            -- Buscar recordatorio inmediato
            SELECT 
                recordatorio_fecha_enviado,
                COALESCE(
                    (SELECT recordatorio_ultramsg_id FROM recordatorios 
                     WHERE id_cita = cita_rec.id_cita AND recordatorio_tipo = 'inmediato' LIMIT 1),
                    (SELECT recordatorio_twilio_sid FROM recordatorios 
                     WHERE id_cita = cita_rec.id_cita AND recordatorio_tipo = 'inmediato' LIMIT 1)
                ) as ultramsg_id,
                recordatorio_mensaje_enviado
            INTO rec_inmediato
            FROM recordatorios
            WHERE id_cita = cita_rec.id_cita 
                AND recordatorio_tipo = 'inmediato'
                AND recordatorio_estado = 'enviado'
            LIMIT 1;
            
            -- Insertar en nueva tabla
            INSERT INTO recordatorios_nuevo (
                id_cita,
                recordatorio_cita_fecha,
                recordatorio_cita_hora_inicio,
                recordatorio_telefono,
                recordatorio_paciente_nombre,
                recordatorio_24h_enviado,
                recordatorio_24h_fecha_programada,
                recordatorio_24h_fecha_enviado,
                recordatorio_24h_ultramsg_id,
                recordatorio_24h_mensaje,
                recordatorio_12h_enviado,
                recordatorio_12h_fecha_programada,
                recordatorio_12h_fecha_enviado,
                recordatorio_12h_ultramsg_id,
                recordatorio_12h_mensaje,
                recordatorio_inmediato_enviado,
                recordatorio_inmediato_fecha_enviado,
                recordatorio_inmediato_ultramsg_id,
                recordatorio_inmediato_mensaje
            ) VALUES (
                cita_rec.id_cita,
                cita_fecha,
                cita_hora,
                paciente_telefono,
                paciente_nombre,
                rec_24h.recordatorio_fecha_enviado IS NOT NULL,
                (SELECT recordatorio_fecha_programada FROM recordatorios 
                 WHERE id_cita = cita_rec.id_cita AND recordatorio_tipo = '24h' LIMIT 1),
                rec_24h.recordatorio_fecha_enviado,
                rec_24h.recordatorio_ultramsg_id,
                rec_24h.recordatorio_mensaje_enviado,
                rec_12h.recordatorio_fecha_enviado IS NOT NULL,
                rec_12h.recordatorio_fecha_programada,
                rec_12h.recordatorio_fecha_enviado,
                rec_12h.recordatorio_ultramsg_id,
                rec_12h.recordatorio_mensaje_enviado,
                rec_inmediato.recordatorio_fecha_enviado IS NOT NULL,
                rec_inmediato.recordatorio_fecha_enviado,
                rec_inmediato.recordatorio_ultramsg_id,
                rec_inmediato.recordatorio_mensaje_enviado
            )
            ON CONFLICT (id_cita) DO NOTHING;
        END;
    END LOOP;
END $$;

-- Paso 3: Crear índices
CREATE INDEX IF NOT EXISTS idx_recordatorios_nuevo_cita ON recordatorios_nuevo(id_cita);
CREATE INDEX IF NOT EXISTS idx_recordatorios_nuevo_24h_pendiente 
    ON recordatorios_nuevo(recordatorio_24h_fecha_programada) 
    WHERE recordatorio_24h_enviado = FALSE;
CREATE INDEX IF NOT EXISTS idx_recordatorios_nuevo_12h_pendiente 
    ON recordatorios_nuevo(recordatorio_12h_fecha_programada) 
    WHERE recordatorio_12h_enviado = FALSE;

-- Paso 4: Backup de tabla antigua (opcional - comentar si no se desea)
-- ALTER TABLE recordatorios RENAME TO recordatorios_backup_$(date +%Y%m%d);

-- Paso 5: Renombrar tablas (DESCOMENTAR SOLO DESPUÉS DE VERIFICAR QUE TODO FUNCIONA)
-- ALTER TABLE recordatorios RENAME TO recordatorios_old;
-- ALTER TABLE recordatorios_nuevo RENAME TO recordatorios;

-- Mensaje final
DO $$
BEGIN
    RAISE NOTICE 'Reestructuración completada. Verificar datos antes de renombrar tablas.';
    RAISE NOTICE 'Tabla nueva: recordatorios_nuevo';
    RAISE NOTICE 'Tabla antigua: recordatorios (hacer backup antes de eliminar)';
END $$;

