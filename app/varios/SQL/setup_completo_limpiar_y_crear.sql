-- ============================================================================
-- SCRIPT COMPLETO: Limpiar TODO y Crear Nueva Estructura de Recordatorios
-- ============================================================================
-- Este script hace TODO en orden:
-- 1. Elimina todas las citas
-- 2. Elimina TODAS las tablas/vistas/índices de recordatorios/avisos
-- 3. Crea nueva tabla con estructura simplificada
-- ============================================================================

-- ============================================================================
-- ⚠️ ADVERTENCIA: Este script ELIMINARÁ TODOS los datos de citas y recordatorios
-- ⚠️ Usar solo para desarrollo/testing o cuando se quiera empezar desde cero
-- ============================================================================

-- ============================================================================
-- PARTE 1: ELIMINAR TODO
-- ============================================================================

-- Paso 1: Eliminar todas las citas (esto también eliminará recordatorios por CASCADE)
DO $$
BEGIN
    DELETE FROM citas;
    RAISE NOTICE '✅ Todas las citas eliminadas';
END $$;

-- Paso 2: Eliminar TODAS las vistas relacionadas con recordatorios
DROP VIEW IF EXISTS v_recordatorios_completos CASCADE;
DROP VIEW IF EXISTS v_recordatorios CASCADE;
DROP VIEW IF EXISTS recordatorios_view CASCADE;
DROP VIEW IF EXISTS v_plantillas_recordatorios CASCADE;

-- Paso 3: Eliminar TODOS los índices relacionados con recordatorios
DROP INDEX IF EXISTS idx_recordatorios_cita;
DROP INDEX IF EXISTS idx_recordatorios_24h_pendiente;
DROP INDEX IF EXISTS idx_recordatorios_12h_pendiente;
DROP INDEX IF EXISTS idx_recordatorios_pendientes;
DROP INDEX IF EXISTS idx_recordatorios_estado;
DROP INDEX IF EXISTS idx_recordatorios_tipo;
DROP INDEX IF EXISTS idx_recordatorios_fecha_programada;
DROP INDEX IF EXISTS idx_recordatorios_activo;

-- Paso 4: Eliminar TODAS las tablas relacionadas con recordatorios/avisos
DROP TABLE IF EXISTS recordatorios CASCADE;
DROP TABLE IF EXISTS recordatorios_nuevo CASCADE;
DROP TABLE IF EXISTS recordatorios_backup CASCADE;
DROP TABLE IF EXISTS plantillas_recordatorios CASCADE;
DROP TABLE IF EXISTS avisos CASCADE;
DROP TABLE IF EXISTS avisos_recordatorios CASCADE;
DROP TABLE IF EXISTS notificaciones CASCADE;
DROP TABLE IF EXISTS notificaciones_citas CASCADE;

DO $$
BEGIN
    RAISE NOTICE '✅ Todas las tablas/vistas/índices de recordatorios eliminados';
END $$;

-- ============================================================================
-- PARTE 2: CREAR NUEVA ESTRUCTURA
-- ============================================================================

-- Paso 5: Crear nueva tabla con estructura simplificada
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

-- Paso 6: Crear índices para optimización
CREATE INDEX idx_recordatorios_cita ON recordatorios(id_cita);
CREATE INDEX idx_recordatorios_24h_pendiente 
    ON recordatorios(recordatorio_24h_fecha_programada) 
    WHERE recordatorio_24h_enviado = FALSE;
CREATE INDEX idx_recordatorios_12h_pendiente 
    ON recordatorios(recordatorio_12h_fecha_programada) 
    WHERE recordatorio_12h_enviado = FALSE;

-- Paso 7: Comentarios en columnas para documentación
COMMENT ON TABLE recordatorios IS 'Tabla simplificada de recordatorios UltraMsg: una fila por cita con columnas booleanas para cada tipo';
COMMENT ON COLUMN recordatorios.recordatorio_inmediato_enviado IS 'TRUE si se envió notificación inmediata al crear/editar la cita';
COMMENT ON COLUMN recordatorios.recordatorio_24h_enviado IS 'TRUE si se envió recordatorio 24 horas antes de la cita';
COMMENT ON COLUMN recordatorios.recordatorio_12h_enviado IS 'TRUE si se envió recordatorio 12 horas antes de la cita';

-- Paso 8: Verificar estructura creada
DO $$
DECLARE
    total_columnas INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_columnas
    FROM information_schema.columns
    WHERE table_name = 'recordatorios';
    
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ SETUP COMPLETO';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Nueva estructura creada:';
    RAISE NOTICE '- Tabla: recordatorios';
    RAISE NOTICE '- Total columnas: %', total_columnas;
    RAISE NOTICE '- Una fila por cita (id_cita UNIQUE)';
    RAISE NOTICE '- Columnas booleanas:';
    RAISE NOTICE '  * recordatorio_inmediato_enviado';
    RAISE NOTICE '  * recordatorio_24h_enviado';
    RAISE NOTICE '  * recordatorio_12h_enviado';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Próximo paso: Actualizar código para usar RecordatorioDaoNuevo';
    RAISE NOTICE '========================================';
END $$;

