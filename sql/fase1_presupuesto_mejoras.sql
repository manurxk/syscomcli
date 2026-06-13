-- ============================================================
-- FASE 1: MEJORAS AL MÓDULO DE PRESUPUESTO
-- Sistema: Angasys / Clausys
-- Fecha:   2026-03-24
-- Autor:   Antigravity (Plan de Implementación Fase 1)
-- ============================================================
-- INSTRUCCIONES: Ejecutar en orden dentro de una transacción.
-- Probar primero en un entorno de desarrollo.
-- ============================================================

BEGIN;

-- -----------------------------------------------------------
-- 1. TABLA: presupuestos
--    Nuevos campos para gestión del ciclo de vida completo
-- -----------------------------------------------------------

-- Fecha de vencimiento calculada (fecha_presupuesto + validez_dias)
-- Se completa automáticamente al crear un presupuesto.
ALTER TABLE presupuestos
    ADD COLUMN IF NOT EXISTS fecha_vencimiento DATE;

-- Motivo cuando un paciente rechaza el presupuesto
ALTER TABLE presupuestos
    ADD COLUMN IF NOT EXISTS motivo_rechazo TEXT;

-- Actualizar registros existentes: calcular fecha_vencimiento desde campos actuales
UPDATE presupuestos
SET fecha_vencimiento = presupuesto_fecha + (presupuesto_validez_dias || ' days')::INTERVAL
WHERE fecha_vencimiento IS NULL
  AND presupuesto_fecha IS NOT NULL
  AND presupuesto_validez_dias IS NOT NULL;

-- Ampliar los valores permitidos de presupuesto_estado.
-- NOTA: Si existe un CHECK constraint sobre este campo, modificarlo aquí.
-- Revisá tu BD para el nombre exacto. Ejemplo genérico:
-- ALTER TABLE presupuestos DROP CONSTRAINT IF EXISTS presupuestos_presupuesto_estado_check;
-- ALTER TABLE presupuestos ADD CONSTRAINT presupuestos_presupuesto_estado_check
--     CHECK (presupuesto_estado IN (
--         'PENDIENTE', 'APROBADO', 'RECHAZADO', 'VENCIDO', 'FACTURADO_PARCIAL', 'FACTURADO'
--     ));

-- Comentario informativo en la columna
COMMENT ON COLUMN presupuestos.fecha_vencimiento IS 'Fecha calculada: presupuesto_fecha + presupuesto_validez_dias';
COMMENT ON COLUMN presupuestos.motivo_rechazo IS 'Motivo por el cual el paciente rechazó el presupuesto. Solo aplica cuando presupuesto_estado = RECHAZADO';

-- -----------------------------------------------------------
-- 2. TABLA: facturas
--    FK para trazabilidad formal con el presupuesto de origen
-- -----------------------------------------------------------

ALTER TABLE facturas
    ADD COLUMN IF NOT EXISTS id_presupuesto INTEGER;

-- Solo agrega la FK si la columna fue añadida exitosamente
ALTER TABLE facturas
    ADD CONSTRAINT fk_facturas_presupuesto
    FOREIGN KEY (id_presupuesto)
    REFERENCES presupuestos(id_presupuesto)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

COMMENT ON COLUMN facturas.id_presupuesto IS 'FK al presupuesto que origina esta factura. NULL si la factura no viene de un presupuesto.';

-- -----------------------------------------------------------
-- 3. ÍNDICES para mejorar performance de consultas frecuentes
-- -----------------------------------------------------------

-- Índice para buscar presupuestos por estado (ej: PENDIENTE, VENCIDO)
CREATE INDEX IF NOT EXISTS idx_presupuestos_estado
    ON presupuestos(presupuesto_estado, est_presupuesto);

-- Índice para buscar facturas que provienen de un presupuesto
CREATE INDEX IF NOT EXISTS idx_facturas_id_presupuesto
    ON facturas(id_presupuesto)
    WHERE id_presupuesto IS NOT NULL;

-- Índice para buscar presupuestos próximos a vencer
CREATE INDEX IF NOT EXISTS idx_presupuestos_vencimiento
    ON presupuestos(fecha_vencimiento, presupuesto_estado)
    WHERE est_presupuesto = 'A';

COMMIT;

-- -----------------------------------------------------------
-- ROLLBACK DE EMERGENCIA (no ejecutar junto con el anterior)
-- -----------------------------------------------------------
-- BEGIN;
-- ALTER TABLE presupuestos DROP COLUMN IF EXISTS fecha_vencimiento;
-- ALTER TABLE presupuestos DROP COLUMN IF EXISTS motivo_rechazo;
-- ALTER TABLE facturas DROP CONSTRAINT IF EXISTS fk_facturas_presupuesto;
-- ALTER TABLE facturas DROP COLUMN IF EXISTS id_presupuesto;
-- DROP INDEX IF EXISTS idx_presupuestos_estado;
-- DROP INDEX IF EXISTS idx_facturas_id_presupuesto;
-- DROP INDEX IF EXISTS idx_presupuestos_vencimiento;
-- COMMIT;
