-- 00_funciones.sql — Funciones generales
-- Generado el 2026-10-18 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Las 6 funciones de la base. Van primero porque los triggers de todos los módulos usan
-- fn_set_fecha_modificacion(). Antes: crear la base vacía (CREATE DATABASE).
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/00_funciones.sql

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: cerrar_sesion(character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.cerrar_sesion(p_token_sesion character varying, p_tipo_cierre character varying DEFAULT 'LOGOUT'::character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id_usuario INTEGER;
BEGIN
    SELECT id_usuario INTO v_id_usuario
    FROM sesiones
    WHERE token_sesion = p_token_sesion
      AND est_sesion = TRUE;

    UPDATE sesiones
    SET est_sesion = FALSE,
        fecha_cierre = CURRENT_TIMESTAMP,
        tipo_cierre = p_tipo_cierre
    WHERE token_sesion = p_token_sesion
      AND est_sesion = TRUE;

    IF v_id_usuario IS NOT NULL THEN
        UPDATE usuarios
        SET sesiones_activas = (
            SELECT COUNT(*)
            FROM sesiones
            WHERE id_usuario = v_id_usuario
              AND est_sesion = TRUE
              AND fecha_expiracion > CURRENT_TIMESTAMP
        )
        WHERE id_usuario = v_id_usuario;
    END IF;

    RETURN FOUND;
END;
$$;

--
-- Name: FUNCTION cerrar_sesion(p_token_sesion character varying, p_tipo_cierre character varying); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.cerrar_sesion(p_token_sesion character varying, p_tipo_cierre character varying) IS 'Cierra una sesión activa y actualiza el contador de sesiones activas del usuario';

--
-- Name: crear_sesion(integer, character varying, character varying, character varying, timestamp without time zone, character varying, text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crear_sesion(p_id_usuario integer, p_token_sesion character varying, p_csrf_token character varying, p_refresh_token character varying, p_fecha_expiracion timestamp without time zone, p_ip_address character varying, p_user_agent text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id_sesion INTEGER;
    v_sesiones_activas INTEGER;
    v_max_sesiones INTEGER;
    v_sesion_antigua INTEGER;
BEGIN
    SELECT max_sesiones_simultaneas INTO v_max_sesiones
    FROM usuarios
    WHERE id_usuario = p_id_usuario;

    SELECT COUNT(*) INTO v_sesiones_activas
    FROM sesiones
    WHERE id_usuario = p_id_usuario
      AND est_sesion = TRUE
      AND fecha_expiracion > CURRENT_TIMESTAMP;

    IF v_sesiones_activas >= v_max_sesiones THEN
        SELECT id_sesion INTO v_sesion_antigua
        FROM sesiones
        WHERE id_usuario = p_id_usuario
          AND est_sesion = TRUE
        ORDER BY fecha_inicio ASC
        LIMIT 1;

        IF v_sesion_antigua IS NOT NULL THEN
            UPDATE sesiones
            SET est_sesion = FALSE,
                fecha_cierre = CURRENT_TIMESTAMP,
                tipo_cierre = 'SECURITY'
            WHERE id_sesion = v_sesion_antigua;
        END IF;
    END IF;

    INSERT INTO sesiones (
        id_usuario, token_sesion, csrf_token, refresh_token,
        fecha_expiracion, ip_address, user_agent
    ) VALUES (
        p_id_usuario, p_token_sesion, p_csrf_token, p_refresh_token,
        p_fecha_expiracion, p_ip_address, p_user_agent
    ) RETURNING id_sesion INTO v_id_sesion;

    UPDATE usuarios
    SET sesiones_activas = (
        SELECT COUNT(*)
        FROM sesiones
        WHERE id_usuario = p_id_usuario
          AND est_sesion = TRUE
          AND fecha_expiracion > CURRENT_TIMESTAMP
    )
    WHERE id_usuario = p_id_usuario;

    RETURN v_id_sesion;
END;
$$;

--
-- Name: FUNCTION crear_sesion(p_id_usuario integer, p_token_sesion character varying, p_csrf_token character varying, p_refresh_token character varying, p_fecha_expiracion timestamp without time zone, p_ip_address character varying, p_user_agent text); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.crear_sesion(p_id_usuario integer, p_token_sesion character varying, p_csrf_token character varying, p_refresh_token character varying, p_fecha_expiracion timestamp without time zone, p_ip_address character varying, p_user_agent text) IS 'Crea una sesión nueva, cerrando la más antigua si se alcanzó el máximo de sesiones simultáneas';

--
-- Name: esta_usuario_bloqueado(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.esta_usuario_bloqueado(p_id_usuario integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_bloqueado_hasta TIMESTAMP;
    v_fecha_bloqueo TIMESTAMP;
BEGIN
    SELECT bloqueado_hasta, fecha_bloqueo
    INTO v_bloqueado_hasta, v_fecha_bloqueo
    FROM usuarios
    WHERE id_usuario = p_id_usuario;

    IF v_fecha_bloqueo IS NULL THEN
        RETURN FALSE;
    END IF;

    IF v_bloqueado_hasta IS NOT NULL AND v_bloqueado_hasta < CURRENT_TIMESTAMP THEN
        UPDATE usuarios
        SET fecha_bloqueo = NULL,
            motivo_bloqueo = NULL,
            bloqueado_hasta = NULL
        WHERE id_usuario = p_id_usuario;
        RETURN FALSE;
    END IF;

    RETURN TRUE;
END;
$$;

--
-- Name: FUNCTION esta_usuario_bloqueado(p_id_usuario integer); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.esta_usuario_bloqueado(p_id_usuario integer) IS 'Verifica si un usuario está bloqueado y si el bloqueo sigue vigente';

--
-- Name: fn_set_fecha_modificacion(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_set_fecha_modificacion() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.fecha_modificacion := now();
    RETURN NEW;
END;
$$;

--
-- Name: limpiar_sesiones_expiradas(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.limpiar_sesiones_expiradas() RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_cantidad INTEGER;
BEGIN
    UPDATE sesiones
    SET est_sesion = FALSE,
        fecha_cierre = CURRENT_TIMESTAMP,
        tipo_cierre = 'TIMEOUT'
    WHERE est_sesion = TRUE
      AND fecha_expiracion <= CURRENT_TIMESTAMP;

    GET DIAGNOSTICS v_cantidad = ROW_COUNT;

    UPDATE usuarios u
    SET sesiones_activas = (
        SELECT COUNT(*)
        FROM sesiones s
        WHERE s.id_usuario = u.id_usuario
          AND s.est_sesion = TRUE
          AND s.fecha_expiracion > CURRENT_TIMESTAMP
    )
    WHERE u.sesiones_activas > 0;

    RETURN v_cantidad;
END;
$$;

--
-- Name: FUNCTION limpiar_sesiones_expiradas(); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.limpiar_sesiones_expiradas() IS 'Cierra (tipo_cierre TIMEOUT) las sesiones con fecha_expiracion vencida y recalcula sesiones_activas por usuario; devuelve la cantidad de sesiones cerradas';

--
-- Name: registrar_intento_login(character varying, integer, boolean, character varying, character varying, text, boolean); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.registrar_intento_login(p_usuario_intentado character varying, p_id_usuario integer, p_exitoso boolean, p_motivo_fallo character varying, p_ip_address character varying, p_user_agent text, p_csrf_valido boolean DEFAULT NULL::boolean) RETURNS integer
    LANGUAGE plpgsql
    AS $$
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
$$;

--
-- Name: FUNCTION registrar_intento_login(p_usuario_intentado character varying, p_id_usuario integer, p_exitoso boolean, p_motivo_fallo character varying, p_ip_address character varying, p_user_agent text, p_csrf_valido boolean); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.registrar_intento_login(p_usuario_intentado character varying, p_id_usuario integer, p_exitoso boolean, p_motivo_fallo character varying, p_ip_address character varying, p_user_agent text, p_csrf_valido boolean) IS 'Registra un intento de login en accesos_sistema y aplica el bloqueo escalonado de la cuenta: 5 fallos -> 30 min; 3 mas -> 1 h; 3 mas -> indefinido (desbloqueo por administrador). Un login exitoso reinicia contador y nivel.';


SET default_tablespace = '';

SET default_table_access_method = heap;
