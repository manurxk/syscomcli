-- 00_funciones.sql — Funciones generales
-- Generado el 2026-10-20 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
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
-- Name: fn_auditar_cambios(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_auditar_cambios() RETURNS trigger
    LANGUAGE plpgsql SECURITY DEFINER
    SET search_path TO 'public'
    AS $$
DECLARE
    v_anterior jsonb;
    v_nuevo    jsonb;
    v_campos   text[];
    v_secreta  text;
BEGIN
    IF TG_OP IN ('UPDATE', 'DELETE') THEN v_anterior := to_jsonb(OLD); END IF;
    IF TG_OP IN ('INSERT', 'UPDATE') THEN v_nuevo := to_jsonb(NEW); END IF;

    IF TG_OP = 'UPDATE' THEN
        -- Columnas de control que no cuentan como cambio: la fecha/usuario de modificación y los datos de
        -- sesión de usuarios (ya quedan en auditoria_sistema y accesos_sistema en cada login/logout).
        SELECT array_agg(n.key ORDER BY n.key) INTO v_campos
          FROM jsonb_each(v_nuevo) n
         WHERE n.value IS DISTINCT FROM v_anterior -> n.key
           AND n.key NOT IN ('fecha_modificacion', 'usuario_modificacion',
                             'sesiones_activas', 'fecha_ultimo_login', 'ip_ultimo_login',
                             'user_agent_ultimo_login');
        IF v_campos IS NULL THEN
            RETURN NULL;  -- nada relevante cambio
        END IF;
    END IF;

    FOREACH v_secreta IN ARRAY ARRAY['usu_clave', 'certificado_firma_digital_password_encrypted', 'codigo_seguridad_contribuyente'] LOOP
        IF v_anterior ? v_secreta THEN v_anterior := jsonb_set(v_anterior, ARRAY[v_secreta], '"***"'); END IF;
        IF v_nuevo ? v_secreta THEN v_nuevo := jsonb_set(v_nuevo, ARRAY[v_secreta], '"***"'); END IF;
    END LOOP;

    INSERT INTO auditoria_transacciones (tabla, modulo, operacion, id_registro, datos_anteriores, datos_nuevos,
                                         campos_modificados, id_usuario, roles, ip_origen)
    VALUES (TG_TABLE_NAME, TG_ARGV[0], TG_OP, COALESCE(v_nuevo, v_anterior) ->> TG_ARGV[1], v_anterior, v_nuevo,
            v_campos, NULLIF(current_setting('app.id_usuario', true), '')::integer,
            NULLIF(current_setting('app.roles', true), ''), NULLIF(current_setting('app.ip', true), '')::inet);
    RETURN NULL;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING 'fn_auditar_cambios: no se audito % en % (%)', TG_OP, TG_TABLE_NAME, SQLERRM;
    RETURN NULL;
END;
$$;

--
-- Name: FUNCTION fn_auditar_cambios(); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_auditar_cambios() IS 'Trigger AFTER INSERT/UPDATE/DELETE de auditoria. Argumentos: modulo y columna de la clave primaria. Guarda antes/despues en auditoria_transacciones con el usuario, roles e IP que la app pasa por set_config (app.id_usuario, app.roles, app.ip). Ignora UPDATE sin cambios reales, enmascara columnas secretas y nunca frena la operacion (EXCEPTION con WARNING).';

--
-- Name: fn_caja_abierta(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_caja_abierta(p_id_caja integer) RETURNS boolean
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
    IF p_id_caja IS NULL THEN
        RAISE EXCEPTION 'Debe indicar la caja.' USING ERRCODE = 'P0001';
    END IF;
    RETURN EXISTS (
        SELECT 1 FROM aperturas_cierre_caja
        WHERE id_caja = p_id_caja
          AND tipo_operacion = 'APERTURA'
          AND est_apertura_cierre = 'A'
    );
END;
$$;

--
-- Name: FUNCTION fn_caja_abierta(p_id_caja integer); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_caja_abierta(p_id_caja integer) IS 'Devuelve true si la caja tiene una apertura activa (tipo APERTURA, estado A). Rechaza un id nulo. La usa sp_cerrar_caja.';

--
-- Name: fn_proteger_factura(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_proteger_factura() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_estado_anterior varchar;
    v_estado_nuevo    varchar;
    v_cambiados       text[];
BEGIN
    IF TG_OP = 'DELETE' THEN
        RAISE EXCEPTION 'La factura % no se puede borrar: es un documento fiscal. Para dejarla sin efecto, anularla.', OLD.factura_numero
            USING ERRCODE = 'P0001';
    END IF;

    SELECT UPPER(des_estado_factura) INTO v_estado_anterior FROM estados_factura WHERE id_estado_factura = OLD.id_estado_factura;
    SELECT UPPER(des_estado_factura) INTO v_estado_nuevo FROM estados_factura WHERE id_estado_factura = NEW.id_estado_factura;

    IF v_estado_anterior = 'ANULADA' THEN
        RAISE EXCEPTION 'La factura % esta anulada y no se puede modificar.', OLD.factura_numero
            USING ERRCODE = 'P0001';
    END IF;

    -- Emitida: solo se acepta la anulación, que cambia el estado y los datos de anulación/modificación
    SELECT array_agg(n.key ORDER BY n.key) INTO v_cambiados
      FROM jsonb_each(to_jsonb(NEW)) n
     WHERE n.value IS DISTINCT FROM to_jsonb(OLD) -> n.key
       AND n.key NOT IN ('id_estado_factura', 'fecha_anulacion', 'usuario_anulacion', 'motivo_anulacion',
                         'fecha_modificacion', 'usuario_modificacion');

    IF v_cambiados IS NOT NULL OR (NEW.id_estado_factura IS DISTINCT FROM OLD.id_estado_factura AND v_estado_nuevo <> 'ANULADA') THEN
        RAISE EXCEPTION 'La factura % ya fue emitida y no se puede modificar (%). Solo se puede anular.',
            OLD.factura_numero, COALESCE(array_to_string(v_cambiados, ', '), 'estado ' || COALESCE(v_estado_nuevo, '?'))
            USING ERRCODE = 'P0001';
    END IF;

    RETURN NEW;
END;
$$;

--
-- Name: FUNCTION fn_proteger_factura(); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_proteger_factura() IS 'Trigger de negocio BEFORE UPDATE OR DELETE en facturas: una factura emitida es un documento fiscal. Solo permite anularla (EMITIDA -> ANULADA, cambiando id_estado_factura, fecha_anulacion, usuario_anulacion, motivo_anulacion y los datos de modificacion). Rechaza otros cambios sobre una emitida, todo cambio sobre una anulada y todo borrado. Cuando se implemente SIFEN (codigo_sifen), agregar esa columna a las permitidas.';

--
-- Name: fn_saldo_esperado_caja(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_saldo_esperado_caja(p_id_caja integer) RETURNS TABLE(saldo_inicial numeric, total_efectivo numeric, total_cheques numeric, total_tarjetas numeric, total_transferencias numeric, saldo_esperado numeric)
    LANGUAGE plpgsql STABLE
    AS $$
DECLARE
    v_apertura RECORD;
BEGIN
    IF p_id_caja IS NULL THEN
        RAISE EXCEPTION 'Debe indicar la caja.' USING ERRCODE = 'P0001';
    END IF;

    SELECT ac.saldo_inicial AS saldo_ini, ac.fecha_operacion AS fecha_ini
      INTO v_apertura
      FROM aperturas_cierre_caja ac
     WHERE ac.id_caja = p_id_caja
       AND ac.tipo_operacion = 'APERTURA'
       AND ac.est_apertura_cierre = 'A'
     ORDER BY ac.fecha_operacion DESC
     LIMIT 1;

    IF NOT FOUND THEN
        RETURN;  -- caja sin apertura activa: no devuelve filas
    END IF;

    RETURN QUERY
    SELECT v_apertura.saldo_ini,
           t.efectivo, t.cheques, t.tarjetas, t.transferencias,
           v_apertura.saldo_ini + t.efectivo + t.cheques + t.tarjetas + t.transferencias
      FROM (
        SELECT COALESCE(SUM(CASE WHEN fc.cod_forma_cobro = 'EFECTIVO' THEN cd.monto_cobrado END), 0) AS efectivo,
               COALESCE(SUM(CASE WHEN fc.cod_forma_cobro = 'CHEQUE' THEN cd.monto_cobrado END), 0) AS cheques,
               COALESCE(SUM(CASE WHEN fc.cod_forma_cobro IN ('TARJETA_CREDITO', 'TARJETA_DEBITO') THEN cd.monto_cobrado END), 0) AS tarjetas,
               COALESCE(SUM(CASE WHEN fc.cod_forma_cobro = 'TRANSFERENCIA' THEN cd.monto_cobrado END), 0) AS transferencias
          FROM cobranzas c
          JOIN cobranza_detalle cd ON cd.id_cobranza = c.id_cobranza
          JOIN formas_cobro fc ON fc.id_forma_cobro = cd.id_forma_cobro
         WHERE c.id_caja = p_id_caja
           AND c.fecha_cobranza >= v_apertura.fecha_ini
           AND c.est_cobranza = 'REGISTRADA'
      ) t;
END;
$$;

--
-- Name: FUNCTION fn_saldo_esperado_caja(p_id_caja integer); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_saldo_esperado_caja(p_id_caja integer) IS 'Saldo que deberia haber en la caja: saldo inicial de la apertura activa + cobros REGISTRADOS desde esa apertura, por forma de cobro (efectivo, cheques, tarjetas, transferencias). Sin apertura activa no devuelve filas. Traslada a la base la logica de AperturaCierreCajaDao.calcularSaldoEsperado; la usa sp_cerrar_caja.';

--
-- Name: fn_set_fecha_modificacion(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_set_fecha_modificacion() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.fecha_modificacion := now();
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING 'fn_set_fecha_modificacion: no se actualizo fecha_modificacion en % (%)', TG_TABLE_NAME, SQLERRM;
    RETURN NEW;
END;
$$;

--
-- Name: FUNCTION fn_set_fecha_modificacion(); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_set_fecha_modificacion() IS 'Trigger BEFORE UPDATE compartido por las tablas con columnas de auditoria: pone fecha_modificacion = now() en cada modificacion (el usuario_modificacion lo pone la app). Si falla, avisa con WARNING y deja seguir el cambio.';

--
-- Name: fn_transicion_cita_valida(text, text, boolean); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_transicion_cita_valida(p_estado_actual text, p_estado_nuevo text, p_mismo_dia boolean DEFAULT false) RETURNS boolean
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT CASE p_estado_actual
        WHEN 'AGENDADA'    THEN p_estado_nuevo IN ('CONFIRMADA', 'EN_CONSULTA', 'AUSENTE', 'CANCELADA')
        WHEN 'CONFIRMADA'  THEN p_estado_nuevo IN ('EN_CONSULTA', 'AUSENTE', 'CANCELADA')
        WHEN 'EN_CONSULTA' THEN p_estado_nuevo = 'COMPLETADA'
        WHEN 'AUSENTE'     THEN COALESCE(p_mismo_dia, false) AND p_estado_nuevo = 'CONFIRMADA'
        WHEN 'CANCELADA'   THEN COALESCE(p_mismo_dia, false) AND p_estado_nuevo = 'AGENDADA'
        ELSE false  -- COMPLETADA y estados desconocidos: no cambian sin autorizacion de un administrador
    END;
$$;

--
-- Name: FUNCTION fn_transicion_cita_valida(p_estado_actual text, p_estado_nuevo text, p_mismo_dia boolean); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_transicion_cita_valida(p_estado_actual text, p_estado_nuevo text, p_mismo_dia boolean) IS 'Mapa de cambios de estado de una cita (codigos de estados_citas). Mismo mapa que CitaDao.TRANSICIONES; con p_mismo_dia = true admite ademas las correcciones del mismo dia (AUSENTE->CONFIRMADA, CANCELADA->AGENDADA). COMPLETADA es final. La usa sp_cambiar_estado_cita.';

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

--
-- Name: sp_anular_factura(integer, integer, text); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.sp_anular_factura(IN p_id_factura integer, IN p_usuario_anulacion integer, OUT o_anulada boolean, OUT o_cobranzas_anuladas integer, OUT o_cuentas_anuladas integer, IN p_motivo text DEFAULT NULL::text)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id_estado_anulada integer;
    v_motivo            text := NULLIF(btrim(p_motivo), '');
BEGIN
    IF p_id_factura IS NULL THEN
        RAISE EXCEPTION 'Debe indicar la factura.';
    END IF;
    IF v_motivo IS NULL OR length(v_motivo) < 3 THEN
        RAISE EXCEPTION 'Debe indicar el motivo de la anulacion (minimo 3 caracteres).';
    END IF;

    SELECT id_estado_factura INTO v_id_estado_anulada
      FROM estados_factura
     WHERE UPPER(des_estado_factura) = 'ANULADA'
     LIMIT 1;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe el estado ANULADA en estados_factura.';
    END IF;

    -- Bloquea la factura: dos anulaciones simultaneas no pueden pasar
    PERFORM 1 FROM facturas WHERE id_factura = p_id_factura FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'La factura % no existe.', p_id_factura;
    END IF;

    -- Una factura con notas vigentes no se anula: primero hay que anular las notas
    IF EXISTS (SELECT 1 FROM notas_credito WHERE id_factura = p_id_factura AND est_nota_credito = 'REGISTRADA')
       OR EXISTS (SELECT 1 FROM notas_debito WHERE id_factura = p_id_factura AND est_nota_debito = 'REGISTRADA') THEN
        RAISE EXCEPTION 'La factura tiene notas de credito o debito vigentes: anule primero las notas.';
    END IF;

    UPDATE facturas
       SET id_estado_factura = v_id_estado_anulada,
           fecha_anulacion = now(),
           usuario_anulacion = p_usuario_anulacion,
           motivo_anulacion = v_motivo,
           usuario_modificacion = p_usuario_anulacion
     WHERE id_factura = p_id_factura AND fecha_anulacion IS NULL;

    IF NOT FOUND THEN
        -- ya estaba anulada: no es un error, pero no se hizo nada
        o_anulada := false;
        o_cobranzas_anuladas := 0;
        o_cuentas_anuladas := 0;
        RETURN;
    END IF;
    o_anulada := true;

    -- El cobro sale de la caja
    UPDATE cobranzas
       SET est_cobranza = 'ANULADA', fecha_modificacion = CURRENT_TIMESTAMP,
           usuario_modificacion = p_usuario_anulacion
     WHERE id_factura = p_id_factura AND est_cobranza = 'REGISTRADA';
    GET DIAGNOSTICS o_cobranzas_anuladas = ROW_COUNT;

    -- La cuenta a cobrar deja de contar (P7)
    UPDATE cuentas_cobrar
       SET est_cuenta_cobrar = 'ANULADA', monto_pagado = 0, monto_pendiente = 0,
           usuario_modificacion = p_usuario_anulacion
     WHERE id_factura = p_id_factura AND est_cuenta_cobrar <> 'ANULADA';
    GET DIAGNOSTICS o_cuentas_anuladas = ROW_COUNT;

    -- En el libro de ventas el comprobante anulado sigue figurando, pero en 0
    UPDATE libro_ventas
       SET monto_gravado = 0, monto_exento = 0, monto_iva = 0, monto_total = 0
     WHERE id_factura = p_id_factura AND tipo_comprobante = 'FACTURA';

EXCEPTION
    WHEN raise_exception THEN
        RAISE;
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'El usuario indicado no existe.';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'No se pudo anular la factura (%): %', SQLSTATE, SQLERRM;
END;
$$;

--
-- Name: PROCEDURE sp_anular_factura(IN p_id_factura integer, IN p_usuario_anulacion integer, OUT o_anulada boolean, OUT o_cobranzas_anuladas integer, OUT o_cuentas_anuladas integer, IN p_motivo text); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON PROCEDURE public.sp_anular_factura(IN p_id_factura integer, IN p_usuario_anulacion integer, OUT o_anulada boolean, OUT o_cobranzas_anuladas integer, OUT o_cuentas_anuladas integer, IN p_motivo text) IS 'Anula una factura emitida con su motivo (obligatorio): cambia su estado a ANULADA, anula sus cobranzas REGISTRADAS (el cobro sale de la caja), pasa su cuenta a cobrar a ANULADA con pagado y pendiente en 0 (P7) y deja en 0 su fila del libro de ventas (el comprobante sigue figurando). Rechaza anular si la factura tiene notas de credito/debito REGISTRADAS. OUT: o_anulada (false si ya estaba anulada), o_cobranzas_anuladas, o_cuentas_anuladas. Sin COMMIT propio: el llamador confirma; ante un error deshace todo. fn_proteger_factura sigue validando que solo se anule.';

--
-- Name: sp_cambiar_estado_cita(integer, text, integer, text); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.sp_cambiar_estado_cita(IN p_id_cita integer, IN p_cod_estado_nuevo text, IN p_usuario_modificacion integer, OUT o_cod_estado_anterior text, OUT o_cod_estado_nuevo text, IN p_motivo text DEFAULT NULL::text)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_cita        RECORD;
    v_nuevo       RECORD;
    v_hoy         date := (now() AT TIME ZONE 'America/Asuncion')::date;
    v_es_pasada   boolean;
    v_es_futura   boolean;
    v_mismo_dia   boolean;
    v_cerrada     boolean;
    v_id_slot     integer;
BEGIN
    IF p_id_cita IS NULL OR p_cod_estado_nuevo IS NULL THEN
        RAISE EXCEPTION 'La cita y el estado nuevo son obligatorios.';
    END IF;

    -- Estado nuevo
    SELECT id_estado_cita, cod_estado_cita, des_estado_cita, es_final
      INTO v_nuevo
      FROM estados_citas
     WHERE cod_estado_cita = p_cod_estado_nuevo AND est_estado_cita = TRUE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Estado ''%'' no encontrado', p_cod_estado_nuevo;
    END IF;

    -- Cita (bloqueada: dos cambios simultaneos no pueden pasar)
    SELECT c.id_cita, c.id_estado_cita, c.id_slot_agenda, c.cita_inicio,
           ec.cod_estado_cita, ec.des_estado_cita
      INTO v_cita
      FROM citas c
      JOIN estados_citas ec ON ec.id_estado_cita = c.id_estado_cita
     WHERE c.id_cita = p_id_cita
       FOR UPDATE OF c;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'La cita indicada no existe';
    END IF;

    o_cod_estado_anterior := v_cita.cod_estado_cita;
    o_cod_estado_nuevo := v_nuevo.cod_estado_cita;

    v_es_pasada := v_cita.cita_inicio::date < v_hoy;
    v_es_futura := v_cita.cita_inicio::date > v_hoy;
    v_mismo_dia := NOT v_es_pasada AND NOT v_es_futura;

    -- Reglas de cambio de estado
    IF NOT fn_transicion_cita_valida(v_cita.cod_estado_cita, v_nuevo.cod_estado_cita, v_mismo_dia) THEN
        v_cerrada := v_cita.cod_estado_cita = 'COMPLETADA'
                     OR (v_cita.cod_estado_cita IN ('AUSENTE', 'CANCELADA') AND NOT v_mismo_dia);
        IF v_cerrada THEN
            RAISE EXCEPTION 'La cita ya está cerrada (estado ''%''). Para corregirla use ''Corregir'' (requiere autorización de un administrador).',
                v_cita.des_estado_cita;
        END IF;
        RAISE EXCEPTION 'Una cita en estado ''%'' no puede pasar a ''%''.', v_cita.des_estado_cita, v_nuevo.cod_estado_cita;
    END IF;
    IF v_es_pasada AND NOT v_nuevo.es_final THEN
        RAISE EXCEPTION 'La cita es de un día anterior: solo puede marcarse como Ausente, Cancelada o Completada (si estaba en consulta), o reprogramarse desde Editar.';
    END IF;
    IF v_es_futura AND v_nuevo.cod_estado_cita IN ('EN_CONSULTA', 'AUSENTE') THEN
        RAISE EXCEPTION 'La cita es de un día futuro: la consulta (o la ausencia) se registra el día de la cita.';
    END IF;

    -- CANCELADA -> AGENDADA: vuelve a reservar su turno (si lo tomó otra cita, falla)
    IF v_cita.cod_estado_cita = 'CANCELADA' THEN
        SELECT sa.id_slot_agenda INTO v_id_slot
          FROM citas c
          JOIN slots_agenda sa ON sa.id_especialista = c.id_especialista AND sa.slot_inicio = c.cita_inicio
         WHERE c.id_cita = p_id_cita AND sa.estado_slot = 'DISPONIBLE'
           FOR UPDATE OF sa;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'El turno de esta cita ya no está libre (lo tomó otra cita o se quitó de la agenda). Agende una cita nueva.';
        END IF;
        UPDATE slots_agenda SET estado_slot = 'RESERVADO' WHERE id_slot_agenda = v_id_slot;
        UPDATE citas SET id_slot_agenda = v_id_slot WHERE id_cita = p_id_cita;
        v_cita.id_slot_agenda := v_id_slot;
    END IF;

    -- Cambio de estado
    UPDATE citas
       SET id_estado_cita = v_nuevo.id_estado_cita,
           usuario_modificacion = p_usuario_modificacion,
           motivo_cancelacion = CASE WHEN v_nuevo.cod_estado_cita = 'CANCELADA' THEN p_motivo ELSE motivo_cancelacion END
     WHERE id_cita = p_id_cita;

    -- Cancelar libera el turno
    IF v_nuevo.cod_estado_cita = 'CANCELADA' AND v_cita.id_slot_agenda IS NOT NULL THEN
        UPDATE slots_agenda SET estado_slot = 'DISPONIBLE'
         WHERE id_slot_agenda = v_cita.id_slot_agenda AND estado_slot = 'RESERVADO';
        UPDATE citas SET id_slot_agenda = NULL WHERE id_cita = p_id_cita;
    END IF;

    -- Completar la cita finaliza su consulta
    IF v_nuevo.cod_estado_cita = 'COMPLETADA' THEN
        UPDATE consultas SET consulta_estado = 'FINALIZADA', usuario_modificacion = p_usuario_modificacion
         WHERE id_cita = p_id_cita AND consulta_estado <> 'FINALIZADA';
    END IF;

    -- Confirmar crea los recordatorios (24 h y 2 h antes)
    IF v_nuevo.cod_estado_cita = 'CONFIRMADA' THEN
        INSERT INTO recordatorios (id_cita, canal, minutos_antes, usuario_creacion)
        VALUES (p_id_cita, 'EMAIL', 1440, p_usuario_modificacion),
               (p_id_cita, 'EMAIL', 120, p_usuario_modificacion)
        ON CONFLICT (id_cita, canal, minutos_antes) DO NOTHING;
    END IF;

    INSERT INTO citas_log_estados (id_cita, id_estado_anterior, id_estado_nuevo, motivo_cambio, usuario_cambio)
    VALUES (p_id_cita, v_cita.id_estado_cita, v_nuevo.id_estado_cita, p_motivo, p_usuario_modificacion);

EXCEPTION
    WHEN raise_exception THEN
        RAISE;
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'El usuario indicado no existe.';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'No se pudo cambiar el estado de la cita (%): %', SQLSTATE, SQLERRM;
END;
$$;

--
-- Name: PROCEDURE sp_cambiar_estado_cita(IN p_id_cita integer, IN p_cod_estado_nuevo text, IN p_usuario_modificacion integer, OUT o_cod_estado_anterior text, OUT o_cod_estado_nuevo text, IN p_motivo text); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON PROCEDURE public.sp_cambiar_estado_cita(IN p_id_cita integer, IN p_cod_estado_nuevo text, IN p_usuario_modificacion integer, OUT o_cod_estado_anterior text, OUT o_cod_estado_nuevo text, IN p_motivo text) IS 'Cambia el estado de una cita (codigo de estados_citas). Bloquea la cita, valida el mapa de cambios (fn_transicion_cita_valida) y la regla del dia en hora de Asuncion (dia anterior: solo estados finales; dia futuro: sin consulta ni ausencia). Cancelar libera el turno; CANCELADA->AGENDADA lo vuelve a reservar si sigue libre; COMPLETADA finaliza la consulta; CONFIRMADA crea los recordatorios; siempre deja el cambio en citas_log_estados. OUT: o_cod_estado_anterior y o_cod_estado_nuevo. No cubre la correccion de una cita cerrada con autorizacion de administrador (CitaDao.corregirCita). Sin COMMIT propio: el llamador confirma; ante un error deshace todo.';

--
-- Name: sp_cerrar_caja(integer, integer, numeric, numeric, numeric, numeric, numeric, text, integer); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.sp_cerrar_caja(IN p_id_caja integer, IN p_id_usuario integer, IN p_saldo_final numeric, OUT o_id_cierre integer, OUT o_saldo_esperado numeric, OUT o_diferencia numeric, IN p_monto_efectivo numeric DEFAULT 0, IN p_monto_cheques numeric DEFAULT 0, IN p_monto_tarjetas numeric DEFAULT 0, IN p_monto_transferencias numeric DEFAULT 0, IN p_observaciones text DEFAULT NULL::text, IN p_usuario_creacion integer DEFAULT NULL::integer)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_apertura RECORD;
BEGIN
    -- 1. Validaciones de entrada
    IF p_id_caja IS NULL OR p_id_usuario IS NULL THEN
        RAISE EXCEPTION 'La caja y el usuario son obligatorios.';
    END IF;
    IF p_saldo_final IS NULL OR p_saldo_final < 0 THEN
        RAISE EXCEPTION 'El saldo final es obligatorio y no puede ser negativo.';
    END IF;
    IF COALESCE(p_monto_efectivo, 0) < 0 OR COALESCE(p_monto_cheques, 0) < 0
       OR COALESCE(p_monto_tarjetas, 0) < 0 OR COALESCE(p_monto_transferencias, 0) < 0 THEN
        RAISE EXCEPTION 'Los montos contados no pueden ser negativos.';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM cajas WHERE id_caja = p_id_caja) THEN
        RAISE EXCEPTION 'La caja % no existe.', p_id_caja;
    END IF;
    IF NOT fn_caja_abierta(p_id_caja) THEN
        RAISE EXCEPTION 'No hay apertura activa para esta caja.';
    END IF;

    -- 2. Bloquea la apertura activa (dos cierres simultaneos no pueden pasar)
    SELECT id_apertura_cierre, saldo_inicial
      INTO v_apertura
      FROM aperturas_cierre_caja
     WHERE id_caja = p_id_caja AND tipo_operacion = 'APERTURA' AND est_apertura_cierre = 'A'
     ORDER BY fecha_operacion DESC
     LIMIT 1
       FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No hay apertura activa para esta caja.';
    END IF;

    -- 3. Saldo esperado y diferencia
    SELECT s.saldo_esperado INTO o_saldo_esperado FROM fn_saldo_esperado_caja(p_id_caja) s;
    o_diferencia := p_saldo_final - COALESCE(o_saldo_esperado, v_apertura.saldo_inicial);

    -- 4. Cierra la apertura, registra el cierre y deja la caja CERRADA
    UPDATE aperturas_cierre_caja
       SET est_apertura_cierre = 'C', usuario_modificacion = p_usuario_creacion
     WHERE id_apertura_cierre = v_apertura.id_apertura_cierre;

    INSERT INTO aperturas_cierre_caja(
        id_caja, id_usuario, tipo_operacion, saldo_inicial, saldo_final,
        monto_efectivo, monto_cheques, monto_tarjetas, monto_transferencias,
        observaciones, est_apertura_cierre, usuario_creacion)
    VALUES (
        p_id_caja, p_id_usuario, 'CIERRE', v_apertura.saldo_inicial, p_saldo_final,
        COALESCE(p_monto_efectivo, 0), COALESCE(p_monto_cheques, 0),
        COALESCE(p_monto_tarjetas, 0), COALESCE(p_monto_transferencias, 0),
        p_observaciones, 'C', p_usuario_creacion)
    RETURNING id_apertura_cierre INTO o_id_cierre;

    UPDATE cajas
       SET caja_estado = 'CERRADA', usuario_modificacion = p_usuario_creacion
     WHERE id_caja = p_id_caja;

EXCEPTION
    WHEN raise_exception THEN
        RAISE;  -- mensajes de validacion propios: pasan tal cual
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'El usuario indicado no existe.';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'No se pudo cerrar la caja (%): %', SQLSTATE, SQLERRM;
END;
$$;

--
-- Name: PROCEDURE sp_cerrar_caja(IN p_id_caja integer, IN p_id_usuario integer, IN p_saldo_final numeric, OUT o_id_cierre integer, OUT o_saldo_esperado numeric, OUT o_diferencia numeric, IN p_monto_efectivo numeric, IN p_monto_cheques numeric, IN p_monto_tarjetas numeric, IN p_monto_transferencias numeric, IN p_observaciones text, IN p_usuario_creacion integer); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON PROCEDURE public.sp_cerrar_caja(IN p_id_caja integer, IN p_id_usuario integer, IN p_saldo_final numeric, OUT o_id_cierre integer, OUT o_saldo_esperado numeric, OUT o_diferencia numeric, IN p_monto_efectivo numeric, IN p_monto_cheques numeric, IN p_monto_tarjetas numeric, IN p_monto_transferencias numeric, IN p_observaciones text, IN p_usuario_creacion integer) IS 'Cierra la caja: valida los datos y que haya apertura activa, bloquea la apertura, marca la apertura como cerrada, inserta el registro CIERRE y pone la caja CERRADA. OUT: o_id_cierre, o_saldo_esperado (fn_saldo_esperado_caja) y o_diferencia (saldo final contado - esperado). Sin COMMIT propio: el llamador confirma. Ante cualquier error deshace todo y lanza un mensaje legible.';


SET default_tablespace = '';

SET default_table_access_method = heap;
