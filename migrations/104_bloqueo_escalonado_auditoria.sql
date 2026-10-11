-- 104_bloqueo_escalonado_auditoria.sql
-- PDF 8 (Seguridad), paso 5: bloqueo escalonado de cuenta + eventos de seguridad en auditoria.
--
-- Escalada de bloqueo por cuenta (definida por el usuario 2026-10-09):
--   Nivel 1: 5 intentos fallidos -> bloqueo 30 minutos
--   Nivel 2: 3 intentos fallidos mas -> bloqueo 1 hora
--   Nivel 3: 3 intentos fallidos mas -> bloqueo indefinido (solo lo levanta un administrador,
--            desde Accesos o Usuarios -> detalle; al desbloquear, la escalada vuelve a nivel 0)
-- Antes eran 3 intentos en todos los niveles.
--
-- Eventos nuevos en auditoria_sistema: RATE_LIMIT (IP frenada / recuperacion frenada),
-- ACCOUNT_LOCKED (cuenta bloqueada), ACCOUNT_UNLOCKED (cuenta desbloqueada por un administrador).
--
--   Get-Content migrations\104_bloqueo_escalonado_auditoria.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

CREATE OR REPLACE FUNCTION public.registrar_intento_login(p_usuario_intentado character varying, p_id_usuario integer, p_exitoso boolean, p_motivo_fallo character varying, p_ip_address character varying, p_user_agent text, p_csrf_valido boolean DEFAULT NULL::boolean)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_id_acceso INTEGER;
    v_intentos_fallidos INTEGER;
    v_nivel INTEGER;
    v_umbral INTEGER;
    v_resultado VARCHAR(30);
BEGIN
    v_resultado := CASE
        WHEN p_exitoso THEN 'EXITOSO'
        WHEN p_motivo_fallo = 'usuario_no_existe' THEN 'FALLIDO_USUARIO_INEXISTENTE'
        WHEN p_motivo_fallo = 'cuenta_bloqueada' THEN 'FALLIDO_BLOQUEADO'
        WHEN p_motivo_fallo = 'sesiones_maximas' THEN 'FALLIDO_SESIONES_MAXIMAS'
        ELSE 'FALLIDO_CLAVE'
    END;

    INSERT INTO accesos_sistema (
        id_usuario, usuario_intentado, resultado,
        ip_origen, user_agent, csrf_valido
    ) VALUES (
        p_id_usuario, p_usuario_intentado, v_resultado,
        p_ip_address::INET, p_user_agent, p_csrf_valido
    ) RETURNING id_acceso INTO v_id_acceso;

    IF p_exitoso AND p_id_usuario IS NOT NULL THEN
        UPDATE usuarios
        SET usu_nro_intentos = 0,
            fecha_ultimo_intento_fallido = NULL,
            nivel_escalada_bloqueo = 0
        WHERE id_usuario = p_id_usuario;
    ELSIF NOT p_exitoso AND p_id_usuario IS NOT NULL THEN
        UPDATE usuarios
        SET usu_nro_intentos = usu_nro_intentos + 1,
            fecha_ultimo_intento_fallido = CURRENT_TIMESTAMP
        WHERE id_usuario = p_id_usuario
        RETURNING usu_nro_intentos, nivel_escalada_bloqueo INTO v_intentos_fallidos, v_nivel;

        -- Primer bloqueo con 5 fallos; reincidencias con 3
        v_umbral := CASE WHEN v_nivel = 0 THEN 5 ELSE 3 END;

        IF v_intentos_fallidos >= v_umbral THEN
            UPDATE usuarios
            SET nivel_escalada_bloqueo = nivel_escalada_bloqueo + 1,
                usu_nro_intentos = 0,
                fecha_bloqueo = CURRENT_TIMESTAMP,
                motivo_bloqueo = CASE
                    WHEN nivel_escalada_bloqueo + 1 = 1 THEN 'Multiples intentos fallidos (bloqueo 30 min)'
                    WHEN nivel_escalada_bloqueo + 1 = 2 THEN 'Multiples intentos fallidos (bloqueo 1 hora, reincidencia)'
                    ELSE 'Multiples intentos fallidos (bloqueo indefinido, requiere administrador)'
                END,
                bloqueado_hasta = CASE
                    WHEN nivel_escalada_bloqueo + 1 = 1 THEN CURRENT_TIMESTAMP + INTERVAL '30 minutes'
                    WHEN nivel_escalada_bloqueo + 1 = 2 THEN CURRENT_TIMESTAMP + INTERVAL '1 hour'
                    ELSE NULL
                END
            WHERE id_usuario = p_id_usuario;
        END IF;
    END IF;

    RETURN v_id_acceso;
END;
$function$;

COMMENT ON FUNCTION public.registrar_intento_login(character varying, integer, boolean, character varying, character varying, text, boolean) IS
    'Registra un intento de login en accesos_sistema y aplica el bloqueo escalonado de la cuenta: 5 fallos -> 30 min; 3 mas -> 1 h; 3 mas -> indefinido (desbloqueo por administrador). Un login exitoso reinicia contador y nivel.';

-- Eventos de seguridad nuevos en auditoria
ALTER TABLE auditoria_sistema DROP CONSTRAINT chk_auditoria_accion;
ALTER TABLE auditoria_sistema ADD CONSTRAINT chk_auditoria_accion CHECK (accion IN (
    'LOGIN', 'LOGOUT', 'LOGIN_FAILED', 'PROFILE_UPDATE',
    'RECORD_CREATE', 'RECORD_UPDATE', 'RECORD_DELETE',
    'PASSWORD_CHANGE', 'REPORT_VIEW',
    'RATE_LIMIT', 'ACCOUNT_LOCKED', 'ACCOUNT_UNLOCKED'
));

COMMIT;
