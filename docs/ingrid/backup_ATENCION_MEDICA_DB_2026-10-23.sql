-- ============================================================================
--  BACKUP COMPLETO - Base de datos ATENCION_MEDICA_DB (Sistema Podologia Barreto)
--  Generado: 2026-10-23 con pg_dump (PostgreSQL 14.15)
--  Contenido: estructura + datos + secuencias + PK + FK + indices + vistas + funciones
--  Excluidas (sin uso en el sistema): OCUPACIONES, FICHAS, NOTIFICACIONES y sus secuencias.
--  Nota: ficha_medicacion_habitual se incluye aunque esta vacia (la usa el modulo Ficha Medica).
--
--  RESTAURAR (en una base vacia):
--    createdb -U postgres ATENCION_MEDICA_DB
--    psql -U postgres -d ATENCION_MEDICA_DB -f backup_ATENCION_MEDICA_DB_2026-10-23.sql
--  Las FK se crean al final del script (ALTER TABLE ... ADD CONSTRAINT ...
--  FOREIGN KEY), despues de cargar los datos, para respetar el orden.
-- ============================================================================
--
--  TABLAS INCLUIDAS (59):
--
--   agenda_medicas  (13 columnas, PK: id_agenda_medica)
--   alergias_paciente  (5 columnas, PK: id_alergia_paciente)
--   anamnesis_podologica  (8 columnas, PK: id_anamnesis)
--   auditoria_accesos  (8 columnas, PK: id_auditoria)
--   avisos_recordatorios  (13 columnas, PK: id_aviso)
--   cajas  (10 columnas, PK: id_caja)
--   citas  (8 columnas, PK: id_cita)
--   ciudades  (2 columnas, PK: id_ciudad)
--   cobranzas  (10 columnas, PK: id_cobranza)
--   consulta_diagnosticos  (7 columnas, PK: id_consulta_diagnostico)
--   consulta_insumos  (5 columnas, PK: id_consulta_insumo)
--   consulta_ordenes  (7 columnas, PK: id_consulta_orden)
--   consulta_procedimientos  (5 columnas, PK: id_consulta_procedimiento)
--   consultas  (20 columnas, PK: id_consulta)
--   consultorio  (9 columnas, PK: id_consultorio)
--   datos_emisor  (14 columnas, PK: id_emisor)
--   dias  (2 columnas, PK: id_dia)
--   disponibilidad_horaria  (7 columnas, PK: id_disponibilidad_horaria)
--   enfermedades  (4 columnas, PK: id_enfermedad)
--   especialidades  (2 columnas, PK: id_especialidad)
--   estado_citas  (2 columnas, PK: id_estado_cita)
--   estado_civiles  (2 columnas, PK: id_estado_civil)
--   estado_laborales  (2 columnas, PK: id_estado_laboral)
--   estados_factura  (2 columnas, PK: id_estado_factura)
--   factura_detalle  (8 columnas, PK: id_factura_detalle)
--   facturas  (24 columnas, PK: id_factura)
--   ficha_antecedentes_familiares  (4 columnas, PK: id_antecedente_familiar)
--   ficha_medica  (32 columnas, PK: id_ficha)
--   ficha_medicacion_habitual  (4 columnas, PK: id_ficha_medicacion)
--   formas_cobro  (3 columnas, PK: id_forma_cobro)
--   funcionarios  (8 columnas, PK: id_funcionario)
--   generos  (2 columnas, PK: id_genero)
--   grupos_sanguineos  (2 columnas, PK: id_grupo_sanguineo)
--   insumos  (9 columnas, PK: id_insumo)
--   justificativos  (8 columnas, PK: id_justificativo)
--   medicamentos  (7 columnas, PK: id_medicamento)
--   medicos  (3 columnas, PK: id_medico)
--   motivos_nota  (3 columnas, PK: id_motivo_nota)
--   notas  (13 columnas, PK: id_nota)
--   orden_analisis  (6 columnas, PK: id_orden_analisis)
--   orden_estudio  (6 columnas, PK: id_orden_estudio)
--   pacientes  (5 columnas, PK: id_paciente)
--   permisos_rol  (3 columnas, PK: id_rol, modulo)
--   personas  (9 columnas, PK: id_persona)
--   receta_detalle  (8 columnas, PK: id_receta_detalle)
--   recetas  (4 columnas, PK: id_receta)
--   roles  (2 columnas, PK: id_rol)
--   sala_atenciones  (2 columnas, PK: id_sala_atencion)
--   servicios_facturables  (5 columnas, PK: id_servicio)
--   signos_vitales  (17 columnas, PK: id_signos_vitales)
--   stock_insumos  (10 columnas, PK: id_movimiento)
--   tipo_orden_analisis  (3 columnas, PK: id_tipo_orden_analisis)
--   tipo_orden_estudio  (3 columnas, PK: id_tipo_orden_estudio)
--   tipos_alergia  (3 columnas, PK: id_tipo_alergia)
--   tipos_comprobante  (3 columnas, PK: id_tipo_comprobante)
--   tipos_iva  (3 columnas, PK: id_tipo_iva)
--   tratamientos  (5 columnas, PK: id_tratamiento)
--   turnos  (2 columnas, PK: id_turno)
--   usuarios  (8 columnas, PK: id_usuario)
--
--  RELACIONES (FOREIGN KEYS) - 85 en total:
--   tabla_hija (columna)  ->  tabla_padre(columna)   [reglas]  nombre_constraint
--
--   agenda_medicas                   (id_dia)  ->  dias(id_dia)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  agenda_medicas_id_dia_fkey
--   agenda_medicas                   (id_especialidad)  ->  especialidades(id_especialidad)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  agenda_medicas_id_especialidad_fkey
--   agenda_medicas                   (id_estado_laboral)  ->  estado_laborales(id_estado_laboral)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  agenda_medicas_id_estado_laboral_fkey
--   agenda_medicas                   (id_medico)  ->  medicos(id_medico)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  agenda_medicas_id_medico_fkey
--   agenda_medicas                   (id_sala_atencion)  ->  sala_atenciones(id_sala_atencion)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  agenda_medicas_id_sala_atencion_fkey
--   agenda_medicas                   (id_turno)  ->  turnos(id_turno)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  agenda_medicas_id_turno_fkey
--   agenda_medicas                   (id_funcionario)  ->  funcionarios(id_funcionario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_agenda_funcionario
--   alergias_paciente                (id_ficha)  ->  ficha_medica(id_ficha)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_alergia_ficha
--   alergias_paciente                (id_tipo_alergia)  ->  tipos_alergia(id_tipo_alergia)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_alergia_tipo
--   anamnesis_podologica             (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_anamnesis_consulta
--   auditoria_accesos                (id_usuario)  ->  usuarios(id_usuario)   [ON DELETE SET NULL / ON UPDATE NO ACTION]  auditoria_accesos_id_usuario_fkey
--   avisos_recordatorios             (id_cita)  ->  citas(id_cita)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  avisos_recordatorios_id_cita_fkey
--   avisos_recordatorios             (id_funcionario)  ->  funcionarios(id_funcionario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  avisos_recordatorios_id_funcionario_fkey
--   cajas                            (id_usuario)  ->  usuarios(id_usuario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_caja_usuario
--   citas                            (id_disponibilidad_horaria)  ->  disponibilidad_horaria(id_disponibilidad_horaria)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  citas_id_disponibilidad_horaria_fkey
--   citas                            (id_estado_cita)  ->  estado_citas(id_estado_cita)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  citas_id_estado_cita_fkey
--   citas                            (id_paciente)  ->  pacientes(id_paciente)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  citas_id_paciente_fkey
--   citas                            (id_funcionario)  ->  funcionarios(id_funcionario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_cita_funcionario
--   cobranzas                        (id_caja)  ->  cajas(id_caja)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_cobranza_caja
--   cobranzas                        (id_factura)  ->  facturas(id_factura)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_cobranza_factura
--   cobranzas                        (id_forma_cobro)  ->  formas_cobro(id_forma_cobro)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_cobranza_forma
--   consulta_diagnosticos            (id_consulta)  ->  consultas(id_consulta)   [ON DELETE CASCADE / ON UPDATE NO ACTION]  consulta_diagnosticos_id_consulta_fkey
--   consulta_diagnosticos            (id_enfermedad)  ->  enfermedades(id_enfermedad)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  consulta_diagnosticos_id_enfermedad_fkey
--   consulta_diagnosticos            (id_tratamiento)  ->  tratamientos(id_tratamiento)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  consulta_diagnosticos_id_tratamiento_fkey
--   consulta_insumos                 (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consulta_insumos_consulta
--   consulta_insumos                 (id_insumo)  ->  insumos(id_insumo)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consulta_insumos_insumo
--   consulta_ordenes                 (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_cord_consulta
--   consulta_procedimientos          (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_cp_consulta
--   consulta_procedimientos          (id_servicio)  ->  servicios_facturables(id_servicio)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_cp_servicio
--   consultas                        (id_cita)  ->  citas(id_cita)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  consultas_id_cita_fkey
--   consultas                        (id_tipo_orden_analisis)  ->  tipo_orden_analisis(id_tipo_orden_analisis)   [ON DELETE SET NULL / ON UPDATE CASCADE]  consultas_id_tipo_orden_analisis_fkey
--   consultas                        (id_tipo_orden_estudio)  ->  tipo_orden_estudio(id_tipo_orden_estudio)   [ON DELETE SET NULL / ON UPDATE CASCADE]  consultas_id_tipo_orden_estudio_fkey
--   consultas                        (id_consultorio)  ->  consultorio(id_consultorio)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consulta_consultorio
--   consultas                        (id_funcionario)  ->  funcionarios(id_funcionario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consulta_funcionario
--   consultas                        (id_cita)  ->  citas(id_cita)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consultas_cita
--   consultas                        (id_enfermedad)  ->  enfermedades(id_enfermedad)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consultas_enfermedad
--   consultas                        (id_tipo_orden_analisis)  ->  tipo_orden_analisis(id_tipo_orden_analisis)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consultas_tipo_analisis
--   consultas                        (id_tipo_orden_estudio)  ->  tipo_orden_estudio(id_tipo_orden_estudio)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consultas_tipo_estudio
--   consultas                        (id_tratamiento)  ->  tratamientos(id_tratamiento)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consultas_tratamiento
--   consultorio                      (id_ciudad)  ->  ciudades(id_ciudad)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_consultorio_ciudad
--   disponibilidad_horaria           (id_agenda_medica)  ->  agenda_medicas(id_agenda_medica)   [ON DELETE CASCADE / ON UPDATE CASCADE]  disponibilidad_horaria_id_agenda_medica_fkey
--   factura_detalle                  (id_factura)  ->  facturas(id_factura)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_detalle_factura
--   factura_detalle                  (id_tipo_iva)  ->  tipos_iva(id_tipo_iva)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_detalle_iva
--   factura_detalle                  (id_servicio)  ->  servicios_facturables(id_servicio)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_detalle_servicio
--   facturas                         (id_caja)  ->  cajas(id_caja)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_factura_caja
--   facturas                         (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_factura_consulta
--   facturas                         (id_emisor)  ->  datos_emisor(id_emisor)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_factura_emisor
--   facturas                         (id_estado_factura)  ->  estados_factura(id_estado_factura)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_factura_estado
--   facturas                         (id_funcionario)  ->  funcionarios(id_funcionario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_factura_funcionario
--   ficha_antecedentes_familiares    (id_ficha)  ->  ficha_medica(id_ficha)   [ON DELETE CASCADE / ON UPDATE NO ACTION]  ficha_antecedentes_familiares_id_ficha_fkey
--   ficha_medica                     (id_grupo_sanguineo)  ->  grupos_sanguineos(id_grupo_sanguineo)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_ficha_grupo_sang
--   ficha_medica                     (id_paciente)  ->  pacientes(id_paciente)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_ficha_paciente
--   ficha_medicacion_habitual        (id_ficha)  ->  ficha_medica(id_ficha)   [ON DELETE CASCADE / ON UPDATE NO ACTION]  ficha_medicacion_habitual_id_ficha_fkey
--   ficha_medicacion_habitual        (id_medicamento)  ->  medicamentos(id_medicamento)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  ficha_medicacion_habitual_id_medicamento_fkey
--   funcionarios                     (id_consultorio)  ->  consultorio(id_consultorio)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_func_consultorio
--   funcionarios                     (id_persona)  ->  personas(id_persona)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_func_persona
--   funcionarios                     (id_rol)  ->  roles(id_rol)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_func_rol
--   funcionarios                     (id_usuario)  ->  usuarios(id_usuario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_func_usuario
--   insumos                          (id_tipo_iva)  ->  tipos_iva(id_tipo_iva)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_insumo_tipo_iva
--   justificativos                   (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_justificativos_consulta
--   medicos                          (id_persona)  ->  personas(id_persona)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  medicos_id_persona_fkey
--   motivos_nota                     (id_tipo_comprobante)  ->  tipos_comprobante(id_tipo_comprobante)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_motivo_tipo
--   notas                            (id_factura)  ->  facturas(id_factura)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_nota_factura
--   notas                            (id_motivo_nota)  ->  motivos_nota(id_motivo_nota)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_nota_motivo
--   notas                            (id_tipo_comprobante)  ->  tipos_comprobante(id_tipo_comprobante)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_nota_tipo
--   notas                            (id_usuario)  ->  usuarios(id_usuario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_nota_usuario
--   orden_analisis                   (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_orden_analisis_consulta
--   orden_analisis                   (id_tipo_orden_analisis)  ->  tipo_orden_analisis(id_tipo_orden_analisis)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  orden_analisis_id_tipo_orden_analisis_fkey
--   orden_estudio                    (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_orden_estudio_consulta
--   orden_estudio                    (id_tipo_orden_estudio)  ->  tipo_orden_estudio(id_tipo_orden_estudio)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  orden_estudio_id_tipo_orden_estudio_fkey
--   pacientes                        (id_persona)  ->  personas(id_persona)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  pacientes_id_persona_fkey
--   permisos_rol                     (id_rol)  ->  roles(id_rol)   [ON DELETE CASCADE / ON UPDATE NO ACTION]  permisos_rol_id_rol_fkey
--   personas                         (id_ciudad)  ->  ciudades(id_ciudad)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  personas_id_ciudad_fkey
--   personas                         (id_estado_civil)  ->  estado_civiles(id_estado_civil)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  personas_id_estado_civil_fkey
--   personas                         (id_genero)  ->  generos(id_genero)   [ON DELETE RESTRICT / ON UPDATE CASCADE]  personas_id_genero_fkey
--   receta_detalle                   (id_medicamento)  ->  medicamentos(id_medicamento)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_receta_detalle_medicamento
--   receta_detalle                   (id_receta)  ->  recetas(id_receta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_receta_detalle_receta
--   recetas                          (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_recetas_consulta
--   servicios_facturables            (id_tipo_iva)  ->  tipos_iva(id_tipo_iva)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_servicio_iva
--   signos_vitales                   (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_signos_consulta
--   stock_insumos                    (id_consulta)  ->  consultas(id_consulta)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_stock_consulta
--   stock_insumos                    (id_insumo)  ->  insumos(id_insumo)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_stock_insumo
--   stock_insumos                    (id_usuario)  ->  usuarios(id_usuario)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_stock_usuario
--   tratamientos                     (id_enfermedad)  ->  enfermedades(id_enfermedad)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_tratamientos_enfermedad
--   usuarios                         (id_rol)  ->  roles(id_rol)   [ON DELETE NO ACTION / ON UPDATE NO ACTION]  fk_usuario_rol
--
-- ============================================================================

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15
-- Dumped by pg_dump version 14.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: fn_descontar_stock(integer, numeric, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_descontar_stock(p_id_insumo integer, p_cantidad numeric, p_id_consulta integer, p_id_usuario integer, p_motivo character varying DEFAULT 'Consulta'::character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_stock_anterior numeric;
    v_stock_nuevo    numeric;
BEGIN
    SELECT stock_actual INTO v_stock_anterior
    FROM public.insumos
    WHERE id_insumo = p_id_insumo
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Insumo % no encontrado', p_id_insumo;
    END IF;

    v_stock_nuevo := v_stock_anterior - p_cantidad;

    -- Permitir stock negativo con advertencia (no bloqueamos la consulta)
    UPDATE public.insumos
    SET stock_actual = v_stock_nuevo
    WHERE id_insumo = p_id_insumo;

    INSERT INTO public.stock_insumos (
        id_insumo, tipo_movimiento, cantidad,
        stock_anterior, stock_nuevo,
        motivo, id_consulta, id_usuario
    ) VALUES (
        p_id_insumo, 'SALIDA', p_cantidad,
        v_stock_anterior, v_stock_nuevo,
        p_motivo || ' #' || COALESCE(p_id_consulta::text, '?'),
        p_id_consulta, p_id_usuario
    );

    RETURN TRUE;
END;
$$;


--
-- Name: FUNCTION fn_descontar_stock(p_id_insumo integer, p_cantidad numeric, p_id_consulta integer, p_id_usuario integer, p_motivo character varying); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_descontar_stock(p_id_insumo integer, p_cantidad numeric, p_id_consulta integer, p_id_usuario integer, p_motivo character varying) IS 'Descuenta stock de un insumo y registra el movimiento. Llamada desde ConsultaDao al guardar insumos.';


--
-- Name: fn_reponer_stock(integer, numeric, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fn_reponer_stock(p_id_insumo integer, p_cantidad numeric, p_id_usuario integer, p_motivo character varying DEFAULT 'Reposición'::character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_stock_anterior numeric;
    v_stock_nuevo    numeric;
BEGIN
    SELECT stock_actual INTO v_stock_anterior
    FROM public.insumos
    WHERE id_insumo = p_id_insumo
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Insumo % no encontrado', p_id_insumo;
    END IF;

    v_stock_nuevo := v_stock_anterior + p_cantidad;

    UPDATE public.insumos
    SET stock_actual = v_stock_nuevo
    WHERE id_insumo = p_id_insumo;

    INSERT INTO public.stock_insumos (
        id_insumo, tipo_movimiento, cantidad,
        stock_anterior, stock_nuevo,
        motivo, id_consulta, id_usuario
    ) VALUES (
        p_id_insumo, 'ENTRADA', p_cantidad,
        v_stock_anterior, v_stock_nuevo,
        p_motivo, NULL, p_id_usuario
    );

    RETURN TRUE;
END;
$$;


--
-- Name: FUNCTION fn_reponer_stock(p_id_insumo integer, p_cantidad numeric, p_id_usuario integer, p_motivo character varying); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.fn_reponer_stock(p_id_insumo integer, p_cantidad numeric, p_id_usuario integer, p_motivo character varying) IS 'Suma stock a un insumo y registra el movimiento de entrada. Llamada desde InsumoDao al reponer.';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agenda_medicas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.agenda_medicas (
    id_agenda_medica integer NOT NULL,
    id_medico integer NOT NULL,
    id_especialidad integer NOT NULL,
    id_turno integer NOT NULL,
    id_dia integer NOT NULL,
    id_estado_laboral integer NOT NULL,
    id_sala_atencion integer NOT NULL,
    id_funcionario integer,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    hora_inicio time without time zone,
    hora_fin time without time zone,
    fecha_desde date,
    fecha_hasta date
);


--
-- Name: agenda_medicas_id_agenda_medica_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.agenda_medicas_id_agenda_medica_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: agenda_medicas_id_agenda_medica_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.agenda_medicas_id_agenda_medica_seq OWNED BY public.agenda_medicas.id_agenda_medica;


--
-- Name: alergias_paciente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alergias_paciente (
    id_alergia_paciente integer NOT NULL,
    id_ficha integer NOT NULL,
    id_tipo_alergia integer NOT NULL,
    descripcion character varying(300) NOT NULL,
    gravedad character varying(50)
);


--
-- Name: TABLE alergias_paciente; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.alergias_paciente IS 'Alergias conocidas del paciente registradas en su ficha';


--
-- Name: COLUMN alergias_paciente.gravedad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.alergias_paciente.gravedad IS 'Nivel de gravedad: Leve, Moderada, Grave, Anafilaxia';


--
-- Name: alergias_paciente_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.alergias_paciente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: alergias_paciente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.alergias_paciente_id_seq OWNED BY public.alergias_paciente.id_alergia_paciente;


--
-- Name: anamnesis_podologica; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.anamnesis_podologica (
    id_anamnesis integer NOT NULL,
    id_consulta integer NOT NULL,
    tipo_pie character varying(150),
    alteracion_de character varying(300),
    onicopatias character varying(300),
    area_trabajo text,
    diagnostico_podologico text,
    proxima_cita date
);


--
-- Name: TABLE anamnesis_podologica; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.anamnesis_podologica IS 'Anamnesis podológica específica por consulta';


--
-- Name: COLUMN anamnesis_podologica.tipo_pie; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anamnesis_podologica.tipo_pie IS 'Tipo de pie: Plano, Cavo, Normal, Mixto';


--
-- Name: COLUMN anamnesis_podologica.alteracion_de; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anamnesis_podologica.alteracion_de IS 'Descripción de alteraciones encontradas';


--
-- Name: COLUMN anamnesis_podologica.onicopatias; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anamnesis_podologica.onicopatias IS 'Descripción de patologías ungueales';


--
-- Name: COLUMN anamnesis_podologica.area_trabajo; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anamnesis_podologica.area_trabajo IS 'Área de trabajo: descripción de zonas del pie tratadas';


--
-- Name: COLUMN anamnesis_podologica.diagnostico_podologico; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anamnesis_podologica.diagnostico_podologico IS 'Diagnóstico podológico específico de la consulta';


--
-- Name: COLUMN anamnesis_podologica.proxima_cita; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anamnesis_podologica.proxima_cita IS 'Fecha sugerida para la próxima consulta';


--
-- Name: anamnesis_podologica_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.anamnesis_podologica_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: anamnesis_podologica_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.anamnesis_podologica_id_seq OWNED BY public.anamnesis_podologica.id_anamnesis;


--
-- Name: auditoria_accesos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auditoria_accesos (
    id_auditoria integer NOT NULL,
    fecha timestamp without time zone DEFAULT now() NOT NULL,
    id_usuario integer,
    usuario character varying(60),
    evento character varying(30) NOT NULL,
    detalle text,
    ip character varying(45),
    navegador character varying(255)
);


--
-- Name: auditoria_accesos_id_auditoria_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auditoria_accesos_id_auditoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auditoria_accesos_id_auditoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auditoria_accesos_id_auditoria_seq OWNED BY public.auditoria_accesos.id_auditoria;


--
-- Name: avisos_recordatorios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.avisos_recordatorios (
    id_aviso integer NOT NULL,
    id_cita integer NOT NULL,
    fecha_programada timestamp without time zone NOT NULL,
    fecha_envio timestamp without time zone,
    metodo_envio character varying(50) DEFAULT 'whatsapp'::character varying,
    mensaje text,
    estado character varying(20) DEFAULT 'pendiente'::character varying,
    destinatario character varying(255),
    intentos_envio integer DEFAULT 0,
    observacion text,
    respuesta character varying(20),
    fecha_respuesta timestamp without time zone,
    id_funcionario integer
);


--
-- Name: avisos_recordatorios_id_aviso_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.avisos_recordatorios_id_aviso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: avisos_recordatorios_id_aviso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.avisos_recordatorios_id_aviso_seq OWNED BY public.avisos_recordatorios.id_aviso;


--
-- Name: cajas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cajas (
    id_caja integer NOT NULL,
    id_usuario integer NOT NULL,
    fecha_apertura timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    monto_apertura numeric(12,2) DEFAULT 0 NOT NULL,
    fecha_cierre timestamp without time zone,
    monto_cierre_declarado numeric(12,2),
    monto_cierre_sistema numeric(12,2),
    diferencia numeric(12,2),
    observaciones_cierre text,
    estado character varying(20) DEFAULT 'Abierta'::character varying NOT NULL
);


--
-- Name: TABLE cajas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.cajas IS 'Apertura y cierre de caja por usuario/turno';


--
-- Name: COLUMN cajas.monto_apertura; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.cajas.monto_apertura IS 'Monto en efectivo con el que se abre la caja';


--
-- Name: COLUMN cajas.monto_cierre_sistema; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.cajas.monto_cierre_sistema IS 'Apertura + cobros en efectivo registrados durante el turno';


--
-- Name: COLUMN cajas.diferencia; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.cajas.diferencia IS 'monto_cierre_declarado - monto_cierre_sistema (sobrante/faltante)';


--
-- Name: cajas_id_caja_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cajas_id_caja_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cajas_id_caja_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cajas_id_caja_seq OWNED BY public.cajas.id_caja;


--
-- Name: citas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.citas (
    id_cita integer NOT NULL,
    id_disponibilidad_horaria integer NOT NULL,
    id_paciente integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    observacion character varying(200),
    id_estado_cita integer NOT NULL,
    id_funcionario integer,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: citas_id_cita_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.citas_id_cita_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: citas_id_cita_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.citas_id_cita_seq OWNED BY public.citas.id_cita;


--
-- Name: ciudades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ciudades (
    id_ciudad integer NOT NULL,
    descripcion character varying(60)
);


--
-- Name: ciudades_id_ciudad_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ciudades_id_ciudad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ciudades_id_ciudad_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ciudades_id_ciudad_seq OWNED BY public.ciudades.id_ciudad;


--
-- Name: cobranzas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cobranzas (
    id_cobranza integer NOT NULL,
    id_factura integer NOT NULL,
    id_caja integer NOT NULL,
    id_forma_cobro integer NOT NULL,
    monto numeric(12,2) NOT NULL,
    referencia character varying(100),
    banco character varying(100),
    fecha_cobro timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    numero_recibo character varying(20) NOT NULL,
    observaciones text
);


--
-- Name: TABLE cobranzas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.cobranzas IS 'Pagos recibidos, pueden ser parciales y de distintas formas de cobro sobre la misma factura';


--
-- Name: COLUMN cobranzas.referencia; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.cobranzas.referencia IS 'Número de cheque, lote de tarjeta, etc. según forma de cobro';


--
-- Name: cobranzas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cobranzas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cobranzas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cobranzas_id_seq OWNED BY public.cobranzas.id_cobranza;


--
-- Name: consulta_diagnosticos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consulta_diagnosticos (
    id_consulta_diagnostico integer NOT NULL,
    id_consulta integer NOT NULL,
    id_enfermedad integer,
    id_tratamiento integer,
    diagnostico text,
    tratamiento text,
    orden smallint DEFAULT 1 NOT NULL,
    CONSTRAINT chk_diag_con_contenido CHECK (((id_enfermedad IS NOT NULL) OR (COALESCE(TRIM(BOTH FROM diagnostico), ''::text) <> ''::text)))
);


--
-- Name: consulta_diagnosticos_id_consulta_diagnostico_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consulta_diagnosticos_id_consulta_diagnostico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consulta_diagnosticos_id_consulta_diagnostico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consulta_diagnosticos_id_consulta_diagnostico_seq OWNED BY public.consulta_diagnosticos.id_consulta_diagnostico;


--
-- Name: consulta_insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consulta_insumos (
    id_consulta_insumo integer NOT NULL,
    id_consulta integer NOT NULL,
    id_insumo integer NOT NULL,
    cantidad numeric(10,2) DEFAULT 1 NOT NULL,
    observacion text
);


--
-- Name: TABLE consulta_insumos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.consulta_insumos IS 'Insumos médicos utilizados durante la consulta (opcional)';


--
-- Name: COLUMN consulta_insumos.cantidad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consulta_insumos.cantidad IS 'Cantidad del insumo consumido en la consulta';


--
-- Name: consulta_insumos_id_consulta_insumo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consulta_insumos_id_consulta_insumo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consulta_insumos_id_consulta_insumo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consulta_insumos_id_consulta_insumo_seq OWNED BY public.consulta_insumos.id_consulta_insumo;


--
-- Name: consulta_ordenes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consulta_ordenes (
    id_consulta_orden integer NOT NULL,
    id_consulta integer NOT NULL,
    tipo character varying(10) NOT NULL,
    id_tipo_orden integer NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE,
    fecha_vencimiento date,
    observacion character varying(300),
    CONSTRAINT chk_tipo CHECK (((tipo)::text = ANY ((ARRAY['estudio'::character varying, 'analisis'::character varying])::text[])))
);


--
-- Name: TABLE consulta_ordenes; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.consulta_ordenes IS 'Órdenes de estudio y análisis múltiples por consulta';


--
-- Name: consulta_ordenes_id_consulta_orden_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consulta_ordenes_id_consulta_orden_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consulta_ordenes_id_consulta_orden_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consulta_ordenes_id_consulta_orden_seq OWNED BY public.consulta_ordenes.id_consulta_orden;


--
-- Name: consulta_procedimientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consulta_procedimientos (
    id_consulta_procedimiento integer NOT NULL,
    id_consulta integer NOT NULL,
    id_servicio integer NOT NULL,
    cantidad numeric(10,2) DEFAULT 1 NOT NULL,
    observacion character varying(300)
);


--
-- Name: TABLE consulta_procedimientos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.consulta_procedimientos IS 'Procedimientos/servicios realizados en la consulta. Sin precios — precios solo en facturación';


--
-- Name: consulta_procedimientos_id_consulta_procedimiento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consulta_procedimientos_id_consulta_procedimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consulta_procedimientos_id_consulta_procedimiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consulta_procedimientos_id_consulta_procedimiento_seq OWNED BY public.consulta_procedimientos.id_consulta_procedimiento;


--
-- Name: consultas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultas (
    id_consulta integer NOT NULL,
    id_cita integer NOT NULL,
    id_tipo_orden_estudio integer,
    fecha_emision_estudio date,
    fecha_vencimiento_estudio date,
    id_tipo_orden_analisis integer,
    fecha_emision_analisis date,
    fecha_vencimiento_analisis date,
    motivo_consulta text NOT NULL,
    diagnostico text,
    tratamiento text,
    observaciones text,
    fecha_consulta timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_enfermedad integer,
    id_tratamiento integer,
    requiere_orden_estudio boolean DEFAULT false,
    requiere_orden_analisis boolean DEFAULT false,
    id_funcionario integer,
    id_consultorio integer,
    diagnostico_presuntivo text
);


--
-- Name: TABLE consultas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.consultas IS 'Registro de consultas médicas realizadas';


--
-- Name: COLUMN consultas.id_cita; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.id_cita IS 'Cita médica asociada a la consulta';


--
-- Name: COLUMN consultas.id_tipo_orden_estudio; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.id_tipo_orden_estudio IS 'Tipo de orden de estudio emitida (opcional)';


--
-- Name: COLUMN consultas.fecha_emision_estudio; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.fecha_emision_estudio IS 'Fecha de emisión de la orden de estudio';


--
-- Name: COLUMN consultas.fecha_vencimiento_estudio; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.fecha_vencimiento_estudio IS 'Fecha de vencimiento de la orden de estudio';


--
-- Name: COLUMN consultas.id_tipo_orden_analisis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.id_tipo_orden_analisis IS 'Tipo de orden de análisis emitida (opcional)';


--
-- Name: COLUMN consultas.fecha_emision_analisis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.fecha_emision_analisis IS 'Fecha de emisión de la orden de análisis';


--
-- Name: COLUMN consultas.fecha_vencimiento_analisis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.fecha_vencimiento_analisis IS 'Fecha de vencimiento de la orden de análisis';


--
-- Name: COLUMN consultas.motivo_consulta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.motivo_consulta IS 'Razón por la que el paciente consulta';


--
-- Name: COLUMN consultas.diagnostico; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.diagnostico IS 'Diagnóstico médico del paciente';


--
-- Name: COLUMN consultas.tratamiento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.tratamiento IS 'Tratamiento prescrito';


--
-- Name: COLUMN consultas.observaciones; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.observaciones IS 'Observaciones adicionales del médico';


--
-- Name: COLUMN consultas.id_enfermedad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.id_enfermedad IS 'Diagnóstico seleccionado del catálogo de enfermedades';


--
-- Name: COLUMN consultas.id_tratamiento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.id_tratamiento IS 'Tratamiento asignado según el diagnóstico';


--
-- Name: COLUMN consultas.requiere_orden_estudio; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.requiere_orden_estudio IS 'Indica si la consulta genera orden de estudio';


--
-- Name: COLUMN consultas.requiere_orden_analisis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.requiere_orden_analisis IS 'Indica si la consulta genera orden de análisis';


--
-- Name: COLUMN consultas.diagnostico_presuntivo; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.diagnostico_presuntivo IS 'Sospecha clínica escrita por el profesional; se imprime en las órdenes';


--
-- Name: consultas_id_consulta_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consultas_id_consulta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consultas_id_consulta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consultas_id_consulta_seq OWNED BY public.consultas.id_consulta;


--
-- Name: consultorio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultorio (
    id_consultorio integer NOT NULL,
    nombre character varying(200) NOT NULL,
    ruc character varying(20),
    direccion character varying(300),
    telefono character varying(50),
    email character varying(150),
    id_ciudad integer,
    estado boolean DEFAULT true,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: consultorio_id_consultorio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consultorio_id_consultorio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consultorio_id_consultorio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consultorio_id_consultorio_seq OWNED BY public.consultorio.id_consultorio;


--
-- Name: datos_emisor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.datos_emisor (
    id_emisor integer NOT NULL,
    razon_social character varying(200) NOT NULL,
    nombre_fantasia character varying(200),
    ruc character varying(20) NOT NULL,
    timbrado character varying(20) NOT NULL,
    fecha_inicio_vigencia date NOT NULL,
    fecha_fin_vigencia date NOT NULL,
    punto_expedicion character varying(3) DEFAULT '001'::character varying NOT NULL,
    establecimiento character varying(3) DEFAULT '001'::character varying NOT NULL,
    direccion character varying(300),
    telefono character varying(50),
    estado boolean DEFAULT true,
    codigo_control character varying(20),
    modalidad character varying(30) DEFAULT 'Factura Virtual'::character varying
);


--
-- Name: TABLE datos_emisor; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.datos_emisor IS 'Datos fiscales del consultorio (emisor de facturas) - RUC y Timbrado vigente';


--
-- Name: COLUMN datos_emisor.punto_expedicion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.datos_emisor.punto_expedicion IS 'Código de punto de expedición, 3 dígitos, Ej: 001';


--
-- Name: COLUMN datos_emisor.establecimiento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.datos_emisor.establecimiento IS 'Código de establecimiento, 3 dígitos, Ej: 001';


--
-- Name: COLUMN datos_emisor.codigo_control; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.datos_emisor.codigo_control IS 'Código de Control (CSC) impreso en la factura virtual / QR';


--
-- Name: COLUMN datos_emisor.modalidad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.datos_emisor.modalidad IS 'Modalidad de facturación: Factura Virtual, Factura Preimpresa, etc.';


--
-- Name: datos_emisor_id_emisor_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.datos_emisor_id_emisor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: datos_emisor_id_emisor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.datos_emisor_id_emisor_seq OWNED BY public.datos_emisor.id_emisor;


--
-- Name: dias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dias (
    id_dia integer NOT NULL,
    descripcion character varying(60)
);


--
-- Name: dias_id_dia_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dias_id_dia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dias_id_dia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dias_id_dia_seq OWNED BY public.dias.id_dia;


--
-- Name: disponibilidad_horaria; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.disponibilidad_horaria (
    id_disponibilidad_horaria integer NOT NULL,
    id_agenda_medica integer NOT NULL,
    fecha date NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fin time without time zone NOT NULL,
    estado boolean DEFAULT true,
    bloqueado boolean DEFAULT false NOT NULL
);


--
-- Name: disponibilidad_horaria_id_disponibilidad_horaria_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.disponibilidad_horaria_id_disponibilidad_horaria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: disponibilidad_horaria_id_disponibilidad_horaria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.disponibilidad_horaria_id_disponibilidad_horaria_seq OWNED BY public.disponibilidad_horaria.id_disponibilidad_horaria;


--
-- Name: enfermedades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enfermedades (
    id_enfermedad integer NOT NULL,
    codigo_cie character varying(10),
    descripcion character varying(200) NOT NULL,
    estado boolean DEFAULT true
);


--
-- Name: TABLE enfermedades; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.enfermedades IS 'Catálogo de enfermedades / diagnósticos (referencia CIE-10)';


--
-- Name: COLUMN enfermedades.codigo_cie; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.enfermedades.codigo_cie IS 'Código CIE-10 opcional para interoperabilidad';


--
-- Name: COLUMN enfermedades.descripcion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.enfermedades.descripcion IS 'Nombre de la enfermedad o diagnóstico';


--
-- Name: enfermedades_id_enfermedad_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enfermedades_id_enfermedad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: enfermedades_id_enfermedad_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enfermedades_id_enfermedad_seq OWNED BY public.enfermedades.id_enfermedad;


--
-- Name: especialidades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.especialidades (
    id_especialidad integer NOT NULL,
    descripcion character varying(60)
);


--
-- Name: especialidades_id_especialidad_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.especialidades_id_especialidad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: especialidades_id_especialidad_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.especialidades_id_especialidad_seq OWNED BY public.especialidades.id_especialidad;


--
-- Name: estado_citas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estado_citas (
    id_estado_cita integer NOT NULL,
    descripcion character varying(60) NOT NULL
);


--
-- Name: estado_citas_id_estado_cita_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estado_citas_id_estado_cita_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: estado_citas_id_estado_cita_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estado_citas_id_estado_cita_seq OWNED BY public.estado_citas.id_estado_cita;


--
-- Name: estado_civiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estado_civiles (
    id_estado_civil integer NOT NULL,
    descripcion character varying(60)
);


--
-- Name: estado_civiles_id_estado_civil_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estado_civiles_id_estado_civil_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: estado_civiles_id_estado_civil_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estado_civiles_id_estado_civil_seq OWNED BY public.estado_civiles.id_estado_civil;


--
-- Name: estado_laborales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estado_laborales (
    id_estado_laboral integer NOT NULL,
    descripcion character varying(60)
);


--
-- Name: estado_laborales_id_estado_laboral_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estado_laborales_id_estado_laboral_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: estado_laborales_id_estado_laboral_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estado_laborales_id_estado_laboral_seq OWNED BY public.estado_laborales.id_estado_laboral;


--
-- Name: estados_factura; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estados_factura (
    id_estado_factura integer NOT NULL,
    descripcion character varying(40) NOT NULL
);


--
-- Name: estados_factura_id_estado_factura_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estados_factura_id_estado_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: estados_factura_id_estado_factura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estados_factura_id_estado_factura_seq OWNED BY public.estados_factura.id_estado_factura;


--
-- Name: factura_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.factura_detalle (
    id_factura_detalle integer NOT NULL,
    id_factura integer NOT NULL,
    id_servicio integer,
    descripcion character varying(300) NOT NULL,
    cantidad numeric(10,2) DEFAULT 1 NOT NULL,
    precio_unitario numeric(12,2) NOT NULL,
    id_tipo_iva integer NOT NULL,
    subtotal numeric(12,2) NOT NULL
);


--
-- Name: TABLE factura_detalle; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.factura_detalle IS 'Ítems individuales de cada factura (servicios y/o insumos cobrables)';


--
-- Name: factura_detalle_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.factura_detalle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: factura_detalle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.factura_detalle_id_seq OWNED BY public.factura_detalle.id_factura_detalle;


--
-- Name: facturas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facturas (
    id_factura integer NOT NULL,
    id_consulta integer NOT NULL,
    id_caja integer,
    id_emisor integer NOT NULL,
    establecimiento character varying(3) NOT NULL,
    punto_expedicion character varying(3) NOT NULL,
    numero_factura character varying(7) NOT NULL,
    timbrado character varying(20) NOT NULL,
    ruc_ci_cliente character varying(20) NOT NULL,
    nombre_cliente character varying(300) NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE NOT NULL,
    condicion_venta character varying(20) DEFAULT 'Contado'::character varying NOT NULL,
    numero_nota_remision character varying(20),
    subtotal_exento numeric(12,2) DEFAULT 0 NOT NULL,
    subtotal_5 numeric(12,2) DEFAULT 0 NOT NULL,
    subtotal_10 numeric(12,2) DEFAULT 0 NOT NULL,
    iva_5 numeric(12,2) DEFAULT 0 NOT NULL,
    iva_10 numeric(12,2) DEFAULT 0 NOT NULL,
    total numeric(12,2) DEFAULT 0 NOT NULL,
    saldo_pendiente numeric(12,2) DEFAULT 0 NOT NULL,
    id_estado_factura integer NOT NULL,
    observaciones text,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_funcionario integer
);


--
-- Name: TABLE facturas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.facturas IS 'Encabezado de factura legal vinculada 1 a 1 con una consulta';


--
-- Name: COLUMN facturas.numero_factura; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.facturas.numero_factura IS 'Correlativo de 7 dígitos dentro del establecimiento+punto de expedición';


--
-- Name: COLUMN facturas.saldo_pendiente; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.facturas.saldo_pendiente IS 'Total menos cobranzas ya aplicadas; 0 = pagada completamente';


--
-- Name: facturas_id_factura_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.facturas_id_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: facturas_id_factura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.facturas_id_factura_seq OWNED BY public.facturas.id_factura;


--
-- Name: ficha_antecedentes_familiares; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ficha_antecedentes_familiares (
    id_antecedente_familiar integer NOT NULL,
    id_ficha integer NOT NULL,
    enfermedad character varying(150) NOT NULL,
    parentesco character varying(150)
);


--
-- Name: ficha_antecedentes_familiares_id_antecedente_familiar_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ficha_antecedentes_familiares_id_antecedente_familiar_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ficha_antecedentes_familiares_id_antecedente_familiar_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ficha_antecedentes_familiares_id_antecedente_familiar_seq OWNED BY public.ficha_antecedentes_familiares.id_antecedente_familiar;


--
-- Name: ficha_medica; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ficha_medica (
    id_ficha integer NOT NULL,
    id_paciente integer NOT NULL,
    id_grupo_sanguineo integer,
    peso_habitual numeric(5,2),
    talla numeric(5,2),
    enfermedades_cronicas text,
    antecedentes_quirurgicos text,
    antecedentes_familiares text,
    medicacion_habitual text,
    tabaquismo boolean DEFAULT false,
    alcoholismo boolean DEFAULT false,
    actividad_fisica boolean DEFAULT false,
    detalle_habitos text,
    observaciones text,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ocupacion character varying(150),
    numero_calzado character varying(10),
    toma_medicamento boolean DEFAULT false,
    alergia_medicamento boolean DEFAULT false,
    padece_diabetes boolean DEFAULT false,
    padece_hta boolean DEFAULT false,
    padece_artritis boolean DEFAULT false,
    padece_artrosis boolean DEFAULT false,
    padece_osteoporosis boolean DEFAULT false,
    padece_otro character varying(300),
    fam_diabetes boolean DEFAULT false,
    fam_diabetes_esp character varying(200),
    fam_hta boolean DEFAULT false,
    fam_hta_esp character varying(200),
    fam_psoriasis boolean DEFAULT false,
    fam_psoriasis_esp character varying(200)
);


--
-- Name: TABLE ficha_medica; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.ficha_medica IS 'Ficha médica estática del paciente (1 por paciente)';


--
-- Name: COLUMN ficha_medica.enfermedades_cronicas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.enfermedades_cronicas IS 'Enfermedades crónicas preexistentes del paciente';


--
-- Name: COLUMN ficha_medica.medicacion_habitual; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.medicacion_habitual IS 'Medicamentos que el paciente toma de forma habitual';


--
-- Name: COLUMN ficha_medica.detalle_habitos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.detalle_habitos IS 'Descripción libre de hábitos relevantes para la salud';


--
-- Name: COLUMN ficha_medica.ocupacion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.ocupacion IS 'Ocupación o profesión del paciente';


--
-- Name: COLUMN ficha_medica.numero_calzado; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.numero_calzado IS 'Número de calzado del paciente';


--
-- Name: COLUMN ficha_medica.toma_medicamento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.toma_medicamento IS 'Indica si el paciente toma algún medicamento actualmente';


--
-- Name: COLUMN ficha_medica.alergia_medicamento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.alergia_medicamento IS 'Indica si el paciente tiene alergia a algún medicamento';


--
-- Name: COLUMN ficha_medica.padece_diabetes; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.padece_diabetes IS 'Enfermedad que padece: Diabetes';


--
-- Name: COLUMN ficha_medica.padece_hta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.padece_hta IS 'Enfermedad que padece: Hipertensión arterial';


--
-- Name: COLUMN ficha_medica.padece_artritis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.padece_artritis IS 'Enfermedad que padece: Artritis';


--
-- Name: COLUMN ficha_medica.padece_artrosis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.padece_artrosis IS 'Enfermedad que padece: Artrosis';


--
-- Name: COLUMN ficha_medica.padece_osteoporosis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.padece_osteoporosis IS 'Enfermedad que padece: Osteoporosis';


--
-- Name: COLUMN ficha_medica.padece_otro; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.padece_otro IS 'Otro padecimiento especificado por el paciente';


--
-- Name: COLUMN ficha_medica.fam_diabetes; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.fam_diabetes IS 'Antecedente familiar: Diabetes';


--
-- Name: COLUMN ficha_medica.fam_hta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.fam_hta IS 'Antecedente familiar: Hipertensión arterial';


--
-- Name: COLUMN ficha_medica.fam_psoriasis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.ficha_medica.fam_psoriasis IS 'Antecedente familiar: Psoriasis';


--
-- Name: ficha_medica_id_ficha_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ficha_medica_id_ficha_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ficha_medica_id_ficha_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ficha_medica_id_ficha_seq OWNED BY public.ficha_medica.id_ficha;


--
-- Name: ficha_medicacion_habitual; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ficha_medicacion_habitual (
    id_ficha_medicacion integer NOT NULL,
    id_ficha integer NOT NULL,
    id_medicamento integer,
    descripcion character varying(200) NOT NULL
);


--
-- Name: ficha_medicacion_habitual_id_ficha_medicacion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ficha_medicacion_habitual_id_ficha_medicacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ficha_medicacion_habitual_id_ficha_medicacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ficha_medicacion_habitual_id_ficha_medicacion_seq OWNED BY public.ficha_medicacion_habitual.id_ficha_medicacion;


--
-- Name: formas_cobro; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.formas_cobro (
    id_forma_cobro integer NOT NULL,
    descripcion character varying(60) NOT NULL,
    requiere_referencia boolean DEFAULT false
);


--
-- Name: formas_cobro_id_forma_cobro_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.formas_cobro_id_forma_cobro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: formas_cobro_id_forma_cobro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.formas_cobro_id_forma_cobro_seq OWNED BY public.formas_cobro.id_forma_cobro;


--
-- Name: funcionarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.funcionarios (
    id_funcionario integer NOT NULL,
    id_persona integer NOT NULL,
    id_usuario integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_rol integer NOT NULL,
    cargo character varying(100),
    fecha_ingreso date DEFAULT CURRENT_DATE NOT NULL,
    estado boolean DEFAULT true
);


--
-- Name: funcionarios_id_funcionario_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.funcionarios_id_funcionario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funcionarios_id_funcionario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.funcionarios_id_funcionario_seq OWNED BY public.funcionarios.id_funcionario;


--
-- Name: generos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.generos (
    id_genero integer NOT NULL,
    descripcion character varying(60)
);


--
-- Name: generos_id_genero_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.generos_id_genero_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: generos_id_genero_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.generos_id_genero_seq OWNED BY public.generos.id_genero;


--
-- Name: grupos_sanguineos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.grupos_sanguineos (
    id_grupo_sanguineo integer NOT NULL,
    descripcion character varying(10) NOT NULL
);


--
-- Name: TABLE grupos_sanguineos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.grupos_sanguineos IS 'Catálogo de grupos sanguíneos ABO + Rh';


--
-- Name: grupos_sanguineos_id_grupo_sanguineo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.grupos_sanguineos_id_grupo_sanguineo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: grupos_sanguineos_id_grupo_sanguineo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.grupos_sanguineos_id_grupo_sanguineo_seq OWNED BY public.grupos_sanguineos.id_grupo_sanguineo;


--
-- Name: insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.insumos (
    id_insumo integer NOT NULL,
    nombre character varying(200) NOT NULL,
    descripcion character varying(300),
    unidad_medida character varying(50),
    estado boolean DEFAULT true,
    precio_venta numeric(12,2) DEFAULT 0 NOT NULL,
    id_tipo_iva integer,
    stock_actual numeric(10,2) DEFAULT 0 NOT NULL,
    stock_minimo numeric(10,2) DEFAULT 0 NOT NULL
);


--
-- Name: TABLE insumos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.insumos IS 'Catálogo de insumos médicos utilizados durante la consulta';


--
-- Name: COLUMN insumos.unidad_medida; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.insumos.unidad_medida IS 'Unidad de medida del insumo (unidad, ml, par, caja, etc.)';


--
-- Name: COLUMN insumos.precio_venta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.insumos.precio_venta IS 'Precio de venta fijo al paciente (aparece en la factura)';


--
-- Name: COLUMN insumos.id_tipo_iva; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.insumos.id_tipo_iva IS 'Tasa de IVA aplicada al insumo al facturar (10%, 5% o Exento)';


--
-- Name: COLUMN insumos.stock_actual; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.insumos.stock_actual IS 'Cantidad disponible en este momento (se descuenta al registrar en consulta)';


--
-- Name: COLUMN insumos.stock_minimo; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.insumos.stock_minimo IS 'Cantidad mínima antes de emitir alerta de reposición';


--
-- Name: insumos_id_insumo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.insumos_id_insumo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: insumos_id_insumo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.insumos_id_insumo_seq OWNED BY public.insumos.id_insumo;


--
-- Name: justificativos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.justificativos (
    id_justificativo integer NOT NULL,
    id_consulta integer NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE NOT NULL,
    motivo text NOT NULL,
    dias_reposo integer,
    fecha_desde date,
    fecha_hasta date,
    observaciones text
);


--
-- Name: TABLE justificativos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.justificativos IS 'Justificativo médico generado al finalizar la consulta';


--
-- Name: COLUMN justificativos.motivo; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.justificativos.motivo IS 'Motivo del justificativo: reposo, inasistencia laboral, etc.';


--
-- Name: COLUMN justificativos.dias_reposo; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.justificativos.dias_reposo IS 'Cantidad de días de reposo indicados (opcional)';


--
-- Name: COLUMN justificativos.fecha_desde; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.justificativos.fecha_desde IS 'Fecha de inicio del período justificado';


--
-- Name: COLUMN justificativos.fecha_hasta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.justificativos.fecha_hasta IS 'Fecha de fin del período justificado';


--
-- Name: justificativos_id_justificativo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.justificativos_id_justificativo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: justificativos_id_justificativo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.justificativos_id_justificativo_seq OWNED BY public.justificativos.id_justificativo;


--
-- Name: medicamentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medicamentos (
    id_medicamento integer NOT NULL,
    nombre character varying(200) NOT NULL,
    principio_activo character varying(200),
    presentacion character varying(100),
    concentracion character varying(100),
    via_administracion character varying(80),
    estado boolean DEFAULT true
);


--
-- Name: TABLE medicamentos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.medicamentos IS 'Catálogo de medicamentos disponibles para receta médica';


--
-- Name: COLUMN medicamentos.presentacion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.medicamentos.presentacion IS 'Forma farmacéutica: comprimido, jarabe, inyectable, etc.';


--
-- Name: COLUMN medicamentos.via_administracion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.medicamentos.via_administracion IS 'Vía de administración del medicamento';


--
-- Name: medicamentos_id_medicamento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.medicamentos_id_medicamento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: medicamentos_id_medicamento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.medicamentos_id_medicamento_seq OWNED BY public.medicamentos.id_medicamento;


--
-- Name: medicos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medicos (
    id_medico integer NOT NULL,
    id_persona integer NOT NULL,
    matricula character varying(255)
);


--
-- Name: medicos_id_medico_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.medicos_id_medico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: medicos_id_medico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.medicos_id_medico_seq OWNED BY public.medicos.id_medico;


--
-- Name: motivos_nota; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.motivos_nota (
    id_motivo_nota integer NOT NULL,
    descripcion character varying(150) NOT NULL,
    id_tipo_comprobante integer NOT NULL
);


--
-- Name: motivos_nota_id_motivo_nota_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.motivos_nota_id_motivo_nota_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: motivos_nota_id_motivo_nota_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.motivos_nota_id_motivo_nota_seq OWNED BY public.motivos_nota.id_motivo_nota;


--
-- Name: notas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notas (
    id_nota integer NOT NULL,
    id_tipo_comprobante integer NOT NULL,
    id_factura integer NOT NULL,
    id_motivo_nota integer NOT NULL,
    establecimiento character varying(3) NOT NULL,
    punto_expedicion character varying(3) NOT NULL,
    numero_nota character varying(7) NOT NULL,
    timbrado character varying(20) NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE NOT NULL,
    monto numeric(12,2) NOT NULL,
    detalle_motivo text,
    id_usuario integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE notas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.notas IS 'Notas de crédito y débito asociadas a una factura existente';


--
-- Name: COLUMN notas.monto; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notas.monto IS 'Monto de la nota: resta (crédito) o suma (débito) al saldo de la factura';


--
-- Name: notas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notas_id_seq OWNED BY public.notas.id_nota;


--
-- Name: orden_analisis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.orden_analisis (
    id_orden_analisis integer NOT NULL,
    id_tipo_orden_analisis integer NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE NOT NULL,
    observacion text,
    estado character varying(20) DEFAULT 'pendiente'::character varying,
    id_consulta integer
);


--
-- Name: COLUMN orden_analisis.id_consulta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.orden_analisis.id_consulta IS 'Consulta en la que se emitió esta orden de análisis';


--
-- Name: orden_analisis_id_orden_analisis_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.orden_analisis_id_orden_analisis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: orden_analisis_id_orden_analisis_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.orden_analisis_id_orden_analisis_seq OWNED BY public.orden_analisis.id_orden_analisis;


--
-- Name: orden_estudio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.orden_estudio (
    id_orden_estudio integer NOT NULL,
    id_tipo_orden_estudio integer NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE NOT NULL,
    observacion text,
    estado character varying(20) DEFAULT 'pendiente'::character varying,
    id_consulta integer
);


--
-- Name: COLUMN orden_estudio.id_consulta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.orden_estudio.id_consulta IS 'Consulta en la que se emitió esta orden de estudio';


--
-- Name: orden_estudio_id_orden_estudio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.orden_estudio_id_orden_estudio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: orden_estudio_id_orden_estudio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.orden_estudio_id_orden_estudio_seq OWNED BY public.orden_estudio.id_orden_estudio;


--
-- Name: pacientes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pacientes (
    id_paciente integer NOT NULL,
    id_persona integer NOT NULL,
    fecha_nacimiento date NOT NULL,
    peso numeric,
    altura numeric,
    CONSTRAINT pacientes_altura_check CHECK ((altura >= (0)::numeric)),
    CONSTRAINT pacientes_peso_check CHECK ((peso >= (0)::numeric))
);


--
-- Name: pacientes_id_paciente_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pacientes_id_paciente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pacientes_id_paciente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pacientes_id_paciente_seq OWNED BY public.pacientes.id_paciente;


--
-- Name: permisos_rol; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permisos_rol (
    id_rol integer NOT NULL,
    modulo character varying(40) NOT NULL,
    puede_modificar boolean DEFAULT false NOT NULL
);


--
-- Name: personas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.personas (
    id_persona integer NOT NULL,
    nombre character varying(255),
    apellido character varying(255),
    cedula text NOT NULL,
    id_genero integer NOT NULL,
    id_estado_civil integer NOT NULL,
    telefono_emergencia text NOT NULL,
    id_ciudad integer NOT NULL,
    gmail character varying(255)
);


--
-- Name: personas_id_persona_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.personas_id_persona_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: personas_id_persona_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.personas_id_persona_seq OWNED BY public.personas.id_persona;


--
-- Name: receta_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.receta_detalle (
    id_receta_detalle integer NOT NULL,
    id_receta integer NOT NULL,
    id_medicamento integer NOT NULL,
    dosis character varying(100) NOT NULL,
    frecuencia character varying(100) NOT NULL,
    duracion character varying(100),
    indicaciones text,
    cantidad integer DEFAULT 1
);


--
-- Name: TABLE receta_detalle; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.receta_detalle IS 'Medicamentos individuales prescritos en la receta médica';


--
-- Name: COLUMN receta_detalle.dosis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.receta_detalle.dosis IS 'Cantidad por toma: Ej. 1 comprimido, 5 ml';


--
-- Name: COLUMN receta_detalle.frecuencia; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.receta_detalle.frecuencia IS 'Intervalo de administración: Ej. cada 8 horas';


--
-- Name: COLUMN receta_detalle.duracion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.receta_detalle.duracion IS 'Duración del tratamiento: Ej. 7 días, 2 semanas';


--
-- Name: COLUMN receta_detalle.cantidad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.receta_detalle.cantidad IS 'Cantidad total de unidades a dispensar';


--
-- Name: receta_detalle_id_receta_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.receta_detalle_id_receta_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: receta_detalle_id_receta_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.receta_detalle_id_receta_detalle_seq OWNED BY public.receta_detalle.id_receta_detalle;


--
-- Name: recetas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recetas (
    id_receta integer NOT NULL,
    id_consulta integer NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE NOT NULL,
    observaciones text
);


--
-- Name: TABLE recetas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.recetas IS 'Encabezado de receta médica generada en la consulta';


--
-- Name: COLUMN recetas.id_consulta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.recetas.id_consulta IS 'Consulta a la que pertenece la receta (relación 1-1)';


--
-- Name: recetas_id_receta_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.recetas_id_receta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: recetas_id_receta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.recetas_id_receta_seq OWNED BY public.recetas.id_receta;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id_rol integer NOT NULL,
    descripcion character varying(50) NOT NULL
);


--
-- Name: roles_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_rol_seq OWNED BY public.roles.id_rol;


--
-- Name: sala_atenciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sala_atenciones (
    id_sala_atencion integer NOT NULL,
    nombre character varying(60)
);


--
-- Name: sala_atenciones_id_sala_atencion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sala_atenciones_id_sala_atencion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sala_atenciones_id_sala_atencion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sala_atenciones_id_sala_atencion_seq OWNED BY public.sala_atenciones.id_sala_atencion;


--
-- Name: servicios_facturables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.servicios_facturables (
    id_servicio integer NOT NULL,
    descripcion character varying(200) NOT NULL,
    precio_unitario numeric(12,2) DEFAULT 0 NOT NULL,
    id_tipo_iva integer NOT NULL,
    estado boolean DEFAULT true
);


--
-- Name: TABLE servicios_facturables; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.servicios_facturables IS 'Catálogo de servicios/precios que pueden facturarse, vinculables a una consulta';


--
-- Name: servicios_facturables_id_servicio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.servicios_facturables_id_servicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: servicios_facturables_id_servicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.servicios_facturables_id_servicio_seq OWNED BY public.servicios_facturables.id_servicio;


--
-- Name: signos_vitales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.signos_vitales (
    id_signos_vitales integer NOT NULL,
    id_consulta integer NOT NULL,
    peso numeric(5,2),
    talla numeric(5,2),
    presion_sistolica integer,
    presion_diastolica integer,
    temperatura numeric(4,1),
    frecuencia_cardiaca integer,
    frecuencia_resp integer,
    saturacion_oxigeno numeric(4,1),
    glucemia numeric(5,1),
    observaciones text,
    pulso_pedio_izq character varying(10),
    pulso_pedio_der character varying(10),
    pulso_tibial_izq character varying(10),
    pulso_tibial_der character varying(10),
    temperatura_pie character varying(20)
);


--
-- Name: TABLE signos_vitales; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.signos_vitales IS 'Signos vitales tomados al inicio de cada consulta';


--
-- Name: COLUMN signos_vitales.presion_sistolica; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.signos_vitales.presion_sistolica IS 'Presión arterial sistólica en mmHg';


--
-- Name: COLUMN signos_vitales.glucemia; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.signos_vitales.glucemia IS 'Glucemia capilar opcional en mg/dL';


--
-- Name: COLUMN signos_vitales.pulso_pedio_izq; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.signos_vitales.pulso_pedio_izq IS 'Pulso pedio izquierdo: + o -';


--
-- Name: COLUMN signos_vitales.pulso_pedio_der; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.signos_vitales.pulso_pedio_der IS 'Pulso pedio derecho: + o -';


--
-- Name: COLUMN signos_vitales.pulso_tibial_izq; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.signos_vitales.pulso_tibial_izq IS 'Pulso tibial izquierdo: + o -';


--
-- Name: COLUMN signos_vitales.pulso_tibial_der; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.signos_vitales.pulso_tibial_der IS 'Pulso tibial derecho: + o -';


--
-- Name: COLUMN signos_vitales.temperatura_pie; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.signos_vitales.temperatura_pie IS 'Temperatura del pie: Fría / Normal / Caliente';


--
-- Name: signos_vitales_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.signos_vitales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: signos_vitales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.signos_vitales_id_seq OWNED BY public.signos_vitales.id_signos_vitales;


--
-- Name: stock_insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_insumos (
    id_movimiento integer NOT NULL,
    id_insumo integer NOT NULL,
    tipo_movimiento character varying(10) NOT NULL,
    cantidad numeric(10,2) NOT NULL,
    stock_anterior numeric(10,2) NOT NULL,
    stock_nuevo numeric(10,2) NOT NULL,
    motivo character varying(200),
    id_consulta integer,
    id_usuario integer,
    fecha_movimiento timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_tipo_movimiento CHECK (((tipo_movimiento)::text = ANY ((ARRAY['ENTRADA'::character varying, 'SALIDA'::character varying])::text[])))
);


--
-- Name: TABLE stock_insumos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.stock_insumos IS 'Historial de movimientos de stock: entradas (reposición) y salidas (consultas)';


--
-- Name: COLUMN stock_insumos.tipo_movimiento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.stock_insumos.tipo_movimiento IS 'ENTRADA = reposición/compra, SALIDA = consumo en consulta o ajuste';


--
-- Name: COLUMN stock_insumos.stock_anterior; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.stock_insumos.stock_anterior IS 'Stock antes del movimiento (para auditoría)';


--
-- Name: COLUMN stock_insumos.stock_nuevo; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.stock_insumos.stock_nuevo IS 'Stock resultante después del movimiento';


--
-- Name: COLUMN stock_insumos.id_consulta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.stock_insumos.id_consulta IS 'Si es SALIDA por consulta, referencia al id_consulta correspondiente';


--
-- Name: stock_insumos_id_movimiento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.stock_insumos_id_movimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: stock_insumos_id_movimiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.stock_insumos_id_movimiento_seq OWNED BY public.stock_insumos.id_movimiento;


--
-- Name: tipo_orden_analisis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_orden_analisis (
    id_tipo_orden_analisis integer NOT NULL,
    descripcion character varying(100) NOT NULL,
    estado boolean DEFAULT true
);


--
-- Name: tipo_orden_analisis_id_tipo_orden_analisis_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_orden_analisis_id_tipo_orden_analisis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_orden_analisis_id_tipo_orden_analisis_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_orden_analisis_id_tipo_orden_analisis_seq OWNED BY public.tipo_orden_analisis.id_tipo_orden_analisis;


--
-- Name: tipo_orden_estudio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_orden_estudio (
    id_tipo_orden_estudio integer NOT NULL,
    descripcion character varying(100) NOT NULL,
    estado boolean DEFAULT true
);


--
-- Name: tipo_orden_estudio_id_tipo_orden_estudio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_orden_estudio_id_tipo_orden_estudio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_orden_estudio_id_tipo_orden_estudio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_orden_estudio_id_tipo_orden_estudio_seq OWNED BY public.tipo_orden_estudio.id_tipo_orden_estudio;


--
-- Name: tipos_alergia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_alergia (
    id_tipo_alergia integer NOT NULL,
    descripcion character varying(100) NOT NULL,
    estado boolean DEFAULT true
);


--
-- Name: TABLE tipos_alergia; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.tipos_alergia IS 'Tipos de alergia registrables en la ficha médica';


--
-- Name: tipos_alergia_id_tipo_alergia_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_alergia_id_tipo_alergia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipos_alergia_id_tipo_alergia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_alergia_id_tipo_alergia_seq OWNED BY public.tipos_alergia.id_tipo_alergia;


--
-- Name: tipos_comprobante; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_comprobante (
    id_tipo_comprobante integer NOT NULL,
    descripcion character varying(60) NOT NULL,
    prefijo character varying(5)
);


--
-- Name: tipos_comprobante_id_tipo_comprobante_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_comprobante_id_tipo_comprobante_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipos_comprobante_id_tipo_comprobante_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_comprobante_id_tipo_comprobante_seq OWNED BY public.tipos_comprobante.id_tipo_comprobante;


--
-- Name: tipos_iva; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_iva (
    id_tipo_iva integer NOT NULL,
    descripcion character varying(40) NOT NULL,
    porcentaje numeric(5,2) NOT NULL
);


--
-- Name: tipos_iva_id_tipo_iva_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_iva_id_tipo_iva_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipos_iva_id_tipo_iva_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_iva_id_tipo_iva_seq OWNED BY public.tipos_iva.id_tipo_iva;


--
-- Name: tratamientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tratamientos (
    id_tratamiento integer NOT NULL,
    id_enfermedad integer NOT NULL,
    descripcion character varying(300) NOT NULL,
    indicaciones text,
    estado boolean DEFAULT true
);


--
-- Name: TABLE tratamientos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.tratamientos IS 'Tratamientos médicos asociados a cada enfermedad/diagnóstico';


--
-- Name: COLUMN tratamientos.id_enfermedad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.tratamientos.id_enfermedad IS 'Enfermedad a la que corresponde este tratamiento';


--
-- Name: COLUMN tratamientos.indicaciones; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.tratamientos.indicaciones IS 'Instrucciones clínicas del tratamiento';


--
-- Name: tratamientos_id_tratamiento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tratamientos_id_tratamiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tratamientos_id_tratamiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tratamientos_id_tratamiento_seq OWNED BY public.tratamientos.id_tratamiento;


--
-- Name: turnos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.turnos (
    id_turno integer NOT NULL,
    descripcion character varying(60)
);


--
-- Name: turnos_id_turno_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.turnos_id_turno_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: turnos_id_turno_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.turnos_id_turno_seq OWNED BY public.turnos.id_turno;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nickname text NOT NULL,
    clave text NOT NULL,
    estado boolean NOT NULL,
    id_rol integer,
    totp_secreto character varying(64),
    totp_activo boolean DEFAULT false NOT NULL,
    totp_ultimo_paso bigint
);


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- Name: vw_alerta_stock; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_alerta_stock AS
 SELECT i.id_insumo,
    i.nombre,
    i.unidad_medida,
    i.stock_actual,
    i.stock_minimo,
    i.precio_venta,
    t.descripcion AS tipo_iva,
    t.porcentaje AS porcentaje_iva,
        CASE
            WHEN (i.stock_actual = (0)::numeric) THEN 'SIN STOCK'::text
            WHEN (i.stock_actual <= i.stock_minimo) THEN 'STOCK MÍNIMO'::text
            ELSE 'OK'::text
        END AS estado_stock
   FROM (public.insumos i
     LEFT JOIN public.tipos_iva t ON ((t.id_tipo_iva = i.id_tipo_iva)))
  WHERE (i.estado = true)
  ORDER BY
        CASE
            WHEN (i.stock_actual = (0)::numeric) THEN 1
            WHEN (i.stock_actual <= i.stock_minimo) THEN 2
            ELSE 3
        END, i.nombre;


--
-- Name: VIEW vw_alerta_stock; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_alerta_stock IS 'Insumos activos con indicador de estado de stock (SIN STOCK / STOCK MÍNIMO / OK)';


--
-- Name: vw_arqueo_caja; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_arqueo_caja AS
 SELECT c.id_caja,
    u.nickname AS usuario,
    c.fecha_apertura,
    c.fecha_cierre,
    c.monto_apertura,
    COALESCE(sum(
        CASE
            WHEN ((fc.descripcion)::text = 'Efectivo'::text) THEN cob.monto
            ELSE (0)::numeric
        END), (0)::numeric) AS total_efectivo,
    COALESCE(sum(
        CASE
            WHEN ((fc.descripcion)::text = 'Cheque'::text) THEN cob.monto
            ELSE (0)::numeric
        END), (0)::numeric) AS total_cheque,
    COALESCE(sum(
        CASE
            WHEN ((fc.descripcion)::text = 'Tarjeta de Crédito'::text) THEN cob.monto
            ELSE (0)::numeric
        END), (0)::numeric) AS total_tarjeta_credito,
    COALESCE(sum(
        CASE
            WHEN ((fc.descripcion)::text = 'Tarjeta de Débito'::text) THEN cob.monto
            ELSE (0)::numeric
        END), (0)::numeric) AS total_tarjeta_debito,
    COALESCE(sum(cob.monto), (0)::numeric) AS total_cobrado,
    (c.monto_apertura + COALESCE(sum(
        CASE
            WHEN ((fc.descripcion)::text = 'Efectivo'::text) THEN cob.monto
            ELSE (0)::numeric
        END), (0)::numeric)) AS efectivo_esperado,
    c.monto_cierre_declarado,
    c.diferencia,
    c.estado
   FROM (((public.cajas c
     JOIN public.usuarios u ON ((u.id_usuario = c.id_usuario)))
     LEFT JOIN public.cobranzas cob ON ((cob.id_caja = c.id_caja)))
     LEFT JOIN public.formas_cobro fc ON ((fc.id_forma_cobro = cob.id_forma_cobro)))
  GROUP BY c.id_caja, u.nickname, c.fecha_apertura, c.fecha_cierre, c.monto_apertura, c.monto_cierre_declarado, c.diferencia, c.estado
  ORDER BY c.fecha_apertura DESC;


--
-- Name: VIEW vw_arqueo_caja; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_arqueo_caja IS 'Resumen de movimientos por caja: efectivo esperado vs declarado, por forma de cobro';


--
-- Name: vw_consulta_completa; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_consulta_completa AS
 SELECT c.id_consulta,
    c.fecha_consulta,
    c.motivo_consulta,
    c.diagnostico AS diagnostico_texto,
    c.tratamiento AS tratamiento_texto,
    c.observaciones,
    c.requiere_orden_estudio,
    c.requiere_orden_analisis,
    toe.descripcion AS tipo_orden_estudio,
    c.fecha_emision_estudio,
    c.fecha_vencimiento_estudio,
    toa.descripcion AS tipo_orden_analisis,
    c.fecha_emision_analisis,
    c.fecha_vencimiento_analisis,
    e.codigo_cie,
    e.descripcion AS enfermedad,
    t.descripcion AS tratamiento_indicado,
    ci.id_cita,
    ci.observacion AS observacion_cita,
    dh.fecha AS fecha_cita,
    dh.hora_inicio,
    dh.hora_fin,
    pac.id_paciente,
    pac.fecha_nacimiento,
    pac.peso,
    pac.altura,
    per_pac.nombre AS paciente_nombre,
    per_pac.apellido AS paciente_apellido,
    per_pac.cedula AS paciente_cedula,
    per_pac.telefono_emergencia AS paciente_telefono,
    per_pac.gmail AS paciente_email,
    med.id_medico,
    med.matricula,
    per_med.nombre AS medico_nombre,
    per_med.apellido AS medico_apellido,
    esp.descripcion AS especialidad,
    sa.nombre AS sala_atencion
   FROM (((((((((((((public.consultas c
     LEFT JOIN public.tipo_orden_estudio toe ON ((toe.id_tipo_orden_estudio = c.id_tipo_orden_estudio)))
     LEFT JOIN public.tipo_orden_analisis toa ON ((toa.id_tipo_orden_analisis = c.id_tipo_orden_analisis)))
     LEFT JOIN public.enfermedades e ON ((e.id_enfermedad = c.id_enfermedad)))
     LEFT JOIN public.tratamientos t ON ((t.id_tratamiento = c.id_tratamiento)))
     JOIN public.citas ci ON ((ci.id_cita = c.id_cita)))
     JOIN public.disponibilidad_horaria dh ON ((dh.id_disponibilidad_horaria = ci.id_disponibilidad_horaria)))
     JOIN public.pacientes pac ON ((pac.id_paciente = ci.id_paciente)))
     JOIN public.personas per_pac ON ((per_pac.id_persona = pac.id_persona)))
     JOIN public.agenda_medicas am ON ((am.id_agenda_medica = dh.id_agenda_medica)))
     JOIN public.medicos med ON ((med.id_medico = am.id_medico)))
     JOIN public.personas per_med ON ((per_med.id_persona = med.id_persona)))
     JOIN public.especialidades esp ON ((esp.id_especialidad = am.id_especialidad)))
     LEFT JOIN public.sala_atenciones sa ON ((sa.id_sala_atencion = am.id_sala_atencion)));


--
-- Name: VIEW vw_consulta_completa; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_consulta_completa IS 'Vista completa de la consulta con datos del paciente, médico, cita, diagnóstico, tratamiento y órdenes';


--
-- Name: vw_consultas_sin_facturar; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_consultas_sin_facturar AS
 SELECT co.id_consulta,
    co.fecha_consulta,
    co.motivo_consulta,
    (((p.nombre)::text || ' '::text) || (p.apellido)::text) AS paciente,
    p.cedula,
    (((pm.nombre)::text || ' '::text) || (pm.apellido)::text) AS medico,
    e.descripcion AS especialidad,
    ( SELECT count(*) AS count
           FROM public.consulta_procedimientos cp
          WHERE (cp.id_consulta = co.id_consulta)) AS total_procedimientos,
    ( SELECT count(*) AS count
           FROM (public.consulta_insumos ci_1
             JOIN public.insumos i ON ((i.id_insumo = ci_1.id_insumo)))
          WHERE ((ci_1.id_consulta = co.id_consulta) AND (i.precio_venta > (0)::numeric))) AS total_insumos
   FROM ((((((((public.consultas co
     JOIN public.citas ci ON ((ci.id_cita = co.id_cita)))
     JOIN public.pacientes pa ON ((pa.id_paciente = ci.id_paciente)))
     JOIN public.personas p ON ((p.id_persona = pa.id_persona)))
     JOIN public.disponibilidad_horaria dh ON ((dh.id_disponibilidad_horaria = ci.id_disponibilidad_horaria)))
     JOIN public.agenda_medicas am ON ((am.id_agenda_medica = dh.id_agenda_medica)))
     JOIN public.medicos m ON ((m.id_medico = am.id_medico)))
     JOIN public.personas pm ON ((pm.id_persona = m.id_persona)))
     JOIN public.especialidades e ON ((e.id_especialidad = am.id_especialidad)))
  WHERE (NOT (co.id_consulta IN ( SELECT facturas.id_consulta
           FROM public.facturas)));


--
-- Name: VIEW vw_consultas_sin_facturar; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_consultas_sin_facturar IS 'Consultas pendientes de facturar con conteo de procedimientos e insumos';


--
-- Name: vw_cuentas_a_cobrar; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_cuentas_a_cobrar AS
 SELECT f.id_factura,
    (((((f.establecimiento)::text || '-'::text) || (f.punto_expedicion)::text) || '-'::text) || (f.numero_factura)::text) AS nro_factura,
    f.fecha_emision,
    f.nombre_cliente,
    f.ruc_ci_cliente,
    f.total,
    f.saldo_pendiente,
    ef.descripcion AS estado_factura
   FROM (public.facturas f
     JOIN public.estados_factura ef ON ((ef.id_estado_factura = f.id_estado_factura)))
  WHERE ((f.saldo_pendiente > (0)::numeric) AND ((ef.descripcion)::text <> 'Anulada'::text))
  ORDER BY f.fecha_emision;


--
-- Name: VIEW vw_cuentas_a_cobrar; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_cuentas_a_cobrar IS 'Facturas con saldo pendiente de cobro';


--
-- Name: vw_ficha_paciente; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_ficha_paciente AS
 SELECT pa.id_paciente,
    per.nombre,
    per.apellido,
    per.cedula,
    per.telefono_emergencia,
    pa.fecha_nacimiento,
    fm.id_ficha,
    gs.descripcion AS grupo_sanguineo,
    fm.peso_habitual,
    fm.talla,
    fm.enfermedades_cronicas,
    fm.antecedentes_quirurgicos,
    fm.antecedentes_familiares,
    fm.medicacion_habitual,
    fm.tabaquismo,
    fm.alcoholismo,
    fm.actividad_fisica,
    fm.detalle_habitos,
    fm.observaciones AS obs_ficha,
    fm.fecha_actualizacion
   FROM (((public.pacientes pa
     JOIN public.personas per ON ((per.id_persona = pa.id_persona)))
     LEFT JOIN public.ficha_medica fm ON ((fm.id_paciente = pa.id_paciente)))
     LEFT JOIN public.grupos_sanguineos gs ON ((gs.id_grupo_sanguineo = fm.id_grupo_sanguineo)));


--
-- Name: VIEW vw_ficha_paciente; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_ficha_paciente IS 'Vista de la ficha médica completa del paciente con datos personales';


--
-- Name: vw_ficha_podologica; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_ficha_podologica AS
 SELECT pa.id_paciente,
    per.nombre,
    per.apellido,
    per.cedula,
    per.telefono_emergencia AS telefono,
    pa.fecha_nacimiento,
    pa.peso,
    pa.altura,
    fm.id_ficha,
    fm.ocupacion,
    fm.numero_calzado,
    fm.toma_medicamento,
    fm.alergia_medicamento,
    fm.medicacion_habitual,
    fm.padece_diabetes,
    fm.padece_hta,
    fm.padece_artritis,
    fm.padece_artrosis,
    fm.padece_osteoporosis,
    fm.padece_otro,
    fm.fam_diabetes,
    fm.fam_diabetes_esp,
    fm.fam_hta,
    fm.fam_hta_esp,
    fm.fam_psoriasis,
    fm.fam_psoriasis_esp,
    gs.descripcion AS grupo_sanguineo,
    fm.enfermedades_cronicas,
    fm.antecedentes_quirurgicos,
    fm.tabaquismo,
    fm.alcoholismo,
    fm.actividad_fisica,
    fm.detalle_habitos,
    fm.observaciones AS obs_ficha,
    fm.fecha_actualizacion
   FROM (((public.pacientes pa
     JOIN public.personas per ON ((per.id_persona = pa.id_persona)))
     LEFT JOIN public.ficha_medica fm ON ((fm.id_paciente = pa.id_paciente)))
     LEFT JOIN public.grupos_sanguineos gs ON ((gs.id_grupo_sanguineo = fm.id_grupo_sanguineo)));


--
-- Name: vw_funcionarios; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_funcionarios AS
 SELECT f.id_funcionario,
    (((p.nombre)::text || ' '::text) || (p.apellido)::text) AS nombre_completo,
    p.cedula,
    u.nickname,
    r.descripcion AS rol,
    f.cargo,
    c.nombre AS consultorio,
    f.fecha_ingreso,
    f.estado
   FROM ((((public.funcionarios f
     JOIN public.personas p ON ((p.id_persona = f.id_persona)))
     JOIN public.usuarios u ON ((u.id_usuario = f.id_usuario)))
     JOIN public.roles r ON ((r.id_rol = f.id_rol)))
     JOIN public.consultorio c ON ((c.id_consultorio = f.id_consultorio)));


--
-- Name: vw_historial_clinico; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_historial_clinico AS
 SELECT co.id_consulta,
    co.fecha_consulta,
    co.motivo_consulta,
    co.diagnostico,
    co.tratamiento,
    co.observaciones,
    enf.descripcion AS enfermedad,
    tra.descripcion AS tratamiento_indicado,
    sv.peso,
    sv.talla,
    sv.presion_sistolica,
    sv.presion_diastolica,
    sv.temperatura,
    sv.frecuencia_cardiaca,
    sv.frecuencia_resp,
    sv.saturacion_oxigeno,
    sv.glucemia,
    (((perm.nombre)::text || ' '::text) || (perm.apellido)::text) AS medico,
    esp.descripcion AS especialidad,
    pa.id_paciente
   FROM ((((((((((public.consultas co
     JOIN public.citas ci ON ((ci.id_cita = co.id_cita)))
     JOIN public.pacientes pa ON ((pa.id_paciente = ci.id_paciente)))
     JOIN public.disponibilidad_horaria dh ON ((dh.id_disponibilidad_horaria = ci.id_disponibilidad_horaria)))
     JOIN public.agenda_medicas am ON ((am.id_agenda_medica = dh.id_agenda_medica)))
     JOIN public.medicos m ON ((m.id_medico = am.id_medico)))
     JOIN public.personas perm ON ((perm.id_persona = m.id_persona)))
     JOIN public.especialidades esp ON ((esp.id_especialidad = am.id_especialidad)))
     LEFT JOIN public.enfermedades enf ON ((enf.id_enfermedad = co.id_enfermedad)))
     LEFT JOIN public.tratamientos tra ON ((tra.id_tratamiento = co.id_tratamiento)))
     LEFT JOIN public.signos_vitales sv ON ((sv.id_consulta = co.id_consulta)))
  ORDER BY co.fecha_consulta DESC;


--
-- Name: VIEW vw_historial_clinico; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_historial_clinico IS 'Historial clínico completo del paciente: consultas + signos vitales + diagnósticos';


--
-- Name: vw_historial_stock; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_historial_stock AS
 SELECT sm.id_movimiento,
    i.nombre AS insumo,
    i.unidad_medida,
    sm.tipo_movimiento,
    sm.cantidad,
    sm.stock_anterior,
    sm.stock_nuevo,
    sm.motivo,
    sm.fecha_movimiento,
    u.nickname AS usuario,
    COALESCE(('Consulta #'::text || (sm.id_consulta)::text), '—'::text) AS consulta_ref
   FROM ((public.stock_insumos sm
     JOIN public.insumos i ON ((i.id_insumo = sm.id_insumo)))
     LEFT JOIN public.usuarios u ON ((u.id_usuario = sm.id_usuario)))
  ORDER BY sm.fecha_movimiento DESC;


--
-- Name: VIEW vw_historial_stock; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_historial_stock IS 'Historial completo de movimientos de stock con datos del insumo y usuario';


--
-- Name: vw_informe_servicios; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_informe_servicios AS
 SELECT fd.id_servicio,
    s.descripcion AS servicio,
    count(*) AS cantidad_facturada,
    sum(fd.subtotal) AS monto_total,
    f.fecha_emision
   FROM ((public.factura_detalle fd
     JOIN public.facturas f ON ((f.id_factura = fd.id_factura)))
     LEFT JOIN public.servicios_facturables s ON ((s.id_servicio = fd.id_servicio)))
  WHERE (f.id_estado_factura <> ( SELECT estados_factura.id_estado_factura
           FROM public.estados_factura
          WHERE ((estados_factura.descripcion)::text = 'Anulada'::text)))
  GROUP BY fd.id_servicio, s.descripcion, f.fecha_emision
  ORDER BY f.fecha_emision DESC;


--
-- Name: VIEW vw_informe_servicios; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_informe_servicios IS 'Resumen de servicios facturados, base para informes web de facturación';


--
-- Name: vw_items_factura_por_consulta; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_items_factura_por_consulta AS
 SELECT co.id_consulta,
    'procedimiento'::text AS tipo,
    cp.id_consulta_procedimiento AS id_item,
    sf.id_servicio AS id_referencia,
    sf.descripcion,
    cp.cantidad,
    sf.precio_unitario,
    round((cp.cantidad * sf.precio_unitario), 2) AS subtotal,
    sf.id_tipo_iva,
    ti.porcentaje AS pct_iva,
    cp.observacion
   FROM (((public.consulta_procedimientos cp
     JOIN public.consultas co ON ((co.id_consulta = cp.id_consulta)))
     JOIN public.servicios_facturables sf ON ((sf.id_servicio = cp.id_servicio)))
     JOIN public.tipos_iva ti ON ((ti.id_tipo_iva = sf.id_tipo_iva)))
UNION ALL
 SELECT co.id_consulta,
    'insumo'::text AS tipo,
    ci.id_consulta_insumo AS id_item,
    i.id_insumo AS id_referencia,
    ((((i.nombre)::text || ' ('::text) || (i.unidad_medida)::text) || ')'::text) AS descripcion,
    ci.cantidad,
    i.precio_venta AS precio_unitario,
    round((ci.cantidad * i.precio_venta), 2) AS subtotal,
    i.id_tipo_iva,
    COALESCE(ti.porcentaje, (0)::numeric) AS pct_iva,
    ci.observacion
   FROM (((public.consulta_insumos ci
     JOIN public.consultas co ON ((co.id_consulta = ci.id_consulta)))
     JOIN public.insumos i ON ((i.id_insumo = ci.id_insumo)))
     LEFT JOIN public.tipos_iva ti ON ((ti.id_tipo_iva = i.id_tipo_iva)))
  WHERE (i.precio_venta > (0)::numeric);


--
-- Name: VIEW vw_items_factura_por_consulta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_items_factura_por_consulta IS 'Unifica procedimientos + insumos de una consulta CON precios. Solo usar desde facturación';


--
-- Name: vw_recaudacion_depositar; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_recaudacion_depositar AS
 SELECT c.id_caja,
    u.nickname AS usuario,
    c.fecha_cierre,
    COALESCE(sum(
        CASE
            WHEN ((fc.descripcion)::text = 'Efectivo'::text) THEN cob.monto
            ELSE (0)::numeric
        END), (0)::numeric) AS efectivo_a_depositar
   FROM (((public.cajas c
     JOIN public.usuarios u ON ((u.id_usuario = c.id_usuario)))
     LEFT JOIN public.cobranzas cob ON ((cob.id_caja = c.id_caja)))
     LEFT JOIN public.formas_cobro fc ON ((fc.id_forma_cobro = cob.id_forma_cobro)))
  WHERE ((c.estado)::text = 'Cerrada'::text)
  GROUP BY c.id_caja, u.nickname, c.fecha_cierre
 HAVING (COALESCE(sum(
        CASE
            WHEN ((fc.descripcion)::text = 'Efectivo'::text) THEN cob.monto
            ELSE (0)::numeric
        END), (0)::numeric) > (0)::numeric)
  ORDER BY c.fecha_cierre DESC;


--
-- Name: VIEW vw_recaudacion_depositar; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vw_recaudacion_depositar IS 'Efectivo recaudado en cajas ya cerradas, listo para depositar en el banco';


--
-- Name: vw_trazabilidad; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_trazabilidad AS
 WITH mov AS (
         SELECT 'Agenda'::text AS proceso,
            am.id_agenda_medica AS id_registro,
            am.fecha_registro,
            ((('Prof. '::text || (pm.nombre)::text) || ' '::text) || (pm.apellido)::text) AS paciente,
            am.id_funcionario
           FROM ((public.agenda_medicas am
             JOIN public.medicos m ON ((m.id_medico = am.id_medico)))
             JOIN public.personas pm ON ((pm.id_persona = m.id_persona)))
        UNION ALL
         SELECT 'Cita'::text,
            c.id_cita,
            c.fecha_registro,
            (((p.nombre)::text || ' '::text) || (p.apellido)::text),
            c.id_funcionario
           FROM ((public.citas c
             JOIN public.pacientes pa ON ((pa.id_paciente = c.id_paciente)))
             JOIN public.personas p ON ((p.id_persona = pa.id_persona)))
        UNION ALL
         SELECT 'Consulta'::text,
            co.id_consulta,
            co.fecha_consulta,
            (((p.nombre)::text || ' '::text) || (p.apellido)::text),
            co.id_funcionario
           FROM (((public.consultas co
             JOIN public.citas c ON ((c.id_cita = co.id_cita)))
             JOIN public.pacientes pa ON ((pa.id_paciente = c.id_paciente)))
             JOIN public.personas p ON ((p.id_persona = pa.id_persona)))
        UNION ALL
         SELECT 'Factura'::text,
            f.id_factura,
            f.fecha_creacion,
            f.nombre_cliente,
            f.id_funcionario
           FROM public.facturas f
        UNION ALL
         SELECT 'Respuesta aviso'::text,
            ar.id_aviso,
            ar.fecha_respuesta,
            (((p.nombre)::text || ' '::text) || (p.apellido)::text),
            ar.id_funcionario
           FROM (((public.avisos_recordatorios ar
             JOIN public.citas c ON ((c.id_cita = ar.id_cita)))
             JOIN public.pacientes pa ON ((pa.id_paciente = c.id_paciente)))
             JOIN public.personas p ON ((p.id_persona = pa.id_persona)))
          WHERE (ar.respuesta IS NOT NULL)
        )
 SELECT mov.proceso,
    mov.id_registro,
    mov.fecha_registro,
    mov.paciente,
    vf.nombre_completo AS funcionario,
    vf.rol AS rol_funcionario,
    vf.consultorio
   FROM (mov
     LEFT JOIN public.vw_funcionarios vf ON ((vf.id_funcionario = mov.id_funcionario)));


--
-- Name: agenda_medicas id_agenda_medica; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas ALTER COLUMN id_agenda_medica SET DEFAULT nextval('public.agenda_medicas_id_agenda_medica_seq'::regclass);


--
-- Name: alergias_paciente id_alergia_paciente; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alergias_paciente ALTER COLUMN id_alergia_paciente SET DEFAULT nextval('public.alergias_paciente_id_seq'::regclass);


--
-- Name: anamnesis_podologica id_anamnesis; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis_podologica ALTER COLUMN id_anamnesis SET DEFAULT nextval('public.anamnesis_podologica_id_seq'::regclass);


--
-- Name: auditoria_accesos id_auditoria; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_accesos ALTER COLUMN id_auditoria SET DEFAULT nextval('public.auditoria_accesos_id_auditoria_seq'::regclass);


--
-- Name: avisos_recordatorios id_aviso; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.avisos_recordatorios ALTER COLUMN id_aviso SET DEFAULT nextval('public.avisos_recordatorios_id_aviso_seq'::regclass);


--
-- Name: cajas id_caja; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas ALTER COLUMN id_caja SET DEFAULT nextval('public.cajas_id_caja_seq'::regclass);


--
-- Name: citas id_cita; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas ALTER COLUMN id_cita SET DEFAULT nextval('public.citas_id_cita_seq'::regclass);


--
-- Name: ciudades id_ciudad; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades ALTER COLUMN id_ciudad SET DEFAULT nextval('public.ciudades_id_ciudad_seq'::regclass);


--
-- Name: cobranzas id_cobranza; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas ALTER COLUMN id_cobranza SET DEFAULT nextval('public.cobranzas_id_seq'::regclass);


--
-- Name: consulta_diagnosticos id_consulta_diagnostico; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_diagnosticos ALTER COLUMN id_consulta_diagnostico SET DEFAULT nextval('public.consulta_diagnosticos_id_consulta_diagnostico_seq'::regclass);


--
-- Name: consulta_insumos id_consulta_insumo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_insumos ALTER COLUMN id_consulta_insumo SET DEFAULT nextval('public.consulta_insumos_id_consulta_insumo_seq'::regclass);


--
-- Name: consulta_ordenes id_consulta_orden; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_ordenes ALTER COLUMN id_consulta_orden SET DEFAULT nextval('public.consulta_ordenes_id_consulta_orden_seq'::regclass);


--
-- Name: consulta_procedimientos id_consulta_procedimiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_procedimientos ALTER COLUMN id_consulta_procedimiento SET DEFAULT nextval('public.consulta_procedimientos_id_consulta_procedimiento_seq'::regclass);


--
-- Name: consultas id_consulta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas ALTER COLUMN id_consulta SET DEFAULT nextval('public.consultas_id_consulta_seq'::regclass);


--
-- Name: consultorio id_consultorio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorio ALTER COLUMN id_consultorio SET DEFAULT nextval('public.consultorio_id_consultorio_seq'::regclass);


--
-- Name: datos_emisor id_emisor; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.datos_emisor ALTER COLUMN id_emisor SET DEFAULT nextval('public.datos_emisor_id_emisor_seq'::regclass);


--
-- Name: dias id_dia; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias ALTER COLUMN id_dia SET DEFAULT nextval('public.dias_id_dia_seq'::regclass);


--
-- Name: disponibilidad_horaria id_disponibilidad_horaria; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disponibilidad_horaria ALTER COLUMN id_disponibilidad_horaria SET DEFAULT nextval('public.disponibilidad_horaria_id_disponibilidad_horaria_seq'::regclass);


--
-- Name: enfermedades id_enfermedad; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enfermedades ALTER COLUMN id_enfermedad SET DEFAULT nextval('public.enfermedades_id_enfermedad_seq'::regclass);


--
-- Name: especialidades id_especialidad; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades ALTER COLUMN id_especialidad SET DEFAULT nextval('public.especialidades_id_especialidad_seq'::regclass);


--
-- Name: estado_citas id_estado_cita; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_citas ALTER COLUMN id_estado_cita SET DEFAULT nextval('public.estado_citas_id_estado_cita_seq'::regclass);


--
-- Name: estado_civiles id_estado_civil; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_civiles ALTER COLUMN id_estado_civil SET DEFAULT nextval('public.estado_civiles_id_estado_civil_seq'::regclass);


--
-- Name: estado_laborales id_estado_laboral; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_laborales ALTER COLUMN id_estado_laboral SET DEFAULT nextval('public.estado_laborales_id_estado_laboral_seq'::regclass);


--
-- Name: estados_factura id_estado_factura; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura ALTER COLUMN id_estado_factura SET DEFAULT nextval('public.estados_factura_id_estado_factura_seq'::regclass);


--
-- Name: factura_detalle id_factura_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle ALTER COLUMN id_factura_detalle SET DEFAULT nextval('public.factura_detalle_id_seq'::regclass);


--
-- Name: facturas id_factura; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas ALTER COLUMN id_factura SET DEFAULT nextval('public.facturas_id_factura_seq'::regclass);


--
-- Name: ficha_antecedentes_familiares id_antecedente_familiar; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_antecedentes_familiares ALTER COLUMN id_antecedente_familiar SET DEFAULT nextval('public.ficha_antecedentes_familiares_id_antecedente_familiar_seq'::regclass);


--
-- Name: ficha_medica id_ficha; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medica ALTER COLUMN id_ficha SET DEFAULT nextval('public.ficha_medica_id_ficha_seq'::regclass);


--
-- Name: ficha_medicacion_habitual id_ficha_medicacion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medicacion_habitual ALTER COLUMN id_ficha_medicacion SET DEFAULT nextval('public.ficha_medicacion_habitual_id_ficha_medicacion_seq'::regclass);


--
-- Name: formas_cobro id_forma_cobro; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro ALTER COLUMN id_forma_cobro SET DEFAULT nextval('public.formas_cobro_id_forma_cobro_seq'::regclass);


--
-- Name: funcionarios id_funcionario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios ALTER COLUMN id_funcionario SET DEFAULT nextval('public.funcionarios_id_funcionario_seq'::regclass);


--
-- Name: generos id_genero; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos ALTER COLUMN id_genero SET DEFAULT nextval('public.generos_id_genero_seq'::regclass);


--
-- Name: grupos_sanguineos id_grupo_sanguineo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.grupos_sanguineos ALTER COLUMN id_grupo_sanguineo SET DEFAULT nextval('public.grupos_sanguineos_id_grupo_sanguineo_seq'::regclass);


--
-- Name: insumos id_insumo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos ALTER COLUMN id_insumo SET DEFAULT nextval('public.insumos_id_insumo_seq'::regclass);


--
-- Name: justificativos id_justificativo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.justificativos ALTER COLUMN id_justificativo SET DEFAULT nextval('public.justificativos_id_justificativo_seq'::regclass);


--
-- Name: medicamentos id_medicamento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicamentos ALTER COLUMN id_medicamento SET DEFAULT nextval('public.medicamentos_id_medicamento_seq'::regclass);


--
-- Name: medicos id_medico; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicos ALTER COLUMN id_medico SET DEFAULT nextval('public.medicos_id_medico_seq'::regclass);


--
-- Name: motivos_nota id_motivo_nota; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.motivos_nota ALTER COLUMN id_motivo_nota SET DEFAULT nextval('public.motivos_nota_id_motivo_nota_seq'::regclass);


--
-- Name: notas id_nota; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas ALTER COLUMN id_nota SET DEFAULT nextval('public.notas_id_seq'::regclass);


--
-- Name: orden_analisis id_orden_analisis; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_analisis ALTER COLUMN id_orden_analisis SET DEFAULT nextval('public.orden_analisis_id_orden_analisis_seq'::regclass);


--
-- Name: orden_estudio id_orden_estudio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_estudio ALTER COLUMN id_orden_estudio SET DEFAULT nextval('public.orden_estudio_id_orden_estudio_seq'::regclass);


--
-- Name: pacientes id_paciente; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes ALTER COLUMN id_paciente SET DEFAULT nextval('public.pacientes_id_paciente_seq'::regclass);


--
-- Name: personas id_persona; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas ALTER COLUMN id_persona SET DEFAULT nextval('public.personas_id_persona_seq'::regclass);


--
-- Name: receta_detalle id_receta_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle ALTER COLUMN id_receta_detalle SET DEFAULT nextval('public.receta_detalle_id_receta_detalle_seq'::regclass);


--
-- Name: recetas id_receta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas ALTER COLUMN id_receta SET DEFAULT nextval('public.recetas_id_receta_seq'::regclass);


--
-- Name: roles id_rol; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id_rol SET DEFAULT nextval('public.roles_id_rol_seq'::regclass);


--
-- Name: sala_atenciones id_sala_atencion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sala_atenciones ALTER COLUMN id_sala_atencion SET DEFAULT nextval('public.sala_atenciones_id_sala_atencion_seq'::regclass);


--
-- Name: servicios_facturables id_servicio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servicios_facturables ALTER COLUMN id_servicio SET DEFAULT nextval('public.servicios_facturables_id_servicio_seq'::regclass);


--
-- Name: signos_vitales id_signos_vitales; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales ALTER COLUMN id_signos_vitales SET DEFAULT nextval('public.signos_vitales_id_seq'::regclass);


--
-- Name: stock_insumos id_movimiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_insumos ALTER COLUMN id_movimiento SET DEFAULT nextval('public.stock_insumos_id_movimiento_seq'::regclass);


--
-- Name: tipo_orden_analisis id_tipo_orden_analisis; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_orden_analisis ALTER COLUMN id_tipo_orden_analisis SET DEFAULT nextval('public.tipo_orden_analisis_id_tipo_orden_analisis_seq'::regclass);


--
-- Name: tipo_orden_estudio id_tipo_orden_estudio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_orden_estudio ALTER COLUMN id_tipo_orden_estudio SET DEFAULT nextval('public.tipo_orden_estudio_id_tipo_orden_estudio_seq'::regclass);


--
-- Name: tipos_alergia id_tipo_alergia; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_alergia ALTER COLUMN id_tipo_alergia SET DEFAULT nextval('public.tipos_alergia_id_tipo_alergia_seq'::regclass);


--
-- Name: tipos_comprobante id_tipo_comprobante; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobante ALTER COLUMN id_tipo_comprobante SET DEFAULT nextval('public.tipos_comprobante_id_tipo_comprobante_seq'::regclass);


--
-- Name: tipos_iva id_tipo_iva; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_iva ALTER COLUMN id_tipo_iva SET DEFAULT nextval('public.tipos_iva_id_tipo_iva_seq'::regclass);


--
-- Name: tratamientos id_tratamiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos ALTER COLUMN id_tratamiento SET DEFAULT nextval('public.tratamientos_id_tratamiento_seq'::regclass);


--
-- Name: turnos id_turno; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.turnos ALTER COLUMN id_turno SET DEFAULT nextval('public.turnos_id_turno_seq'::regclass);


--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- Data for Name: agenda_medicas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.agenda_medicas (id_agenda_medica, id_medico, id_especialidad, id_turno, id_dia, id_estado_laboral, id_sala_atencion, id_funcionario, fecha_registro, hora_inicio, hora_fin, fecha_desde, fecha_hasta) FROM stdin;
17	16	1	3	1	2	1	\N	2026-07-19 14:40:40.97319	\N	\N	\N	\N
18	17	1	3	1	2	2	\N	2026-07-19 14:40:40.97319	\N	\N	\N	\N
19	12	1	2	1	2	1	\N	2026-07-19 14:40:40.97319	\N	\N	\N	\N
20	18	1	3	2	2	1	\N	2026-09-07 18:30:15.763207	\N	\N	\N	\N
25	17	1	2	11	2	1	\N	2026-10-15 20:38:52.06369	\N	\N	\N	\N
26	12	1	3	6	2	1	\N	2026-10-15 20:39:44.525365	\N	\N	\N	\N
27	18	1	3	3	2	1	\N	2026-10-18 11:06:53.168726	\N	\N	\N	\N
32	12	1	2	1	2	1	\N	2026-10-18 21:38:44.074033	06:00:00	12:00:00	2026-10-18	2027-10-18
33	12	1	2	2	2	1	\N	2026-10-18 21:38:44.074033	06:00:00	12:00:00	2026-10-18	2027-10-18
34	16	1	2	2	2	2	\N	2026-10-20 20:40:15.302701	05:00:00	12:00:00	2026-10-20	2026-12-30
35	16	1	2	3	2	2	\N	2026-10-20 20:40:15.302701	05:00:00	12:00:00	2026-10-20	2026-12-30
37	18	1	2	11	2	2	3	2026-10-20 21:13:24.380082	09:00:00	14:00:00	2026-10-21	2026-12-31
38	18	1	2	5	2	2	3	2026-10-20 21:13:24.380082	09:00:00	14:00:00	2026-10-21	2026-12-31
\.


--
-- Data for Name: alergias_paciente; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alergias_paciente (id_alergia_paciente, id_ficha, id_tipo_alergia, descripcion, gravedad) FROM stdin;
1	6	4	irrita la piel	Leve
2	6	2	aparecen ronchas	Moderada
3	12	1	HHHHH	Leve
4	12	7	MMMM	Moderada
\.


--
-- Data for Name: anamnesis_podologica; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.anamnesis_podologica (id_anamnesis, id_consulta, tipo_pie, alteracion_de, onicopatias, area_trabajo, diagnostico_podologico, proxima_cita) FROM stdin;
10	25						\N
11	27						\N
12	28						\N
14	30						\N
15	31						\N
16	32						\N
18	33						\N
\.


--
-- Data for Name: auditoria_accesos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auditoria_accesos (id_auditoria, fecha, id_usuario, usuario, evento, detalle, ip, navegador) FROM stdin;
24	2026-10-20 22:08:01.715064	2	INGRID	LOGIN_OK	Inicio de sesión correcto	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
25	2026-10-20 22:12:20.815031	2	INGRID	LOGOUT	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
26	2026-10-20 22:12:31.059026	2	INGRID	LOGIN_FALLIDO	Clave incorrecta	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
27	2026-10-20 22:12:55.320685	\N	NORMA	LOGIN_FALLIDO	Usuario inexistente o inactivo	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
28	2026-10-20 22:13:00.773066	2	INGRID	LOGIN_OK	Inicio de sesión correcto	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
29	2026-10-20 22:13:53.85745	2	INGRID	LOGOUT	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
30	2026-10-20 22:13:59.809369	7	CAJERA LILA	LOGIN_OK	Inicio de sesión correcto	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
31	2026-10-20 22:14:20.259218	7	CAJERA LILA	LOGOUT	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
32	2026-10-20 22:14:22.431717	7	CAJERA LILA	LOGIN_OK	Inicio de sesión correcto	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
33	2026-10-20 22:14:29.535546	7	CAJERA LILA	LOGOUT	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
34	2026-10-20 22:14:34.978127	2	INGRID	LOGIN_OK	Inicio de sesión correcto	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
35	2026-10-20 22:17:47.078612	2	INGRID	LOGOUT	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
36	2026-10-20 22:17:52.445268	7	CAJERA LILA	LOGIN_OK	Inicio de sesión correcto	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
37	2026-10-20 22:18:32.289587	7	CAJERA LILA	LOGOUT	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
38	2026-10-20 22:19:13.695176	2	INGRID	LOGIN_OK	Inicio de sesión correcto	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
55	2026-10-20 22:34:54.098389	2	INGRID	2FA_ACTIVADO	Configuró la app de autenticación	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
56	2026-10-20 22:34:54.182356	2	INGRID	LOGIN_OK	Inicio de sesión correcto (2FA recién activado)	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
57	2026-10-20 22:35:41.326555	2	INGRID	LOGOUT	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
58	2026-10-20 22:36:47.251372	2	INGRID	2FA_FALLIDO	Código incorrecto (intento 1 de 5)	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
59	2026-10-21 21:23:17.915936	2	INGRID	LOGIN_OK	Inicio de sesión correcto (contraseña + código 2FA)	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36
\.


--
-- Data for Name: avisos_recordatorios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.avisos_recordatorios (id_aviso, id_cita, fecha_programada, fecha_envio, metodo_envio, mensaje, estado, destinatario, intentos_envio, observacion, respuesta, fecha_respuesta, id_funcionario) FROM stdin;
25	44	2026-10-18 21:00:00	2026-10-18 20:49:05.920562	whatsapp	Recordatorio de cita. Por favor, confirme su asistencia.	enviado	0972985793	1	\N	confirmado	2026-10-18 20:50:02.218113	\N
23	36	2026-10-18 12:00:00	2026-10-18 20:54:11.59024	whatsapp	Recordatorio de cita. Por favor, confirme su asistencia.	enviado	0971928380	2	\N	confirmado	2026-10-18 20:54:18.817744	\N
26	46	2026-10-18 09:00:00	\N	whatsapp	Recordatorio de cita. Por favor, confirme su asistencia.	pendiente	098754216	0	\N	\N	\N	\N
20	38	2026-10-23 21:00:00	2026-10-18 13:11:42.340513	whatsapp	Recordatorio de cita. Por favor, confirme su asistencia.	enviado	0972985793	1	\N	confirmado	2026-10-18 13:32:01.073042	\N
\.


--
-- Data for Name: cajas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cajas (id_caja, id_usuario, fecha_apertura, monto_apertura, fecha_cierre, monto_cierre_declarado, monto_cierre_sistema, diferencia, observaciones_cierre, estado) FROM stdin;
1	2	2026-06-22 11:54:27.041147	500.00	2026-06-22 11:55:49.778642	100.00	500.00	-400.00		Cerrada
2	2	2026-06-22 11:56:26.882842	3000.00	2026-06-22 11:56:41.630154	700000.00	3000.00	697000.00		Cerrada
3	2	2026-06-22 12:06:34.554801	200000.00	2026-06-22 12:12:40.300208	0.00	350000.00	-350000.00		Cerrada
4	2	2026-06-23 19:06:52.733911	5555555.00	2026-07-09 19:19:46.192836	440000.00	5555555.00	-5115555.00		Cerrada
5	2	2026-07-09 19:25:32.022199	24000.00	2026-09-01 18:34:54.077007	20000.00	24000.00	-4000.00		Cerrada
6	2	2026-09-01 18:35:17.098348	50000.00	2026-09-06 13:09:55.290121	50000.00	50000.00	0.00		Cerrada
7	2	2026-09-06 13:10:18.888127	3000.00	2026-09-07 18:27:19.099899	673000.00	673000.00	0.00		Cerrada
8	2	2026-09-07 18:34:36.216232	12000.00	2026-10-15 20:53:22.362576	382.00	382000.00	-381618.00		Cerrada
9	2	2026-10-15 20:53:34.607967	20000.00	\N	\N	\N	\N	\N	Abierta
\.


--
-- Data for Name: citas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.citas (id_cita, id_disponibilidad_horaria, id_paciente, fecha_creacion, observacion, id_estado_cita, id_funcionario, fecha_registro) FROM stdin;
25	15	18	2026-06-15 19:45:52.025267		2	\N	2026-07-19 14:40:40.97319
26	16	18	2026-06-15 19:55:34.898102		2	\N	2026-07-19 14:40:40.97319
27	17	17	2026-06-21 19:17:33.858146		2	\N	2026-07-19 14:40:40.97319
28	18	16	2026-07-19 14:10:53.036236		1	\N	2026-07-19 14:40:40.97319
29	19	19	2026-08-31 21:24:22.894818		2	\N	2026-08-31 21:24:22.894818
30	20	19	2026-09-06 14:27:09.026727		2	\N	2026-09-06 14:27:09.026727
31	21	18	2026-09-06 20:36:45.546246	ninguna	2	\N	2026-09-06 20:36:45.546246
32	22	19	2026-09-06 21:10:29.641271		2	\N	2026-09-06 21:10:29.641271
33	23	17	2026-09-07 18:31:48.116677	CONSULTA	2	\N	2026-09-07 18:31:48.116677
34	24	16	2026-09-07 18:36:57.852175		2	\N	2026-09-07 18:36:57.852175
35	25	20	2026-09-29 09:33:52.217478		2	\N	2026-09-29 09:33:52.217478
38	28	21	2026-10-18 13:10:49.462185		2	\N	2026-10-18 13:10:49.462185
37	26	20	2026-10-15 20:42:36.252903		2	\N	2026-10-15 20:42:36.252903
44	35	21	2026-10-18 20:48:03.196174		2	\N	2026-10-18 20:48:03.196174
36	27	19	2026-10-15 20:42:02.507311		2	\N	2026-10-15 20:42:02.507311
40	30	22	2026-10-18 20:23:43.33129		5	\N	2026-10-18 20:23:43.33129
46	75	16	2026-10-18 21:42:05.357948		1	\N	2026-10-18 21:42:05.357948
\.


--
-- Data for Name: ciudades; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ciudades (id_ciudad, descripcion) FROM stdin;
1	SAN ANTONIO
2	ÑEMBY
3	FDO. DE LA MORA
\.


--
-- Data for Name: cobranzas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cobranzas (id_cobranza, id_factura, id_caja, id_forma_cobro, monto, referencia, banco, fecha_cobro, numero_recibo, observaciones) FROM stdin;
1	1	3	1	150000.00			2026-06-22 12:09:20.894594	0000001	
2	2	7	1	150000.00			2026-09-06 13:13:20.083181	0000002	
3	3	7	1	300000.00			2026-09-06 13:18:37.291599	0000003	
6	4	7	1	220000.00			2026-09-06 21:13:48.111849	0000004	
7	5	8	1	370000.00			2026-09-07 18:56:28.861735	0000005	
8	7	9	1	370000.00			2026-10-15 20:55:04.019263	0000006	
9	8	9	1	210000.00			2026-10-18 10:55:00.61404	0000007	
\.


--
-- Data for Name: consulta_diagnosticos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.consulta_diagnosticos (id_consulta_diagnostico, id_consulta, id_enfermedad, id_tratamiento, diagnostico, tratamiento, orden) FROM stdin;
1	28	20	20	\N	\N	1
2	30	16	16	\N	\N	1
3	31	13	13	\N	\N	1
4	32	25	25	\N	\N	1
5	33	22	22	\N	\N	1
9	39	13	13	\N	\N	1
10	39	14	14	\N	\N	2
11	39	16	16	\N	\N	3
\.


--
-- Data for Name: consulta_insumos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.consulta_insumos (id_consulta_insumo, id_consulta, id_insumo, cantidad, observacion) FROM stdin;
27	25	6	1.00	
28	25	3	1.00	
29	27	5	1.00	
30	27	4	2.00	
31	27	9	1.00	
32	28	5	1.00	
33	28	4	1.00	
34	28	9	1.00	
35	28	7	1.00	
36	30	5	1.00	
37	30	4	1.00	
38	30	6	1.00	
39	30	7	1.00	
40	31	9	1.00	
41	31	6	1.00	
42	31	5	1.00	
43	32	9	1.00	
44	32	5	1.00	
45	33	5	1.00	
46	33	9	1.00	
56	39	5	1.00	
57	39	6	3.00	
58	39	7	2.00	TAMAÑOS MEDIANO
62	41	5	1.00	
63	41	7	1.00	
64	41	1	1.00	
65	41	10	1.00	
\.


--
-- Data for Name: consulta_ordenes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.consulta_ordenes (id_consulta_orden, id_consulta, tipo, id_tipo_orden, fecha_emision, fecha_vencimiento, observacion) FROM stdin;
32	37	estudio	3	2026-10-13	2026-11-13	
33	37	estudio	7	2026-10-13	2026-11-13	
34	37	analisis	6	2026-10-13	2026-11-13	
35	37	analisis	11	2026-10-13	2026-10-31	
36	38	estudio	2	2026-10-13	2026-10-31	
37	38	estudio	1	2026-10-13	2026-10-31	
39	39	analisis	2	2026-10-15	2026-10-20	
40	39	analisis	1	2026-10-15	2026-10-29	
42	41	estudio	1	2026-10-18	2026-10-25	
\.


--
-- Data for Name: consulta_procedimientos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.consulta_procedimientos (id_consulta_procedimiento, id_consulta, id_servicio, cantidad, observacion) FROM stdin;
1	30	4	1.00	
2	32	1	1.00	
3	33	1	1.00	
4	33	4	1.00	
17	39	1	1.00	
18	39	4	1.00	
\.


--
-- Data for Name: consultas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.consultas (id_consulta, id_cita, id_tipo_orden_estudio, fecha_emision_estudio, fecha_vencimiento_estudio, id_tipo_orden_analisis, fecha_emision_analisis, fecha_vencimiento_analisis, motivo_consulta, diagnostico, tratamiento, observaciones, fecha_consulta, id_enfermedad, id_tratamiento, requiere_orden_estudio, requiere_orden_analisis, id_funcionario, id_consultorio, diagnostico_presuntivo) FROM stdin;
23	25	\N	\N	\N	\N	\N	\N	Alergia en la piel				2026-06-21 20:36:13.51667	\N	\N	f	f	\N	\N	\N
26	26	\N	2026-09-01	\N	\N	2026-09-01	\N	CONSULTA			DDD	2026-09-01 18:38:27.787723	\N	\N	t	t	\N	\N	\N
27	29	\N	\N	\N	\N	\N	\N	ckekeo			ninguno	2026-09-06 13:03:07.587478	\N	\N	f	f	\N	\N	\N
28	30	\N	\N	\N	\N	\N	\N	chequeo				2026-09-06 14:27:44.468764	20	20	f	f	\N	\N	\N
30	31	\N	\N	\N	\N	\N	\N	ninguna				2026-09-06 20:49:50.532624	16	16	f	f	\N	\N	\N
31	32	\N	\N	\N	\N	\N	\N	chequeo				2026-09-06 21:11:27.177255	13	13	f	f	\N	\N	\N
32	33	\N	\N	\N	\N	\N	\N	CONSULTA				2026-09-07 18:32:22.423871	25	25	f	f	\N	\N	\N
33	34	\N	\N	\N	\N	\N	\N	CONSULTA				2026-09-07 18:47:08.859619	22	22	f	f	\N	\N	\N
25	28	\N	\N	\N	\N	\N	\N	CONSULTA				2026-07-19 14:45:41.413333	\N	\N	f	f	\N	\N	\N
37	35	\N	\N	\N	\N	\N	\N	CHEQUEO				2026-10-13 21:33:33.890284	\N	\N	f	f	\N	\N	\N
38	27	\N	\N	\N	\N	\N	\N	CHEQUEO				2026-10-13 22:05:02.692556	\N	\N	f	f	\N	\N	\N
39	36	\N	\N	\N	\N	\N	\N	DOLORES INTENSOS EN EL TOBILLO				2026-10-15 20:45:00.537055	13	13	f	f	\N	\N	FRACTURA
41	37	\N	\N	\N	\N	\N	\N	DOLORES MUSCULARES				2026-10-18 10:50:45.168692	\N	\N	f	f	\N	\N	POSIBLE FRACTURA
\.


--
-- Data for Name: consultorio; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.consultorio (id_consultorio, nombre, ruc, direccion, telefono, email, id_ciudad, estado, fecha_creacion) FROM stdin;
2	Pódologia Barreto	5601041	San Antonio	0972985793	ingridenriquez74@gmail.com	1	t	2026-10-18 14:14:41.317354
\.


--
-- Data for Name: datos_emisor; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.datos_emisor (id_emisor, razon_social, nombre_fantasia, ruc, timbrado, fecha_inicio_vigencia, fecha_fin_vigencia, punto_expedicion, establecimiento, direccion, telefono, estado, codigo_control, modalidad) FROM stdin;
1	Barreto Gonzalez Silvia Beatriz	Podóloga Silvia Barreto	6326425-0	17232267	2024-05-21	2029-05-21	001	001	Calle San Roque Gonzalez de Santa Cruz, Número #9999 // Casa	0985 11836	t	A04109A3	Factura Virtual
\.


--
-- Data for Name: dias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dias (id_dia, descripcion) FROM stdin;
1	LUNES
2	MARTES
3	MIERCOLES
5	VIERNES
6	SÁBADO
11	JUEVES
\.


--
-- Data for Name: disponibilidad_horaria; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.disponibilidad_horaria (id_disponibilidad_horaria, id_agenda_medica, fecha, hora_inicio, hora_fin, estado, bloqueado) FROM stdin;
76	32	2026-10-19	07:00:00	08:00:00	t	f
77	32	2026-10-19	08:00:00	09:00:00	t	f
78	32	2026-10-19	10:00:00	11:00:00	t	f
79	32	2026-10-19	11:00:00	12:00:00	t	f
80	32	2026-10-26	06:00:00	07:00:00	t	f
81	32	2026-10-26	07:00:00	08:00:00	t	f
82	32	2026-10-26	08:00:00	09:00:00	t	f
83	32	2026-10-26	09:00:00	10:00:00	t	f
84	32	2026-10-26	10:00:00	11:00:00	t	f
85	32	2026-10-26	11:00:00	12:00:00	t	f
86	32	2026-11-02	06:00:00	07:00:00	t	f
87	32	2026-11-02	07:00:00	08:00:00	t	f
88	32	2026-11-02	08:00:00	09:00:00	t	f
89	32	2026-11-02	09:00:00	10:00:00	t	f
90	32	2026-11-02	10:00:00	11:00:00	t	f
91	32	2026-11-02	11:00:00	12:00:00	t	f
92	32	2026-11-09	06:00:00	07:00:00	t	f
93	32	2026-11-09	07:00:00	08:00:00	t	f
94	32	2026-11-09	08:00:00	09:00:00	t	f
95	32	2026-11-09	09:00:00	10:00:00	t	f
96	32	2026-11-09	10:00:00	11:00:00	t	f
97	32	2026-11-09	11:00:00	12:00:00	t	f
98	32	2026-11-16	06:00:00	07:00:00	t	f
99	32	2026-11-16	07:00:00	08:00:00	t	f
100	32	2026-11-16	08:00:00	09:00:00	t	f
101	32	2026-11-16	09:00:00	10:00:00	t	f
102	32	2026-11-16	10:00:00	11:00:00	t	f
103	32	2026-11-16	11:00:00	12:00:00	t	f
104	32	2026-11-23	06:00:00	07:00:00	t	f
105	32	2026-11-23	07:00:00	08:00:00	t	f
106	32	2026-11-23	08:00:00	09:00:00	t	f
107	32	2026-11-23	09:00:00	10:00:00	t	f
108	32	2026-11-23	10:00:00	11:00:00	t	f
109	32	2026-11-23	11:00:00	12:00:00	t	f
110	32	2026-11-30	06:00:00	07:00:00	t	f
111	32	2026-11-30	07:00:00	08:00:00	t	f
112	32	2026-11-30	08:00:00	09:00:00	t	f
15	17	2026-06-22	20:30:00	21:00:00	f	f
16	18	2026-06-23	23:57:00	12:57:00	f	f
17	19	2026-06-29	22:00:00	23:00:00	f	f
18	17	2026-07-27	20:00:00	21:00:00	f	f
19	19	2026-09-07	07:22:00	10:22:00	f	f
20	17	2026-09-15	17:28:00	18:29:00	f	f
21	18	2026-09-07	19:35:00	22:36:00	f	f
22	19	2026-09-21	09:12:00	11:12:00	f	f
23	20	2026-09-08	19:00:00	20:00:00	f	f
24	20	2026-09-15	20:00:00	21:00:00	f	f
25	19	2026-09-30	11:01:00	12:30:00	f	f
27	19	2026-10-19	09:00:00	10:00:00	f	f
26	25	2026-10-22	10:00:00	12:00:00	f	f
28	26	2026-10-24	18:00:00	19:05:00	f	f
113	32	2026-11-30	09:00:00	10:00:00	t	f
114	32	2026-11-30	10:00:00	11:00:00	t	f
30	20	2026-10-13	17:00:00	20:21:00	f	f
115	32	2026-11-30	11:00:00	12:00:00	t	f
116	32	2026-12-07	06:00:00	07:00:00	t	f
117	32	2026-12-07	07:00:00	08:00:00	t	f
118	32	2026-12-07	08:00:00	09:00:00	t	f
119	32	2026-12-07	09:00:00	10:00:00	t	f
120	32	2026-12-07	10:00:00	11:00:00	t	f
121	32	2026-12-07	11:00:00	12:00:00	t	f
122	32	2026-12-14	06:00:00	07:00:00	t	f
123	32	2026-12-14	07:00:00	08:00:00	t	f
35	18	2026-10-19	18:00:00	19:00:00	f	f
124	32	2026-12-14	08:00:00	09:00:00	t	f
125	32	2026-12-14	09:00:00	10:00:00	t	f
126	32	2026-12-14	10:00:00	11:00:00	t	f
127	32	2026-12-14	11:00:00	12:00:00	t	f
128	32	2026-12-21	06:00:00	07:00:00	t	f
129	32	2026-12-21	07:00:00	08:00:00	t	f
130	32	2026-12-21	08:00:00	09:00:00	t	f
131	32	2026-12-21	09:00:00	10:00:00	t	f
132	32	2026-12-21	10:00:00	11:00:00	t	f
133	32	2026-12-21	11:00:00	12:00:00	t	f
134	32	2026-12-28	06:00:00	07:00:00	t	f
135	32	2026-12-28	07:00:00	08:00:00	t	f
136	32	2026-12-28	08:00:00	09:00:00	t	f
137	32	2026-12-28	09:00:00	10:00:00	t	f
138	32	2026-12-28	10:00:00	11:00:00	t	f
139	32	2026-12-28	11:00:00	12:00:00	t	f
140	32	2027-01-04	06:00:00	07:00:00	t	f
141	32	2027-01-04	07:00:00	08:00:00	t	f
142	32	2027-01-04	08:00:00	09:00:00	t	f
143	32	2027-01-04	09:00:00	10:00:00	t	f
144	32	2027-01-04	10:00:00	11:00:00	t	f
145	32	2027-01-04	11:00:00	12:00:00	t	f
146	32	2027-01-11	06:00:00	07:00:00	t	f
147	32	2027-01-11	07:00:00	08:00:00	t	f
148	32	2027-01-11	08:00:00	09:00:00	t	f
149	32	2027-01-11	09:00:00	10:00:00	t	f
150	32	2027-01-11	10:00:00	11:00:00	t	f
151	32	2027-01-11	11:00:00	12:00:00	t	f
152	32	2027-01-18	06:00:00	07:00:00	t	f
153	32	2027-01-18	07:00:00	08:00:00	t	f
154	32	2027-01-18	08:00:00	09:00:00	t	f
155	32	2027-01-18	09:00:00	10:00:00	t	f
156	32	2027-01-18	10:00:00	11:00:00	t	f
157	32	2027-01-18	11:00:00	12:00:00	t	f
158	32	2027-01-25	06:00:00	07:00:00	t	f
159	32	2027-01-25	07:00:00	08:00:00	t	f
160	32	2027-01-25	08:00:00	09:00:00	t	f
161	32	2027-01-25	09:00:00	10:00:00	t	f
162	32	2027-01-25	10:00:00	11:00:00	t	f
163	32	2027-01-25	11:00:00	12:00:00	t	f
164	32	2027-02-01	06:00:00	07:00:00	t	f
165	32	2027-02-01	07:00:00	08:00:00	t	f
166	32	2027-02-01	08:00:00	09:00:00	t	f
167	32	2027-02-01	09:00:00	10:00:00	t	f
168	32	2027-02-01	10:00:00	11:00:00	t	f
169	32	2027-02-01	11:00:00	12:00:00	t	f
170	32	2027-02-08	06:00:00	07:00:00	t	f
171	32	2027-02-08	07:00:00	08:00:00	t	f
172	32	2027-02-08	08:00:00	09:00:00	t	f
173	32	2027-02-08	09:00:00	10:00:00	t	f
174	32	2027-02-08	10:00:00	11:00:00	t	f
175	32	2027-02-08	11:00:00	12:00:00	t	f
176	32	2027-02-15	06:00:00	07:00:00	t	f
177	32	2027-02-15	07:00:00	08:00:00	t	f
178	32	2027-02-15	08:00:00	09:00:00	t	f
179	32	2027-02-15	09:00:00	10:00:00	t	f
180	32	2027-02-15	10:00:00	11:00:00	t	f
181	32	2027-02-15	11:00:00	12:00:00	t	f
182	32	2027-02-22	06:00:00	07:00:00	t	f
183	32	2027-02-22	07:00:00	08:00:00	t	f
184	32	2027-02-22	08:00:00	09:00:00	t	f
185	32	2027-02-22	09:00:00	10:00:00	t	f
186	32	2027-02-22	10:00:00	11:00:00	t	f
187	32	2027-02-22	11:00:00	12:00:00	t	f
188	32	2027-03-01	06:00:00	07:00:00	t	f
189	32	2027-03-01	07:00:00	08:00:00	t	f
190	32	2027-03-01	08:00:00	09:00:00	t	f
191	32	2027-03-01	09:00:00	10:00:00	t	f
192	32	2027-03-01	10:00:00	11:00:00	t	f
193	32	2027-03-01	11:00:00	12:00:00	t	f
194	32	2027-03-08	06:00:00	07:00:00	t	f
195	32	2027-03-08	07:00:00	08:00:00	t	f
196	32	2027-03-08	08:00:00	09:00:00	t	f
197	32	2027-03-08	09:00:00	10:00:00	t	f
198	32	2027-03-08	10:00:00	11:00:00	t	f
199	32	2027-03-08	11:00:00	12:00:00	t	f
200	32	2027-03-15	06:00:00	07:00:00	t	f
201	32	2027-03-15	07:00:00	08:00:00	t	f
202	32	2027-03-15	08:00:00	09:00:00	t	f
203	32	2027-03-15	09:00:00	10:00:00	t	f
204	32	2027-03-15	10:00:00	11:00:00	t	f
205	32	2027-03-15	11:00:00	12:00:00	t	f
206	32	2027-03-22	06:00:00	07:00:00	t	f
207	32	2027-03-22	07:00:00	08:00:00	t	f
208	32	2027-03-22	08:00:00	09:00:00	t	f
209	32	2027-03-22	09:00:00	10:00:00	t	f
210	32	2027-03-22	10:00:00	11:00:00	t	f
211	32	2027-03-22	11:00:00	12:00:00	t	f
212	32	2027-03-29	06:00:00	07:00:00	t	f
213	32	2027-03-29	07:00:00	08:00:00	t	f
214	32	2027-03-29	08:00:00	09:00:00	t	f
215	32	2027-03-29	09:00:00	10:00:00	t	f
216	32	2027-03-29	10:00:00	11:00:00	t	f
217	32	2027-03-29	11:00:00	12:00:00	t	f
218	32	2027-04-05	06:00:00	07:00:00	t	f
219	32	2027-04-05	07:00:00	08:00:00	t	f
220	32	2027-04-05	08:00:00	09:00:00	t	f
221	32	2027-04-05	09:00:00	10:00:00	t	f
222	32	2027-04-05	10:00:00	11:00:00	t	f
223	32	2027-04-05	11:00:00	12:00:00	t	f
224	32	2027-04-12	06:00:00	07:00:00	t	f
225	32	2027-04-12	07:00:00	08:00:00	t	f
226	32	2027-04-12	08:00:00	09:00:00	t	f
227	32	2027-04-12	09:00:00	10:00:00	t	f
228	32	2027-04-12	10:00:00	11:00:00	t	f
229	32	2027-04-12	11:00:00	12:00:00	t	f
230	32	2027-04-19	06:00:00	07:00:00	t	f
231	32	2027-04-19	07:00:00	08:00:00	t	f
232	32	2027-04-19	08:00:00	09:00:00	t	f
233	32	2027-04-19	09:00:00	10:00:00	t	f
234	32	2027-04-19	10:00:00	11:00:00	t	f
235	32	2027-04-19	11:00:00	12:00:00	t	f
236	32	2027-04-26	06:00:00	07:00:00	t	f
237	32	2027-04-26	07:00:00	08:00:00	t	f
238	32	2027-04-26	08:00:00	09:00:00	t	f
239	32	2027-04-26	09:00:00	10:00:00	t	f
240	32	2027-04-26	10:00:00	11:00:00	t	f
241	32	2027-04-26	11:00:00	12:00:00	t	f
242	32	2027-05-03	06:00:00	07:00:00	t	f
243	32	2027-05-03	07:00:00	08:00:00	t	f
244	32	2027-05-03	08:00:00	09:00:00	t	f
245	32	2027-05-03	09:00:00	10:00:00	t	f
246	32	2027-05-03	10:00:00	11:00:00	t	f
247	32	2027-05-03	11:00:00	12:00:00	t	f
248	32	2027-05-10	06:00:00	07:00:00	t	f
249	32	2027-05-10	07:00:00	08:00:00	t	f
250	32	2027-05-10	08:00:00	09:00:00	t	f
251	32	2027-05-10	09:00:00	10:00:00	t	f
252	32	2027-05-10	10:00:00	11:00:00	t	f
253	32	2027-05-10	11:00:00	12:00:00	t	f
254	32	2027-05-17	06:00:00	07:00:00	t	f
255	32	2027-05-17	07:00:00	08:00:00	t	f
256	32	2027-05-17	08:00:00	09:00:00	t	f
257	32	2027-05-17	09:00:00	10:00:00	t	f
258	32	2027-05-17	10:00:00	11:00:00	t	f
259	32	2027-05-17	11:00:00	12:00:00	t	f
260	32	2027-05-24	06:00:00	07:00:00	t	f
261	32	2027-05-24	07:00:00	08:00:00	t	f
262	32	2027-05-24	08:00:00	09:00:00	t	f
263	32	2027-05-24	09:00:00	10:00:00	t	f
264	32	2027-05-24	10:00:00	11:00:00	t	f
265	32	2027-05-24	11:00:00	12:00:00	t	f
266	32	2027-05-31	06:00:00	07:00:00	t	f
267	32	2027-05-31	07:00:00	08:00:00	t	f
268	32	2027-05-31	08:00:00	09:00:00	t	f
269	32	2027-05-31	09:00:00	10:00:00	t	f
270	32	2027-05-31	10:00:00	11:00:00	t	f
271	32	2027-05-31	11:00:00	12:00:00	t	f
272	32	2027-06-07	06:00:00	07:00:00	t	f
273	32	2027-06-07	07:00:00	08:00:00	t	f
274	32	2027-06-07	08:00:00	09:00:00	t	f
275	32	2027-06-07	09:00:00	10:00:00	t	f
276	32	2027-06-07	10:00:00	11:00:00	t	f
277	32	2027-06-07	11:00:00	12:00:00	t	f
278	32	2027-06-14	06:00:00	07:00:00	t	f
279	32	2027-06-14	07:00:00	08:00:00	t	f
280	32	2027-06-14	08:00:00	09:00:00	t	f
281	32	2027-06-14	09:00:00	10:00:00	t	f
282	32	2027-06-14	10:00:00	11:00:00	t	f
283	32	2027-06-14	11:00:00	12:00:00	t	f
284	32	2027-06-21	06:00:00	07:00:00	t	f
285	32	2027-06-21	07:00:00	08:00:00	t	f
286	32	2027-06-21	08:00:00	09:00:00	t	f
287	32	2027-06-21	09:00:00	10:00:00	t	f
288	32	2027-06-21	10:00:00	11:00:00	t	f
289	32	2027-06-21	11:00:00	12:00:00	t	f
290	32	2027-06-28	06:00:00	07:00:00	t	f
291	32	2027-06-28	07:00:00	08:00:00	t	f
292	32	2027-06-28	08:00:00	09:00:00	t	f
293	32	2027-06-28	09:00:00	10:00:00	t	f
294	32	2027-06-28	10:00:00	11:00:00	t	f
295	32	2027-06-28	11:00:00	12:00:00	t	f
296	32	2027-07-05	06:00:00	07:00:00	t	f
297	32	2027-07-05	07:00:00	08:00:00	t	f
298	32	2027-07-05	08:00:00	09:00:00	t	f
299	32	2027-07-05	09:00:00	10:00:00	t	f
300	32	2027-07-05	10:00:00	11:00:00	t	f
301	32	2027-07-05	11:00:00	12:00:00	t	f
302	32	2027-07-12	06:00:00	07:00:00	t	f
303	32	2027-07-12	07:00:00	08:00:00	t	f
304	32	2027-07-12	08:00:00	09:00:00	t	f
305	32	2027-07-12	09:00:00	10:00:00	t	f
306	32	2027-07-12	10:00:00	11:00:00	t	f
307	32	2027-07-12	11:00:00	12:00:00	t	f
308	32	2027-07-19	06:00:00	07:00:00	t	f
309	32	2027-07-19	07:00:00	08:00:00	t	f
310	32	2027-07-19	08:00:00	09:00:00	t	f
311	32	2027-07-19	09:00:00	10:00:00	t	f
312	32	2027-07-19	10:00:00	11:00:00	t	f
313	32	2027-07-19	11:00:00	12:00:00	t	f
314	32	2027-07-26	06:00:00	07:00:00	t	f
315	32	2027-07-26	07:00:00	08:00:00	t	f
316	32	2027-07-26	08:00:00	09:00:00	t	f
317	32	2027-07-26	09:00:00	10:00:00	t	f
318	32	2027-07-26	10:00:00	11:00:00	t	f
319	32	2027-07-26	11:00:00	12:00:00	t	f
320	32	2027-08-02	06:00:00	07:00:00	t	f
321	32	2027-08-02	07:00:00	08:00:00	t	f
322	32	2027-08-02	08:00:00	09:00:00	t	f
323	32	2027-08-02	09:00:00	10:00:00	t	f
324	32	2027-08-02	10:00:00	11:00:00	t	f
325	32	2027-08-02	11:00:00	12:00:00	t	f
326	32	2027-08-09	06:00:00	07:00:00	t	f
327	32	2027-08-09	07:00:00	08:00:00	t	f
328	32	2027-08-09	08:00:00	09:00:00	t	f
329	32	2027-08-09	09:00:00	10:00:00	t	f
330	32	2027-08-09	10:00:00	11:00:00	t	f
331	32	2027-08-09	11:00:00	12:00:00	t	f
332	32	2027-08-16	06:00:00	07:00:00	t	f
333	32	2027-08-16	07:00:00	08:00:00	t	f
334	32	2027-08-16	08:00:00	09:00:00	t	f
335	32	2027-08-16	09:00:00	10:00:00	t	f
336	32	2027-08-16	10:00:00	11:00:00	t	f
337	32	2027-08-16	11:00:00	12:00:00	t	f
338	32	2027-08-23	06:00:00	07:00:00	t	f
339	32	2027-08-23	07:00:00	08:00:00	t	f
340	32	2027-08-23	08:00:00	09:00:00	t	f
341	32	2027-08-23	09:00:00	10:00:00	t	f
342	32	2027-08-23	10:00:00	11:00:00	t	f
343	32	2027-08-23	11:00:00	12:00:00	t	f
344	32	2027-08-30	06:00:00	07:00:00	t	f
345	32	2027-08-30	07:00:00	08:00:00	t	f
346	32	2027-08-30	08:00:00	09:00:00	t	f
347	32	2027-08-30	09:00:00	10:00:00	t	f
348	32	2027-08-30	10:00:00	11:00:00	t	f
349	32	2027-08-30	11:00:00	12:00:00	t	f
350	32	2027-09-06	06:00:00	07:00:00	t	f
351	32	2027-09-06	07:00:00	08:00:00	t	f
352	32	2027-09-06	08:00:00	09:00:00	t	f
353	32	2027-09-06	09:00:00	10:00:00	t	f
354	32	2027-09-06	10:00:00	11:00:00	t	f
355	32	2027-09-06	11:00:00	12:00:00	t	f
356	32	2027-09-13	06:00:00	07:00:00	t	f
357	32	2027-09-13	07:00:00	08:00:00	t	f
358	32	2027-09-13	08:00:00	09:00:00	t	f
359	32	2027-09-13	09:00:00	10:00:00	t	f
360	32	2027-09-13	10:00:00	11:00:00	t	f
361	32	2027-09-13	11:00:00	12:00:00	t	f
362	32	2027-09-20	06:00:00	07:00:00	t	f
363	32	2027-09-20	07:00:00	08:00:00	t	f
364	32	2027-09-20	08:00:00	09:00:00	t	f
365	32	2027-09-20	09:00:00	10:00:00	t	f
366	32	2027-09-20	10:00:00	11:00:00	t	f
367	32	2027-09-20	11:00:00	12:00:00	t	f
368	32	2027-09-27	06:00:00	07:00:00	t	f
369	32	2027-09-27	07:00:00	08:00:00	t	f
370	32	2027-09-27	08:00:00	09:00:00	t	f
371	32	2027-09-27	09:00:00	10:00:00	t	f
372	32	2027-09-27	10:00:00	11:00:00	t	f
373	32	2027-09-27	11:00:00	12:00:00	t	f
374	32	2027-10-04	06:00:00	07:00:00	t	f
375	32	2027-10-04	07:00:00	08:00:00	t	f
376	32	2027-10-04	08:00:00	09:00:00	t	f
377	32	2027-10-04	09:00:00	10:00:00	t	f
378	32	2027-10-04	10:00:00	11:00:00	t	f
379	32	2027-10-04	11:00:00	12:00:00	t	f
380	32	2027-10-11	06:00:00	07:00:00	t	f
381	32	2027-10-11	07:00:00	08:00:00	t	f
382	32	2027-10-11	08:00:00	09:00:00	t	f
383	32	2027-10-11	09:00:00	10:00:00	t	f
384	32	2027-10-11	10:00:00	11:00:00	t	f
385	32	2027-10-11	11:00:00	12:00:00	t	f
386	32	2027-10-18	06:00:00	07:00:00	t	f
387	32	2027-10-18	07:00:00	08:00:00	t	f
388	32	2027-10-18	08:00:00	09:00:00	t	f
389	32	2027-10-18	09:00:00	10:00:00	t	f
390	32	2027-10-18	10:00:00	11:00:00	t	f
391	32	2027-10-18	11:00:00	12:00:00	t	f
392	33	2026-10-20	06:00:00	07:00:00	t	f
393	33	2026-10-20	07:00:00	08:00:00	t	f
394	33	2026-10-20	08:00:00	09:00:00	t	f
395	33	2026-10-20	09:00:00	10:00:00	t	f
396	33	2026-10-20	10:00:00	11:00:00	t	f
397	33	2026-10-20	11:00:00	12:00:00	t	f
398	33	2026-10-27	06:00:00	07:00:00	t	f
399	33	2026-10-27	07:00:00	08:00:00	t	f
400	33	2026-10-27	08:00:00	09:00:00	t	f
401	33	2026-10-27	09:00:00	10:00:00	t	f
402	33	2026-10-27	10:00:00	11:00:00	t	f
403	33	2026-10-27	11:00:00	12:00:00	t	f
404	33	2026-11-03	06:00:00	07:00:00	t	f
405	33	2026-11-03	07:00:00	08:00:00	t	f
406	33	2026-11-03	08:00:00	09:00:00	t	f
407	33	2026-11-03	09:00:00	10:00:00	t	f
408	33	2026-11-03	10:00:00	11:00:00	t	f
409	33	2026-11-03	11:00:00	12:00:00	t	f
410	33	2026-11-10	06:00:00	07:00:00	t	f
411	33	2026-11-10	07:00:00	08:00:00	t	f
412	33	2026-11-10	08:00:00	09:00:00	t	f
413	33	2026-11-10	09:00:00	10:00:00	t	f
414	33	2026-11-10	10:00:00	11:00:00	t	f
415	33	2026-11-10	11:00:00	12:00:00	t	f
416	33	2026-11-17	06:00:00	07:00:00	t	f
417	33	2026-11-17	07:00:00	08:00:00	t	f
418	33	2026-11-17	08:00:00	09:00:00	t	f
419	33	2026-11-17	09:00:00	10:00:00	t	f
420	33	2026-11-17	10:00:00	11:00:00	t	f
421	33	2026-11-17	11:00:00	12:00:00	t	f
422	33	2026-11-24	06:00:00	07:00:00	t	f
423	33	2026-11-24	07:00:00	08:00:00	t	f
424	33	2026-11-24	08:00:00	09:00:00	t	f
425	33	2026-11-24	09:00:00	10:00:00	t	f
426	33	2026-11-24	10:00:00	11:00:00	t	f
427	33	2026-11-24	11:00:00	12:00:00	t	f
428	33	2026-12-01	06:00:00	07:00:00	t	f
429	33	2026-12-01	07:00:00	08:00:00	t	f
430	33	2026-12-01	08:00:00	09:00:00	t	f
431	33	2026-12-01	09:00:00	10:00:00	t	f
432	33	2026-12-01	10:00:00	11:00:00	t	f
433	33	2026-12-01	11:00:00	12:00:00	t	f
434	33	2026-12-08	06:00:00	07:00:00	t	f
435	33	2026-12-08	07:00:00	08:00:00	t	f
436	33	2026-12-08	08:00:00	09:00:00	t	f
437	33	2026-12-08	09:00:00	10:00:00	t	f
438	33	2026-12-08	10:00:00	11:00:00	t	f
439	33	2026-12-08	11:00:00	12:00:00	t	f
440	33	2026-12-15	06:00:00	07:00:00	t	f
441	33	2026-12-15	07:00:00	08:00:00	t	f
442	33	2026-12-15	08:00:00	09:00:00	t	f
443	33	2026-12-15	09:00:00	10:00:00	t	f
444	33	2026-12-15	10:00:00	11:00:00	t	f
445	33	2026-12-15	11:00:00	12:00:00	t	f
446	33	2026-12-22	06:00:00	07:00:00	t	f
447	33	2026-12-22	07:00:00	08:00:00	t	f
448	33	2026-12-22	08:00:00	09:00:00	t	f
449	33	2026-12-22	09:00:00	10:00:00	t	f
450	33	2026-12-22	10:00:00	11:00:00	t	f
451	33	2026-12-22	11:00:00	12:00:00	t	f
452	33	2026-12-29	06:00:00	07:00:00	t	f
453	33	2026-12-29	07:00:00	08:00:00	t	f
454	33	2026-12-29	08:00:00	09:00:00	t	f
455	33	2026-12-29	09:00:00	10:00:00	t	f
456	33	2026-12-29	10:00:00	11:00:00	t	f
457	33	2026-12-29	11:00:00	12:00:00	t	f
458	33	2027-01-05	06:00:00	07:00:00	t	f
459	33	2027-01-05	07:00:00	08:00:00	t	f
460	33	2027-01-05	08:00:00	09:00:00	t	f
461	33	2027-01-05	09:00:00	10:00:00	t	f
462	33	2027-01-05	10:00:00	11:00:00	t	f
463	33	2027-01-05	11:00:00	12:00:00	t	f
464	33	2027-01-12	06:00:00	07:00:00	t	f
465	33	2027-01-12	07:00:00	08:00:00	t	f
466	33	2027-01-12	08:00:00	09:00:00	t	f
467	33	2027-01-12	09:00:00	10:00:00	t	f
468	33	2027-01-12	10:00:00	11:00:00	t	f
469	33	2027-01-12	11:00:00	12:00:00	t	f
470	33	2027-01-19	06:00:00	07:00:00	t	f
471	33	2027-01-19	07:00:00	08:00:00	t	f
472	33	2027-01-19	08:00:00	09:00:00	t	f
473	33	2027-01-19	09:00:00	10:00:00	t	f
474	33	2027-01-19	10:00:00	11:00:00	t	f
475	33	2027-01-19	11:00:00	12:00:00	t	f
476	33	2027-01-26	06:00:00	07:00:00	t	f
477	33	2027-01-26	07:00:00	08:00:00	t	f
478	33	2027-01-26	08:00:00	09:00:00	t	f
479	33	2027-01-26	09:00:00	10:00:00	t	f
480	33	2027-01-26	10:00:00	11:00:00	t	f
481	33	2027-01-26	11:00:00	12:00:00	t	f
482	33	2027-02-02	06:00:00	07:00:00	t	f
483	33	2027-02-02	07:00:00	08:00:00	t	f
484	33	2027-02-02	08:00:00	09:00:00	t	f
485	33	2027-02-02	09:00:00	10:00:00	t	f
486	33	2027-02-02	10:00:00	11:00:00	t	f
487	33	2027-02-02	11:00:00	12:00:00	t	f
488	33	2027-02-09	06:00:00	07:00:00	t	f
489	33	2027-02-09	07:00:00	08:00:00	t	f
490	33	2027-02-09	08:00:00	09:00:00	t	f
491	33	2027-02-09	09:00:00	10:00:00	t	f
492	33	2027-02-09	10:00:00	11:00:00	t	f
493	33	2027-02-09	11:00:00	12:00:00	t	f
494	33	2027-02-16	06:00:00	07:00:00	t	f
495	33	2027-02-16	07:00:00	08:00:00	t	f
496	33	2027-02-16	08:00:00	09:00:00	t	f
497	33	2027-02-16	09:00:00	10:00:00	t	f
498	33	2027-02-16	10:00:00	11:00:00	t	f
499	33	2027-02-16	11:00:00	12:00:00	t	f
500	33	2027-02-23	06:00:00	07:00:00	t	f
501	33	2027-02-23	07:00:00	08:00:00	t	f
502	33	2027-02-23	08:00:00	09:00:00	t	f
503	33	2027-02-23	09:00:00	10:00:00	t	f
504	33	2027-02-23	10:00:00	11:00:00	t	f
505	33	2027-02-23	11:00:00	12:00:00	t	f
506	33	2027-03-02	06:00:00	07:00:00	t	f
507	33	2027-03-02	07:00:00	08:00:00	t	f
508	33	2027-03-02	08:00:00	09:00:00	t	f
509	33	2027-03-02	09:00:00	10:00:00	t	f
510	33	2027-03-02	10:00:00	11:00:00	t	f
511	33	2027-03-02	11:00:00	12:00:00	t	f
512	33	2027-03-09	06:00:00	07:00:00	t	f
513	33	2027-03-09	07:00:00	08:00:00	t	f
514	33	2027-03-09	08:00:00	09:00:00	t	f
515	33	2027-03-09	09:00:00	10:00:00	t	f
516	33	2027-03-09	10:00:00	11:00:00	t	f
517	33	2027-03-09	11:00:00	12:00:00	t	f
518	33	2027-03-16	06:00:00	07:00:00	t	f
519	33	2027-03-16	07:00:00	08:00:00	t	f
520	33	2027-03-16	08:00:00	09:00:00	t	f
521	33	2027-03-16	09:00:00	10:00:00	t	f
522	33	2027-03-16	10:00:00	11:00:00	t	f
523	33	2027-03-16	11:00:00	12:00:00	t	f
524	33	2027-03-23	06:00:00	07:00:00	t	f
525	33	2027-03-23	07:00:00	08:00:00	t	f
526	33	2027-03-23	08:00:00	09:00:00	t	f
527	33	2027-03-23	09:00:00	10:00:00	t	f
528	33	2027-03-23	10:00:00	11:00:00	t	f
529	33	2027-03-23	11:00:00	12:00:00	t	f
530	33	2027-03-30	06:00:00	07:00:00	t	f
531	33	2027-03-30	07:00:00	08:00:00	t	f
532	33	2027-03-30	08:00:00	09:00:00	t	f
533	33	2027-03-30	09:00:00	10:00:00	t	f
534	33	2027-03-30	10:00:00	11:00:00	t	f
535	33	2027-03-30	11:00:00	12:00:00	t	f
536	33	2027-04-06	06:00:00	07:00:00	t	f
537	33	2027-04-06	07:00:00	08:00:00	t	f
538	33	2027-04-06	08:00:00	09:00:00	t	f
539	33	2027-04-06	09:00:00	10:00:00	t	f
540	33	2027-04-06	10:00:00	11:00:00	t	f
541	33	2027-04-06	11:00:00	12:00:00	t	f
542	33	2027-04-13	06:00:00	07:00:00	t	f
543	33	2027-04-13	07:00:00	08:00:00	t	f
544	33	2027-04-13	08:00:00	09:00:00	t	f
545	33	2027-04-13	09:00:00	10:00:00	t	f
546	33	2027-04-13	10:00:00	11:00:00	t	f
547	33	2027-04-13	11:00:00	12:00:00	t	f
548	33	2027-04-20	06:00:00	07:00:00	t	f
549	33	2027-04-20	07:00:00	08:00:00	t	f
550	33	2027-04-20	08:00:00	09:00:00	t	f
551	33	2027-04-20	09:00:00	10:00:00	t	f
552	33	2027-04-20	10:00:00	11:00:00	t	f
553	33	2027-04-20	11:00:00	12:00:00	t	f
554	33	2027-04-27	06:00:00	07:00:00	t	f
555	33	2027-04-27	07:00:00	08:00:00	t	f
556	33	2027-04-27	08:00:00	09:00:00	t	f
557	33	2027-04-27	09:00:00	10:00:00	t	f
558	33	2027-04-27	10:00:00	11:00:00	t	f
559	33	2027-04-27	11:00:00	12:00:00	t	f
560	33	2027-05-04	06:00:00	07:00:00	t	f
561	33	2027-05-04	07:00:00	08:00:00	t	f
562	33	2027-05-04	08:00:00	09:00:00	t	f
563	33	2027-05-04	09:00:00	10:00:00	t	f
564	33	2027-05-04	10:00:00	11:00:00	t	f
565	33	2027-05-04	11:00:00	12:00:00	t	f
566	33	2027-05-11	06:00:00	07:00:00	t	f
567	33	2027-05-11	07:00:00	08:00:00	t	f
568	33	2027-05-11	08:00:00	09:00:00	t	f
569	33	2027-05-11	09:00:00	10:00:00	t	f
570	33	2027-05-11	10:00:00	11:00:00	t	f
571	33	2027-05-11	11:00:00	12:00:00	t	f
572	33	2027-05-18	06:00:00	07:00:00	t	f
573	33	2027-05-18	07:00:00	08:00:00	t	f
574	33	2027-05-18	08:00:00	09:00:00	t	f
575	33	2027-05-18	09:00:00	10:00:00	t	f
576	33	2027-05-18	10:00:00	11:00:00	t	f
577	33	2027-05-18	11:00:00	12:00:00	t	f
578	33	2027-05-25	06:00:00	07:00:00	t	f
579	33	2027-05-25	07:00:00	08:00:00	t	f
580	33	2027-05-25	08:00:00	09:00:00	t	f
581	33	2027-05-25	09:00:00	10:00:00	t	f
582	33	2027-05-25	10:00:00	11:00:00	t	f
583	33	2027-05-25	11:00:00	12:00:00	t	f
584	33	2027-06-01	06:00:00	07:00:00	t	f
585	33	2027-06-01	07:00:00	08:00:00	t	f
586	33	2027-06-01	08:00:00	09:00:00	t	f
587	33	2027-06-01	09:00:00	10:00:00	t	f
588	33	2027-06-01	10:00:00	11:00:00	t	f
589	33	2027-06-01	11:00:00	12:00:00	t	f
590	33	2027-06-08	06:00:00	07:00:00	t	f
591	33	2027-06-08	07:00:00	08:00:00	t	f
592	33	2027-06-08	08:00:00	09:00:00	t	f
593	33	2027-06-08	09:00:00	10:00:00	t	f
594	33	2027-06-08	10:00:00	11:00:00	t	f
595	33	2027-06-08	11:00:00	12:00:00	t	f
596	33	2027-06-15	06:00:00	07:00:00	t	f
597	33	2027-06-15	07:00:00	08:00:00	t	f
598	33	2027-06-15	08:00:00	09:00:00	t	f
599	33	2027-06-15	09:00:00	10:00:00	t	f
600	33	2027-06-15	10:00:00	11:00:00	t	f
601	33	2027-06-15	11:00:00	12:00:00	t	f
602	33	2027-06-22	06:00:00	07:00:00	t	f
603	33	2027-06-22	07:00:00	08:00:00	t	f
604	33	2027-06-22	08:00:00	09:00:00	t	f
605	33	2027-06-22	09:00:00	10:00:00	t	f
606	33	2027-06-22	10:00:00	11:00:00	t	f
607	33	2027-06-22	11:00:00	12:00:00	t	f
608	33	2027-06-29	06:00:00	07:00:00	t	f
609	33	2027-06-29	07:00:00	08:00:00	t	f
610	33	2027-06-29	08:00:00	09:00:00	t	f
611	33	2027-06-29	09:00:00	10:00:00	t	f
612	33	2027-06-29	10:00:00	11:00:00	t	f
613	33	2027-06-29	11:00:00	12:00:00	t	f
614	33	2027-07-06	06:00:00	07:00:00	t	f
615	33	2027-07-06	07:00:00	08:00:00	t	f
616	33	2027-07-06	08:00:00	09:00:00	t	f
617	33	2027-07-06	09:00:00	10:00:00	t	f
618	33	2027-07-06	10:00:00	11:00:00	t	f
619	33	2027-07-06	11:00:00	12:00:00	t	f
620	33	2027-07-13	06:00:00	07:00:00	t	f
621	33	2027-07-13	07:00:00	08:00:00	t	f
622	33	2027-07-13	08:00:00	09:00:00	t	f
623	33	2027-07-13	09:00:00	10:00:00	t	f
624	33	2027-07-13	10:00:00	11:00:00	t	f
625	33	2027-07-13	11:00:00	12:00:00	t	f
626	33	2027-07-20	06:00:00	07:00:00	t	f
627	33	2027-07-20	07:00:00	08:00:00	t	f
628	33	2027-07-20	08:00:00	09:00:00	t	f
629	33	2027-07-20	09:00:00	10:00:00	t	f
630	33	2027-07-20	10:00:00	11:00:00	t	f
631	33	2027-07-20	11:00:00	12:00:00	t	f
632	33	2027-07-27	06:00:00	07:00:00	t	f
633	33	2027-07-27	07:00:00	08:00:00	t	f
634	33	2027-07-27	08:00:00	09:00:00	t	f
635	33	2027-07-27	09:00:00	10:00:00	t	f
636	33	2027-07-27	10:00:00	11:00:00	t	f
637	33	2027-07-27	11:00:00	12:00:00	t	f
638	33	2027-08-03	06:00:00	07:00:00	t	f
639	33	2027-08-03	07:00:00	08:00:00	t	f
640	33	2027-08-03	08:00:00	09:00:00	t	f
641	33	2027-08-03	09:00:00	10:00:00	t	f
642	33	2027-08-03	10:00:00	11:00:00	t	f
643	33	2027-08-03	11:00:00	12:00:00	t	f
644	33	2027-08-10	06:00:00	07:00:00	t	f
645	33	2027-08-10	07:00:00	08:00:00	t	f
646	33	2027-08-10	08:00:00	09:00:00	t	f
647	33	2027-08-10	09:00:00	10:00:00	t	f
648	33	2027-08-10	10:00:00	11:00:00	t	f
649	33	2027-08-10	11:00:00	12:00:00	t	f
650	33	2027-08-17	06:00:00	07:00:00	t	f
651	33	2027-08-17	07:00:00	08:00:00	t	f
652	33	2027-08-17	08:00:00	09:00:00	t	f
653	33	2027-08-17	09:00:00	10:00:00	t	f
654	33	2027-08-17	10:00:00	11:00:00	t	f
655	33	2027-08-17	11:00:00	12:00:00	t	f
656	33	2027-08-24	06:00:00	07:00:00	t	f
657	33	2027-08-24	07:00:00	08:00:00	t	f
658	33	2027-08-24	08:00:00	09:00:00	t	f
659	33	2027-08-24	09:00:00	10:00:00	t	f
660	33	2027-08-24	10:00:00	11:00:00	t	f
661	33	2027-08-24	11:00:00	12:00:00	t	f
662	33	2027-08-31	06:00:00	07:00:00	t	f
663	33	2027-08-31	07:00:00	08:00:00	t	f
664	33	2027-08-31	08:00:00	09:00:00	t	f
665	33	2027-08-31	09:00:00	10:00:00	t	f
666	33	2027-08-31	10:00:00	11:00:00	t	f
667	33	2027-08-31	11:00:00	12:00:00	t	f
668	33	2027-09-07	06:00:00	07:00:00	t	f
669	33	2027-09-07	07:00:00	08:00:00	t	f
670	33	2027-09-07	08:00:00	09:00:00	t	f
671	33	2027-09-07	09:00:00	10:00:00	t	f
672	33	2027-09-07	10:00:00	11:00:00	t	f
673	33	2027-09-07	11:00:00	12:00:00	t	f
674	33	2027-09-14	06:00:00	07:00:00	t	f
675	33	2027-09-14	07:00:00	08:00:00	t	f
676	33	2027-09-14	08:00:00	09:00:00	t	f
677	33	2027-09-14	09:00:00	10:00:00	t	f
678	33	2027-09-14	10:00:00	11:00:00	t	f
679	33	2027-09-14	11:00:00	12:00:00	t	f
680	33	2027-09-21	06:00:00	07:00:00	t	f
681	33	2027-09-21	07:00:00	08:00:00	t	f
682	33	2027-09-21	08:00:00	09:00:00	t	f
683	33	2027-09-21	09:00:00	10:00:00	t	f
684	33	2027-09-21	10:00:00	11:00:00	t	f
685	33	2027-09-21	11:00:00	12:00:00	t	f
686	33	2027-09-28	06:00:00	07:00:00	t	f
687	33	2027-09-28	07:00:00	08:00:00	t	f
688	33	2027-09-28	08:00:00	09:00:00	t	f
689	33	2027-09-28	09:00:00	10:00:00	t	f
690	33	2027-09-28	10:00:00	11:00:00	t	f
691	33	2027-09-28	11:00:00	12:00:00	t	f
692	33	2027-10-05	06:00:00	07:00:00	t	f
693	33	2027-10-05	07:00:00	08:00:00	t	f
694	33	2027-10-05	08:00:00	09:00:00	t	f
695	33	2027-10-05	09:00:00	10:00:00	t	f
696	33	2027-10-05	10:00:00	11:00:00	t	f
697	33	2027-10-05	11:00:00	12:00:00	t	f
698	33	2027-10-12	06:00:00	07:00:00	t	f
699	33	2027-10-12	07:00:00	08:00:00	t	f
700	33	2027-10-12	08:00:00	09:00:00	t	f
701	33	2027-10-12	09:00:00	10:00:00	t	f
702	33	2027-10-12	10:00:00	11:00:00	t	f
703	33	2027-10-12	11:00:00	12:00:00	t	f
75	32	2026-10-19	06:00:00	07:00:00	f	f
704	34	2026-10-20	05:00:00	06:00:00	t	f
705	34	2026-10-20	06:00:00	07:00:00	t	f
706	34	2026-10-20	07:00:00	08:00:00	t	f
707	34	2026-10-20	08:00:00	09:00:00	t	f
708	34	2026-10-20	09:00:00	10:00:00	t	f
709	34	2026-10-20	10:00:00	11:00:00	t	f
710	34	2026-10-20	11:00:00	12:00:00	t	f
711	34	2026-10-27	05:00:00	06:00:00	t	f
712	34	2026-10-27	06:00:00	07:00:00	t	f
713	34	2026-10-27	07:00:00	08:00:00	t	f
714	34	2026-10-27	08:00:00	09:00:00	t	f
715	34	2026-10-27	09:00:00	10:00:00	t	f
716	34	2026-10-27	10:00:00	11:00:00	t	f
717	34	2026-10-27	11:00:00	12:00:00	t	f
718	34	2026-11-03	05:00:00	06:00:00	t	f
719	34	2026-11-03	06:00:00	07:00:00	t	f
720	34	2026-11-03	07:00:00	08:00:00	t	f
721	34	2026-11-03	08:00:00	09:00:00	t	f
722	34	2026-11-03	09:00:00	10:00:00	t	f
723	34	2026-11-03	10:00:00	11:00:00	t	f
724	34	2026-11-03	11:00:00	12:00:00	t	f
725	34	2026-11-10	05:00:00	06:00:00	t	f
726	34	2026-11-10	06:00:00	07:00:00	t	f
727	34	2026-11-10	07:00:00	08:00:00	t	f
728	34	2026-11-10	08:00:00	09:00:00	t	f
729	34	2026-11-10	09:00:00	10:00:00	t	f
730	34	2026-11-10	10:00:00	11:00:00	t	f
731	34	2026-11-10	11:00:00	12:00:00	t	f
732	34	2026-11-17	05:00:00	06:00:00	t	f
733	34	2026-11-17	06:00:00	07:00:00	t	f
734	34	2026-11-17	07:00:00	08:00:00	t	f
735	34	2026-11-17	08:00:00	09:00:00	t	f
736	34	2026-11-17	09:00:00	10:00:00	t	f
737	34	2026-11-17	10:00:00	11:00:00	t	f
738	34	2026-11-17	11:00:00	12:00:00	t	f
739	34	2026-11-24	05:00:00	06:00:00	t	f
740	34	2026-11-24	06:00:00	07:00:00	t	f
741	34	2026-11-24	07:00:00	08:00:00	t	f
742	34	2026-11-24	08:00:00	09:00:00	t	f
743	34	2026-11-24	09:00:00	10:00:00	t	f
744	34	2026-11-24	10:00:00	11:00:00	t	f
745	34	2026-11-24	11:00:00	12:00:00	t	f
746	34	2026-12-01	05:00:00	06:00:00	t	f
747	34	2026-12-01	06:00:00	07:00:00	t	f
748	34	2026-12-01	07:00:00	08:00:00	t	f
749	34	2026-12-01	08:00:00	09:00:00	t	f
750	34	2026-12-01	09:00:00	10:00:00	t	f
751	34	2026-12-01	10:00:00	11:00:00	t	f
752	34	2026-12-01	11:00:00	12:00:00	t	f
753	34	2026-12-08	05:00:00	06:00:00	t	f
754	34	2026-12-08	06:00:00	07:00:00	t	f
755	34	2026-12-08	07:00:00	08:00:00	t	f
756	34	2026-12-08	08:00:00	09:00:00	t	f
757	34	2026-12-08	09:00:00	10:00:00	t	f
758	34	2026-12-08	10:00:00	11:00:00	t	f
759	34	2026-12-08	11:00:00	12:00:00	t	f
760	34	2026-12-15	05:00:00	06:00:00	t	f
761	34	2026-12-15	06:00:00	07:00:00	t	f
762	34	2026-12-15	07:00:00	08:00:00	t	f
763	34	2026-12-15	08:00:00	09:00:00	t	f
764	34	2026-12-15	09:00:00	10:00:00	t	f
765	34	2026-12-15	10:00:00	11:00:00	t	f
766	34	2026-12-15	11:00:00	12:00:00	t	f
767	34	2026-12-22	05:00:00	06:00:00	t	f
768	34	2026-12-22	06:00:00	07:00:00	t	f
769	34	2026-12-22	07:00:00	08:00:00	t	f
770	34	2026-12-22	08:00:00	09:00:00	t	f
771	34	2026-12-22	09:00:00	10:00:00	t	f
772	34	2026-12-22	10:00:00	11:00:00	t	f
773	34	2026-12-22	11:00:00	12:00:00	t	f
774	34	2026-12-29	05:00:00	06:00:00	t	f
775	34	2026-12-29	06:00:00	07:00:00	t	f
776	34	2026-12-29	07:00:00	08:00:00	t	f
777	34	2026-12-29	08:00:00	09:00:00	t	f
778	34	2026-12-29	09:00:00	10:00:00	t	f
779	34	2026-12-29	10:00:00	11:00:00	t	f
780	34	2026-12-29	11:00:00	12:00:00	t	f
781	35	2026-10-21	05:00:00	06:00:00	t	f
782	35	2026-10-21	06:00:00	07:00:00	t	f
783	35	2026-10-21	07:00:00	08:00:00	t	f
784	35	2026-10-21	08:00:00	09:00:00	t	f
785	35	2026-10-21	09:00:00	10:00:00	t	f
786	35	2026-10-21	10:00:00	11:00:00	t	f
787	35	2026-10-21	11:00:00	12:00:00	t	f
788	35	2026-10-28	05:00:00	06:00:00	t	f
789	35	2026-10-28	06:00:00	07:00:00	t	f
790	35	2026-10-28	07:00:00	08:00:00	t	f
791	35	2026-10-28	08:00:00	09:00:00	t	f
792	35	2026-10-28	09:00:00	10:00:00	t	f
793	35	2026-10-28	10:00:00	11:00:00	t	f
794	35	2026-10-28	11:00:00	12:00:00	t	f
795	35	2026-11-04	05:00:00	06:00:00	t	f
796	35	2026-11-04	06:00:00	07:00:00	t	f
797	35	2026-11-04	07:00:00	08:00:00	t	f
798	35	2026-11-04	08:00:00	09:00:00	t	f
799	35	2026-11-04	09:00:00	10:00:00	t	f
800	35	2026-11-04	10:00:00	11:00:00	t	f
801	35	2026-11-04	11:00:00	12:00:00	t	f
802	35	2026-11-11	05:00:00	06:00:00	t	f
803	35	2026-11-11	06:00:00	07:00:00	t	f
804	35	2026-11-11	07:00:00	08:00:00	t	f
805	35	2026-11-11	08:00:00	09:00:00	t	f
806	35	2026-11-11	09:00:00	10:00:00	t	f
807	35	2026-11-11	10:00:00	11:00:00	t	f
808	35	2026-11-11	11:00:00	12:00:00	t	f
809	35	2026-11-18	05:00:00	06:00:00	t	f
810	35	2026-11-18	06:00:00	07:00:00	t	f
811	35	2026-11-18	07:00:00	08:00:00	t	f
812	35	2026-11-18	08:00:00	09:00:00	t	f
813	35	2026-11-18	09:00:00	10:00:00	t	f
814	35	2026-11-18	10:00:00	11:00:00	t	f
815	35	2026-11-18	11:00:00	12:00:00	t	f
816	35	2026-11-25	05:00:00	06:00:00	t	f
817	35	2026-11-25	06:00:00	07:00:00	t	f
818	35	2026-11-25	07:00:00	08:00:00	t	f
819	35	2026-11-25	08:00:00	09:00:00	t	f
820	35	2026-11-25	09:00:00	10:00:00	t	f
821	35	2026-11-25	10:00:00	11:00:00	t	f
822	35	2026-11-25	11:00:00	12:00:00	t	f
823	35	2026-12-02	05:00:00	06:00:00	t	f
824	35	2026-12-02	06:00:00	07:00:00	t	f
825	35	2026-12-02	07:00:00	08:00:00	t	f
826	35	2026-12-02	08:00:00	09:00:00	t	f
827	35	2026-12-02	09:00:00	10:00:00	t	f
828	35	2026-12-02	10:00:00	11:00:00	t	f
829	35	2026-12-02	11:00:00	12:00:00	t	f
830	35	2026-12-09	05:00:00	06:00:00	t	f
831	35	2026-12-09	06:00:00	07:00:00	t	f
832	35	2026-12-09	07:00:00	08:00:00	t	f
833	35	2026-12-09	08:00:00	09:00:00	t	f
834	35	2026-12-09	09:00:00	10:00:00	t	f
835	35	2026-12-09	10:00:00	11:00:00	t	f
836	35	2026-12-09	11:00:00	12:00:00	t	f
837	35	2026-12-16	05:00:00	06:00:00	t	f
838	35	2026-12-16	06:00:00	07:00:00	t	f
839	35	2026-12-16	07:00:00	08:00:00	t	f
840	35	2026-12-16	08:00:00	09:00:00	t	f
841	35	2026-12-16	09:00:00	10:00:00	t	f
842	35	2026-12-16	10:00:00	11:00:00	t	f
843	35	2026-12-16	11:00:00	12:00:00	t	f
844	35	2026-12-23	05:00:00	06:00:00	t	f
845	35	2026-12-23	06:00:00	07:00:00	t	f
846	35	2026-12-23	07:00:00	08:00:00	t	f
847	35	2026-12-23	08:00:00	09:00:00	t	f
848	35	2026-12-23	09:00:00	10:00:00	t	f
849	35	2026-12-23	10:00:00	11:00:00	t	f
850	35	2026-12-23	11:00:00	12:00:00	t	f
851	35	2026-12-30	05:00:00	06:00:00	t	f
852	35	2026-12-30	06:00:00	07:00:00	t	f
853	35	2026-12-30	07:00:00	08:00:00	t	f
854	35	2026-12-30	08:00:00	09:00:00	t	f
855	35	2026-12-30	09:00:00	10:00:00	t	f
856	35	2026-12-30	10:00:00	11:00:00	t	f
857	35	2026-12-30	11:00:00	12:00:00	t	f
908	37	2026-10-22	09:00:00	10:00:00	t	f
909	37	2026-10-22	10:00:00	11:00:00	t	f
910	37	2026-10-22	11:00:00	12:00:00	t	f
911	37	2026-10-22	12:00:00	13:00:00	t	f
912	37	2026-10-22	13:00:00	14:00:00	t	f
913	37	2026-10-29	09:00:00	10:00:00	t	f
914	37	2026-10-29	10:00:00	11:00:00	t	f
915	37	2026-10-29	11:00:00	12:00:00	t	f
916	37	2026-10-29	12:00:00	13:00:00	t	f
917	37	2026-10-29	13:00:00	14:00:00	t	f
918	37	2026-11-05	09:00:00	10:00:00	t	f
919	37	2026-11-05	10:00:00	11:00:00	t	f
920	37	2026-11-05	11:00:00	12:00:00	t	f
921	37	2026-11-05	12:00:00	13:00:00	t	f
922	37	2026-11-05	13:00:00	14:00:00	t	f
923	37	2026-11-12	09:00:00	10:00:00	t	f
924	37	2026-11-12	10:00:00	11:00:00	t	f
925	37	2026-11-12	11:00:00	12:00:00	t	f
926	37	2026-11-12	12:00:00	13:00:00	t	f
927	37	2026-11-12	13:00:00	14:00:00	t	f
928	37	2026-11-19	09:00:00	10:00:00	t	f
929	37	2026-11-19	10:00:00	11:00:00	t	f
930	37	2026-11-19	11:00:00	12:00:00	t	f
931	37	2026-11-19	12:00:00	13:00:00	t	f
932	37	2026-11-19	13:00:00	14:00:00	t	f
933	37	2026-11-26	09:00:00	10:00:00	t	f
934	37	2026-11-26	10:00:00	11:00:00	t	f
935	37	2026-11-26	11:00:00	12:00:00	t	f
936	37	2026-11-26	12:00:00	13:00:00	t	f
937	37	2026-11-26	13:00:00	14:00:00	t	f
938	37	2026-12-03	09:00:00	10:00:00	t	f
939	37	2026-12-03	10:00:00	11:00:00	t	f
940	37	2026-12-03	11:00:00	12:00:00	t	f
941	37	2026-12-03	12:00:00	13:00:00	t	f
942	37	2026-12-03	13:00:00	14:00:00	t	f
943	37	2026-12-10	09:00:00	10:00:00	t	f
944	37	2026-12-10	10:00:00	11:00:00	t	f
945	37	2026-12-10	11:00:00	12:00:00	t	f
946	37	2026-12-10	12:00:00	13:00:00	t	f
947	37	2026-12-10	13:00:00	14:00:00	t	f
948	37	2026-12-17	09:00:00	10:00:00	t	f
949	37	2026-12-17	10:00:00	11:00:00	t	f
950	37	2026-12-17	11:00:00	12:00:00	t	f
951	37	2026-12-17	12:00:00	13:00:00	t	f
952	37	2026-12-17	13:00:00	14:00:00	t	f
953	37	2026-12-24	09:00:00	10:00:00	t	f
954	37	2026-12-24	10:00:00	11:00:00	t	f
955	37	2026-12-24	11:00:00	12:00:00	t	f
956	37	2026-12-24	12:00:00	13:00:00	t	f
957	37	2026-12-24	13:00:00	14:00:00	t	f
958	37	2026-12-31	09:00:00	10:00:00	t	f
959	37	2026-12-31	10:00:00	11:00:00	t	f
960	37	2026-12-31	11:00:00	12:00:00	t	f
961	37	2026-12-31	12:00:00	13:00:00	t	f
962	37	2026-12-31	13:00:00	14:00:00	t	f
963	38	2026-10-23	09:00:00	10:00:00	t	f
964	38	2026-10-23	10:00:00	11:00:00	t	f
965	38	2026-10-23	11:00:00	12:00:00	t	f
966	38	2026-10-23	12:00:00	13:00:00	t	f
967	38	2026-10-23	13:00:00	14:00:00	t	f
968	38	2026-10-30	09:00:00	10:00:00	t	f
969	38	2026-10-30	10:00:00	11:00:00	t	f
970	38	2026-10-30	11:00:00	12:00:00	t	f
971	38	2026-10-30	12:00:00	13:00:00	t	f
972	38	2026-10-30	13:00:00	14:00:00	t	f
973	38	2026-11-06	09:00:00	10:00:00	t	f
974	38	2026-11-06	10:00:00	11:00:00	t	f
975	38	2026-11-06	11:00:00	12:00:00	t	f
976	38	2026-11-06	12:00:00	13:00:00	t	f
977	38	2026-11-06	13:00:00	14:00:00	t	f
978	38	2026-11-13	09:00:00	10:00:00	t	f
979	38	2026-11-13	10:00:00	11:00:00	t	f
980	38	2026-11-13	11:00:00	12:00:00	t	f
981	38	2026-11-13	12:00:00	13:00:00	t	f
982	38	2026-11-13	13:00:00	14:00:00	t	f
983	38	2026-11-20	09:00:00	10:00:00	t	f
984	38	2026-11-20	10:00:00	11:00:00	t	f
985	38	2026-11-20	11:00:00	12:00:00	t	f
986	38	2026-11-20	12:00:00	13:00:00	t	f
987	38	2026-11-20	13:00:00	14:00:00	t	f
988	38	2026-11-27	09:00:00	10:00:00	t	f
989	38	2026-11-27	10:00:00	11:00:00	t	f
990	38	2026-11-27	11:00:00	12:00:00	t	f
991	38	2026-11-27	12:00:00	13:00:00	t	f
992	38	2026-11-27	13:00:00	14:00:00	t	f
993	38	2026-12-04	09:00:00	10:00:00	t	f
994	38	2026-12-04	10:00:00	11:00:00	t	f
995	38	2026-12-04	11:00:00	12:00:00	t	f
996	38	2026-12-04	12:00:00	13:00:00	t	f
997	38	2026-12-04	13:00:00	14:00:00	t	f
998	38	2026-12-11	09:00:00	10:00:00	t	f
999	38	2026-12-11	10:00:00	11:00:00	t	f
1000	38	2026-12-11	11:00:00	12:00:00	t	f
1001	38	2026-12-11	12:00:00	13:00:00	t	f
1002	38	2026-12-11	13:00:00	14:00:00	t	f
1003	38	2026-12-18	09:00:00	10:00:00	t	f
1004	38	2026-12-18	10:00:00	11:00:00	t	f
1005	38	2026-12-18	11:00:00	12:00:00	t	f
1006	38	2026-12-18	12:00:00	13:00:00	t	f
1007	38	2026-12-18	13:00:00	14:00:00	t	f
1008	38	2026-12-25	09:00:00	10:00:00	t	f
1009	38	2026-12-25	10:00:00	11:00:00	t	f
1010	38	2026-12-25	11:00:00	12:00:00	t	f
1011	38	2026-12-25	12:00:00	13:00:00	t	f
1012	38	2026-12-25	13:00:00	14:00:00	t	f
\.


--
-- Data for Name: enfermedades; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enfermedades (id_enfermedad, codigo_cie, descripcion, estado) FROM stdin;
1	J06.9	Infección aguda de las vías respiratorias superiores	t
2	J18.9	Neumonía, no especificada	t
3	E11	Diabetes mellitus tipo 2	t
4	I10	Hipertensión esencial (primaria)	t
5	K29.7	Gastritis, no especificada	t
6	M54.5	Lumbago	t
7	J30.1	Rinitis alérgica	t
8	L23	Dermatitis alérgica de contacto	t
9	N39.0	Infección de vías urinarias	t
10	R51	Cefalea	t
11	M20.1	Hallux valgus (juanete) adquirido	t
12	M20.4	Otros dedos del pie en martillo (adquiridos)	t
13	M21.6	Otras deformidades adquiridas del tobillo y del pie	t
14	M72.2	Fibromatosis de la fascia plantar (fascitis plantar)	t
15	M77.3	Espolón calcáneo	t
16	L60.0	Uña encarnada (onicocriptosis)	t
17	L60.2	Onicogrifosis	t
18	L60.3	Distrofia ungueal	t
19	B35.1	Onicomicosis (tiña ungueal)	t
20	L84	Callosidades y callos (helomas)	t
21	L98.9	Lesión cutánea del pie, no especificada (heridas/úlceras superficiales)	t
22	Q66.5	Pie plano congénito	t
23	Q66.7	Pie cavo congénito	t
24	I73.9	Enfermedad vascular periférica, no especificada	t
25	E11.5	Diabetes mellitus tipo 2 con complicaciones circulatorias periféricas (pie diabético)	t
\.


--
-- Data for Name: especialidades; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.especialidades (id_especialidad, descripcion) FROM stdin;
1	PODOLOGIA
\.


--
-- Data for Name: estado_citas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.estado_citas (id_estado_cita, descripcion) FROM stdin;
1	Pendiente
2	Confirmada
3	Cancelada
4	Completada
5	No Asistió
\.


--
-- Data for Name: estado_civiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.estado_civiles (id_estado_civil, descripcion) FROM stdin;
1	CASADO
2	MENOR DE EDAD
3	SOLTERO
\.


--
-- Data for Name: estado_laborales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.estado_laborales (id_estado_laboral, descripcion) FROM stdin;
1	INACTIVO
2	ACTIVO
\.


--
-- Data for Name: estados_factura; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.estados_factura (id_estado_factura, descripcion) FROM stdin;
1	Pendiente
2	Pagada Parcial
3	Pagada
4	Anulada
\.


--
-- Data for Name: factura_detalle; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.factura_detalle (id_factura_detalle, id_factura, id_servicio, descripcion, cantidad, precio_unitario, id_tipo_iva, subtotal) FROM stdin;
1	1	1	Consulta Podológica General	1.00	150000.00	1	150000.00
2	2	1	Consulta Podológica General	1.00	150000.00	1	150000.00
3	3	1	Consulta Podológica General	1.00	150000.00	1	150000.00
4	4	4	Corrección de Uña Encarnada	1.00	220000.00	1	220000.00
5	5	1	Consulta Podológica General	1.00	150000.00	1	150000.00
6	5	4	Corrección de Uña Encarnada	1.00	220000.00	1	220000.00
9	7	1	Consulta Podológica General	1.00	150000.00	1	150000.00
10	7	4	Corrección de Uña Encarnada	1.00	220000.00	1	220000.00
11	8	1	Consulta Podológica General	1.00	150000.00	1	150000.00
12	8	\N	Alcohol 70° (Ml)	1.00	10000.00	2	10000.00
13	8	\N	Tiras reactivas glucemia (Unidad)	1.00	50000.00	2	50000.00
\.


--
-- Data for Name: facturas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facturas (id_factura, id_consulta, id_caja, id_emisor, establecimiento, punto_expedicion, numero_factura, timbrado, ruc_ci_cliente, nombre_cliente, fecha_emision, condicion_venta, numero_nota_remision, subtotal_exento, subtotal_5, subtotal_10, iva_5, iva_10, total, saldo_pendiente, id_estado_factura, observaciones, fecha_creacion, id_funcionario) FROM stdin;
1	23	3	1	001	001	0000001	17232267	345672	CLAUDIA MUÑOZ	2026-06-22	Contado	\N	0.00	0.00	150000.00	0.00	13636.36	150000.00	0.00	3		2026-06-22 12:08:52.059218	\N
2	25	5	1	001	001	0000002	17232267	34567219	APARICIA VERA	2026-07-19	Contado	\N	0.00	0.00	150000.00	0.00	13636.36	150000.00	0.00	3		2026-07-19 14:48:51.962609	\N
3	27	7	1	001	001	0000003	17232267	5678349	LUCAS COLARTE	2026-09-06	Contado	\N	0.00	0.00	150000.00	0.00	13636.36	150000.00	0.00	3		2026-09-06 13:15:09.374956	\N
4	30	7	1	001	001	0000004	17232267	345672	CLAUDIA MUÑOZ	2026-09-06	Contado	\N	0.00	0.00	220000.00	0.00	20000.00	220000.00	0.00	3		2026-09-06 20:53:55.479942	\N
5	33	8	1	001	001	0000005	17232267	34567219	APARICIA VERA	2026-09-07	Contado	\N	0.00	0.00	370000.00	0.00	33636.36	370000.00	0.00	3		2026-09-07 18:54:42.382327	\N
7	39	9	1	001	001	0000006	17232267	5678349	LUCAS COLARTE	2026-10-15	Contado	\N	0.00	0.00	370000.00	0.00	33636.36	370000.00	0.00	3		2026-10-15 20:54:40.517694	\N
8	41	9	1	001	001	0000007	17232267	654327	SANTI VERA	2026-10-18	Contado	\N	0.00	60000.00	150000.00	2857.14	13636.36	210000.00	0.00	3		2026-10-18 10:53:59.072764	\N
\.


--
-- Data for Name: ficha_antecedentes_familiares; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ficha_antecedentes_familiares (id_antecedente_familiar, id_ficha, enfermedad, parentesco) FROM stdin;
1	6	Diabetes	padre
2	20	Diabetes	\N
3	20	Hipertensión (HTA)	\N
4	20	Psoriasis	\N
\.


--
-- Data for Name: ficha_medica; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ficha_medica (id_ficha, id_paciente, id_grupo_sanguineo, peso_habitual, talla, enfermedades_cronicas, antecedentes_quirurgicos, antecedentes_familiares, medicacion_habitual, tabaquismo, alcoholismo, actividad_fisica, detalle_habitos, observaciones, fecha_creacion, fecha_actualizacion, ocupacion, numero_calzado, toma_medicamento, alergia_medicamento, padece_diabetes, padece_hta, padece_artritis, padece_artrosis, padece_osteoporosis, padece_otro, fam_diabetes, fam_diabetes_esp, fam_hta, fam_hta_esp, fam_psoriasis, fam_psoriasis_esp) FROM stdin;
6	18	2	\N	\N			\N		f	f	f			2026-06-15 19:49:40.537548	2026-09-06 20:50:12.881105	contadora	36	f	t	f	f	f	f	f	hipotiroidismo	t	padre	f		f	
13	19	\N	\N	\N			\N		f	f	f			2026-09-06 13:05:35.039501	2026-09-06 21:11:33.070163			f	f	f	f	f	f	f		f		f		f	
8	17	6	\N	\N			\N		f	f	f			2026-06-21 19:21:26.766441	2026-09-07 18:32:44.085014			f	f	f	f	f	f	f		f		f		f	
12	16	1	\N	\N			\N		f	f	f			2026-07-19 14:45:51.853172	2026-09-07 18:50:04.027918	contadora	36	f	f	f	f	f	f	f		f		f		f	
20	20	2	\N	\N			\N		f	f	f			2026-09-29 11:45:17.87975	2026-09-29 11:45:17.87975	SIN	36	f	f	t	t	f	f	f		t		t		t	
\.


--
-- Data for Name: ficha_medicacion_habitual; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ficha_medicacion_habitual (id_ficha_medicacion, id_ficha, id_medicamento, descripcion) FROM stdin;
\.


--
-- Data for Name: formas_cobro; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.formas_cobro (id_forma_cobro, descripcion, requiere_referencia) FROM stdin;
1	Efectivo	f
2	Cheque	t
3	Tarjeta de Crédito	t
4	Tarjeta de Débito	t
\.


--
-- Data for Name: funcionarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.funcionarios (id_funcionario, id_persona, id_usuario, id_consultorio, id_rol, cargo, fecha_ingreso, estado) FROM stdin;
2	1	2	2	1	ADMINISTRADOR GENERAL DEL SISTEMA	2026-10-18	t
3	26	8	2	3	PODOLOGO	2026-10-21	t
4	25	6	2	2	\N	2026-10-21	t
5	24	7	2	4	\N	2026-10-21	t
\.


--
-- Data for Name: generos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.generos (id_genero, descripcion) FROM stdin;
1	MACULINO
2	FEMENINO
\.


--
-- Data for Name: grupos_sanguineos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.grupos_sanguineos (id_grupo_sanguineo, descripcion) FROM stdin;
1	A+
2	A-
3	B+
4	B-
5	AB+
6	AB-
7	O+
8	O-
\.


--
-- Data for Name: insumos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.insumos (id_insumo, nombre, descripcion, unidad_medida, estado, precio_venta, id_tipo_iva, stock_actual, stock_minimo) FROM stdin;
3	Jeringa 10 ml	Jeringa descartable con aguja	Unidad	t	10000.00	2	11.00	0.00
2	Jeringa 5 ml	Jeringa descartable con aguja	Unidad	t	50000.00	2	29.00	0.00
5	Alcohol 70°	Alcohol etílico al 70%	Ml	t	10000.00	2	10.00	1.00
7	Venda elástica	Venda elástica 10 cm x 4,5 m	Unidad	t	0.00	\N	15.00	0.00
1	Guantes de látex	Guantes descartables de exploración	Par	t	0.00	\N	199.00	0.00
10	Tiras reactivas glucemia	Tiras para glucómetro	Unidad	t	50000.00	2	19.00	0.00
4	Algodón	Torundas de algodón estéril	Gramo	t	5000.00	1	47.00	0.00
6	Gasa estéril	Apósito de gasa estéril 10x10 cm	Unidad	t	0.00	\N	14.00	0.00
8	Esparadrapo	Cinta adhesiva médica hipoalergénica	Metro	t	15000.00	2	1.00	0.00
9	Tapaboca	Mascarilla descartable 3 capas	Unidad	t	0.00	\N	25.00	0.00
\.


--
-- Data for Name: justificativos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.justificativos (id_justificativo, id_consulta, fecha_emision, motivo, dias_reposo, fecha_desde, fecha_hasta, observaciones) FROM stdin;
4	38	2026-10-13	CHEQUEO	13	2026-10-13	2026-10-14	
\.


--
-- Data for Name: medicamentos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.medicamentos (id_medicamento, nombre, principio_activo, presentacion, concentracion, via_administracion, estado) FROM stdin;
1	Paracetamol	Paracetamol	Comprimido	500 mg	Oral	t
2	Ibuprofeno	Ibuprofeno	Comprimido	400 mg	Oral	t
3	Amoxicilina	Amoxicilina	Cápsula	500 mg	Oral	t
4	Azitromicina	Azitromicina	Comprimido	500 mg	Oral	t
5	Omeprazol	Omeprazol	Cápsula	20 mg	Oral	t
6	Loratadina	Loratadina	Comprimido	10 mg	Oral	t
7	Metformina	Metformina	Comprimido	850 mg	Oral	t
8	Losartán	Losartán	Comprimido	50 mg	Oral	t
9	Ciprofloxacino	Ciprofloxacino	Comprimido	500 mg	Oral	t
10	Diclofenaco	Diclofenaco sódico	Ampolla	75 mg/3 ml	Intramuscular	t
11	Ranitidina	Ranitidina	Comprimido	150 mg	Oral	t
12	Betametasona	Betametasona	Crema	0,1%	Tópica	t
13	Suero fisiológico	Cloruro de sodio	Solución	0,9% x 250 ml	Intravenosa	t
14	Metoclopramida	Metoclopramida	Comprimido	10 mg	Oral	t
15	Dexametasona	Dexametasona	Ampolla	4 mg/ml	Intramuscular	t
\.


--
-- Data for Name: medicos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.medicos (id_medico, id_persona, matricula) FROM stdin;
12	11	8755847F
16	18	666HHR93
17	6	JGK096JS
18	16	123456V4
\.


--
-- Data for Name: motivos_nota; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.motivos_nota (id_motivo_nota, descripcion, id_tipo_comprobante) FROM stdin;
1	Devolución / Anulación de factura	2
2	Descuento posterior a la facturación	2
3	Error en el monto facturado (a favor del cliente)	2
4	Recargo por mora	3
5	Ajuste de saldo a favor del consultorio	3
\.


--
-- Data for Name: notas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notas (id_nota, id_tipo_comprobante, id_factura, id_motivo_nota, establecimiento, punto_expedicion, numero_nota, timbrado, fecha_emision, monto, detalle_motivo, id_usuario, fecha_creacion) FROM stdin;
1	3	3	4	001	001	0000001	17232267	2026-09-06	150000.00		2	2026-09-06 13:16:07.644498
\.


--
-- Data for Name: orden_analisis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.orden_analisis (id_orden_analisis, id_tipo_orden_analisis, fecha_emision, observacion, estado, id_consulta) FROM stdin;
1	3	2025-10-12	Perfil lipídico completo - Control de colesterol	pendiente	\N
2	4	2025-10-13	Función renal (urea y creatinina) - Control post-tratamiento	pendiente	\N
3	5	2025-10-14	Función hepática - Evaluación de enzimas	pendiente	\N
4	1	2025-10-10	Hemograma completo - Control de anemia	pendiente	\N
5	2	2025-10-11	Glucemia en ayunas - Evaluación de diabetes	pendiente	\N
6	5	2025-10-14	Función hepática - Evaluación de enzimas	pendiente	\N
7	4	2025-10-13	Función renal (urea y creatinina) - Control post-tratamiento	pendiente	\N
8	3	2025-10-12	Perfil lipídico completo - Control de colesterol	pendiente	\N
\.


--
-- Data for Name: orden_estudio; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.orden_estudio (id_orden_estudio, id_tipo_orden_estudio, fecha_emision, observacion, estado, id_consulta) FROM stdin;
1	1	2025-10-10	Radiografía de tórax - Control post-operatorio	pendiente	\N
2	2	2025-10-12	Tomografía de abdomen - Sospecha de cálculos renales	pendiente	\N
3	3	2025-10-13	Resonancia de columna lumbar - Dolor crónico	pendiente	\N
4	4	2025-10-14	Ecografía abdominal completa - Control de rutina	pendiente	\N
5	5	2025-10-15	Electrocardiograma - Evaluación preoperatoria	pendiente	\N
\.


--
-- Data for Name: pacientes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pacientes (id_paciente, id_persona, fecha_nacimiento, peso, altura) FROM stdin;
16	11	2009-02-11	\N	\N
17	16	2008-05-15	\N	\N
18	19	1989-02-15	\N	\N
19	20	2004-10-31	\N	\N
20	21	2025-08-19	\N	\N
21	22	2003-09-23	\N	\N
22	23	2017-05-28	\N	\N
\.


--
-- Data for Name: permisos_rol; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.permisos_rol (id_rol, modulo, puede_modificar) FROM stdin;
3	consulta	t
3	disponibilidad	f
3	agenda	f
4	insumos	t
4	facturacion	t
2	agenda	t
2	avisos	t
2	citas	t
2	disponibilidad	t
2	pacientes	t
2	personas	t
\.


--
-- Data for Name: personas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.personas (id_persona, nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad, gmail) FROM stdin;
1	INGRID DAHIANA	ENRIQUEZ DOS SANTOS	5681041	2	3	0992394123	1	\N
4	ARAMI	GONZALEZ	598775	2	3	0983343508	2	\N
2	SIVIA 	BARRETO	6987456	2	1	0972134567	1	\N
6	KEYLA	F	5	2	3	98977766	2	\N
9	LU	ENRI	444	2	1	3333	3	\N
10	SANDRA	DOS SANTOS	4356782	2	1	09453134	1	\N
12	MARISA	DOS SANTOS	675428	2	1	0991223679	1	\N
13	ARANTXA ITZEL	ROGER ENRIQUEZ	654789	2	2	09743567	2	\N
15	MARIA MERCEDES	MARTINEZ	5789467	2	3	098756475	1	\N
16	CAMILA	CARDOZO	5674983	2	1	09634562	2	camila54@.com
11	APARICIA	VERA	34567219	2	1	098754216	3	aparicia22@.com
17	TAMARA	VERA	543267	2	1	09754325	1	11111@.com
18	FELIPE	CARDOZO	5678349	1	1	09874312	1	felipe36a.com
19	CLAUDIA	MUÑOZ	345672	2	1	0972985793	3	calaudiaQmail.com
20	LUCAS	COLARTE	5678349	1	2	09874312	3	felipe36a.com
21	SANTI	VERA	654327	1	2	0981765432	2	santi.vera.com.py
22	ROJO	VERDE	6681041	1	1	0972985793	1	rojo.verde.com.py
23	LUCIANO	DOS SANTOS	6743215	1	2	0972985793	2	luc.ano.com.py
24	LILI	LOPEZ	8765325	2	1	0972985793	1	lila.com.py
25	NORMA	CAÑETE	454356	2	3	0972985798	3	norma.com.py
26	PEDRO	OTAZU	8765334	1	3	095432165	1	pedro.com.py
\.


--
-- Data for Name: receta_detalle; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.receta_detalle (id_receta_detalle, id_receta, id_medicamento, dosis, frecuencia, duracion, indicaciones, cantidad) FROM stdin;
14	9	8	1	3	4		10
15	10	10	1 comp	8hs	7 días		1
16	11	3	6	12	6		1
17	12	2	6	12	6		1
18	13	1	6	5	6		1
19	14	8	12	3	4		1
20	15	1	12	3	4		1
23	17	14	12	1	4		12
24	17	9	4	1	4		4
25	18	3	4	4	43		23
\.


--
-- Data for Name: recetas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.recetas (id_receta, id_consulta, fecha_emision, observaciones) FROM stdin;
9	25	2026-07-19	
10	27	2026-09-06	
11	28	2026-09-06	
12	30	2026-09-06	
13	31	2026-09-06	
14	32	2026-09-07	
15	33	2026-09-07	
17	38	2026-10-13	
18	39	2026-10-15	
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (id_rol, descripcion) FROM stdin;
1	Administrador
2	Recepcionista
3	Profesional
4	Cajero
\.


--
-- Data for Name: sala_atenciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sala_atenciones (id_sala_atencion, nombre) FROM stdin;
1	B2
2	A1
\.


--
-- Data for Name: servicios_facturables; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.servicios_facturables (id_servicio, descripcion, precio_unitario, id_tipo_iva, estado) FROM stdin;
1	Consulta Podológica General	150000.00	1	t
2	Tratamiento de Onicomicosis	200000.00	1	t
3	Curación / Cuidado de Pie Diabético	180000.00	1	t
4	Corrección de Uña Encarnada	220000.00	1	t
\.


--
-- Data for Name: signos_vitales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.signos_vitales (id_signos_vitales, id_consulta, peso, talla, presion_sistolica, presion_diastolica, temperatura, frecuencia_cardiaca, frecuencia_resp, saturacion_oxigeno, glucemia, observaciones, pulso_pedio_izq, pulso_pedio_der, pulso_tibial_izq, pulso_tibial_der, temperatura_pie) FROM stdin;
10	23	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N
12	25	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N
13	27	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	-	-	\N
14	28	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N
16	30	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N
17	31	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N
18	32	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N
19	33	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N
\.


--
-- Data for Name: stock_insumos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.stock_insumos (id_movimiento, id_insumo, tipo_movimiento, cantidad, stock_anterior, stock_nuevo, motivo, id_consulta, id_usuario, fecha_movimiento) FROM stdin;
1	6	SALIDA	1.00	0.00	-1.00	Consulta #25	25	2	2026-07-19 14:47:35.819532
2	3	SALIDA	1.00	0.00	-1.00	Consulta #25	25	2	2026-07-19 14:47:35.819532
3	5	SALIDA	1.00	0.00	-1.00	Consulta #27	27	2	2026-09-06 13:08:34.444965
4	4	SALIDA	2.00	0.00	-2.00	Consulta #27	27	2	2026-09-06 13:08:34.444965
5	9	SALIDA	1.00	0.00	-1.00	Consulta #27	27	2	2026-09-06 13:08:34.444965
6	5	SALIDA	1.00	-1.00	-2.00	Consulta #28	28	\N	2026-09-06 14:30:36.351296
7	4	SALIDA	1.00	-2.00	-3.00	Consulta #28	28	\N	2026-09-06 14:30:36.351296
8	9	SALIDA	1.00	-1.00	-2.00	Consulta #28	28	\N	2026-09-06 14:30:36.351296
9	7	SALIDA	1.00	0.00	-1.00	Consulta #28	28	\N	2026-09-06 14:30:36.351296
10	5	SALIDA	1.00	-2.00	-3.00	Consulta #30	30	2	2026-09-06 20:52:21.541647
11	4	SALIDA	1.00	-3.00	-4.00	Consulta #30	30	2	2026-09-06 20:52:21.541647
12	6	SALIDA	1.00	-1.00	-2.00	Consulta #30	30	2	2026-09-06 20:52:21.541647
13	7	SALIDA	1.00	-1.00	-2.00	Consulta #30	30	2	2026-09-06 20:52:21.541647
14	9	SALIDA	1.00	-2.00	-3.00	Consulta #31	31	2	2026-09-06 21:13:10.020536
15	6	SALIDA	1.00	-2.00	-3.00	Consulta #31	31	2	2026-09-06 21:13:10.020536
16	5	SALIDA	1.00	-3.00	-4.00	Consulta #31	31	2	2026-09-06 21:13:10.020536
17	9	SALIDA	1.00	-3.00	-4.00	Consulta #32	32	2	2026-09-07 18:34:09.822428
18	5	SALIDA	1.00	-4.00	-5.00	Consulta #32	32	2	2026-09-07 18:34:09.822428
19	5	SALIDA	1.00	-5.00	-6.00	Consulta #33	33	2	2026-09-07 18:53:01.99803
20	9	SALIDA	1.00	-4.00	-5.00	Consulta #33	33	2	2026-09-07 18:53:01.99803
24	6	ENTRADA	1.00	-4.00	-3.00	Reposición por eliminación de consulta #36	\N	2	2026-09-29 19:16:10.071821
25	9	ENTRADA	1.00	-6.00	-5.00	Reposición por eliminación de consulta #36	\N	2	2026-09-29 19:16:10.071821
26	5	ENTRADA	1.00	-7.00	-6.00	Reposición por eliminación de consulta #36	\N	2	2026-09-29 19:16:10.071821
21	6	SALIDA	1.00	-3.00	-4.00	Consulta #36	\N	2	2026-09-29 11:50:54.190771
22	9	SALIDA	1.00	-5.00	-6.00	Consulta #36	\N	2	2026-09-29 11:50:54.190771
23	5	SALIDA	1.00	-6.00	-7.00	Consulta #36	\N	2	2026-09-29 11:50:54.190771
27	4	ENTRADA	1.00	-4.00	-3.00	Reposición por eliminación de consulta #24	\N	2	2026-10-13 21:56:48.568789
28	8	ENTRADA	1.00	0.00	1.00	Reposición por eliminación de consulta #24	\N	2	2026-10-13 21:56:48.568789
34	5	SALIDA	1.00	-6.00	-7.00	Consulta #39	39	2	2026-10-15 20:49:57.132128
35	6	SALIDA	3.00	-3.00	-6.00	Consulta #39	39	2	2026-10-15 20:49:57.132128
36	7	SALIDA	2.00	-2.00	-4.00	Consulta #39	39	2	2026-10-15 20:49:57.132128
40	4	ENTRADA	1.00	-4.00	-3.00	Reposición por eliminación de consulta #40	\N	2	2026-10-18 10:40:12.704853
41	7	ENTRADA	1.00	-5.00	-4.00	Reposición por eliminación de consulta #40	\N	2	2026-10-18 10:40:12.704853
42	5	ENTRADA	1.00	-8.00	-7.00	Reposición por eliminación de consulta #40	\N	2	2026-10-18 10:40:12.704853
37	4	SALIDA	1.00	-3.00	-4.00	Consulta #40	\N	2	2026-10-18 10:37:12.420631
38	7	SALIDA	1.00	-4.00	-5.00	Consulta #40	\N	2	2026-10-18 10:37:12.420631
39	5	SALIDA	1.00	-7.00	-8.00	Consulta #40	\N	2	2026-10-18 10:37:12.420631
43	5	ENTRADA	18.00	-7.00	11.00	Reposición	\N	2	2026-10-18 10:42:49.668129
44	4	ENTRADA	50.00	-3.00	47.00	Reposición	\N	2	2026-10-18 10:43:02.228069
45	6	ENTRADA	20.00	-6.00	14.00	Reposición	\N	2	2026-10-18 10:43:10.611707
46	9	ENTRADA	30.00	-5.00	25.00	Reposición	\N	2	2026-10-18 10:44:46.920593
47	7	ENTRADA	20.00	-4.00	16.00	Reposición	\N	2	2026-10-18 10:45:44.452424
48	10	ENTRADA	20.00	0.00	20.00	Reposición	\N	2	2026-10-18 10:46:22.665605
49	1	ENTRADA	200.00	0.00	200.00	Reposición	\N	2	2026-10-18 10:47:36.449318
50	3	ENTRADA	12.00	-1.00	11.00	Reposición	\N	2	2026-10-18 10:48:34.663804
51	2	ENTRADA	29.00	0.00	29.00	Reposición	\N	2	2026-10-18 10:49:05.123967
52	5	SALIDA	1.00	11.00	10.00	Consulta #41	41	2	2026-10-18 10:51:56.306028
53	7	SALIDA	1.00	16.00	15.00	Consulta #41	41	2	2026-10-18 10:51:56.306028
54	1	SALIDA	1.00	200.00	199.00	Consulta #41	41	2	2026-10-18 10:51:56.306028
55	10	SALIDA	1.00	20.00	19.00	Consulta #41	41	2	2026-10-18 10:51:56.306028
\.


--
-- Data for Name: tipo_orden_analisis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipo_orden_analisis (id_tipo_orden_analisis, descripcion, estado) FROM stdin;
1	Hemograma Completo	t
2	Glucemia	t
3	Perfil Lipídico	t
4	Función Renal	t
5	Función Hepática	t
6	Orina Completa	t
7	Heces	t
8	Perfil Tiroideo	t
9	Hemoglobina Glicosilada	t
10	Cultivo	t
11	Perfil Hormonal	t
12	Ninguno	t
\.


--
-- Data for Name: tipo_orden_estudio; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipo_orden_estudio (id_tipo_orden_estudio, descripcion, estado) FROM stdin;
1	Radiografía	t
2	Tomografía	t
3	Resonancia Magnética	t
4	Ecografía	t
5	Electrocardiograma	t
6	Endoscopía	t
7	Mamografía	t
8	Colonoscopía	t
9	Densitometría Ósea	t
10	Ninguno	t
\.


--
-- Data for Name: tipos_alergia; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipos_alergia (id_tipo_alergia, descripcion, estado) FROM stdin;
1	Medicamentos	t
2	Alimentos	t
3	Polen / Ambiental	t
4	Látex	t
5	Picadura de insectos	t
6	Productos químicos	t
7	Otras	t
\.


--
-- Data for Name: tipos_comprobante; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipos_comprobante (id_tipo_comprobante, descripcion, prefijo) FROM stdin;
1	Factura	FAC
2	Nota de Crédito	NCR
3	Nota de Débito	NDB
\.


--
-- Data for Name: tipos_iva; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipos_iva (id_tipo_iva, descripcion, porcentaje) FROM stdin;
1	IVA 10%	10.00
2	IVA 5%	5.00
3	Exento	0.00
\.


--
-- Data for Name: tratamientos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tratamientos (id_tratamiento, id_enfermedad, descripcion, indicaciones, estado) FROM stdin;
1	1	Reposo + Hidratación + Analgésicos	Reposo relativo, abundante líquido, control de temperatura	t
2	2	Antibioticoterapia + Oxigenoterapia	Hospitalización según gravedad, control de saturación	t
3	3	Control glucémico + Dieta + Antidiabéticos orales	Monitoreo de glucosa en ayunas, actividad física moderada	t
4	4	Antihipertensivos + Reducción de sal	Control de presión arterial diario, dieta hiposódica	t
5	5	Antiácidos + Dieta blanda + Inhibidores de bomba de protones	Evitar picantes y alcohol, fraccionamiento de comidas	t
6	6	Analgésicos + Relajantes musculares + Fisioterapia	Reposo relativo, fisioterapia 3 veces por semana	t
7	7	Antihistamínicos + Lavados nasales	Evitar alérgenos, uso de antihistamínico según indicación	t
8	8	Corticoides tópicos + Antihistamínicos	Identificar y evitar el agente causante	t
9	9	Antibioticoterapia + Hidratación	Abundante líquido, completar ciclo antibiótico	t
10	10	Analgésicos + Hidratación + Reposo	Descanso en ambiente tranquilo, analgesia según intensidad	t
11	11	Corrección ortésica + descarga de presión	Uso de plantillas ortopédicas, separador interdigital, calzado amplio en la zona del antepié	t
12	12	Almohadillado + corrección digital	Uso de órtesis de silicona, calzado con puntera amplia	t
13	13	Evaluación biomecánica + plantillas correctivas	Control podológico periódico, estudio de la marcha	t
14	14	Estiramientos + taloneras de descarga + AINEs locales	Reposo relativo, hielo local, ejercicios de estiramiento de la fascia plantar	t
15	15	Taloneras de silicona + fisioterapia	Evitar impacto excesivo, uso de calzado con buena amortiguación	t
16	16	Corrección quirúrgica ungueal ambulatoria	Higiene local, antibiótico tópico si hay signos de infección, control en 7 días	t
17	17	Fresado y reducción de espesor ungueal	Control cada 4-6 semanas, hidratación de la lámina ungueal	t
18	18	Cuidado ungueal + protección de la lámina	Evitar traumatismos, uso de calzado adecuado	t
19	19	Antimicótico tópico/oral + fresado	Tratamiento prolongado (varios meses), mantener pie seco y ventilado	t
20	20	Deslaminación + descarga local	Uso de plantillas de descarga, hidratación diaria de la piel	t
21	21	Curación local + apósito + control evolutivo	Limpieza diaria, cambio de apósito, vigilar signos de infección	t
22	22	Plantillas ortopédicas correctivas	Seguimiento por especialista, ejercicios de fortalecimiento del arco	t
23	23	Plantillas de descarga + calzado adaptado	Evaluación postural, control periódico	t
24	24	Evaluación vascular + cuidado preventivo del pie	Control de pulsos periódico, evitar lesiones, derivar a especialista vascular si empeora	t
25	25	Cuidado podológico preventivo del pie diabético	Inspección diaria del pie, control glucémico estricto, calzado especializado, evitar caminar descalzo	t
\.


--
-- Data for Name: turnos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.turnos (id_turno, descripcion) FROM stdin;
1	TARDE
2	MAÑANA
3	NOCHE
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (id_usuario, nickname, clave, estado, id_rol, totp_secreto, totp_activo, totp_ultimo_paso) FROM stdin;
3	SILVI	scrypt:32768:8:1$8RU470k6PZ7damQG$801e6951b29d9050ecfc81fa0e50b814e976579437fff261c008878249965c16b3c8762c12194fb70ed22c49fe1db67a3b6e3ccdf3658c435fa82fab4717ad52	t	1	\N	f	\N
5	ADMINISTRADOR	scrypt:32768:8:1$H4m5s4ASi7qqmpqB$5175fbebae2beeb6e7c9a0d8435c23b046e850905948070ae02ad733f24b4039e2e33334cc6e02d26a413867403cfabe4da0153a456fb37496294ec209946467	t	1	\N	f	\N
8	PROFECIONAL PEDRO	scrypt:32768:8:1$WARa1FQgT2aX0Wjc$c9754006b82861ba0c663518810a8f2cfb76386d7e6089430c88c7f7146dec8231dc4f7c9111c378be1994f3e528a3005513f9698fad861f1224656494da3c69	t	3	\N	f	\N
6	RECEPCIONISTA NORMA	scrypt:32768:8:1$PzhC23UUWjACY48E$418e618fff648a87f5d4e6a79370183455d01085e2ee62db5d489c88b540cf5ef7a969533bf1a6e47ac518ac097621d479dc523e1e82f8ffa1af5ecd1a4fb5c2	t	2	\N	f	\N
7	CAJERA LILA	scrypt:32768:8:1$GUJ2c9qTrztYYdVR$ed77d22d22008d19ac8600127f4d66278c03d516ea9054e58e173b244bd6b7b6173990afd7de43d8e3efeb44cdb38bfd4486f75589f02d15a6e1bc5e2c9c6f36	t	4	\N	f	\N
2	INGRID	scrypt:32768:8:1$hJSx6gXyzeT1SSUe$d7d1cfb918936a050f47d7f4c111b95c783404642e05a06fd93d32a2c9b947e45ccba3ee9b46fc5108535adbd66d1200058925aeb74b3fc7f50994728e2c24b3	t	1	7AQ4YJHINLCKU7MZU6SQQDZHSLXDM5B7	t	59754286
\.


--
-- Name: agenda_medicas_id_agenda_medica_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.agenda_medicas_id_agenda_medica_seq', 38, true);


--
-- Name: alergias_paciente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.alergias_paciente_id_seq', 4, true);


--
-- Name: anamnesis_podologica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.anamnesis_podologica_id_seq', 18, true);


--
-- Name: auditoria_accesos_id_auditoria_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auditoria_accesos_id_auditoria_seq', 59, true);


--
-- Name: avisos_recordatorios_id_aviso_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.avisos_recordatorios_id_aviso_seq', 26, true);


--
-- Name: cajas_id_caja_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cajas_id_caja_seq', 9, true);


--
-- Name: citas_id_cita_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.citas_id_cita_seq', 46, true);


--
-- Name: ciudades_id_ciudad_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ciudades_id_ciudad_seq', 3, true);


--
-- Name: cobranzas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cobranzas_id_seq', 9, true);


--
-- Name: consulta_diagnosticos_id_consulta_diagnostico_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consulta_diagnosticos_id_consulta_diagnostico_seq', 12, true);


--
-- Name: consulta_insumos_id_consulta_insumo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consulta_insumos_id_consulta_insumo_seq', 65, true);


--
-- Name: consulta_ordenes_id_consulta_orden_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consulta_ordenes_id_consulta_orden_seq', 42, true);


--
-- Name: consulta_procedimientos_id_consulta_procedimiento_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consulta_procedimientos_id_consulta_procedimiento_seq', 19, true);


--
-- Name: consultas_id_consulta_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consultas_id_consulta_seq', 42, true);


--
-- Name: consultorio_id_consultorio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consultorio_id_consultorio_seq', 2, true);


--
-- Name: datos_emisor_id_emisor_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.datos_emisor_id_emisor_seq', 1, true);


--
-- Name: dias_id_dia_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.dias_id_dia_seq', 19, true);


--
-- Name: disponibilidad_horaria_id_disponibilidad_horaria_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.disponibilidad_horaria_id_disponibilidad_horaria_seq', 1012, true);


--
-- Name: enfermedades_id_enfermedad_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enfermedades_id_enfermedad_seq', 25, true);


--
-- Name: especialidades_id_especialidad_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.especialidades_id_especialidad_seq', 5, true);


--
-- Name: estado_citas_id_estado_cita_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.estado_citas_id_estado_cita_seq', 5, true);


--
-- Name: estado_civiles_id_estado_civil_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.estado_civiles_id_estado_civil_seq', 3, true);


--
-- Name: estado_laborales_id_estado_laboral_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.estado_laborales_id_estado_laboral_seq', 2, true);


--
-- Name: estados_factura_id_estado_factura_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.estados_factura_id_estado_factura_seq', 4, true);


--
-- Name: factura_detalle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.factura_detalle_id_seq', 13, true);


--
-- Name: facturas_id_factura_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facturas_id_factura_seq', 8, true);


--
-- Name: ficha_antecedentes_familiares_id_antecedente_familiar_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ficha_antecedentes_familiares_id_antecedente_familiar_seq', 4, true);


--
-- Name: ficha_medica_id_ficha_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ficha_medica_id_ficha_seq', 20, true);


--
-- Name: ficha_medicacion_habitual_id_ficha_medicacion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ficha_medicacion_habitual_id_ficha_medicacion_seq', 1, false);


--
-- Name: formas_cobro_id_forma_cobro_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.formas_cobro_id_forma_cobro_seq', 4, true);


--
-- Name: funcionarios_id_funcionario_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.funcionarios_id_funcionario_seq', 5, true);


--
-- Name: generos_id_genero_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.generos_id_genero_seq', 2, true);


--
-- Name: grupos_sanguineos_id_grupo_sanguineo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.grupos_sanguineos_id_grupo_sanguineo_seq', 8, true);


--
-- Name: insumos_id_insumo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.insumos_id_insumo_seq', 11, true);


--
-- Name: justificativos_id_justificativo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.justificativos_id_justificativo_seq', 4, true);


--
-- Name: medicamentos_id_medicamento_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.medicamentos_id_medicamento_seq', 15, true);


--
-- Name: medicos_id_medico_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.medicos_id_medico_seq', 18, true);


--
-- Name: motivos_nota_id_motivo_nota_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.motivos_nota_id_motivo_nota_seq', 5, true);


--
-- Name: notas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notas_id_seq', 1, true);


--
-- Name: orden_analisis_id_orden_analisis_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.orden_analisis_id_orden_analisis_seq', 8, true);


--
-- Name: orden_estudio_id_orden_estudio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.orden_estudio_id_orden_estudio_seq', 5, true);


--
-- Name: pacientes_id_paciente_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pacientes_id_paciente_seq', 22, true);


--
-- Name: personas_id_persona_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.personas_id_persona_seq', 26, true);


--
-- Name: receta_detalle_id_receta_detalle_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.receta_detalle_id_receta_detalle_seq', 26, true);


--
-- Name: recetas_id_receta_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.recetas_id_receta_seq', 19, true);


--
-- Name: roles_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.roles_id_rol_seq', 4, true);


--
-- Name: sala_atenciones_id_sala_atencion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sala_atenciones_id_sala_atencion_seq', 2, true);


--
-- Name: servicios_facturables_id_servicio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.servicios_facturables_id_servicio_seq', 4, true);


--
-- Name: signos_vitales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.signos_vitales_id_seq', 21, true);


--
-- Name: stock_insumos_id_movimiento_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.stock_insumos_id_movimiento_seq', 55, true);


--
-- Name: tipo_orden_analisis_id_tipo_orden_analisis_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipo_orden_analisis_id_tipo_orden_analisis_seq', 12, true);


--
-- Name: tipo_orden_estudio_id_tipo_orden_estudio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipo_orden_estudio_id_tipo_orden_estudio_seq', 10, true);


--
-- Name: tipos_alergia_id_tipo_alergia_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipos_alergia_id_tipo_alergia_seq', 7, true);


--
-- Name: tipos_comprobante_id_tipo_comprobante_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipos_comprobante_id_tipo_comprobante_seq', 3, true);


--
-- Name: tipos_iva_id_tipo_iva_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipos_iva_id_tipo_iva_seq', 3, true);


--
-- Name: tratamientos_id_tratamiento_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tratamientos_id_tratamiento_seq', 25, true);


--
-- Name: turnos_id_turno_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.turnos_id_turno_seq', 9, true);


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 16, true);


--
-- Name: agenda_medicas agenda_medicas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT agenda_medicas_pkey PRIMARY KEY (id_agenda_medica);


--
-- Name: auditoria_accesos auditoria_accesos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_accesos
    ADD CONSTRAINT auditoria_accesos_pkey PRIMARY KEY (id_auditoria);


--
-- Name: avisos_recordatorios avisos_recordatorios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.avisos_recordatorios
    ADD CONSTRAINT avisos_recordatorios_pkey PRIMARY KEY (id_aviso);


--
-- Name: citas citas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_pkey PRIMARY KEY (id_cita);


--
-- Name: ciudades ciudades_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades
    ADD CONSTRAINT ciudades_descripcion_key UNIQUE (descripcion);


--
-- Name: ciudades ciudades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades
    ADD CONSTRAINT ciudades_pkey PRIMARY KEY (id_ciudad);


--
-- Name: consulta_diagnosticos consulta_diagnosticos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_diagnosticos
    ADD CONSTRAINT consulta_diagnosticos_pkey PRIMARY KEY (id_consulta_diagnostico);


--
-- Name: consulta_ordenes consulta_ordenes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_ordenes
    ADD CONSTRAINT consulta_ordenes_pkey PRIMARY KEY (id_consulta_orden);


--
-- Name: consulta_procedimientos consulta_procedimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_procedimientos
    ADD CONSTRAINT consulta_procedimientos_pkey PRIMARY KEY (id_consulta_procedimiento);


--
-- Name: consultas consultas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_pkey PRIMARY KEY (id_consulta);


--
-- Name: consultorio consultorio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorio
    ADD CONSTRAINT consultorio_pkey PRIMARY KEY (id_consultorio);


--
-- Name: datos_emisor datos_emisor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.datos_emisor
    ADD CONSTRAINT datos_emisor_pkey PRIMARY KEY (id_emisor);


--
-- Name: dias dias_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias
    ADD CONSTRAINT dias_descripcion_key UNIQUE (descripcion);


--
-- Name: dias dias_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias
    ADD CONSTRAINT dias_pkey PRIMARY KEY (id_dia);


--
-- Name: disponibilidad_horaria disponibilidad_horaria_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disponibilidad_horaria
    ADD CONSTRAINT disponibilidad_horaria_pkey PRIMARY KEY (id_disponibilidad_horaria);


--
-- Name: especialidades especialidades_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_descripcion_key UNIQUE (descripcion);


--
-- Name: especialidades especialidades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_pkey PRIMARY KEY (id_especialidad);


--
-- Name: estado_citas estado_citas_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_citas
    ADD CONSTRAINT estado_citas_descripcion_key UNIQUE (descripcion);


--
-- Name: estado_citas estado_citas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_citas
    ADD CONSTRAINT estado_citas_pkey PRIMARY KEY (id_estado_cita);


--
-- Name: estado_civiles estado_civiles_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_civiles
    ADD CONSTRAINT estado_civiles_descripcion_key UNIQUE (descripcion);


--
-- Name: estado_civiles estado_civiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_civiles
    ADD CONSTRAINT estado_civiles_pkey PRIMARY KEY (id_estado_civil);


--
-- Name: estado_laborales estado_laborales_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_laborales
    ADD CONSTRAINT estado_laborales_descripcion_key UNIQUE (descripcion);


--
-- Name: estado_laborales estado_laborales_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_laborales
    ADD CONSTRAINT estado_laborales_pkey PRIMARY KEY (id_estado_laboral);


--
-- Name: estados_factura estados_factura_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura
    ADD CONSTRAINT estados_factura_descripcion_key UNIQUE (descripcion);


--
-- Name: estados_factura estados_factura_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura
    ADD CONSTRAINT estados_factura_pkey PRIMARY KEY (id_estado_factura);


--
-- Name: ficha_antecedentes_familiares ficha_antecedentes_familiares_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_antecedentes_familiares
    ADD CONSTRAINT ficha_antecedentes_familiares_pkey PRIMARY KEY (id_antecedente_familiar);


--
-- Name: ficha_medicacion_habitual ficha_medicacion_habitual_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medicacion_habitual
    ADD CONSTRAINT ficha_medicacion_habitual_pkey PRIMARY KEY (id_ficha_medicacion);


--
-- Name: formas_cobro formas_cobro_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro
    ADD CONSTRAINT formas_cobro_descripcion_key UNIQUE (descripcion);


--
-- Name: formas_cobro formas_cobro_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro
    ADD CONSTRAINT formas_cobro_pkey PRIMARY KEY (id_forma_cobro);


--
-- Name: funcionarios funcionarios_id_usuario_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_id_usuario_key UNIQUE (id_usuario);


--
-- Name: funcionarios funcionarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_pkey PRIMARY KEY (id_funcionario);


--
-- Name: generos generos_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos
    ADD CONSTRAINT generos_descripcion_key UNIQUE (descripcion);


--
-- Name: generos generos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos
    ADD CONSTRAINT generos_pkey PRIMARY KEY (id_genero);


--
-- Name: grupos_sanguineos grupos_sanguineos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.grupos_sanguineos
    ADD CONSTRAINT grupos_sanguineos_pkey PRIMARY KEY (id_grupo_sanguineo);


--
-- Name: medicos medicos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicos
    ADD CONSTRAINT medicos_pkey PRIMARY KEY (id_medico);


--
-- Name: motivos_nota motivos_nota_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.motivos_nota
    ADD CONSTRAINT motivos_nota_pkey PRIMARY KEY (id_motivo_nota);


--
-- Name: orden_analisis orden_analisis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_analisis
    ADD CONSTRAINT orden_analisis_pkey PRIMARY KEY (id_orden_analisis);


--
-- Name: orden_estudio orden_estudio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_estudio
    ADD CONSTRAINT orden_estudio_pkey PRIMARY KEY (id_orden_estudio);


--
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (id_paciente);


--
-- Name: permisos_rol permisos_rol_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permisos_rol
    ADD CONSTRAINT permisos_rol_pkey PRIMARY KEY (id_rol, modulo);


--
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id_persona);


--
-- Name: alergias_paciente pk_alergias_paciente; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alergias_paciente
    ADD CONSTRAINT pk_alergias_paciente PRIMARY KEY (id_alergia_paciente);


--
-- Name: anamnesis_podologica pk_anamnesis_podologica; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis_podologica
    ADD CONSTRAINT pk_anamnesis_podologica PRIMARY KEY (id_anamnesis);


--
-- Name: cajas pk_cajas; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT pk_cajas PRIMARY KEY (id_caja);


--
-- Name: cobranzas pk_cobranzas; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT pk_cobranzas PRIMARY KEY (id_cobranza);


--
-- Name: consulta_insumos pk_consulta_insumos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_insumos
    ADD CONSTRAINT pk_consulta_insumos PRIMARY KEY (id_consulta_insumo);


--
-- Name: enfermedades pk_enfermedades; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enfermedades
    ADD CONSTRAINT pk_enfermedades PRIMARY KEY (id_enfermedad);


--
-- Name: factura_detalle pk_factura_detalle; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT pk_factura_detalle PRIMARY KEY (id_factura_detalle);


--
-- Name: facturas pk_facturas; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT pk_facturas PRIMARY KEY (id_factura);


--
-- Name: ficha_medica pk_ficha_medica; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medica
    ADD CONSTRAINT pk_ficha_medica PRIMARY KEY (id_ficha);


--
-- Name: insumos pk_insumos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT pk_insumos PRIMARY KEY (id_insumo);


--
-- Name: justificativos pk_justificativos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.justificativos
    ADD CONSTRAINT pk_justificativos PRIMARY KEY (id_justificativo);


--
-- Name: medicamentos pk_medicamentos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicamentos
    ADD CONSTRAINT pk_medicamentos PRIMARY KEY (id_medicamento);


--
-- Name: notas pk_notas; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT pk_notas PRIMARY KEY (id_nota);


--
-- Name: receta_detalle pk_receta_detalle; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT pk_receta_detalle PRIMARY KEY (id_receta_detalle);


--
-- Name: recetas pk_recetas; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT pk_recetas PRIMARY KEY (id_receta);


--
-- Name: signos_vitales pk_signos_vitales; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales
    ADD CONSTRAINT pk_signos_vitales PRIMARY KEY (id_signos_vitales);


--
-- Name: tratamientos pk_tratamientos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT pk_tratamientos PRIMARY KEY (id_tratamiento);


--
-- Name: roles roles_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_descripcion_key UNIQUE (descripcion);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_rol);


--
-- Name: sala_atenciones sala_atenciones_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sala_atenciones
    ADD CONSTRAINT sala_atenciones_nombre_key UNIQUE (nombre);


--
-- Name: sala_atenciones sala_atenciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sala_atenciones
    ADD CONSTRAINT sala_atenciones_pkey PRIMARY KEY (id_sala_atencion);


--
-- Name: servicios_facturables servicios_facturables_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servicios_facturables
    ADD CONSTRAINT servicios_facturables_pkey PRIMARY KEY (id_servicio);


--
-- Name: stock_insumos stock_insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_insumos
    ADD CONSTRAINT stock_insumos_pkey PRIMARY KEY (id_movimiento);


--
-- Name: tipo_orden_analisis tipo_orden_analisis_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_orden_analisis
    ADD CONSTRAINT tipo_orden_analisis_descripcion_key UNIQUE (descripcion);


--
-- Name: tipo_orden_analisis tipo_orden_analisis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_orden_analisis
    ADD CONSTRAINT tipo_orden_analisis_pkey PRIMARY KEY (id_tipo_orden_analisis);


--
-- Name: tipo_orden_estudio tipo_orden_estudio_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_orden_estudio
    ADD CONSTRAINT tipo_orden_estudio_descripcion_key UNIQUE (descripcion);


--
-- Name: tipo_orden_estudio tipo_orden_estudio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_orden_estudio
    ADD CONSTRAINT tipo_orden_estudio_pkey PRIMARY KEY (id_tipo_orden_estudio);


--
-- Name: tipos_alergia tipos_alergia_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_alergia
    ADD CONSTRAINT tipos_alergia_pkey PRIMARY KEY (id_tipo_alergia);


--
-- Name: tipos_comprobante tipos_comprobante_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobante
    ADD CONSTRAINT tipos_comprobante_descripcion_key UNIQUE (descripcion);


--
-- Name: tipos_comprobante tipos_comprobante_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobante
    ADD CONSTRAINT tipos_comprobante_pkey PRIMARY KEY (id_tipo_comprobante);


--
-- Name: tipos_iva tipos_iva_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_iva
    ADD CONSTRAINT tipos_iva_descripcion_key UNIQUE (descripcion);


--
-- Name: tipos_iva tipos_iva_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_iva
    ADD CONSTRAINT tipos_iva_pkey PRIMARY KEY (id_tipo_iva);


--
-- Name: turnos turnos_descripcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.turnos
    ADD CONSTRAINT turnos_descripcion_key UNIQUE (descripcion);


--
-- Name: turnos turnos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.turnos
    ADD CONSTRAINT turnos_pkey PRIMARY KEY (id_turno);


--
-- Name: anamnesis_podologica uix_anamnesis_consulta; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis_podologica
    ADD CONSTRAINT uix_anamnesis_consulta UNIQUE (id_consulta);


--
-- Name: facturas uix_factura_consulta; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT uix_factura_consulta UNIQUE (id_consulta);


--
-- Name: facturas uix_factura_numeracion; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT uix_factura_numeracion UNIQUE (establecimiento, punto_expedicion, numero_factura);


--
-- Name: ficha_medica uix_ficha_paciente; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medica
    ADD CONSTRAINT uix_ficha_paciente UNIQUE (id_paciente);


--
-- Name: justificativos uix_justificativos_consulta; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.justificativos
    ADD CONSTRAINT uix_justificativos_consulta UNIQUE (id_consulta);


--
-- Name: notas uix_nota_numeracion; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT uix_nota_numeracion UNIQUE (establecimiento, punto_expedicion, numero_nota, id_tipo_comprobante);


--
-- Name: recetas uix_recetas_consulta; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT uix_recetas_consulta UNIQUE (id_consulta);


--
-- Name: signos_vitales uix_signos_consulta; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales
    ADD CONSTRAINT uix_signos_consulta UNIQUE (id_consulta);


--
-- Name: citas uq_cita; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT uq_cita UNIQUE (id_disponibilidad_horaria);


--
-- Name: consultas uq_consulta_cita; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT uq_consulta_cita UNIQUE (id_cita);


--
-- Name: disponibilidad_horaria uq_disponibilidad; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disponibilidad_horaria
    ADD CONSTRAINT uq_disponibilidad UNIQUE (id_agenda_medica, fecha, hora_inicio, hora_fin);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- Name: idx_cajas_usuario_estado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cajas_usuario_estado ON public.cajas USING btree (id_usuario, estado);


--
-- Name: idx_cobranzas_caja; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cobranzas_caja ON public.cobranzas USING btree (id_caja);


--
-- Name: idx_cobranzas_factura; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cobranzas_factura ON public.cobranzas USING btree (id_factura);


--
-- Name: idx_consulta_diagnosticos_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consulta_diagnosticos_consulta ON public.consulta_diagnosticos USING btree (id_consulta);


--
-- Name: idx_consultas_cita; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consultas_cita ON public.consultas USING btree (id_cita);


--
-- Name: idx_consultas_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consultas_fecha ON public.consultas USING btree (fecha_consulta);


--
-- Name: idx_cord_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cord_consulta ON public.consulta_ordenes USING btree (id_consulta);


--
-- Name: idx_cp_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cp_consulta ON public.consulta_procedimientos USING btree (id_consulta);


--
-- Name: idx_facturas_estado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_facturas_estado ON public.facturas USING btree (id_estado_factura);


--
-- Name: idx_facturas_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_facturas_fecha ON public.facturas USING btree (fecha_emision);


--
-- Name: idx_ficha_antecedentes_ficha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ficha_antecedentes_ficha ON public.ficha_antecedentes_familiares USING btree (id_ficha);


--
-- Name: idx_ficha_medicacion_ficha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ficha_medicacion_ficha ON public.ficha_medicacion_habitual USING btree (id_ficha);


--
-- Name: idx_stock_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_stock_consulta ON public.stock_insumos USING btree (id_consulta);


--
-- Name: idx_stock_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_stock_fecha ON public.stock_insumos USING btree (fecha_movimiento DESC);


--
-- Name: idx_stock_insumo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_stock_insumo ON public.stock_insumos USING btree (id_insumo);


--
-- Name: ix_auditoria_accesos_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_auditoria_accesos_fecha ON public.auditoria_accesos USING btree (fecha);


--
-- Name: uix_consultas_cita; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uix_consultas_cita ON public.consultas USING btree (id_cita);


--
-- Name: agenda_medicas agenda_medicas_id_dia_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT agenda_medicas_id_dia_fkey FOREIGN KEY (id_dia) REFERENCES public.dias(id_dia) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: agenda_medicas agenda_medicas_id_especialidad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT agenda_medicas_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES public.especialidades(id_especialidad) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: agenda_medicas agenda_medicas_id_estado_laboral_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT agenda_medicas_id_estado_laboral_fkey FOREIGN KEY (id_estado_laboral) REFERENCES public.estado_laborales(id_estado_laboral) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: agenda_medicas agenda_medicas_id_medico_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT agenda_medicas_id_medico_fkey FOREIGN KEY (id_medico) REFERENCES public.medicos(id_medico) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: agenda_medicas agenda_medicas_id_sala_atencion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT agenda_medicas_id_sala_atencion_fkey FOREIGN KEY (id_sala_atencion) REFERENCES public.sala_atenciones(id_sala_atencion) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: agenda_medicas agenda_medicas_id_turno_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT agenda_medicas_id_turno_fkey FOREIGN KEY (id_turno) REFERENCES public.turnos(id_turno) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: auditoria_accesos auditoria_accesos_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_accesos
    ADD CONSTRAINT auditoria_accesos_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON DELETE SET NULL;


--
-- Name: avisos_recordatorios avisos_recordatorios_id_cita_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.avisos_recordatorios
    ADD CONSTRAINT avisos_recordatorios_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES public.citas(id_cita);


--
-- Name: avisos_recordatorios avisos_recordatorios_id_funcionario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.avisos_recordatorios
    ADD CONSTRAINT avisos_recordatorios_id_funcionario_fkey FOREIGN KEY (id_funcionario) REFERENCES public.funcionarios(id_funcionario);


--
-- Name: citas citas_id_disponibilidad_horaria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_disponibilidad_horaria_fkey FOREIGN KEY (id_disponibilidad_horaria) REFERENCES public.disponibilidad_horaria(id_disponibilidad_horaria) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: citas citas_id_estado_cita_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_estado_cita_fkey FOREIGN KEY (id_estado_cita) REFERENCES public.estado_citas(id_estado_cita) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: citas citas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: consulta_diagnosticos consulta_diagnosticos_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_diagnosticos
    ADD CONSTRAINT consulta_diagnosticos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE CASCADE;


--
-- Name: consulta_diagnosticos consulta_diagnosticos_id_enfermedad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_diagnosticos
    ADD CONSTRAINT consulta_diagnosticos_id_enfermedad_fkey FOREIGN KEY (id_enfermedad) REFERENCES public.enfermedades(id_enfermedad);


--
-- Name: consulta_diagnosticos consulta_diagnosticos_id_tratamiento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_diagnosticos
    ADD CONSTRAINT consulta_diagnosticos_id_tratamiento_fkey FOREIGN KEY (id_tratamiento) REFERENCES public.tratamientos(id_tratamiento);


--
-- Name: consultas consultas_id_cita_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES public.citas(id_cita) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: consultas consultas_id_tipo_orden_analisis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_id_tipo_orden_analisis_fkey FOREIGN KEY (id_tipo_orden_analisis) REFERENCES public.tipo_orden_analisis(id_tipo_orden_analisis) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: consultas consultas_id_tipo_orden_estudio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_id_tipo_orden_estudio_fkey FOREIGN KEY (id_tipo_orden_estudio) REFERENCES public.tipo_orden_estudio(id_tipo_orden_estudio) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: disponibilidad_horaria disponibilidad_horaria_id_agenda_medica_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disponibilidad_horaria
    ADD CONSTRAINT disponibilidad_horaria_id_agenda_medica_fkey FOREIGN KEY (id_agenda_medica) REFERENCES public.agenda_medicas(id_agenda_medica) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ficha_antecedentes_familiares ficha_antecedentes_familiares_id_ficha_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_antecedentes_familiares
    ADD CONSTRAINT ficha_antecedentes_familiares_id_ficha_fkey FOREIGN KEY (id_ficha) REFERENCES public.ficha_medica(id_ficha) ON DELETE CASCADE;


--
-- Name: ficha_medicacion_habitual ficha_medicacion_habitual_id_ficha_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medicacion_habitual
    ADD CONSTRAINT ficha_medicacion_habitual_id_ficha_fkey FOREIGN KEY (id_ficha) REFERENCES public.ficha_medica(id_ficha) ON DELETE CASCADE;


--
-- Name: ficha_medicacion_habitual ficha_medicacion_habitual_id_medicamento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medicacion_habitual
    ADD CONSTRAINT ficha_medicacion_habitual_id_medicamento_fkey FOREIGN KEY (id_medicamento) REFERENCES public.medicamentos(id_medicamento);


--
-- Name: agenda_medicas fk_agenda_funcionario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_medicas
    ADD CONSTRAINT fk_agenda_funcionario FOREIGN KEY (id_funcionario) REFERENCES public.funcionarios(id_funcionario);


--
-- Name: alergias_paciente fk_alergia_ficha; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alergias_paciente
    ADD CONSTRAINT fk_alergia_ficha FOREIGN KEY (id_ficha) REFERENCES public.ficha_medica(id_ficha);


--
-- Name: alergias_paciente fk_alergia_tipo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alergias_paciente
    ADD CONSTRAINT fk_alergia_tipo FOREIGN KEY (id_tipo_alergia) REFERENCES public.tipos_alergia(id_tipo_alergia);


--
-- Name: anamnesis_podologica fk_anamnesis_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis_podologica
    ADD CONSTRAINT fk_anamnesis_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: cajas fk_caja_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT fk_caja_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: citas fk_cita_funcionario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT fk_cita_funcionario FOREIGN KEY (id_funcionario) REFERENCES public.funcionarios(id_funcionario);


--
-- Name: cobranzas fk_cobranza_caja; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT fk_cobranza_caja FOREIGN KEY (id_caja) REFERENCES public.cajas(id_caja);


--
-- Name: cobranzas fk_cobranza_factura; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT fk_cobranza_factura FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);


--
-- Name: cobranzas fk_cobranza_forma; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT fk_cobranza_forma FOREIGN KEY (id_forma_cobro) REFERENCES public.formas_cobro(id_forma_cobro);


--
-- Name: consultas fk_consulta_consultorio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT fk_consulta_consultorio FOREIGN KEY (id_consultorio) REFERENCES public.consultorio(id_consultorio);


--
-- Name: consultas fk_consulta_funcionario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT fk_consulta_funcionario FOREIGN KEY (id_funcionario) REFERENCES public.funcionarios(id_funcionario);


--
-- Name: consulta_insumos fk_consulta_insumos_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_insumos
    ADD CONSTRAINT fk_consulta_insumos_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: consulta_insumos fk_consulta_insumos_insumo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_insumos
    ADD CONSTRAINT fk_consulta_insumos_insumo FOREIGN KEY (id_insumo) REFERENCES public.insumos(id_insumo);


--
-- Name: consultas fk_consultas_cita; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT fk_consultas_cita FOREIGN KEY (id_cita) REFERENCES public.citas(id_cita);


--
-- Name: consultas fk_consultas_enfermedad; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT fk_consultas_enfermedad FOREIGN KEY (id_enfermedad) REFERENCES public.enfermedades(id_enfermedad);


--
-- Name: consultas fk_consultas_tipo_analisis; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT fk_consultas_tipo_analisis FOREIGN KEY (id_tipo_orden_analisis) REFERENCES public.tipo_orden_analisis(id_tipo_orden_analisis);


--
-- Name: consultas fk_consultas_tipo_estudio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT fk_consultas_tipo_estudio FOREIGN KEY (id_tipo_orden_estudio) REFERENCES public.tipo_orden_estudio(id_tipo_orden_estudio);


--
-- Name: consultas fk_consultas_tratamiento; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT fk_consultas_tratamiento FOREIGN KEY (id_tratamiento) REFERENCES public.tratamientos(id_tratamiento);


--
-- Name: consultorio fk_consultorio_ciudad; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorio
    ADD CONSTRAINT fk_consultorio_ciudad FOREIGN KEY (id_ciudad) REFERENCES public.ciudades(id_ciudad);


--
-- Name: consulta_ordenes fk_cord_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_ordenes
    ADD CONSTRAINT fk_cord_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: consulta_procedimientos fk_cp_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_procedimientos
    ADD CONSTRAINT fk_cp_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: consulta_procedimientos fk_cp_servicio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consulta_procedimientos
    ADD CONSTRAINT fk_cp_servicio FOREIGN KEY (id_servicio) REFERENCES public.servicios_facturables(id_servicio);


--
-- Name: factura_detalle fk_detalle_factura; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT fk_detalle_factura FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);


--
-- Name: factura_detalle fk_detalle_iva; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT fk_detalle_iva FOREIGN KEY (id_tipo_iva) REFERENCES public.tipos_iva(id_tipo_iva);


--
-- Name: factura_detalle fk_detalle_servicio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT fk_detalle_servicio FOREIGN KEY (id_servicio) REFERENCES public.servicios_facturables(id_servicio);


--
-- Name: facturas fk_factura_caja; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT fk_factura_caja FOREIGN KEY (id_caja) REFERENCES public.cajas(id_caja);


--
-- Name: facturas fk_factura_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT fk_factura_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: facturas fk_factura_emisor; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT fk_factura_emisor FOREIGN KEY (id_emisor) REFERENCES public.datos_emisor(id_emisor);


--
-- Name: facturas fk_factura_estado; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT fk_factura_estado FOREIGN KEY (id_estado_factura) REFERENCES public.estados_factura(id_estado_factura);


--
-- Name: facturas fk_factura_funcionario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT fk_factura_funcionario FOREIGN KEY (id_funcionario) REFERENCES public.funcionarios(id_funcionario);


--
-- Name: ficha_medica fk_ficha_grupo_sang; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medica
    ADD CONSTRAINT fk_ficha_grupo_sang FOREIGN KEY (id_grupo_sanguineo) REFERENCES public.grupos_sanguineos(id_grupo_sanguineo);


--
-- Name: ficha_medica fk_ficha_paciente; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ficha_medica
    ADD CONSTRAINT fk_ficha_paciente FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente);


--
-- Name: funcionarios fk_func_consultorio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT fk_func_consultorio FOREIGN KEY (id_consultorio) REFERENCES public.consultorio(id_consultorio);


--
-- Name: funcionarios fk_func_persona; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT fk_func_persona FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- Name: funcionarios fk_func_rol; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT fk_func_rol FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol);


--
-- Name: funcionarios fk_func_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT fk_func_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: insumos fk_insumo_tipo_iva; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT fk_insumo_tipo_iva FOREIGN KEY (id_tipo_iva) REFERENCES public.tipos_iva(id_tipo_iva);


--
-- Name: justificativos fk_justificativos_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.justificativos
    ADD CONSTRAINT fk_justificativos_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: motivos_nota fk_motivo_tipo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.motivos_nota
    ADD CONSTRAINT fk_motivo_tipo FOREIGN KEY (id_tipo_comprobante) REFERENCES public.tipos_comprobante(id_tipo_comprobante);


--
-- Name: notas fk_nota_factura; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_nota_factura FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);


--
-- Name: notas fk_nota_motivo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_nota_motivo FOREIGN KEY (id_motivo_nota) REFERENCES public.motivos_nota(id_motivo_nota);


--
-- Name: notas fk_nota_tipo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_nota_tipo FOREIGN KEY (id_tipo_comprobante) REFERENCES public.tipos_comprobante(id_tipo_comprobante);


--
-- Name: notas fk_nota_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_nota_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: orden_analisis fk_orden_analisis_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_analisis
    ADD CONSTRAINT fk_orden_analisis_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: orden_estudio fk_orden_estudio_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_estudio
    ADD CONSTRAINT fk_orden_estudio_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: receta_detalle fk_receta_detalle_medicamento; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT fk_receta_detalle_medicamento FOREIGN KEY (id_medicamento) REFERENCES public.medicamentos(id_medicamento);


--
-- Name: receta_detalle fk_receta_detalle_receta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT fk_receta_detalle_receta FOREIGN KEY (id_receta) REFERENCES public.recetas(id_receta);


--
-- Name: recetas fk_recetas_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT fk_recetas_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: servicios_facturables fk_servicio_iva; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servicios_facturables
    ADD CONSTRAINT fk_servicio_iva FOREIGN KEY (id_tipo_iva) REFERENCES public.tipos_iva(id_tipo_iva);


--
-- Name: signos_vitales fk_signos_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales
    ADD CONSTRAINT fk_signos_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: stock_insumos fk_stock_consulta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_insumos
    ADD CONSTRAINT fk_stock_consulta FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);


--
-- Name: stock_insumos fk_stock_insumo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_insumos
    ADD CONSTRAINT fk_stock_insumo FOREIGN KEY (id_insumo) REFERENCES public.insumos(id_insumo);


--
-- Name: stock_insumos fk_stock_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_insumos
    ADD CONSTRAINT fk_stock_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: tratamientos fk_tratamientos_enfermedad; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT fk_tratamientos_enfermedad FOREIGN KEY (id_enfermedad) REFERENCES public.enfermedades(id_enfermedad);


--
-- Name: usuarios fk_usuario_rol; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol);


--
-- Name: medicos medicos_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicos
    ADD CONSTRAINT medicos_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: orden_analisis orden_analisis_id_tipo_orden_analisis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_analisis
    ADD CONSTRAINT orden_analisis_id_tipo_orden_analisis_fkey FOREIGN KEY (id_tipo_orden_analisis) REFERENCES public.tipo_orden_analisis(id_tipo_orden_analisis) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: orden_estudio orden_estudio_id_tipo_orden_estudio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_estudio
    ADD CONSTRAINT orden_estudio_id_tipo_orden_estudio_fkey FOREIGN KEY (id_tipo_orden_estudio) REFERENCES public.tipo_orden_estudio(id_tipo_orden_estudio) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: pacientes pacientes_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: permisos_rol permisos_rol_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permisos_rol
    ADD CONSTRAINT permisos_rol_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol) ON DELETE CASCADE;


--
-- Name: personas personas_id_ciudad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_ciudad_fkey FOREIGN KEY (id_ciudad) REFERENCES public.ciudades(id_ciudad) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: personas personas_id_estado_civil_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_estado_civil_fkey FOREIGN KEY (id_estado_civil) REFERENCES public.estado_civiles(id_estado_civil) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: personas personas_id_genero_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_genero_fkey FOREIGN KEY (id_genero) REFERENCES public.generos(id_genero) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

