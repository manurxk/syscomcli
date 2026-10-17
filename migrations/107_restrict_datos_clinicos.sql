-- 107_restrict_datos_clinicos.sql
-- PDF 3 (Base de datos), paso 2: la historia clínica no se borra en cascada.
--
-- Política (plan maestro §2, decisión D2 aprobada 2026-10-13): en datos clínicos la FK es
-- RESTRICT. Borrar una consulta ya NO borra en silencio sus diagnósticos, signos, síntomas,
-- procedimientos, insumos, tratamientos, órdenes, recetas ni certificados; borrar una cita
-- ya NO borra su historial de estados. La base rechaza el DELETE: primero hay que decidir
-- qué pasa con esos datos (en Sysclin no se borran: consultas y citas se anulan por estado).
--
-- Se mantienen en CASCADE, a propósito:
--   - los detalles de un documento (orden_detalle, receta_detalle, factura_detalle, ...):
--     son parte del documento, se borran solo con él (composición);
--   - recordatorios -> citas: avisos de turno, no son datos clínicos;
--   - las tablas de seguridad (roles_paginas, roles_permisos, mfa_codigos, usuarios_roles).
--
-- Mismos nombres de constraint que antes; solo cambia ON DELETE (ON UPDATE se conserva).
--
--   Get-Content migrations\107_restrict_datos_clinicos.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

ALTER TABLE registro_diagnosticos
    DROP CONSTRAINT registro_diagnosticos_id_consulta_fkey,
    ADD CONSTRAINT registro_diagnosticos_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE registro_signos
    DROP CONSTRAINT registro_signos_id_consulta_fkey,
    ADD CONSTRAINT registro_signos_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE registro_sintomas
    DROP CONSTRAINT registro_sintomas_id_consulta_fkey,
    ADD CONSTRAINT registro_sintomas_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE registro_procedimientos
    DROP CONSTRAINT registro_procedimientos_id_consulta_fkey,
    ADD CONSTRAINT registro_procedimientos_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE registro_insumos
    DROP CONSTRAINT registro_insumos_id_consulta_fkey,
    ADD CONSTRAINT registro_insumos_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE tratamientos
    DROP CONSTRAINT tratamientos_id_consulta_fkey,
    ADD CONSTRAINT tratamientos_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE ordenes
    DROP CONSTRAINT ordenes_id_consulta_fkey,
    ADD CONSTRAINT ordenes_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE recetas
    DROP CONSTRAINT recetas_id_consulta_fkey,
    ADD CONSTRAINT recetas_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE certificados_medicos
    DROP CONSTRAINT certificados_medicos_id_consulta_fkey,
    ADD CONSTRAINT certificados_medicos_id_consulta_fkey
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT;

ALTER TABLE citas_log_estados
    DROP CONSTRAINT citas_log_estados_id_cita_fkey,
    ADD CONSTRAINT citas_log_estados_id_cita_fkey
        FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON UPDATE CASCADE ON DELETE RESTRICT;

COMMENT ON CONSTRAINT registro_diagnosticos_id_consulta_fkey ON registro_diagnosticos IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus diagnósticos (migración 107).';
COMMENT ON CONSTRAINT registro_signos_id_consulta_fkey ON registro_signos IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus signos (migración 107).';
COMMENT ON CONSTRAINT registro_sintomas_id_consulta_fkey ON registro_sintomas IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus síntomas (migración 107).';
COMMENT ON CONSTRAINT registro_procedimientos_id_consulta_fkey ON registro_procedimientos IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus procedimientos (migración 107).';
COMMENT ON CONSTRAINT registro_insumos_id_consulta_fkey ON registro_insumos IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus insumos (migración 107).';
COMMENT ON CONSTRAINT tratamientos_id_consulta_fkey ON tratamientos IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus tratamientos (migración 107).';
COMMENT ON CONSTRAINT ordenes_id_consulta_fkey ON ordenes IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus órdenes (migración 107).';
COMMENT ON CONSTRAINT recetas_id_consulta_fkey ON recetas IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus recetas (migración 107).';
COMMENT ON CONSTRAINT certificados_medicos_id_consulta_fkey ON certificados_medicos IS
    'RESTRICT: historia clínica; borrar la consulta no borra sus certificados (migración 107).';
COMMENT ON CONSTRAINT citas_log_estados_id_cita_fkey ON citas_log_estados IS
    'RESTRICT: historial de estados de la cita; borrar la cita no borra su historial (migración 107).';

COMMIT;

-- Vuelta atrás (solo si hiciera falta): repetir cada ALTER con ON DELETE CASCADE, por ejemplo
--   ALTER TABLE recetas DROP CONSTRAINT recetas_id_consulta_fkey,
--       ADD CONSTRAINT recetas_id_consulta_fkey
--           FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE;
--   (citas_log_estados: ON UPDATE CASCADE ON DELETE CASCADE)
