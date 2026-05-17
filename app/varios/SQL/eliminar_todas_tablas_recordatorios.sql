-- ============================================================================
-- SCRIPT: Eliminar TODAS las Tablas de Recordatorios/Avisos
-- ============================================================================
-- Este script elimina todas las tablas, vistas e índices relacionados con recordatorios
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

-- Paso 5: Verificar que se eliminaron
DO $$
DECLARE
    tablas_restantes TEXT;
BEGIN
    SELECT string_agg(table_name, ', ')
    INTO tablas_restantes
    FROM information_schema.tables
    WHERE table_schema = 'public'
        AND (
            table_name LIKE '%recordatorio%' 
            OR table_name LIKE '%aviso%'
            OR table_name LIKE '%notificacion%'
            OR table_name LIKE '%plantilla%recordatorio%'
        );
    
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ Limpieza completada';
    RAISE NOTICE '========================================';
    
    IF tablas_restantes IS NULL THEN
        RAISE NOTICE '✅ Todas las tablas de recordatorios/avisos eliminadas';
    ELSE
        RAISE NOTICE '⚠️ Tablas restantes: %', tablas_restantes;
    END IF;
    
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Ahora puedes ejecutar:';
    RAISE NOTICE 'setup_completo_recordatorios_ultramsg.sql';
    RAISE NOTICE '========================================';
END $$;

