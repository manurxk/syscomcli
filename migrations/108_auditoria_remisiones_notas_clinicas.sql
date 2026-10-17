-- 108_auditoria_remisiones_notas_clinicas.sql
-- PDF 3 (Base de datos), paso 3: completar la auditoría por tabla (criterio 1).
--
-- 1. remisiones tenía las 4 columnas de auditoría pero no el trigger compartido
--    fn_set_fecha_modificacion: su fecha_modificacion nunca se actualizaba.
-- 2. notas_clinicas se da de baja con UPDATE (est_nota = FALSE) pero no tenía
--    fecha_modificacion ni usuario_modificacion: no quedaba quién ni cuándo anuló una nota.
--    Se agregan con el mismo tipo y FK que el resto de las tablas, más el trigger.
-- 3. COMMENT ON TABLE de notas_clinicas (decisión D3, 2026-10-13): no es redundante con
--    registro_*; se documenta la diferencia.
--
-- Mismo nombre de trigger que los otros 91: trg_<tabla>_fecha_mod, BEFORE UPDATE, FOR EACH ROW.
--
--   Get-Content migrations\108_auditoria_remisiones_notas_clinicas.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

CREATE TRIGGER trg_remisiones_fecha_mod
    BEFORE UPDATE ON public.remisiones
    FOR EACH ROW EXECUTE FUNCTION fn_set_fecha_modificacion();

ALTER TABLE notas_clinicas
    ADD COLUMN fecha_modificacion timestamp without time zone,
    ADD COLUMN usuario_modificacion integer,
    ADD CONSTRAINT notas_clinicas_usuario_modificacion_fkey
        FOREIGN KEY (usuario_modificacion) REFERENCES usuarios(id_usuario);

CREATE TRIGGER trg_notas_clinicas_fecha_mod
    BEFORE UPDATE ON public.notas_clinicas
    FOR EACH ROW EXECUTE FUNCTION fn_set_fecha_modificacion();

COMMENT ON TABLE notas_clinicas IS
    'Notas libres por PACIENTE en su ficha clínica (seguimiento entre consultas, observaciones del especialista). '
    'No duplica a registro_diagnosticos/signos/sintomas/procedimientos/insumos, que son datos estructurados por CONSULTA. '
    'Baja lógica con est_nota; fecha_modificacion/usuario_modificacion registran quién y cuándo la anuló (migración 108).';

COMMENT ON TABLE remisiones IS
    'Notas de remisión (entrega de servicios/insumos), número REM-AAAA-MM-NNNN. '
    'fecha_modificacion la mantiene el trigger trg_remisiones_fecha_mod (migración 108).';

COMMIT;

-- Vuelta atrás (solo si hiciera falta):
--   DROP TRIGGER trg_remisiones_fecha_mod ON remisiones;
--   DROP TRIGGER trg_notas_clinicas_fecha_mod ON notas_clinicas;
--   ALTER TABLE notas_clinicas DROP COLUMN usuario_modificacion, DROP COLUMN fecha_modificacion;
