-- ============================================================================
-- SCRIPT: Eliminar Todas las Citas y Recordatorios
-- ============================================================================
-- ADVERTENCIA: Este script ELIMINARÁ TODOS los datos de citas y recordatorios
-- Usar solo para desarrollo/testing o cuando se quiera empezar desde cero
-- ============================================================================

-- Paso 1: Eliminar todos los recordatorios (si existen)
DELETE FROM recordatorios;

-- Paso 2: Eliminar todas las citas
-- NOTA: Esto también eliminará automáticamente los recordatorios por CASCADE
DELETE FROM citas;

-- Paso 3: Verificar que se eliminaron
DO $$
DECLARE
    total_citas INTEGER;
    total_recordatorios INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_citas FROM citas;
    SELECT COUNT(*) INTO total_recordatorios FROM recordatorios;
    
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Limpieza completada:';
    RAISE NOTICE '- Citas restantes: %', total_citas;
    RAISE NOTICE '- Recordatorios restantes: %', total_recordatorios;
    RAISE NOTICE '========================================';
END $$;

