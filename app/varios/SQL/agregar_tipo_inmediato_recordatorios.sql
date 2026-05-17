-- ============================================================================
-- SCRIPT: Agregar tipo 'inmediato' a recordatorios
-- ============================================================================
-- Este script actualiza la restricción CHECK para permitir el tipo 'inmediato'
-- además de '12h' y '24h'
-- ============================================================================

-- Eliminar la restricción CHECK existente si existe
DO $$
DECLARE
    constraint_name TEXT;
BEGIN
    -- Buscar el nombre de la restricción CHECK
    SELECT conname INTO constraint_name
    FROM pg_constraint
    WHERE conrelid = 'recordatorios'::regclass
        AND contype = 'c'
        AND pg_get_constraintdef(oid) LIKE '%recordatorio_tipo%';
    
    -- Si se encontró, eliminarla
    IF constraint_name IS NOT NULL THEN
        EXECUTE format('ALTER TABLE recordatorios DROP CONSTRAINT IF EXISTS %I', constraint_name);
        RAISE NOTICE 'Restricción CHECK eliminada: %', constraint_name;
    END IF;
END $$;

-- Agregar nueva restricción CHECK que incluye 'inmediato'
ALTER TABLE recordatorios 
ADD CONSTRAINT chk_recordatorio_tipo 
CHECK (recordatorio_tipo IN ('12h', '24h', 'inmediato'));

RAISE NOTICE 'Restricción CHECK actualizada para permitir tipo "inmediato"';

