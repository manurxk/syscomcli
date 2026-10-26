-- Pruebas de los procedimientos almacenados (PDF 5): sp_cerrar_caja, sp_anular_factura y
-- sp_cambiar_estado_cita, con sus funciones auxiliares. Caso feliz y casos de error de cada uno.
--
-- No deja ningun cambio en la base: cada caso feliz hace su trabajo dentro de un sub-bloque que termina
-- con un error propio (PRB01), y PostgreSQL deshace ese sub-bloque. Los datos se buscan solos
-- (una caja abierta, una factura emitida con cobro, citas en distintos estados); si falta alguno,
-- el caso sale como OMITIDO.
--
-- Uso (ver manual_administrador.md, seccion de procedimientos almacenados):
--   docker cp docs/scripts/pruebas_procedimientos.sql syscomcli_bd:/tmp/pruebas_procedimientos.sql
--   docker exec syscomcli_bd psql -U postgres -d sysclin_bd -f /tmp/pruebas_procedimientos.sql
-- Cada linea empieza con OK, FALLO u OMITIDO (psql las muestra como NOTICE).
\set VERBOSITY terse
SET client_min_messages = notice;

CREATE FUNCTION pg_temp.informar(p_caso text, p_ok boolean, p_detalle text DEFAULT '') RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    RAISE NOTICE '% - %', CASE WHEN p_ok THEN 'OK     ' ELSE 'FALLO  ' END,
        p_caso || CASE WHEN p_detalle = '' THEN '' ELSE ' (' || p_detalle || ')' END;
END;
$$;

-- Ejecuta una sentencia que DEBE fallar con un mensaje de la forma esperada
CREATE FUNCTION pg_temp.espera_error(p_caso text, p_sql text, p_patron text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE p_sql;
    PERFORM pg_temp.informar(p_caso, false, 'no fallo');
EXCEPTION WHEN OTHERS THEN
    PERFORM pg_temp.informar(p_caso, SQLERRM ILIKE p_patron, SQLERRM);
END;
$$;

-- ═══════════════════════════ fn_caja_abierta / fn_saldo_esperado_caja / fn_transicion_cita_valida
DO $$
DECLARE v_caja integer; v_n integer;
BEGIN
    SELECT id_caja INTO v_caja FROM cajas WHERE fn_caja_abierta(id_caja) LIMIT 1;
    IF FOUND THEN
        PERFORM pg_temp.informar('fn_caja_abierta: caja con apertura activa', fn_caja_abierta(v_caja));
        SELECT count(*) INTO v_n FROM fn_saldo_esperado_caja(v_caja);
        PERFORM pg_temp.informar('fn_saldo_esperado_caja: devuelve una fila', v_n = 1);
    ELSE
        PERFORM pg_temp.informar('fn_caja_abierta / fn_saldo_esperado_caja: OMITIDO (no hay caja abierta)', true);
    END IF;
    PERFORM pg_temp.informar('fn_caja_abierta: caja inexistente = false', NOT fn_caja_abierta(-1));
    SELECT count(*) INTO v_n FROM fn_saldo_esperado_caja(-1);
    PERFORM pg_temp.informar('fn_saldo_esperado_caja: caja sin apertura = 0 filas', v_n = 0);
    PERFORM pg_temp.informar('fn_transicion_cita_valida: AGENDADA -> CONFIRMADA', fn_transicion_cita_valida('AGENDADA', 'CONFIRMADA'));
    PERFORM pg_temp.informar('fn_transicion_cita_valida: COMPLETADA -> AGENDADA no', NOT fn_transicion_cita_valida('COMPLETADA', 'AGENDADA', true));
    PERFORM pg_temp.informar('fn_transicion_cita_valida: AUSENTE -> CONFIRMADA solo el mismo dia',
        NOT fn_transicion_cita_valida('AUSENTE', 'CONFIRMADA') AND fn_transicion_cita_valida('AUSENTE', 'CONFIRMADA', true));
END $$;
DO $$ BEGIN PERFORM pg_temp.espera_error('fn_caja_abierta: id nulo', 'SELECT fn_caja_abierta(NULL)', '%Debe indicar la caja%'); END $$;

-- ═══════════════════════════ sp_cerrar_caja
DO $$
DECLARE
    v_caja integer; v_usr integer; v_id integer; v_esp numeric; v_dif numeric; v_estado text; v_abiertas integer;
BEGIN
    SELECT id_caja INTO v_caja FROM cajas WHERE fn_caja_abierta(id_caja) LIMIT 1;
    SELECT id_usuario INTO v_usr FROM usuarios ORDER BY id_usuario LIMIT 1;
    IF v_caja IS NULL THEN
        PERFORM pg_temp.informar('sp_cerrar_caja feliz: OMITIDO (no hay caja abierta)', true);
        RETURN;
    END IF;
    BEGIN
        SELECT s.saldo_esperado INTO v_esp FROM fn_saldo_esperado_caja(v_caja) s;
        CALL sp_cerrar_caja(v_caja, v_usr, v_esp, v_id, v_esp, v_dif, v_esp);  -- el saldo final es la suma de lo contado: todo en efectivo
        SELECT caja_estado INTO v_estado FROM cajas WHERE id_caja = v_caja;
        SELECT count(*) INTO v_abiertas FROM aperturas_cierre_caja WHERE id_caja = v_caja AND est_apertura_cierre = 'A';
        PERFORM pg_temp.informar('sp_cerrar_caja feliz: devuelve id de cierre y diferencia 0', v_id IS NOT NULL AND v_dif = 0, 'cierre ' || v_id);
        PERFORM pg_temp.informar('sp_cerrar_caja feliz: caja CERRADA y sin apertura activa', v_estado = 'CERRADA' AND v_abiertas = 0);
        PERFORM pg_temp.espera_error('sp_cerrar_caja: segundo cierre sin apertura activa',
            format('CALL sp_cerrar_caja(%s, %s, 0, NULL, NULL, NULL)', v_caja, v_usr), '%No hay apertura activa%');
        RAISE EXCEPTION 'prueba' USING ERRCODE = 'PRB01';
    EXCEPTION WHEN SQLSTATE 'PRB01' THEN NULL;
    END;
    PERFORM pg_temp.informar('sp_cerrar_caja: la prueba no dejo cambios (caja sigue abierta)', fn_caja_abierta(v_caja));
    PERFORM pg_temp.espera_error('sp_cerrar_caja: caja nula', format('CALL sp_cerrar_caja(NULL, %s, 0, NULL, NULL, NULL)', v_usr), '%obligatorios%');
    PERFORM pg_temp.espera_error('sp_cerrar_caja: saldo negativo', format('CALL sp_cerrar_caja(%s, %s, -5, NULL, NULL, NULL)', v_caja, v_usr), '%saldo final%');
    PERFORM pg_temp.espera_error('sp_cerrar_caja: monto negativo', format('CALL sp_cerrar_caja(%s, %s, 5, NULL, NULL, NULL, -1)', v_caja, v_usr), '%montos contados%');
    PERFORM pg_temp.espera_error('sp_cerrar_caja: saldo final distinto de lo contado', format('CALL sp_cerrar_caja(%s, %s, 5, NULL, NULL, NULL, 3)', v_caja, v_usr), '%suma de los montos contados%');
    PERFORM pg_temp.espera_error('sp_cerrar_caja: caja inexistente', format('CALL sp_cerrar_caja(-1, %s, 5, NULL, NULL, NULL, 5)', v_usr), '%no existe%');
    PERFORM pg_temp.espera_error('sp_cerrar_caja: usuario inexistente', format('CALL sp_cerrar_caja(%s, -1, 5, NULL, NULL, NULL, 5)', v_caja), '%usuario indicado no existe%');
END $$;

-- ═══════════════════════════ sp_anular_factura
DO $$
DECLARE
    v_fac integer; v_usr integer; v_anulada boolean; v_cob integer; v_cta integer;
    v_est text; v_pend numeric; v_libro numeric; v_regs integer; v_motivo text; v_fac_nota integer;
BEGIN
    SELECT id_usuario INTO v_usr FROM usuarios ORDER BY id_usuario LIMIT 1;
    SELECT f.id_factura INTO v_fac
      FROM facturas f
      JOIN cuentas_cobrar cc ON cc.id_factura = f.id_factura
     WHERE f.fecha_anulacion IS NULL
       AND EXISTS (SELECT 1 FROM cobranzas c WHERE c.id_factura = f.id_factura AND c.est_cobranza = 'REGISTRADA')
       AND NOT EXISTS (SELECT 1 FROM notas_credito n WHERE n.id_factura = f.id_factura AND n.est_nota_credito = 'REGISTRADA')
       AND NOT EXISTS (SELECT 1 FROM notas_debito n WHERE n.id_factura = f.id_factura AND n.est_nota_debito = 'REGISTRADA')
     ORDER BY f.id_factura LIMIT 1;
    IF v_fac IS NULL THEN
        PERFORM pg_temp.informar('sp_anular_factura feliz: OMITIDO (no hay factura emitida con cobro)', true);
    ELSE
        BEGIN
            CALL sp_anular_factura(v_fac, v_usr, v_anulada, v_cob, v_cta, 'Prueba automatica');
            SELECT cc.est_cuenta_cobrar, cc.monto_pendiente INTO v_est, v_pend FROM cuentas_cobrar cc WHERE cc.id_factura = v_fac;
            SELECT monto_total INTO v_libro FROM libro_ventas WHERE id_factura = v_fac AND tipo_comprobante = 'FACTURA';
            SELECT count(*) INTO v_regs FROM cobranzas WHERE id_factura = v_fac AND est_cobranza = 'REGISTRADA';
            SELECT motivo_anulacion INTO v_motivo FROM facturas WHERE id_factura = v_fac;
            PERFORM pg_temp.informar('sp_anular_factura feliz: anulada y cobranzas anuladas', v_anulada AND v_cob >= 1 AND v_regs = 0, v_cob || ' cobranza(s)');
            PERFORM pg_temp.informar('sp_anular_factura feliz: cuenta ANULADA sin pendiente (P7)', v_est = 'ANULADA' AND v_pend = 0 AND v_cta = 1);
            PERFORM pg_temp.informar('sp_anular_factura feliz: libro de ventas en 0 y motivo guardado', COALESCE(v_libro, 0) = 0 AND v_motivo = 'Prueba automatica');
            CALL sp_anular_factura(v_fac, v_usr, v_anulada, v_cob, v_cta, 'Otra vez');
            PERFORM pg_temp.informar('sp_anular_factura: factura ya anulada devuelve o_anulada = false', NOT v_anulada);
            RAISE EXCEPTION 'prueba' USING ERRCODE = 'PRB01';
        EXCEPTION WHEN SQLSTATE 'PRB01' THEN NULL;
        END;
        PERFORM pg_temp.informar('sp_anular_factura: la prueba no dejo cambios', (SELECT fecha_anulacion IS NULL FROM facturas WHERE id_factura = v_fac));
        PERFORM pg_temp.espera_error('sp_anular_factura: sin motivo', format('CALL sp_anular_factura(%s, %s, NULL, NULL, NULL)', v_fac, v_usr), '%motivo%');
        PERFORM pg_temp.espera_error('sp_anular_factura: motivo en blanco', format('CALL sp_anular_factura(%s, %s, NULL, NULL, NULL, ''  '')', v_fac, v_usr), '%motivo%');
        PERFORM pg_temp.espera_error('sp_anular_factura: usuario inexistente', format('CALL sp_anular_factura(%s, -1, NULL, NULL, NULL, ''prueba'')', v_fac), '%usuario indicado no existe%');
    END IF;

    SELECT f.id_factura INTO v_fac_nota FROM facturas f
     WHERE f.fecha_anulacion IS NULL
       AND (EXISTS (SELECT 1 FROM notas_credito n WHERE n.id_factura = f.id_factura AND n.est_nota_credito = 'REGISTRADA')
         OR EXISTS (SELECT 1 FROM notas_debito n WHERE n.id_factura = f.id_factura AND n.est_nota_debito = 'REGISTRADA'))
     ORDER BY f.id_factura LIMIT 1;
    IF v_fac_nota IS NULL THEN
        PERFORM pg_temp.informar('sp_anular_factura con notas vigentes: OMITIDO (no hay factura con notas)', true);
    ELSE
        PERFORM pg_temp.espera_error('sp_anular_factura: factura con notas vigentes',
            format('CALL sp_anular_factura(%s, %s, NULL, NULL, NULL, ''prueba'')', v_fac_nota, v_usr), '%notas%');
    END IF;
    PERFORM pg_temp.espera_error('sp_anular_factura: factura nula', format('CALL sp_anular_factura(NULL, %s, NULL, NULL, NULL, ''prueba'')', v_usr), '%Debe indicar la factura%');
    PERFORM pg_temp.espera_error('sp_anular_factura: factura inexistente', format('CALL sp_anular_factura(-1, %s, NULL, NULL, NULL, ''prueba'')', v_usr), '%no existe%');
END $$;

-- ═══════════════════════════ sp_cambiar_estado_cita
DO $$
DECLARE
    v_usr integer; v_hoy date := (now() AT TIME ZONE 'America/Asuncion')::date;
    v_cita integer; v_ant text; v_nuevo text; v_slot integer; v_estado_slot text; v_log integer; v_rec integer;
BEGIN
    SELECT id_usuario INTO v_usr FROM usuarios ORDER BY id_usuario LIMIT 1;

    -- Cita futura confirmada -> cancelar: libera el turno, guarda el motivo y el log
    SELECT c.id_cita INTO v_cita FROM citas c JOIN estados_citas e USING (id_estado_cita)
     WHERE e.cod_estado_cita IN ('AGENDADA', 'CONFIRMADA') AND c.cita_inicio::date > v_hoy AND c.id_slot_agenda IS NOT NULL
     ORDER BY c.id_cita LIMIT 1;
    IF v_cita IS NULL THEN
        PERFORM pg_temp.informar('sp_cambiar_estado_cita cancelar futura: OMITIDO (no hay cita futura)', true);
    ELSE
        SELECT id_slot_agenda INTO v_slot FROM citas WHERE id_cita = v_cita;
        BEGIN
            CALL sp_cambiar_estado_cita(v_cita, 'CANCELADA', v_usr, v_ant, v_nuevo, 'Prueba automatica');
            SELECT estado_slot INTO v_estado_slot FROM slots_agenda WHERE id_slot_agenda = v_slot;
            SELECT count(*) INTO v_log FROM citas_log_estados WHERE id_cita = v_cita AND motivo_cambio = 'Prueba automatica';
            PERFORM pg_temp.informar('sp_cambiar_estado_cita cancelar futura: estado nuevo y turno DISPONIBLE', v_nuevo = 'CANCELADA' AND v_estado_slot = 'DISPONIBLE', v_ant || ' -> ' || v_nuevo);
            PERFORM pg_temp.informar('sp_cambiar_estado_cita cancelar futura: deja el log y quita el turno de la cita',
                v_log = 1 AND (SELECT id_slot_agenda IS NULL FROM citas WHERE id_cita = v_cita));
            PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: cancelada de otro dia no se reabre',
                format('CALL sp_cambiar_estado_cita(%s, ''AGENDADA'', %s, NULL, NULL)', v_cita, v_usr), '%ya está cerrada%');
            RAISE EXCEPTION 'prueba' USING ERRCODE = 'PRB01';
        EXCEPTION WHEN SQLSTATE 'PRB01' THEN NULL;
        END;
        PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: cita futura no pasa a EN_CONSULTA',
            format('CALL sp_cambiar_estado_cita(%s, ''EN_CONSULTA'', %s, NULL, NULL)', v_cita, v_usr), '%día futuro%');
        PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: cita futura no pasa a AUSENTE',
            format('CALL sp_cambiar_estado_cita(%s, ''AUSENTE'', %s, NULL, NULL)', v_cita, v_usr), '%día futuro%');
    END IF;

    -- Cita completada: cerrada
    SELECT c.id_cita INTO v_cita FROM citas c JOIN estados_citas e USING (id_estado_cita) WHERE e.cod_estado_cita = 'COMPLETADA' ORDER BY c.id_cita LIMIT 1;
    IF v_cita IS NOT NULL THEN
        PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: completada no se reabre',
            format('CALL sp_cambiar_estado_cita(%s, ''AGENDADA'', %s, NULL, NULL)', v_cita, v_usr), '%ya está cerrada%');
    END IF;

    -- Cita de un dia anterior: solo estados finales
    SELECT c.id_cita INTO v_cita FROM citas c JOIN estados_citas e USING (id_estado_cita)
     WHERE e.cod_estado_cita = 'AGENDADA' AND c.cita_inicio::date < v_hoy ORDER BY c.id_cita LIMIT 1;
    IF v_cita IS NULL THEN
        PERFORM pg_temp.informar('sp_cambiar_estado_cita dia anterior: OMITIDO (no hay cita agendada de un dia anterior)', true);
    ELSE
        PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: dia anterior no se confirma',
            format('CALL sp_cambiar_estado_cita(%s, ''CONFIRMADA'', %s, NULL, NULL)', v_cita, v_usr), '%día anterior%');
        BEGIN
            CALL sp_cambiar_estado_cita(v_cita, 'AUSENTE', v_usr, v_ant, v_nuevo);
            PERFORM pg_temp.informar('sp_cambiar_estado_cita dia anterior: se cierra como AUSENTE', v_nuevo = 'AUSENTE');
            RAISE EXCEPTION 'prueba' USING ERRCODE = 'PRB01';
        EXCEPTION WHEN SQLSTATE 'PRB01' THEN NULL;
        END;
    END IF;

    -- Mismo dia (se mueve una cita a hoy dentro del sub-bloque): consulta, ausencia y correccion
    SELECT c.id_cita INTO v_cita FROM citas c JOIN estados_citas e USING (id_estado_cita)
     WHERE e.cod_estado_cita = 'CONFIRMADA' ORDER BY c.id_cita LIMIT 1;
    IF v_cita IS NULL THEN
        PERFORM pg_temp.informar('sp_cambiar_estado_cita mismo dia: OMITIDO (no hay cita confirmada)', true);
    ELSE
        BEGIN
            UPDATE citas SET cita_inicio = v_hoy + time '06:07', cita_fin = v_hoy + time '06:50' WHERE id_cita = v_cita;
            CALL sp_cambiar_estado_cita(v_cita, 'AUSENTE', v_usr, v_ant, v_nuevo);
            CALL sp_cambiar_estado_cita(v_cita, 'CONFIRMADA', v_usr, v_ant, v_nuevo);
            SELECT count(*) INTO v_rec FROM recordatorios WHERE id_cita = v_cita;
            PERFORM pg_temp.informar('sp_cambiar_estado_cita mismo dia: AUSENTE -> CONFIRMADA (correccion) y recordatorios', v_ant = 'AUSENTE' AND v_nuevo = 'CONFIRMADA' AND v_rec = 2);
            CALL sp_cambiar_estado_cita(v_cita, 'EN_CONSULTA', v_usr, v_ant, v_nuevo);
            PERFORM pg_temp.informar('sp_cambiar_estado_cita mismo dia: CONFIRMADA -> EN_CONSULTA', v_nuevo = 'EN_CONSULTA');
            CALL sp_cambiar_estado_cita(v_cita, 'COMPLETADA', v_usr, v_ant, v_nuevo);
            PERFORM pg_temp.informar('sp_cambiar_estado_cita mismo dia: EN_CONSULTA -> COMPLETADA', v_nuevo = 'COMPLETADA');
            RAISE EXCEPTION 'prueba' USING ERRCODE = 'PRB01';
        EXCEPTION WHEN SQLSTATE 'PRB01' THEN NULL;
        END;
    END IF;

    PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: cita o estado nulo', format('CALL sp_cambiar_estado_cita(NULL, ''CONFIRMADA'', %s, NULL, NULL)', v_usr), '%obligatorios%');
    PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: estado inexistente', format('CALL sp_cambiar_estado_cita(1, ''XXX'', %s, NULL, NULL)', v_usr), '%no encontrado%');
    PERFORM pg_temp.espera_error('sp_cambiar_estado_cita: cita inexistente', format('CALL sp_cambiar_estado_cita(-1, ''CONFIRMADA'', %s, NULL, NULL)', v_usr), '%no existe%');
END $$;
