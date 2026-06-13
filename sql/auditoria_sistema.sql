-- =============================================================================
-- ANGASYS - INFRAESTRUCTURA DE AUDITORÍA
-- Script:  auditoria_sistema.sql
-- Autor:   DBA Angasys
-- Fecha:   2026-03-22
-- Uso:     \i sql/auditoria_sistema.sql   (desde psql)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. TABLA PRINCIPAL: auditoria_sistema
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS auditoria_sistema (
    id_auditoria            SERIAL          PRIMARY KEY,
    id_usuario              INTEGER         NOT NULL
                                            REFERENCES usuarios(id_usuario)
                                            ON DELETE SET NULL
                                            DEFERRABLE INITIALLY DEFERRED,
    accion                  VARCHAR(50)     NOT NULL
                                            CHECK (accion IN (
                                                'LOGIN',
                                                'LOGOUT',
                                                'PROFILE_UPDATE',
                                                'RECORD_CREATE',
                                                'RECORD_UPDATE',
                                                'RECORD_DELETE',
                                                'PASSWORD_CHANGE'
                                            )),
    tabla_afectada          VARCHAR(100)    NULL,
    id_registro_afectado    INTEGER         NULL,
    detalle                 TEXT            NULL,
    ip_origen               VARCHAR(45)     NULL,   -- soporta IPv4 e IPv6
    fecha_evento            TIMESTAMP WITH TIME ZONE
                                            NOT NULL
                                            DEFAULT NOW()
);

-- Nota: El ícono visual de cada acción se maneja en la capa Python
-- mediante un diccionario (p.ej. ICONS = {'LOGIN': 'bi-box-arrow-in-right', ...}).
-- Mantener esto fuera de la BD garantiza una tabla agnóstica al frontend.

-- -----------------------------------------------------------------------------
-- 2. COMENTARIOS EN COLUMNAS
-- -----------------------------------------------------------------------------
COMMENT ON TABLE auditoria_sistema IS
    'Registro inmutable de eventos de auditoría del sistema Angasys.';

COMMENT ON COLUMN auditoria_sistema.id_auditoria IS
    'Identificador único autoincremental del evento de auditoría.';

COMMENT ON COLUMN auditoria_sistema.id_usuario IS
    'FK al usuario que generó el evento. Se conserva NULL si el usuario fue eliminado (ON DELETE SET NULL).';

COMMENT ON COLUMN auditoria_sistema.accion IS
    'Tipo de acción auditada. Valores permitidos: LOGIN, LOGOUT, PROFILE_UPDATE, RECORD_CREATE, RECORD_UPDATE, RECORD_DELETE, PASSWORD_CHANGE.';

COMMENT ON COLUMN auditoria_sistema.tabla_afectada IS
    'Nombre de la tabla de base de datos afectada por la acción (NULL para eventos de sesión como LOGIN/LOGOUT).';

COMMENT ON COLUMN auditoria_sistema.id_registro_afectado IS
    'PK del registro específico afectado dentro de tabla_afectada (NULL si no aplica).';

COMMENT ON COLUMN auditoria_sistema.detalle IS
    'Descripción textual libre del evento, cambios realizados o contexto adicional.';

COMMENT ON COLUMN auditoria_sistema.ip_origen IS
    'Dirección IP del cliente que originó el evento. Admite notación IPv4 (15 chars) e IPv6 (hasta 45 chars).';

COMMENT ON COLUMN auditoria_sistema.fecha_evento IS
    'Marca temporal con zona horaria del momento en que ocurrió el evento. Default: NOW().';

-- -----------------------------------------------------------------------------
-- 3. ÍNDICES OBLIGATORIOS
-- -----------------------------------------------------------------------------

-- Consultas frecuentes: histórico de acciones de un usuario ordenadas por fecha
CREATE INDEX IF NOT EXISTS idx_auditoria_usuario_fecha
    ON auditoria_sistema (id_usuario, fecha_evento DESC);

-- Consultas de rango temporal (dashboards, reportes de período)
CREATE INDEX IF NOT EXISTS idx_auditoria_fecha
    ON auditoria_sistema (fecha_evento DESC);

-- Filtrado por tipo de acción (p.ej. todos los LOGIN fallidos)
CREATE INDEX IF NOT EXISTS idx_auditoria_accion
    ON auditoria_sistema (accion);

-- -----------------------------------------------------------------------------
-- 4. POLÍTICA DE RETENCIÓN  (comentada — ejecutar manualmente o via pg_cron)
-- -----------------------------------------------------------------------------
-- Elimina registros con más de 12 meses de antigüedad.
-- Programar como job periódico (pg_cron, cron OS, o tarea de mantenimiento):
--
--   DELETE FROM auditoria_sistema
--    WHERE fecha_evento < NOW() - INTERVAL '12 months';
--
-- Para pg_cron (si está disponible):
--   SELECT cron.schedule(
--       'purge_auditoria_anual',
--       '0 3 1 * *',   -- primer día de cada mes a las 03:00
--       $$ DELETE FROM auditoria_sistema WHERE fecha_evento < NOW() - INTERVAL '12 months' $$
--   );

-- -----------------------------------------------------------------------------
-- 5. INSERT DE PRUEBA
-- -----------------------------------------------------------------------------
INSERT INTO auditoria_sistema (
    id_usuario,
    accion,
    tabla_afectada,
    id_registro_afectado,
    detalle,
    ip_origen
) VALUES (
    1,
    'LOGIN',
    NULL,
    NULL,
    'Migración inicial - test',
    '127.0.0.1'
);

-- Verificación rápida
SELECT
    id_auditoria,
    id_usuario,
    accion,
    detalle,
    ip_origen,
    fecha_evento
FROM auditoria_sistema
ORDER BY id_auditoria DESC
LIMIT 5;

-- =============================================================================
-- FIN DEL SCRIPT
-- =============================================================================
