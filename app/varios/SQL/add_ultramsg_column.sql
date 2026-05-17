-- ============================================================================
-- SCRIPT: Agregar columna para tracking de mensajes UltraMsg
-- ============================================================================
-- Este script agrega la columna recordatorio_ultramsg_id para almacenar
-- el ID del mensaje enviado por UltraMsg (opcional pero recomendado)
--
-- Fecha: 2026-01-22
-- ============================================================================

-- Verificar y agregar columna recordatorio_ultramsg_id
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'recordatorios' 
        AND column_name = 'recordatorio_ultramsg_id'
    ) THEN
        ALTER TABLE recordatorios 
        ADD COLUMN recordatorio_ultramsg_id VARCHAR(100);
        
        RAISE NOTICE 'Columna recordatorio_ultramsg_id agregada exitosamente';
    ELSE
        RAISE NOTICE 'Columna recordatorio_ultramsg_id ya existe';
    END IF;
END $$;

-- Verificar estructura final
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_name = 'recordatorios'
    AND column_name IN ('recordatorio_ultramsg_id', 'recordatorio_twilio_sid')
ORDER BY column_name;

-- Mensaje final
DO $$
BEGIN
    RAISE NOTICE 'Script completado. La columna recordatorio_ultramsg_id está lista para usar.';
END $$;

