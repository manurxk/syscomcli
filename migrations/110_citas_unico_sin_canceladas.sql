-- 110_citas_unico_sin_canceladas.sql
-- PDF 3 (Base de datos), hallazgo H13 / P16 (decisión del usuario 2026-10-13).
--
-- Problema: la restricción única uq_citas_especialista_inicio (id_especialista, cita_inicio)
-- contaba también las citas CANCELADAS. Al cancelar, CitaDao.cambiarEstadoCita libera el
-- turno (slots_agenda vuelve a DISPONIBLE) y deja la cita con id_slot_agenda = NULL; pero
-- el INSERT de una cita nueva en ese turno chocaba con la cancelada. El turno figuraba
-- libre y no se podía reservar (3 turnos así al 2026-10-13).
--
-- Solución: índice único PARCIAL, solo para las citas que ocupan un turno
-- (id_slot_agenda IS NOT NULL). Las canceladas son las únicas sin turno, así que dejan de
-- bloquear, sin escribir en el índice el id de ningún estado. Las citas activas siguen
-- sin poder duplicarse para el mismo especialista y hora.
-- Las búsquedas siguen usando idx_citas_especialista_inicio (índice común, sin cambios).
--
--   Get-Content migrations\110_citas_unico_sin_canceladas.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

ALTER TABLE citas DROP CONSTRAINT uq_citas_especialista_inicio;

CREATE UNIQUE INDEX uq_citas_especialista_inicio
    ON public.citas USING btree (id_especialista, cita_inicio)
    WHERE id_slot_agenda IS NOT NULL;

COMMENT ON INDEX uq_citas_especialista_inicio IS
    'Un especialista no puede tener dos citas a la misma hora. Solo cuenta las citas con turno '
    '(id_slot_agenda no nulo): una cita cancelada libera su turno y no impide reservarlo de nuevo (migración 110).';

COMMIT;

-- Vuelta atrás (solo si hiciera falta; falla si ya hay una cita nueva sobre una cancelada):
--   DROP INDEX uq_citas_especialista_inicio;
--   ALTER TABLE citas ADD CONSTRAINT uq_citas_especialista_inicio UNIQUE (id_especialista, cita_inicio);
