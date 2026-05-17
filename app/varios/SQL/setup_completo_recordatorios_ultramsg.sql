-- ============================================================================
-- SCRIPT COMPLETO: Setup de Recordatorios UltraMsg desde Cero
-- ============================================================================
-- Este script hace todo en orden:
-- 1. Elimina citas y recordatorios existentes
-- 2. Elimina tabla recordatorios antigua
-- 3. Crea nueva tabla con estructura simplificada
-- ============================================================================

-- ============================================================================
-- ⚠️ ADVERTENCIA: Este script ELIMINARÁ TODOS los datos de citas y recordatorios
-- ⚠️ Usar solo para desarrollo/testing o cuando se quiera empezar desde cero
-- ============================================================================

-- Paso 1: Eliminar todas las citas (esto también eliminará recordatorios por CASCADE)
DO $$
BEGIN
    DELETE FROM citas;
    RAISE NOTICE '✅ Todas las citas eliminadas';
END $$;

-- Paso 2: Eliminar índices antiguos (si existen)
DROP INDEX IF EXISTS idx_recordatorios_cita;
DROP INDEX IF EXISTS idx_recordatorios_24h_pendiente;
DROP INDEX IF EXISTS idx_recordatorios_12h_pendiente;
DROP INDEX IF EXISTS idx_recordatorios_pendientes;
DROP INDEX IF EXISTS idx_recordatorios_estado;

-- Paso 3: Eliminar tabla recordatorios antigua (si existe)
DROP TABLE IF EXISTS recordatorios CASCADE;
DROP VIEW IF EXISTS v_recordatorios_completos CASCADE;

DO $$
BEGIN
    RAISE NOTICE '✅ Tabla recordatorios antigua eliminada';
END $$;

-- Paso 4: Crear nueva tabla con estructura simplificada
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

-- Paso 5: Crear índices para optimización
CREATE INDEX idx_recordatorios_cita ON recordatorios(id_cita);
CREATE INDEX idx_recordatorios_24h_pendiente 
    ON recordatorios(recordatorio_24h_fecha_programada) 
    WHERE recordatorio_24h_enviado = FALSE;
CREATE INDEX idx_recordatorios_12h_pendiente 
    ON recordatorios(recordatorio_12h_fecha_programada) 
    WHERE recordatorio_12h_enviado = FALSE;

-- Paso 6: Comentarios en columnas para documentación
COMMENT ON TABLE recordatorios IS 'Tabla simplificada de recordatorios UltraMsg: una fila por cita con columnas booleanas para cada tipo';
COMMENT ON COLUMN recordatorios.recordatorio_inmediato_enviado IS 'TRUE si se envió notificación inmediata al crear/editar la cita';
COMMENT ON COLUMN recordatorios.recordatorio_24h_enviado IS 'TRUE si se envió recordatorio 24 horas antes de la cita';
COMMENT ON COLUMN recordatorios.recordatorio_12h_enviado IS 'TRUE si se envió recordatorio 12 horas antes de la cita';

-- Paso 7: Verificar estructura creada
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ SETUP COMPLETO';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Nueva estructura creada:';
    RAISE NOTICE '- Una fila por cita (id_cita UNIQUE)';
    RAISE NOTICE '- Columnas booleanas:';
    RAISE NOTICE '  * recordatorio_inmediato_enviado';
    RAISE NOTICE '  * recordatorio_24h_enviado';
    RAISE NOTICE '  * recordatorio_12h_enviado';
    RAISE NOTICE '- Cada tipo tiene:';
    RAISE NOTICE '  * _enviado (boolean)';
    RAISE NOTICE '  * _fecha_enviado (timestamp)';
    RAISE NOTICE '  * _ultramsg_id (varchar)';
    RAISE NOTICE '  * _mensaje (text)';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Próximo paso: Actualizar código para usar RecordatorioDaoNuevo';
    RAISE NOTICE '========================================';
END $$;

