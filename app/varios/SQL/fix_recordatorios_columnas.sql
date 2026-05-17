-- ============================================================================
-- SCRIPT DE CORRECCIÓN: Agregar columnas faltantes a tabla recordatorios
-- ============================================================================
-- Este script agrega las columnas necesarias para el sistema de recordatorios
-- si no existen en la base de datos.
--
-- Ejecutar este script si se obtienen errores como:
--   "no existe la columna «recordatorio_activo»"
--   "no existe la columna «recordatorio_telefono»"
--   etc.
--
-- Fecha: 2026-01-22
-- ============================================================================

-- Verificar y agregar columna recordatorio_activo
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'recordatorios' 
        AND column_name = 'recordatorio_activo'
    ) THEN
        ALTER TABLE recordatorios 
        ADD COLUMN recordatorio_activo BOOLEAN DEFAULT TRUE;
        
        -- Actualizar registros existentes
        UPDATE recordatorios 
        SET recordatorio_activo = TRUE 
        WHERE recordatorio_activo IS NULL;
        
        RAISE NOTICE 'Columna recordatorio_activo agregada exitosamente';
    ELSE
        RAISE NOTICE 'Columna recordatorio_activo ya existe';
    END IF;
END $$;

-- Verificar y agregar columna recordatorio_telefono
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'recordatorios' 
        AND column_name = 'recordatorio_telefono'
    ) THEN
        ALTER TABLE recordatorios 
        ADD COLUMN recordatorio_telefono VARCHAR(20);
        
        RAISE NOTICE 'Columna recordatorio_telefono agregada exitosamente';
    ELSE
        RAISE NOTICE 'Columna recordatorio_telefono ya existe';
    END IF;
END $$;

-- Verificar y agregar columna recordatorio_paciente_nombre
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'recordatorios' 
        AND column_name = 'recordatorio_paciente_nombre'
    ) THEN
        ALTER TABLE recordatorios 
        ADD COLUMN recordatorio_paciente_nombre VARCHAR(200);
        
        RAISE NOTICE 'Columna recordatorio_paciente_nombre agregada exitosamente';
    ELSE
        RAISE NOTICE 'Columna recordatorio_paciente_nombre ya existe';
    END IF;
END $$;

-- Verificar y agregar columna recordatorio_creacion_usuario (si no existe)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'recordatorios' 
        AND column_name = 'recordatorio_creacion_usuario'
    ) THEN
        ALTER TABLE recordatorios 
        ADD COLUMN recordatorio_creacion_usuario INTEGER;
        
        RAISE NOTICE 'Columna recordatorio_creacion_usuario agregada exitosamente';
    ELSE
        RAISE NOTICE 'Columna recordatorio_creacion_usuario ya existe';
    END IF;
END $$;

-- Verificar y agregar columna recordatorio_creacion_fecha (si no existe)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'recordatorios' 
        AND column_name = 'recordatorio_creacion_fecha'
    ) THEN
        ALTER TABLE recordatorios 
        ADD COLUMN recordatorio_creacion_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        
        RAISE NOTICE 'Columna recordatorio_creacion_fecha agregada exitosamente';
    ELSE
        RAISE NOTICE 'Columna recordatorio_creacion_fecha ya existe';
    END IF;
END $$;

-- Crear índice para optimizar consultas de recordatorios pendientes
-- Solo si existe la columna recordatorio_activo
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'recordatorios' 
        AND column_name = 'recordatorio_activo'
    ) THEN
        -- Crear índice con recordatorio_activo
        CREATE INDEX IF NOT EXISTS idx_recordatorios_pendientes 
        ON recordatorios(recordatorio_estado, recordatorio_fecha_programada) 
        WHERE recordatorio_estado = 'pendiente' AND recordatorio_activo = TRUE;
        
        RAISE NOTICE 'Índice idx_recordatorios_pendientes creado con recordatorio_activo';
    ELSE
        -- Crear índice sin recordatorio_activo
        CREATE INDEX IF NOT EXISTS idx_recordatorios_pendientes 
        ON recordatorios(recordatorio_estado, recordatorio_fecha_programada) 
        WHERE recordatorio_estado = 'pendiente';
        
        RAISE NOTICE 'Índice idx_recordatorios_pendientes creado sin recordatorio_activo';
    END IF;
END $$;

-- Verificar estructura final
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns
WHERE table_name = 'recordatorios'
ORDER BY ordinal_position;

-- Mensaje final
DO $$
BEGIN
    RAISE NOTICE 'Script de corrección completado. Verifique la estructura de la tabla arriba.';
END $$;

