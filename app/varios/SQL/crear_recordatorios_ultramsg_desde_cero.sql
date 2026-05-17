-- ============================================================================
-- SCRIPT: Crear Tabla de Recordatorios UltraMsg desde Cero
-- ============================================================================
-- Este script elimina la tabla antigua y crea la nueva estructura simplificada
-- ============================================================================

-- ============================================================================
-- ADVERTENCIA: Este script ELIMINARÁ todos los datos de recordatorios existentes
-- ============================================================================

-- Paso 1: Eliminar tabla antigua (si existe)
DROP TABLE IF EXISTS recordatorios CASCADE;

-- Paso 2: Eliminar cualquier vista relacionada
DROP VIEW IF EXISTS v_recordatorios_completos CASCADE;

-- Paso 3: Crear nueva tabla con estructura simplificada
CREATE TABLE recordatorios (
    id_recordatorio SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL UNIQUE REFERENCES citas(id_cita) ON DELETE CASCADE,
    
    -- Datos de la cita (cache para evitar JOINs)
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

-- Paso 4: Crear índices para optimización
CREATE INDEX idx_recordatorios_cita ON recordatorios(id_cita);
CREATE INDEX idx_recordatorios_24h_pendiente 
    ON recordatorios(recordatorio_24h_fecha_programada) 
    WHERE recordatorio_24h_enviado = FALSE;
CREATE INDEX idx_recordatorios_12h_pendiente 
    ON recordatorios(recordatorio_12h_fecha_programada) 
    WHERE recordatorio_12h_enviado = FALSE;

-- Paso 5: Comentarios en columnas para documentación
COMMENT ON TABLE recordatorios IS 'Tabla simplificada de recordatorios: una fila por cita con columnas booleanas para cada tipo';
COMMENT ON COLUMN recordatorios.recordatorio_inmediato_enviado IS 'TRUE si se envió notificación inmediata al crear/editar la cita';
COMMENT ON COLUMN recordatorios.recordatorio_24h_enviado IS 'TRUE si se envió recordatorio 24 horas antes de la cita';
COMMENT ON COLUMN recordatorios.recordatorio_12h_enviado IS 'TRUE si se envió recordatorio 12 horas antes de la cita';

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ Tabla recordatorios creada exitosamente';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Estructura:';
    RAISE NOTICE '- Una fila por cita (id_cita UNIQUE)';
    RAISE NOTICE '- Columnas booleanas: inmediato, 24h, 12h';
    RAISE NOTICE '- Cada tipo tiene: enviado, fecha_enviado, ultramsg_id, mensaje';
    RAISE NOTICE '========================================';
END $$;

