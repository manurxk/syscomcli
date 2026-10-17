-- 113_presupuesto_plan_tratamiento.sql
-- Presupuesto de plan de tratamiento: el presupuesto puede quedar ligado a una versión del PEI
-- del paciente (opcional). Si tiene id_pei, el PDF sale como "Presupuesto de plan de
-- tratamiento" con la referencia al PEI (versión, estado, especialista, cronograma de
-- seguimiento); sin objetivos/áreas/estrategias, porque el presupuesto lo maneja VENTAS y ese
-- contenido es clínico.
--
-- Se liga a la versión puntual (id_pei), no al paciente: si el plan cambia se emite una nueva
-- versión del PEI y un nuevo presupuesto. RESTRICT como el resto de los datos clínicos (107).
--
-- Diseño aprobado sobre docs/prototipos/presupuesto_plan_tratamiento_ejemplo.pdf, 2026-10-16.
--   Get-Content migrations\113_presupuesto_plan_tratamiento.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

ALTER TABLE presupuestos
    ADD COLUMN IF NOT EXISTS id_pei INTEGER NULL;

ALTER TABLE presupuestos
    DROP CONSTRAINT IF EXISTS presupuestos_id_pei_fkey,
    ADD CONSTRAINT presupuestos_id_pei_fkey
        FOREIGN KEY (id_pei) REFERENCES pei(id_pei) ON UPDATE CASCADE ON DELETE RESTRICT;

CREATE INDEX IF NOT EXISTS idx_presupuestos_pei ON presupuestos (id_pei);

COMMENT ON COLUMN presupuestos.id_pei IS
    'Versión del PEI que presupuesta (opcional). Con valor, el PDF es el presupuesto de plan de tratamiento.';

COMMIT;
