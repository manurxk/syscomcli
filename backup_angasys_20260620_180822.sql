--
-- PostgreSQL database dump
--

\restrict 2cnVbQwHvvCiihqzcho5z9RUAeFeOqOpMX37EMP6ObPu3AmXZO4wS5jQ6oCtkna

-- Dumped from database version 17.9 (Debian 17.9-1.pgdg13+1)
-- Dumped by pg_dump version 17.9 (Debian 17.9-1.pgdg13+1)

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
-- Name: consultorio; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA consultorio;


ALTER SCHEMA consultorio OWNER TO postgres;

--
-- Name: core; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA core;


ALTER SCHEMA core OWNER TO postgres;

--
-- Name: facturacion; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA facturacion;


ALTER SCHEMA facturacion OWNER TO postgres;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: canal_notificacion_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.canal_notificacion_domain AS text
	CONSTRAINT canal_notificacion_domain_check CHECK ((VALUE = ANY (ARRAY['WHATSAPP'::text, 'SMS'::text, 'EMAIL'::text, 'PUSH'::text])));


ALTER DOMAIN public.canal_notificacion_domain OWNER TO postgres;

--
-- Name: estado_empresa_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.estado_empresa_domain AS text
	CONSTRAINT estado_empresa_domain_check CHECK ((VALUE = ANY (ARRAY['LEAD'::text, 'ACTIVO'::text, 'VENCIDO'::text, 'SUSPENDIDO'::text, 'CANCELADO'::text])));


ALTER DOMAIN public.estado_empresa_domain OWNER TO postgres;

--
-- Name: estado_envio_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.estado_envio_domain AS text
	CONSTRAINT estado_envio_domain_check CHECK ((VALUE = ANY (ARRAY['PENDIENTE'::text, 'ENVIANDO'::text, 'ENVIADO'::text, 'ENTREGADO'::text, 'FALLIDO'::text, 'CANCELADO'::text])));


ALTER DOMAIN public.estado_envio_domain OWNER TO postgres;

--
-- Name: estado_ruc_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.estado_ruc_domain AS text
	CONSTRAINT estado_ruc_domain_check CHECK ((VALUE = ANY (ARRAY['ACTIVO'::text, 'PENDIENTE'::text, 'SUSPENDIDO'::text])));


ALTER DOMAIN public.estado_ruc_domain OWNER TO postgres;

--
-- Name: evento_suscripcion_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.evento_suscripcion_domain AS text
	CONSTRAINT evento_suscripcion_domain_check CHECK ((VALUE = ANY (ARRAY['CREACION'::text, 'CAMBIO_PLAN'::text, 'RENOVACION'::text, 'CANCELACION'::text, 'SUSPENSION'::text, 'REACTIVACION'::text, 'VENCIMIENTO'::text])));


ALTER DOMAIN public.evento_suscripcion_domain OWNER TO postgres;

--
-- Name: forma_juridica_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.forma_juridica_domain AS text
	CONSTRAINT forma_juridica_domain_check CHECK ((VALUE = ANY (ARRAY['EAS'::text, 'SRL'::text, 'SA'::text, 'UNIPERSONAL'::text, 'OTRO'::text])));


ALTER DOMAIN public.forma_juridica_domain OWNER TO postgres;

--
-- Name: modalidad_cita_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.modalidad_cita_domain AS text
	CONSTRAINT modalidad_cita_domain_check CHECK ((VALUE = ANY (ARRAY['PRESENCIAL'::text, 'REMOTA'::text, 'DOMICILIO'::text])));


ALTER DOMAIN public.modalidad_cita_domain OWNER TO postgres;

--
-- Name: tipo_certificado_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.tipo_certificado_domain AS text
	CONSTRAINT tipo_certificado_domain_check CHECK ((VALUE = ANY (ARRAY['SIFEN_P12'::text, 'SSL_TLS'::text, 'FIRMA_ELECTRONICA'::text])));


ALTER DOMAIN public.tipo_certificado_domain OWNER TO postgres;

--
-- Name: tipo_empresa_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.tipo_empresa_domain AS text
	CONSTRAINT tipo_empresa_domain_check CHECK ((VALUE = ANY (ARRAY['CONSULTORIO_MEDICO_GENERAL'::text, 'CONSULTORIO_ODONTOLOGIA'::text, 'CONSULTORIO_PSICOLOGIA'::text, 'CONSULTORIO_NUTRICION'::text, 'CONSULTORIO_FISIOTERAPIA'::text, 'CONSULTORIO_PEDIATRIA'::text, 'CLINICA_MULTIESPECIALIDAD'::text, 'CLINICA_ESTETICA'::text, 'CENTRO_REHABILITACION'::text, 'CENTRO_SALUD_MENTAL'::text, 'CENTRO_IMAGENOLOGIA'::text, 'LABORATORIO'::text, 'FARMACIA'::text, 'OPTICA_MEDICA'::text, 'SANATORIO'::text, 'OPERADORA_SAAS'::text])));


ALTER DOMAIN public.tipo_empresa_domain OWNER TO postgres;

--
-- Name: tipo_excedente_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.tipo_excedente_domain AS text
	CONSTRAINT tipo_excedente_domain_check CHECK ((VALUE = ANY (ARRAY['USUARIO_EXTRA'::text, 'FUNCIONARIO_EXTRA'::text, 'SEDE_EXTRA'::text, 'PACIENTE_EXTRA'::text, 'ESPECIALISTA_EXTRA'::text])));


ALTER DOMAIN public.tipo_excedente_domain OWNER TO postgres;

--
-- Name: tipo_firma_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.tipo_firma_domain AS text
	CONSTRAINT tipo_firma_domain_check CHECK ((VALUE = ANY (ARRAY['DIGITAL'::text, 'PANTALLA'::text, 'ESCANEADA'::text])));


ALTER DOMAIN public.tipo_firma_domain OWNER TO postgres;

--
-- Name: tipo_mov_stock_domain; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.tipo_mov_stock_domain AS text
	CONSTRAINT tipo_mov_stock_domain_check CHECK ((VALUE = ANY (ARRAY['ENTRADA'::text, 'SALIDA'::text, 'AJUSTE'::text])));


ALTER DOMAIN public.tipo_mov_stock_domain OWNER TO postgres;

--
-- Name: fn_next_nro_contrato(integer); Type: FUNCTION; Schema: consultorio; Owner: postgres
--

CREATE FUNCTION consultorio.fn_next_nro_contrato(p_id_empresa integer) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_next BIGINT;
BEGIN
  PERFORM pg_advisory_xact_lock(p_id_empresa::BIGINT + 9000000);
  SELECT COALESCE(MAX(nro_contrato), 0) + 1
    INTO v_next
    FROM consultorio.contratos_tratamiento
   WHERE id_empresa = p_id_empresa;
  RETURN v_next;
END;
$$;


ALTER FUNCTION consultorio.fn_next_nro_contrato(p_id_empresa integer) OWNER TO postgres;

--
-- Name: fn_next_nro_documento(integer, text); Type: FUNCTION; Schema: consultorio; Owner: postgres
--

CREATE FUNCTION consultorio.fn_next_nro_documento(p_id_empresa integer, p_tipo_doc text) RETURNS bigint
    LANGUAGE plpgsql
    AS $_$
DECLARE
  v_tabla TEXT;
  v_next  BIGINT;
BEGIN
  v_tabla := CASE p_tipo_doc
    WHEN 'RECETA'         THEN 'recetas'
    WHEN 'ORDEN_ESTUDIOS' THEN 'ordenes_estudios'
    WHEN 'ORDEN_ANALISIS' THEN 'ordenes_analisis'
    WHEN 'JUSTIFICATIVO'  THEN 'justificativos'
    ELSE NULL
  END;
  IF v_tabla IS NULL THEN
    RAISE EXCEPTION 'fn_next_nro_documento: tipo_doc no reconocido: %', p_tipo_doc;
  END IF;
  PERFORM pg_advisory_xact_lock(
    hashtext(p_id_empresa::text || ':' || p_tipo_doc)::bigint
  );
  EXECUTE format(
    'SELECT COALESCE(MAX(nro_documento), 0) + 1 FROM consultorio.%I WHERE id_empresa = $1',
    v_tabla
  ) INTO v_next USING p_id_empresa;
  RETURN v_next;
END;
$_$;


ALTER FUNCTION consultorio.fn_next_nro_documento(p_id_empresa integer, p_tipo_doc text) OWNER TO postgres;

--
-- Name: fn_next_nro_episodio(integer); Type: FUNCTION; Schema: consultorio; Owner: postgres
--

CREATE FUNCTION consultorio.fn_next_nro_episodio(p_id_empresa integer) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_next BIGINT;
BEGIN
  PERFORM pg_advisory_xact_lock(p_id_empresa::BIGINT);
  SELECT COALESCE(MAX(nro_episodio_empresa), 0) + 1
    INTO v_next
    FROM consultorio.episodios
   WHERE id_empresa = p_id_empresa;
  RETURN v_next;
END;
$$;


ALTER FUNCTION consultorio.fn_next_nro_episodio(p_id_empresa integer) OWNER TO postgres;

--
-- Name: fn_seed_antecedentes_por_tipo(integer, text); Type: FUNCTION; Schema: consultorio; Owner: postgres
--

CREATE FUNCTION consultorio.fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN

  IF p_cod_tipo = 'PSICOLOGIA' THEN

    INSERT INTO consultorio.formularios_definicion
      (id_empresa, des_formulario, cod_especialidad, cod_tipo_formulario, des_estructura, id_usuario_creacion)
    VALUES (
      p_id_empresa,
      'Antecedentes Psicológicos',
      'PSICOLOGIA',
      'ANTECEDENTES',
      '{
        "campos": [
          {
            "id": "ant_familiares_psiq",
            "label": "Antecedentes familiares psiquiátricos",
            "tipo": "texto",
            "placeholder": "Diagnósticos en familiares directos...",
            "requerido": false
          },
          {
            "id": "diagnosticos_previos",
            "label": "Diagnósticos psicológicos / psiquiátricos previos",
            "tipo": "texto",
            "requerido": false
          },
          {
            "id": "tratamientos_previos",
            "label": "Tratamientos psicológicos previos",
            "tipo": "texto",
            "placeholder": "Terapias, profesionales, duración...",
            "requerido": false
          },
          {
            "id": "internaciones_psiq",
            "label": "Internaciones psiquiátricas",
            "tipo": "boolean",
            "requerido": false
          },
          {
            "id": "intentos_autolesion",
            "label": "Antecedentes de autolesión o intentos",
            "tipo": "boolean",
            "requerido": false
          },
          {
            "id": "consumo_sustancias",
            "label": "Consumo de sustancias",
            "tipo": "texto",
            "placeholder": "Tipo, frecuencia, estado actual...",
            "requerido": false
          },
          {
            "id": "motivo_consulta_inicial",
            "label": "Motivo de consulta inicial",
            "tipo": "texto",
            "requerido": false
          }
        ]
      }'::jsonb,
      1
    )
    ON CONFLICT (id_empresa, des_formulario) DO NOTHING;

  ELSIF p_cod_tipo = 'DERMATOLOGIA' THEN

    INSERT INTO consultorio.formularios_definicion
      (id_empresa, des_formulario, cod_especialidad, cod_tipo_formulario, des_estructura, id_usuario_creacion)
    VALUES (
      p_id_empresa,
      'Antecedentes Dermatológicos',
      'DERMATOLOGIA',
      'ANTECEDENTES',
      '{
        "campos": [
          {
            "id": "tipo_piel",
            "label": "Tipo de piel",
            "tipo": "select",
            "opciones": ["", "Normal","Seca","Grasa","Mixta","Sensible"],
            "requerido": false
          },
          {
            "id": "fototipo",
            "label": "Fototipo Fitzpatrick",
            "tipo": "select",
            "opciones": ["", "I","II","III","IV","V","VI"],
            "requerido": false
          },
          {
            "id": "ant_dermatologicos",
            "label": "Antecedentes dermatológicos",
            "tipo": "texto",
            "placeholder": "Afecciones previas, tratamientos...",
            "requerido": false
          },
          {
            "id": "tratamientos_previos",
            "label": "Tratamientos estéticos / dermatológicos previos",
            "tipo": "texto",
            "requerido": false
          },
          {
            "id": "exposicion_solar",
            "label": "Exposición solar habitual",
            "tipo": "select",
            "opciones": ["", "Baja","Moderada","Alta"],
            "requerido": false
          }
        ]
      }'::jsonb,
      1
    )
    ON CONFLICT (id_empresa, des_formulario) DO NOTHING;

  ELSIF p_cod_tipo = 'SPA' THEN

    INSERT INTO consultorio.formularios_definicion
      (id_empresa, des_formulario, cod_especialidad, cod_tipo_formulario, des_estructura, id_usuario_creacion)
    VALUES (
      p_id_empresa,
      'Antecedentes Spa / Estética',
      'SPA',
      'ANTECEDENTES',
      '{
        "campos": [
          {
            "id": "embarazo_lactancia",
            "label": "¿Embarazo o lactancia actual?",
            "tipo": "boolean",
            "requerido": false
          },
          {
            "id": "patologias_contraindicadas",
            "label": "Patologías que contraindican tratamientos",
            "tipo": "texto",
            "placeholder": "Varices, marcapasos, prótesis metálicas...",
            "requerido": false
          },
          {
            "id": "tratamientos_previos",
            "label": "Tratamientos previos en spa / estética",
            "tipo": "texto",
            "requerido": false
          },
          {
            "id": "objetivos",
            "label": "Objetivos del paciente",
            "tipo": "texto",
            "placeholder": "Qué espera lograr con los tratamientos...",
            "requerido": false
          }
        ]
      }'::jsonb,
      1
    )
    ON CONFLICT (id_empresa, des_formulario) DO NOTHING;

  ELSIF p_cod_tipo = 'PODOLOGIA' THEN

    INSERT INTO consultorio.formularios_definicion
      (id_empresa, des_formulario, cod_especialidad, cod_tipo_formulario, des_estructura, id_usuario_creacion)
    VALUES (
      p_id_empresa,
      'Antecedentes Podológicos',
      'PODOLOGIA',
      'ANTECEDENTES',
      '{
        "campos": [
          {
            "id": "diabetes",
            "label": "Diabetes",
            "tipo": "boolean",
            "requerido": false
          },
          {
            "id": "tipo_diabetes",
            "label": "Tipo de diabetes (si aplica)",
            "tipo": "select",
            "opciones": ["", "Tipo 1","Tipo 2","Gestacional","MODY"],
            "requerido": false
          },
          {
            "id": "ant_vasculares",
            "label": "Antecedentes vasculares",
            "tipo": "texto",
            "placeholder": "Varices, insuficiencia venosa, arteriopatía...",
            "requerido": false
          },
          {
            "id": "patologias_pie",
            "label": "Patologías del pie previas",
            "tipo": "texto",
            "placeholder": "Hongos, callosidades, uñas encarnadas...",
            "requerido": false
          },
          {
            "id": "usa_plantillas",
            "label": "Usa plantillas ortopédicas",
            "tipo": "boolean",
            "requerido": false
          }
        ]
      }'::jsonb,
      1
    )
    ON CONFLICT (id_empresa, des_formulario) DO NOTHING;

  ELSE
    -- CLINICA_GENERAL y cualquier tipo no específico → sin datos_especificos
    -- Los campos universales (alergias, medicación, grupo sanguíneo,
    -- antecedentes personales/familiares) ya cubren el caso general.
    NULL;

  END IF;

END;
$$;


ALTER FUNCTION consultorio.fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text) OWNER TO postgres;

--
-- Name: fn_seed_consultorio_por_tipo(integer, text); Type: FUNCTION; Schema: consultorio; Owner: postgres
--

CREATE FUNCTION consultorio.fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_id_tipo_rep_laboral   INTEGER;
  v_id_tipo_consulta      INTEGER;
  v_id_tipo_constancia    INTEGER;
  v_id_tipo_reposo_esc    INTEGER;
  v_id_perfil_clinico     INTEGER;
BEGIN

  -- ----------------------------------------------------------------
  -- BLOQUE A — Procedimientos (universal + los de la especialidad)
  -- ----------------------------------------------------------------
  INSERT INTO consultorio.procedimientos_empresa
    (id_empresa, id_tipo_procedimiento, cod_procedimiento, des_procedimiento,
     duracion_min, es_requiere_insumos, id_usuario_creacion)
  SELECT
    p_id_empresa,
    tp.id_tipo_procedimiento,
    tp.cod_tipo_procedimiento,
    tp.des_tipo_procedimiento,
    CASE tp.cod_tipo_procedimiento
      WHEN 'PRIMERA_CONSULTA'       THEN 60
      WHEN 'CONSULTA_CONTROL'       THEN 50
      WHEN 'CONSULTA_URGENCIA'      THEN 30
      WHEN 'SESION_INDIVIDUAL'      THEN 50
      WHEN 'SESION_GRUPAL'          THEN 90
      WHEN 'EVALUACION_PSICOLOGICA' THEN 90
      WHEN 'INFORME_PSICOLOGICO'    THEN 30
      WHEN 'ORIENTACION_FAMILIAR'   THEN 60
      ELSE 30
    END,
    FALSE,
    1
  FROM consultorio.tipos_procedimientos tp
  WHERE tp.est_tipo_procedimiento = TRUE
    AND (tp.cod_especialidad_base IS NULL OR tp.cod_especialidad_base = p_cod_tipo)
  ON CONFLICT (id_empresa, cod_procedimiento) DO NOTHING;

  -- ----------------------------------------------------------------
  -- BLOQUE B — Medicamentos (solo para tipos que lo requieren)
  -- ----------------------------------------------------------------
  IF p_cod_tipo = 'PSICOLOGIA' THEN

    INSERT INTO consultorio.medicamentos_empresa
      (id_empresa, des_medicamento, des_principio_activo, des_concentracion,
       des_forma_farmaceutica, es_psicofarmaco, id_usuario_creacion)
    VALUES
      (p_id_empresa, 'Alprazolam 0.25mg',       'Alprazolam',         '0.25mg', 'Comprimido', TRUE,  1),
      (p_id_empresa, 'Alprazolam 0.5mg',        'Alprazolam',         '0.5mg',  'Comprimido', TRUE,  1),
      (p_id_empresa, 'Alprazolam 1mg',           'Alprazolam',         '1mg',    'Comprimido', TRUE,  1),
      (p_id_empresa, 'Clonazepam 0.5mg',        'Clonazepam',         '0.5mg',  'Comprimido', TRUE,  1),
      (p_id_empresa, 'Clonazepam 2mg',           'Clonazepam',         '2mg',    'Comprimido', TRUE,  1),
      (p_id_empresa, 'Diazepam 5mg',             'Diazepam',           '5mg',    'Comprimido', TRUE,  1),
      (p_id_empresa, 'Lorazepam 1mg',            'Lorazepam',          '1mg',    'Comprimido', TRUE,  1),
      (p_id_empresa, 'Fluoxetina 20mg',          'Fluoxetina',         '20mg',   'Cápsula',    TRUE,  1),
      (p_id_empresa, 'Sertralina 50mg',          'Sertralina',         '50mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Sertralina 100mg',         'Sertralina',         '100mg',  'Comprimido', TRUE,  1),
      (p_id_empresa, 'Escitalopram 10mg',        'Escitalopram',       '10mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Escitalopram 20mg',        'Escitalopram',       '20mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Paroxetina 20mg',          'Paroxetina',         '20mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Venlafaxina 75mg',         'Venlafaxina',        '75mg',   'Cápsula',    TRUE,  1),
      (p_id_empresa, 'Venlafaxina 150mg',        'Venlafaxina',        '150mg',  'Cápsula',    TRUE,  1),
      (p_id_empresa, 'Duloxetina 60mg',          'Duloxetina',         '60mg',   'Cápsula',    TRUE,  1),
      (p_id_empresa, 'Risperidona 1mg',          'Risperidona',        '1mg',    'Comprimido', TRUE,  1),
      (p_id_empresa, 'Risperidona 2mg',          'Risperidona',        '2mg',    'Comprimido', TRUE,  1),
      (p_id_empresa, 'Quetiapina 25mg',          'Quetiapina',         '25mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Quetiapina 100mg',         'Quetiapina',         '100mg',  'Comprimido', TRUE,  1),
      (p_id_empresa, 'Quetiapina 200mg',         'Quetiapina',         '200mg',  'Comprimido', TRUE,  1),
      (p_id_empresa, 'Olanzapina 5mg',           'Olanzapina',         '5mg',    'Comprimido', TRUE,  1),
      (p_id_empresa, 'Olanzapina 10mg',          'Olanzapina',         '10mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Aripiprazol 10mg',         'Aripiprazol',        '10mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Carbonato de Litio 300mg', 'Carbonato de Litio', '300mg',  'Comprimido', TRUE,  1),
      (p_id_empresa, 'Ácido Valproico 500mg',    'Ácido Valproico',    '500mg',  'Comprimido', TRUE,  1),
      (p_id_empresa, 'Zolpidem 10mg',            'Zolpidem',           '10mg',   'Comprimido', TRUE,  1),
      (p_id_empresa, 'Melatonina 3mg',           'Melatonina',         '3mg',    'Comprimido', FALSE, 1),
      (p_id_empresa, 'Buspirona 10mg',           'Buspirona',          '10mg',   'Comprimido', TRUE,  1)
    ON CONFLICT (id_empresa, des_medicamento, des_concentracion) DO NOTHING;

  END IF;

  -- ----------------------------------------------------------------
  -- BLOQUE C — Plantillas de justificativos
  -- ----------------------------------------------------------------
  SELECT id_tipo_justificativo INTO v_id_tipo_rep_laboral
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'REPOSO_LABORAL';
  SELECT id_tipo_justificativo INTO v_id_tipo_consulta
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'CONSULTA';
  SELECT id_tipo_justificativo INTO v_id_tipo_constancia
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'CONSTANCIA_TRATAMIENTO';
  SELECT id_tipo_justificativo INTO v_id_tipo_reposo_esc
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'REPOSO_ESCOLAR';

  INSERT INTO consultorio.plantillas_justificativos
    (id_empresa, id_tipo_justificativo, des_titulo, des_cuerpo_template, id_usuario_creacion)
  VALUES
    (p_id_empresa, v_id_tipo_rep_laboral,
     'Reposo Laboral Estándar',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La paciente {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, fue atendido/a en consulta el día {{fecha_emision}} y se indica REPOSO por {{dias_reposo}} día/s, desde el {{fecha_inicio_reposo}} hasta el {{fecha_fin_reposo}}.

Diagnóstico: {{diagnostico}}

Se extiende el presente certificado a solicitud de la parte interesada, en {{nombre_empresa}}.', 1),

    (p_id_empresa, v_id_tipo_reposo_esc,
     'Reposo Escolar Estándar',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La alumno/a {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, requiere REPOSO ESCOLAR por {{dias_reposo}} día/s, desde el {{fecha_inicio_reposo}} hasta el {{fecha_fin_reposo}}.

Diagnóstico: {{diagnostico}}

Se extiende el presente certificado a solicitud de la parte interesada, en {{nombre_empresa}}.', 1),

    (p_id_empresa, v_id_tipo_consulta,
     'Constancia de Consulta',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La paciente {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, se presentó a consulta en {{nombre_empresa}} el día {{fecha_emision}}.

Se extiende el presente certificado a solicitud de la parte interesada.', 1),

    (p_id_empresa, v_id_tipo_constancia,
     'Constancia de Tratamiento en Curso',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La paciente {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, se encuentra bajo tratamiento psicológico en {{nombre_empresa}} desde el {{fecha_inicio_tratamiento}}.

Diagnóstico: {{diagnostico}}

Se extiende el presente certificado a solicitud de la parte interesada.', 1)

  ON CONFLICT (id_empresa, id_tipo_justificativo, des_titulo) DO NOTHING;

  -- ----------------------------------------------------------------
  -- BLOQUE D — Formulario de preconsulta
  -- ----------------------------------------------------------------
  IF p_cod_tipo = 'PSICOLOGIA' THEN

    INSERT INTO consultorio.formularios_definicion
      (id_empresa, des_formulario, cod_especialidad, des_estructura, id_usuario_creacion)
    VALUES (
      p_id_empresa,
      'Formulario de Preconsulta Psicológica',
      'PSICOLOGIA',
      '{
        "campos": [
          {"id":"estado_animo","label":"¿Cómo te sentís hoy?","tipo":"select",
           "opciones":["Muy bien","Bien","Regular","Mal","Muy mal"],"requerido":true},
          {"id":"nivel_ansiedad","label":"Nivel de ansiedad (0 = ninguna, 10 = máxima)",
           "tipo":"escala","min":0,"max":10,"requerido":false},
          {"id":"duracion_sueno","label":"¿Cuántas horas dormiste anoche?",
           "tipo":"numero","min":0,"max":24,"requerido":false},
          {"id":"tomo_medicacion","label":"¿Tomaste tu medicación hoy?",
           "tipo":"boolean","requerido":false},
          {"id":"motivo_sesion","label":"¿Hay algo puntual que quieras trabajar en esta sesión?",
           "tipo":"texto","requerido":false}
        ]
      }'::jsonb,
      1
    )
    ON CONFLICT (id_empresa, des_formulario) DO NOTHING;

  END IF;

  -- ----------------------------------------------------------------
  -- BLOQUE E — Spine clínico + perfil psicología (nuevo en m13)
  -- ----------------------------------------------------------------
  INSERT INTO consultorio.empresa_perfil_clinico
    (id_empresa, cod_tipo_clinico, id_usuario_creacion)
  VALUES (p_id_empresa, p_cod_tipo, 1)
  ON CONFLICT (id_empresa) DO NOTHING
  RETURNING id_empresa_perfil_clinico INTO v_id_perfil_clinico;

  -- Si DO NOTHING se disparó, recuperar el id existente
  IF v_id_perfil_clinico IS NULL THEN
    SELECT id_empresa_perfil_clinico INTO v_id_perfil_clinico
    FROM consultorio.empresa_perfil_clinico
    WHERE id_empresa = p_id_empresa;
  END IF;

  IF p_cod_tipo = 'PSICOLOGIA' THEN
    INSERT INTO consultorio.psicologia_perfil_empresa
      (id_empresa_perfil_clinico, id_empresa, id_usuario_creacion)
    VALUES (v_id_perfil_clinico, p_id_empresa, 1)
    ON CONFLICT (id_empresa_perfil_clinico) DO NOTHING;
  END IF;

END;
$$;


ALTER FUNCTION consultorio.fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text) OWNER TO postgres;

--
-- Name: fn_check_limite_sedes(); Type: FUNCTION; Schema: core; Owner: postgres
--

CREATE FUNCTION core.fn_check_limite_sedes() RETURNS trigger
    LANGUAGE plpgsql SECURITY DEFINER
    AS $$
DECLARE
  v_max_sedes      INTEGER;
  v_sedes_actuales INTEGER;
BEGIN
  SELECT p.max_sedes INTO v_max_sedes
  FROM suscripciones s
  JOIN planes p ON s.id_plan = p.id_plan
  WHERE s.id_empresa = NEW.id_empresa
    AND s.est_suscripcion = TRUE
    AND s.fec_vencimiento > now()
  ORDER BY s.fec_vencimiento DESC
  LIMIT 1;

  IF v_max_sedes IS NULL THEN
    RETURN NEW;
  END IF;

  SELECT COUNT(*) INTO v_sedes_actuales
  FROM sedes
  WHERE id_empresa = NEW.id_empresa
    AND est_sede = TRUE
    AND fec_eliminacion IS NULL;

  IF v_sedes_actuales >= v_max_sedes THEN
    RAISE EXCEPTION 'LIMITE_SEDES: Límite de % sede(s) alcanzado para el plan activo.', v_max_sedes
      USING ERRCODE = 'P0001';
  END IF;

  RETURN NEW;
END;
$$;


ALTER FUNCTION core.fn_check_limite_sedes() OWNER TO postgres;

--
-- Name: fn_next_nro_de(integer, integer, character, character, character, character); Type: FUNCTION; Schema: facturacion; Owner: postgres
--

CREATE FUNCTION facturacion.fn_next_nro_de(p_id_empresa integer, p_id_timbrado integer, p_cod_establecimiento character, p_cod_punto_expedicion character, p_cod_tipo_de character, p_cod_serie character) RETURNS character
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_nro_ultimo BIGINT;
BEGIN
  -- Crea la fila de secuencia si no existe para esta combinación (idempotente)
  INSERT INTO facturacion.secuencias_numeracion (
    id_empresa, id_timbrado, cod_establecimiento, cod_punto_expedicion,
    cod_tipo_de, cod_serie, nro_ultimo, est_secuencia,
    id_usuario_creacion, fec_creacion
  )
  VALUES (
    p_id_empresa, p_id_timbrado, p_cod_establecimiento, p_cod_punto_expedicion,
    p_cod_tipo_de, p_cod_serie, 0, TRUE, 0, now()
  )
  ON CONFLICT DO NOTHING;

  -- Bloqueo pesimista: un solo proceso avanza la secuencia a la vez
  SELECT nro_ultimo
    INTO v_nro_ultimo
    FROM facturacion.secuencias_numeracion
   WHERE id_empresa            = p_id_empresa
     AND id_timbrado           = p_id_timbrado
     AND cod_establecimiento   = p_cod_establecimiento
     AND cod_punto_expedicion  = p_cod_punto_expedicion
     AND cod_tipo_de           = p_cod_tipo_de
     AND (cod_serie = p_cod_serie OR (cod_serie IS NULL AND p_cod_serie IS NULL))
   FOR UPDATE;

  IF v_nro_ultimo >= 9999999 THEN
    RAISE EXCEPTION
      'SECUENCIA_AGOTADA: timbrado=%, tipo_de=%, serie=%. Iniciar nueva serie o timbrado.',
      p_id_timbrado, p_cod_tipo_de, COALESCE(p_cod_serie, 'NULL');
  END IF;

  UPDATE facturacion.secuencias_numeracion
     SET nro_ultimo         = nro_ultimo + 1,
         fec_modificacion   = now()
   WHERE id_empresa            = p_id_empresa
     AND id_timbrado           = p_id_timbrado
     AND cod_establecimiento   = p_cod_establecimiento
     AND cod_punto_expedicion  = p_cod_punto_expedicion
     AND cod_tipo_de           = p_cod_tipo_de
     AND (cod_serie = p_cod_serie OR (cod_serie IS NULL AND p_cod_serie IS NULL));

  RETURN lpad((v_nro_ultimo + 1)::TEXT, 7, '0');
END;
$$;


ALTER FUNCTION facturacion.fn_next_nro_de(p_id_empresa integer, p_id_timbrado integer, p_cod_establecimiento character, p_cod_punto_expedicion character, p_cod_tipo_de character, p_cod_serie character) OWNER TO postgres;

--
-- Name: app_current_tenant_id(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.app_current_tenant_id() RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v TEXT;
BEGIN
  v := current_setting('app.current_tenant_id', TRUE);
  IF v IS NULL OR v = '' THEN
    RAISE EXCEPTION 'Tenant no seteado: app.current_tenant_id';
  END IF;
  RETURN v::BIGINT;
END;
$$;


ALTER FUNCTION public.app_current_tenant_id() OWNER TO postgres;

--
-- Name: app_current_user_id(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.app_current_user_id() RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v TEXT;
BEGIN
  v := current_setting('app.current_user_id', TRUE);
  IF v IS NULL OR v = '' THEN RETURN NULL; END IF;
  RETURN v::BIGINT;
END;
$$;


ALTER FUNCTION public.app_current_user_id() OWNER TO postgres;

--
-- Name: app_is_super_admin(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.app_is_super_admin() RETURNS boolean
    LANGUAGE sql
    AS $$
  SELECT COALESCE(NULLIF(current_setting('app.is_super_admin', TRUE), ''), 'false')::BOOLEAN
$$;


ALTER FUNCTION public.app_is_super_admin() OWNER TO postgres;

--
-- Name: fn_rls_tenant_match(bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_rls_tenant_match(p_id_empresa bigint) RETURNS boolean
    LANGUAGE sql
    AS $$
  SELECT app_is_super_admin() OR (p_id_empresa = app_current_tenant_id())
$$;


ALTER FUNCTION public.fn_rls_tenant_match(p_id_empresa bigint) OWNER TO postgres;

--
-- Name: fn_seed_antecedentes_por_tipo(integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN

  IF p_cod_tipo = 'PSICOLOGIA' THEN

    INSERT INTO consultorio.formularios_definicion
      (id_empresa, des_formulario, cod_especialidad, cod_tipo_formulario, des_estructura, id_usuario_creacion)
    VALUES (
      p_id_empresa,
      'Antecedentes Psicológicos',
      'PSICOLOGIA',
      'ANTECEDENTES',
      '{
        "campos": [
          {
            "id": "ant_familiares_psiq",
            "label": "Antecedentes familiares psiquiátricos",
            "tipo": "texto",
            "placeholder": "Diagnósticos en familiares directos...",
            "requerido": false
          },
          {
            "id": "diagnosticos_previos",
            "label": "Diagnósticos psicológicos / psiquiátricos previos",
            "tipo": "texto",
            "requerido": false
          },
          {
            "id": "tratamientos_previos",
            "label": "Tratamientos psicológicos previos",
            "tipo": "texto",
            "placeholder": "Terapias, profesionales, duración...",
            "requerido": false
          },
          {
            "id": "internaciones_psiq",
            "label": "Internaciones psiquiátricas",
            "tipo": "boolean",
            "requerido": false
          },
          {
            "id": "intentos_autolesion",
            "label": "Antecedentes de autolesión o intentos",
            "tipo": "boolean",
            "requerido": false
          },
          {
            "id": "consumo_sustancias",
            "label": "Consumo de sustancias",
            "tipo": "texto",
            "placeholder": "Tipo, frecuencia, estado actual...",
            "requerido": false
          },
          {
            "id": "motivo_consulta_inicial",
            "label": "Motivo de consulta inicial",
            "tipo": "texto",
            "requerido": false
          }
        ]
      }'::jsonb,
      1
    )
    ON CONFLICT (id_empresa, des_formulario) DO NOTHING;

  END IF;

END;
$$;


ALTER FUNCTION public.fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text) OWNER TO postgres;

--
-- Name: fn_seed_consultorio_por_tipo(integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_id_tipo_rep_laboral    INTEGER;
  v_id_tipo_consulta       INTEGER;
  v_id_tipo_constancia     INTEGER;
  v_id_tipo_reposo_esc     INTEGER;
BEGIN

  -- ----------------------------------------------------------------
  -- BLOQUE A — Procedimientos (universal + psicología)
  -- ----------------------------------------------------------------
  INSERT INTO consultorio.procedimientos_empresa
    (id_empresa, id_tipo_procedimiento, cod_procedimiento, des_procedimiento, duracion_min, es_requiere_insumos, id_usuario_creacion)
  SELECT
    p_id_empresa,
    tp.id_tipo_procedimiento,
    tp.cod_tipo_procedimiento,
    tp.des_tipo_procedimiento,
    CASE tp.cod_tipo_procedimiento
      WHEN 'PRIMERA_CONSULTA'       THEN 60
      WHEN 'CONSULTA_CONTROL'       THEN 50
      WHEN 'CONSULTA_URGENCIA'      THEN 30
      WHEN 'SESION_INDIVIDUAL'      THEN 50
      WHEN 'SESION_GRUPAL'          THEN 90
      WHEN 'EVALUACION_PSICOLOGICA' THEN 90
      WHEN 'INFORME_PSICOLOGICO'    THEN 30
      WHEN 'ORIENTACION_FAMILIAR'   THEN 60
      ELSE 30
    END,
    FALSE,
    1
  FROM consultorio.tipos_procedimientos tp
  WHERE tp.est_tipo_procedimiento = TRUE
    AND (tp.cod_especialidad_base IS NULL OR tp.cod_especialidad_base = p_cod_tipo)
  ON CONFLICT (id_empresa, cod_procedimiento) DO NOTHING;

  -- ----------------------------------------------------------------
  -- BLOQUE B — Medicamentos (psicofármacos)
  -- ----------------------------------------------------------------
  IF p_cod_tipo = 'PSICOLOGIA' THEN

    INSERT INTO consultorio.medicamentos_empresa
      (id_empresa, des_medicamento, des_principio_activo, des_concentracion, des_forma_farmaceutica, es_psicofarmaco, id_usuario_creacion)
    VALUES
      -- Ansiolíticos
      (p_id_empresa, 'Alprazolam 0.25mg',    'Alprazolam',    '0.25mg', 'Comprimido', TRUE, 1),
      (p_id_empresa, 'Alprazolam 0.5mg',     'Alprazolam',    '0.5mg',  'Comprimido', TRUE, 1),
      (p_id_empresa, 'Alprazolam 1mg',        'Alprazolam',    '1mg',    'Comprimido', TRUE, 1),
      (p_id_empresa, 'Clonazepam 0.5mg',     'Clonazepam',    '0.5mg',  'Comprimido', TRUE, 1),
      (p_id_empresa, 'Clonazepam 2mg',        'Clonazepam',    '2mg',    'Comprimido', TRUE, 1),
      (p_id_empresa, 'Diazepam 5mg',          'Diazepam',      '5mg',    'Comprimido', TRUE, 1),
      (p_id_empresa, 'Lorazepam 1mg',         'Lorazepam',     '1mg',    'Comprimido', TRUE, 1),
      -- Antidepresivos ISRS
      (p_id_empresa, 'Fluoxetina 20mg',       'Fluoxetina',    '20mg',   'Cápsula',    TRUE, 1),
      (p_id_empresa, 'Sertralina 50mg',       'Sertralina',    '50mg',   'Comprimido', TRUE, 1),
      (p_id_empresa, 'Sertralina 100mg',      'Sertralina',    '100mg',  'Comprimido', TRUE, 1),
      (p_id_empresa, 'Escitalopram 10mg',     'Escitalopram',  '10mg',   'Comprimido', TRUE, 1),
      (p_id_empresa, 'Escitalopram 20mg',     'Escitalopram',  '20mg',   'Comprimido', TRUE, 1),
      (p_id_empresa, 'Paroxetina 20mg',       'Paroxetina',    '20mg',   'Comprimido', TRUE, 1),
      -- Antidepresivos duales
      (p_id_empresa, 'Venlafaxina 75mg',      'Venlafaxina',   '75mg',   'Cápsula',    TRUE, 1),
      (p_id_empresa, 'Venlafaxina 150mg',     'Venlafaxina',   '150mg',  'Cápsula',    TRUE, 1),
      (p_id_empresa, 'Duloxetina 60mg',       'Duloxetina',    '60mg',   'Cápsula',    TRUE, 1),
      -- Antipsicóticos atípicos
      (p_id_empresa, 'Risperidona 1mg',       'Risperidona',   '1mg',    'Comprimido', TRUE, 1),
      (p_id_empresa, 'Risperidona 2mg',       'Risperidona',   '2mg',    'Comprimido', TRUE, 1),
      (p_id_empresa, 'Quetiapina 25mg',       'Quetiapina',    '25mg',   'Comprimido', TRUE, 1),
      (p_id_empresa, 'Quetiapina 100mg',      'Quetiapina',    '100mg',  'Comprimido', TRUE, 1),
      (p_id_empresa, 'Quetiapina 200mg',      'Quetiapina',    '200mg',  'Comprimido', TRUE, 1),
      (p_id_empresa, 'Olanzapina 5mg',        'Olanzapina',    '5mg',    'Comprimido', TRUE, 1),
      (p_id_empresa, 'Olanzapina 10mg',       'Olanzapina',    '10mg',   'Comprimido', TRUE, 1),
      (p_id_empresa, 'Aripiprazol 10mg',      'Aripiprazol',   '10mg',   'Comprimido', TRUE, 1),
      -- Estabilizadores del ánimo
      (p_id_empresa, 'Carbonato de Litio 300mg','Carbonato de Litio','300mg','Comprimido', TRUE, 1),
      (p_id_empresa, 'Ácido Valproico 500mg', 'Ácido Valproico','500mg', 'Comprimido', TRUE, 1),
      -- Insomnio / otros
      (p_id_empresa, 'Zolpidem 10mg',         'Zolpidem',      '10mg',   'Comprimido', TRUE, 1),
      (p_id_empresa, 'Melatonina 3mg',         'Melatonina',    '3mg',    'Comprimido', FALSE, 1),
      (p_id_empresa, 'Buspirona 10mg',         'Buspirona',     '10mg',   'Comprimido', TRUE, 1)
    ON CONFLICT (id_empresa, des_medicamento, des_concentracion) DO NOTHING;

  END IF;

  -- ----------------------------------------------------------------
  -- BLOQUE C — Plantillas de justificativos
  -- ----------------------------------------------------------------
  SELECT id_tipo_justificativo INTO v_id_tipo_rep_laboral
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'REPOSO_LABORAL';
  SELECT id_tipo_justificativo INTO v_id_tipo_consulta
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'CONSULTA';
  SELECT id_tipo_justificativo INTO v_id_tipo_constancia
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'CONSTANCIA_TRATAMIENTO';
  SELECT id_tipo_justificativo INTO v_id_tipo_reposo_esc
    FROM consultorio.tipos_justificativos WHERE cod_tipo_justificativo = 'REPOSO_ESCOLAR';

  INSERT INTO consultorio.plantillas_justificativos
    (id_empresa, id_tipo_justificativo, des_titulo, des_cuerpo_template, id_usuario_creacion)
  VALUES
    (p_id_empresa, v_id_tipo_rep_laboral,
     'Reposo Laboral Estándar',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La paciente {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, fue atendido/a en consulta el día {{fecha_emision}} y se indica REPOSO por {{dias_reposo}} día/s, desde el {{fecha_inicio_reposo}} hasta el {{fecha_fin_reposo}}.

Diagnóstico: {{diagnostico}}

Se extiende el presente certificado a solicitud de la parte interesada, en {{nombre_empresa}}.', 1),

    (p_id_empresa, v_id_tipo_reposo_esc,
     'Reposo Escolar Estándar',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La alumno/a {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, requiere REPOSO ESCOLAR por {{dias_reposo}} día/s, desde el {{fecha_inicio_reposo}} hasta el {{fecha_fin_reposo}}.

Diagnóstico: {{diagnostico}}

Se extiende el presente certificado a solicitud de la parte interesada, en {{nombre_empresa}}.', 1),

    (p_id_empresa, v_id_tipo_consulta,
     'Constancia de Consulta',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La paciente {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, se presentó a consulta en {{nombre_empresa}} el día {{fecha_emision}}.

Se extiende el presente certificado a solicitud de la parte interesada.', 1),

    (p_id_empresa, v_id_tipo_constancia,
     'Constancia de Tratamiento en Curso',
     'Quien suscribe, {{nombre_profesional}}, matriculado/a bajo N° {{matricula_profesional}},

CERTIFICA QUE:

El/La paciente {{nombre_paciente}} {{apellido_paciente}}, C.I. {{cedula_paciente}}, se encuentra actualmente en tratamiento en {{nombre_empresa}}.

Se extiende el presente certificado a solicitud de la parte interesada, en {{nombre_empresa}}.', 1)
  ON CONFLICT (id_empresa, id_tipo_justificativo, des_titulo) DO NOTHING;

  -- ----------------------------------------------------------------
  -- BLOQUE D — Formulario de preconsulta (psicología)
  -- ----------------------------------------------------------------
  IF p_cod_tipo = 'PSICOLOGIA' THEN

    INSERT INTO consultorio.formularios_definicion
      (id_empresa, des_formulario, cod_especialidad, cod_tipo_formulario, des_estructura, id_usuario_creacion)
    VALUES (
      p_id_empresa,
      'Preconsulta Psicológica',
      'PSICOLOGIA',
      'PRECONSULTA',
      '{
        "campos": [
          {
            "id": "estado_animo",
            "label": "¿Cómo te sentís hoy?",
            "tipo": "select",
            "opciones": ["", "Muy bien", "Bien", "Regular", "Mal", "Muy mal"],
            "requerido": true
          },
          {
            "id": "nivel_ansiedad",
            "label": "Nivel de ansiedad (0 = ninguna, 10 = máxima)",
            "tipo": "escala",
            "requerido": false
          },
          {
            "id": "duracion_sueno",
            "label": "¿Cuántas horas dormiste anoche?",
            "tipo": "numero",
            "requerido": false
          },
          {
            "id": "tomo_medicacion",
            "label": "¿Tomaste tu medicación según lo indicado?",
            "tipo": "boolean",
            "requerido": false
          },
          {
            "id": "motivo_sesion",
            "label": "¿Hay algo puntual que quieras trabajar hoy?",
            "tipo": "texto",
            "requerido": false
          }
        ]
      }'::jsonb,
      1
    )
    ON CONFLICT (id_empresa, des_formulario) DO NOTHING;

  END IF;

END;
$$;


ALTER FUNCTION public.fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text) OWNER TO postgres;

--
-- Name: fn_set_fec_modificacion(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_set_fec_modificacion() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.fec_modificacion = now();
  IF NEW.id_usuario_modificacion IS NULL THEN
    NEW.id_usuario_modificacion = app_current_user_id();
  END IF;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.fn_set_fec_modificacion() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: acuerdo_monto_historial; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.acuerdo_monto_historial (
    id_acuerdo_monto bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_acuerdo_terapeutico bigint NOT NULL,
    monto numeric(15,0) NOT NULL,
    cod_moneda character varying(3) DEFAULT 'PYG'::character varying NOT NULL,
    fec_vigencia_desde date NOT NULL,
    fec_vigencia_hasta date,
    des_motivo_cambio text,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE ONLY consultorio.acuerdo_monto_historial FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.acuerdo_monto_historial OWNER TO postgres;

--
-- Name: acuerdo_monto_historial_id_acuerdo_monto_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.acuerdo_monto_historial_id_acuerdo_monto_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.acuerdo_monto_historial_id_acuerdo_monto_seq OWNER TO postgres;

--
-- Name: acuerdo_monto_historial_id_acuerdo_monto_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.acuerdo_monto_historial_id_acuerdo_monto_seq OWNED BY consultorio.acuerdo_monto_historial.id_acuerdo_monto;


--
-- Name: acuerdos_terapeuticos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.acuerdos_terapeuticos (
    id_acuerdo_terapeutico bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    nro_version smallint DEFAULT 1 NOT NULL,
    fec_firma date,
    tipo_fecha_pago character varying(10) DEFAULT 'RECURRENTE'::character varying NOT NULL,
    dia_pago_recurrente smallint,
    fec_pago_especifica date,
    sesiones_semanales smallint NOT NULL,
    hrs_preaviso_ausencia smallint NOT NULL,
    pct_multa_ausencia numeric(5,2) NOT NULL,
    monto_multa_atraso_dia numeric(15,0) NOT NULL,
    max_ausencias_consecutivas smallint NOT NULL,
    dias_elaboracion_informe smallint NOT NULL,
    cod_moneda character varying(3) DEFAULT 'PYG'::character varying NOT NULL,
    es_entrevista_docente boolean DEFAULT false NOT NULL,
    monto_entrevista_docente numeric(15,0),
    tipo_informe_adicional character varying(20),
    monto_informe_adicional numeric(15,0),
    es_consentimiento_camaras boolean DEFAULT false NOT NULL,
    fec_consentimiento_camaras timestamp with time zone,
    url_firma_profesional text,
    url_firma_tutor text,
    des_observaciones text,
    est_acuerdo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT acuerdos_terapeuticos_dia_pago_recurrente_check CHECK (((dia_pago_recurrente >= 1) AND (dia_pago_recurrente <= 31))),
    CONSTRAINT acuerdos_terapeuticos_tipo_fecha_pago_check CHECK (((tipo_fecha_pago)::text = ANY (ARRAY[('RECURRENTE'::character varying)::text, ('ESPECIFICA'::character varying)::text]))),
    CONSTRAINT acuerdos_terapeuticos_tipo_informe_adicional_check CHECK (((tipo_informe_adicional)::text = ANY (ARRAY[('EDUCATIVO'::character varying)::text, ('LEGAL'::character varying)::text, ('EVOLUCION'::character varying)::text]))),
    CONSTRAINT chk_acuerdo_fecha_pago CHECK (((((tipo_fecha_pago)::text = 'RECURRENTE'::text) AND (dia_pago_recurrente IS NOT NULL) AND (fec_pago_especifica IS NULL)) OR (((tipo_fecha_pago)::text = 'ESPECIFICA'::text) AND (fec_pago_especifica IS NOT NULL) AND (dia_pago_recurrente IS NULL))))
);

ALTER TABLE ONLY consultorio.acuerdos_terapeuticos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.acuerdos_terapeuticos OWNER TO postgres;

--
-- Name: acuerdos_terapeuticos_id_acuerdo_terapeutico_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.acuerdos_terapeuticos_id_acuerdo_terapeutico_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.acuerdos_terapeuticos_id_acuerdo_terapeutico_seq OWNER TO postgres;

--
-- Name: acuerdos_terapeuticos_id_acuerdo_terapeutico_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.acuerdos_terapeuticos_id_acuerdo_terapeutico_seq OWNED BY consultorio.acuerdos_terapeuticos.id_acuerdo_terapeutico;


--
-- Name: anamnesis; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.anamnesis (
    id_anamnesis bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    tipo_anamnesis character varying(10) NOT NULL,
    nro_version smallint DEFAULT 1 NOT NULL,
    fec_consulta date NOT NULL,
    des_lugar_nacimiento text,
    des_domicilio text,
    des_informantes text,
    des_motivo_consulta text,
    des_antecedentes_fam_similares text,
    des_antecedentes_fam_patologicos text,
    des_componentes_familiares text,
    des_antecedentes_patologicos text,
    des_historia_rehabilitacion text,
    des_alimentacion text,
    des_sueno text,
    des_actividad_motriz text,
    des_actividad_emocional text,
    des_socializacion text,
    des_observaciones_entrevistador text,
    des_conclusion text,
    est_anamnesis boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT anamnesis_tipo_anamnesis_check CHECK (((tipo_anamnesis)::text = ANY (ARRAY[('INFANTIL'::character varying)::text, ('ADULTO'::character varying)::text])))
);

ALTER TABLE ONLY consultorio.anamnesis FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.anamnesis OWNER TO postgres;

--
-- Name: anamnesis_adulto_ext; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.anamnesis_adulto_ext (
    id_anamnesis_adulto_ext bigint NOT NULL,
    id_anamnesis bigint NOT NULL,
    id_empresa integer NOT NULL,
    des_nivel_instruccion character varying(20),
    des_profesion_ocupacion text,
    des_historia_familiar text,
    des_historia_academica text,
    des_historia_laboral text,
    des_actividad_sexual text,
    des_plan_evaluacion text,
    des_conclusiones text,
    CONSTRAINT anamnesis_adulto_ext_des_nivel_instruccion_check CHECK (((des_nivel_instruccion)::text = ANY (ARRAY[('PRIMARIO'::character varying)::text, ('SECUNDARIO'::character varying)::text, ('TERCIARIO'::character varying)::text, ('UNIVERSITARIO'::character varying)::text, ('POSGRADO'::character varying)::text])))
);

ALTER TABLE ONLY consultorio.anamnesis_adulto_ext FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.anamnesis_adulto_ext OWNER TO postgres;

--
-- Name: anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq OWNER TO postgres;

--
-- Name: anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq OWNED BY consultorio.anamnesis_adulto_ext.id_anamnesis_adulto_ext;


--
-- Name: anamnesis_id_anamnesis_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.anamnesis_id_anamnesis_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.anamnesis_id_anamnesis_seq OWNER TO postgres;

--
-- Name: anamnesis_id_anamnesis_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.anamnesis_id_anamnesis_seq OWNED BY consultorio.anamnesis.id_anamnesis;


--
-- Name: anamnesis_infantil_ext; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.anamnesis_infantil_ext (
    id_anamnesis_infantil_ext bigint NOT NULL,
    id_anamnesis bigint NOT NULL,
    id_empresa integer NOT NULL,
    des_nombre_madre text,
    des_ocupacion_madre text,
    tel_madre text,
    des_nombre_padre text,
    des_ocupacion_padre text,
    tel_padre text,
    des_colegio text,
    des_grado_escolar text,
    es_embarazo_planificado boolean,
    es_embarazo_controlado boolean,
    des_complicaciones_embarazo text,
    tipo_parto character varying(12),
    es_sufrimiento_fetal boolean,
    des_sufrimiento_fetal text,
    des_complicaciones_parto text,
    sem_gestacion smallint,
    apgar_min_1 smallint,
    apgar_min_5 smallint,
    peso_nacer_gramos integer,
    des_complicaciones_neonatales text,
    des_sueno_neonatal text,
    des_llanto_neonatal text,
    des_alimentacion_neonatal text,
    mes_control_cefalico smallint,
    es_control_cefalico_na boolean DEFAULT false NOT NULL,
    mes_control_tronco smallint,
    es_control_tronco_na boolean DEFAULT false NOT NULL,
    mes_gateo smallint,
    es_gateo_na boolean DEFAULT false NOT NULL,
    mes_bipedestacion smallint,
    es_bipedestacion_na boolean DEFAULT false NOT NULL,
    mes_camino smallint,
    es_camino_na boolean DEFAULT false NOT NULL,
    mes_primeras_palabras smallint,
    es_primeras_palabras_na boolean DEFAULT false NOT NULL,
    mes_habla_clara smallint,
    es_habla_clara_na boolean DEFAULT false NOT NULL,
    mes_control_esfinteres smallint,
    es_control_esfinteres_na boolean DEFAULT false NOT NULL,
    CONSTRAINT anamnesis_infantil_ext_apgar_min_1_check CHECK (((apgar_min_1 >= 0) AND (apgar_min_1 <= 10))),
    CONSTRAINT anamnesis_infantil_ext_apgar_min_5_check CHECK (((apgar_min_5 >= 0) AND (apgar_min_5 <= 10))),
    CONSTRAINT anamnesis_infantil_ext_tipo_parto_check CHECK (((tipo_parto)::text = ANY (ARRAY[('NATURAL'::character varying)::text, ('CESAREA'::character varying)::text, ('INSTRUMENTAL'::character varying)::text])))
);

ALTER TABLE ONLY consultorio.anamnesis_infantil_ext FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.anamnesis_infantil_ext OWNER TO postgres;

--
-- Name: anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq OWNER TO postgres;

--
-- Name: anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq OWNED BY consultorio.anamnesis_infantil_ext.id_anamnesis_infantil_ext;


--
-- Name: antecedentes_paciente; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.antecedentes_paciente (
    id_antecedente_paciente bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente bigint NOT NULL,
    des_antecedentes_personales text,
    des_antecedentes_familiares text,
    des_antecedentes_psicologicos text,
    des_alergias text,
    des_medicacion_actual text,
    cod_grupo_sanguineo text,
    des_observaciones text,
    est_antecedente_paciente boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    datos_especificos jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT antecedentes_paciente_cod_grupo_sanguineo_check CHECK ((cod_grupo_sanguineo = ANY (ARRAY['A+'::text, 'A-'::text, 'B+'::text, 'B-'::text, 'AB+'::text, 'AB-'::text, 'O+'::text, 'O-'::text])))
);

ALTER TABLE ONLY consultorio.antecedentes_paciente FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.antecedentes_paciente OWNER TO postgres;

--
-- Name: antecedentes_paciente_id_antecedente_paciente_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.antecedentes_paciente_id_antecedente_paciente_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.antecedentes_paciente_id_antecedente_paciente_seq OWNER TO postgres;

--
-- Name: antecedentes_paciente_id_antecedente_paciente_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.antecedentes_paciente_id_antecedente_paciente_seq OWNED BY consultorio.antecedentes_paciente.id_antecedente_paciente;


--
-- Name: cobros_simples; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.cobros_simples (
    id_cobro_simple bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_acuerdo bigint,
    monto numeric(18,0) NOT NULL,
    metodo_pago text DEFAULT 'EFECTIVO'::text NOT NULL,
    fec_cobro date DEFAULT CURRENT_DATE NOT NULL,
    nro_recibo_interno text,
    obs text,
    id_factura bigint,
    est_cobro_simple boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT ck_cobros_simples_metodo CHECK ((metodo_pago = ANY (ARRAY['EFECTIVO'::text, 'TRANSFERENCIA'::text, 'TARJETA'::text, 'CHEQUE'::text, 'OTRO'::text]))),
    CONSTRAINT cobros_simples_monto_check CHECK ((monto > (0)::numeric))
);

ALTER TABLE ONLY consultorio.cobros_simples FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.cobros_simples OWNER TO postgres;

--
-- Name: cobros_simples_id_cobro_simple_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.cobros_simples_id_cobro_simple_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.cobros_simples_id_cobro_simple_seq OWNER TO postgres;

--
-- Name: cobros_simples_id_cobro_simple_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.cobros_simples_id_cobro_simple_seq OWNED BY consultorio.cobros_simples.id_cobro_simple;


--
-- Name: consentimientos_firmados; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.consentimientos_firmados (
    id_consentimiento bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    des_tipo_consentimiento text NOT NULL,
    des_texto_consentimiento text NOT NULL,
    fec_firma date,
    des_nombre_firmante text,
    des_relacion_firmante text,
    des_observaciones text,
    est_consentimiento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.consentimientos_firmados FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.consentimientos_firmados OWNER TO postgres;

--
-- Name: consentimientos_firmados_id_consentimiento_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.consentimientos_firmados_id_consentimiento_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.consentimientos_firmados_id_consentimiento_seq OWNER TO postgres;

--
-- Name: consentimientos_firmados_id_consentimiento_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.consentimientos_firmados_id_consentimiento_seq OWNED BY consultorio.consentimientos_firmados.id_consentimiento;


--
-- Name: contratos_tratamiento; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.contratos_tratamiento (
    id_contrato_tratamiento bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    id_episodio_apertura bigint,
    id_contrato_anterior bigint,
    nro_contrato bigint NOT NULL,
    cod_estado_contrato text DEFAULT 'BORRADOR'::text NOT NULL,
    des_objetivo_general text,
    des_condiciones text,
    nro_sesiones_pactadas smallint NOT NULL,
    nro_sesiones_realizadas smallint DEFAULT 0 NOT NULL,
    val_precio_sesion numeric(18,2),
    val_total_contrato numeric(18,2),
    fec_firma date,
    fec_inicio date,
    fec_vencimiento date,
    est_contrato_tratamiento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT contratos_tratamiento_check CHECK ((nro_sesiones_realizadas <= nro_sesiones_pactadas)),
    CONSTRAINT contratos_tratamiento_cod_estado_contrato_check CHECK ((cod_estado_contrato = ANY (ARRAY['BORRADOR'::text, 'ACTIVO'::text, 'PAUSADO'::text, 'COMPLETADO'::text, 'CANCELADO'::text]))),
    CONSTRAINT contratos_tratamiento_nro_sesiones_pactadas_check CHECK ((nro_sesiones_pactadas > 0)),
    CONSTRAINT contratos_tratamiento_nro_sesiones_realizadas_check CHECK ((nro_sesiones_realizadas >= 0))
);

ALTER TABLE ONLY consultorio.contratos_tratamiento FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.contratos_tratamiento OWNER TO postgres;

--
-- Name: contratos_tratamiento_acuerdos_pago; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.contratos_tratamiento_acuerdos_pago (
    id_acuerdo_pago bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_contrato_tratamiento bigint NOT NULL,
    id_modalidad_pago bigint NOT NULL,
    val_acordado numeric(18,2) NOT NULL,
    fec_acuerdo date DEFAULT CURRENT_DATE NOT NULL,
    des_observaciones text,
    est_acuerdo_pago boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT contratos_tratamiento_acuerdos_pago_val_acordado_check CHECK ((val_acordado >= (0)::numeric))
);

ALTER TABLE ONLY consultorio.contratos_tratamiento_acuerdos_pago FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.contratos_tratamiento_acuerdos_pago OWNER TO postgres;

--
-- Name: contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq OWNER TO postgres;

--
-- Name: contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq OWNED BY consultorio.contratos_tratamiento_acuerdos_pago.id_acuerdo_pago;


--
-- Name: contratos_tratamiento_id_contrato_tratamiento_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.contratos_tratamiento_id_contrato_tratamiento_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.contratos_tratamiento_id_contrato_tratamiento_seq OWNER TO postgres;

--
-- Name: contratos_tratamiento_id_contrato_tratamiento_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.contratos_tratamiento_id_contrato_tratamiento_seq OWNED BY consultorio.contratos_tratamiento.id_contrato_tratamiento;


--
-- Name: contratos_tratamiento_modalidades_pago; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.contratos_tratamiento_modalidades_pago (
    id_modalidad_pago bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_contrato_tratamiento bigint NOT NULL,
    des_modalidad text NOT NULL,
    cod_tipo_modalidad text DEFAULT 'POR_SESION'::text NOT NULL,
    nro_sesiones_modalidad smallint,
    val_precio_modalidad numeric(18,2) NOT NULL,
    val_porcentaje_descuento numeric(5,2) DEFAULT 0 NOT NULL,
    est_modalidad_pago boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT contratos_tratamiento_modalidade_val_porcentaje_descuento_check CHECK ((val_porcentaje_descuento >= (0)::numeric)),
    CONSTRAINT contratos_tratamiento_modalidades__nro_sesiones_modalidad_check CHECK ((nro_sesiones_modalidad > 0)),
    CONSTRAINT contratos_tratamiento_modalidades_pa_val_precio_modalidad_check CHECK ((val_precio_modalidad >= (0)::numeric)),
    CONSTRAINT contratos_tratamiento_modalidades_pago_cod_tipo_modalidad_check CHECK ((cod_tipo_modalidad = ANY (ARRAY['POR_SESION'::text, 'PAQUETE'::text, 'TOTAL_ANTICIPADO'::text])))
);

ALTER TABLE ONLY consultorio.contratos_tratamiento_modalidades_pago FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.contratos_tratamiento_modalidades_pago OWNER TO postgres;

--
-- Name: contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq OWNER TO postgres;

--
-- Name: contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq OWNED BY consultorio.contratos_tratamiento_modalidades_pago.id_modalidad_pago;


--
-- Name: contratos_tratamiento_pagos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.contratos_tratamiento_pagos (
    id_pago bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_contrato_tratamiento bigint NOT NULL,
    id_acuerdo_pago bigint NOT NULL,
    val_monto numeric(18,2) NOT NULL,
    cod_forma_pago text DEFAULT 'EFECTIVO'::text NOT NULL,
    fec_pago date DEFAULT CURRENT_DATE NOT NULL,
    des_referencia text,
    des_observaciones text,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_factura bigint,
    CONSTRAINT contratos_tratamiento_pagos_cod_forma_pago_check CHECK ((cod_forma_pago = ANY (ARRAY['EFECTIVO'::text, 'TRANSFERENCIA'::text, 'TARJETA_DEBITO'::text, 'TARJETA_CREDITO'::text, 'CHEQUE'::text, 'OTRO'::text])))
);

ALTER TABLE ONLY consultorio.contratos_tratamiento_pagos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.contratos_tratamiento_pagos OWNER TO postgres;

--
-- Name: contratos_tratamiento_pagos_id_pago_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.contratos_tratamiento_pagos_id_pago_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.contratos_tratamiento_pagos_id_pago_seq OWNER TO postgres;

--
-- Name: contratos_tratamiento_pagos_id_pago_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.contratos_tratamiento_pagos_id_pago_seq OWNED BY consultorio.contratos_tratamiento_pagos.id_pago;


--
-- Name: contratos_tratamiento_sesiones; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.contratos_tratamiento_sesiones (
    id_contrato_sesion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_contrato_tratamiento bigint NOT NULL,
    nro_sesion smallint NOT NULL,
    id_cita bigint,
    id_cita_anterior bigint,
    id_episodio bigint,
    cod_estado_sesion text DEFAULT 'PROGRAMADA'::text NOT NULL,
    fec_sesion_programada date,
    des_observaciones text,
    est_contrato_sesion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT contratos_tratamiento_sesiones_cod_estado_sesion_check CHECK ((cod_estado_sesion = ANY (ARRAY['PROGRAMADA'::text, 'REALIZADA'::text, 'AUSENTE_JUSTIFICADO'::text, 'AUSENTE_SIN_AVISO'::text, 'CANCELADA'::text]))),
    CONSTRAINT contratos_tratamiento_sesiones_nro_sesion_check CHECK ((nro_sesion > 0))
);

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.contratos_tratamiento_sesiones OWNER TO postgres;

--
-- Name: contratos_tratamiento_sesiones_id_contrato_sesion_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.contratos_tratamiento_sesiones_id_contrato_sesion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.contratos_tratamiento_sesiones_id_contrato_sesion_seq OWNER TO postgres;

--
-- Name: contratos_tratamiento_sesiones_id_contrato_sesion_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.contratos_tratamiento_sesiones_id_contrato_sesion_seq OWNED BY consultorio.contratos_tratamiento_sesiones.id_contrato_sesion;


--
-- Name: derivaciones; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.derivaciones (
    id_derivacion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    des_especialidad_destino text NOT NULL,
    des_profesional_destino text,
    des_motivo_derivacion text NOT NULL,
    des_observaciones text,
    cod_estado_derivacion text DEFAULT 'EMITIDA'::text NOT NULL,
    fec_emision date DEFAULT CURRENT_DATE NOT NULL,
    est_derivacion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_tipo_derivacion text DEFAULT 'EXTERNA'::text NOT NULL,
    id_especialista_destino integer,
    CONSTRAINT derivaciones_cod_estado_derivacion_check CHECK ((cod_estado_derivacion = ANY (ARRAY['EMITIDA'::text, 'ACEPTADA'::text, 'RECHAZADA'::text, 'COMPLETADA'::text, 'CANCELADA'::text]))),
    CONSTRAINT derivaciones_cod_tipo_derivacion_check CHECK ((cod_tipo_derivacion = ANY (ARRAY['INTERNA'::text, 'EXTERNA'::text])))
);

ALTER TABLE ONLY consultorio.derivaciones FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.derivaciones OWNER TO postgres;

--
-- Name: derivaciones_id_derivacion_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.derivaciones_id_derivacion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.derivaciones_id_derivacion_seq OWNER TO postgres;

--
-- Name: derivaciones_id_derivacion_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.derivaciones_id_derivacion_seq OWNED BY consultorio.derivaciones.id_derivacion;


--
-- Name: diagnosticos_cie10; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.diagnosticos_cie10 (
    id_diagnostico_cie10 integer NOT NULL,
    codigo text NOT NULL,
    des_diagnostico text NOT NULL,
    des_capitulo text,
    des_bloque text,
    est_diagnostico_cie10 boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE consultorio.diagnosticos_cie10 OWNER TO postgres;

--
-- Name: diagnosticos_cie10_dsm5_equivalencias; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.diagnosticos_cie10_dsm5_equivalencias (
    id_equivalencia integer NOT NULL,
    id_diagnostico_cie10 integer NOT NULL,
    id_diagnostico_dsm5 integer NOT NULL,
    est_equivalencia boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE consultorio.diagnosticos_cie10_dsm5_equivalencias OWNER TO postgres;

--
-- Name: diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq OWNER TO postgres;

--
-- Name: diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq OWNED BY consultorio.diagnosticos_cie10_dsm5_equivalencias.id_equivalencia;


--
-- Name: diagnosticos_cie10_id_diagnostico_cie10_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.diagnosticos_cie10_id_diagnostico_cie10_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.diagnosticos_cie10_id_diagnostico_cie10_seq OWNER TO postgres;

--
-- Name: diagnosticos_cie10_id_diagnostico_cie10_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.diagnosticos_cie10_id_diagnostico_cie10_seq OWNED BY consultorio.diagnosticos_cie10.id_diagnostico_cie10;


--
-- Name: diagnosticos_dsm5; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.diagnosticos_dsm5 (
    id_diagnostico_dsm5 integer NOT NULL,
    codigo text NOT NULL,
    des_diagnostico text NOT NULL,
    des_categoria text,
    des_especificadores text,
    est_diagnostico_dsm5 boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE consultorio.diagnosticos_dsm5 OWNER TO postgres;

--
-- Name: diagnosticos_dsm5_id_diagnostico_dsm5_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.diagnosticos_dsm5_id_diagnostico_dsm5_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.diagnosticos_dsm5_id_diagnostico_dsm5_seq OWNER TO postgres;

--
-- Name: diagnosticos_dsm5_id_diagnostico_dsm5_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.diagnosticos_dsm5_id_diagnostico_dsm5_seq OWNED BY consultorio.diagnosticos_dsm5.id_diagnostico_dsm5;


--
-- Name: documentos_adjuntos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.documentos_adjuntos (
    id_documento_adjunto bigint NOT NULL,
    id_empresa integer NOT NULL,
    cod_tipo_entidad text NOT NULL,
    id_entidad bigint NOT NULL,
    des_nombre_archivo text NOT NULL,
    des_ruta_almacenamiento text NOT NULL,
    des_tipo_mime text,
    val_tamanio_bytes bigint,
    des_descripcion text,
    est_documento_adjunto boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT documentos_adjuntos_cod_tipo_entidad_check CHECK ((cod_tipo_entidad = ANY (ARRAY['EPISODIO'::text, 'FICHA_CLINICA'::text, 'RECETA'::text, 'JUSTIFICATIVO'::text, 'ORDEN_ESTUDIOS'::text, 'ORDEN_ANALISIS'::text, 'RESULTADO_ANALISIS'::text, 'CONSENTIMIENTO'::text, 'DERIVACION'::text, 'PLAN_TRATAMIENTO'::text, 'CONTRATO_TRATAMIENTO'::text])))
);

ALTER TABLE ONLY consultorio.documentos_adjuntos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.documentos_adjuntos OWNER TO postgres;

--
-- Name: documentos_adjuntos_id_documento_adjunto_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.documentos_adjuntos_id_documento_adjunto_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.documentos_adjuntos_id_documento_adjunto_seq OWNER TO postgres;

--
-- Name: documentos_adjuntos_id_documento_adjunto_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.documentos_adjuntos_id_documento_adjunto_seq OWNED BY consultorio.documentos_adjuntos.id_documento_adjunto;


--
-- Name: empresa_perfil_clinico; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.empresa_perfil_clinico (
    id_empresa_perfil_clinico integer NOT NULL,
    id_empresa integer NOT NULL,
    cod_tipo_clinico character varying(30) NOT NULL,
    est_perfil_clinico boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.empresa_perfil_clinico FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.empresa_perfil_clinico OWNER TO postgres;

--
-- Name: empresa_perfil_clinico_id_empresa_perfil_clinico_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.empresa_perfil_clinico_id_empresa_perfil_clinico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.empresa_perfil_clinico_id_empresa_perfil_clinico_seq OWNER TO postgres;

--
-- Name: empresa_perfil_clinico_id_empresa_perfil_clinico_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.empresa_perfil_clinico_id_empresa_perfil_clinico_seq OWNED BY consultorio.empresa_perfil_clinico.id_empresa_perfil_clinico;


--
-- Name: episodio_diagnosticos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.episodio_diagnosticos (
    id_episodio_diagnostico bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_diagnostico_cie10 integer,
    id_diagnostico_dsm5 integer,
    cod_tipo_diagnostico text DEFAULT 'PRINCIPAL'::text NOT NULL,
    es_cronico boolean DEFAULT false NOT NULL,
    des_observacion text,
    est_episodio_diagnostico boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT episodio_diagnosticos_check CHECK (((id_diagnostico_cie10 IS NOT NULL) OR (id_diagnostico_dsm5 IS NOT NULL))),
    CONSTRAINT episodio_diagnosticos_cod_tipo_diagnostico_check CHECK ((cod_tipo_diagnostico = ANY (ARRAY['PRINCIPAL'::text, 'SECUNDARIO'::text, 'PRESUNTIVO'::text, 'DEFINITIVO'::text, 'DESCARTADO'::text])))
);

ALTER TABLE ONLY consultorio.episodio_diagnosticos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.episodio_diagnosticos OWNER TO postgres;

--
-- Name: episodio_diagnosticos_id_episodio_diagnostico_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.episodio_diagnosticos_id_episodio_diagnostico_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.episodio_diagnosticos_id_episodio_diagnostico_seq OWNER TO postgres;

--
-- Name: episodio_diagnosticos_id_episodio_diagnostico_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.episodio_diagnosticos_id_episodio_diagnostico_seq OWNED BY consultorio.episodio_diagnosticos.id_episodio_diagnostico;


--
-- Name: episodio_procedimientos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.episodio_procedimientos (
    id_episodio_procedimiento bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_procedimiento_empresa integer NOT NULL,
    nro_orden smallint DEFAULT 1 NOT NULL,
    des_observaciones text,
    est_episodio_procedimiento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT episodio_procedimientos_nro_orden_check CHECK ((nro_orden > 0))
);

ALTER TABLE ONLY consultorio.episodio_procedimientos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.episodio_procedimientos OWNER TO postgres;

--
-- Name: episodio_procedimientos_id_episodio_procedimiento_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.episodio_procedimientos_id_episodio_procedimiento_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.episodio_procedimientos_id_episodio_procedimiento_seq OWNER TO postgres;

--
-- Name: episodio_procedimientos_id_episodio_procedimiento_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.episodio_procedimientos_id_episodio_procedimiento_seq OWNED BY consultorio.episodio_procedimientos.id_episodio_procedimiento;


--
-- Name: episodio_procedimientos_insumos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.episodio_procedimientos_insumos (
    id_ep_insumo bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio_procedimiento bigint NOT NULL,
    id_insumo_empresa integer NOT NULL,
    val_cantidad numeric(10,3) DEFAULT 1 NOT NULL,
    des_observacion text,
    est_ep_insumo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT episodio_procedimientos_insumos_val_cantidad_check CHECK ((val_cantidad > (0)::numeric))
);

ALTER TABLE ONLY consultorio.episodio_procedimientos_insumos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.episodio_procedimientos_insumos OWNER TO postgres;

--
-- Name: episodio_procedimientos_insumos_id_ep_insumo_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.episodio_procedimientos_insumos_id_ep_insumo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.episodio_procedimientos_insumos_id_ep_insumo_seq OWNER TO postgres;

--
-- Name: episodio_procedimientos_insumos_id_ep_insumo_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.episodio_procedimientos_insumos_id_ep_insumo_seq OWNED BY consultorio.episodio_procedimientos_insumos.id_ep_insumo;


--
-- Name: episodios; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.episodios (
    id_episodio bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_episodio_empresa bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    id_especialidad integer NOT NULL,
    id_cita bigint,
    id_episodio_origen bigint,
    cod_estado_episodio text DEFAULT 'EN_SALA'::text NOT NULL,
    cod_modalidad_atencion text DEFAULT 'PRESENCIAL'::text NOT NULL,
    fec_apertura timestamp with time zone DEFAULT now() NOT NULL,
    fec_inicio_consulta timestamp with time zone,
    fec_cierre timestamp with time zone,
    des_motivo_consulta text,
    est_episodio boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT episodios_cod_estado_episodio_check CHECK ((cod_estado_episodio = ANY (ARRAY['EN_SALA'::text, 'EN_CONSULTA'::text, 'CERRADO'::text, 'ANULADO'::text]))),
    CONSTRAINT episodios_cod_modalidad_atencion_check CHECK ((cod_modalidad_atencion = ANY (ARRAY['PRESENCIAL'::text, 'DOMICILIO'::text, 'TELEMEDICINA'::text])))
);

ALTER TABLE ONLY consultorio.episodios FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.episodios OWNER TO postgres;

--
-- Name: episodios_id_episodio_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.episodios_id_episodio_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.episodios_id_episodio_seq OWNER TO postgres;

--
-- Name: episodios_id_episodio_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.episodios_id_episodio_seq OWNED BY consultorio.episodios.id_episodio;


--
-- Name: fichas_clinicas; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.fichas_clinicas (
    id_ficha_clinica bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_formulario_definicion integer,
    des_anamnesis text,
    des_examen_fisico text,
    des_plan_terapeutico text,
    des_indicaciones text,
    des_respuestas_preconsulta jsonb,
    est_ficha_clinica boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.fichas_clinicas FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.fichas_clinicas OWNER TO postgres;

--
-- Name: fichas_clinicas_id_ficha_clinica_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.fichas_clinicas_id_ficha_clinica_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.fichas_clinicas_id_ficha_clinica_seq OWNER TO postgres;

--
-- Name: fichas_clinicas_id_ficha_clinica_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.fichas_clinicas_id_ficha_clinica_seq OWNED BY consultorio.fichas_clinicas.id_ficha_clinica;


--
-- Name: fichas_psicologia; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.fichas_psicologia (
    id_ficha_psicologia bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_ficha_clinica bigint NOT NULL,
    des_estado_mental text,
    des_observaciones_conductuales text,
    des_tecnicas_utilizadas text,
    des_temas_abordados text,
    des_tarea_terapeutica text,
    des_evolucion_sesion text,
    cod_estado_emocional_paciente text,
    es_sesion_crisis boolean DEFAULT false NOT NULL,
    est_ficha_psicologia boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    des_anamnesis text,
    CONSTRAINT fichas_psicologia_cod_estado_emocional_paciente_check CHECK ((cod_estado_emocional_paciente = ANY (ARRAY['ESTABLE'::text, 'ANSIOSO'::text, 'DEPRIMIDO'::text, 'IRRITABLE'::text, 'EUFÓRICO'::text, 'FLUCTUANTE'::text, 'OTRO'::text])))
);

ALTER TABLE ONLY consultorio.fichas_psicologia FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.fichas_psicologia OWNER TO postgres;

--
-- Name: COLUMN fichas_psicologia.des_anamnesis; Type: COMMENT; Schema: consultorio; Owner: postgres
--

COMMENT ON COLUMN consultorio.fichas_psicologia.des_anamnesis IS 'Anamnesis / Historia del problema actual. C??mo inici??, evoluci??n, contexto, tratamientos previos.';


--
-- Name: fichas_psicologia_id_ficha_psicologia_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.fichas_psicologia_id_ficha_psicologia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.fichas_psicologia_id_ficha_psicologia_seq OWNER TO postgres;

--
-- Name: fichas_psicologia_id_ficha_psicologia_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.fichas_psicologia_id_ficha_psicologia_seq OWNED BY consultorio.fichas_psicologia.id_ficha_psicologia;


--
-- Name: formularios_definicion; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.formularios_definicion (
    id_formulario_definicion integer NOT NULL,
    id_empresa integer NOT NULL,
    des_formulario text NOT NULL,
    cod_especialidad text,
    des_estructura jsonb DEFAULT '{"campos": []}'::jsonb NOT NULL,
    est_formulario_definicion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_tipo_formulario text DEFAULT 'PRECONSULTA'::text NOT NULL,
    CONSTRAINT formularios_definicion_cod_tipo_formulario_check CHECK ((cod_tipo_formulario = ANY (ARRAY['PRECONSULTA'::text, 'ANTECEDENTES'::text])))
);

ALTER TABLE ONLY consultorio.formularios_definicion FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.formularios_definicion OWNER TO postgres;

--
-- Name: formularios_definicion_id_formulario_definicion_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.formularios_definicion_id_formulario_definicion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.formularios_definicion_id_formulario_definicion_seq OWNER TO postgres;

--
-- Name: formularios_definicion_id_formulario_definicion_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.formularios_definicion_id_formulario_definicion_seq OWNED BY consultorio.formularios_definicion.id_formulario_definicion;


--
-- Name: indicaciones_no_farmacologicas; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.indicaciones_no_farmacologicas (
    id_indicacion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    cod_tipo_indicacion text DEFAULT 'GENERAL'::text NOT NULL,
    nro_orden smallint DEFAULT 1 NOT NULL,
    des_indicacion text NOT NULL,
    est_indicacion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT indicaciones_no_farmacologicas_cod_tipo_indicacion_check CHECK ((cod_tipo_indicacion = ANY (ARRAY['GENERAL'::text, 'DIETA'::text, 'EJERCICIO'::text, 'REPOSO'::text, 'PSICOLOGICA'::text, 'OTRO'::text]))),
    CONSTRAINT indicaciones_no_farmacologicas_nro_orden_check CHECK ((nro_orden > 0))
);

ALTER TABLE ONLY consultorio.indicaciones_no_farmacologicas FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.indicaciones_no_farmacologicas OWNER TO postgres;

--
-- Name: indicaciones_no_farmacologicas_id_indicacion_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.indicaciones_no_farmacologicas_id_indicacion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.indicaciones_no_farmacologicas_id_indicacion_seq OWNER TO postgres;

--
-- Name: indicaciones_no_farmacologicas_id_indicacion_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.indicaciones_no_farmacologicas_id_indicacion_seq OWNED BY consultorio.indicaciones_no_farmacologicas.id_indicacion;


--
-- Name: insumos_empresa; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.insumos_empresa (
    id_insumo_empresa integer NOT NULL,
    id_empresa integer NOT NULL,
    cod_insumo text,
    des_insumo text NOT NULL,
    des_unidad_medida text,
    es_controlado_stock boolean DEFAULT false NOT NULL,
    est_insumo_empresa boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.insumos_empresa FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.insumos_empresa OWNER TO postgres;

--
-- Name: insumos_empresa_id_insumo_empresa_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.insumos_empresa_id_insumo_empresa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.insumos_empresa_id_insumo_empresa_seq OWNER TO postgres;

--
-- Name: insumos_empresa_id_insumo_empresa_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.insumos_empresa_id_insumo_empresa_seq OWNED BY consultorio.insumos_empresa.id_insumo_empresa;


--
-- Name: justificativos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.justificativos (
    id_justificativo bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    id_tipo_justificativo integer NOT NULL,
    id_plantilla_justificativo integer,
    id_justificativo_origen bigint,
    nro_documento bigint NOT NULL,
    cod_estado_justificativo text DEFAULT 'BORRADOR'::text NOT NULL,
    fec_emision date,
    fec_inicio_reposo date,
    fec_fin_reposo date,
    nro_dias_reposo smallint,
    des_diagnostico text,
    des_resultado_aptitud text,
    des_cuerpo_generado text,
    des_observaciones text,
    est_justificativo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT justificativos_cod_estado_justificativo_check CHECK ((cod_estado_justificativo = ANY (ARRAY['BORRADOR'::text, 'EMITIDO'::text, 'ANULADO'::text]))),
    CONSTRAINT justificativos_nro_dias_reposo_check CHECK ((nro_dias_reposo > 0))
);

ALTER TABLE ONLY consultorio.justificativos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.justificativos OWNER TO postgres;

--
-- Name: justificativos_id_justificativo_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.justificativos_id_justificativo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.justificativos_id_justificativo_seq OWNER TO postgres;

--
-- Name: justificativos_id_justificativo_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.justificativos_id_justificativo_seq OWNED BY consultorio.justificativos.id_justificativo;


--
-- Name: medicamentos_empresa; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.medicamentos_empresa (
    id_medicamento_empresa integer NOT NULL,
    id_empresa integer NOT NULL,
    des_medicamento text NOT NULL,
    des_principio_activo text,
    des_concentracion text,
    des_forma_farmaceutica text,
    es_psicofarmaco boolean DEFAULT false NOT NULL,
    est_medicamento_empresa boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.medicamentos_empresa FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.medicamentos_empresa OWNER TO postgres;

--
-- Name: medicamentos_empresa_id_medicamento_empresa_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.medicamentos_empresa_id_medicamento_empresa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.medicamentos_empresa_id_medicamento_empresa_seq OWNER TO postgres;

--
-- Name: medicamentos_empresa_id_medicamento_empresa_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.medicamentos_empresa_id_medicamento_empresa_seq OWNED BY consultorio.medicamentos_empresa.id_medicamento_empresa;


--
-- Name: notas_evolucion; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.notas_evolucion (
    id_nota_evolucion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_plan_tratamiento bigint,
    cod_tipo_nota text DEFAULT 'EVOLUCION'::text NOT NULL,
    fec_nota timestamp with time zone DEFAULT now() NOT NULL,
    des_nota text NOT NULL,
    est_nota_evolucion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT notas_evolucion_cod_tipo_nota_check CHECK ((cod_tipo_nota = ANY (ARRAY['EVOLUCION'::text, 'ADDENDUM'::text, 'OBSERVACION'::text])))
);

ALTER TABLE ONLY consultorio.notas_evolucion FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.notas_evolucion OWNER TO postgres;

--
-- Name: notas_evolucion_id_nota_evolucion_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.notas_evolucion_id_nota_evolucion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.notas_evolucion_id_nota_evolucion_seq OWNER TO postgres;

--
-- Name: notas_evolucion_id_nota_evolucion_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.notas_evolucion_id_nota_evolucion_seq OWNED BY consultorio.notas_evolucion.id_nota_evolucion;


--
-- Name: ordenes_analisis; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.ordenes_analisis (
    id_orden_analisis bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    id_orden_analisis_origen bigint,
    nro_documento bigint NOT NULL,
    cod_estado_orden text DEFAULT 'EMITIDA'::text NOT NULL,
    fec_emision date DEFAULT CURRENT_DATE NOT NULL,
    des_indicacion_clinica text,
    des_observaciones text,
    est_orden_analisis boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT ordenes_analisis_cod_estado_orden_check CHECK ((cod_estado_orden = ANY (ARRAY['EMITIDA'::text, 'CANCELADA'::text, 'CON_RESULTADO'::text])))
);

ALTER TABLE ONLY consultorio.ordenes_analisis FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.ordenes_analisis OWNER TO postgres;

--
-- Name: ordenes_analisis_detalle; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.ordenes_analisis_detalle (
    id_orden_analisis_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_orden_analisis bigint NOT NULL,
    nro_orden smallint DEFAULT 1 NOT NULL,
    des_analisis text NOT NULL,
    des_observaciones_tecnicas text,
    est_orden_analisis_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT ordenes_analisis_detalle_nro_orden_check CHECK ((nro_orden > 0))
);

ALTER TABLE ONLY consultorio.ordenes_analisis_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.ordenes_analisis_detalle OWNER TO postgres;

--
-- Name: ordenes_analisis_detalle_id_orden_analisis_detalle_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.ordenes_analisis_detalle_id_orden_analisis_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.ordenes_analisis_detalle_id_orden_analisis_detalle_seq OWNER TO postgres;

--
-- Name: ordenes_analisis_detalle_id_orden_analisis_detalle_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.ordenes_analisis_detalle_id_orden_analisis_detalle_seq OWNED BY consultorio.ordenes_analisis_detalle.id_orden_analisis_detalle;


--
-- Name: ordenes_analisis_id_orden_analisis_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.ordenes_analisis_id_orden_analisis_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.ordenes_analisis_id_orden_analisis_seq OWNER TO postgres;

--
-- Name: ordenes_analisis_id_orden_analisis_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.ordenes_analisis_id_orden_analisis_seq OWNED BY consultorio.ordenes_analisis.id_orden_analisis;


--
-- Name: ordenes_estudios; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.ordenes_estudios (
    id_orden_estudios bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    id_orden_estudios_origen bigint,
    nro_documento bigint NOT NULL,
    cod_estado_orden text DEFAULT 'EMITIDA'::text NOT NULL,
    fec_emision date DEFAULT CURRENT_DATE NOT NULL,
    des_indicacion_clinica text,
    des_observaciones text,
    est_orden_estudios boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT ordenes_estudios_cod_estado_orden_check CHECK ((cod_estado_orden = ANY (ARRAY['EMITIDA'::text, 'CANCELADA'::text, 'CON_RESULTADO'::text])))
);

ALTER TABLE ONLY consultorio.ordenes_estudios FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.ordenes_estudios OWNER TO postgres;

--
-- Name: ordenes_estudios_detalle; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.ordenes_estudios_detalle (
    id_orden_estudios_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_orden_estudios bigint NOT NULL,
    nro_orden smallint DEFAULT 1 NOT NULL,
    des_estudio text NOT NULL,
    des_region_anatomica text,
    des_observaciones_tecnicas text,
    est_orden_estudios_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT ordenes_estudios_detalle_nro_orden_check CHECK ((nro_orden > 0))
);

ALTER TABLE ONLY consultorio.ordenes_estudios_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.ordenes_estudios_detalle OWNER TO postgres;

--
-- Name: ordenes_estudios_detalle_id_orden_estudios_detalle_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.ordenes_estudios_detalle_id_orden_estudios_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.ordenes_estudios_detalle_id_orden_estudios_detalle_seq OWNER TO postgres;

--
-- Name: ordenes_estudios_detalle_id_orden_estudios_detalle_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.ordenes_estudios_detalle_id_orden_estudios_detalle_seq OWNED BY consultorio.ordenes_estudios_detalle.id_orden_estudios_detalle;


--
-- Name: ordenes_estudios_id_orden_estudios_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.ordenes_estudios_id_orden_estudios_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.ordenes_estudios_id_orden_estudios_seq OWNER TO postgres;

--
-- Name: ordenes_estudios_id_orden_estudios_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.ordenes_estudios_id_orden_estudios_seq OWNED BY consultorio.ordenes_estudios.id_orden_estudios;


--
-- Name: paciente_tokens; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.paciente_tokens (
    id_paciente_token bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente bigint NOT NULL,
    des_token text NOT NULL,
    cod_tipo_acceso text DEFAULT 'LECTURA'::text NOT NULL,
    cod_estado_token text DEFAULT 'ACTIVO'::text NOT NULL,
    fec_expiracion timestamp with time zone NOT NULL,
    fec_uso timestamp with time zone,
    est_paciente_token boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT paciente_tokens_cod_estado_token_check CHECK ((cod_estado_token = ANY (ARRAY['ACTIVO'::text, 'USADO'::text, 'EXPIRADO'::text, 'REVOCADO'::text]))),
    CONSTRAINT paciente_tokens_cod_tipo_acceso_check CHECK ((cod_tipo_acceso = ANY (ARRAY['LECTURA'::text, 'FORMULARIO'::text])))
);

ALTER TABLE ONLY consultorio.paciente_tokens FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.paciente_tokens OWNER TO postgres;

--
-- Name: paciente_tokens_id_paciente_token_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.paciente_tokens_id_paciente_token_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.paciente_tokens_id_paciente_token_seq OWNER TO postgres;

--
-- Name: paciente_tokens_id_paciente_token_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.paciente_tokens_id_paciente_token_seq OWNED BY consultorio.paciente_tokens.id_paciente_token;


--
-- Name: pei; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei (
    id_pei bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    id_cotratante integer,
    id_pei_anterior bigint,
    fec_inicio date NOT NULL,
    des_escolarizacion_inicio text,
    areas_intervencion text[] DEFAULT '{}'::text[] NOT NULL,
    tipos_programa text[] DEFAULT '{}'::text[] NOT NULL,
    des_diagnostico_presuntivo text,
    des_tiempo_estimado text,
    sesiones_semanales smallint,
    des_repertorio_inicio text,
    des_notas text,
    est_pei boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.pei FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei OWNER TO postgres;

--
-- Name: pei_calendario_eventos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_calendario_eventos (
    id_pei_calendario_evento bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei bigint NOT NULL,
    cod_tipo_evento character varying(25) NOT NULL,
    fec_evento date NOT NULL,
    des_notas text,
    es_genera_cobro boolean DEFAULT false NOT NULL,
    cod_estado_evento character varying(10) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    CONSTRAINT pei_calendario_eventos_cod_estado_evento_check CHECK (((cod_estado_evento)::text = ANY (ARRAY[('PENDIENTE'::character varying)::text, ('REALIZADO'::character varying)::text, ('CANCELADO'::character varying)::text]))),
    CONSTRAINT pei_calendario_eventos_cod_tipo_evento_check CHECK (((cod_tipo_evento)::text = ANY (ARRAY[('REEVALUACION'::character varying)::text, ('REUNION_CLINICA'::character varying)::text, ('ENTREVISTA_PADRES'::character varying)::text, ('ENTREVISTA_COLEGIO'::character varying)::text])))
);

ALTER TABLE ONLY consultorio.pei_calendario_eventos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_calendario_eventos OWNER TO postgres;

--
-- Name: pei_calendario_eventos_id_pei_calendario_evento_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_calendario_eventos_id_pei_calendario_evento_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_calendario_eventos_id_pei_calendario_evento_seq OWNER TO postgres;

--
-- Name: pei_calendario_eventos_id_pei_calendario_evento_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_calendario_eventos_id_pei_calendario_evento_seq OWNED BY consultorio.pei_calendario_eventos.id_pei_calendario_evento;


--
-- Name: pei_estrategias; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_estrategias (
    id_pei_estrategia bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei bigint NOT NULL,
    nro_orden smallint NOT NULL,
    des_estrategia text NOT NULL,
    est_pei_estrategia boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.pei_estrategias FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_estrategias OWNER TO postgres;

--
-- Name: pei_estrategias_id_pei_estrategia_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_estrategias_id_pei_estrategia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_estrategias_id_pei_estrategia_seq OWNER TO postgres;

--
-- Name: pei_estrategias_id_pei_estrategia_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_estrategias_id_pei_estrategia_seq OWNED BY consultorio.pei_estrategias.id_pei_estrategia;


--
-- Name: pei_habilidades_entrenamiento; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_habilidades_entrenamiento (
    id_pei_habilidad bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei_registro_mensual bigint NOT NULL,
    des_habilidad text NOT NULL,
    cod_estado character varying(10) DEFAULT 'EN_CURSO'::character varying NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    CONSTRAINT pei_habilidades_entrenamiento_cod_estado_check CHECK (((cod_estado)::text = ANY (ARRAY[('EN_CURSO'::character varying)::text, ('LOGRADA'::character varying)::text, ('PAUSADA'::character varying)::text, ('CANCELADA'::character varying)::text])))
);

ALTER TABLE ONLY consultorio.pei_habilidades_entrenamiento FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_habilidades_entrenamiento OWNER TO postgres;

--
-- Name: pei_habilidades_entrenamiento_id_pei_habilidad_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_habilidades_entrenamiento_id_pei_habilidad_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_habilidades_entrenamiento_id_pei_habilidad_seq OWNER TO postgres;

--
-- Name: pei_habilidades_entrenamiento_id_pei_habilidad_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_habilidades_entrenamiento_id_pei_habilidad_seq OWNED BY consultorio.pei_habilidades_entrenamiento.id_pei_habilidad;


--
-- Name: pei_id_pei_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_id_pei_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_id_pei_seq OWNER TO postgres;

--
-- Name: pei_id_pei_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_id_pei_seq OWNED BY consultorio.pei.id_pei;


--
-- Name: pei_objetivos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_objetivos (
    id_pei_objetivo bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei bigint NOT NULL,
    nro_orden smallint NOT NULL,
    des_objetivo text NOT NULL,
    cod_estado character varying(10) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    fec_logro date,
    est_pei_objetivo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    CONSTRAINT pei_objetivos_cod_estado_check CHECK (((cod_estado)::text = ANY (ARRAY[('PENDIENTE'::character varying)::text, ('EN_CURSO'::character varying)::text, ('LOGRADO'::character varying)::text, ('CANCELADO'::character varying)::text])))
);

ALTER TABLE ONLY consultorio.pei_objetivos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_objetivos OWNER TO postgres;

--
-- Name: pei_objetivos_id_pei_objetivo_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_objetivos_id_pei_objetivo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_objetivos_id_pei_objetivo_seq OWNER TO postgres;

--
-- Name: pei_objetivos_id_pei_objetivo_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_objetivos_id_pei_objetivo_seq OWNED BY consultorio.pei_objetivos.id_pei_objetivo;


--
-- Name: pei_registro_mensual; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_registro_mensual (
    id_pei_registro_mensual bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei bigint NOT NULL,
    fec_registro date NOT NULL,
    nro_periodo smallint NOT NULL,
    des_observaciones text,
    des_recordatorio text,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.pei_registro_mensual FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_registro_mensual OWNER TO postgres;

--
-- Name: pei_registro_mensual_id_pei_registro_mensual_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_registro_mensual_id_pei_registro_mensual_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_registro_mensual_id_pei_registro_mensual_seq OWNER TO postgres;

--
-- Name: pei_registro_mensual_id_pei_registro_mensual_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_registro_mensual_id_pei_registro_mensual_seq OWNED BY consultorio.pei_registro_mensual.id_pei_registro_mensual;


--
-- Name: pei_reunion_clinica; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_reunion_clinica (
    id_pei_reunion_clinica bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei bigint NOT NULL,
    id_pei_calendario_evento bigint,
    nro_version smallint DEFAULT 1 NOT NULL,
    fec_reunion date NOT NULL,
    des_epicrisis text NOT NULL,
    des_diagnostico_acordado text,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.pei_reunion_clinica FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_reunion_clinica OWNER TO postgres;

--
-- Name: pei_reunion_clinica_id_pei_reunion_clinica_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_reunion_clinica_id_pei_reunion_clinica_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_reunion_clinica_id_pei_reunion_clinica_seq OWNER TO postgres;

--
-- Name: pei_reunion_clinica_id_pei_reunion_clinica_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_reunion_clinica_id_pei_reunion_clinica_seq OWNED BY consultorio.pei_reunion_clinica.id_pei_reunion_clinica;


--
-- Name: pei_reunion_participantes; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_reunion_participantes (
    id_pei_reunion_participante bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei_reunion_clinica bigint NOT NULL,
    id_especialista integer,
    des_nombre_externo text,
    des_rol_externo text,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT chk_participante_identificado CHECK (((id_especialista IS NOT NULL) OR (des_nombre_externo IS NOT NULL)))
);

ALTER TABLE ONLY consultorio.pei_reunion_participantes FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_reunion_participantes OWNER TO postgres;

--
-- Name: pei_reunion_participantes_id_pei_reunion_participante_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_reunion_participantes_id_pei_reunion_participante_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_reunion_participantes_id_pei_reunion_participante_seq OWNER TO postgres;

--
-- Name: pei_reunion_participantes_id_pei_reunion_participante_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_reunion_participantes_id_pei_reunion_participante_seq OWNED BY consultorio.pei_reunion_participantes.id_pei_reunion_participante;


--
-- Name: pei_reunion_recomendaciones; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_reunion_recomendaciones (
    id_pei_recomendacion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei_reunion_clinica bigint NOT NULL,
    nro_orden smallint NOT NULL,
    des_recomendacion text NOT NULL,
    es_cumplida boolean DEFAULT false NOT NULL,
    fec_cumplimiento date,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.pei_reunion_recomendaciones FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_reunion_recomendaciones OWNER TO postgres;

--
-- Name: pei_reunion_recomendaciones_id_pei_recomendacion_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_reunion_recomendaciones_id_pei_recomendacion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_reunion_recomendaciones_id_pei_recomendacion_seq OWNER TO postgres;

--
-- Name: pei_reunion_recomendaciones_id_pei_recomendacion_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_reunion_recomendaciones_id_pei_recomendacion_seq OWNED BY consultorio.pei_reunion_recomendaciones.id_pei_recomendacion;


--
-- Name: pei_sesion_actividades; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_sesion_actividades (
    id_pei_sesion_actividad bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei_sesion bigint NOT NULL,
    nro_orden smallint NOT NULL,
    des_actividad text NOT NULL,
    es_realizada boolean DEFAULT false NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.pei_sesion_actividades FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_sesion_actividades OWNER TO postgres;

--
-- Name: pei_sesion_actividades_id_pei_sesion_actividad_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_sesion_actividades_id_pei_sesion_actividad_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_sesion_actividades_id_pei_sesion_actividad_seq OWNER TO postgres;

--
-- Name: pei_sesion_actividades_id_pei_sesion_actividad_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_sesion_actividades_id_pei_sesion_actividad_seq OWNED BY consultorio.pei_sesion_actividades.id_pei_sesion_actividad;


--
-- Name: pei_sesion_planificada; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.pei_sesion_planificada (
    id_pei_sesion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_pei bigint NOT NULL,
    id_episodio bigint,
    fec_sesion date NOT NULL,
    des_materiales text,
    des_notas text,
    est_pei_sesion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.pei_sesion_planificada FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.pei_sesion_planificada OWNER TO postgres;

--
-- Name: pei_sesion_planificada_id_pei_sesion_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.pei_sesion_planificada_id_pei_sesion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.pei_sesion_planificada_id_pei_sesion_seq OWNER TO postgres;

--
-- Name: pei_sesion_planificada_id_pei_sesion_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.pei_sesion_planificada_id_pei_sesion_seq OWNED BY consultorio.pei_sesion_planificada.id_pei_sesion;


--
-- Name: planes_tratamiento; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.planes_tratamiento (
    id_plan_tratamiento bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    des_objetivo_general text,
    des_descripcion text,
    cod_estado_plan text DEFAULT 'ACTIVO'::text NOT NULL,
    fec_inicio date,
    fec_fin_estimada date,
    fec_cierre date,
    nro_sesiones_estimadas smallint,
    est_plan_tratamiento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT planes_tratamiento_cod_estado_plan_check CHECK ((cod_estado_plan = ANY (ARRAY['ACTIVO'::text, 'COMPLETADO'::text, 'SUSPENDIDO'::text, 'ABANDONADO'::text]))),
    CONSTRAINT planes_tratamiento_nro_sesiones_estimadas_check CHECK ((nro_sesiones_estimadas > 0))
);

ALTER TABLE ONLY consultorio.planes_tratamiento FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.planes_tratamiento OWNER TO postgres;

--
-- Name: planes_tratamiento_id_plan_tratamiento_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.planes_tratamiento_id_plan_tratamiento_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.planes_tratamiento_id_plan_tratamiento_seq OWNER TO postgres;

--
-- Name: planes_tratamiento_id_plan_tratamiento_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.planes_tratamiento_id_plan_tratamiento_seq OWNED BY consultorio.planes_tratamiento.id_plan_tratamiento;


--
-- Name: planes_tratamiento_items; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.planes_tratamiento_items (
    id_plan_tratamiento_item bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_plan_tratamiento bigint NOT NULL,
    nro_orden smallint DEFAULT 1 NOT NULL,
    des_objetivo text NOT NULL,
    des_estrategia text,
    cod_estado_item text DEFAULT 'PENDIENTE'::text NOT NULL,
    fec_completado date,
    est_plan_tratamiento_item boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT planes_tratamiento_items_cod_estado_item_check CHECK ((cod_estado_item = ANY (ARRAY['PENDIENTE'::text, 'EN_PROGRESO'::text, 'COMPLETADO'::text, 'SUSPENDIDO'::text]))),
    CONSTRAINT planes_tratamiento_items_nro_orden_check CHECK ((nro_orden > 0))
);

ALTER TABLE ONLY consultorio.planes_tratamiento_items FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.planes_tratamiento_items OWNER TO postgres;

--
-- Name: planes_tratamiento_items_id_plan_tratamiento_item_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.planes_tratamiento_items_id_plan_tratamiento_item_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.planes_tratamiento_items_id_plan_tratamiento_item_seq OWNER TO postgres;

--
-- Name: planes_tratamiento_items_id_plan_tratamiento_item_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.planes_tratamiento_items_id_plan_tratamiento_item_seq OWNED BY consultorio.planes_tratamiento_items.id_plan_tratamiento_item;


--
-- Name: plantillas_justificativos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.plantillas_justificativos (
    id_plantilla_justificativo integer NOT NULL,
    id_empresa integer NOT NULL,
    id_tipo_justificativo integer NOT NULL,
    des_titulo text NOT NULL,
    des_cuerpo_template text NOT NULL,
    est_plantilla_justificativo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.plantillas_justificativos FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.plantillas_justificativos OWNER TO postgres;

--
-- Name: plantillas_justificativos_id_plantilla_justificativo_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.plantillas_justificativos_id_plantilla_justificativo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.plantillas_justificativos_id_plantilla_justificativo_seq OWNER TO postgres;

--
-- Name: plantillas_justificativos_id_plantilla_justificativo_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.plantillas_justificativos_id_plantilla_justificativo_seq OWNED BY consultorio.plantillas_justificativos.id_plantilla_justificativo;


--
-- Name: procedimientos_empresa; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.procedimientos_empresa (
    id_procedimiento_empresa integer NOT NULL,
    id_empresa integer NOT NULL,
    id_tipo_procedimiento integer,
    cod_procedimiento text NOT NULL,
    des_procedimiento text NOT NULL,
    duracion_min smallint,
    es_requiere_insumos boolean DEFAULT false NOT NULL,
    est_procedimiento_empresa boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT procedimientos_empresa_duracion_min_check CHECK ((duracion_min > 0))
);

ALTER TABLE ONLY consultorio.procedimientos_empresa FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.procedimientos_empresa OWNER TO postgres;

--
-- Name: procedimientos_empresa_id_procedimiento_empresa_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.procedimientos_empresa_id_procedimiento_empresa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.procedimientos_empresa_id_procedimiento_empresa_seq OWNER TO postgres;

--
-- Name: procedimientos_empresa_id_procedimiento_empresa_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.procedimientos_empresa_id_procedimiento_empresa_seq OWNED BY consultorio.procedimientos_empresa.id_procedimiento_empresa;


--
-- Name: psicologia_perfil_empresa; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.psicologia_perfil_empresa (
    id_psicologia_perfil integer NOT NULL,
    id_empresa_perfil_clinico integer NOT NULL,
    id_empresa integer NOT NULL,
    hrs_preaviso_ausencia smallint DEFAULT 24 NOT NULL,
    pct_multa_ausencia numeric(5,2) DEFAULT 50.00 NOT NULL,
    monto_multa_atraso_dia numeric(15,0) DEFAULT 5000 NOT NULL,
    max_ausencias_consecutivas smallint DEFAULT 3 NOT NULL,
    dias_elaboracion_informe smallint DEFAULT 7 NOT NULL,
    duracion_sesion_min smallint DEFAULT 50 NOT NULL,
    usa_dsm5 boolean DEFAULT true NOT NULL,
    usa_cie10 boolean DEFAULT true NOT NULL,
    cod_moneda character varying(3) DEFAULT 'PYG'::character varying NOT NULL,
    est_psicologia_perfil boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.psicologia_perfil_empresa FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.psicologia_perfil_empresa OWNER TO postgres;

--
-- Name: psicologia_perfil_empresa_id_psicologia_perfil_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.psicologia_perfil_empresa_id_psicologia_perfil_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.psicologia_perfil_empresa_id_psicologia_perfil_seq OWNER TO postgres;

--
-- Name: psicologia_perfil_empresa_id_psicologia_perfil_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.psicologia_perfil_empresa_id_psicologia_perfil_seq OWNED BY consultorio.psicologia_perfil_empresa.id_psicologia_perfil;


--
-- Name: recetas; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.recetas (
    id_receta bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    id_receta_origen bigint,
    nro_documento bigint NOT NULL,
    cod_estado_receta text DEFAULT 'EMITIDA'::text NOT NULL,
    fec_emision date DEFAULT CURRENT_DATE NOT NULL,
    fec_vencimiento date,
    des_observaciones text,
    est_receta boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT recetas_cod_estado_receta_check CHECK ((cod_estado_receta = ANY (ARRAY['EMITIDA'::text, 'ANULADA'::text])))
);

ALTER TABLE ONLY consultorio.recetas FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.recetas OWNER TO postgres;

--
-- Name: recetas_detalle; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.recetas_detalle (
    id_receta_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_receta bigint NOT NULL,
    id_medicamento_empresa integer,
    des_medicamento_libre text,
    des_dosis text NOT NULL,
    des_duracion_tratamiento text,
    nro_cantidad smallint,
    nro_orden smallint DEFAULT 1 NOT NULL,
    des_indicaciones_especiales text,
    est_receta_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT recetas_detalle_check CHECK (((id_medicamento_empresa IS NOT NULL) OR (des_medicamento_libre IS NOT NULL))),
    CONSTRAINT recetas_detalle_nro_cantidad_check CHECK ((nro_cantidad > 0)),
    CONSTRAINT recetas_detalle_nro_orden_check CHECK ((nro_orden > 0))
);

ALTER TABLE ONLY consultorio.recetas_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.recetas_detalle OWNER TO postgres;

--
-- Name: recetas_detalle_id_receta_detalle_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.recetas_detalle_id_receta_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.recetas_detalle_id_receta_detalle_seq OWNER TO postgres;

--
-- Name: recetas_detalle_id_receta_detalle_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.recetas_detalle_id_receta_detalle_seq OWNED BY consultorio.recetas_detalle.id_receta_detalle;


--
-- Name: recetas_id_receta_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.recetas_id_receta_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.recetas_id_receta_seq OWNER TO postgres;

--
-- Name: recetas_id_receta_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.recetas_id_receta_seq OWNED BY consultorio.recetas.id_receta;


--
-- Name: resultados_analisis; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.resultados_analisis (
    id_resultado_analisis bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_orden_analisis bigint NOT NULL,
    fec_resultado date NOT NULL,
    des_laboratorio text,
    des_observaciones_generales text,
    est_resultado_analisis boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.resultados_analisis FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.resultados_analisis OWNER TO postgres;

--
-- Name: resultados_analisis_detalle; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.resultados_analisis_detalle (
    id_resultado_analisis_det bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_resultado_analisis bigint NOT NULL,
    id_orden_analisis_detalle bigint,
    des_analisis text NOT NULL,
    des_valor text NOT NULL,
    des_unidad text,
    des_rango_referencia text,
    es_fuera_rango boolean DEFAULT false NOT NULL,
    est_resultado_analisis_det boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.resultados_analisis_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.resultados_analisis_detalle OWNER TO postgres;

--
-- Name: resultados_analisis_detalle_id_resultado_analisis_det_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.resultados_analisis_detalle_id_resultado_analisis_det_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.resultados_analisis_detalle_id_resultado_analisis_det_seq OWNER TO postgres;

--
-- Name: resultados_analisis_detalle_id_resultado_analisis_det_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.resultados_analisis_detalle_id_resultado_analisis_det_seq OWNED BY consultorio.resultados_analisis_detalle.id_resultado_analisis_det;


--
-- Name: resultados_analisis_id_resultado_analisis_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.resultados_analisis_id_resultado_analisis_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.resultados_analisis_id_resultado_analisis_seq OWNER TO postgres;

--
-- Name: resultados_analisis_id_resultado_analisis_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.resultados_analisis_id_resultado_analisis_seq OWNED BY consultorio.resultados_analisis.id_resultado_analisis;


--
-- Name: signos_vitales; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.signos_vitales (
    id_signos_vitales bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_episodio bigint NOT NULL,
    id_paciente bigint NOT NULL,
    id_especialista integer NOT NULL,
    fec_toma timestamp with time zone DEFAULT now() NOT NULL,
    des_observaciones text,
    est_signos_vitales boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.signos_vitales FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.signos_vitales OWNER TO postgres;

--
-- Name: signos_vitales_detalle; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.signos_vitales_detalle (
    id_signos_vitales_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_signos_vitales bigint NOT NULL,
    id_tipo_signo_vital integer NOT NULL,
    val_valor numeric(10,3) NOT NULL,
    des_observacion text,
    est_signos_vitales_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY consultorio.signos_vitales_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE consultorio.signos_vitales_detalle OWNER TO postgres;

--
-- Name: signos_vitales_detalle_id_signos_vitales_detalle_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.signos_vitales_detalle_id_signos_vitales_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.signos_vitales_detalle_id_signos_vitales_detalle_seq OWNER TO postgres;

--
-- Name: signos_vitales_detalle_id_signos_vitales_detalle_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.signos_vitales_detalle_id_signos_vitales_detalle_seq OWNED BY consultorio.signos_vitales_detalle.id_signos_vitales_detalle;


--
-- Name: signos_vitales_id_signos_vitales_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.signos_vitales_id_signos_vitales_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.signos_vitales_id_signos_vitales_seq OWNER TO postgres;

--
-- Name: signos_vitales_id_signos_vitales_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.signos_vitales_id_signos_vitales_seq OWNED BY consultorio.signos_vitales.id_signos_vitales;


--
-- Name: tipos_justificativos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.tipos_justificativos (
    id_tipo_justificativo integer NOT NULL,
    cod_tipo_justificativo text NOT NULL,
    des_tipo_justificativo text NOT NULL,
    es_requiere_dias boolean DEFAULT false NOT NULL,
    es_requiere_diagnostico boolean DEFAULT true NOT NULL,
    es_requiere_resultado_aptitud boolean DEFAULT false NOT NULL,
    est_tipo_justificativo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE consultorio.tipos_justificativos OWNER TO postgres;

--
-- Name: tipos_justificativos_id_tipo_justificativo_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.tipos_justificativos_id_tipo_justificativo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.tipos_justificativos_id_tipo_justificativo_seq OWNER TO postgres;

--
-- Name: tipos_justificativos_id_tipo_justificativo_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.tipos_justificativos_id_tipo_justificativo_seq OWNED BY consultorio.tipos_justificativos.id_tipo_justificativo;


--
-- Name: tipos_procedimientos; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.tipos_procedimientos (
    id_tipo_procedimiento integer NOT NULL,
    cod_tipo_procedimiento text NOT NULL,
    des_tipo_procedimiento text NOT NULL,
    cod_especialidad_base text,
    est_tipo_procedimiento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE consultorio.tipos_procedimientos OWNER TO postgres;

--
-- Name: tipos_procedimientos_id_tipo_procedimiento_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.tipos_procedimientos_id_tipo_procedimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.tipos_procedimientos_id_tipo_procedimiento_seq OWNER TO postgres;

--
-- Name: tipos_procedimientos_id_tipo_procedimiento_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.tipos_procedimientos_id_tipo_procedimiento_seq OWNED BY consultorio.tipos_procedimientos.id_tipo_procedimiento;


--
-- Name: tipos_signos_vitales; Type: TABLE; Schema: consultorio; Owner: postgres
--

CREATE TABLE consultorio.tipos_signos_vitales (
    id_tipo_signo_vital integer NOT NULL,
    cod_tipo_signo_vital text NOT NULL,
    des_tipo_signo_vital text NOT NULL,
    des_unidad_medida text,
    val_min_referencia numeric(10,3),
    val_max_referencia numeric(10,3),
    est_tipo_signo_vital boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE consultorio.tipos_signos_vitales OWNER TO postgres;

--
-- Name: tipos_signos_vitales_id_tipo_signo_vital_seq; Type: SEQUENCE; Schema: consultorio; Owner: postgres
--

CREATE SEQUENCE consultorio.tipos_signos_vitales_id_tipo_signo_vital_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE consultorio.tipos_signos_vitales_id_tipo_signo_vital_seq OWNER TO postgres;

--
-- Name: tipos_signos_vitales_id_tipo_signo_vital_seq; Type: SEQUENCE OWNED BY; Schema: consultorio; Owner: postgres
--

ALTER SEQUENCE consultorio.tipos_signos_vitales_id_tipo_signo_vital_seq OWNED BY consultorio.tipos_signos_vitales.id_tipo_signo_vital;


--
-- Name: agenda_horarios; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.agenda_horarios (
    id_agenda_horario integer NOT NULL,
    id_empresa integer NOT NULL,
    id_sede integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_especialista integer NOT NULL,
    id_especialidad integer,
    id_dia_semana integer NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fin time without time zone NOT NULL,
    duracion_turno_min smallint DEFAULT 60 NOT NULL,
    cupos_totales smallint DEFAULT 1 NOT NULL,
    modalidad_default public.modalidad_cita_domain DEFAULT 'PRESENCIAL'::text NOT NULL,
    porcentaje_overbooking smallint DEFAULT 0 NOT NULL,
    fec_desde date NOT NULL,
    fec_hasta date,
    observaciones text,
    est_agenda_horario boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT agenda_horarios_cupos_totales_check CHECK ((cupos_totales > 0)),
    CONSTRAINT agenda_horarios_duracion_turno_min_check CHECK ((duracion_turno_min > 0)),
    CONSTRAINT agenda_horarios_porcentaje_overbooking_check CHECK (((porcentaje_overbooking >= 0) AND (porcentaje_overbooking <= 100))),
    CONSTRAINT chk_agenda_fechas CHECK (((fec_hasta IS NULL) OR (fec_hasta >= fec_desde))),
    CONSTRAINT chk_agenda_horas CHECK ((hora_fin > hora_inicio))
);

ALTER TABLE ONLY core.agenda_horarios FORCE ROW LEVEL SECURITY;


ALTER TABLE core.agenda_horarios OWNER TO postgres;

--
-- Name: agenda_horarios_excepciones; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.agenda_horarios_excepciones (
    id_agenda_horario_excepcion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_agenda_horario integer NOT NULL,
    fec_inicio date NOT NULL,
    fec_fin date NOT NULL,
    tipo_excepcion text NOT NULL,
    detalle text,
    est_agenda_horario_excepcion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT agenda_horarios_excepciones_tipo_excepcion_check CHECK ((tipo_excepcion = ANY (ARRAY['BLOQUEO'::text, 'EXTENSION'::text, 'FERIADO'::text]))),
    CONSTRAINT chk_excepcion_fechas CHECK ((fec_fin >= fec_inicio))
);

ALTER TABLE ONLY core.agenda_horarios_excepciones FORCE ROW LEVEL SECURITY;


ALTER TABLE core.agenda_horarios_excepciones OWNER TO postgres;

--
-- Name: agenda_horarios_excepciones_id_agenda_horario_excepcion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.agenda_horarios_excepciones_id_agenda_horario_excepcion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.agenda_horarios_excepciones_id_agenda_horario_excepcion_seq OWNER TO postgres;

--
-- Name: agenda_horarios_excepciones_id_agenda_horario_excepcion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.agenda_horarios_excepciones_id_agenda_horario_excepcion_seq OWNED BY core.agenda_horarios_excepciones.id_agenda_horario_excepcion;


--
-- Name: agenda_horarios_id_agenda_horario_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.agenda_horarios_id_agenda_horario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.agenda_horarios_id_agenda_horario_seq OWNER TO postgres;

--
-- Name: agenda_horarios_id_agenda_horario_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.agenda_horarios_id_agenda_horario_seq OWNED BY core.agenda_horarios.id_agenda_horario;


--
-- Name: auditoria_sistema; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.auditoria_sistema (
    id_auditoria_sistema bigint NOT NULL,
    id_empresa integer,
    id_usuario integer,
    accion text NOT NULL,
    entidad text,
    id_registro bigint,
    ip_origen text,
    user_agent text,
    detalle jsonb DEFAULT '{}'::jsonb NOT NULL,
    fec_evento timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
)
PARTITION BY RANGE (fec_evento);

ALTER TABLE ONLY core.auditoria_sistema FORCE ROW LEVEL SECURITY;


ALTER TABLE core.auditoria_sistema OWNER TO postgres;

--
-- Name: auditoria_sistema_id_auditoria_sistema_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.auditoria_sistema_id_auditoria_sistema_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.auditoria_sistema_id_auditoria_sistema_seq OWNER TO postgres;

--
-- Name: auditoria_sistema_id_auditoria_sistema_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.auditoria_sistema_id_auditoria_sistema_seq OWNED BY core.auditoria_sistema.id_auditoria_sistema;


--
-- Name: auditoria_sistema_y2026; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.auditoria_sistema_y2026 (
    id_auditoria_sistema bigint DEFAULT nextval('core.auditoria_sistema_id_auditoria_sistema_seq'::regclass) NOT NULL,
    id_empresa integer,
    id_usuario integer,
    accion text NOT NULL,
    entidad text,
    id_registro bigint,
    ip_origen text,
    user_agent text,
    detalle jsonb DEFAULT '{}'::jsonb NOT NULL,
    fec_evento timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE ONLY core.auditoria_sistema_y2026 FORCE ROW LEVEL SECURITY;


ALTER TABLE core.auditoria_sistema_y2026 OWNER TO postgres;

--
-- Name: auditoria_sistema_y2027; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.auditoria_sistema_y2027 (
    id_auditoria_sistema bigint DEFAULT nextval('core.auditoria_sistema_id_auditoria_sistema_seq'::regclass) NOT NULL,
    id_empresa integer,
    id_usuario integer,
    accion text NOT NULL,
    entidad text,
    id_registro bigint,
    ip_origen text,
    user_agent text,
    detalle jsonb DEFAULT '{}'::jsonb NOT NULL,
    fec_evento timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE ONLY core.auditoria_sistema_y2027 FORCE ROW LEVEL SECURITY;


ALTER TABLE core.auditoria_sistema_y2027 OWNER TO postgres;

--
-- Name: auditoria_sistema_y2028; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.auditoria_sistema_y2028 (
    id_auditoria_sistema bigint DEFAULT nextval('core.auditoria_sistema_id_auditoria_sistema_seq'::regclass) NOT NULL,
    id_empresa integer,
    id_usuario integer,
    accion text NOT NULL,
    entidad text,
    id_registro bigint,
    ip_origen text,
    user_agent text,
    detalle jsonb DEFAULT '{}'::jsonb NOT NULL,
    fec_evento timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE ONLY core.auditoria_sistema_y2028 FORCE ROW LEVEL SECURITY;


ALTER TABLE core.auditoria_sistema_y2028 OWNER TO postgres;

--
-- Name: cargos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.cargos (
    id_cargo integer NOT NULL,
    id_empresa integer NOT NULL,
    des_cargo text NOT NULL,
    est_cargo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    es_especialista boolean DEFAULT false NOT NULL
);

ALTER TABLE ONLY core.cargos FORCE ROW LEVEL SECURITY;


ALTER TABLE core.cargos OWNER TO postgres;

--
-- Name: COLUMN cargos.es_especialista; Type: COMMENT; Schema: core; Owner: postgres
--

COMMENT ON COLUMN core.cargos.es_especialista IS 'Si TRUE, al crear/editar un funcionario con este cargo se habilitan los campos de matrícula y especialidades.';


--
-- Name: cargos_id_cargo_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.cargos_id_cargo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.cargos_id_cargo_seq OWNER TO postgres;

--
-- Name: cargos_id_cargo_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.cargos_id_cargo_seq OWNED BY core.cargos.id_cargo;


--
-- Name: citas; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.citas (
    id_cita bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_sede integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_especialista integer NOT NULL,
    id_especialidad integer NOT NULL,
    id_paciente integer NOT NULL,
    id_estado_cita integer NOT NULL,
    id_slot_agenda bigint,
    modalidad public.modalidad_cita_domain DEFAULT 'PRESENCIAL'::text NOT NULL,
    remota_url text,
    cita_inicio timestamp with time zone NOT NULL,
    cita_fin timestamp with time zone NOT NULL,
    motivo text,
    observaciones text,
    motivo_cancelacion text,
    est_cita boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cita_es_primera_vez boolean DEFAULT true NOT NULL,
    cita_numero_sesion smallint,
    id_contrato_tratamiento bigint,
    cod_origen_cita text DEFAULT 'MANUAL'::text NOT NULL,
    CONSTRAINT chk_citas_horario CHECK ((cita_fin > cita_inicio)),
    CONSTRAINT citas_cod_origen_cita_check CHECK ((cod_origen_cita = ANY (ARRAY['MANUAL'::text, 'CONTRATO'::text, 'LISTA_ESPERA'::text])))
);

ALTER TABLE ONLY core.citas FORCE ROW LEVEL SECURITY;


ALTER TABLE core.citas OWNER TO postgres;

--
-- Name: citas_id_cita_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.citas_id_cita_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.citas_id_cita_seq OWNER TO postgres;

--
-- Name: citas_id_cita_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.citas_id_cita_seq OWNED BY core.citas.id_cita;


--
-- Name: citas_log_estados; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.citas_log_estados (
    id_cita_log_estado bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_cita bigint NOT NULL,
    id_estado_anterior integer,
    id_estado_nuevo integer NOT NULL,
    motivo_cambio text,
    fec_cambio timestamp with time zone DEFAULT now() NOT NULL,
    est_cita_log_estado boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.citas_log_estados FORCE ROW LEVEL SECURITY;


ALTER TABLE core.citas_log_estados OWNER TO postgres;

--
-- Name: citas_log_estados_id_cita_log_estado_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.citas_log_estados_id_cita_log_estado_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.citas_log_estados_id_cita_log_estado_seq OWNER TO postgres;

--
-- Name: citas_log_estados_id_cita_log_estado_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.citas_log_estados_id_cita_log_estado_seq OWNED BY core.citas_log_estados.id_cita_log_estado;


--
-- Name: ciudades; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.ciudades (
    id_ciudad integer NOT NULL,
    id_departamento integer NOT NULL,
    des_ciudad text NOT NULL,
    est_ciudad boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_ciudad_sifen integer,
    cod_distrito_sifen integer,
    des_distrito_sifen text
);


ALTER TABLE core.ciudades OWNER TO postgres;

--
-- Name: ciudades_id_ciudad_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.ciudades_id_ciudad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.ciudades_id_ciudad_seq OWNER TO postgres;

--
-- Name: ciudades_id_ciudad_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.ciudades_id_ciudad_seq OWNED BY core.ciudades.id_ciudad;


--
-- Name: condiciones_venta; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.condiciones_venta (
    id_condicion_venta integer NOT NULL,
    cod_condicion_venta text NOT NULL,
    des_condicion_venta text NOT NULL,
    est_condicion_venta boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_sifen character(1),
    cnt_dias_credito smallint DEFAULT 0 NOT NULL,
    est_permite_cuotas boolean DEFAULT false NOT NULL,
    cnt_cuotas_max smallint DEFAULT 1 NOT NULL,
    CONSTRAINT chk_condicion_venta_cod_sifen CHECK (((cod_sifen IS NULL) OR (cod_sifen = ANY (ARRAY['1'::bpchar, '2'::bpchar])))),
    CONSTRAINT chk_condicion_venta_cuotas CHECK ((cnt_cuotas_max >= 1)),
    CONSTRAINT chk_condicion_venta_dias CHECK ((cnt_dias_credito >= 0))
);


ALTER TABLE core.condiciones_venta OWNER TO postgres;

--
-- Name: condiciones_venta_id_condicion_venta_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.condiciones_venta_id_condicion_venta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.condiciones_venta_id_condicion_venta_seq OWNER TO postgres;

--
-- Name: condiciones_venta_id_condicion_venta_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.condiciones_venta_id_condicion_venta_seq OWNED BY core.condiciones_venta.id_condicion_venta;


--
-- Name: consultorios; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.consultorios (
    id_consultorio integer NOT NULL,
    id_empresa integer NOT NULL,
    id_sede integer NOT NULL,
    des_consultorio text NOT NULL,
    est_consultorio boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.consultorios FORCE ROW LEVEL SECURITY;


ALTER TABLE core.consultorios OWNER TO postgres;

--
-- Name: consultorios_id_consultorio_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.consultorios_id_consultorio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.consultorios_id_consultorio_seq OWNER TO postgres;

--
-- Name: consultorios_id_consultorio_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.consultorios_id_consultorio_seq OWNED BY core.consultorios.id_consultorio;


--
-- Name: departamentos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.departamentos (
    id_departamento integer NOT NULL,
    id_pais integer NOT NULL,
    cod_departamento text,
    des_departamento text NOT NULL,
    est_departamento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_departamento_sifen smallint
);


ALTER TABLE core.departamentos OWNER TO postgres;

--
-- Name: departamentos_id_departamento_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.departamentos_id_departamento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.departamentos_id_departamento_seq OWNER TO postgres;

--
-- Name: departamentos_id_departamento_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.departamentos_id_departamento_seq OWNED BY core.departamentos.id_departamento;


--
-- Name: dias_semana; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.dias_semana (
    id_dia_semana integer NOT NULL,
    nro_dia smallint NOT NULL,
    des_dia text NOT NULL,
    est_dia_semana boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT dias_semana_nro_dia_check CHECK (((nro_dia >= 1) AND (nro_dia <= 7)))
);


ALTER TABLE core.dias_semana OWNER TO postgres;

--
-- Name: dias_semana_id_dia_semana_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.dias_semana_id_dia_semana_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.dias_semana_id_dia_semana_seq OWNER TO postgres;

--
-- Name: dias_semana_id_dia_semana_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.dias_semana_id_dia_semana_seq OWNED BY core.dias_semana.id_dia_semana;


--
-- Name: empresa_certificados; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.empresa_certificados (
    id_empresa_certificado integer NOT NULL,
    id_empresa integer NOT NULL,
    tipo_certificado public.tipo_certificado_domain NOT NULL,
    ruta_interna text NOT NULL,
    fingerprint_sha256 text NOT NULL,
    fec_vencimiento timestamp with time zone,
    est_empresa_certificado boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    des_cert_pass_encrypted text,
    des_cert_subject text
);

ALTER TABLE ONLY core.empresa_certificados FORCE ROW LEVEL SECURITY;


ALTER TABLE core.empresa_certificados OWNER TO postgres;

--
-- Name: empresa_certificados_id_empresa_certificado_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.empresa_certificados_id_empresa_certificado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.empresa_certificados_id_empresa_certificado_seq OWNER TO postgres;

--
-- Name: empresa_certificados_id_empresa_certificado_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.empresa_certificados_id_empresa_certificado_seq OWNED BY core.empresa_certificados.id_empresa_certificado;


--
-- Name: empresa_configuracion; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.empresa_configuracion (
    id_empresa_configuracion integer NOT NULL,
    id_empresa integer NOT NULL,
    config_json jsonb DEFAULT '{}'::jsonb NOT NULL,
    est_empresa_configuracion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.empresa_configuracion FORCE ROW LEVEL SECURITY;


ALTER TABLE core.empresa_configuracion OWNER TO postgres;

--
-- Name: empresa_configuracion_id_empresa_configuracion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.empresa_configuracion_id_empresa_configuracion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.empresa_configuracion_id_empresa_configuracion_seq OWNER TO postgres;

--
-- Name: empresa_configuracion_id_empresa_configuracion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.empresa_configuracion_id_empresa_configuracion_seq OWNED BY core.empresa_configuracion.id_empresa_configuracion;


--
-- Name: empresa_modulos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.empresa_modulos (
    id_empresa_modulo integer NOT NULL,
    id_empresa integer NOT NULL,
    id_modulo integer NOT NULL,
    fec_activacion timestamp with time zone DEFAULT now() NOT NULL,
    fec_vencimiento timestamp with time zone,
    est_empresa_modulo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.empresa_modulos FORCE ROW LEVEL SECURITY;


ALTER TABLE core.empresa_modulos OWNER TO postgres;

--
-- Name: empresa_modulos_id_empresa_modulo_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.empresa_modulos_id_empresa_modulo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.empresa_modulos_id_empresa_modulo_seq OWNER TO postgres;

--
-- Name: empresa_modulos_id_empresa_modulo_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.empresa_modulos_id_empresa_modulo_seq OWNED BY core.empresa_modulos.id_empresa_modulo;


--
-- Name: empresas; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.empresas (
    id_empresa integer NOT NULL,
    tipo_empresa public.tipo_empresa_domain NOT NULL,
    forma_juridica public.forma_juridica_domain,
    estado_empresa public.estado_empresa_domain DEFAULT 'ACTIVO'::text NOT NULL,
    estado_ruc public.estado_ruc_domain DEFAULT 'PENDIENTE'::text NOT NULL,
    razon_social text NOT NULL,
    nombre_comercial text,
    ruc_nit text,
    digito_verificador text,
    cod_actividad_economica text,
    email text,
    telefono text,
    celular text,
    id_departamento integer,
    id_ciudad integer,
    direccion_fiscal text,
    nombre_representante text,
    doc_representante text,
    nombre_dueno text,
    telefono_dueno text,
    email_dueno text,
    nombre_operativo text,
    email_operativo text,
    fec_vencimiento_contrato date,
    path_contrato text,
    fec_aceptacion_contrato timestamp with time zone,
    ip_aceptacion text,
    requiere_anual boolean DEFAULT false NOT NULL,
    timezone text DEFAULT 'America/Asuncion'::text NOT NULL,
    est_empresa boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    mfa_requerido boolean DEFAULT false NOT NULL,
    CONSTRAINT chk_empresas_email CHECK (((email IS NULL) OR (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text)))
);

ALTER TABLE ONLY core.empresas FORCE ROW LEVEL SECURITY;


ALTER TABLE core.empresas OWNER TO postgres;

--
-- Name: empresas_id_empresa_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.empresas_id_empresa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.empresas_id_empresa_seq OWNER TO postgres;

--
-- Name: empresas_id_empresa_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.empresas_id_empresa_seq OWNED BY core.empresas.id_empresa;


--
-- Name: especialidades; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.especialidades (
    id_especialidad integer NOT NULL,
    id_empresa integer NOT NULL,
    des_especialidad text NOT NULL,
    est_especialidad boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_tipo_clinico character varying(30)
);

ALTER TABLE ONLY core.especialidades FORCE ROW LEVEL SECURITY;


ALTER TABLE core.especialidades OWNER TO postgres;

--
-- Name: especialidades_id_especialidad_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.especialidades_id_especialidad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.especialidades_id_especialidad_seq OWNER TO postgres;

--
-- Name: especialidades_id_especialidad_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.especialidades_id_especialidad_seq OWNED BY core.especialidades.id_especialidad;


--
-- Name: especialista_especialidades; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.especialista_especialidades (
    id_especialista_especialidad integer NOT NULL,
    id_empresa integer NOT NULL,
    id_especialista integer NOT NULL,
    id_especialidad integer NOT NULL,
    est_especialista_especialidad boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.especialista_especialidades FORCE ROW LEVEL SECURITY;


ALTER TABLE core.especialista_especialidades OWNER TO postgres;

--
-- Name: especialista_especialidades_id_especialista_especialidad_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.especialista_especialidades_id_especialista_especialidad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.especialista_especialidades_id_especialista_especialidad_seq OWNER TO postgres;

--
-- Name: especialista_especialidades_id_especialista_especialidad_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.especialista_especialidades_id_especialista_especialidad_seq OWNED BY core.especialista_especialidades.id_especialista_especialidad;


--
-- Name: especialistas; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.especialistas (
    id_especialista integer NOT NULL,
    id_empresa integer NOT NULL,
    id_funcionario integer NOT NULL,
    esp_matricula text,
    esp_color_agenda character varying(7) DEFAULT '#3498db'::character varying NOT NULL,
    est_especialista boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.especialistas FORCE ROW LEVEL SECURITY;


ALTER TABLE core.especialistas OWNER TO postgres;

--
-- Name: especialistas_id_especialista_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.especialistas_id_especialista_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.especialistas_id_especialista_seq OWNER TO postgres;

--
-- Name: especialistas_id_especialista_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.especialistas_id_especialista_seq OWNED BY core.especialistas.id_especialista;


--
-- Name: establecimientos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.establecimientos (
    id_establecimiento integer NOT NULL,
    id_empresa integer NOT NULL,
    id_sede integer NOT NULL,
    cod_establecimiento text NOT NULL,
    des_establecimiento text NOT NULL,
    es_principal boolean DEFAULT false NOT NULL,
    est_establecimiento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_establecimientos_codigo CHECK ((length(cod_establecimiento) = 3))
);

ALTER TABLE ONLY core.establecimientos FORCE ROW LEVEL SECURITY;


ALTER TABLE core.establecimientos OWNER TO postgres;

--
-- Name: establecimientos_id_establecimiento_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.establecimientos_id_establecimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.establecimientos_id_establecimiento_seq OWNER TO postgres;

--
-- Name: establecimientos_id_establecimiento_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.establecimientos_id_establecimiento_seq OWNED BY core.establecimientos.id_establecimiento;


--
-- Name: estados_citas; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.estados_citas (
    id_estado_cita integer NOT NULL,
    id_empresa integer NOT NULL,
    cod_estado_cita text NOT NULL,
    des_estado_cita text NOT NULL,
    orden smallint DEFAULT 0 NOT NULL,
    es_final boolean DEFAULT false NOT NULL,
    est_estado_cita boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.estados_citas FORCE ROW LEVEL SECURITY;


ALTER TABLE core.estados_citas OWNER TO postgres;

--
-- Name: estados_citas_id_estado_cita_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.estados_citas_id_estado_cita_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.estados_citas_id_estado_cita_seq OWNER TO postgres;

--
-- Name: estados_citas_id_estado_cita_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.estados_citas_id_estado_cita_seq OWNED BY core.estados_citas.id_estado_cita;


--
-- Name: estados_civiles; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.estados_civiles (
    id_estado_civil integer NOT NULL,
    des_estado_civil text NOT NULL,
    est_estado_civil boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.estados_civiles OWNER TO postgres;

--
-- Name: estados_civiles_id_estado_civil_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.estados_civiles_id_estado_civil_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.estados_civiles_id_estado_civil_seq OWNER TO postgres;

--
-- Name: estados_civiles_id_estado_civil_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.estados_civiles_id_estado_civil_seq OWNED BY core.estados_civiles.id_estado_civil;


--
-- Name: estados_factura; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.estados_factura (
    id_estado_factura integer NOT NULL,
    cod_estado_factura text NOT NULL,
    des_estado_factura text NOT NULL,
    est_estado_factura boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.estados_factura OWNER TO postgres;

--
-- Name: estados_factura_id_estado_factura_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.estados_factura_id_estado_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.estados_factura_id_estado_factura_seq OWNER TO postgres;

--
-- Name: estados_factura_id_estado_factura_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.estados_factura_id_estado_factura_seq OWNED BY core.estados_factura.id_estado_factura;


--
-- Name: feriados; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.feriados (
    id_feriado integer NOT NULL,
    id_empresa integer NOT NULL,
    fecha date NOT NULL,
    descripcion text NOT NULL,
    est_feriado boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.feriados FORCE ROW LEVEL SECURITY;


ALTER TABLE core.feriados OWNER TO postgres;

--
-- Name: feriados_id_feriado_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.feriados_id_feriado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.feriados_id_feriado_seq OWNER TO postgres;

--
-- Name: feriados_id_feriado_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.feriados_id_feriado_seq OWNED BY core.feriados.id_feriado;


--
-- Name: formas_cobro; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.formas_cobro (
    id_forma_cobro integer NOT NULL,
    cod_forma_cobro text NOT NULL,
    des_forma_cobro text NOT NULL,
    est_forma_cobro boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_sifen smallint
);


ALTER TABLE core.formas_cobro OWNER TO postgres;

--
-- Name: formas_cobro_id_forma_cobro_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.formas_cobro_id_forma_cobro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.formas_cobro_id_forma_cobro_seq OWNER TO postgres;

--
-- Name: formas_cobro_id_forma_cobro_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.formas_cobro_id_forma_cobro_seq OWNED BY core.formas_cobro.id_forma_cobro;


--
-- Name: frecuencias_agendamiento; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.frecuencias_agendamiento (
    id_frecuencia_agendamiento integer NOT NULL,
    cod_frecuencia text NOT NULL,
    des_frecuencia text NOT NULL,
    est_frecuencia_agendamiento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.frecuencias_agendamiento OWNER TO postgres;

--
-- Name: frecuencias_agendamiento_id_frecuencia_agendamiento_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.frecuencias_agendamiento_id_frecuencia_agendamiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.frecuencias_agendamiento_id_frecuencia_agendamiento_seq OWNER TO postgres;

--
-- Name: frecuencias_agendamiento_id_frecuencia_agendamiento_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.frecuencias_agendamiento_id_frecuencia_agendamiento_seq OWNED BY core.frecuencias_agendamiento.id_frecuencia_agendamiento;


--
-- Name: funcionarios; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.funcionarios (
    id_funcionario integer NOT NULL,
    id_empresa integer NOT NULL,
    id_persona integer NOT NULL,
    id_cargo integer,
    id_usuario integer,
    est_funcionario boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.funcionarios FORCE ROW LEVEL SECURITY;


ALTER TABLE core.funcionarios OWNER TO postgres;

--
-- Name: funcionarios_id_funcionario_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.funcionarios_id_funcionario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.funcionarios_id_funcionario_seq OWNER TO postgres;

--
-- Name: funcionarios_id_funcionario_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.funcionarios_id_funcionario_seq OWNED BY core.funcionarios.id_funcionario;


--
-- Name: generos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.generos (
    id_genero integer NOT NULL,
    des_genero text NOT NULL,
    est_genero boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.generos OWNER TO postgres;

--
-- Name: generos_id_genero_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.generos_id_genero_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.generos_id_genero_seq OWNER TO postgres;

--
-- Name: generos_id_genero_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.generos_id_genero_seq OWNED BY core.generos.id_genero;


--
-- Name: historial_suscripciones; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.historial_suscripciones (
    id_historial_suscripcion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_suscripcion bigint NOT NULL,
    evento public.evento_suscripcion_domain NOT NULL,
    detalle jsonb DEFAULT '{}'::jsonb NOT NULL,
    fec_evento timestamp with time zone DEFAULT now() NOT NULL,
    est_historial_suscripcion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.historial_suscripciones FORCE ROW LEVEL SECURITY;


ALTER TABLE core.historial_suscripciones OWNER TO postgres;

--
-- Name: historial_suscripciones_id_historial_suscripcion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.historial_suscripciones_id_historial_suscripcion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.historial_suscripciones_id_historial_suscripcion_seq OWNER TO postgres;

--
-- Name: historial_suscripciones_id_historial_suscripcion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.historial_suscripciones_id_historial_suscripcion_seq OWNED BY core.historial_suscripciones.id_historial_suscripcion;


--
-- Name: licencias; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.licencias (
    id_licencia integer NOT NULL,
    id_empresa integer NOT NULL,
    clave_licencia text NOT NULL,
    fec_vencimiento timestamp with time zone NOT NULL,
    max_usuarios integer,
    hash_validacion text NOT NULL,
    est_licencia boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.licencias FORCE ROW LEVEL SECURITY;


ALTER TABLE core.licencias OWNER TO postgres;

--
-- Name: licencias_id_licencia_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.licencias_id_licencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.licencias_id_licencia_seq OWNER TO postgres;

--
-- Name: licencias_id_licencia_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.licencias_id_licencia_seq OWNED BY core.licencias.id_licencia;


--
-- Name: lista_espera; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.lista_espera (
    id_lista_espera bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_agenda_horario integer NOT NULL,
    id_paciente integer NOT NULL,
    estado text DEFAULT 'PENDIENTE'::text NOT NULL,
    prioridad smallint DEFAULT 0 NOT NULL,
    motivo text,
    fec_solicitud timestamp with time zone DEFAULT now() NOT NULL,
    fec_ultima_notificacion timestamp with time zone,
    est_lista_espera boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT lista_espera_estado_check CHECK ((estado = ANY (ARRAY['PENDIENTE'::text, 'NOTIFICADO'::text, 'ACEPTADO'::text, 'CANCELADO'::text, 'EXPIRADO'::text])))
);

ALTER TABLE ONLY core.lista_espera FORCE ROW LEVEL SECURITY;


ALTER TABLE core.lista_espera OWNER TO postgres;

--
-- Name: lista_espera_id_lista_espera_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.lista_espera_id_lista_espera_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.lista_espera_id_lista_espera_seq OWNER TO postgres;

--
-- Name: lista_espera_id_lista_espera_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.lista_espera_id_lista_espera_seq OWNED BY core.lista_espera.id_lista_espera;


--
-- Name: login_attempts; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.login_attempts (
    id_login_attempt bigint NOT NULL,
    id_empresa integer,
    usu_nick public.citext,
    ip_address text,
    user_agent text,
    fue_exitoso boolean DEFAULT false NOT NULL,
    fec_intento timestamp with time zone DEFAULT now() NOT NULL,
    est_login_attempt boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    pais_origen text,
    des_motivo text
);

ALTER TABLE ONLY core.login_attempts FORCE ROW LEVEL SECURITY;


ALTER TABLE core.login_attempts OWNER TO postgres;

--
-- Name: login_attempts_id_login_attempt_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.login_attempts_id_login_attempt_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.login_attempts_id_login_attempt_seq OWNER TO postgres;

--
-- Name: login_attempts_id_login_attempt_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.login_attempts_id_login_attempt_seq OWNED BY core.login_attempts.id_login_attempt;


--
-- Name: marcas_tarjeta; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.marcas_tarjeta (
    id_marca_tarjeta integer NOT NULL,
    des_marca_tarjeta text NOT NULL,
    est_marca_tarjeta boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.marcas_tarjeta OWNER TO postgres;

--
-- Name: marcas_tarjeta_id_marca_tarjeta_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.marcas_tarjeta_id_marca_tarjeta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.marcas_tarjeta_id_marca_tarjeta_seq OWNER TO postgres;

--
-- Name: marcas_tarjeta_id_marca_tarjeta_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.marcas_tarjeta_id_marca_tarjeta_seq OWNED BY core.marcas_tarjeta.id_marca_tarjeta;


--
-- Name: metricas_diarias; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.metricas_diarias (
    id_metrica_diaria bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_sede integer,
    dia date NOT NULL,
    citas_creadas integer DEFAULT 0 NOT NULL,
    citas_atendidas integer DEFAULT 0 NOT NULL,
    citas_canceladas integer DEFAULT 0 NOT NULL,
    citas_ausentes integer DEFAULT 0 NOT NULL,
    tasa_ocupacion numeric(5,2),
    facturacion_total numeric(18,2) DEFAULT 0 NOT NULL,
    cobrado_total numeric(18,2) DEFAULT 0 NOT NULL,
    pendiente_cobro numeric(18,2) DEFAULT 0 NOT NULL,
    facturas_emitidas integer DEFAULT 0 NOT NULL,
    facturas_anuladas integer DEFAULT 0 NOT NULL,
    pacientes_nuevos integer DEFAULT 0 NOT NULL,
    pacientes_recurrentes integer DEFAULT 0 NOT NULL,
    usuarios_activos integer DEFAULT 0 NOT NULL,
    est_metrica_diaria boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.metricas_diarias FORCE ROW LEVEL SECURITY;


ALTER TABLE core.metricas_diarias OWNER TO postgres;

--
-- Name: metricas_diarias_id_metrica_diaria_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.metricas_diarias_id_metrica_diaria_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.metricas_diarias_id_metrica_diaria_seq OWNER TO postgres;

--
-- Name: metricas_diarias_id_metrica_diaria_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.metricas_diarias_id_metrica_diaria_seq OWNED BY core.metricas_diarias.id_metrica_diaria;


--
-- Name: mfa_tokens; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.mfa_tokens (
    id_mfa_token integer NOT NULL,
    id_usuario integer NOT NULL,
    codigo character varying(8) NOT NULL,
    fec_expiracion timestamp with time zone NOT NULL,
    fue_usado boolean DEFAULT false NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE ONLY core.mfa_tokens FORCE ROW LEVEL SECURITY;


ALTER TABLE core.mfa_tokens OWNER TO postgres;

--
-- Name: mfa_tokens_id_mfa_token_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.mfa_tokens_id_mfa_token_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.mfa_tokens_id_mfa_token_seq OWNER TO postgres;

--
-- Name: mfa_tokens_id_mfa_token_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.mfa_tokens_id_mfa_token_seq OWNED BY core.mfa_tokens.id_mfa_token;


--
-- Name: modulos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.modulos (
    id_modulo integer NOT NULL,
    cod_modulo text NOT NULL,
    des_modulo text NOT NULL,
    est_modulo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.modulos OWNER TO postgres;

--
-- Name: modulos_id_modulo_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.modulos_id_modulo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.modulos_id_modulo_seq OWNER TO postgres;

--
-- Name: modulos_id_modulo_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.modulos_id_modulo_seq OWNED BY core.modulos.id_modulo;


--
-- Name: monedas; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.monedas (
    id_moneda integer NOT NULL,
    cod_moneda text NOT NULL,
    des_moneda text NOT NULL,
    simbolo text,
    est_moneda boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.monedas OWNER TO postgres;

--
-- Name: monedas_id_moneda_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.monedas_id_moneda_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.monedas_id_moneda_seq OWNER TO postgres;

--
-- Name: monedas_id_moneda_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.monedas_id_moneda_seq OWNED BY core.monedas.id_moneda;


--
-- Name: niveles_instruccion; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.niveles_instruccion (
    id_nivel_instruccion integer NOT NULL,
    des_nivel_instruccion text NOT NULL,
    est_nivel_instruccion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_nivel_instruccion text,
    orden integer
);


ALTER TABLE core.niveles_instruccion OWNER TO postgres;

--
-- Name: niveles_instruccion_id_nivel_instruccion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.niveles_instruccion_id_nivel_instruccion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.niveles_instruccion_id_nivel_instruccion_seq OWNER TO postgres;

--
-- Name: niveles_instruccion_id_nivel_instruccion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.niveles_instruccion_id_nivel_instruccion_seq OWNED BY core.niveles_instruccion.id_nivel_instruccion;


--
-- Name: notificaciones_cola; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.notificaciones_cola (
    id_notificacion_cola bigint NOT NULL,
    id_empresa integer NOT NULL,
    canal public.canal_notificacion_domain NOT NULL,
    evento text NOT NULL,
    destinatario text NOT NULL,
    payload jsonb DEFAULT '{}'::jsonb NOT NULL,
    idempotency_key text NOT NULL,
    estado public.estado_envio_domain DEFAULT 'PENDIENTE'::text NOT NULL,
    intentos integer DEFAULT 0 NOT NULL,
    max_intentos integer DEFAULT 5 NOT NULL,
    fec_disponible_desde timestamp with time zone DEFAULT now() NOT NULL,
    fec_ultimo_intento timestamp with time zone,
    est_notificacion_cola boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT notificaciones_cola_max_intentos_check CHECK (((max_intentos >= 1) AND (max_intentos <= 20)))
);

ALTER TABLE ONLY core.notificaciones_cola FORCE ROW LEVEL SECURITY;


ALTER TABLE core.notificaciones_cola OWNER TO postgres;

--
-- Name: notificaciones_cola_id_notificacion_cola_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.notificaciones_cola_id_notificacion_cola_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.notificaciones_cola_id_notificacion_cola_seq OWNER TO postgres;

--
-- Name: notificaciones_cola_id_notificacion_cola_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.notificaciones_cola_id_notificacion_cola_seq OWNED BY core.notificaciones_cola.id_notificacion_cola;


--
-- Name: notificaciones_config; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.notificaciones_config (
    id_notificacion_config integer NOT NULL,
    id_empresa integer NOT NULL,
    canal public.canal_notificacion_domain NOT NULL,
    config jsonb DEFAULT '{}'::jsonb NOT NULL,
    est_notificacion_config boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.notificaciones_config FORCE ROW LEVEL SECURITY;


ALTER TABLE core.notificaciones_config OWNER TO postgres;

--
-- Name: notificaciones_config_id_notificacion_config_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.notificaciones_config_id_notificacion_config_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.notificaciones_config_id_notificacion_config_seq OWNER TO postgres;

--
-- Name: notificaciones_config_id_notificacion_config_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.notificaciones_config_id_notificacion_config_seq OWNED BY core.notificaciones_config.id_notificacion_config;


--
-- Name: notificaciones_log; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.notificaciones_log (
    id_notificacion_log bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_notificacion_cola bigint,
    canal public.canal_notificacion_domain NOT NULL,
    evento text NOT NULL,
    destinatario text NOT NULL,
    estado public.estado_envio_domain NOT NULL,
    proveedor text,
    proveedor_message_id text,
    error_codigo text,
    error_mensaje text,
    respuesta jsonb DEFAULT '{}'::jsonb NOT NULL,
    fec_evento timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE ONLY core.notificaciones_log FORCE ROW LEVEL SECURITY;


ALTER TABLE core.notificaciones_log OWNER TO postgres;

--
-- Name: notificaciones_log_id_notificacion_log_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.notificaciones_log_id_notificacion_log_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.notificaciones_log_id_notificacion_log_seq OWNER TO postgres;

--
-- Name: notificaciones_log_id_notificacion_log_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.notificaciones_log_id_notificacion_log_seq OWNED BY core.notificaciones_log.id_notificacion_log;


--
-- Name: notificaciones_plantillas; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.notificaciones_plantillas (
    id_notificacion_plantilla integer NOT NULL,
    id_empresa integer NOT NULL,
    canal public.canal_notificacion_domain NOT NULL,
    evento text NOT NULL,
    asunto text,
    cuerpo_template text NOT NULL,
    est_notificacion_plantilla boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.notificaciones_plantillas FORCE ROW LEVEL SECURITY;


ALTER TABLE core.notificaciones_plantillas OWNER TO postgres;

--
-- Name: notificaciones_plantillas_id_notificacion_plantilla_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.notificaciones_plantillas_id_notificacion_plantilla_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.notificaciones_plantillas_id_notificacion_plantilla_seq OWNER TO postgres;

--
-- Name: notificaciones_plantillas_id_notificacion_plantilla_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.notificaciones_plantillas_id_notificacion_plantilla_seq OWNED BY core.notificaciones_plantillas.id_notificacion_plantilla;


--
-- Name: paciente_profesional; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.paciente_profesional (
    id_paciente_profesional integer NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    tipo_relacion text DEFAULT 'ASIGNADO'::text NOT NULL,
    fec_asignacion timestamp with time zone DEFAULT now() NOT NULL,
    fec_finalizacion timestamp with time zone,
    pap_observaciones text,
    est_paciente_profesional boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT paciente_profesional_tipo_relacion_check CHECK ((tipo_relacion = ANY (ARRAY['ASIGNADO'::text, 'DERIVADO'::text, 'TEMPORAL'::text])))
);

ALTER TABLE ONLY core.paciente_profesional FORCE ROW LEVEL SECURITY;


ALTER TABLE core.paciente_profesional OWNER TO postgres;

--
-- Name: paciente_profesional_id_paciente_profesional_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.paciente_profesional_id_paciente_profesional_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.paciente_profesional_id_paciente_profesional_seq OWNER TO postgres;

--
-- Name: paciente_profesional_id_paciente_profesional_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.paciente_profesional_id_paciente_profesional_seq OWNED BY core.paciente_profesional.id_paciente_profesional;


--
-- Name: pacientes; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.pacientes (
    id_paciente integer NOT NULL,
    id_empresa integer NOT NULL,
    id_persona integer NOT NULL,
    pac_historia_clinica text,
    pac_observaciones text,
    est_paciente boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.pacientes FORCE ROW LEVEL SECURITY;


ALTER TABLE core.pacientes OWNER TO postgres;

--
-- Name: pacientes_id_paciente_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.pacientes_id_paciente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.pacientes_id_paciente_seq OWNER TO postgres;

--
-- Name: pacientes_id_paciente_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.pacientes_id_paciente_seq OWNED BY core.pacientes.id_paciente;


--
-- Name: pacientes_menores; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.pacientes_menores (
    id_paciente_menor integer NOT NULL,
    id_empresa integer NOT NULL,
    id_paciente integer NOT NULL,
    id_persona_tutor integer,
    pam_relacion_tutor text,
    pam_doc_tutor text,
    pam_email_tutor public.citext,
    pam_tel_tutor_alt text,
    pam_dom_tutor text,
    pam_nom_padre text,
    pam_tel_padre text,
    pam_nom_madre text,
    pam_tel_madre text,
    pam_grupo_sanguineo text,
    pam_alergias text,
    pam_medicacion_actual text,
    pam_educacion text,
    pam_colegio text,
    pam_tel_colegio text,
    pam_convive_con text,
    pam_custodia text,
    pam_autoriza_solo boolean DEFAULT false NOT NULL,
    est_paciente_menor boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT pacientes_menores_pam_convive_con_check CHECK (((pam_convive_con = ANY (ARRAY['AMBOS_PADRES'::text, 'MADRE'::text, 'PADRE'::text, 'TUTOR'::text])) OR (pam_convive_con IS NULL)))
);

ALTER TABLE ONLY core.pacientes_menores FORCE ROW LEVEL SECURITY;


ALTER TABLE core.pacientes_menores OWNER TO postgres;

--
-- Name: pacientes_menores_id_paciente_menor_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.pacientes_menores_id_paciente_menor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.pacientes_menores_id_paciente_menor_seq OWNER TO postgres;

--
-- Name: pacientes_menores_id_paciente_menor_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.pacientes_menores_id_paciente_menor_seq OWNED BY core.pacientes_menores.id_paciente_menor;


--
-- Name: paises; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.paises (
    id_pais integer NOT NULL,
    iso2 character(2),
    iso3 character(3),
    des_pais text NOT NULL,
    est_pais boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.paises OWNER TO postgres;

--
-- Name: paises_id_pais_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.paises_id_pais_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.paises_id_pais_seq OWNER TO postgres;

--
-- Name: paises_id_pais_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.paises_id_pais_seq OWNED BY core.paises.id_pais;


--
-- Name: password_history; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.password_history (
    id_password_history bigint NOT NULL,
    id_usuario integer NOT NULL,
    password_hash text NOT NULL,
    fec_cambio timestamp with time zone DEFAULT now() NOT NULL,
    est_password_history boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.password_history OWNER TO postgres;

--
-- Name: password_history_id_password_history_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.password_history_id_password_history_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.password_history_id_password_history_seq OWNER TO postgres;

--
-- Name: password_history_id_password_history_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.password_history_id_password_history_seq OWNED BY core.password_history.id_password_history;


--
-- Name: password_reset_tokens; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.password_reset_tokens (
    id_password_reset_token bigint NOT NULL,
    id_usuario integer NOT NULL,
    token text NOT NULL,
    fec_expiracion timestamp with time zone NOT NULL,
    esta_usado boolean DEFAULT false NOT NULL,
    est_password_reset_token boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.password_reset_tokens OWNER TO postgres;

--
-- Name: password_reset_tokens_id_password_reset_token_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.password_reset_tokens_id_password_reset_token_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.password_reset_tokens_id_password_reset_token_seq OWNER TO postgres;

--
-- Name: password_reset_tokens_id_password_reset_token_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.password_reset_tokens_id_password_reset_token_seq OWNED BY core.password_reset_tokens.id_password_reset_token;


--
-- Name: permisos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.permisos (
    id_permiso integer NOT NULL,
    cod_permiso text NOT NULL,
    des_permiso text,
    est_permiso boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.permisos OWNER TO postgres;

--
-- Name: permisos_id_permiso_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.permisos_id_permiso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.permisos_id_permiso_seq OWNER TO postgres;

--
-- Name: permisos_id_permiso_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.permisos_id_permiso_seq OWNED BY core.permisos.id_permiso;


--
-- Name: personas; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.personas (
    id_persona integer NOT NULL,
    id_empresa integer NOT NULL,
    id_tipo_documento integer NOT NULL,
    per_nro_documento text,
    per_nombres text NOT NULL,
    per_apellidos text NOT NULL,
    per_fec_nacimiento date,
    per_telefono text,
    per_email public.citext,
    id_genero integer,
    id_estado_civil integer,
    id_nivel_instruccion integer,
    id_profesion integer,
    id_ciudad integer,
    id_ciudad_nacimiento integer,
    per_direccion text,
    per_latitud numeric(10,8),
    per_longitud numeric(11,8),
    est_persona boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.personas FORCE ROW LEVEL SECURITY;


ALTER TABLE core.personas OWNER TO postgres;

--
-- Name: personas_id_persona_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.personas_id_persona_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.personas_id_persona_seq OWNER TO postgres;

--
-- Name: personas_id_persona_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.personas_id_persona_seq OWNED BY core.personas.id_persona;


--
-- Name: plan_modulos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.plan_modulos (
    id_plan_modulo integer NOT NULL,
    id_plan integer NOT NULL,
    id_modulo integer NOT NULL,
    est_plan_modulo boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.plan_modulos OWNER TO postgres;

--
-- Name: plan_modulos_id_plan_modulo_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.plan_modulos_id_plan_modulo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.plan_modulos_id_plan_modulo_seq OWNER TO postgres;

--
-- Name: plan_modulos_id_plan_modulo_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.plan_modulos_id_plan_modulo_seq OWNED BY core.plan_modulos.id_plan_modulo;


--
-- Name: planes; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.planes (
    id_plan integer NOT NULL,
    cod_plan text NOT NULL,
    des_plan text NOT NULL,
    es_prueba boolean DEFAULT false NOT NULL,
    duracion_meses smallint DEFAULT 1 NOT NULL,
    precio_base_mensual numeric(18,2) DEFAULT 0 NOT NULL,
    max_usuarios_base integer DEFAULT 1 NOT NULL,
    max_usuarios_techo integer,
    max_funcionarios_base integer,
    max_funcionarios_techo integer,
    max_especialistas integer,
    max_pacientes integer,
    max_sedes integer,
    est_plan boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    precio_anual numeric(18,2),
    precio_extra_usuario numeric(12,0) DEFAULT 0 NOT NULL,
    precio_extra_sede numeric(12,0) DEFAULT 0 NOT NULL,
    CONSTRAINT planes_duracion_meses_check CHECK ((duracion_meses > 0))
);


ALTER TABLE core.planes OWNER TO postgres;

--
-- Name: planes_id_plan_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.planes_id_plan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.planes_id_plan_seq OWNER TO postgres;

--
-- Name: planes_id_plan_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.planes_id_plan_seq OWNED BY core.planes.id_plan;


--
-- Name: preferencias_ui; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.preferencias_ui (
    id_preferencia_ui integer NOT NULL,
    id_empresa integer,
    id_usuario integer NOT NULL,
    preferencias jsonb DEFAULT '{}'::jsonb NOT NULL,
    est_preferencia_ui boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.preferencias_ui FORCE ROW LEVEL SECURITY;


ALTER TABLE core.preferencias_ui OWNER TO postgres;

--
-- Name: preferencias_ui_id_preferencia_ui_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.preferencias_ui_id_preferencia_ui_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.preferencias_ui_id_preferencia_ui_seq OWNER TO postgres;

--
-- Name: preferencias_ui_id_preferencia_ui_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.preferencias_ui_id_preferencia_ui_seq OWNED BY core.preferencias_ui.id_preferencia_ui;


--
-- Name: profesiones; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.profesiones (
    id_profesion integer NOT NULL,
    des_profesion text NOT NULL,
    est_profesion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.profesiones OWNER TO postgres;

--
-- Name: profesiones_id_profesion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.profesiones_id_profesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.profesiones_id_profesion_seq OWNER TO postgres;

--
-- Name: profesiones_id_profesion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.profesiones_id_profesion_seq OWNED BY core.profesiones.id_profesion;


--
-- Name: puntos_expedicion; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.puntos_expedicion (
    id_punto_expedicion integer NOT NULL,
    id_empresa integer NOT NULL,
    id_establecimiento integer NOT NULL,
    cod_punto_expedicion text NOT NULL,
    des_punto_expedicion text NOT NULL,
    est_punto_expedicion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_puntos_expedicion_codigo CHECK ((length(cod_punto_expedicion) = 3))
);

ALTER TABLE ONLY core.puntos_expedicion FORCE ROW LEVEL SECURITY;


ALTER TABLE core.puntos_expedicion OWNER TO postgres;

--
-- Name: puntos_expedicion_id_punto_expedicion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.puntos_expedicion_id_punto_expedicion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.puntos_expedicion_id_punto_expedicion_seq OWNER TO postgres;

--
-- Name: puntos_expedicion_id_punto_expedicion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.puntos_expedicion_id_punto_expedicion_seq OWNED BY core.puntos_expedicion.id_punto_expedicion;


--
-- Name: recordatorios; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.recordatorios (
    id_recordatorio bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_cita bigint NOT NULL,
    canal public.canal_notificacion_domain NOT NULL,
    minutos_antes integer NOT NULL,
    est_recordatorio boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT recordatorios_minutos_antes_check CHECK ((minutos_antes > 0))
);

ALTER TABLE ONLY core.recordatorios FORCE ROW LEVEL SECURITY;


ALTER TABLE core.recordatorios OWNER TO postgres;

--
-- Name: recordatorios_id_recordatorio_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.recordatorios_id_recordatorio_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.recordatorios_id_recordatorio_seq OWNER TO postgres;

--
-- Name: recordatorios_id_recordatorio_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.recordatorios_id_recordatorio_seq OWNED BY core.recordatorios.id_recordatorio;


--
-- Name: reportes_jobs; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.reportes_jobs (
    id_reporte_job bigint NOT NULL,
    id_empresa integer NOT NULL,
    tipo_reporte text NOT NULL,
    parametros jsonb DEFAULT '{}'::jsonb NOT NULL,
    estado_job text DEFAULT 'PENDIENTE'::text NOT NULL,
    fec_solicitud timestamp with time zone DEFAULT now() NOT NULL,
    fec_inicio_proceso timestamp with time zone,
    fec_completado timestamp with time zone,
    url_resultado text,
    error_mensaje text,
    est_reporte_job boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT reportes_jobs_estado_job_check CHECK ((estado_job = ANY (ARRAY['PENDIENTE'::text, 'PROCESANDO'::text, 'COMPLETADO'::text, 'FALLIDO'::text, 'CANCELADO'::text]))),
    CONSTRAINT reportes_jobs_tipo_reporte_check CHECK ((tipo_reporte = ANY (ARRAY['AGENDA_DIA'::text, 'CITAS_RANGO'::text, 'PACIENTES'::text, 'FINANZAS'::text, 'METRICAS_DIARIAS'::text, 'ESTADISTICAS_CLINICAS'::text])))
);

ALTER TABLE ONLY core.reportes_jobs FORCE ROW LEVEL SECURITY;


ALTER TABLE core.reportes_jobs OWNER TO postgres;

--
-- Name: reportes_jobs_id_reporte_job_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.reportes_jobs_id_reporte_job_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.reportes_jobs_id_reporte_job_seq OWNER TO postgres;

--
-- Name: reportes_jobs_id_reporte_job_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.reportes_jobs_id_reporte_job_seq OWNED BY core.reportes_jobs.id_reporte_job;


--
-- Name: reportes_jobs_log; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.reportes_jobs_log (
    id_reporte_job_log bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_reporte_job bigint NOT NULL,
    nivel text DEFAULT 'INFO'::text NOT NULL,
    mensaje text NOT NULL,
    detalle jsonb,
    fec_log timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT reportes_jobs_log_nivel_check CHECK ((nivel = ANY (ARRAY['INFO'::text, 'WARN'::text, 'ERROR'::text])))
);

ALTER TABLE ONLY core.reportes_jobs_log FORCE ROW LEVEL SECURITY;


ALTER TABLE core.reportes_jobs_log OWNER TO postgres;

--
-- Name: reportes_jobs_log_id_reporte_job_log_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.reportes_jobs_log_id_reporte_job_log_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.reportes_jobs_log_id_reporte_job_log_seq OWNER TO postgres;

--
-- Name: reportes_jobs_log_id_reporte_job_log_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.reportes_jobs_log_id_reporte_job_log_seq OWNED BY core.reportes_jobs_log.id_reporte_job_log;


--
-- Name: roles_base; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.roles_base (
    id_rol_base integer NOT NULL,
    cod_rol_base text NOT NULL,
    des_rol_base text NOT NULL,
    nivel smallint NOT NULL,
    est_rol_base boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT roles_base_nivel_check CHECK (((nivel >= 1) AND (nivel <= 5)))
);


ALTER TABLE core.roles_base OWNER TO postgres;

--
-- Name: roles_base_id_rol_base_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.roles_base_id_rol_base_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.roles_base_id_rol_base_seq OWNER TO postgres;

--
-- Name: roles_base_id_rol_base_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.roles_base_id_rol_base_seq OWNED BY core.roles_base.id_rol_base;


--
-- Name: roles_empresa; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.roles_empresa (
    id_rol_empresa integer NOT NULL,
    id_empresa integer NOT NULL,
    cod_rol_empresa text NOT NULL,
    des_rol_empresa text,
    est_rol_empresa boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.roles_empresa FORCE ROW LEVEL SECURITY;


ALTER TABLE core.roles_empresa OWNER TO postgres;

--
-- Name: roles_empresa_id_rol_empresa_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.roles_empresa_id_rol_empresa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.roles_empresa_id_rol_empresa_seq OWNER TO postgres;

--
-- Name: roles_empresa_id_rol_empresa_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.roles_empresa_id_rol_empresa_seq OWNED BY core.roles_empresa.id_rol_empresa;


--
-- Name: roles_empresa_permisos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.roles_empresa_permisos (
    id_rol_empresa_permiso integer NOT NULL,
    id_empresa integer NOT NULL,
    id_rol_empresa integer NOT NULL,
    id_permiso integer NOT NULL,
    est_rol_empresa_permiso boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.roles_empresa_permisos FORCE ROW LEVEL SECURITY;


ALTER TABLE core.roles_empresa_permisos OWNER TO postgres;

--
-- Name: roles_empresa_permisos_id_rol_empresa_permiso_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.roles_empresa_permisos_id_rol_empresa_permiso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.roles_empresa_permisos_id_rol_empresa_permiso_seq OWNER TO postgres;

--
-- Name: roles_empresa_permisos_id_rol_empresa_permiso_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.roles_empresa_permisos_id_rol_empresa_permiso_seq OWNED BY core.roles_empresa_permisos.id_rol_empresa_permiso;


--
-- Name: schema_migrations; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.schema_migrations (
    id_schema_migration bigint NOT NULL,
    version text NOT NULL,
    applied_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE core.schema_migrations OWNER TO postgres;

--
-- Name: schema_migrations_id_schema_migration_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.schema_migrations_id_schema_migration_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.schema_migrations_id_schema_migration_seq OWNER TO postgres;

--
-- Name: schema_migrations_id_schema_migration_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.schema_migrations_id_schema_migration_seq OWNED BY core.schema_migrations.id_schema_migration;


--
-- Name: sedes; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.sedes (
    id_sede integer NOT NULL,
    id_empresa integer NOT NULL,
    des_sede text NOT NULL,
    es_principal boolean DEFAULT false NOT NULL,
    id_ciudad integer,
    direccion text,
    telefono text,
    email public.citext,
    est_sede boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY core.sedes FORCE ROW LEVEL SECURITY;


ALTER TABLE core.sedes OWNER TO postgres;

--
-- Name: sedes_id_sede_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.sedes_id_sede_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.sedes_id_sede_seq OWNER TO postgres;

--
-- Name: sedes_id_sede_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.sedes_id_sede_seq OWNED BY core.sedes.id_sede;


--
-- Name: sesiones; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.sesiones (
    id_sesion bigint NOT NULL,
    id_empresa integer,
    id_usuario integer NOT NULL,
    token_sesion text NOT NULL,
    csrf_token text,
    refresh_token text,
    fec_inicio timestamp with time zone DEFAULT now() NOT NULL,
    fec_ultimo_ping timestamp with time zone DEFAULT now() NOT NULL,
    fec_expiracion timestamp with time zone NOT NULL,
    fec_cierre timestamp with time zone,
    ip_address text,
    user_agent text,
    tipo_cierre text,
    est_sesion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_sesiones_exp CHECK ((fec_expiracion > fec_inicio)),
    CONSTRAINT sesiones_tipo_cierre_check CHECK ((tipo_cierre = ANY (ARRAY['LOGOUT'::text, 'EXPIRACION'::text, 'REVOCACION'::text, 'ADMIN'::text])))
);

ALTER TABLE ONLY core.sesiones FORCE ROW LEVEL SECURITY;


ALTER TABLE core.sesiones OWNER TO postgres;

--
-- Name: sesiones_id_sesion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.sesiones_id_sesion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.sesiones_id_sesion_seq OWNER TO postgres;

--
-- Name: sesiones_id_sesion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.sesiones_id_sesion_seq OWNED BY core.sesiones.id_sesion;


--
-- Name: slots_agenda; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.slots_agenda (
    id_slot_agenda bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_sede integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_agenda_horario integer NOT NULL,
    id_especialista integer NOT NULL,
    id_especialidad integer,
    slot_inicio timestamp with time zone NOT NULL,
    slot_fin timestamp with time zone NOT NULL,
    estado_slot text DEFAULT 'DISPONIBLE'::text NOT NULL,
    est_slot_agenda boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_slots_horario CHECK ((slot_fin > slot_inicio)),
    CONSTRAINT slots_agenda_estado_slot_check CHECK ((estado_slot = ANY (ARRAY['DISPONIBLE'::text, 'RESERVADO'::text, 'BLOQUEADO'::text, 'OBSOLETO'::text])))
);

ALTER TABLE ONLY core.slots_agenda FORCE ROW LEVEL SECURITY;


ALTER TABLE core.slots_agenda OWNER TO postgres;

--
-- Name: slots_agenda_id_slot_agenda_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.slots_agenda_id_slot_agenda_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.slots_agenda_id_slot_agenda_seq OWNER TO postgres;

--
-- Name: slots_agenda_id_slot_agenda_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.slots_agenda_id_slot_agenda_seq OWNED BY core.slots_agenda.id_slot_agenda;


--
-- Name: suscripcion_excedentes; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.suscripcion_excedentes (
    id_suscripcion_excedente bigint NOT NULL,
    id_empresa integer NOT NULL,
    tipo_excedente public.tipo_excedente_domain NOT NULL,
    cantidad integer DEFAULT 1 NOT NULL,
    mes_facturacion date NOT NULL,
    esta_procesado boolean DEFAULT false NOT NULL,
    est_suscripcion_excedente boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT suscripcion_excedentes_cantidad_check CHECK ((cantidad > 0))
);

ALTER TABLE ONLY core.suscripcion_excedentes FORCE ROW LEVEL SECURITY;


ALTER TABLE core.suscripcion_excedentes OWNER TO postgres;

--
-- Name: suscripcion_excedentes_id_suscripcion_excedente_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.suscripcion_excedentes_id_suscripcion_excedente_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.suscripcion_excedentes_id_suscripcion_excedente_seq OWNER TO postgres;

--
-- Name: suscripcion_excedentes_id_suscripcion_excedente_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.suscripcion_excedentes_id_suscripcion_excedente_seq OWNED BY core.suscripcion_excedentes.id_suscripcion_excedente;


--
-- Name: suscripcion_expansiones; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.suscripcion_expansiones (
    id_expansion integer NOT NULL,
    id_suscripcion integer NOT NULL,
    tipo character varying(20) NOT NULL,
    cantidad integer NOT NULL,
    precio_unitario numeric(12,0) DEFAULT 0 NOT NULL,
    fec_inicio date DEFAULT CURRENT_DATE NOT NULL,
    fec_vencimiento date,
    obs text,
    est_expansion boolean DEFAULT true NOT NULL,
    id_usuario_creacion integer,
    fec_creacion timestamp without time zone DEFAULT now(),
    id_usuario_modificacion integer,
    fec_modificacion timestamp without time zone,
    CONSTRAINT suscripcion_expansiones_cantidad_check CHECK ((cantidad > 0)),
    CONSTRAINT suscripcion_expansiones_tipo_check CHECK (((tipo)::text = ANY (ARRAY[('USUARIOS'::character varying)::text, ('FUNCIONARIOS'::character varying)::text])))
);


ALTER TABLE core.suscripcion_expansiones OWNER TO postgres;

--
-- Name: suscripcion_expansiones_id_expansion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.suscripcion_expansiones_id_expansion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.suscripcion_expansiones_id_expansion_seq OWNER TO postgres;

--
-- Name: suscripcion_expansiones_id_expansion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.suscripcion_expansiones_id_expansion_seq OWNED BY core.suscripcion_expansiones.id_expansion;


--
-- Name: suscripciones; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.suscripciones (
    id_suscripcion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_plan integer NOT NULL,
    nro_contrato text,
    fec_inicio timestamp with time zone NOT NULL,
    fec_vencimiento timestamp with time zone NOT NULL,
    max_funcionarios_contratados integer,
    est_suscripcion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    max_usuarios_contratados integer,
    es_anual boolean DEFAULT false NOT NULL,
    CONSTRAINT chk_suscripciones_fechas CHECK ((fec_vencimiento > fec_inicio))
);

ALTER TABLE ONLY core.suscripciones FORCE ROW LEVEL SECURITY;


ALTER TABLE core.suscripciones OWNER TO postgres;

--
-- Name: suscripciones_id_suscripcion_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.suscripciones_id_suscripcion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.suscripciones_id_suscripcion_seq OWNER TO postgres;

--
-- Name: suscripciones_id_suscripcion_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.suscripciones_id_suscripcion_seq OWNED BY core.suscripciones.id_suscripcion;


--
-- Name: tipos_clinicos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.tipos_clinicos (
    cod_tipo_clinico character varying(30) NOT NULL,
    des_tipo_clinico text NOT NULL,
    tabs_config jsonb DEFAULT '{}'::jsonb NOT NULL,
    des_descripcion text,
    est_tipo_clinico boolean DEFAULT true NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE core.tipos_clinicos OWNER TO postgres;

--
-- Name: TABLE tipos_clinicos; Type: COMMENT; Schema: core; Owner: postgres
--

COMMENT ON TABLE core.tipos_clinicos IS 'Catálogo global de perfiles clínicos. Define qué secciones del episodio son relevantes por especialidad.';


--
-- Name: COLUMN tipos_clinicos.tabs_config; Type: COMMENT; Schema: core; Owner: postgres
--

COMMENT ON COLUMN core.tipos_clinicos.tabs_config IS 'JSONB con flags de visibilidad de tabs en el episodio. Ej: {"signos_vitales":false,"psicologia":true}';


--
-- Name: tipos_comprobantes; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.tipos_comprobantes (
    id_tipo_comprobante integer NOT NULL,
    cod_tipo_comprobante text NOT NULL,
    des_tipo_comprobante text NOT NULL,
    est_tipo_comprobante boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    cod_tipo_de character(2),
    est_genera_cuenta_cobrar boolean DEFAULT false NOT NULL,
    est_afecta_libro_ventas boolean DEFAULT true NOT NULL,
    CONSTRAINT chk_tipo_comprobante_cod_tipo_de CHECK (((cod_tipo_de IS NULL) OR (cod_tipo_de = ANY (ARRAY['01'::bpchar, '04'::bpchar, '05'::bpchar, '06'::bpchar, '07'::bpchar]))))
);


ALTER TABLE core.tipos_comprobantes OWNER TO postgres;

--
-- Name: tipos_comprobantes_id_tipo_comprobante_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.tipos_comprobantes_id_tipo_comprobante_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.tipos_comprobantes_id_tipo_comprobante_seq OWNER TO postgres;

--
-- Name: tipos_comprobantes_id_tipo_comprobante_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.tipos_comprobantes_id_tipo_comprobante_seq OWNED BY core.tipos_comprobantes.id_tipo_comprobante;


--
-- Name: tipos_documentos_identidad; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.tipos_documentos_identidad (
    id_tipo_documento integer NOT NULL,
    cod_sifen smallint NOT NULL,
    cod_tipo_documento text NOT NULL,
    des_tipo_documento text NOT NULL,
    max_longitud smallint DEFAULT 20 NOT NULL,
    patron_regex text,
    es_paraguayo boolean DEFAULT false NOT NULL,
    est_tipo_documento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT tipos_documentos_identidad_cod_sifen_check CHECK (((cod_sifen >= 1) AND (cod_sifen <= 9)))
);


ALTER TABLE core.tipos_documentos_identidad OWNER TO postgres;

--
-- Name: tipos_documentos_identidad_id_tipo_documento_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.tipos_documentos_identidad_id_tipo_documento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.tipos_documentos_identidad_id_tipo_documento_seq OWNER TO postgres;

--
-- Name: tipos_documentos_identidad_id_tipo_documento_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.tipos_documentos_identidad_id_tipo_documento_seq OWNED BY core.tipos_documentos_identidad.id_tipo_documento;


--
-- Name: tipos_impuestos; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.tipos_impuestos (
    id_tipo_impuesto integer NOT NULL,
    cod_tipo_impuesto text NOT NULL,
    des_tipo_impuesto text NOT NULL,
    porcentaje numeric(6,3),
    est_tipo_impuesto boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.tipos_impuestos OWNER TO postgres;

--
-- Name: tipos_impuestos_id_tipo_impuesto_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.tipos_impuestos_id_tipo_impuesto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.tipos_impuestos_id_tipo_impuesto_seq OWNER TO postgres;

--
-- Name: tipos_impuestos_id_tipo_impuesto_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.tipos_impuestos_id_tipo_impuesto_seq OWNED BY core.tipos_impuestos.id_tipo_impuesto;


--
-- Name: tipos_items; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.tipos_items (
    id_tipo_item integer NOT NULL,
    cod_tipo_item text NOT NULL,
    des_tipo_item text NOT NULL,
    est_tipo_item boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.tipos_items OWNER TO postgres;

--
-- Name: tipos_items_id_tipo_item_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.tipos_items_id_tipo_item_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.tipos_items_id_tipo_item_seq OWNER TO postgres;

--
-- Name: tipos_items_id_tipo_item_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.tipos_items_id_tipo_item_seq OWNED BY core.tipos_items.id_tipo_item;


--
-- Name: usuarios; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.usuarios (
    id_usuario integer NOT NULL,
    id_empresa integer,
    email public.citext,
    usu_nick public.citext NOT NULL,
    password_hash text NOT NULL,
    requiere_cambio_password boolean DEFAULT false NOT NULL,
    fec_ultimo_login timestamp with time zone,
    ip_ultimo_login text,
    user_agent_ultimo_login text,
    intentos_fallidos integer DEFAULT 0 NOT NULL,
    fec_ultimo_intento_fallido timestamp with time zone,
    bloqueado_hasta timestamp with time zone,
    est_usuario boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    mfa_habilitado boolean DEFAULT false NOT NULL,
    mfa_metodo character varying(10),
    mfa_totp_secret text,
    mfa_totp_verified boolean DEFAULT false NOT NULL,
    CONSTRAINT chk_usuarios_email CHECK (((email IS NULL) OR (email OPERATOR(public.~*) '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::public.citext))),
    CONSTRAINT usuarios_mfa_metodo_check CHECK (((mfa_metodo)::text = ANY (ARRAY[('EMAIL'::character varying)::text, ('TOTP'::character varying)::text])))
);

ALTER TABLE ONLY core.usuarios FORCE ROW LEVEL SECURITY;


ALTER TABLE core.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.usuarios_id_usuario_seq OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.usuarios_id_usuario_seq OWNED BY core.usuarios.id_usuario;


--
-- Name: usuarios_roles_base; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.usuarios_roles_base (
    id_usuario_rol_base integer NOT NULL,
    id_usuario integer NOT NULL,
    id_rol_base integer NOT NULL,
    est_usuario_rol_base boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);


ALTER TABLE core.usuarios_roles_base OWNER TO postgres;

--
-- Name: usuarios_roles_base_id_usuario_rol_base_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.usuarios_roles_base_id_usuario_rol_base_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.usuarios_roles_base_id_usuario_rol_base_seq OWNER TO postgres;

--
-- Name: usuarios_roles_base_id_usuario_rol_base_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.usuarios_roles_base_id_usuario_rol_base_seq OWNED BY core.usuarios_roles_base.id_usuario_rol_base;


--
-- Name: usuarios_roles_empresa; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.usuarios_roles_empresa (
    id_usuario_rol_empresa integer NOT NULL,
    id_empresa integer NOT NULL,
    id_usuario integer NOT NULL,
    id_rol_empresa integer NOT NULL,
    orden_rol smallint DEFAULT 1 NOT NULL,
    est_usuario_rol_empresa boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint DEFAULT 1 NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_ure_orden_rol CHECK (((orden_rol >= 1) AND (orden_rol <= 3)))
);

ALTER TABLE ONLY core.usuarios_roles_empresa FORCE ROW LEVEL SECURITY;


ALTER TABLE core.usuarios_roles_empresa OWNER TO postgres;

--
-- Name: usuarios_roles_empresa_id_usuario_rol_empresa_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.usuarios_roles_empresa_id_usuario_rol_empresa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.usuarios_roles_empresa_id_usuario_rol_empresa_seq OWNER TO postgres;

--
-- Name: usuarios_roles_empresa_id_usuario_rol_empresa_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.usuarios_roles_empresa_id_usuario_rol_empresa_seq OWNED BY core.usuarios_roles_empresa.id_usuario_rol_empresa;


--
-- Name: aperturas_caja; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.aperturas_caja (
    id_apertura_caja bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_caja integer NOT NULL,
    id_usuario_apertura bigint NOT NULL,
    fec_apertura timestamp with time zone DEFAULT now() NOT NULL,
    mto_saldo_inicial numeric(18,2) DEFAULT 0 NOT NULL,
    id_usuario_cierre bigint,
    fec_cierre timestamp with time zone,
    mto_saldo_calculado numeric(18,2),
    mto_saldo_real numeric(18,2),
    mto_diferencia numeric(18,2) GENERATED ALWAYS AS ((mto_saldo_real - mto_saldo_calculado)) STORED,
    des_observaciones_apertura text,
    des_observaciones_cierre text,
    cod_estado text DEFAULT 'ABIERTA'::text NOT NULL,
    est_apertura_caja boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT aperturas_caja_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['ABIERTA'::text, 'CERRADA'::text])))
);

ALTER TABLE ONLY facturacion.aperturas_caja FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.aperturas_caja OWNER TO postgres;

--
-- Name: aperturas_caja_id_apertura_caja_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.aperturas_caja_id_apertura_caja_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.aperturas_caja_id_apertura_caja_seq OWNER TO postgres;

--
-- Name: aperturas_caja_id_apertura_caja_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.aperturas_caja_id_apertura_caja_seq OWNED BY facturacion.aperturas_caja.id_apertura_caja;


--
-- Name: arqueos_caja; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.arqueos_caja (
    id_arqueo_caja bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_caja integer NOT NULL,
    id_apertura_caja bigint NOT NULL,
    id_usuario_arqueo bigint NOT NULL,
    fec_arqueo timestamp with time zone DEFAULT now() NOT NULL,
    dat_desglose jsonb,
    mto_efectivo_contado numeric(18,2) DEFAULT 0 NOT NULL,
    mto_cheques numeric(18,2) DEFAULT 0 NOT NULL,
    mto_tarjetas numeric(18,2) DEFAULT 0 NOT NULL,
    mto_transferencias numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total_contado numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total_calculado numeric(18,2) DEFAULT 0 NOT NULL,
    mto_diferencia numeric(18,2) GENERATED ALWAYS AS ((mto_total_contado - mto_total_calculado)) STORED,
    des_observaciones text,
    est_arqueo_caja boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY facturacion.arqueos_caja FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.arqueos_caja OWNER TO postgres;

--
-- Name: arqueos_caja_id_arqueo_caja_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.arqueos_caja_id_arqueo_caja_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.arqueos_caja_id_arqueo_caja_seq OWNER TO postgres;

--
-- Name: arqueos_caja_id_arqueo_caja_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.arqueos_caja_id_arqueo_caja_seq OWNED BY facturacion.arqueos_caja.id_arqueo_caja;


--
-- Name: autofactura_detalle; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.autofactura_detalle (
    id_autofactura_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_autofactura bigint NOT NULL,
    nro_linea smallint NOT NULL,
    id_item bigint,
    cod_item character varying(30),
    des_descripcion character varying(2000) NOT NULL,
    cod_unidad_medida smallint DEFAULT 77 NOT NULL,
    dec_cantidad numeric(14,4) NOT NULL,
    mto_precio_unitario numeric(18,2) NOT NULL,
    mto_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    cod_afectacion_iva smallint NOT NULL,
    pct_proporcion_gravada numeric(5,2) DEFAULT 100 NOT NULL,
    pct_iva numeric(5,2) NOT NULL,
    mto_base_gravada numeric(18,2) DEFAULT 0 NOT NULL,
    mto_base_exenta numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    est_autofactura_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT autofactura_detalle_cod_afectacion_iva_check CHECK ((cod_afectacion_iva = ANY (ARRAY[1, 2, 3, 4]))),
    CONSTRAINT autofactura_detalle_dec_cantidad_check CHECK ((dec_cantidad > (0)::numeric)),
    CONSTRAINT autofactura_detalle_mto_descuento_check CHECK ((mto_descuento >= (0)::numeric)),
    CONSTRAINT autofactura_detalle_pct_iva_check CHECK ((pct_iva = ANY (ARRAY[(0)::numeric, (5)::numeric, (10)::numeric]))),
    CONSTRAINT autofactura_detalle_pct_proporcion_gravada_check CHECK (((pct_proporcion_gravada >= (0)::numeric) AND (pct_proporcion_gravada <= (100)::numeric)))
);

ALTER TABLE ONLY facturacion.autofactura_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.autofactura_detalle OWNER TO postgres;

--
-- Name: autofactura_detalle_id_autofactura_detalle_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.autofactura_detalle_id_autofactura_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.autofactura_detalle_id_autofactura_detalle_seq OWNER TO postgres;

--
-- Name: autofactura_detalle_id_autofactura_detalle_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.autofactura_detalle_id_autofactura_detalle_seq OWNED BY facturacion.autofactura_detalle.id_autofactura_detalle;


--
-- Name: autofacturas; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.autofacturas (
    id_autofactura bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_autofactura character varying(15) NOT NULL,
    id_timbrado integer NOT NULL,
    id_establecimiento integer NOT NULL,
    id_punto_expedicion integer NOT NULL,
    cod_serie character(2),
    des_nombre_vendedor character varying(255) NOT NULL,
    nro_documento_vendedor character varying(20) NOT NULL,
    dat_vendedor jsonb,
    fec_emision timestamp with time zone NOT NULL,
    id_moneda integer NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    id_de bigint,
    cod_estado text DEFAULT 'BORRADOR'::text NOT NULL,
    des_observaciones text,
    est_autofactura boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT autofacturas_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['BORRADOR'::text, 'EMITIDA'::text, 'ANULADA'::text])))
);

ALTER TABLE ONLY facturacion.autofacturas FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.autofacturas OWNER TO postgres;

--
-- Name: autofacturas_id_autofactura_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.autofacturas_id_autofactura_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.autofacturas_id_autofactura_seq OWNER TO postgres;

--
-- Name: autofacturas_id_autofactura_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.autofacturas_id_autofactura_seq OWNED BY facturacion.autofacturas.id_autofactura;


--
-- Name: cajas; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.cajas (
    id_caja integer NOT NULL,
    id_empresa integer NOT NULL,
    id_sede integer NOT NULL,
    cod_caja character varying(15) NOT NULL,
    des_caja character varying(100) NOT NULL,
    est_caja boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY facturacion.cajas FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.cajas OWNER TO postgres;

--
-- Name: cajas_id_caja_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.cajas_id_caja_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.cajas_id_caja_seq OWNER TO postgres;

--
-- Name: cajas_id_caja_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.cajas_id_caja_seq OWNED BY facturacion.cajas.id_caja;


--
-- Name: categorias_items; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.categorias_items (
    id_categoria_item integer NOT NULL,
    id_empresa integer,
    des_categoria_item character varying(100) NOT NULL,
    est_categoria_item boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY facturacion.categorias_items FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.categorias_items OWNER TO postgres;

--
-- Name: categorias_items_id_categoria_item_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.categorias_items_id_categoria_item_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.categorias_items_id_categoria_item_seq OWNER TO postgres;

--
-- Name: categorias_items_id_categoria_item_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.categorias_items_id_categoria_item_seq OWNED BY facturacion.categorias_items.id_categoria_item;


--
-- Name: cheques_recibidos; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.cheques_recibidos (
    id_cheque_recibido bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_entidad_bancaria integer NOT NULL,
    nro_cheque character varying(30) NOT NULL,
    nro_cuenta_origen character varying(30),
    des_titular character varying(200) NOT NULL,
    mto_importe numeric(18,2) NOT NULL,
    fec_emision date NOT NULL,
    fec_cobro date NOT NULL,
    cod_estado text DEFAULT 'AL_COBRO'::text NOT NULL,
    est_cheque_recibido boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT cheques_recibidos_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['AL_COBRO'::text, 'DEPOSITADO'::text, 'COBRADO'::text, 'RECHAZADO'::text]))),
    CONSTRAINT cheques_recibidos_mto_importe_check CHECK ((mto_importe > (0)::numeric))
);

ALTER TABLE ONLY facturacion.cheques_recibidos FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.cheques_recibidos OWNER TO postgres;

--
-- Name: cheques_recibidos_id_cheque_recibido_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.cheques_recibidos_id_cheque_recibido_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.cheques_recibidos_id_cheque_recibido_seq OWNER TO postgres;

--
-- Name: cheques_recibidos_id_cheque_recibido_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.cheques_recibidos_id_cheque_recibido_seq OWNED BY facturacion.cheques_recibidos.id_cheque_recibido;


--
-- Name: cobranza_detalle; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.cobranza_detalle (
    id_cobranza_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_cobranza bigint NOT NULL,
    id_forma_cobro integer NOT NULL,
    mto_importe numeric(18,2) NOT NULL,
    id_marca_tarjeta integer,
    id_entidad_bancaria integer,
    nro_operacion character varying(50),
    id_cheque_recibido bigint,
    est_cobranza_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT cobranza_detalle_mto_importe_check CHECK ((mto_importe > (0)::numeric))
);

ALTER TABLE ONLY facturacion.cobranza_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.cobranza_detalle OWNER TO postgres;

--
-- Name: cobranza_detalle_id_cobranza_detalle_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.cobranza_detalle_id_cobranza_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.cobranza_detalle_id_cobranza_detalle_seq OWNER TO postgres;

--
-- Name: cobranza_detalle_id_cobranza_detalle_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.cobranza_detalle_id_cobranza_detalle_seq OWNED BY facturacion.cobranza_detalle.id_cobranza_detalle;


--
-- Name: cobranzas; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.cobranzas (
    id_cobranza bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_cobranza character varying(30) NOT NULL,
    id_cuenta_cobrar bigint,
    id_cuota_cobrar bigint,
    id_paciente integer,
    id_entidad_pagadora integer,
    id_caja integer NOT NULL,
    id_apertura_caja bigint NOT NULL,
    fec_cobranza timestamp with time zone DEFAULT now() NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    cod_estado text DEFAULT 'REGISTRADA'::text NOT NULL,
    des_observaciones text,
    est_cobranza boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT cobranzas_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['REGISTRADA'::text, 'ANULADA'::text]))),
    CONSTRAINT cobranzas_mto_total_check CHECK ((mto_total > (0)::numeric))
);

ALTER TABLE ONLY facturacion.cobranzas FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.cobranzas OWNER TO postgres;

--
-- Name: cobranzas_id_cobranza_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.cobranzas_id_cobranza_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.cobranzas_id_cobranza_seq OWNER TO postgres;

--
-- Name: cobranzas_id_cobranza_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.cobranzas_id_cobranza_seq OWNED BY facturacion.cobranzas.id_cobranza;


--
-- Name: cuentas_cobrar; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.cuentas_cobrar (
    id_cuenta_cobrar bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_cuenta_cobrar character varying(30) NOT NULL,
    id_factura bigint,
    id_nota_debito bigint,
    id_paciente integer,
    id_entidad_pagadora integer,
    fec_emision date NOT NULL,
    fec_vencimiento date NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    mto_pagado numeric(18,2) DEFAULT 0 NOT NULL,
    mto_pendiente numeric(18,2) GENERATED ALWAYS AS ((mto_total - mto_pagado)) STORED,
    cod_estado text DEFAULT 'PENDIENTE'::text NOT NULL,
    des_observaciones text,
    est_cuenta_cobrar boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_cuenta_cobrar_origen_unico CHECK (((id_factura IS NOT NULL) <> (id_nota_debito IS NOT NULL))),
    CONSTRAINT cuentas_cobrar_check CHECK (((mto_pagado >= (0)::numeric) AND (mto_pagado <= mto_total))),
    CONSTRAINT cuentas_cobrar_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['PENDIENTE'::text, 'PARCIAL'::text, 'PAGADA'::text, 'VENCIDA'::text]))),
    CONSTRAINT cuentas_cobrar_mto_total_check CHECK ((mto_total > (0)::numeric))
);

ALTER TABLE ONLY facturacion.cuentas_cobrar FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.cuentas_cobrar OWNER TO postgres;

--
-- Name: cuentas_cobrar_id_cuenta_cobrar_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.cuentas_cobrar_id_cuenta_cobrar_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.cuentas_cobrar_id_cuenta_cobrar_seq OWNER TO postgres;

--
-- Name: cuentas_cobrar_id_cuenta_cobrar_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.cuentas_cobrar_id_cuenta_cobrar_seq OWNED BY facturacion.cuentas_cobrar.id_cuenta_cobrar;


--
-- Name: cuotas_cobrar; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.cuotas_cobrar (
    id_cuota_cobrar bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_cuenta_cobrar bigint NOT NULL,
    nro_cuota smallint NOT NULL,
    fec_vencimiento date NOT NULL,
    mto_cuota numeric(18,2) NOT NULL,
    mto_pagado numeric(18,2) DEFAULT 0 NOT NULL,
    cod_estado text DEFAULT 'PENDIENTE'::text NOT NULL,
    est_cuota_cobrar boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT cuotas_cobrar_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['PENDIENTE'::text, 'PARCIAL'::text, 'PAGADA'::text, 'VENCIDA'::text]))),
    CONSTRAINT cuotas_cobrar_mto_cuota_check CHECK ((mto_cuota > (0)::numeric)),
    CONSTRAINT cuotas_cobrar_mto_pagado_check CHECK ((mto_pagado >= (0)::numeric)),
    CONSTRAINT cuotas_cobrar_nro_cuota_check CHECK ((nro_cuota > 0))
);

ALTER TABLE ONLY facturacion.cuotas_cobrar FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.cuotas_cobrar OWNER TO postgres;

--
-- Name: cuotas_cobrar_id_cuota_cobrar_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.cuotas_cobrar_id_cuota_cobrar_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.cuotas_cobrar_id_cuota_cobrar_seq OWNER TO postgres;

--
-- Name: cuotas_cobrar_id_cuota_cobrar_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.cuotas_cobrar_id_cuota_cobrar_seq OWNED BY facturacion.cuotas_cobrar.id_cuota_cobrar;


--
-- Name: documentos_electronicos; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.documentos_electronicos (
    id_de bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_tipo_comprobante integer NOT NULL,
    cod_cdc character(44) NOT NULL,
    nro_timbrado character(8) NOT NULL,
    cod_establecimiento character(3) NOT NULL,
    cod_punto_expedicion character(3) NOT NULL,
    nro_documento character(7) NOT NULL,
    cod_serie character(2),
    cod_seguridad character(9) NOT NULL,
    cod_ambiente text NOT NULL,
    fec_emision timestamp with time zone NOT NULL,
    fec_firma timestamp with time zone,
    cod_estado text DEFAULT 'GENERADO'::text NOT NULL,
    des_xml_path text,
    des_kude_path text,
    nro_lote_sifen character varying(20),
    cod_respuesta_sifen character(4),
    des_msg_respuesta text,
    des_xml_respuesta_path text,
    cnt_reintentos smallint DEFAULT 0 NOT NULL,
    est_de boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT documentos_electronicos_cnt_reintentos_check CHECK ((cnt_reintentos >= 0)),
    CONSTRAINT documentos_electronicos_cod_ambiente_check CHECK ((cod_ambiente = ANY (ARRAY['TEST'::text, 'PRODUCCION'::text]))),
    CONSTRAINT documentos_electronicos_cod_cdc_check CHECK ((cod_cdc ~ '^[0-9]{44}$'::text)),
    CONSTRAINT documentos_electronicos_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['GENERADO'::text, 'FIRMADO'::text, 'ENCOLADO'::text, 'ENVIADO'::text, 'APROBADO'::text, 'APROBADO_OBS'::text, 'RECHAZADO'::text, 'CANCELADO'::text])))
);

ALTER TABLE ONLY facturacion.documentos_electronicos FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.documentos_electronicos OWNER TO postgres;

--
-- Name: documentos_electronicos_id_de_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.documentos_electronicos_id_de_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.documentos_electronicos_id_de_seq OWNER TO postgres;

--
-- Name: documentos_electronicos_id_de_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.documentos_electronicos_id_de_seq OWNED BY facturacion.documentos_electronicos.id_de;


--
-- Name: entidades_bancarias; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.entidades_bancarias (
    id_entidad_bancaria integer NOT NULL,
    cod_entidad_bancaria character varying(20) NOT NULL,
    des_entidad_bancaria character varying(100) NOT NULL,
    nro_ruc character varying(8),
    cod_dv_ruc character(1),
    cod_tipo text NOT NULL,
    est_entidad_bancaria boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT entidades_bancarias_cod_tipo_check CHECK ((cod_tipo = ANY (ARRAY['BANCO'::text, 'FINANCIERA'::text, 'COOPERATIVA'::text, 'PROCESADORA_TARJETA'::text])))
);


ALTER TABLE facturacion.entidades_bancarias OWNER TO postgres;

--
-- Name: entidades_bancarias_id_entidad_bancaria_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.entidades_bancarias_id_entidad_bancaria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.entidades_bancarias_id_entidad_bancaria_seq OWNER TO postgres;

--
-- Name: entidades_bancarias_id_entidad_bancaria_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.entidades_bancarias_id_entidad_bancaria_seq OWNED BY facturacion.entidades_bancarias.id_entidad_bancaria;


--
-- Name: entidades_pagadoras; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.entidades_pagadoras (
    id_entidad_pagadora integer NOT NULL,
    id_empresa integer NOT NULL,
    des_entidad_pagadora character varying(200) NOT NULL,
    nro_ruc character varying(8),
    cod_dv_ruc character(1),
    cod_tipo text NOT NULL,
    id_departamento integer,
    id_ciudad integer,
    des_direccion text,
    des_email character varying(150),
    nro_telefono character varying(30),
    est_entidad_pagadora boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT entidades_pagadoras_cod_tipo_check CHECK ((cod_tipo = ANY (ARRAY['OBRA_SOCIAL'::text, 'SEGURO'::text, 'EMPRESA'::text, 'MUTUAL'::text])))
);

ALTER TABLE ONLY facturacion.entidades_pagadoras FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.entidades_pagadoras OWNER TO postgres;

--
-- Name: entidades_pagadoras_id_entidad_pagadora_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.entidades_pagadoras_id_entidad_pagadora_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.entidades_pagadoras_id_entidad_pagadora_seq OWNER TO postgres;

--
-- Name: entidades_pagadoras_id_entidad_pagadora_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.entidades_pagadoras_id_entidad_pagadora_seq OWNED BY facturacion.entidades_pagadoras.id_entidad_pagadora;


--
-- Name: factura_detalle; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.factura_detalle (
    id_factura_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_factura bigint NOT NULL,
    nro_linea smallint NOT NULL,
    id_item bigint,
    cod_item character varying(30),
    des_descripcion character varying(2000) NOT NULL,
    cod_unidad_medida smallint DEFAULT 77 NOT NULL,
    dec_cantidad numeric(14,4) NOT NULL,
    mto_precio_unitario numeric(18,2) NOT NULL,
    mto_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    cod_afectacion_iva smallint NOT NULL,
    pct_proporcion_gravada numeric(5,2) DEFAULT 100 NOT NULL,
    pct_iva numeric(5,2) NOT NULL,
    mto_base_gravada numeric(18,2) DEFAULT 0 NOT NULL,
    mto_base_exenta numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    est_factura_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT factura_detalle_cod_afectacion_iva_check CHECK ((cod_afectacion_iva = ANY (ARRAY[1, 2, 3, 4]))),
    CONSTRAINT factura_detalle_dec_cantidad_check CHECK ((dec_cantidad > (0)::numeric)),
    CONSTRAINT factura_detalle_mto_descuento_check CHECK ((mto_descuento >= (0)::numeric)),
    CONSTRAINT factura_detalle_pct_iva_check CHECK ((pct_iva = ANY (ARRAY[(0)::numeric, (5)::numeric, (10)::numeric]))),
    CONSTRAINT factura_detalle_pct_proporcion_gravada_check CHECK (((pct_proporcion_gravada >= (0)::numeric) AND (pct_proporcion_gravada <= (100)::numeric)))
);

ALTER TABLE ONLY facturacion.factura_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.factura_detalle OWNER TO postgres;

--
-- Name: factura_detalle_id_factura_detalle_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.factura_detalle_id_factura_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.factura_detalle_id_factura_detalle_seq OWNER TO postgres;

--
-- Name: factura_detalle_id_factura_detalle_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.factura_detalle_id_factura_detalle_seq OWNED BY facturacion.factura_detalle.id_factura_detalle;


--
-- Name: factura_medios_pago; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.factura_medios_pago (
    id_factura_medio_pago bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_factura bigint NOT NULL,
    id_forma_cobro integer NOT NULL,
    mto_importe numeric(18,2) NOT NULL,
    id_moneda integer,
    mto_tipo_cambio numeric(13,4),
    cnt_cuotas smallint,
    dat_detalle jsonb,
    est_factura_medio_pago boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT factura_medios_pago_cnt_cuotas_check CHECK (((cnt_cuotas IS NULL) OR (cnt_cuotas > 0))),
    CONSTRAINT factura_medios_pago_mto_importe_check CHECK ((mto_importe > (0)::numeric))
);

ALTER TABLE ONLY facturacion.factura_medios_pago FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.factura_medios_pago OWNER TO postgres;

--
-- Name: factura_medios_pago_id_factura_medio_pago_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.factura_medios_pago_id_factura_medio_pago_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.factura_medios_pago_id_factura_medio_pago_seq OWNER TO postgres;

--
-- Name: factura_medios_pago_id_factura_medio_pago_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.factura_medios_pago_id_factura_medio_pago_seq OWNED BY facturacion.factura_medios_pago.id_factura_medio_pago;


--
-- Name: facturas; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.facturas (
    id_factura bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_factura character varying(15) NOT NULL,
    id_timbrado integer NOT NULL,
    id_establecimiento integer NOT NULL,
    id_punto_expedicion integer NOT NULL,
    cod_serie character(2),
    id_episodio bigint,
    id_contrato_tratamiento bigint,
    id_plan_tratamiento bigint,
    des_origen text,
    id_paciente integer,
    id_receptor integer,
    id_entidad_pagadora integer,
    cod_naturaleza_receptor smallint NOT NULL,
    cod_tipo_operacion smallint NOT NULL,
    id_tipo_documento integer,
    nro_documento_receptor character varying(20),
    nro_ruc_receptor character varying(8),
    cod_dv_receptor character(1),
    des_nombre_receptor character varying(255) NOT NULL,
    des_direccion_receptor character varying(255),
    nro_casa_receptor integer,
    id_pais_receptor integer NOT NULL,
    id_departamento_receptor integer,
    id_ciudad_receptor integer,
    des_email_receptor character varying(150),
    id_condicion_venta integer NOT NULL,
    cod_tipo_transaccion smallint DEFAULT 2 NOT NULL,
    id_moneda integer NOT NULL,
    mto_tipo_cambio numeric(13,4),
    fec_emision timestamp with time zone NOT NULL,
    fec_vencimiento date,
    mto_subtotal_exento numeric(18,2) DEFAULT 0 NOT NULL,
    mto_subtotal_gravado_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_subtotal_gravado_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_descuento_total numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total_iva numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    des_total_letras text,
    id_de bigint,
    cod_estado text DEFAULT 'BORRADOR'::text NOT NULL,
    des_observaciones text,
    est_factura boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_factura_contribuyente_ruc CHECK ((((cod_naturaleza_receptor = 1) AND (nro_ruc_receptor IS NOT NULL)) OR (cod_naturaleza_receptor = 2))),
    CONSTRAINT chk_factura_pagador_exclusivo CHECK (((id_receptor IS NULL) OR (id_entidad_pagadora IS NULL))),
    CONSTRAINT chk_factura_receptor_identificado CHECK (((id_paciente IS NOT NULL) OR (id_receptor IS NOT NULL) OR (id_entidad_pagadora IS NOT NULL) OR (cod_naturaleza_receptor = 2))),
    CONSTRAINT facturas_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['BORRADOR'::text, 'EMITIDA'::text, 'ANULADA'::text]))),
    CONSTRAINT facturas_cod_naturaleza_receptor_check CHECK ((cod_naturaleza_receptor = ANY (ARRAY[1, 2]))),
    CONSTRAINT facturas_cod_tipo_operacion_check CHECK (((cod_tipo_operacion >= 1) AND (cod_tipo_operacion <= 4))),
    CONSTRAINT facturas_cod_tipo_transaccion_check CHECK (((cod_tipo_transaccion >= 1) AND (cod_tipo_transaccion <= 13)))
);

ALTER TABLE ONLY facturacion.facturas FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.facturas OWNER TO postgres;

--
-- Name: facturas_id_factura_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.facturas_id_factura_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.facturas_id_factura_seq OWNER TO postgres;

--
-- Name: facturas_id_factura_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.facturas_id_factura_seq OWNED BY facturacion.facturas.id_factura;


--
-- Name: items; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.items (
    id_item bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_categoria_item integer,
    cod_item character varying(30) NOT NULL,
    des_item character varying(200) NOT NULL,
    des_descripcion text,
    id_tipo_item integer NOT NULL,
    id_tipo_impuesto integer NOT NULL,
    cod_afectacion_iva smallint NOT NULL,
    pct_proporcion_gravada numeric(5,2) DEFAULT 100 NOT NULL,
    cod_unidad_medida smallint DEFAULT 77 NOT NULL,
    id_procedimiento_empresa integer,
    est_item boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT items_check CHECK ((((cod_afectacion_iva <> 4) AND (pct_proporcion_gravada = (100)::numeric)) OR (cod_afectacion_iva = 4))),
    CONSTRAINT items_cod_afectacion_iva_check CHECK ((cod_afectacion_iva = ANY (ARRAY[1, 2, 3, 4]))),
    CONSTRAINT items_pct_proporcion_gravada_check CHECK (((pct_proporcion_gravada >= (0)::numeric) AND (pct_proporcion_gravada <= (100)::numeric)))
);

ALTER TABLE ONLY facturacion.items FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.items OWNER TO postgres;

--
-- Name: items_id_item_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.items_id_item_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.items_id_item_seq OWNER TO postgres;

--
-- Name: items_id_item_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.items_id_item_seq OWNED BY facturacion.items.id_item;


--
-- Name: libro_ventas; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.libro_ventas (
    id_libro_venta bigint NOT NULL,
    id_empresa integer NOT NULL,
    fec_emision date NOT NULL,
    id_tipo_comprobante integer NOT NULL,
    nro_comprobante character varying(20) NOT NULL,
    cod_cdc character(44) NOT NULL,
    id_paciente integer,
    des_nombre_receptor character varying(255) NOT NULL,
    nro_ruc_receptor character varying(10),
    mto_gravado_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_gravado_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_exento numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    cod_estado text DEFAULT 'EMITIDO'::text NOT NULL,
    id_factura bigint,
    id_nota_credito bigint,
    id_nota_debito bigint,
    id_de bigint NOT NULL,
    est_libro_venta boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_libro_origen_unico CHECK ((((
CASE
    WHEN (id_factura IS NOT NULL) THEN 1
    ELSE 0
END +
CASE
    WHEN (id_nota_credito IS NOT NULL) THEN 1
    ELSE 0
END) +
CASE
    WHEN (id_nota_debito IS NOT NULL) THEN 1
    ELSE 0
END) = 1)),
    CONSTRAINT libro_ventas_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['EMITIDO'::text, 'ANULADO'::text])))
);

ALTER TABLE ONLY facturacion.libro_ventas FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.libro_ventas OWNER TO postgres;

--
-- Name: libro_ventas_id_libro_venta_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.libro_ventas_id_libro_venta_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.libro_ventas_id_libro_venta_seq OWNER TO postgres;

--
-- Name: libro_ventas_id_libro_venta_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.libro_ventas_id_libro_venta_seq OWNED BY facturacion.libro_ventas.id_libro_venta;


--
-- Name: movimientos_caja; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.movimientos_caja (
    id_movimiento_caja bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_caja integer NOT NULL,
    id_apertura_caja bigint NOT NULL,
    cod_tipo_movimiento text NOT NULL,
    cod_sentido character(1) NOT NULL,
    id_cobranza bigint,
    mto_importe numeric(18,2) NOT NULL,
    des_concepto text NOT NULL,
    est_movimiento_caja boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT movimientos_caja_cod_sentido_check CHECK ((cod_sentido = ANY (ARRAY['E'::bpchar, 'S'::bpchar]))),
    CONSTRAINT movimientos_caja_cod_tipo_movimiento_check CHECK ((cod_tipo_movimiento = ANY (ARRAY['INGRESO_COBRANZA'::text, 'INGRESO_OTRO'::text, 'EGRESO_RETIRO'::text, 'EGRESO_PAGO'::text, 'AJUSTE_ENTRADA'::text, 'AJUSTE_SALIDA'::text]))),
    CONSTRAINT movimientos_caja_mto_importe_check CHECK ((mto_importe > (0)::numeric))
);

ALTER TABLE ONLY facturacion.movimientos_caja FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.movimientos_caja OWNER TO postgres;

--
-- Name: movimientos_caja_id_movimiento_caja_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.movimientos_caja_id_movimiento_caja_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.movimientos_caja_id_movimiento_caja_seq OWNER TO postgres;

--
-- Name: movimientos_caja_id_movimiento_caja_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.movimientos_caja_id_movimiento_caja_seq OWNED BY facturacion.movimientos_caja.id_movimiento_caja;


--
-- Name: nota_credito_detalle; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.nota_credito_detalle (
    id_nota_credito_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_nota_credito bigint NOT NULL,
    nro_linea smallint NOT NULL,
    id_item bigint,
    cod_item character varying(30),
    des_descripcion character varying(2000) NOT NULL,
    cod_unidad_medida smallint DEFAULT 77 NOT NULL,
    dec_cantidad numeric(14,4) NOT NULL,
    mto_precio_unitario numeric(18,2) NOT NULL,
    mto_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    cod_afectacion_iva smallint NOT NULL,
    pct_proporcion_gravada numeric(5,2) DEFAULT 100 NOT NULL,
    pct_iva numeric(5,2) NOT NULL,
    mto_base_gravada numeric(18,2) DEFAULT 0 NOT NULL,
    mto_base_exenta numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    est_nota_credito_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT nota_credito_detalle_cod_afectacion_iva_check CHECK ((cod_afectacion_iva = ANY (ARRAY[1, 2, 3, 4]))),
    CONSTRAINT nota_credito_detalle_dec_cantidad_check CHECK ((dec_cantidad > (0)::numeric)),
    CONSTRAINT nota_credito_detalle_mto_descuento_check CHECK ((mto_descuento >= (0)::numeric)),
    CONSTRAINT nota_credito_detalle_pct_iva_check CHECK ((pct_iva = ANY (ARRAY[(0)::numeric, (5)::numeric, (10)::numeric]))),
    CONSTRAINT nota_credito_detalle_pct_proporcion_gravada_check CHECK (((pct_proporcion_gravada >= (0)::numeric) AND (pct_proporcion_gravada <= (100)::numeric)))
);

ALTER TABLE ONLY facturacion.nota_credito_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.nota_credito_detalle OWNER TO postgres;

--
-- Name: nota_credito_detalle_id_nota_credito_detalle_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.nota_credito_detalle_id_nota_credito_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.nota_credito_detalle_id_nota_credito_detalle_seq OWNER TO postgres;

--
-- Name: nota_credito_detalle_id_nota_credito_detalle_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.nota_credito_detalle_id_nota_credito_detalle_seq OWNED BY facturacion.nota_credito_detalle.id_nota_credito_detalle;


--
-- Name: nota_debito_detalle; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.nota_debito_detalle (
    id_nota_debito_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_nota_debito bigint NOT NULL,
    nro_linea smallint NOT NULL,
    id_item bigint,
    cod_item character varying(30),
    des_descripcion character varying(2000) NOT NULL,
    cod_unidad_medida smallint DEFAULT 77 NOT NULL,
    dec_cantidad numeric(14,4) NOT NULL,
    mto_precio_unitario numeric(18,2) NOT NULL,
    mto_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    cod_afectacion_iva smallint NOT NULL,
    pct_proporcion_gravada numeric(5,2) DEFAULT 100 NOT NULL,
    pct_iva numeric(5,2) NOT NULL,
    mto_base_gravada numeric(18,2) DEFAULT 0 NOT NULL,
    mto_base_exenta numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    est_nota_debito_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT nota_debito_detalle_cod_afectacion_iva_check CHECK ((cod_afectacion_iva = ANY (ARRAY[1, 2, 3, 4]))),
    CONSTRAINT nota_debito_detalle_dec_cantidad_check CHECK ((dec_cantidad > (0)::numeric)),
    CONSTRAINT nota_debito_detalle_mto_descuento_check CHECK ((mto_descuento >= (0)::numeric)),
    CONSTRAINT nota_debito_detalle_pct_iva_check CHECK ((pct_iva = ANY (ARRAY[(0)::numeric, (5)::numeric, (10)::numeric]))),
    CONSTRAINT nota_debito_detalle_pct_proporcion_gravada_check CHECK (((pct_proporcion_gravada >= (0)::numeric) AND (pct_proporcion_gravada <= (100)::numeric)))
);

ALTER TABLE ONLY facturacion.nota_debito_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.nota_debito_detalle OWNER TO postgres;

--
-- Name: nota_debito_detalle_id_nota_debito_detalle_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.nota_debito_detalle_id_nota_debito_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.nota_debito_detalle_id_nota_debito_detalle_seq OWNER TO postgres;

--
-- Name: nota_debito_detalle_id_nota_debito_detalle_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.nota_debito_detalle_id_nota_debito_detalle_seq OWNED BY facturacion.nota_debito_detalle.id_nota_debito_detalle;


--
-- Name: nota_remision_detalle; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.nota_remision_detalle (
    id_nota_remision_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_nota_remision bigint NOT NULL,
    nro_linea smallint NOT NULL,
    id_item bigint,
    cod_item character varying(30),
    des_descripcion character varying(2000) NOT NULL,
    cod_unidad_medida smallint DEFAULT 77 NOT NULL,
    dec_cantidad numeric(14,4) NOT NULL,
    est_nota_remision_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT nota_remision_detalle_dec_cantidad_check CHECK ((dec_cantidad > (0)::numeric))
);

ALTER TABLE ONLY facturacion.nota_remision_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.nota_remision_detalle OWNER TO postgres;

--
-- Name: nota_remision_detalle_id_nota_remision_detalle_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.nota_remision_detalle_id_nota_remision_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.nota_remision_detalle_id_nota_remision_detalle_seq OWNER TO postgres;

--
-- Name: nota_remision_detalle_id_nota_remision_detalle_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.nota_remision_detalle_id_nota_remision_detalle_seq OWNED BY facturacion.nota_remision_detalle.id_nota_remision_detalle;


--
-- Name: notas_credito; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.notas_credito (
    id_nota_credito bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_nota_credito character varying(15) NOT NULL,
    id_timbrado integer NOT NULL,
    id_establecimiento integer NOT NULL,
    id_punto_expedicion integer NOT NULL,
    cod_serie character(2),
    id_factura bigint NOT NULL,
    cod_motivo_emision smallint NOT NULL,
    des_motivo text,
    cod_naturaleza_receptor smallint NOT NULL,
    cod_tipo_operacion smallint NOT NULL,
    id_tipo_documento integer,
    nro_documento_receptor character varying(20),
    nro_ruc_receptor character varying(8),
    cod_dv_receptor character(1),
    des_nombre_receptor character varying(255) NOT NULL,
    id_pais_receptor integer NOT NULL,
    id_departamento_receptor integer,
    id_ciudad_receptor integer,
    des_email_receptor character varying(150),
    id_condicion_venta integer NOT NULL,
    id_moneda integer NOT NULL,
    fec_emision timestamp with time zone NOT NULL,
    mto_subtotal_exento numeric(18,2) DEFAULT 0 NOT NULL,
    mto_subtotal_gravado_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_subtotal_gravado_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_descuento_total numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total_iva numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    id_de bigint,
    cod_estado text DEFAULT 'BORRADOR'::text NOT NULL,
    des_observaciones text,
    est_nota_credito boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT notas_credito_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['BORRADOR'::text, 'EMITIDA'::text, 'ANULADA'::text]))),
    CONSTRAINT notas_credito_cod_motivo_emision_check CHECK (((cod_motivo_emision >= 1) AND (cod_motivo_emision <= 8))),
    CONSTRAINT notas_credito_cod_naturaleza_receptor_check CHECK ((cod_naturaleza_receptor = ANY (ARRAY[1, 2]))),
    CONSTRAINT notas_credito_cod_tipo_operacion_check CHECK (((cod_tipo_operacion >= 1) AND (cod_tipo_operacion <= 4)))
);

ALTER TABLE ONLY facturacion.notas_credito FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.notas_credito OWNER TO postgres;

--
-- Name: notas_credito_id_nota_credito_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.notas_credito_id_nota_credito_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.notas_credito_id_nota_credito_seq OWNER TO postgres;

--
-- Name: notas_credito_id_nota_credito_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.notas_credito_id_nota_credito_seq OWNED BY facturacion.notas_credito.id_nota_credito;


--
-- Name: notas_debito; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.notas_debito (
    id_nota_debito bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_nota_debito character varying(15) NOT NULL,
    id_timbrado integer NOT NULL,
    id_establecimiento integer NOT NULL,
    id_punto_expedicion integer NOT NULL,
    cod_serie character(2),
    id_factura bigint NOT NULL,
    cod_motivo_emision smallint NOT NULL,
    des_motivo text,
    cod_naturaleza_receptor smallint NOT NULL,
    cod_tipo_operacion smallint NOT NULL,
    id_tipo_documento integer,
    nro_documento_receptor character varying(20),
    nro_ruc_receptor character varying(8),
    cod_dv_receptor character(1),
    des_nombre_receptor character varying(255) NOT NULL,
    id_pais_receptor integer NOT NULL,
    id_departamento_receptor integer,
    id_ciudad_receptor integer,
    des_email_receptor character varying(150),
    id_condicion_venta integer NOT NULL,
    id_moneda integer NOT NULL,
    fec_emision timestamp with time zone NOT NULL,
    mto_subtotal_exento numeric(18,2) DEFAULT 0 NOT NULL,
    mto_subtotal_gravado_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_subtotal_gravado_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_descuento_total numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_5 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_iva_10 numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total_iva numeric(18,2) DEFAULT 0 NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    id_de bigint,
    cod_estado text DEFAULT 'BORRADOR'::text NOT NULL,
    des_observaciones text,
    est_nota_debito boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT notas_debito_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['BORRADOR'::text, 'EMITIDA'::text, 'ANULADA'::text]))),
    CONSTRAINT notas_debito_cod_motivo_emision_check CHECK (((cod_motivo_emision >= 1) AND (cod_motivo_emision <= 8))),
    CONSTRAINT notas_debito_cod_naturaleza_receptor_check CHECK ((cod_naturaleza_receptor = ANY (ARRAY[1, 2]))),
    CONSTRAINT notas_debito_cod_tipo_operacion_check CHECK (((cod_tipo_operacion >= 1) AND (cod_tipo_operacion <= 4)))
);

ALTER TABLE ONLY facturacion.notas_debito FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.notas_debito OWNER TO postgres;

--
-- Name: notas_debito_id_nota_debito_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.notas_debito_id_nota_debito_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.notas_debito_id_nota_debito_seq OWNER TO postgres;

--
-- Name: notas_debito_id_nota_debito_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.notas_debito_id_nota_debito_seq OWNED BY facturacion.notas_debito.id_nota_debito;


--
-- Name: notas_remision; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.notas_remision (
    id_nota_remision bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_nota_remision character varying(15) NOT NULL,
    id_timbrado integer NOT NULL,
    id_establecimiento integer NOT NULL,
    id_punto_expedicion integer NOT NULL,
    cod_serie character(2),
    id_factura bigint,
    cod_motivo_traslado smallint NOT NULL,
    cod_responsable_emision smallint NOT NULL,
    dat_transporte jsonb,
    fec_inicio_traslado date,
    fec_emision timestamp with time zone NOT NULL,
    id_de bigint,
    cod_estado text DEFAULT 'BORRADOR'::text NOT NULL,
    des_observaciones text,
    est_nota_remision boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT notas_remision_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['BORRADOR'::text, 'EMITIDA'::text, 'ANULADA'::text]))),
    CONSTRAINT notas_remision_cod_motivo_traslado_check CHECK (((cod_motivo_traslado >= 1) AND (cod_motivo_traslado <= 99))),
    CONSTRAINT notas_remision_cod_responsable_emision_check CHECK ((cod_responsable_emision = ANY (ARRAY[1, 2, 3, 4, 5])))
);

ALTER TABLE ONLY facturacion.notas_remision FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.notas_remision OWNER TO postgres;

--
-- Name: notas_remision_id_nota_remision_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.notas_remision_id_nota_remision_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.notas_remision_id_nota_remision_seq OWNER TO postgres;

--
-- Name: notas_remision_id_nota_remision_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.notas_remision_id_nota_remision_seq OWNED BY facturacion.notas_remision.id_nota_remision;


--
-- Name: recaudacion_detalle; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.recaudacion_detalle (
    id_recaudacion_detalle bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_recaudacion bigint NOT NULL,
    id_cobranza bigint NOT NULL,
    mto_importe numeric(18,2) NOT NULL,
    est_recaudacion_detalle boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT recaudacion_detalle_mto_importe_check CHECK ((mto_importe > (0)::numeric))
);

ALTER TABLE ONLY facturacion.recaudacion_detalle FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.recaudacion_detalle OWNER TO postgres;

--
-- Name: recaudacion_detalle_id_recaudacion_detalle_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.recaudacion_detalle_id_recaudacion_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.recaudacion_detalle_id_recaudacion_detalle_seq OWNER TO postgres;

--
-- Name: recaudacion_detalle_id_recaudacion_detalle_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.recaudacion_detalle_id_recaudacion_detalle_seq OWNED BY facturacion.recaudacion_detalle.id_recaudacion_detalle;


--
-- Name: recaudaciones; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.recaudaciones (
    id_recaudacion bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_caja integer NOT NULL,
    nro_recaudacion character varying(30) NOT NULL,
    fec_recaudacion date NOT NULL,
    mto_total numeric(18,2) NOT NULL,
    id_entidad_bancaria integer,
    nro_boleta_deposito character varying(30),
    fec_deposito date,
    cod_estado text DEFAULT 'PREPARADA'::text NOT NULL,
    des_observaciones text,
    est_recaudacion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT recaudaciones_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['PREPARADA'::text, 'DEPOSITADA'::text, 'CONFIRMADA'::text]))),
    CONSTRAINT recaudaciones_mto_total_check CHECK ((mto_total > (0)::numeric))
);

ALTER TABLE ONLY facturacion.recaudaciones FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.recaudaciones OWNER TO postgres;

--
-- Name: recaudaciones_id_recaudacion_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.recaudaciones_id_recaudacion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.recaudaciones_id_recaudacion_seq OWNER TO postgres;

--
-- Name: recaudaciones_id_recaudacion_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.recaudaciones_id_recaudacion_seq OWNED BY facturacion.recaudaciones.id_recaudacion;


--
-- Name: secuencias_numeracion; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.secuencias_numeracion (
    id_secuencia integer NOT NULL,
    id_empresa integer NOT NULL,
    id_timbrado integer NOT NULL,
    cod_establecimiento character(3) NOT NULL,
    cod_punto_expedicion character(3) NOT NULL,
    cod_tipo_de character(2) NOT NULL,
    cod_serie character(2),
    nro_ultimo bigint DEFAULT 0 NOT NULL,
    est_secuencia boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT secuencias_numeracion_cod_establecimiento_check CHECK ((cod_establecimiento ~ '^[0-9]{3}$'::text)),
    CONSTRAINT secuencias_numeracion_cod_punto_expedicion_check CHECK ((cod_punto_expedicion ~ '^[0-9]{3}$'::text)),
    CONSTRAINT secuencias_numeracion_cod_serie_check CHECK (((cod_serie IS NULL) OR (cod_serie ~ '^[A-Z]{2}$'::text))),
    CONSTRAINT secuencias_numeracion_cod_tipo_de_check CHECK ((cod_tipo_de = ANY (ARRAY['01'::bpchar, '04'::bpchar, '05'::bpchar, '06'::bpchar, '07'::bpchar]))),
    CONSTRAINT secuencias_numeracion_nro_ultimo_check CHECK (((nro_ultimo >= 0) AND (nro_ultimo <= 9999999)))
);

ALTER TABLE ONLY facturacion.secuencias_numeracion FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.secuencias_numeracion OWNER TO postgres;

--
-- Name: secuencias_numeracion_id_secuencia_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.secuencias_numeracion_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.secuencias_numeracion_id_secuencia_seq OWNER TO postgres;

--
-- Name: secuencias_numeracion_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.secuencias_numeracion_id_secuencia_seq OWNED BY facturacion.secuencias_numeracion.id_secuencia;


--
-- Name: sifen_config; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.sifen_config (
    id_sifen_config integer NOT NULL,
    id_empresa integer NOT NULL,
    id_empresa_certificado integer NOT NULL,
    cod_ambiente text DEFAULT 'TEST'::text NOT NULL,
    cod_tipo_contribuyente smallint NOT NULL,
    cod_id_csc character(4) NOT NULL,
    des_csc_encrypted text NOT NULL,
    cod_id_csc_2 character(4),
    des_csc_2_encrypted text,
    est_sifen_config boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_sifen_config_csc_2 CHECK ((((cod_id_csc_2 IS NULL) AND (des_csc_2_encrypted IS NULL)) OR ((cod_id_csc_2 IS NOT NULL) AND (des_csc_2_encrypted IS NOT NULL)))),
    CONSTRAINT sifen_config_cod_ambiente_check CHECK ((cod_ambiente = ANY (ARRAY['TEST'::text, 'PRODUCCION'::text]))),
    CONSTRAINT sifen_config_cod_tipo_contribuyente_check CHECK ((cod_tipo_contribuyente = ANY (ARRAY[1, 2])))
);

ALTER TABLE ONLY facturacion.sifen_config FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.sifen_config OWNER TO postgres;

--
-- Name: sifen_config_id_sifen_config_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.sifen_config_id_sifen_config_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.sifen_config_id_sifen_config_seq OWNER TO postgres;

--
-- Name: sifen_config_id_sifen_config_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.sifen_config_id_sifen_config_seq OWNED BY facturacion.sifen_config.id_sifen_config;


--
-- Name: sifen_eventos; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.sifen_eventos (
    id_evento bigint NOT NULL,
    id_empresa integer NOT NULL,
    cod_tipo_evento smallint NOT NULL,
    id_de bigint,
    id_timbrado integer,
    cod_establecimiento character(3),
    cod_punto_expedicion character(3),
    cod_tipo_de character(2),
    nro_inicio integer,
    nro_fin integer,
    des_motivo character varying(500) NOT NULL,
    cod_estado text DEFAULT 'PENDIENTE'::text NOT NULL,
    cod_respuesta_sifen character(4),
    des_msg_respuesta text,
    est_evento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_evento_estructura CHECK ((((cod_tipo_evento = 1) AND (id_de IS NOT NULL) AND (nro_inicio IS NULL) AND (nro_fin IS NULL) AND (id_timbrado IS NULL)) OR ((cod_tipo_evento = 2) AND (id_de IS NULL) AND (id_timbrado IS NOT NULL) AND (cod_establecimiento IS NOT NULL) AND (cod_punto_expedicion IS NOT NULL) AND (cod_tipo_de IS NOT NULL) AND (nro_inicio IS NOT NULL) AND (nro_fin IS NOT NULL)))),
    CONSTRAINT sifen_eventos_check CHECK (((nro_fin IS NULL) OR ((nro_fin >= nro_inicio) AND ((nro_fin - nro_inicio) < 1000)))),
    CONSTRAINT sifen_eventos_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['PENDIENTE'::text, 'ENVIADO'::text, 'APROBADO'::text, 'RECHAZADO'::text]))),
    CONSTRAINT sifen_eventos_cod_tipo_de_check CHECK (((cod_tipo_de IS NULL) OR (cod_tipo_de = ANY (ARRAY['01'::bpchar, '04'::bpchar, '05'::bpchar, '06'::bpchar, '07'::bpchar])))),
    CONSTRAINT sifen_eventos_cod_tipo_evento_check CHECK ((cod_tipo_evento = ANY (ARRAY[1, 2]))),
    CONSTRAINT sifen_eventos_des_motivo_check CHECK (((length((des_motivo)::text) >= 5) AND (length((des_motivo)::text) <= 500))),
    CONSTRAINT sifen_eventos_nro_inicio_check CHECK (((nro_inicio IS NULL) OR ((nro_inicio >= 1) AND (nro_inicio <= 9999999))))
);

ALTER TABLE ONLY facturacion.sifen_eventos FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.sifen_eventos OWNER TO postgres;

--
-- Name: sifen_eventos_id_evento_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.sifen_eventos_id_evento_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.sifen_eventos_id_evento_seq OWNER TO postgres;

--
-- Name: sifen_eventos_id_evento_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.sifen_eventos_id_evento_seq OWNED BY facturacion.sifen_eventos.id_evento;


--
-- Name: sifen_lote_documentos; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.sifen_lote_documentos (
    id_lote_documento bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_lote bigint NOT NULL,
    id_de bigint NOT NULL,
    cod_resultado character(4),
    des_msg_resultado text,
    est_lote_documento boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY facturacion.sifen_lote_documentos FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.sifen_lote_documentos OWNER TO postgres;

--
-- Name: sifen_lote_documentos_id_lote_documento_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.sifen_lote_documentos_id_lote_documento_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.sifen_lote_documentos_id_lote_documento_seq OWNER TO postgres;

--
-- Name: sifen_lote_documentos_id_lote_documento_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.sifen_lote_documentos_id_lote_documento_seq OWNED BY facturacion.sifen_lote_documentos.id_lote_documento;


--
-- Name: sifen_lotes; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.sifen_lotes (
    id_lote bigint NOT NULL,
    id_empresa integer NOT NULL,
    nro_lote_sifen character varying(20),
    cnt_documentos smallint NOT NULL,
    cod_estado text DEFAULT 'PREPARADO'::text NOT NULL,
    cod_respuesta character(4),
    des_msg_respuesta text,
    fec_envio timestamp with time zone,
    fec_respuesta timestamp with time zone,
    est_lote boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT sifen_lotes_cnt_documentos_check CHECK (((cnt_documentos >= 1) AND (cnt_documentos <= 50))),
    CONSTRAINT sifen_lotes_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['PREPARADO'::text, 'ENVIADO'::text, 'PROCESADO'::text, 'PARCIAL'::text, 'ERROR'::text])))
);

ALTER TABLE ONLY facturacion.sifen_lotes FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.sifen_lotes OWNER TO postgres;

--
-- Name: sifen_lotes_id_lote_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.sifen_lotes_id_lote_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.sifen_lotes_id_lote_seq OWNER TO postgres;

--
-- Name: sifen_lotes_id_lote_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.sifen_lotes_id_lote_seq OWNED BY facturacion.sifen_lotes.id_lote;


--
-- Name: sifen_transmision_log; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.sifen_transmision_log (
    id_transmision_log bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_de bigint,
    id_lote bigint,
    cod_servicio text NOT NULL,
    cod_http smallint,
    cod_respuesta character(4),
    des_request_path text,
    des_response_path text,
    cnt_duracion_ms integer,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT sifen_transmision_log_cnt_duracion_ms_check CHECK (((cnt_duracion_ms IS NULL) OR (cnt_duracion_ms >= 0))),
    CONSTRAINT sifen_transmision_log_cod_servicio_check CHECK ((cod_servicio = ANY (ARRAY['RECIBE'::text, 'RECIBE_LOTE'::text, 'CONSULTA_LOTE'::text, 'EVENTO'::text, 'CONSULTA_DE'::text, 'CONSULTA_RUC'::text])))
);

ALTER TABLE ONLY facturacion.sifen_transmision_log FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.sifen_transmision_log OWNER TO postgres;

--
-- Name: sifen_transmision_log_id_transmision_log_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.sifen_transmision_log_id_transmision_log_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.sifen_transmision_log_id_transmision_log_seq OWNER TO postgres;

--
-- Name: sifen_transmision_log_id_transmision_log_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.sifen_transmision_log_id_transmision_log_seq OWNED BY facturacion.sifen_transmision_log.id_transmision_log;


--
-- Name: tarifario_precios; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.tarifario_precios (
    id_tarifario_precio bigint NOT NULL,
    id_empresa integer NOT NULL,
    id_item bigint NOT NULL,
    id_moneda integer NOT NULL,
    id_entidad_pagadora integer,
    mto_precio numeric(18,2) NOT NULL,
    fec_vigencia_desde date NOT NULL,
    fec_vigencia_hasta date,
    est_tarifario_precio boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT chk_tarifario_vigencia CHECK (((fec_vigencia_hasta IS NULL) OR (fec_vigencia_hasta >= fec_vigencia_desde))),
    CONSTRAINT tarifario_precios_mto_precio_check CHECK ((mto_precio > (0)::numeric))
);

ALTER TABLE ONLY facturacion.tarifario_precios FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.tarifario_precios OWNER TO postgres;

--
-- Name: tarifario_precios_id_tarifario_precio_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.tarifario_precios_id_tarifario_precio_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.tarifario_precios_id_tarifario_precio_seq OWNER TO postgres;

--
-- Name: tarifario_precios_id_tarifario_precio_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.tarifario_precios_id_tarifario_precio_seq OWNED BY facturacion.tarifario_precios.id_tarifario_precio;


--
-- Name: timbrado_habilitaciones; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.timbrado_habilitaciones (
    id_timbrado_habilitacion integer NOT NULL,
    id_empresa integer NOT NULL,
    id_timbrado integer NOT NULL,
    id_punto_expedicion integer NOT NULL,
    est_timbrado_habilitacion boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone
);

ALTER TABLE ONLY facturacion.timbrado_habilitaciones FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.timbrado_habilitaciones OWNER TO postgres;

--
-- Name: timbrado_habilitaciones_id_timbrado_habilitacion_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.timbrado_habilitaciones_id_timbrado_habilitacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.timbrado_habilitaciones_id_timbrado_habilitacion_seq OWNER TO postgres;

--
-- Name: timbrado_habilitaciones_id_timbrado_habilitacion_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.timbrado_habilitaciones_id_timbrado_habilitacion_seq OWNED BY facturacion.timbrado_habilitaciones.id_timbrado_habilitacion;


--
-- Name: timbrados; Type: TABLE; Schema: facturacion; Owner: postgres
--

CREATE TABLE facturacion.timbrados (
    id_timbrado integer NOT NULL,
    id_empresa integer NOT NULL,
    id_tipo_comprobante integer NOT NULL,
    nro_timbrado character(8) NOT NULL,
    fec_inicio date NOT NULL,
    fec_vencimiento date,
    cod_estado text DEFAULT 'ACTIVO'::text NOT NULL,
    des_observaciones text,
    est_timbrado boolean DEFAULT true NOT NULL,
    id_usuario_creacion bigint NOT NULL,
    fec_creacion timestamp with time zone DEFAULT now() NOT NULL,
    id_usuario_modificacion bigint,
    fec_modificacion timestamp with time zone,
    id_usuario_eliminacion bigint,
    fec_eliminacion timestamp with time zone,
    CONSTRAINT timbrados_cod_estado_check CHECK ((cod_estado = ANY (ARRAY['ACTIVO'::text, 'VENCIDO'::text, 'DADO_BAJA'::text, 'SUSPENDIDO'::text]))),
    CONSTRAINT timbrados_nro_timbrado_check CHECK ((nro_timbrado ~ '^[0-9]{8}$'::text))
);

ALTER TABLE ONLY facturacion.timbrados FORCE ROW LEVEL SECURITY;


ALTER TABLE facturacion.timbrados OWNER TO postgres;

--
-- Name: timbrados_id_timbrado_seq; Type: SEQUENCE; Schema: facturacion; Owner: postgres
--

CREATE SEQUENCE facturacion.timbrados_id_timbrado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facturacion.timbrados_id_timbrado_seq OWNER TO postgres;

--
-- Name: timbrados_id_timbrado_seq; Type: SEQUENCE OWNED BY; Schema: facturacion; Owner: postgres
--

ALTER SEQUENCE facturacion.timbrados_id_timbrado_seq OWNED BY facturacion.timbrados.id_timbrado;


--
-- Name: auditoria_sistema_y2026; Type: TABLE ATTACH; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema ATTACH PARTITION core.auditoria_sistema_y2026 FOR VALUES FROM ('2026-01-01 00:00:00-03') TO ('2027-01-01 00:00:00-03');


--
-- Name: auditoria_sistema_y2027; Type: TABLE ATTACH; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema ATTACH PARTITION core.auditoria_sistema_y2027 FOR VALUES FROM ('2027-01-01 00:00:00-03') TO ('2028-01-01 00:00:00-03');


--
-- Name: auditoria_sistema_y2028; Type: TABLE ATTACH; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema ATTACH PARTITION core.auditoria_sistema_y2028 FOR VALUES FROM ('2028-01-01 00:00:00-03') TO ('2029-01-01 00:00:00-03');


--
-- Name: acuerdo_monto_historial id_acuerdo_monto; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdo_monto_historial ALTER COLUMN id_acuerdo_monto SET DEFAULT nextval('consultorio.acuerdo_monto_historial_id_acuerdo_monto_seq'::regclass);


--
-- Name: acuerdos_terapeuticos id_acuerdo_terapeutico; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdos_terapeuticos ALTER COLUMN id_acuerdo_terapeutico SET DEFAULT nextval('consultorio.acuerdos_terapeuticos_id_acuerdo_terapeutico_seq'::regclass);


--
-- Name: anamnesis id_anamnesis; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis ALTER COLUMN id_anamnesis SET DEFAULT nextval('consultorio.anamnesis_id_anamnesis_seq'::regclass);


--
-- Name: anamnesis_adulto_ext id_anamnesis_adulto_ext; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_adulto_ext ALTER COLUMN id_anamnesis_adulto_ext SET DEFAULT nextval('consultorio.anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq'::regclass);


--
-- Name: anamnesis_infantil_ext id_anamnesis_infantil_ext; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_infantil_ext ALTER COLUMN id_anamnesis_infantil_ext SET DEFAULT nextval('consultorio.anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq'::regclass);


--
-- Name: antecedentes_paciente id_antecedente_paciente; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.antecedentes_paciente ALTER COLUMN id_antecedente_paciente SET DEFAULT nextval('consultorio.antecedentes_paciente_id_antecedente_paciente_seq'::regclass);


--
-- Name: cobros_simples id_cobro_simple; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.cobros_simples ALTER COLUMN id_cobro_simple SET DEFAULT nextval('consultorio.cobros_simples_id_cobro_simple_seq'::regclass);


--
-- Name: consentimientos_firmados id_consentimiento; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.consentimientos_firmados ALTER COLUMN id_consentimiento SET DEFAULT nextval('consultorio.consentimientos_firmados_id_consentimiento_seq'::regclass);


--
-- Name: contratos_tratamiento id_contrato_tratamiento; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento ALTER COLUMN id_contrato_tratamiento SET DEFAULT nextval('consultorio.contratos_tratamiento_id_contrato_tratamiento_seq'::regclass);


--
-- Name: contratos_tratamiento_acuerdos_pago id_acuerdo_pago; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_acuerdos_pago ALTER COLUMN id_acuerdo_pago SET DEFAULT nextval('consultorio.contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq'::regclass);


--
-- Name: contratos_tratamiento_modalidades_pago id_modalidad_pago; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_modalidades_pago ALTER COLUMN id_modalidad_pago SET DEFAULT nextval('consultorio.contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq'::regclass);


--
-- Name: contratos_tratamiento_pagos id_pago; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_pagos ALTER COLUMN id_pago SET DEFAULT nextval('consultorio.contratos_tratamiento_pagos_id_pago_seq'::regclass);


--
-- Name: contratos_tratamiento_sesiones id_contrato_sesion; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones ALTER COLUMN id_contrato_sesion SET DEFAULT nextval('consultorio.contratos_tratamiento_sesiones_id_contrato_sesion_seq'::regclass);


--
-- Name: derivaciones id_derivacion; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.derivaciones ALTER COLUMN id_derivacion SET DEFAULT nextval('consultorio.derivaciones_id_derivacion_seq'::regclass);


--
-- Name: diagnosticos_cie10 id_diagnostico_cie10; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10 ALTER COLUMN id_diagnostico_cie10 SET DEFAULT nextval('consultorio.diagnosticos_cie10_id_diagnostico_cie10_seq'::regclass);


--
-- Name: diagnosticos_cie10_dsm5_equivalencias id_equivalencia; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10_dsm5_equivalencias ALTER COLUMN id_equivalencia SET DEFAULT nextval('consultorio.diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq'::regclass);


--
-- Name: diagnosticos_dsm5 id_diagnostico_dsm5; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_dsm5 ALTER COLUMN id_diagnostico_dsm5 SET DEFAULT nextval('consultorio.diagnosticos_dsm5_id_diagnostico_dsm5_seq'::regclass);


--
-- Name: documentos_adjuntos id_documento_adjunto; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.documentos_adjuntos ALTER COLUMN id_documento_adjunto SET DEFAULT nextval('consultorio.documentos_adjuntos_id_documento_adjunto_seq'::regclass);


--
-- Name: empresa_perfil_clinico id_empresa_perfil_clinico; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.empresa_perfil_clinico ALTER COLUMN id_empresa_perfil_clinico SET DEFAULT nextval('consultorio.empresa_perfil_clinico_id_empresa_perfil_clinico_seq'::regclass);


--
-- Name: episodio_diagnosticos id_episodio_diagnostico; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_diagnosticos ALTER COLUMN id_episodio_diagnostico SET DEFAULT nextval('consultorio.episodio_diagnosticos_id_episodio_diagnostico_seq'::regclass);


--
-- Name: episodio_procedimientos id_episodio_procedimiento; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos ALTER COLUMN id_episodio_procedimiento SET DEFAULT nextval('consultorio.episodio_procedimientos_id_episodio_procedimiento_seq'::regclass);


--
-- Name: episodio_procedimientos_insumos id_ep_insumo; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos_insumos ALTER COLUMN id_ep_insumo SET DEFAULT nextval('consultorio.episodio_procedimientos_insumos_id_ep_insumo_seq'::regclass);


--
-- Name: episodios id_episodio; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios ALTER COLUMN id_episodio SET DEFAULT nextval('consultorio.episodios_id_episodio_seq'::regclass);


--
-- Name: fichas_clinicas id_ficha_clinica; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_clinicas ALTER COLUMN id_ficha_clinica SET DEFAULT nextval('consultorio.fichas_clinicas_id_ficha_clinica_seq'::regclass);


--
-- Name: fichas_psicologia id_ficha_psicologia; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_psicologia ALTER COLUMN id_ficha_psicologia SET DEFAULT nextval('consultorio.fichas_psicologia_id_ficha_psicologia_seq'::regclass);


--
-- Name: formularios_definicion id_formulario_definicion; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.formularios_definicion ALTER COLUMN id_formulario_definicion SET DEFAULT nextval('consultorio.formularios_definicion_id_formulario_definicion_seq'::regclass);


--
-- Name: indicaciones_no_farmacologicas id_indicacion; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.indicaciones_no_farmacologicas ALTER COLUMN id_indicacion SET DEFAULT nextval('consultorio.indicaciones_no_farmacologicas_id_indicacion_seq'::regclass);


--
-- Name: insumos_empresa id_insumo_empresa; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.insumos_empresa ALTER COLUMN id_insumo_empresa SET DEFAULT nextval('consultorio.insumos_empresa_id_insumo_empresa_seq'::regclass);


--
-- Name: justificativos id_justificativo; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos ALTER COLUMN id_justificativo SET DEFAULT nextval('consultorio.justificativos_id_justificativo_seq'::regclass);


--
-- Name: medicamentos_empresa id_medicamento_empresa; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.medicamentos_empresa ALTER COLUMN id_medicamento_empresa SET DEFAULT nextval('consultorio.medicamentos_empresa_id_medicamento_empresa_seq'::regclass);


--
-- Name: notas_evolucion id_nota_evolucion; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.notas_evolucion ALTER COLUMN id_nota_evolucion SET DEFAULT nextval('consultorio.notas_evolucion_id_nota_evolucion_seq'::regclass);


--
-- Name: ordenes_analisis id_orden_analisis; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis ALTER COLUMN id_orden_analisis SET DEFAULT nextval('consultorio.ordenes_analisis_id_orden_analisis_seq'::regclass);


--
-- Name: ordenes_analisis_detalle id_orden_analisis_detalle; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis_detalle ALTER COLUMN id_orden_analisis_detalle SET DEFAULT nextval('consultorio.ordenes_analisis_detalle_id_orden_analisis_detalle_seq'::regclass);


--
-- Name: ordenes_estudios id_orden_estudios; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios ALTER COLUMN id_orden_estudios SET DEFAULT nextval('consultorio.ordenes_estudios_id_orden_estudios_seq'::regclass);


--
-- Name: ordenes_estudios_detalle id_orden_estudios_detalle; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios_detalle ALTER COLUMN id_orden_estudios_detalle SET DEFAULT nextval('consultorio.ordenes_estudios_detalle_id_orden_estudios_detalle_seq'::regclass);


--
-- Name: paciente_tokens id_paciente_token; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.paciente_tokens ALTER COLUMN id_paciente_token SET DEFAULT nextval('consultorio.paciente_tokens_id_paciente_token_seq'::regclass);


--
-- Name: pei id_pei; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei ALTER COLUMN id_pei SET DEFAULT nextval('consultorio.pei_id_pei_seq'::regclass);


--
-- Name: pei_calendario_eventos id_pei_calendario_evento; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_calendario_eventos ALTER COLUMN id_pei_calendario_evento SET DEFAULT nextval('consultorio.pei_calendario_eventos_id_pei_calendario_evento_seq'::regclass);


--
-- Name: pei_estrategias id_pei_estrategia; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_estrategias ALTER COLUMN id_pei_estrategia SET DEFAULT nextval('consultorio.pei_estrategias_id_pei_estrategia_seq'::regclass);


--
-- Name: pei_habilidades_entrenamiento id_pei_habilidad; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_habilidades_entrenamiento ALTER COLUMN id_pei_habilidad SET DEFAULT nextval('consultorio.pei_habilidades_entrenamiento_id_pei_habilidad_seq'::regclass);


--
-- Name: pei_objetivos id_pei_objetivo; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_objetivos ALTER COLUMN id_pei_objetivo SET DEFAULT nextval('consultorio.pei_objetivos_id_pei_objetivo_seq'::regclass);


--
-- Name: pei_registro_mensual id_pei_registro_mensual; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_registro_mensual ALTER COLUMN id_pei_registro_mensual SET DEFAULT nextval('consultorio.pei_registro_mensual_id_pei_registro_mensual_seq'::regclass);


--
-- Name: pei_reunion_clinica id_pei_reunion_clinica; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_clinica ALTER COLUMN id_pei_reunion_clinica SET DEFAULT nextval('consultorio.pei_reunion_clinica_id_pei_reunion_clinica_seq'::regclass);


--
-- Name: pei_reunion_participantes id_pei_reunion_participante; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_participantes ALTER COLUMN id_pei_reunion_participante SET DEFAULT nextval('consultorio.pei_reunion_participantes_id_pei_reunion_participante_seq'::regclass);


--
-- Name: pei_reunion_recomendaciones id_pei_recomendacion; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_recomendaciones ALTER COLUMN id_pei_recomendacion SET DEFAULT nextval('consultorio.pei_reunion_recomendaciones_id_pei_recomendacion_seq'::regclass);


--
-- Name: pei_sesion_actividades id_pei_sesion_actividad; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_actividades ALTER COLUMN id_pei_sesion_actividad SET DEFAULT nextval('consultorio.pei_sesion_actividades_id_pei_sesion_actividad_seq'::regclass);


--
-- Name: pei_sesion_planificada id_pei_sesion; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_planificada ALTER COLUMN id_pei_sesion SET DEFAULT nextval('consultorio.pei_sesion_planificada_id_pei_sesion_seq'::regclass);


--
-- Name: planes_tratamiento id_plan_tratamiento; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento ALTER COLUMN id_plan_tratamiento SET DEFAULT nextval('consultorio.planes_tratamiento_id_plan_tratamiento_seq'::regclass);


--
-- Name: planes_tratamiento_items id_plan_tratamiento_item; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento_items ALTER COLUMN id_plan_tratamiento_item SET DEFAULT nextval('consultorio.planes_tratamiento_items_id_plan_tratamiento_item_seq'::regclass);


--
-- Name: plantillas_justificativos id_plantilla_justificativo; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.plantillas_justificativos ALTER COLUMN id_plantilla_justificativo SET DEFAULT nextval('consultorio.plantillas_justificativos_id_plantilla_justificativo_seq'::regclass);


--
-- Name: procedimientos_empresa id_procedimiento_empresa; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.procedimientos_empresa ALTER COLUMN id_procedimiento_empresa SET DEFAULT nextval('consultorio.procedimientos_empresa_id_procedimiento_empresa_seq'::regclass);


--
-- Name: psicologia_perfil_empresa id_psicologia_perfil; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.psicologia_perfil_empresa ALTER COLUMN id_psicologia_perfil SET DEFAULT nextval('consultorio.psicologia_perfil_empresa_id_psicologia_perfil_seq'::regclass);


--
-- Name: recetas id_receta; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas ALTER COLUMN id_receta SET DEFAULT nextval('consultorio.recetas_id_receta_seq'::regclass);


--
-- Name: recetas_detalle id_receta_detalle; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas_detalle ALTER COLUMN id_receta_detalle SET DEFAULT nextval('consultorio.recetas_detalle_id_receta_detalle_seq'::regclass);


--
-- Name: resultados_analisis id_resultado_analisis; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis ALTER COLUMN id_resultado_analisis SET DEFAULT nextval('consultorio.resultados_analisis_id_resultado_analisis_seq'::regclass);


--
-- Name: resultados_analisis_detalle id_resultado_analisis_det; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis_detalle ALTER COLUMN id_resultado_analisis_det SET DEFAULT nextval('consultorio.resultados_analisis_detalle_id_resultado_analisis_det_seq'::regclass);


--
-- Name: signos_vitales id_signos_vitales; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales ALTER COLUMN id_signos_vitales SET DEFAULT nextval('consultorio.signos_vitales_id_signos_vitales_seq'::regclass);


--
-- Name: signos_vitales_detalle id_signos_vitales_detalle; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales_detalle ALTER COLUMN id_signos_vitales_detalle SET DEFAULT nextval('consultorio.signos_vitales_detalle_id_signos_vitales_detalle_seq'::regclass);


--
-- Name: tipos_justificativos id_tipo_justificativo; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_justificativos ALTER COLUMN id_tipo_justificativo SET DEFAULT nextval('consultorio.tipos_justificativos_id_tipo_justificativo_seq'::regclass);


--
-- Name: tipos_procedimientos id_tipo_procedimiento; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_procedimientos ALTER COLUMN id_tipo_procedimiento SET DEFAULT nextval('consultorio.tipos_procedimientos_id_tipo_procedimiento_seq'::regclass);


--
-- Name: tipos_signos_vitales id_tipo_signo_vital; Type: DEFAULT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_signos_vitales ALTER COLUMN id_tipo_signo_vital SET DEFAULT nextval('consultorio.tipos_signos_vitales_id_tipo_signo_vital_seq'::regclass);


--
-- Name: agenda_horarios id_agenda_horario; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios ALTER COLUMN id_agenda_horario SET DEFAULT nextval('core.agenda_horarios_id_agenda_horario_seq'::regclass);


--
-- Name: agenda_horarios_excepciones id_agenda_horario_excepcion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios_excepciones ALTER COLUMN id_agenda_horario_excepcion SET DEFAULT nextval('core.agenda_horarios_excepciones_id_agenda_horario_excepcion_seq'::regclass);


--
-- Name: auditoria_sistema id_auditoria_sistema; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema ALTER COLUMN id_auditoria_sistema SET DEFAULT nextval('core.auditoria_sistema_id_auditoria_sistema_seq'::regclass);


--
-- Name: cargos id_cargo; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.cargos ALTER COLUMN id_cargo SET DEFAULT nextval('core.cargos_id_cargo_seq'::regclass);


--
-- Name: citas id_cita; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas ALTER COLUMN id_cita SET DEFAULT nextval('core.citas_id_cita_seq'::regclass);


--
-- Name: citas_log_estados id_cita_log_estado; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas_log_estados ALTER COLUMN id_cita_log_estado SET DEFAULT nextval('core.citas_log_estados_id_cita_log_estado_seq'::regclass);


--
-- Name: ciudades id_ciudad; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.ciudades ALTER COLUMN id_ciudad SET DEFAULT nextval('core.ciudades_id_ciudad_seq'::regclass);


--
-- Name: condiciones_venta id_condicion_venta; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.condiciones_venta ALTER COLUMN id_condicion_venta SET DEFAULT nextval('core.condiciones_venta_id_condicion_venta_seq'::regclass);


--
-- Name: consultorios id_consultorio; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.consultorios ALTER COLUMN id_consultorio SET DEFAULT nextval('core.consultorios_id_consultorio_seq'::regclass);


--
-- Name: departamentos id_departamento; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.departamentos ALTER COLUMN id_departamento SET DEFAULT nextval('core.departamentos_id_departamento_seq'::regclass);


--
-- Name: dias_semana id_dia_semana; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.dias_semana ALTER COLUMN id_dia_semana SET DEFAULT nextval('core.dias_semana_id_dia_semana_seq'::regclass);


--
-- Name: empresa_certificados id_empresa_certificado; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_certificados ALTER COLUMN id_empresa_certificado SET DEFAULT nextval('core.empresa_certificados_id_empresa_certificado_seq'::regclass);


--
-- Name: empresa_configuracion id_empresa_configuracion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_configuracion ALTER COLUMN id_empresa_configuracion SET DEFAULT nextval('core.empresa_configuracion_id_empresa_configuracion_seq'::regclass);


--
-- Name: empresa_modulos id_empresa_modulo; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_modulos ALTER COLUMN id_empresa_modulo SET DEFAULT nextval('core.empresa_modulos_id_empresa_modulo_seq'::regclass);


--
-- Name: empresas id_empresa; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresas ALTER COLUMN id_empresa SET DEFAULT nextval('core.empresas_id_empresa_seq'::regclass);


--
-- Name: especialidades id_especialidad; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialidades ALTER COLUMN id_especialidad SET DEFAULT nextval('core.especialidades_id_especialidad_seq'::regclass);


--
-- Name: especialista_especialidades id_especialista_especialidad; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialista_especialidades ALTER COLUMN id_especialista_especialidad SET DEFAULT nextval('core.especialista_especialidades_id_especialista_especialidad_seq'::regclass);


--
-- Name: especialistas id_especialista; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialistas ALTER COLUMN id_especialista SET DEFAULT nextval('core.especialistas_id_especialista_seq'::regclass);


--
-- Name: establecimientos id_establecimiento; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.establecimientos ALTER COLUMN id_establecimiento SET DEFAULT nextval('core.establecimientos_id_establecimiento_seq'::regclass);


--
-- Name: estados_citas id_estado_cita; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_citas ALTER COLUMN id_estado_cita SET DEFAULT nextval('core.estados_citas_id_estado_cita_seq'::regclass);


--
-- Name: estados_civiles id_estado_civil; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_civiles ALTER COLUMN id_estado_civil SET DEFAULT nextval('core.estados_civiles_id_estado_civil_seq'::regclass);


--
-- Name: estados_factura id_estado_factura; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_factura ALTER COLUMN id_estado_factura SET DEFAULT nextval('core.estados_factura_id_estado_factura_seq'::regclass);


--
-- Name: feriados id_feriado; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.feriados ALTER COLUMN id_feriado SET DEFAULT nextval('core.feriados_id_feriado_seq'::regclass);


--
-- Name: formas_cobro id_forma_cobro; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.formas_cobro ALTER COLUMN id_forma_cobro SET DEFAULT nextval('core.formas_cobro_id_forma_cobro_seq'::regclass);


--
-- Name: frecuencias_agendamiento id_frecuencia_agendamiento; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.frecuencias_agendamiento ALTER COLUMN id_frecuencia_agendamiento SET DEFAULT nextval('core.frecuencias_agendamiento_id_frecuencia_agendamiento_seq'::regclass);


--
-- Name: funcionarios id_funcionario; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.funcionarios ALTER COLUMN id_funcionario SET DEFAULT nextval('core.funcionarios_id_funcionario_seq'::regclass);


--
-- Name: generos id_genero; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.generos ALTER COLUMN id_genero SET DEFAULT nextval('core.generos_id_genero_seq'::regclass);


--
-- Name: historial_suscripciones id_historial_suscripcion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.historial_suscripciones ALTER COLUMN id_historial_suscripcion SET DEFAULT nextval('core.historial_suscripciones_id_historial_suscripcion_seq'::regclass);


--
-- Name: licencias id_licencia; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.licencias ALTER COLUMN id_licencia SET DEFAULT nextval('core.licencias_id_licencia_seq'::regclass);


--
-- Name: lista_espera id_lista_espera; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.lista_espera ALTER COLUMN id_lista_espera SET DEFAULT nextval('core.lista_espera_id_lista_espera_seq'::regclass);


--
-- Name: login_attempts id_login_attempt; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.login_attempts ALTER COLUMN id_login_attempt SET DEFAULT nextval('core.login_attempts_id_login_attempt_seq'::regclass);


--
-- Name: marcas_tarjeta id_marca_tarjeta; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.marcas_tarjeta ALTER COLUMN id_marca_tarjeta SET DEFAULT nextval('core.marcas_tarjeta_id_marca_tarjeta_seq'::regclass);


--
-- Name: metricas_diarias id_metrica_diaria; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.metricas_diarias ALTER COLUMN id_metrica_diaria SET DEFAULT nextval('core.metricas_diarias_id_metrica_diaria_seq'::regclass);


--
-- Name: mfa_tokens id_mfa_token; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.mfa_tokens ALTER COLUMN id_mfa_token SET DEFAULT nextval('core.mfa_tokens_id_mfa_token_seq'::regclass);


--
-- Name: modulos id_modulo; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.modulos ALTER COLUMN id_modulo SET DEFAULT nextval('core.modulos_id_modulo_seq'::regclass);


--
-- Name: monedas id_moneda; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.monedas ALTER COLUMN id_moneda SET DEFAULT nextval('core.monedas_id_moneda_seq'::regclass);


--
-- Name: niveles_instruccion id_nivel_instruccion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.niveles_instruccion ALTER COLUMN id_nivel_instruccion SET DEFAULT nextval('core.niveles_instruccion_id_nivel_instruccion_seq'::regclass);


--
-- Name: notificaciones_cola id_notificacion_cola; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_cola ALTER COLUMN id_notificacion_cola SET DEFAULT nextval('core.notificaciones_cola_id_notificacion_cola_seq'::regclass);


--
-- Name: notificaciones_config id_notificacion_config; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_config ALTER COLUMN id_notificacion_config SET DEFAULT nextval('core.notificaciones_config_id_notificacion_config_seq'::regclass);


--
-- Name: notificaciones_log id_notificacion_log; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_log ALTER COLUMN id_notificacion_log SET DEFAULT nextval('core.notificaciones_log_id_notificacion_log_seq'::regclass);


--
-- Name: notificaciones_plantillas id_notificacion_plantilla; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_plantillas ALTER COLUMN id_notificacion_plantilla SET DEFAULT nextval('core.notificaciones_plantillas_id_notificacion_plantilla_seq'::regclass);


--
-- Name: paciente_profesional id_paciente_profesional; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paciente_profesional ALTER COLUMN id_paciente_profesional SET DEFAULT nextval('core.paciente_profesional_id_paciente_profesional_seq'::regclass);


--
-- Name: pacientes id_paciente; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.pacientes ALTER COLUMN id_paciente SET DEFAULT nextval('core.pacientes_id_paciente_seq'::regclass);


--
-- Name: pacientes_menores id_paciente_menor; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.pacientes_menores ALTER COLUMN id_paciente_menor SET DEFAULT nextval('core.pacientes_menores_id_paciente_menor_seq'::regclass);


--
-- Name: paises id_pais; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paises ALTER COLUMN id_pais SET DEFAULT nextval('core.paises_id_pais_seq'::regclass);


--
-- Name: password_history id_password_history; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_history ALTER COLUMN id_password_history SET DEFAULT nextval('core.password_history_id_password_history_seq'::regclass);


--
-- Name: password_reset_tokens id_password_reset_token; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_reset_tokens ALTER COLUMN id_password_reset_token SET DEFAULT nextval('core.password_reset_tokens_id_password_reset_token_seq'::regclass);


--
-- Name: permisos id_permiso; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.permisos ALTER COLUMN id_permiso SET DEFAULT nextval('core.permisos_id_permiso_seq'::regclass);


--
-- Name: personas id_persona; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.personas ALTER COLUMN id_persona SET DEFAULT nextval('core.personas_id_persona_seq'::regclass);


--
-- Name: plan_modulos id_plan_modulo; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.plan_modulos ALTER COLUMN id_plan_modulo SET DEFAULT nextval('core.plan_modulos_id_plan_modulo_seq'::regclass);


--
-- Name: planes id_plan; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.planes ALTER COLUMN id_plan SET DEFAULT nextval('core.planes_id_plan_seq'::regclass);


--
-- Name: preferencias_ui id_preferencia_ui; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.preferencias_ui ALTER COLUMN id_preferencia_ui SET DEFAULT nextval('core.preferencias_ui_id_preferencia_ui_seq'::regclass);


--
-- Name: profesiones id_profesion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.profesiones ALTER COLUMN id_profesion SET DEFAULT nextval('core.profesiones_id_profesion_seq'::regclass);


--
-- Name: puntos_expedicion id_punto_expedicion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.puntos_expedicion ALTER COLUMN id_punto_expedicion SET DEFAULT nextval('core.puntos_expedicion_id_punto_expedicion_seq'::regclass);


--
-- Name: recordatorios id_recordatorio; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.recordatorios ALTER COLUMN id_recordatorio SET DEFAULT nextval('core.recordatorios_id_recordatorio_seq'::regclass);


--
-- Name: reportes_jobs id_reporte_job; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.reportes_jobs ALTER COLUMN id_reporte_job SET DEFAULT nextval('core.reportes_jobs_id_reporte_job_seq'::regclass);


--
-- Name: reportes_jobs_log id_reporte_job_log; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.reportes_jobs_log ALTER COLUMN id_reporte_job_log SET DEFAULT nextval('core.reportes_jobs_log_id_reporte_job_log_seq'::regclass);


--
-- Name: roles_base id_rol_base; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_base ALTER COLUMN id_rol_base SET DEFAULT nextval('core.roles_base_id_rol_base_seq'::regclass);


--
-- Name: roles_empresa id_rol_empresa; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_empresa ALTER COLUMN id_rol_empresa SET DEFAULT nextval('core.roles_empresa_id_rol_empresa_seq'::regclass);


--
-- Name: roles_empresa_permisos id_rol_empresa_permiso; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_empresa_permisos ALTER COLUMN id_rol_empresa_permiso SET DEFAULT nextval('core.roles_empresa_permisos_id_rol_empresa_permiso_seq'::regclass);


--
-- Name: schema_migrations id_schema_migration; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.schema_migrations ALTER COLUMN id_schema_migration SET DEFAULT nextval('core.schema_migrations_id_schema_migration_seq'::regclass);


--
-- Name: sedes id_sede; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.sedes ALTER COLUMN id_sede SET DEFAULT nextval('core.sedes_id_sede_seq'::regclass);


--
-- Name: sesiones id_sesion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.sesiones ALTER COLUMN id_sesion SET DEFAULT nextval('core.sesiones_id_sesion_seq'::regclass);


--
-- Name: slots_agenda id_slot_agenda; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.slots_agenda ALTER COLUMN id_slot_agenda SET DEFAULT nextval('core.slots_agenda_id_slot_agenda_seq'::regclass);


--
-- Name: suscripcion_excedentes id_suscripcion_excedente; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.suscripcion_excedentes ALTER COLUMN id_suscripcion_excedente SET DEFAULT nextval('core.suscripcion_excedentes_id_suscripcion_excedente_seq'::regclass);


--
-- Name: suscripcion_expansiones id_expansion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.suscripcion_expansiones ALTER COLUMN id_expansion SET DEFAULT nextval('core.suscripcion_expansiones_id_expansion_seq'::regclass);


--
-- Name: suscripciones id_suscripcion; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.suscripciones ALTER COLUMN id_suscripcion SET DEFAULT nextval('core.suscripciones_id_suscripcion_seq'::regclass);


--
-- Name: tipos_comprobantes id_tipo_comprobante; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_comprobantes ALTER COLUMN id_tipo_comprobante SET DEFAULT nextval('core.tipos_comprobantes_id_tipo_comprobante_seq'::regclass);


--
-- Name: tipos_documentos_identidad id_tipo_documento; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_documentos_identidad ALTER COLUMN id_tipo_documento SET DEFAULT nextval('core.tipos_documentos_identidad_id_tipo_documento_seq'::regclass);


--
-- Name: tipos_impuestos id_tipo_impuesto; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_impuestos ALTER COLUMN id_tipo_impuesto SET DEFAULT nextval('core.tipos_impuestos_id_tipo_impuesto_seq'::regclass);


--
-- Name: tipos_items id_tipo_item; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_items ALTER COLUMN id_tipo_item SET DEFAULT nextval('core.tipos_items_id_tipo_item_seq'::regclass);


--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('core.usuarios_id_usuario_seq'::regclass);


--
-- Name: usuarios_roles_base id_usuario_rol_base; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios_roles_base ALTER COLUMN id_usuario_rol_base SET DEFAULT nextval('core.usuarios_roles_base_id_usuario_rol_base_seq'::regclass);


--
-- Name: usuarios_roles_empresa id_usuario_rol_empresa; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios_roles_empresa ALTER COLUMN id_usuario_rol_empresa SET DEFAULT nextval('core.usuarios_roles_empresa_id_usuario_rol_empresa_seq'::regclass);


--
-- Name: aperturas_caja id_apertura_caja; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.aperturas_caja ALTER COLUMN id_apertura_caja SET DEFAULT nextval('facturacion.aperturas_caja_id_apertura_caja_seq'::regclass);


--
-- Name: arqueos_caja id_arqueo_caja; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.arqueos_caja ALTER COLUMN id_arqueo_caja SET DEFAULT nextval('facturacion.arqueos_caja_id_arqueo_caja_seq'::regclass);


--
-- Name: autofactura_detalle id_autofactura_detalle; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofactura_detalle ALTER COLUMN id_autofactura_detalle SET DEFAULT nextval('facturacion.autofactura_detalle_id_autofactura_detalle_seq'::regclass);


--
-- Name: autofacturas id_autofactura; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas ALTER COLUMN id_autofactura SET DEFAULT nextval('facturacion.autofacturas_id_autofactura_seq'::regclass);


--
-- Name: cajas id_caja; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cajas ALTER COLUMN id_caja SET DEFAULT nextval('facturacion.cajas_id_caja_seq'::regclass);


--
-- Name: categorias_items id_categoria_item; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.categorias_items ALTER COLUMN id_categoria_item SET DEFAULT nextval('facturacion.categorias_items_id_categoria_item_seq'::regclass);


--
-- Name: cheques_recibidos id_cheque_recibido; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cheques_recibidos ALTER COLUMN id_cheque_recibido SET DEFAULT nextval('facturacion.cheques_recibidos_id_cheque_recibido_seq'::regclass);


--
-- Name: cobranza_detalle id_cobranza_detalle; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle ALTER COLUMN id_cobranza_detalle SET DEFAULT nextval('facturacion.cobranza_detalle_id_cobranza_detalle_seq'::regclass);


--
-- Name: cobranzas id_cobranza; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas ALTER COLUMN id_cobranza SET DEFAULT nextval('facturacion.cobranzas_id_cobranza_seq'::regclass);


--
-- Name: cuentas_cobrar id_cuenta_cobrar; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar ALTER COLUMN id_cuenta_cobrar SET DEFAULT nextval('facturacion.cuentas_cobrar_id_cuenta_cobrar_seq'::regclass);


--
-- Name: cuotas_cobrar id_cuota_cobrar; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuotas_cobrar ALTER COLUMN id_cuota_cobrar SET DEFAULT nextval('facturacion.cuotas_cobrar_id_cuota_cobrar_seq'::regclass);


--
-- Name: documentos_electronicos id_de; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.documentos_electronicos ALTER COLUMN id_de SET DEFAULT nextval('facturacion.documentos_electronicos_id_de_seq'::regclass);


--
-- Name: entidades_bancarias id_entidad_bancaria; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_bancarias ALTER COLUMN id_entidad_bancaria SET DEFAULT nextval('facturacion.entidades_bancarias_id_entidad_bancaria_seq'::regclass);


--
-- Name: entidades_pagadoras id_entidad_pagadora; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_pagadoras ALTER COLUMN id_entidad_pagadora SET DEFAULT nextval('facturacion.entidades_pagadoras_id_entidad_pagadora_seq'::regclass);


--
-- Name: factura_detalle id_factura_detalle; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_detalle ALTER COLUMN id_factura_detalle SET DEFAULT nextval('facturacion.factura_detalle_id_factura_detalle_seq'::regclass);


--
-- Name: factura_medios_pago id_factura_medio_pago; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_medios_pago ALTER COLUMN id_factura_medio_pago SET DEFAULT nextval('facturacion.factura_medios_pago_id_factura_medio_pago_seq'::regclass);


--
-- Name: facturas id_factura; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas ALTER COLUMN id_factura SET DEFAULT nextval('facturacion.facturas_id_factura_seq'::regclass);


--
-- Name: items id_item; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items ALTER COLUMN id_item SET DEFAULT nextval('facturacion.items_id_item_seq'::regclass);


--
-- Name: libro_ventas id_libro_venta; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas ALTER COLUMN id_libro_venta SET DEFAULT nextval('facturacion.libro_ventas_id_libro_venta_seq'::regclass);


--
-- Name: movimientos_caja id_movimiento_caja; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.movimientos_caja ALTER COLUMN id_movimiento_caja SET DEFAULT nextval('facturacion.movimientos_caja_id_movimiento_caja_seq'::regclass);


--
-- Name: nota_credito_detalle id_nota_credito_detalle; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_credito_detalle ALTER COLUMN id_nota_credito_detalle SET DEFAULT nextval('facturacion.nota_credito_detalle_id_nota_credito_detalle_seq'::regclass);


--
-- Name: nota_debito_detalle id_nota_debito_detalle; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_debito_detalle ALTER COLUMN id_nota_debito_detalle SET DEFAULT nextval('facturacion.nota_debito_detalle_id_nota_debito_detalle_seq'::regclass);


--
-- Name: nota_remision_detalle id_nota_remision_detalle; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_remision_detalle ALTER COLUMN id_nota_remision_detalle SET DEFAULT nextval('facturacion.nota_remision_detalle_id_nota_remision_detalle_seq'::regclass);


--
-- Name: notas_credito id_nota_credito; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito ALTER COLUMN id_nota_credito SET DEFAULT nextval('facturacion.notas_credito_id_nota_credito_seq'::regclass);


--
-- Name: notas_debito id_nota_debito; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito ALTER COLUMN id_nota_debito SET DEFAULT nextval('facturacion.notas_debito_id_nota_debito_seq'::regclass);


--
-- Name: notas_remision id_nota_remision; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision ALTER COLUMN id_nota_remision SET DEFAULT nextval('facturacion.notas_remision_id_nota_remision_seq'::regclass);


--
-- Name: recaudacion_detalle id_recaudacion_detalle; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudacion_detalle ALTER COLUMN id_recaudacion_detalle SET DEFAULT nextval('facturacion.recaudacion_detalle_id_recaudacion_detalle_seq'::regclass);


--
-- Name: recaudaciones id_recaudacion; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudaciones ALTER COLUMN id_recaudacion SET DEFAULT nextval('facturacion.recaudaciones_id_recaudacion_seq'::regclass);


--
-- Name: secuencias_numeracion id_secuencia; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.secuencias_numeracion ALTER COLUMN id_secuencia SET DEFAULT nextval('facturacion.secuencias_numeracion_id_secuencia_seq'::regclass);


--
-- Name: sifen_config id_sifen_config; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_config ALTER COLUMN id_sifen_config SET DEFAULT nextval('facturacion.sifen_config_id_sifen_config_seq'::regclass);


--
-- Name: sifen_eventos id_evento; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_eventos ALTER COLUMN id_evento SET DEFAULT nextval('facturacion.sifen_eventos_id_evento_seq'::regclass);


--
-- Name: sifen_lote_documentos id_lote_documento; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lote_documentos ALTER COLUMN id_lote_documento SET DEFAULT nextval('facturacion.sifen_lote_documentos_id_lote_documento_seq'::regclass);


--
-- Name: sifen_lotes id_lote; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lotes ALTER COLUMN id_lote SET DEFAULT nextval('facturacion.sifen_lotes_id_lote_seq'::regclass);


--
-- Name: sifen_transmision_log id_transmision_log; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_transmision_log ALTER COLUMN id_transmision_log SET DEFAULT nextval('facturacion.sifen_transmision_log_id_transmision_log_seq'::regclass);


--
-- Name: tarifario_precios id_tarifario_precio; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.tarifario_precios ALTER COLUMN id_tarifario_precio SET DEFAULT nextval('facturacion.tarifario_precios_id_tarifario_precio_seq'::regclass);


--
-- Name: timbrado_habilitaciones id_timbrado_habilitacion; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrado_habilitaciones ALTER COLUMN id_timbrado_habilitacion SET DEFAULT nextval('facturacion.timbrado_habilitaciones_id_timbrado_habilitacion_seq'::regclass);


--
-- Name: timbrados id_timbrado; Type: DEFAULT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrados ALTER COLUMN id_timbrado SET DEFAULT nextval('facturacion.timbrados_id_timbrado_seq'::regclass);


--
-- Name: acuerdo_monto_historial acuerdo_monto_historial_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdo_monto_historial
    ADD CONSTRAINT acuerdo_monto_historial_pkey PRIMARY KEY (id_acuerdo_monto);


--
-- Name: acuerdos_terapeuticos acuerdos_terapeuticos_id_empresa_id_paciente_nro_version_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdos_terapeuticos
    ADD CONSTRAINT acuerdos_terapeuticos_id_empresa_id_paciente_nro_version_key UNIQUE (id_empresa, id_paciente, nro_version);


--
-- Name: acuerdos_terapeuticos acuerdos_terapeuticos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdos_terapeuticos
    ADD CONSTRAINT acuerdos_terapeuticos_pkey PRIMARY KEY (id_acuerdo_terapeutico);


--
-- Name: anamnesis_adulto_ext anamnesis_adulto_ext_id_anamnesis_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_adulto_ext
    ADD CONSTRAINT anamnesis_adulto_ext_id_anamnesis_key UNIQUE (id_anamnesis);


--
-- Name: anamnesis_adulto_ext anamnesis_adulto_ext_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_adulto_ext
    ADD CONSTRAINT anamnesis_adulto_ext_pkey PRIMARY KEY (id_anamnesis_adulto_ext);


--
-- Name: anamnesis anamnesis_id_empresa_id_paciente_tipo_anamnesis_nro_version_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis
    ADD CONSTRAINT anamnesis_id_empresa_id_paciente_tipo_anamnesis_nro_version_key UNIQUE (id_empresa, id_paciente, tipo_anamnesis, nro_version);


--
-- Name: anamnesis_infantil_ext anamnesis_infantil_ext_id_anamnesis_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_infantil_ext
    ADD CONSTRAINT anamnesis_infantil_ext_id_anamnesis_key UNIQUE (id_anamnesis);


--
-- Name: anamnesis_infantil_ext anamnesis_infantil_ext_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_infantil_ext
    ADD CONSTRAINT anamnesis_infantil_ext_pkey PRIMARY KEY (id_anamnesis_infantil_ext);


--
-- Name: anamnesis anamnesis_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis
    ADD CONSTRAINT anamnesis_pkey PRIMARY KEY (id_anamnesis);


--
-- Name: antecedentes_paciente antecedentes_paciente_id_empresa_id_paciente_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.antecedentes_paciente
    ADD CONSTRAINT antecedentes_paciente_id_empresa_id_paciente_key UNIQUE (id_empresa, id_paciente);


--
-- Name: antecedentes_paciente antecedentes_paciente_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.antecedentes_paciente
    ADD CONSTRAINT antecedentes_paciente_pkey PRIMARY KEY (id_antecedente_paciente);


--
-- Name: cobros_simples cobros_simples_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.cobros_simples
    ADD CONSTRAINT cobros_simples_pkey PRIMARY KEY (id_cobro_simple);


--
-- Name: consentimientos_firmados consentimientos_firmados_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.consentimientos_firmados
    ADD CONSTRAINT consentimientos_firmados_pkey PRIMARY KEY (id_consentimiento);


--
-- Name: contratos_tratamiento_acuerdos_pago contratos_tratamiento_acuerdos_pago_id_contrato_tratamiento_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_acuerdos_pago
    ADD CONSTRAINT contratos_tratamiento_acuerdos_pago_id_contrato_tratamiento_key UNIQUE (id_contrato_tratamiento);


--
-- Name: contratos_tratamiento_acuerdos_pago contratos_tratamiento_acuerdos_pago_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_acuerdos_pago
    ADD CONSTRAINT contratos_tratamiento_acuerdos_pago_pkey PRIMARY KEY (id_acuerdo_pago);


--
-- Name: contratos_tratamiento contratos_tratamiento_id_empresa_nro_contrato_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento
    ADD CONSTRAINT contratos_tratamiento_id_empresa_nro_contrato_key UNIQUE (id_empresa, nro_contrato);


--
-- Name: contratos_tratamiento_modalidades_pago contratos_tratamiento_modalidades_pago_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_modalidades_pago
    ADD CONSTRAINT contratos_tratamiento_modalidades_pago_pkey PRIMARY KEY (id_modalidad_pago);


--
-- Name: contratos_tratamiento_pagos contratos_tratamiento_pagos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_pagos
    ADD CONSTRAINT contratos_tratamiento_pagos_pkey PRIMARY KEY (id_pago);


--
-- Name: contratos_tratamiento contratos_tratamiento_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento
    ADD CONSTRAINT contratos_tratamiento_pkey PRIMARY KEY (id_contrato_tratamiento);


--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesione_id_contrato_tratamiento_nro_s_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones
    ADD CONSTRAINT contratos_tratamiento_sesione_id_contrato_tratamiento_nro_s_key UNIQUE (id_contrato_tratamiento, nro_sesion);


--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesiones_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones
    ADD CONSTRAINT contratos_tratamiento_sesiones_pkey PRIMARY KEY (id_contrato_sesion);


--
-- Name: derivaciones derivaciones_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.derivaciones
    ADD CONSTRAINT derivaciones_pkey PRIMARY KEY (id_derivacion);


--
-- Name: diagnosticos_cie10 diagnosticos_cie10_codigo_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10
    ADD CONSTRAINT diagnosticos_cie10_codigo_key UNIQUE (codigo);


--
-- Name: diagnosticos_cie10_dsm5_equivalencias diagnosticos_cie10_dsm5_equiv_id_diagnostico_cie10_id_diagn_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10_dsm5_equivalencias
    ADD CONSTRAINT diagnosticos_cie10_dsm5_equiv_id_diagnostico_cie10_id_diagn_key UNIQUE (id_diagnostico_cie10, id_diagnostico_dsm5);


--
-- Name: diagnosticos_cie10_dsm5_equivalencias diagnosticos_cie10_dsm5_equivalencias_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10_dsm5_equivalencias
    ADD CONSTRAINT diagnosticos_cie10_dsm5_equivalencias_pkey PRIMARY KEY (id_equivalencia);


--
-- Name: diagnosticos_cie10 diagnosticos_cie10_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10
    ADD CONSTRAINT diagnosticos_cie10_pkey PRIMARY KEY (id_diagnostico_cie10);


--
-- Name: diagnosticos_dsm5 diagnosticos_dsm5_codigo_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_dsm5
    ADD CONSTRAINT diagnosticos_dsm5_codigo_key UNIQUE (codigo);


--
-- Name: diagnosticos_dsm5 diagnosticos_dsm5_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_dsm5
    ADD CONSTRAINT diagnosticos_dsm5_pkey PRIMARY KEY (id_diagnostico_dsm5);


--
-- Name: documentos_adjuntos documentos_adjuntos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.documentos_adjuntos
    ADD CONSTRAINT documentos_adjuntos_pkey PRIMARY KEY (id_documento_adjunto);


--
-- Name: empresa_perfil_clinico empresa_perfil_clinico_id_empresa_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.empresa_perfil_clinico
    ADD CONSTRAINT empresa_perfil_clinico_id_empresa_key UNIQUE (id_empresa);


--
-- Name: empresa_perfil_clinico empresa_perfil_clinico_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.empresa_perfil_clinico
    ADD CONSTRAINT empresa_perfil_clinico_pkey PRIMARY KEY (id_empresa_perfil_clinico);


--
-- Name: episodio_diagnosticos episodio_diagnosticos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_diagnosticos
    ADD CONSTRAINT episodio_diagnosticos_pkey PRIMARY KEY (id_episodio_diagnostico);


--
-- Name: episodio_procedimientos_insumos episodio_procedimientos_insumos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos_insumos
    ADD CONSTRAINT episodio_procedimientos_insumos_pkey PRIMARY KEY (id_ep_insumo);


--
-- Name: episodio_procedimientos episodio_procedimientos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos
    ADD CONSTRAINT episodio_procedimientos_pkey PRIMARY KEY (id_episodio_procedimiento);


--
-- Name: episodios episodios_id_empresa_nro_episodio_empresa_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_id_empresa_nro_episodio_empresa_key UNIQUE (id_empresa, nro_episodio_empresa);


--
-- Name: episodios episodios_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_pkey PRIMARY KEY (id_episodio);


--
-- Name: fichas_clinicas fichas_clinicas_id_episodio_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_id_episodio_key UNIQUE (id_episodio);


--
-- Name: fichas_clinicas fichas_clinicas_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_pkey PRIMARY KEY (id_ficha_clinica);


--
-- Name: fichas_psicologia fichas_psicologia_id_ficha_clinica_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_psicologia
    ADD CONSTRAINT fichas_psicologia_id_ficha_clinica_key UNIQUE (id_ficha_clinica);


--
-- Name: fichas_psicologia fichas_psicologia_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_psicologia
    ADD CONSTRAINT fichas_psicologia_pkey PRIMARY KEY (id_ficha_psicologia);


--
-- Name: formularios_definicion formularios_definicion_id_empresa_des_formulario_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.formularios_definicion
    ADD CONSTRAINT formularios_definicion_id_empresa_des_formulario_key UNIQUE (id_empresa, des_formulario);


--
-- Name: formularios_definicion formularios_definicion_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.formularios_definicion
    ADD CONSTRAINT formularios_definicion_pkey PRIMARY KEY (id_formulario_definicion);


--
-- Name: indicaciones_no_farmacologicas indicaciones_no_farmacologicas_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.indicaciones_no_farmacologicas
    ADD CONSTRAINT indicaciones_no_farmacologicas_pkey PRIMARY KEY (id_indicacion);


--
-- Name: insumos_empresa insumos_empresa_id_empresa_des_insumo_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.insumos_empresa
    ADD CONSTRAINT insumos_empresa_id_empresa_des_insumo_key UNIQUE (id_empresa, des_insumo);


--
-- Name: insumos_empresa insumos_empresa_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.insumos_empresa
    ADD CONSTRAINT insumos_empresa_pkey PRIMARY KEY (id_insumo_empresa);


--
-- Name: justificativos justificativos_id_empresa_nro_documento_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_empresa_nro_documento_key UNIQUE (id_empresa, nro_documento);


--
-- Name: justificativos justificativos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_pkey PRIMARY KEY (id_justificativo);


--
-- Name: medicamentos_empresa medicamentos_empresa_id_empresa_des_medicamento_des_concent_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.medicamentos_empresa
    ADD CONSTRAINT medicamentos_empresa_id_empresa_des_medicamento_des_concent_key UNIQUE (id_empresa, des_medicamento, des_concentracion);


--
-- Name: medicamentos_empresa medicamentos_empresa_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.medicamentos_empresa
    ADD CONSTRAINT medicamentos_empresa_pkey PRIMARY KEY (id_medicamento_empresa);


--
-- Name: notas_evolucion notas_evolucion_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.notas_evolucion
    ADD CONSTRAINT notas_evolucion_pkey PRIMARY KEY (id_nota_evolucion);


--
-- Name: ordenes_analisis_detalle ordenes_analisis_detalle_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis_detalle
    ADD CONSTRAINT ordenes_analisis_detalle_pkey PRIMARY KEY (id_orden_analisis_detalle);


--
-- Name: ordenes_analisis ordenes_analisis_id_empresa_nro_documento_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis
    ADD CONSTRAINT ordenes_analisis_id_empresa_nro_documento_key UNIQUE (id_empresa, nro_documento);


--
-- Name: ordenes_analisis ordenes_analisis_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis
    ADD CONSTRAINT ordenes_analisis_pkey PRIMARY KEY (id_orden_analisis);


--
-- Name: ordenes_estudios_detalle ordenes_estudios_detalle_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios_detalle
    ADD CONSTRAINT ordenes_estudios_detalle_pkey PRIMARY KEY (id_orden_estudios_detalle);


--
-- Name: ordenes_estudios ordenes_estudios_id_empresa_nro_documento_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios
    ADD CONSTRAINT ordenes_estudios_id_empresa_nro_documento_key UNIQUE (id_empresa, nro_documento);


--
-- Name: ordenes_estudios ordenes_estudios_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios
    ADD CONSTRAINT ordenes_estudios_pkey PRIMARY KEY (id_orden_estudios);


--
-- Name: paciente_tokens paciente_tokens_des_token_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.paciente_tokens
    ADD CONSTRAINT paciente_tokens_des_token_key UNIQUE (des_token);


--
-- Name: paciente_tokens paciente_tokens_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.paciente_tokens
    ADD CONSTRAINT paciente_tokens_pkey PRIMARY KEY (id_paciente_token);


--
-- Name: pei_calendario_eventos pei_calendario_eventos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_calendario_eventos
    ADD CONSTRAINT pei_calendario_eventos_pkey PRIMARY KEY (id_pei_calendario_evento);


--
-- Name: pei_estrategias pei_estrategias_id_pei_nro_orden_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_estrategias
    ADD CONSTRAINT pei_estrategias_id_pei_nro_orden_key UNIQUE (id_pei, nro_orden);


--
-- Name: pei_estrategias pei_estrategias_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_estrategias
    ADD CONSTRAINT pei_estrategias_pkey PRIMARY KEY (id_pei_estrategia);


--
-- Name: pei_habilidades_entrenamiento pei_habilidades_entrenamiento_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_habilidades_entrenamiento
    ADD CONSTRAINT pei_habilidades_entrenamiento_pkey PRIMARY KEY (id_pei_habilidad);


--
-- Name: pei_objetivos pei_objetivos_id_pei_nro_orden_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_objetivos
    ADD CONSTRAINT pei_objetivos_id_pei_nro_orden_key UNIQUE (id_pei, nro_orden);


--
-- Name: pei_objetivos pei_objetivos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_objetivos
    ADD CONSTRAINT pei_objetivos_pkey PRIMARY KEY (id_pei_objetivo);


--
-- Name: pei pei_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei
    ADD CONSTRAINT pei_pkey PRIMARY KEY (id_pei);


--
-- Name: pei_registro_mensual pei_registro_mensual_id_pei_nro_periodo_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_registro_mensual
    ADD CONSTRAINT pei_registro_mensual_id_pei_nro_periodo_key UNIQUE (id_pei, nro_periodo);


--
-- Name: pei_registro_mensual pei_registro_mensual_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_registro_mensual
    ADD CONSTRAINT pei_registro_mensual_pkey PRIMARY KEY (id_pei_registro_mensual);


--
-- Name: pei_reunion_clinica pei_reunion_clinica_id_pei_nro_version_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_clinica
    ADD CONSTRAINT pei_reunion_clinica_id_pei_nro_version_key UNIQUE (id_pei, nro_version);


--
-- Name: pei_reunion_clinica pei_reunion_clinica_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_clinica
    ADD CONSTRAINT pei_reunion_clinica_pkey PRIMARY KEY (id_pei_reunion_clinica);


--
-- Name: pei_reunion_participantes pei_reunion_participantes_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_participantes
    ADD CONSTRAINT pei_reunion_participantes_pkey PRIMARY KEY (id_pei_reunion_participante);


--
-- Name: pei_reunion_recomendaciones pei_reunion_recomendaciones_id_pei_reunion_clinica_nro_orde_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_recomendaciones
    ADD CONSTRAINT pei_reunion_recomendaciones_id_pei_reunion_clinica_nro_orde_key UNIQUE (id_pei_reunion_clinica, nro_orden);


--
-- Name: pei_reunion_recomendaciones pei_reunion_recomendaciones_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_recomendaciones
    ADD CONSTRAINT pei_reunion_recomendaciones_pkey PRIMARY KEY (id_pei_recomendacion);


--
-- Name: pei_sesion_actividades pei_sesion_actividades_id_pei_sesion_nro_orden_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_actividades
    ADD CONSTRAINT pei_sesion_actividades_id_pei_sesion_nro_orden_key UNIQUE (id_pei_sesion, nro_orden);


--
-- Name: pei_sesion_actividades pei_sesion_actividades_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_actividades
    ADD CONSTRAINT pei_sesion_actividades_pkey PRIMARY KEY (id_pei_sesion_actividad);


--
-- Name: pei_sesion_planificada pei_sesion_planificada_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_planificada
    ADD CONSTRAINT pei_sesion_planificada_pkey PRIMARY KEY (id_pei_sesion);


--
-- Name: planes_tratamiento_items planes_tratamiento_items_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento_items
    ADD CONSTRAINT planes_tratamiento_items_pkey PRIMARY KEY (id_plan_tratamiento_item);


--
-- Name: planes_tratamiento planes_tratamiento_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento
    ADD CONSTRAINT planes_tratamiento_pkey PRIMARY KEY (id_plan_tratamiento);


--
-- Name: plantillas_justificativos plantillas_justificativos_id_empresa_id_tipo_justificativo__key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.plantillas_justificativos
    ADD CONSTRAINT plantillas_justificativos_id_empresa_id_tipo_justificativo__key UNIQUE (id_empresa, id_tipo_justificativo, des_titulo);


--
-- Name: plantillas_justificativos plantillas_justificativos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.plantillas_justificativos
    ADD CONSTRAINT plantillas_justificativos_pkey PRIMARY KEY (id_plantilla_justificativo);


--
-- Name: procedimientos_empresa procedimientos_empresa_id_empresa_cod_procedimiento_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.procedimientos_empresa
    ADD CONSTRAINT procedimientos_empresa_id_empresa_cod_procedimiento_key UNIQUE (id_empresa, cod_procedimiento);


--
-- Name: procedimientos_empresa procedimientos_empresa_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.procedimientos_empresa
    ADD CONSTRAINT procedimientos_empresa_pkey PRIMARY KEY (id_procedimiento_empresa);


--
-- Name: psicologia_perfil_empresa psicologia_perfil_empresa_id_empresa_perfil_clinico_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.psicologia_perfil_empresa
    ADD CONSTRAINT psicologia_perfil_empresa_id_empresa_perfil_clinico_key UNIQUE (id_empresa_perfil_clinico);


--
-- Name: psicologia_perfil_empresa psicologia_perfil_empresa_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.psicologia_perfil_empresa
    ADD CONSTRAINT psicologia_perfil_empresa_pkey PRIMARY KEY (id_psicologia_perfil);


--
-- Name: recetas_detalle recetas_detalle_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas_detalle
    ADD CONSTRAINT recetas_detalle_pkey PRIMARY KEY (id_receta_detalle);


--
-- Name: recetas recetas_id_empresa_nro_documento_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas
    ADD CONSTRAINT recetas_id_empresa_nro_documento_key UNIQUE (id_empresa, nro_documento);


--
-- Name: recetas recetas_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas
    ADD CONSTRAINT recetas_pkey PRIMARY KEY (id_receta);


--
-- Name: resultados_analisis_detalle resultados_analisis_detalle_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis_detalle
    ADD CONSTRAINT resultados_analisis_detalle_pkey PRIMARY KEY (id_resultado_analisis_det);


--
-- Name: resultados_analisis resultados_analisis_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis
    ADD CONSTRAINT resultados_analisis_pkey PRIMARY KEY (id_resultado_analisis);


--
-- Name: signos_vitales_detalle signos_vitales_detalle_id_signos_vitales_id_tipo_signo_vita_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales_detalle
    ADD CONSTRAINT signos_vitales_detalle_id_signos_vitales_id_tipo_signo_vita_key UNIQUE (id_signos_vitales, id_tipo_signo_vital);


--
-- Name: signos_vitales_detalle signos_vitales_detalle_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales_detalle
    ADD CONSTRAINT signos_vitales_detalle_pkey PRIMARY KEY (id_signos_vitales_detalle);


--
-- Name: signos_vitales signos_vitales_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales
    ADD CONSTRAINT signos_vitales_pkey PRIMARY KEY (id_signos_vitales);


--
-- Name: tipos_justificativos tipos_justificativos_cod_tipo_justificativo_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_justificativos
    ADD CONSTRAINT tipos_justificativos_cod_tipo_justificativo_key UNIQUE (cod_tipo_justificativo);


--
-- Name: tipos_justificativos tipos_justificativos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_justificativos
    ADD CONSTRAINT tipos_justificativos_pkey PRIMARY KEY (id_tipo_justificativo);


--
-- Name: tipos_procedimientos tipos_procedimientos_cod_tipo_procedimiento_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_procedimientos
    ADD CONSTRAINT tipos_procedimientos_cod_tipo_procedimiento_key UNIQUE (cod_tipo_procedimiento);


--
-- Name: tipos_procedimientos tipos_procedimientos_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_procedimientos
    ADD CONSTRAINT tipos_procedimientos_pkey PRIMARY KEY (id_tipo_procedimiento);


--
-- Name: tipos_signos_vitales tipos_signos_vitales_cod_tipo_signo_vital_key; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_signos_vitales
    ADD CONSTRAINT tipos_signos_vitales_cod_tipo_signo_vital_key UNIQUE (cod_tipo_signo_vital);


--
-- Name: tipos_signos_vitales tipos_signos_vitales_pkey; Type: CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.tipos_signos_vitales
    ADD CONSTRAINT tipos_signos_vitales_pkey PRIMARY KEY (id_tipo_signo_vital);


--
-- Name: agenda_horarios_excepciones agenda_horarios_excepciones_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios_excepciones
    ADD CONSTRAINT agenda_horarios_excepciones_pkey PRIMARY KEY (id_agenda_horario_excepcion);


--
-- Name: agenda_horarios agenda_horarios_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios
    ADD CONSTRAINT agenda_horarios_pkey PRIMARY KEY (id_agenda_horario);


--
-- Name: auditoria_sistema auditoria_sistema_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema
    ADD CONSTRAINT auditoria_sistema_pkey PRIMARY KEY (id_auditoria_sistema, fec_evento);


--
-- Name: auditoria_sistema_y2026 auditoria_sistema_y2026_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema_y2026
    ADD CONSTRAINT auditoria_sistema_y2026_pkey PRIMARY KEY (id_auditoria_sistema, fec_evento);


--
-- Name: auditoria_sistema_y2027 auditoria_sistema_y2027_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema_y2027
    ADD CONSTRAINT auditoria_sistema_y2027_pkey PRIMARY KEY (id_auditoria_sistema, fec_evento);


--
-- Name: auditoria_sistema_y2028 auditoria_sistema_y2028_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auditoria_sistema_y2028
    ADD CONSTRAINT auditoria_sistema_y2028_pkey PRIMARY KEY (id_auditoria_sistema, fec_evento);


--
-- Name: cargos cargos_id_empresa_des_cargo_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.cargos
    ADD CONSTRAINT cargos_id_empresa_des_cargo_key UNIQUE (id_empresa, des_cargo);


--
-- Name: cargos cargos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.cargos
    ADD CONSTRAINT cargos_pkey PRIMARY KEY (id_cargo);


--
-- Name: citas_log_estados citas_log_estados_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas_log_estados
    ADD CONSTRAINT citas_log_estados_pkey PRIMARY KEY (id_cita_log_estado);


--
-- Name: citas citas_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_pkey PRIMARY KEY (id_cita);


--
-- Name: ciudades ciudades_id_departamento_des_ciudad_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.ciudades
    ADD CONSTRAINT ciudades_id_departamento_des_ciudad_key UNIQUE (id_departamento, des_ciudad);


--
-- Name: ciudades ciudades_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.ciudades
    ADD CONSTRAINT ciudades_pkey PRIMARY KEY (id_ciudad);


--
-- Name: condiciones_venta condiciones_venta_cod_condicion_venta_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.condiciones_venta
    ADD CONSTRAINT condiciones_venta_cod_condicion_venta_key UNIQUE (cod_condicion_venta);


--
-- Name: condiciones_venta condiciones_venta_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.condiciones_venta
    ADD CONSTRAINT condiciones_venta_pkey PRIMARY KEY (id_condicion_venta);


--
-- Name: consultorios consultorios_id_sede_des_consultorio_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.consultorios
    ADD CONSTRAINT consultorios_id_sede_des_consultorio_key UNIQUE (id_sede, des_consultorio);


--
-- Name: consultorios consultorios_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.consultorios
    ADD CONSTRAINT consultorios_pkey PRIMARY KEY (id_consultorio);


--
-- Name: departamentos departamentos_id_pais_des_departamento_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.departamentos
    ADD CONSTRAINT departamentos_id_pais_des_departamento_key UNIQUE (id_pais, des_departamento);


--
-- Name: departamentos departamentos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.departamentos
    ADD CONSTRAINT departamentos_pkey PRIMARY KEY (id_departamento);


--
-- Name: dias_semana dias_semana_des_dia_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.dias_semana
    ADD CONSTRAINT dias_semana_des_dia_key UNIQUE (des_dia);


--
-- Name: dias_semana dias_semana_nro_dia_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.dias_semana
    ADD CONSTRAINT dias_semana_nro_dia_key UNIQUE (nro_dia);


--
-- Name: dias_semana dias_semana_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.dias_semana
    ADD CONSTRAINT dias_semana_pkey PRIMARY KEY (id_dia_semana);


--
-- Name: empresa_certificados empresa_certificados_id_empresa_tipo_certificado_fingerprin_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_certificados
    ADD CONSTRAINT empresa_certificados_id_empresa_tipo_certificado_fingerprin_key UNIQUE (id_empresa, tipo_certificado, fingerprint_sha256);


--
-- Name: empresa_certificados empresa_certificados_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_certificados
    ADD CONSTRAINT empresa_certificados_pkey PRIMARY KEY (id_empresa_certificado);


--
-- Name: empresa_configuracion empresa_configuracion_id_empresa_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_configuracion
    ADD CONSTRAINT empresa_configuracion_id_empresa_key UNIQUE (id_empresa);


--
-- Name: empresa_configuracion empresa_configuracion_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_configuracion
    ADD CONSTRAINT empresa_configuracion_pkey PRIMARY KEY (id_empresa_configuracion);


--
-- Name: empresa_modulos empresa_modulos_id_empresa_id_modulo_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_modulos
    ADD CONSTRAINT empresa_modulos_id_empresa_id_modulo_key UNIQUE (id_empresa, id_modulo);


--
-- Name: empresa_modulos empresa_modulos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_modulos
    ADD CONSTRAINT empresa_modulos_pkey PRIMARY KEY (id_empresa_modulo);


--
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (id_empresa);


--
-- Name: especialidades especialidades_id_empresa_des_especialidad_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialidades
    ADD CONSTRAINT especialidades_id_empresa_des_especialidad_key UNIQUE (id_empresa, des_especialidad);


--
-- Name: especialidades especialidades_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialidades
    ADD CONSTRAINT especialidades_pkey PRIMARY KEY (id_especialidad);


--
-- Name: especialista_especialidades especialista_especialidades_id_especialista_id_especialidad_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_id_especialista_id_especialidad_key UNIQUE (id_especialista, id_especialidad);


--
-- Name: especialista_especialidades especialista_especialidades_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_pkey PRIMARY KEY (id_especialista_especialidad);


--
-- Name: especialistas especialistas_id_empresa_id_funcionario_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialistas
    ADD CONSTRAINT especialistas_id_empresa_id_funcionario_key UNIQUE (id_empresa, id_funcionario);


--
-- Name: especialistas especialistas_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialistas
    ADD CONSTRAINT especialistas_pkey PRIMARY KEY (id_especialista);


--
-- Name: establecimientos establecimientos_id_sede_cod_establecimiento_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.establecimientos
    ADD CONSTRAINT establecimientos_id_sede_cod_establecimiento_key UNIQUE (id_sede, cod_establecimiento);


--
-- Name: establecimientos establecimientos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.establecimientos
    ADD CONSTRAINT establecimientos_pkey PRIMARY KEY (id_establecimiento);


--
-- Name: estados_citas estados_citas_id_empresa_cod_estado_cita_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_citas
    ADD CONSTRAINT estados_citas_id_empresa_cod_estado_cita_key UNIQUE (id_empresa, cod_estado_cita);


--
-- Name: estados_citas estados_citas_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_citas
    ADD CONSTRAINT estados_citas_pkey PRIMARY KEY (id_estado_cita);


--
-- Name: estados_civiles estados_civiles_des_estado_civil_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_civiles
    ADD CONSTRAINT estados_civiles_des_estado_civil_key UNIQUE (des_estado_civil);


--
-- Name: estados_civiles estados_civiles_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_civiles
    ADD CONSTRAINT estados_civiles_pkey PRIMARY KEY (id_estado_civil);


--
-- Name: estados_factura estados_factura_cod_estado_factura_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_factura
    ADD CONSTRAINT estados_factura_cod_estado_factura_key UNIQUE (cod_estado_factura);


--
-- Name: estados_factura estados_factura_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.estados_factura
    ADD CONSTRAINT estados_factura_pkey PRIMARY KEY (id_estado_factura);


--
-- Name: feriados feriados_id_empresa_fecha_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.feriados
    ADD CONSTRAINT feriados_id_empresa_fecha_key UNIQUE (id_empresa, fecha);


--
-- Name: feriados feriados_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.feriados
    ADD CONSTRAINT feriados_pkey PRIMARY KEY (id_feriado);


--
-- Name: formas_cobro formas_cobro_cod_forma_cobro_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.formas_cobro
    ADD CONSTRAINT formas_cobro_cod_forma_cobro_key UNIQUE (cod_forma_cobro);


--
-- Name: formas_cobro formas_cobro_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.formas_cobro
    ADD CONSTRAINT formas_cobro_pkey PRIMARY KEY (id_forma_cobro);


--
-- Name: frecuencias_agendamiento frecuencias_agendamiento_cod_frecuencia_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.frecuencias_agendamiento
    ADD CONSTRAINT frecuencias_agendamiento_cod_frecuencia_key UNIQUE (cod_frecuencia);


--
-- Name: frecuencias_agendamiento frecuencias_agendamiento_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.frecuencias_agendamiento
    ADD CONSTRAINT frecuencias_agendamiento_pkey PRIMARY KEY (id_frecuencia_agendamiento);


--
-- Name: funcionarios funcionarios_id_empresa_id_persona_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.funcionarios
    ADD CONSTRAINT funcionarios_id_empresa_id_persona_key UNIQUE (id_empresa, id_persona);


--
-- Name: funcionarios funcionarios_id_usuario_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.funcionarios
    ADD CONSTRAINT funcionarios_id_usuario_key UNIQUE (id_usuario);


--
-- Name: funcionarios funcionarios_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.funcionarios
    ADD CONSTRAINT funcionarios_pkey PRIMARY KEY (id_funcionario);


--
-- Name: generos generos_des_genero_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.generos
    ADD CONSTRAINT generos_des_genero_key UNIQUE (des_genero);


--
-- Name: generos generos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.generos
    ADD CONSTRAINT generos_pkey PRIMARY KEY (id_genero);


--
-- Name: historial_suscripciones historial_suscripciones_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.historial_suscripciones
    ADD CONSTRAINT historial_suscripciones_pkey PRIMARY KEY (id_historial_suscripcion);


--
-- Name: licencias licencias_clave_licencia_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.licencias
    ADD CONSTRAINT licencias_clave_licencia_key UNIQUE (clave_licencia);


--
-- Name: licencias licencias_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.licencias
    ADD CONSTRAINT licencias_pkey PRIMARY KEY (id_licencia);


--
-- Name: lista_espera lista_espera_id_agenda_horario_id_paciente_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.lista_espera
    ADD CONSTRAINT lista_espera_id_agenda_horario_id_paciente_key UNIQUE (id_agenda_horario, id_paciente);


--
-- Name: lista_espera lista_espera_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.lista_espera
    ADD CONSTRAINT lista_espera_pkey PRIMARY KEY (id_lista_espera);


--
-- Name: login_attempts login_attempts_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.login_attempts
    ADD CONSTRAINT login_attempts_pkey PRIMARY KEY (id_login_attempt);


--
-- Name: marcas_tarjeta marcas_tarjeta_des_marca_tarjeta_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.marcas_tarjeta
    ADD CONSTRAINT marcas_tarjeta_des_marca_tarjeta_key UNIQUE (des_marca_tarjeta);


--
-- Name: marcas_tarjeta marcas_tarjeta_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.marcas_tarjeta
    ADD CONSTRAINT marcas_tarjeta_pkey PRIMARY KEY (id_marca_tarjeta);


--
-- Name: metricas_diarias metricas_diarias_id_empresa_id_sede_dia_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.metricas_diarias
    ADD CONSTRAINT metricas_diarias_id_empresa_id_sede_dia_key UNIQUE (id_empresa, id_sede, dia);


--
-- Name: metricas_diarias metricas_diarias_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.metricas_diarias
    ADD CONSTRAINT metricas_diarias_pkey PRIMARY KEY (id_metrica_diaria);


--
-- Name: mfa_tokens mfa_tokens_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.mfa_tokens
    ADD CONSTRAINT mfa_tokens_pkey PRIMARY KEY (id_mfa_token);


--
-- Name: modulos modulos_cod_modulo_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.modulos
    ADD CONSTRAINT modulos_cod_modulo_key UNIQUE (cod_modulo);


--
-- Name: modulos modulos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.modulos
    ADD CONSTRAINT modulos_pkey PRIMARY KEY (id_modulo);


--
-- Name: monedas monedas_cod_moneda_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.monedas
    ADD CONSTRAINT monedas_cod_moneda_key UNIQUE (cod_moneda);


--
-- Name: monedas monedas_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.monedas
    ADD CONSTRAINT monedas_pkey PRIMARY KEY (id_moneda);


--
-- Name: niveles_instruccion niveles_instruccion_des_nivel_instruccion_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.niveles_instruccion
    ADD CONSTRAINT niveles_instruccion_des_nivel_instruccion_key UNIQUE (des_nivel_instruccion);


--
-- Name: niveles_instruccion niveles_instruccion_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.niveles_instruccion
    ADD CONSTRAINT niveles_instruccion_pkey PRIMARY KEY (id_nivel_instruccion);


--
-- Name: notificaciones_cola notificaciones_cola_id_empresa_idempotency_key_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_cola
    ADD CONSTRAINT notificaciones_cola_id_empresa_idempotency_key_key UNIQUE (id_empresa, idempotency_key);


--
-- Name: notificaciones_cola notificaciones_cola_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_cola
    ADD CONSTRAINT notificaciones_cola_pkey PRIMARY KEY (id_notificacion_cola);


--
-- Name: notificaciones_config notificaciones_config_id_empresa_canal_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_config
    ADD CONSTRAINT notificaciones_config_id_empresa_canal_key UNIQUE (id_empresa, canal);


--
-- Name: notificaciones_config notificaciones_config_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_config
    ADD CONSTRAINT notificaciones_config_pkey PRIMARY KEY (id_notificacion_config);


--
-- Name: notificaciones_log notificaciones_log_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_log
    ADD CONSTRAINT notificaciones_log_pkey PRIMARY KEY (id_notificacion_log);


--
-- Name: notificaciones_plantillas notificaciones_plantillas_id_empresa_canal_evento_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_plantillas
    ADD CONSTRAINT notificaciones_plantillas_id_empresa_canal_evento_key UNIQUE (id_empresa, canal, evento);


--
-- Name: notificaciones_plantillas notificaciones_plantillas_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notificaciones_plantillas
    ADD CONSTRAINT notificaciones_plantillas_pkey PRIMARY KEY (id_notificacion_plantilla);


--
-- Name: paciente_profesional paciente_profesional_id_paciente_id_especialista_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paciente_profesional
    ADD CONSTRAINT paciente_profesional_id_paciente_id_especialista_key UNIQUE (id_paciente, id_especialista) DEFERRABLE;


--
-- Name: paciente_profesional paciente_profesional_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paciente_profesional
    ADD CONSTRAINT paciente_profesional_pkey PRIMARY KEY (id_paciente_profesional);


--
-- Name: pacientes pacientes_id_empresa_id_persona_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.pacientes
    ADD CONSTRAINT pacientes_id_empresa_id_persona_key UNIQUE (id_empresa, id_persona);


--
-- Name: pacientes pacientes_id_empresa_pac_historia_clinica_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.pacientes
    ADD CONSTRAINT pacientes_id_empresa_pac_historia_clinica_key UNIQUE (id_empresa, pac_historia_clinica);


--
-- Name: pacientes_menores pacientes_menores_id_paciente_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.pacientes_menores
    ADD CONSTRAINT pacientes_menores_id_paciente_key UNIQUE (id_paciente);


--
-- Name: pacientes_menores pacientes_menores_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.pacientes_menores
    ADD CONSTRAINT pacientes_menores_pkey PRIMARY KEY (id_paciente_menor);


--
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (id_paciente);


--
-- Name: paises paises_des_pais_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paises
    ADD CONSTRAINT paises_des_pais_key UNIQUE (des_pais);


--
-- Name: paises paises_iso2_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paises
    ADD CONSTRAINT paises_iso2_key UNIQUE (iso2);


--
-- Name: paises paises_iso3_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paises
    ADD CONSTRAINT paises_iso3_key UNIQUE (iso3);


--
-- Name: paises paises_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.paises
    ADD CONSTRAINT paises_pkey PRIMARY KEY (id_pais);


--
-- Name: password_history password_history_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_history
    ADD CONSTRAINT password_history_pkey PRIMARY KEY (id_password_history);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id_password_reset_token);


--
-- Name: password_reset_tokens password_reset_tokens_token_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_token_key UNIQUE (token);


--
-- Name: permisos permisos_cod_permiso_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.permisos
    ADD CONSTRAINT permisos_cod_permiso_key UNIQUE (cod_permiso);


--
-- Name: permisos permisos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.permisos
    ADD CONSTRAINT permisos_pkey PRIMARY KEY (id_permiso);


--
-- Name: personas personas_id_empresa_per_nro_documento_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.personas
    ADD CONSTRAINT personas_id_empresa_per_nro_documento_key UNIQUE (id_empresa, per_nro_documento);


--
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id_persona);


--
-- Name: plan_modulos plan_modulos_id_plan_id_modulo_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.plan_modulos
    ADD CONSTRAINT plan_modulos_id_plan_id_modulo_key UNIQUE (id_plan, id_modulo);


--
-- Name: plan_modulos plan_modulos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.plan_modulos
    ADD CONSTRAINT plan_modulos_pkey PRIMARY KEY (id_plan_modulo);


--
-- Name: planes planes_cod_plan_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.planes
    ADD CONSTRAINT planes_cod_plan_key UNIQUE (cod_plan);


--
-- Name: planes planes_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.planes
    ADD CONSTRAINT planes_pkey PRIMARY KEY (id_plan);


--
-- Name: preferencias_ui preferencias_ui_id_usuario_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.preferencias_ui
    ADD CONSTRAINT preferencias_ui_id_usuario_key UNIQUE (id_usuario);


--
-- Name: preferencias_ui preferencias_ui_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.preferencias_ui
    ADD CONSTRAINT preferencias_ui_pkey PRIMARY KEY (id_preferencia_ui);


--
-- Name: profesiones profesiones_des_profesion_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.profesiones
    ADD CONSTRAINT profesiones_des_profesion_key UNIQUE (des_profesion);


--
-- Name: profesiones profesiones_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.profesiones
    ADD CONSTRAINT profesiones_pkey PRIMARY KEY (id_profesion);


--
-- Name: puntos_expedicion puntos_expedicion_id_establecimiento_cod_punto_expedicion_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.puntos_expedicion
    ADD CONSTRAINT puntos_expedicion_id_establecimiento_cod_punto_expedicion_key UNIQUE (id_establecimiento, cod_punto_expedicion);


--
-- Name: puntos_expedicion puntos_expedicion_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.puntos_expedicion
    ADD CONSTRAINT puntos_expedicion_pkey PRIMARY KEY (id_punto_expedicion);


--
-- Name: recordatorios recordatorios_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.recordatorios
    ADD CONSTRAINT recordatorios_pkey PRIMARY KEY (id_recordatorio);


--
-- Name: reportes_jobs_log reportes_jobs_log_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.reportes_jobs_log
    ADD CONSTRAINT reportes_jobs_log_pkey PRIMARY KEY (id_reporte_job_log);


--
-- Name: reportes_jobs reportes_jobs_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.reportes_jobs
    ADD CONSTRAINT reportes_jobs_pkey PRIMARY KEY (id_reporte_job);


--
-- Name: roles_base roles_base_cod_rol_base_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_base
    ADD CONSTRAINT roles_base_cod_rol_base_key UNIQUE (cod_rol_base);


--
-- Name: roles_base roles_base_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_base
    ADD CONSTRAINT roles_base_pkey PRIMARY KEY (id_rol_base);


--
-- Name: roles_empresa roles_empresa_id_empresa_cod_rol_empresa_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_empresa
    ADD CONSTRAINT roles_empresa_id_empresa_cod_rol_empresa_key UNIQUE (id_empresa, cod_rol_empresa);


--
-- Name: roles_empresa_permisos roles_empresa_permisos_id_rol_empresa_id_permiso_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_empresa_permisos
    ADD CONSTRAINT roles_empresa_permisos_id_rol_empresa_id_permiso_key UNIQUE (id_rol_empresa, id_permiso);


--
-- Name: roles_empresa_permisos roles_empresa_permisos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_empresa_permisos
    ADD CONSTRAINT roles_empresa_permisos_pkey PRIMARY KEY (id_rol_empresa_permiso);


--
-- Name: roles_empresa roles_empresa_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles_empresa
    ADD CONSTRAINT roles_empresa_pkey PRIMARY KEY (id_rol_empresa);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (id_schema_migration);


--
-- Name: schema_migrations schema_migrations_version_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.schema_migrations
    ADD CONSTRAINT schema_migrations_version_key UNIQUE (version);


--
-- Name: sedes sedes_id_empresa_des_sede_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.sedes
    ADD CONSTRAINT sedes_id_empresa_des_sede_key UNIQUE (id_empresa, des_sede);


--
-- Name: sedes sedes_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.sedes
    ADD CONSTRAINT sedes_pkey PRIMARY KEY (id_sede);


--
-- Name: sesiones sesiones_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.sesiones
    ADD CONSTRAINT sesiones_pkey PRIMARY KEY (id_sesion);


--
-- Name: sesiones sesiones_token_sesion_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.sesiones
    ADD CONSTRAINT sesiones_token_sesion_key UNIQUE (token_sesion);


--
-- Name: slots_agenda slots_agenda_id_agenda_horario_slot_inicio_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.slots_agenda
    ADD CONSTRAINT slots_agenda_id_agenda_horario_slot_inicio_key UNIQUE (id_agenda_horario, slot_inicio);


--
-- Name: slots_agenda slots_agenda_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.slots_agenda
    ADD CONSTRAINT slots_agenda_pkey PRIMARY KEY (id_slot_agenda);


--
-- Name: suscripcion_excedentes suscripcion_excedentes_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.suscripcion_excedentes
    ADD CONSTRAINT suscripcion_excedentes_pkey PRIMARY KEY (id_suscripcion_excedente);


--
-- Name: suscripcion_expansiones suscripcion_expansiones_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.suscripcion_expansiones
    ADD CONSTRAINT suscripcion_expansiones_pkey PRIMARY KEY (id_expansion);


--
-- Name: suscripciones suscripciones_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.suscripciones
    ADD CONSTRAINT suscripciones_pkey PRIMARY KEY (id_suscripcion);


--
-- Name: tipos_clinicos tipos_clinicos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_clinicos
    ADD CONSTRAINT tipos_clinicos_pkey PRIMARY KEY (cod_tipo_clinico);


--
-- Name: tipos_comprobantes tipos_comprobantes_cod_tipo_comprobante_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_comprobantes
    ADD CONSTRAINT tipos_comprobantes_cod_tipo_comprobante_key UNIQUE (cod_tipo_comprobante);


--
-- Name: tipos_comprobantes tipos_comprobantes_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_comprobantes
    ADD CONSTRAINT tipos_comprobantes_pkey PRIMARY KEY (id_tipo_comprobante);


--
-- Name: tipos_documentos_identidad tipos_documentos_identidad_cod_sifen_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_documentos_identidad
    ADD CONSTRAINT tipos_documentos_identidad_cod_sifen_key UNIQUE (cod_sifen);


--
-- Name: tipos_documentos_identidad tipos_documentos_identidad_cod_tipo_documento_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_documentos_identidad
    ADD CONSTRAINT tipos_documentos_identidad_cod_tipo_documento_key UNIQUE (cod_tipo_documento);


--
-- Name: tipos_documentos_identidad tipos_documentos_identidad_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_documentos_identidad
    ADD CONSTRAINT tipos_documentos_identidad_pkey PRIMARY KEY (id_tipo_documento);


--
-- Name: tipos_impuestos tipos_impuestos_cod_tipo_impuesto_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_impuestos
    ADD CONSTRAINT tipos_impuestos_cod_tipo_impuesto_key UNIQUE (cod_tipo_impuesto);


--
-- Name: tipos_impuestos tipos_impuestos_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_impuestos
    ADD CONSTRAINT tipos_impuestos_pkey PRIMARY KEY (id_tipo_impuesto);


--
-- Name: tipos_items tipos_items_cod_tipo_item_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_items
    ADD CONSTRAINT tipos_items_cod_tipo_item_key UNIQUE (cod_tipo_item);


--
-- Name: tipos_items tipos_items_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.tipos_items
    ADD CONSTRAINT tipos_items_pkey PRIMARY KEY (id_tipo_item);


--
-- Name: niveles_instruccion uq_cod_nivel_instruccion; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.niveles_instruccion
    ADD CONSTRAINT uq_cod_nivel_instruccion UNIQUE (cod_nivel_instruccion);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- Name: usuarios_roles_base usuarios_roles_base_id_usuario_id_rol_base_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios_roles_base
    ADD CONSTRAINT usuarios_roles_base_id_usuario_id_rol_base_key UNIQUE (id_usuario, id_rol_base);


--
-- Name: usuarios_roles_base usuarios_roles_base_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios_roles_base
    ADD CONSTRAINT usuarios_roles_base_pkey PRIMARY KEY (id_usuario_rol_base);


--
-- Name: usuarios_roles_empresa usuarios_roles_empresa_id_empresa_id_usuario_id_rol_empresa_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios_roles_empresa
    ADD CONSTRAINT usuarios_roles_empresa_id_empresa_id_usuario_id_rol_empresa_key UNIQUE (id_empresa, id_usuario, id_rol_empresa);


--
-- Name: usuarios_roles_empresa usuarios_roles_empresa_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios_roles_empresa
    ADD CONSTRAINT usuarios_roles_empresa_pkey PRIMARY KEY (id_usuario_rol_empresa);


--
-- Name: usuarios usuarios_usu_nick_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.usuarios
    ADD CONSTRAINT usuarios_usu_nick_key UNIQUE (usu_nick);


--
-- Name: aperturas_caja aperturas_caja_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.aperturas_caja
    ADD CONSTRAINT aperturas_caja_pkey PRIMARY KEY (id_apertura_caja);


--
-- Name: arqueos_caja arqueos_caja_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.arqueos_caja
    ADD CONSTRAINT arqueos_caja_pkey PRIMARY KEY (id_arqueo_caja);


--
-- Name: autofactura_detalle autofactura_detalle_id_autofactura_nro_linea_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofactura_detalle
    ADD CONSTRAINT autofactura_detalle_id_autofactura_nro_linea_key UNIQUE (id_autofactura, nro_linea);


--
-- Name: autofactura_detalle autofactura_detalle_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofactura_detalle
    ADD CONSTRAINT autofactura_detalle_pkey PRIMARY KEY (id_autofactura_detalle);


--
-- Name: autofacturas autofacturas_id_empresa_id_timbrado_nro_autofactura_cod_ser_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_id_empresa_id_timbrado_nro_autofactura_cod_ser_key UNIQUE NULLS NOT DISTINCT (id_empresa, id_timbrado, nro_autofactura, cod_serie);


--
-- Name: autofacturas autofacturas_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_pkey PRIMARY KEY (id_autofactura);


--
-- Name: cajas cajas_id_empresa_cod_caja_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cajas
    ADD CONSTRAINT cajas_id_empresa_cod_caja_key UNIQUE (id_empresa, cod_caja);


--
-- Name: cajas cajas_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cajas
    ADD CONSTRAINT cajas_pkey PRIMARY KEY (id_caja);


--
-- Name: categorias_items categorias_items_id_empresa_des_categoria_item_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.categorias_items
    ADD CONSTRAINT categorias_items_id_empresa_des_categoria_item_key UNIQUE NULLS NOT DISTINCT (id_empresa, des_categoria_item);


--
-- Name: categorias_items categorias_items_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.categorias_items
    ADD CONSTRAINT categorias_items_pkey PRIMARY KEY (id_categoria_item);


--
-- Name: cheques_recibidos cheques_recibidos_id_empresa_id_entidad_bancaria_nro_cheque_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cheques_recibidos
    ADD CONSTRAINT cheques_recibidos_id_empresa_id_entidad_bancaria_nro_cheque_key UNIQUE (id_empresa, id_entidad_bancaria, nro_cheque);


--
-- Name: cheques_recibidos cheques_recibidos_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cheques_recibidos
    ADD CONSTRAINT cheques_recibidos_pkey PRIMARY KEY (id_cheque_recibido);


--
-- Name: cobranza_detalle cobranza_detalle_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_pkey PRIMARY KEY (id_cobranza_detalle);


--
-- Name: cobranzas cobranzas_id_empresa_nro_cobranza_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT cobranzas_id_empresa_nro_cobranza_key UNIQUE (id_empresa, nro_cobranza);


--
-- Name: cobranzas cobranzas_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT cobranzas_pkey PRIMARY KEY (id_cobranza);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_empresa_nro_cuenta_cobrar_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_empresa_nro_cuenta_cobrar_key UNIQUE (id_empresa, nro_cuenta_cobrar);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_factura_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_factura_key UNIQUE (id_factura);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_nota_debito_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_nota_debito_key UNIQUE (id_nota_debito);


--
-- Name: cuentas_cobrar cuentas_cobrar_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_pkey PRIMARY KEY (id_cuenta_cobrar);


--
-- Name: cuotas_cobrar cuotas_cobrar_id_cuenta_cobrar_nro_cuota_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuotas_cobrar
    ADD CONSTRAINT cuotas_cobrar_id_cuenta_cobrar_nro_cuota_key UNIQUE (id_cuenta_cobrar, nro_cuota);


--
-- Name: cuotas_cobrar cuotas_cobrar_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuotas_cobrar
    ADD CONSTRAINT cuotas_cobrar_pkey PRIMARY KEY (id_cuota_cobrar);


--
-- Name: documentos_electronicos documentos_electronicos_cod_cdc_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.documentos_electronicos
    ADD CONSTRAINT documentos_electronicos_cod_cdc_key UNIQUE (cod_cdc);


--
-- Name: documentos_electronicos documentos_electronicos_id_empresa_nro_timbrado_cod_estable_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.documentos_electronicos
    ADD CONSTRAINT documentos_electronicos_id_empresa_nro_timbrado_cod_estable_key UNIQUE NULLS NOT DISTINCT (id_empresa, nro_timbrado, cod_establecimiento, cod_punto_expedicion, id_tipo_comprobante, nro_documento, cod_serie);


--
-- Name: documentos_electronicos documentos_electronicos_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.documentos_electronicos
    ADD CONSTRAINT documentos_electronicos_pkey PRIMARY KEY (id_de);


--
-- Name: entidades_bancarias entidades_bancarias_cod_entidad_bancaria_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_bancarias
    ADD CONSTRAINT entidades_bancarias_cod_entidad_bancaria_key UNIQUE (cod_entidad_bancaria);


--
-- Name: entidades_bancarias entidades_bancarias_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_bancarias
    ADD CONSTRAINT entidades_bancarias_pkey PRIMARY KEY (id_entidad_bancaria);


--
-- Name: entidades_pagadoras entidades_pagadoras_id_empresa_des_entidad_pagadora_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_pagadoras
    ADD CONSTRAINT entidades_pagadoras_id_empresa_des_entidad_pagadora_key UNIQUE (id_empresa, des_entidad_pagadora);


--
-- Name: entidades_pagadoras entidades_pagadoras_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_pagadoras
    ADD CONSTRAINT entidades_pagadoras_pkey PRIMARY KEY (id_entidad_pagadora);


--
-- Name: factura_detalle factura_detalle_id_factura_nro_linea_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_detalle
    ADD CONSTRAINT factura_detalle_id_factura_nro_linea_key UNIQUE (id_factura, nro_linea);


--
-- Name: factura_detalle factura_detalle_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_detalle
    ADD CONSTRAINT factura_detalle_pkey PRIMARY KEY (id_factura_detalle);


--
-- Name: factura_medios_pago factura_medios_pago_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_medios_pago
    ADD CONSTRAINT factura_medios_pago_pkey PRIMARY KEY (id_factura_medio_pago);


--
-- Name: facturas facturas_id_empresa_id_timbrado_nro_factura_cod_serie_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_empresa_id_timbrado_nro_factura_cod_serie_key UNIQUE NULLS NOT DISTINCT (id_empresa, id_timbrado, nro_factura, cod_serie);


--
-- Name: facturas facturas_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_pkey PRIMARY KEY (id_factura);


--
-- Name: items items_id_empresa_cod_item_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items
    ADD CONSTRAINT items_id_empresa_cod_item_key UNIQUE (id_empresa, cod_item);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id_item);


--
-- Name: libro_ventas libro_ventas_cod_cdc_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_cod_cdc_key UNIQUE (cod_cdc);


--
-- Name: libro_ventas libro_ventas_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_pkey PRIMARY KEY (id_libro_venta);


--
-- Name: movimientos_caja movimientos_caja_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.movimientos_caja
    ADD CONSTRAINT movimientos_caja_pkey PRIMARY KEY (id_movimiento_caja);


--
-- Name: nota_credito_detalle nota_credito_detalle_id_nota_credito_nro_linea_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_id_nota_credito_nro_linea_key UNIQUE (id_nota_credito, nro_linea);


--
-- Name: nota_credito_detalle nota_credito_detalle_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_pkey PRIMARY KEY (id_nota_credito_detalle);


--
-- Name: nota_debito_detalle nota_debito_detalle_id_nota_debito_nro_linea_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_id_nota_debito_nro_linea_key UNIQUE (id_nota_debito, nro_linea);


--
-- Name: nota_debito_detalle nota_debito_detalle_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_pkey PRIMARY KEY (id_nota_debito_detalle);


--
-- Name: nota_remision_detalle nota_remision_detalle_id_nota_remision_nro_linea_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_remision_detalle
    ADD CONSTRAINT nota_remision_detalle_id_nota_remision_nro_linea_key UNIQUE (id_nota_remision, nro_linea);


--
-- Name: nota_remision_detalle nota_remision_detalle_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_remision_detalle
    ADD CONSTRAINT nota_remision_detalle_pkey PRIMARY KEY (id_nota_remision_detalle);


--
-- Name: notas_credito notas_credito_id_empresa_id_timbrado_nro_nota_credito_cod_s_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_empresa_id_timbrado_nro_nota_credito_cod_s_key UNIQUE NULLS NOT DISTINCT (id_empresa, id_timbrado, nro_nota_credito, cod_serie);


--
-- Name: notas_credito notas_credito_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_pkey PRIMARY KEY (id_nota_credito);


--
-- Name: notas_debito notas_debito_id_empresa_id_timbrado_nro_nota_debito_cod_ser_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_empresa_id_timbrado_nro_nota_debito_cod_ser_key UNIQUE NULLS NOT DISTINCT (id_empresa, id_timbrado, nro_nota_debito, cod_serie);


--
-- Name: notas_debito notas_debito_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_pkey PRIMARY KEY (id_nota_debito);


--
-- Name: notas_remision notas_remision_id_empresa_id_timbrado_nro_nota_remision_cod_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_id_empresa_id_timbrado_nro_nota_remision_cod_key UNIQUE NULLS NOT DISTINCT (id_empresa, id_timbrado, nro_nota_remision, cod_serie);


--
-- Name: notas_remision notas_remision_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_pkey PRIMARY KEY (id_nota_remision);


--
-- Name: recaudacion_detalle recaudacion_detalle_id_recaudacion_id_cobranza_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudacion_detalle
    ADD CONSTRAINT recaudacion_detalle_id_recaudacion_id_cobranza_key UNIQUE (id_recaudacion, id_cobranza);


--
-- Name: recaudacion_detalle recaudacion_detalle_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudacion_detalle
    ADD CONSTRAINT recaudacion_detalle_pkey PRIMARY KEY (id_recaudacion_detalle);


--
-- Name: recaudaciones recaudaciones_id_empresa_nro_recaudacion_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudaciones
    ADD CONSTRAINT recaudaciones_id_empresa_nro_recaudacion_key UNIQUE (id_empresa, nro_recaudacion);


--
-- Name: recaudaciones recaudaciones_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudaciones
    ADD CONSTRAINT recaudaciones_pkey PRIMARY KEY (id_recaudacion);


--
-- Name: secuencias_numeracion secuencias_numeracion_id_empresa_id_timbrado_cod_establecim_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.secuencias_numeracion
    ADD CONSTRAINT secuencias_numeracion_id_empresa_id_timbrado_cod_establecim_key UNIQUE NULLS NOT DISTINCT (id_empresa, id_timbrado, cod_establecimiento, cod_punto_expedicion, cod_tipo_de, cod_serie);


--
-- Name: secuencias_numeracion secuencias_numeracion_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.secuencias_numeracion
    ADD CONSTRAINT secuencias_numeracion_pkey PRIMARY KEY (id_secuencia);


--
-- Name: sifen_config sifen_config_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_config
    ADD CONSTRAINT sifen_config_pkey PRIMARY KEY (id_sifen_config);


--
-- Name: sifen_eventos sifen_eventos_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_eventos
    ADD CONSTRAINT sifen_eventos_pkey PRIMARY KEY (id_evento);


--
-- Name: sifen_lote_documentos sifen_lote_documentos_id_lote_id_de_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lote_documentos
    ADD CONSTRAINT sifen_lote_documentos_id_lote_id_de_key UNIQUE (id_lote, id_de);


--
-- Name: sifen_lote_documentos sifen_lote_documentos_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lote_documentos
    ADD CONSTRAINT sifen_lote_documentos_pkey PRIMARY KEY (id_lote_documento);


--
-- Name: sifen_lotes sifen_lotes_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lotes
    ADD CONSTRAINT sifen_lotes_pkey PRIMARY KEY (id_lote);


--
-- Name: sifen_transmision_log sifen_transmision_log_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_transmision_log
    ADD CONSTRAINT sifen_transmision_log_pkey PRIMARY KEY (id_transmision_log);


--
-- Name: tarifario_precios tarifario_precios_id_item_coalesce_id_moneda_daterange_excl; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.tarifario_precios
    ADD CONSTRAINT tarifario_precios_id_item_coalesce_id_moneda_daterange_excl EXCLUDE USING gist (id_item WITH =, COALESCE(id_entidad_pagadora, 0) WITH =, id_moneda WITH =, daterange(fec_vigencia_desde, COALESCE(fec_vigencia_hasta, 'infinity'::date), '[]'::text) WITH &&) WHERE ((fec_eliminacion IS NULL));


--
-- Name: tarifario_precios tarifario_precios_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.tarifario_precios
    ADD CONSTRAINT tarifario_precios_pkey PRIMARY KEY (id_tarifario_precio);


--
-- Name: timbrado_habilitaciones timbrado_habilitaciones_id_empresa_id_timbrado_id_punto_exp_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrado_habilitaciones
    ADD CONSTRAINT timbrado_habilitaciones_id_empresa_id_timbrado_id_punto_exp_key UNIQUE (id_empresa, id_timbrado, id_punto_expedicion);


--
-- Name: timbrado_habilitaciones timbrado_habilitaciones_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrado_habilitaciones
    ADD CONSTRAINT timbrado_habilitaciones_pkey PRIMARY KEY (id_timbrado_habilitacion);


--
-- Name: timbrados timbrados_id_empresa_nro_timbrado_id_tipo_comprobante_key; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrados
    ADD CONSTRAINT timbrados_id_empresa_nro_timbrado_id_tipo_comprobante_key UNIQUE (id_empresa, nro_timbrado, id_tipo_comprobante);


--
-- Name: timbrados timbrados_pkey; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrados
    ADD CONSTRAINT timbrados_pkey PRIMARY KEY (id_timbrado);


--
-- Name: sifen_config uq_sifen_config_empresa; Type: CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_config
    ADD CONSTRAINT uq_sifen_config_empresa UNIQUE (id_empresa);


--
-- Name: idx_acuerdo_especialista; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_acuerdo_especialista ON consultorio.acuerdos_terapeuticos USING btree (id_especialista);


--
-- Name: idx_acuerdo_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_acuerdo_paciente ON consultorio.acuerdos_terapeuticos USING btree (id_empresa, id_paciente);


--
-- Name: idx_acuerdos_contrato; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_acuerdos_contrato ON consultorio.contratos_tratamiento_acuerdos_pago USING btree (id_contrato_tratamiento);


--
-- Name: idx_anamnesis_adu_anamnesis; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_anamnesis_adu_anamnesis ON consultorio.anamnesis_adulto_ext USING btree (id_anamnesis);


--
-- Name: idx_anamnesis_inf_anamnesis; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_anamnesis_inf_anamnesis ON consultorio.anamnesis_infantil_ext USING btree (id_anamnesis);


--
-- Name: idx_anamnesis_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_anamnesis_paciente ON consultorio.anamnesis USING btree (id_empresa, id_paciente);


--
-- Name: idx_anamnesis_tipo; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_anamnesis_tipo ON consultorio.anamnesis USING btree (tipo_anamnesis);


--
-- Name: idx_ant_paciente_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ant_paciente_empresa ON consultorio.antecedentes_paciente USING btree (id_empresa);


--
-- Name: idx_ant_paciente_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ant_paciente_paciente ON consultorio.antecedentes_paciente USING btree (id_paciente);


--
-- Name: idx_antecedentes_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_antecedentes_paciente ON consultorio.antecedentes_paciente USING btree (id_paciente, id_empresa);


--
-- Name: idx_cie10_codigo; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_cie10_codigo ON consultorio.diagnosticos_cie10 USING btree (codigo);


--
-- Name: idx_cie10_descripcion; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_cie10_descripcion ON consultorio.diagnosticos_cie10 USING gin (des_diagnostico public.gin_trgm_ops);


--
-- Name: idx_cobros_simples_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_cobros_simples_empresa ON consultorio.cobros_simples USING btree (id_empresa);


--
-- Name: idx_cobros_simples_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_cobros_simples_episodio ON consultorio.cobros_simples USING btree (id_episodio);


--
-- Name: idx_consentimientos_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_consentimientos_episodio ON consultorio.consentimientos_firmados USING btree (id_episodio);


--
-- Name: idx_consentimientos_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_consentimientos_paciente ON consultorio.consentimientos_firmados USING btree (id_paciente);


--
-- Name: idx_contratos_activos; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_contratos_activos ON consultorio.contratos_tratamiento USING btree (id_especialista) WHERE (cod_estado_contrato = ANY (ARRAY['ACTIVO'::text, 'PAUSADO'::text]));


--
-- Name: idx_contratos_anterior; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_contratos_anterior ON consultorio.contratos_tratamiento USING btree (id_contrato_anterior) WHERE (id_contrato_anterior IS NOT NULL);


--
-- Name: idx_contratos_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_contratos_empresa ON consultorio.contratos_tratamiento USING btree (id_empresa);


--
-- Name: idx_contratos_especialista; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_contratos_especialista ON consultorio.contratos_tratamiento USING btree (id_especialista, cod_estado_contrato);


--
-- Name: idx_contratos_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_contratos_paciente ON consultorio.contratos_tratamiento USING btree (id_paciente, fec_creacion DESC);


--
-- Name: idx_ct_pagos_factura; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ct_pagos_factura ON consultorio.contratos_tratamiento_pagos USING btree (id_factura) WHERE (id_factura IS NOT NULL);


--
-- Name: idx_deriv_destinatario; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_deriv_destinatario ON consultorio.derivaciones USING btree (id_especialista_destino) WHERE (id_especialista_destino IS NOT NULL);


--
-- Name: idx_derivaciones_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_derivaciones_episodio ON consultorio.derivaciones USING btree (id_episodio);


--
-- Name: idx_derivaciones_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_derivaciones_paciente ON consultorio.derivaciones USING btree (id_paciente, fec_emision DESC);


--
-- Name: idx_documentos_entidad; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_documentos_entidad ON consultorio.documentos_adjuntos USING btree (id_empresa, cod_tipo_entidad, id_entidad);


--
-- Name: idx_dsm5_codigo; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_dsm5_codigo ON consultorio.diagnosticos_dsm5 USING btree (codigo);


--
-- Name: idx_dsm5_descripcion; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_dsm5_descripcion ON consultorio.diagnosticos_dsm5 USING gin (des_diagnostico public.gin_trgm_ops);


--
-- Name: idx_ep_insumos_procedimiento; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ep_insumos_procedimiento ON consultorio.episodio_procedimientos_insumos USING btree (id_episodio_procedimiento);


--
-- Name: idx_ep_procedimientos_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ep_procedimientos_episodio ON consultorio.episodio_procedimientos USING btree (id_episodio);


--
-- Name: idx_epc_tipo; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_epc_tipo ON consultorio.empresa_perfil_clinico USING btree (cod_tipo_clinico);


--
-- Name: idx_episodio_diag_cronicos; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodio_diag_cronicos ON consultorio.episodio_diagnosticos USING btree (id_paciente) WHERE (es_cronico = true);


--
-- Name: idx_episodio_diag_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodio_diag_episodio ON consultorio.episodio_diagnosticos USING btree (id_episodio);


--
-- Name: idx_episodio_diag_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodio_diag_paciente ON consultorio.episodio_diagnosticos USING btree (id_paciente, id_episodio);


--
-- Name: idx_episodios_cita; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodios_cita ON consultorio.episodios USING btree (id_cita) WHERE (id_cita IS NOT NULL);


--
-- Name: idx_episodios_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodios_empresa ON consultorio.episodios USING btree (id_empresa);


--
-- Name: idx_episodios_especialista; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodios_especialista ON consultorio.episodios USING btree (id_especialista, fec_apertura DESC);


--
-- Name: idx_episodios_estado; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodios_estado ON consultorio.episodios USING btree (id_empresa, cod_estado_episodio) WHERE (cod_estado_episodio = ANY (ARRAY['EN_SALA'::text, 'EN_CONSULTA'::text]));


--
-- Name: idx_episodios_origen; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodios_origen ON consultorio.episodios USING btree (id_episodio_origen) WHERE (id_episodio_origen IS NOT NULL);


--
-- Name: idx_episodios_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_episodios_paciente ON consultorio.episodios USING btree (id_paciente, fec_apertura DESC);


--
-- Name: idx_equiv_cie10; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_equiv_cie10 ON consultorio.diagnosticos_cie10_dsm5_equivalencias USING btree (id_diagnostico_cie10);


--
-- Name: idx_equiv_dsm5; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_equiv_dsm5 ON consultorio.diagnosticos_cie10_dsm5_equivalencias USING btree (id_diagnostico_dsm5);


--
-- Name: idx_fichas_clinicas_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_fichas_clinicas_episodio ON consultorio.fichas_clinicas USING btree (id_episodio);


--
-- Name: idx_fichas_psicologia_ficha; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_fichas_psicologia_ficha ON consultorio.fichas_psicologia USING btree (id_ficha_clinica);


--
-- Name: idx_formulario_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_formulario_empresa ON consultorio.formularios_definicion USING btree (id_empresa);


--
-- Name: idx_formulario_especialidad; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_formulario_especialidad ON consultorio.formularios_definicion USING btree (id_empresa, cod_especialidad) WHERE (cod_especialidad IS NOT NULL);


--
-- Name: idx_indicaciones_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_indicaciones_episodio ON consultorio.indicaciones_no_farmacologicas USING btree (id_episodio);


--
-- Name: idx_insumo_empresa_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_insumo_empresa_empresa ON consultorio.insumos_empresa USING btree (id_empresa);


--
-- Name: idx_justif_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_justif_episodio ON consultorio.justificativos USING btree (id_episodio) WHERE (id_episodio IS NOT NULL);


--
-- Name: idx_justif_nro_doc; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_justif_nro_doc ON consultorio.justificativos USING btree (id_empresa, nro_documento);


--
-- Name: idx_justif_origen; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_justif_origen ON consultorio.justificativos USING btree (id_justificativo_origen) WHERE (id_justificativo_origen IS NOT NULL);


--
-- Name: idx_justif_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_justif_paciente ON consultorio.justificativos USING btree (id_paciente, fec_emision DESC);


--
-- Name: idx_med_empresa_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_med_empresa_empresa ON consultorio.medicamentos_empresa USING btree (id_empresa);


--
-- Name: idx_med_empresa_nombre; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_med_empresa_nombre ON consultorio.medicamentos_empresa USING gin (des_medicamento public.gin_trgm_ops);


--
-- Name: idx_modalidades_contrato; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_modalidades_contrato ON consultorio.contratos_tratamiento_modalidades_pago USING btree (id_contrato_tratamiento);


--
-- Name: idx_monto_acuerdo; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_monto_acuerdo ON consultorio.acuerdo_monto_historial USING btree (id_acuerdo_terapeutico);


--
-- Name: idx_monto_vigente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_monto_vigente ON consultorio.acuerdo_monto_historial USING btree (id_acuerdo_terapeutico) WHERE (fec_vigencia_hasta IS NULL);


--
-- Name: idx_notas_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_notas_episodio ON consultorio.notas_evolucion USING btree (id_episodio, fec_nota DESC);


--
-- Name: idx_notas_plan; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_notas_plan ON consultorio.notas_evolucion USING btree (id_plan_tratamiento) WHERE (id_plan_tratamiento IS NOT NULL);


--
-- Name: idx_ord_ana_det_orden; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ord_ana_det_orden ON consultorio.ordenes_analisis_detalle USING btree (id_orden_analisis, nro_orden);


--
-- Name: idx_ord_est_det_orden; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ord_est_det_orden ON consultorio.ordenes_estudios_detalle USING btree (id_orden_estudios, nro_orden);


--
-- Name: idx_ordenes_ana_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ordenes_ana_episodio ON consultorio.ordenes_analisis USING btree (id_episodio);


--
-- Name: idx_ordenes_ana_origen; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ordenes_ana_origen ON consultorio.ordenes_analisis USING btree (id_orden_analisis_origen) WHERE (id_orden_analisis_origen IS NOT NULL);


--
-- Name: idx_ordenes_ana_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ordenes_ana_paciente ON consultorio.ordenes_analisis USING btree (id_paciente, fec_emision DESC);


--
-- Name: idx_ordenes_est_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ordenes_est_episodio ON consultorio.ordenes_estudios USING btree (id_episodio);


--
-- Name: idx_ordenes_est_origen; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ordenes_est_origen ON consultorio.ordenes_estudios USING btree (id_orden_estudios_origen) WHERE (id_orden_estudios_origen IS NOT NULL);


--
-- Name: idx_ordenes_est_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_ordenes_est_paciente ON consultorio.ordenes_estudios USING btree (id_paciente, fec_emision DESC);


--
-- Name: idx_paciente_tokens_activos; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_paciente_tokens_activos ON consultorio.paciente_tokens USING btree (id_empresa, cod_estado_token) WHERE (cod_estado_token = 'ACTIVO'::text);


--
-- Name: idx_paciente_tokens_lookup; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_paciente_tokens_lookup ON consultorio.paciente_tokens USING btree (des_token);


--
-- Name: idx_paciente_tokens_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_paciente_tokens_paciente ON consultorio.paciente_tokens USING btree (id_paciente, id_empresa);


--
-- Name: idx_pagos_contrato; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pagos_contrato ON consultorio.contratos_tratamiento_pagos USING btree (id_contrato_tratamiento, fec_pago DESC);


--
-- Name: idx_pagos_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pagos_empresa ON consultorio.contratos_tratamiento_pagos USING btree (id_empresa, fec_pago DESC);


--
-- Name: idx_pei_actividades_sesion; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_actividades_sesion ON consultorio.pei_sesion_actividades USING btree (id_pei_sesion);


--
-- Name: idx_pei_areas; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_areas ON consultorio.pei USING gin (areas_intervencion);


--
-- Name: idx_pei_calendario_cobro; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_calendario_cobro ON consultorio.pei_calendario_eventos USING btree (id_pei) WHERE (es_genera_cobro = true);


--
-- Name: idx_pei_calendario_fecha; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_calendario_fecha ON consultorio.pei_calendario_eventos USING btree (fec_evento);


--
-- Name: idx_pei_calendario_pei; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_calendario_pei ON consultorio.pei_calendario_eventos USING btree (id_pei);


--
-- Name: idx_pei_empresa_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_empresa_paciente ON consultorio.pei USING btree (id_empresa, id_paciente);


--
-- Name: idx_pei_especialista; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_especialista ON consultorio.pei USING btree (id_especialista);


--
-- Name: idx_pei_estrategias_pei; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_estrategias_pei ON consultorio.pei_estrategias USING btree (id_pei);


--
-- Name: idx_pei_habilidades_registro; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_habilidades_registro ON consultorio.pei_habilidades_entrenamiento USING btree (id_pei_registro_mensual);


--
-- Name: idx_pei_objetivos_pei; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_objetivos_pei ON consultorio.pei_objetivos USING btree (id_pei);


--
-- Name: idx_pei_participantes_reunion; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_participantes_reunion ON consultorio.pei_reunion_participantes USING btree (id_pei_reunion_clinica);


--
-- Name: idx_pei_recomendaciones_pendientes; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_recomendaciones_pendientes ON consultorio.pei_reunion_recomendaciones USING btree (id_pei_reunion_clinica) WHERE (es_cumplida = false);


--
-- Name: idx_pei_recomendaciones_reunion; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_recomendaciones_reunion ON consultorio.pei_reunion_recomendaciones USING btree (id_pei_reunion_clinica);


--
-- Name: idx_pei_registro_pei; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_registro_pei ON consultorio.pei_registro_mensual USING btree (id_pei);


--
-- Name: idx_pei_reunion_fecha; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_reunion_fecha ON consultorio.pei_reunion_clinica USING btree (fec_reunion);


--
-- Name: idx_pei_reunion_pei; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_reunion_pei ON consultorio.pei_reunion_clinica USING btree (id_pei);


--
-- Name: idx_pei_sesion_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_sesion_episodio ON consultorio.pei_sesion_planificada USING btree (id_episodio) WHERE (id_episodio IS NOT NULL);


--
-- Name: idx_pei_sesion_pei; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pei_sesion_pei ON consultorio.pei_sesion_planificada USING btree (id_pei);


--
-- Name: idx_planes_trat_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_planes_trat_episodio ON consultorio.planes_tratamiento USING btree (id_episodio);


--
-- Name: idx_planes_trat_estado; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_planes_trat_estado ON consultorio.planes_tratamiento USING btree (id_especialista, cod_estado_plan) WHERE (cod_estado_plan = 'ACTIVO'::text);


--
-- Name: idx_planes_trat_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_planes_trat_paciente ON consultorio.planes_tratamiento USING btree (id_paciente, fec_creacion DESC);


--
-- Name: idx_plantilla_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_plantilla_empresa ON consultorio.plantillas_justificativos USING btree (id_empresa);


--
-- Name: idx_plantilla_tipo; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_plantilla_tipo ON consultorio.plantillas_justificativos USING btree (id_tipo_justificativo);


--
-- Name: idx_proc_empresa_empresa; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_proc_empresa_empresa ON consultorio.procedimientos_empresa USING btree (id_empresa);


--
-- Name: idx_proc_empresa_tipo; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_proc_empresa_tipo ON consultorio.procedimientos_empresa USING btree (id_tipo_procedimiento) WHERE (id_tipo_procedimiento IS NOT NULL);


--
-- Name: idx_pti_plan; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_pti_plan ON consultorio.planes_tratamiento_items USING btree (id_plan_tratamiento, nro_orden);


--
-- Name: idx_rad_alertas; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_rad_alertas ON consultorio.resultados_analisis_detalle USING btree (id_resultado_analisis) WHERE (es_fuera_rango = true);


--
-- Name: idx_rad_resultado; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_rad_resultado ON consultorio.resultados_analisis_detalle USING btree (id_resultado_analisis);


--
-- Name: idx_recetas_det_receta; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_recetas_det_receta ON consultorio.recetas_detalle USING btree (id_receta, nro_orden);


--
-- Name: idx_recetas_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_recetas_episodio ON consultorio.recetas USING btree (id_episodio);


--
-- Name: idx_recetas_origen; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_recetas_origen ON consultorio.recetas USING btree (id_receta_origen) WHERE (id_receta_origen IS NOT NULL);


--
-- Name: idx_recetas_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_recetas_paciente ON consultorio.recetas USING btree (id_paciente, fec_emision DESC);


--
-- Name: idx_resultado_ana_orden; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_resultado_ana_orden ON consultorio.resultados_analisis USING btree (id_orden_analisis, fec_resultado DESC);


--
-- Name: idx_sesiones_cita; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_sesiones_cita ON consultorio.contratos_tratamiento_sesiones USING btree (id_cita) WHERE (id_cita IS NOT NULL);


--
-- Name: idx_sesiones_contrato; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_sesiones_contrato ON consultorio.contratos_tratamiento_sesiones USING btree (id_contrato_tratamiento, nro_sesion);


--
-- Name: idx_sesiones_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_sesiones_episodio ON consultorio.contratos_tratamiento_sesiones USING btree (id_episodio) WHERE (id_episodio IS NOT NULL);


--
-- Name: idx_sesiones_pendientes; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_sesiones_pendientes ON consultorio.contratos_tratamiento_sesiones USING btree (id_contrato_tratamiento) WHERE (cod_estado_sesion = 'PROGRAMADA'::text);


--
-- Name: idx_signos_vitales_episodio; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_signos_vitales_episodio ON consultorio.signos_vitales USING btree (id_episodio);


--
-- Name: idx_signos_vitales_paciente; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_signos_vitales_paciente ON consultorio.signos_vitales USING btree (id_paciente, fec_toma DESC);


--
-- Name: idx_svd_signos_vitales; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_svd_signos_vitales ON consultorio.signos_vitales_detalle USING btree (id_signos_vitales);


--
-- Name: idx_tipos_procedimientos_especialidad; Type: INDEX; Schema: consultorio; Owner: postgres
--

CREATE INDEX idx_tipos_procedimientos_especialidad ON consultorio.tipos_procedimientos USING btree (cod_especialidad_base) WHERE (cod_especialidad_base IS NOT NULL);


--
-- Name: idx_auditoria_detalle; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_auditoria_detalle ON ONLY core.auditoria_sistema USING gin (detalle);


--
-- Name: auditoria_sistema_y2026_detalle_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2026_detalle_idx ON core.auditoria_sistema_y2026 USING gin (detalle);


--
-- Name: idx_auditoria_empresa_fecha; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_auditoria_empresa_fecha ON ONLY core.auditoria_sistema USING btree (id_empresa, fec_evento DESC);


--
-- Name: auditoria_sistema_y2026_id_empresa_fec_evento_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2026_id_empresa_fec_evento_idx ON core.auditoria_sistema_y2026 USING btree (id_empresa, fec_evento DESC);


--
-- Name: idx_auditoria_usuario_fecha; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_auditoria_usuario_fecha ON ONLY core.auditoria_sistema USING btree (id_usuario, fec_evento DESC);


--
-- Name: auditoria_sistema_y2026_id_usuario_fec_evento_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2026_id_usuario_fec_evento_idx ON core.auditoria_sistema_y2026 USING btree (id_usuario, fec_evento DESC);


--
-- Name: auditoria_sistema_y2027_detalle_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2027_detalle_idx ON core.auditoria_sistema_y2027 USING gin (detalle);


--
-- Name: auditoria_sistema_y2027_id_empresa_fec_evento_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2027_id_empresa_fec_evento_idx ON core.auditoria_sistema_y2027 USING btree (id_empresa, fec_evento DESC);


--
-- Name: auditoria_sistema_y2027_id_usuario_fec_evento_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2027_id_usuario_fec_evento_idx ON core.auditoria_sistema_y2027 USING btree (id_usuario, fec_evento DESC);


--
-- Name: auditoria_sistema_y2028_detalle_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2028_detalle_idx ON core.auditoria_sistema_y2028 USING gin (detalle);


--
-- Name: auditoria_sistema_y2028_id_empresa_fec_evento_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2028_id_empresa_fec_evento_idx ON core.auditoria_sistema_y2028 USING btree (id_empresa, fec_evento DESC);


--
-- Name: auditoria_sistema_y2028_id_usuario_fec_evento_idx; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX auditoria_sistema_y2028_id_usuario_fec_evento_idx ON core.auditoria_sistema_y2028 USING btree (id_usuario, fec_evento DESC);


--
-- Name: idx_agenda_excepciones_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_agenda_excepciones_empresa ON core.agenda_horarios_excepciones USING btree (id_empresa, fec_inicio DESC);


--
-- Name: idx_agenda_horarios_consultorio; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_agenda_horarios_consultorio ON core.agenda_horarios USING btree (id_empresa, id_consultorio, fec_desde DESC);


--
-- Name: idx_agenda_horarios_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_agenda_horarios_empresa ON core.agenda_horarios USING btree (id_empresa);


--
-- Name: idx_agenda_horarios_especialista; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_agenda_horarios_especialista ON core.agenda_horarios USING btree (id_empresa, id_especialista, fec_desde DESC);


--
-- Name: idx_cargos_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_cargos_empresa ON core.cargos USING btree (id_empresa);


--
-- Name: idx_citas_contrato; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_citas_contrato ON core.citas USING btree (id_contrato_tratamiento) WHERE (id_contrato_tratamiento IS NOT NULL);


--
-- Name: idx_citas_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_citas_empresa ON core.citas USING btree (id_empresa);


--
-- Name: idx_citas_empresa_especialista; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_citas_empresa_especialista ON core.citas USING btree (id_empresa, id_especialista, cita_inicio DESC);


--
-- Name: idx_citas_empresa_inicio; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_citas_empresa_inicio ON core.citas USING btree (id_empresa, cita_inicio DESC);


--
-- Name: idx_citas_empresa_paciente; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_citas_empresa_paciente ON core.citas USING btree (id_empresa, id_paciente, cita_inicio DESC);


--
-- Name: idx_citas_estado; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_citas_estado ON core.citas USING btree (id_empresa, id_estado_cita, cita_inicio DESC);


--
-- Name: idx_citas_log_empresa_cita; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_citas_log_empresa_cita ON core.citas_log_estados USING btree (id_empresa, id_cita, fec_cambio DESC);


--
-- Name: idx_ciudades_departamento; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_ciudades_departamento ON core.ciudades USING btree (id_departamento);


--
-- Name: idx_consultorios_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_consultorios_empresa ON core.consultorios USING btree (id_empresa);


--
-- Name: idx_consultorios_sede; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_consultorios_sede ON core.consultorios USING btree (id_sede);


--
-- Name: idx_departamentos_pais; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_departamentos_pais ON core.departamentos USING btree (id_pais);


--
-- Name: idx_empresa_certificados_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresa_certificados_empresa ON core.empresa_certificados USING btree (id_empresa);


--
-- Name: idx_empresa_configuracion_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresa_configuracion_empresa ON core.empresa_configuracion USING btree (id_empresa);


--
-- Name: idx_empresa_configuracion_json; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresa_configuracion_json ON core.empresa_configuracion USING gin (config_json);


--
-- Name: idx_empresa_modulos_activos; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresa_modulos_activos ON core.empresa_modulos USING btree (id_empresa) WHERE (est_empresa_modulo IS TRUE);


--
-- Name: idx_empresa_modulos_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresa_modulos_empresa ON core.empresa_modulos USING btree (id_empresa);


--
-- Name: idx_empresa_modulos_modulo; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresa_modulos_modulo ON core.empresa_modulos USING btree (id_modulo);


--
-- Name: idx_empresas_est; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresas_est ON core.empresas USING btree (est_empresa) WHERE (est_empresa IS TRUE);


--
-- Name: idx_empresas_estado; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresas_estado ON core.empresas USING btree (estado_empresa);


--
-- Name: idx_empresas_tipo; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_empresas_tipo ON core.empresas USING btree (tipo_empresa);


--
-- Name: idx_especialidades_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_especialidades_empresa ON core.especialidades USING btree (id_empresa);


--
-- Name: idx_especialidades_tipo_clinico; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_especialidades_tipo_clinico ON core.especialidades USING btree (cod_tipo_clinico);


--
-- Name: idx_especialista_especialidades_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_especialista_especialidades_empresa ON core.especialista_especialidades USING btree (id_empresa);


--
-- Name: idx_especialista_especialidades_especialista; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_especialista_especialidades_especialista ON core.especialista_especialidades USING btree (id_especialista);


--
-- Name: idx_especialistas_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_especialistas_empresa ON core.especialistas USING btree (id_empresa);


--
-- Name: idx_establecimientos_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_establecimientos_empresa ON core.establecimientos USING btree (id_empresa);


--
-- Name: idx_establecimientos_sede; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_establecimientos_sede ON core.establecimientos USING btree (id_sede);


--
-- Name: idx_estados_citas_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_estados_citas_empresa ON core.estados_citas USING btree (id_empresa);


--
-- Name: idx_feriados_empresa_fecha; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_feriados_empresa_fecha ON core.feriados USING btree (id_empresa, fecha);


--
-- Name: idx_funcionarios_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_funcionarios_empresa ON core.funcionarios USING btree (id_empresa);


--
-- Name: idx_funcionarios_usuario; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_funcionarios_usuario ON core.funcionarios USING btree (id_usuario) WHERE (id_usuario IS NOT NULL);


--
-- Name: idx_hist_suscripciones_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_hist_suscripciones_empresa ON core.historial_suscripciones USING btree (id_empresa, fec_evento DESC);


--
-- Name: idx_licencias_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_licencias_empresa ON core.licencias USING btree (id_empresa);


--
-- Name: idx_lista_espera_empresa_estado; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_lista_espera_empresa_estado ON core.lista_espera USING btree (id_empresa, estado, fec_solicitud DESC);


--
-- Name: idx_login_attempts_empresa_fecha; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_login_attempts_empresa_fecha ON core.login_attempts USING btree (id_empresa, fec_intento DESC);


--
-- Name: idx_login_attempts_ip; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_login_attempts_ip ON core.login_attempts USING btree (ip_address, fec_intento DESC);


--
-- Name: idx_login_attempts_pais; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_login_attempts_pais ON core.login_attempts USING btree (pais_origen, fec_intento DESC);


--
-- Name: idx_metricas_diarias_empresa_dia; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_metricas_diarias_empresa_dia ON core.metricas_diarias USING btree (id_empresa, dia DESC);


--
-- Name: idx_mfa_tokens_activos; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_mfa_tokens_activos ON core.mfa_tokens USING btree (id_usuario, fue_usado, fec_expiracion);


--
-- Name: idx_mfa_tokens_usuario; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_mfa_tokens_usuario ON core.mfa_tokens USING btree (id_usuario);


--
-- Name: idx_modulos_est; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_modulos_est ON core.modulos USING btree (est_modulo) WHERE (est_modulo IS TRUE);


--
-- Name: idx_notif_cola_empresa_estado; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_notif_cola_empresa_estado ON core.notificaciones_cola USING btree (id_empresa, estado, fec_disponible_desde);


--
-- Name: idx_notif_cola_payload; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_notif_cola_payload ON core.notificaciones_cola USING gin (payload);


--
-- Name: idx_notif_log_empresa_fecha; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_notif_log_empresa_fecha ON core.notificaciones_log USING btree (id_empresa, fec_evento DESC);


--
-- Name: idx_notif_log_respuesta; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_notif_log_respuesta ON core.notificaciones_log USING gin (respuesta);


--
-- Name: idx_notif_plantillas_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_notif_plantillas_empresa ON core.notificaciones_plantillas USING btree (id_empresa);


--
-- Name: idx_notificaciones_config_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_notificaciones_config_empresa ON core.notificaciones_config USING btree (id_empresa);


--
-- Name: idx_notificaciones_config_json; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_notificaciones_config_json ON core.notificaciones_config USING gin (config);


--
-- Name: idx_paciente_profesional_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_paciente_profesional_empresa ON core.paciente_profesional USING btree (id_empresa);


--
-- Name: idx_paciente_profesional_especialista; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_paciente_profesional_especialista ON core.paciente_profesional USING btree (id_empresa, id_especialista);


--
-- Name: idx_paciente_profesional_paciente; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_paciente_profesional_paciente ON core.paciente_profesional USING btree (id_empresa, id_paciente);


--
-- Name: idx_pacientes_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_pacientes_empresa ON core.pacientes USING btree (id_empresa);


--
-- Name: idx_pacientes_menores_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_pacientes_menores_empresa ON core.pacientes_menores USING btree (id_empresa);


--
-- Name: idx_paises_est; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_paises_est ON core.paises USING btree (est_pais) WHERE (est_pais IS TRUE);


--
-- Name: idx_password_history_usuario; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_password_history_usuario ON core.password_history USING btree (id_usuario, fec_cambio DESC);


--
-- Name: idx_password_reset_tokens_usuario; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_password_reset_tokens_usuario ON core.password_reset_tokens USING btree (id_usuario, fec_expiracion DESC);


--
-- Name: idx_permisos_est; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_permisos_est ON core.permisos USING btree (est_permiso) WHERE (est_permiso IS TRUE);


--
-- Name: idx_personas_doc_global; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_personas_doc_global ON core.personas USING btree (per_nro_documento);


--
-- Name: idx_personas_documento; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_personas_documento ON core.personas USING btree (id_empresa, per_nro_documento);


--
-- Name: idx_personas_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_personas_empresa ON core.personas USING btree (id_empresa);


--
-- Name: idx_personas_nombre_trgm; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_personas_nombre_trgm ON core.personas USING gin ((((per_nombres || ' '::text) || per_apellidos)) public.gin_trgm_ops);


--
-- Name: idx_plan_modulos_activos; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_plan_modulos_activos ON core.plan_modulos USING btree (id_plan) WHERE (est_plan_modulo IS TRUE);


--
-- Name: idx_plan_modulos_modulo; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_plan_modulos_modulo ON core.plan_modulos USING btree (id_modulo);


--
-- Name: idx_plan_modulos_plan; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_plan_modulos_plan ON core.plan_modulos USING btree (id_plan);


--
-- Name: idx_planes_est; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_planes_est ON core.planes USING btree (est_plan) WHERE (est_plan IS TRUE);


--
-- Name: idx_preferencias_ui_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_preferencias_ui_empresa ON core.preferencias_ui USING btree (id_empresa);


--
-- Name: idx_preferencias_ui_json; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_preferencias_ui_json ON core.preferencias_ui USING gin (preferencias);


--
-- Name: idx_puntos_expedicion_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_puntos_expedicion_empresa ON core.puntos_expedicion USING btree (id_empresa);


--
-- Name: idx_puntos_expedicion_establecimiento; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_puntos_expedicion_establecimiento ON core.puntos_expedicion USING btree (id_establecimiento);


--
-- Name: idx_recordatorios_empresa_cita; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_recordatorios_empresa_cita ON core.recordatorios USING btree (id_empresa, id_cita);


--
-- Name: idx_reportes_jobs_empresa_estado; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_reportes_jobs_empresa_estado ON core.reportes_jobs USING btree (id_empresa, estado_job, fec_solicitud DESC);


--
-- Name: idx_reportes_jobs_log_job; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_reportes_jobs_log_job ON core.reportes_jobs_log USING btree (id_reporte_job, fec_log DESC);


--
-- Name: idx_reportes_jobs_log_nivel; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_reportes_jobs_log_nivel ON core.reportes_jobs_log USING btree (id_empresa, nivel, fec_log DESC);


--
-- Name: idx_reportes_jobs_parametros; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_reportes_jobs_parametros ON core.reportes_jobs USING gin (parametros);


--
-- Name: idx_roles_base_nivel; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_roles_base_nivel ON core.roles_base USING btree (nivel);


--
-- Name: idx_roles_empresa_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_roles_empresa_empresa ON core.roles_empresa USING btree (id_empresa);


--
-- Name: idx_roles_empresa_permisos_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_roles_empresa_permisos_empresa ON core.roles_empresa_permisos USING btree (id_empresa);


--
-- Name: idx_roles_empresa_permisos_permiso; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_roles_empresa_permisos_permiso ON core.roles_empresa_permisos USING btree (id_permiso);


--
-- Name: idx_sedes_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_sedes_empresa ON core.sedes USING btree (id_empresa);


--
-- Name: idx_sesiones_activas; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_sesiones_activas ON core.sesiones USING btree (id_usuario, fec_expiracion) WHERE (est_sesion IS TRUE);


--
-- Name: idx_sesiones_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_sesiones_empresa ON core.sesiones USING btree (id_empresa, est_sesion);


--
-- Name: idx_sesiones_usuario; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_sesiones_usuario ON core.sesiones USING btree (id_usuario, est_sesion);


--
-- Name: idx_slots_empresa_consultorio; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_slots_empresa_consultorio ON core.slots_agenda USING btree (id_empresa, id_consultorio, slot_inicio DESC);


--
-- Name: idx_slots_empresa_especialista; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_slots_empresa_especialista ON core.slots_agenda USING btree (id_empresa, id_especialista, slot_inicio DESC);


--
-- Name: idx_slots_empresa_inicio; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_slots_empresa_inicio ON core.slots_agenda USING btree (id_empresa, slot_inicio DESC);


--
-- Name: idx_suscripcion_excedentes_empresa_mes; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_suscripcion_excedentes_empresa_mes ON core.suscripcion_excedentes USING btree (id_empresa, mes_facturacion);


--
-- Name: idx_suscripciones_activas; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_suscripciones_activas ON core.suscripciones USING btree (id_empresa, fec_vencimiento) WHERE (est_suscripcion IS TRUE);


--
-- Name: idx_suscripciones_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_suscripciones_empresa ON core.suscripciones USING btree (id_empresa);


--
-- Name: idx_suscripciones_empresa_venc; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_suscripciones_empresa_venc ON core.suscripciones USING btree (id_empresa, fec_vencimiento DESC);


--
-- Name: idx_usuarios_activos_por_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_usuarios_activos_por_empresa ON core.usuarios USING btree (id_empresa) WHERE ((est_usuario IS TRUE) AND (id_empresa IS NOT NULL));


--
-- Name: idx_usuarios_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_usuarios_empresa ON core.usuarios USING btree (id_empresa);


--
-- Name: idx_usuarios_empresa_activos; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_usuarios_empresa_activos ON core.usuarios USING btree (id_empresa) WHERE (est_usuario IS TRUE);


--
-- Name: idx_usuarios_roles_base_usuario; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_usuarios_roles_base_usuario ON core.usuarios_roles_base USING btree (id_usuario);


--
-- Name: idx_usuarios_roles_empresa_empresa; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_usuarios_roles_empresa_empresa ON core.usuarios_roles_empresa USING btree (id_empresa);


--
-- Name: idx_usuarios_roles_empresa_usuario; Type: INDEX; Schema: core; Owner: postgres
--

CREATE INDEX idx_usuarios_roles_empresa_usuario ON core.usuarios_roles_empresa USING btree (id_usuario);


--
-- Name: uix_ure_un_principal; Type: INDEX; Schema: core; Owner: postgres
--

CREATE UNIQUE INDEX uix_ure_un_principal ON core.usuarios_roles_empresa USING btree (id_empresa, id_usuario) WHERE (orden_rol = 1);


--
-- Name: idx_af_det_autofactura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_af_det_autofactura ON facturacion.autofactura_detalle USING btree (id_autofactura);


--
-- Name: idx_aperturas_caja_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_aperturas_caja_empresa ON facturacion.aperturas_caja USING btree (id_empresa, fec_apertura DESC);


--
-- Name: idx_arqueos_apertura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_arqueos_apertura ON facturacion.arqueos_caja USING btree (id_apertura_caja);


--
-- Name: idx_autofacturas_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_autofacturas_empresa ON facturacion.autofacturas USING btree (id_empresa, fec_emision DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_cajas_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cajas_empresa ON facturacion.cajas USING btree (id_empresa);


--
-- Name: idx_cc_empresa_estado; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cc_empresa_estado ON facturacion.cuentas_cobrar USING btree (id_empresa, cod_estado, fec_vencimiento);


--
-- Name: idx_cc_entidad; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cc_entidad ON facturacion.cuentas_cobrar USING btree (id_entidad_pagadora) WHERE (id_entidad_pagadora IS NOT NULL);


--
-- Name: idx_cc_paciente; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cc_paciente ON facturacion.cuentas_cobrar USING btree (id_paciente) WHERE (id_paciente IS NOT NULL);


--
-- Name: idx_cc_vencidas; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cc_vencidas ON facturacion.cuentas_cobrar USING btree (id_empresa, fec_vencimiento) WHERE ((cod_estado = ANY (ARRAY['PENDIENTE'::text, 'PARCIAL'::text])) AND (fec_eliminacion IS NULL));


--
-- Name: idx_cheques_empresa_estado; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cheques_empresa_estado ON facturacion.cheques_recibidos USING btree (id_empresa, cod_estado);


--
-- Name: idx_cob_det_cobranza; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cob_det_cobranza ON facturacion.cobranza_detalle USING btree (id_cobranza);


--
-- Name: idx_cobranzas_apertura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cobranzas_apertura ON facturacion.cobranzas USING btree (id_apertura_caja);


--
-- Name: idx_cobranzas_caja_apertura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cobranzas_caja_apertura ON facturacion.cobranzas USING btree (id_caja, id_apertura_caja) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_cobranzas_cuenta; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cobranzas_cuenta ON facturacion.cobranzas USING btree (id_cuenta_cobrar) WHERE (id_cuenta_cobrar IS NOT NULL);


--
-- Name: idx_cobranzas_empresa_fec; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cobranzas_empresa_fec ON facturacion.cobranzas USING btree (id_empresa, fec_cobranza DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_cuotas_cuenta; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cuotas_cuenta ON facturacion.cuotas_cobrar USING btree (id_cuenta_cobrar);


--
-- Name: idx_cuotas_vencimiento; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_cuotas_vencimiento ON facturacion.cuotas_cobrar USING btree (id_empresa, fec_vencimiento) WHERE (cod_estado = ANY (ARRAY['PENDIENTE'::text, 'PARCIAL'::text]));


--
-- Name: idx_de_cola_envio; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_de_cola_envio ON facturacion.documentos_electronicos USING btree (id_empresa, fec_emision) WHERE ((cod_estado = ANY (ARRAY['FIRMADO'::text, 'ENCOLADO'::text])) AND (fec_eliminacion IS NULL));


--
-- Name: idx_de_empresa_estado; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_de_empresa_estado ON facturacion.documentos_electronicos USING btree (id_empresa, cod_estado);


--
-- Name: idx_de_empresa_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_de_empresa_fecha ON facturacion.documentos_electronicos USING btree (id_empresa, fec_emision DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_entidades_pag_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_entidades_pag_empresa ON facturacion.entidades_pagadoras USING btree (id_empresa);


--
-- Name: idx_eventos_de; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_eventos_de ON facturacion.sifen_eventos USING btree (id_de) WHERE (id_de IS NOT NULL);


--
-- Name: idx_eventos_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_eventos_empresa ON facturacion.sifen_eventos USING btree (id_empresa, cod_estado);


--
-- Name: idx_factura_det_factura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_factura_det_factura ON facturacion.factura_detalle USING btree (id_factura);


--
-- Name: idx_factura_mp_factura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_factura_mp_factura ON facturacion.factura_medios_pago USING btree (id_factura);


--
-- Name: idx_facturas_de; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_facturas_de ON facturacion.facturas USING btree (id_de) WHERE (id_de IS NOT NULL);


--
-- Name: idx_facturas_empresa_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_facturas_empresa_fecha ON facturacion.facturas USING btree (id_empresa, fec_emision DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_facturas_estado; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_facturas_estado ON facturacion.facturas USING btree (cod_estado) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_facturas_estado_emp; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_facturas_estado_emp ON facturacion.facturas USING btree (id_empresa, cod_estado) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_facturas_paciente; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_facturas_paciente ON facturacion.facturas USING btree (id_paciente) WHERE (id_paciente IS NOT NULL);


--
-- Name: idx_items_categoria; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_items_categoria ON facturacion.items USING btree (id_categoria_item) WHERE (id_categoria_item IS NOT NULL);


--
-- Name: idx_items_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_items_empresa ON facturacion.items USING btree (id_empresa, est_item) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_libro_ventas_de; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_libro_ventas_de ON facturacion.libro_ventas USING btree (id_de);


--
-- Name: idx_libro_ventas_empresa_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_libro_ventas_empresa_fecha ON facturacion.libro_ventas USING btree (id_empresa, fec_emision);


--
-- Name: idx_libro_ventas_periodo; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_libro_ventas_periodo ON facturacion.libro_ventas USING btree (id_empresa, fec_emision, cod_estado);


--
-- Name: idx_lote_docs_de; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_lote_docs_de ON facturacion.sifen_lote_documentos USING btree (id_de);


--
-- Name: idx_lote_docs_lote; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_lote_docs_lote ON facturacion.sifen_lote_documentos USING btree (id_lote);


--
-- Name: idx_lotes_empresa_estado; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_lotes_empresa_estado ON facturacion.sifen_lotes USING btree (id_empresa, cod_estado);


--
-- Name: idx_mov_caja_apertura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_mov_caja_apertura ON facturacion.movimientos_caja USING btree (id_apertura_caja);


--
-- Name: idx_mov_caja_apertura_sentido; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_mov_caja_apertura_sentido ON facturacion.movimientos_caja USING btree (id_apertura_caja, cod_sentido) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_mov_caja_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_mov_caja_fecha ON facturacion.movimientos_caja USING btree (id_empresa, fec_creacion DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_nc_det_nc; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nc_det_nc ON facturacion.nota_credito_detalle USING btree (id_nota_credito);


--
-- Name: idx_nc_empresa_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nc_empresa_fecha ON facturacion.notas_credito USING btree (id_empresa, fec_emision DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_nc_factura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nc_factura ON facturacion.notas_credito USING btree (id_factura);


--
-- Name: idx_nd_det_nd; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nd_det_nd ON facturacion.nota_debito_detalle USING btree (id_nota_debito);


--
-- Name: idx_nd_empresa_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nd_empresa_fecha ON facturacion.notas_debito USING btree (id_empresa, fec_emision DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_nd_factura; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nd_factura ON facturacion.notas_debito USING btree (id_factura);


--
-- Name: idx_nr_det_nr; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nr_det_nr ON facturacion.nota_remision_detalle USING btree (id_nota_remision);


--
-- Name: idx_nr_empresa_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_nr_empresa_fecha ON facturacion.notas_remision USING btree (id_empresa, fec_emision DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_rec_det_recaudacion; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_rec_det_recaudacion ON facturacion.recaudacion_detalle USING btree (id_recaudacion);


--
-- Name: idx_recaudaciones_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_recaudaciones_empresa ON facturacion.recaudaciones USING btree (id_empresa, fec_recaudacion DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_secuencias_timbrado; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_secuencias_timbrado ON facturacion.secuencias_numeracion USING btree (id_empresa, id_timbrado);


--
-- Name: idx_tarifario_item; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_tarifario_item ON facturacion.tarifario_precios USING btree (id_item, fec_vigencia_desde DESC) WHERE (fec_eliminacion IS NULL);


--
-- Name: idx_timbrado_hab_timbrado; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_timbrado_hab_timbrado ON facturacion.timbrado_habilitaciones USING btree (id_timbrado);


--
-- Name: idx_timbrados_empresa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_timbrados_empresa ON facturacion.timbrados USING btree (id_empresa, cod_estado);


--
-- Name: idx_trans_log_de; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_trans_log_de ON facturacion.sifen_transmision_log USING btree (id_de) WHERE (id_de IS NOT NULL);


--
-- Name: idx_trans_log_fecha; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_trans_log_fecha ON facturacion.sifen_transmision_log USING btree (id_empresa, fec_creacion DESC);


--
-- Name: idx_trans_log_lote; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE INDEX idx_trans_log_lote ON facturacion.sifen_transmision_log USING btree (id_lote) WHERE (id_lote IS NOT NULL);


--
-- Name: uq_apertura_activa; Type: INDEX; Schema: facturacion; Owner: postgres
--

CREATE UNIQUE INDEX uq_apertura_activa ON facturacion.aperturas_caja USING btree (id_caja) WHERE ((cod_estado = 'ABIERTA'::text) AND (fec_eliminacion IS NULL));


--
-- Name: auditoria_sistema_y2026_detalle_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_detalle ATTACH PARTITION core.auditoria_sistema_y2026_detalle_idx;


--
-- Name: auditoria_sistema_y2026_id_empresa_fec_evento_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_empresa_fecha ATTACH PARTITION core.auditoria_sistema_y2026_id_empresa_fec_evento_idx;


--
-- Name: auditoria_sistema_y2026_id_usuario_fec_evento_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_usuario_fecha ATTACH PARTITION core.auditoria_sistema_y2026_id_usuario_fec_evento_idx;


--
-- Name: auditoria_sistema_y2026_pkey; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.auditoria_sistema_pkey ATTACH PARTITION core.auditoria_sistema_y2026_pkey;


--
-- Name: auditoria_sistema_y2027_detalle_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_detalle ATTACH PARTITION core.auditoria_sistema_y2027_detalle_idx;


--
-- Name: auditoria_sistema_y2027_id_empresa_fec_evento_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_empresa_fecha ATTACH PARTITION core.auditoria_sistema_y2027_id_empresa_fec_evento_idx;


--
-- Name: auditoria_sistema_y2027_id_usuario_fec_evento_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_usuario_fecha ATTACH PARTITION core.auditoria_sistema_y2027_id_usuario_fec_evento_idx;


--
-- Name: auditoria_sistema_y2027_pkey; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.auditoria_sistema_pkey ATTACH PARTITION core.auditoria_sistema_y2027_pkey;


--
-- Name: auditoria_sistema_y2028_detalle_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_detalle ATTACH PARTITION core.auditoria_sistema_y2028_detalle_idx;


--
-- Name: auditoria_sistema_y2028_id_empresa_fec_evento_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_empresa_fecha ATTACH PARTITION core.auditoria_sistema_y2028_id_empresa_fec_evento_idx;


--
-- Name: auditoria_sistema_y2028_id_usuario_fec_evento_idx; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.idx_auditoria_usuario_fecha ATTACH PARTITION core.auditoria_sistema_y2028_id_usuario_fec_evento_idx;


--
-- Name: auditoria_sistema_y2028_pkey; Type: INDEX ATTACH; Schema: core; Owner: postgres
--

ALTER INDEX core.auditoria_sistema_pkey ATTACH PARTITION core.auditoria_sistema_y2028_pkey;


--
-- Name: acuerdos_terapeuticos trg_acuerdos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_acuerdos_fec_mod BEFORE UPDATE ON consultorio.acuerdos_terapeuticos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: contratos_tratamiento_acuerdos_pago trg_acuerdos_pago_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_acuerdos_pago_fec_mod BEFORE UPDATE ON consultorio.contratos_tratamiento_acuerdos_pago FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: anamnesis trg_anamnesis_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_anamnesis_fec_mod BEFORE UPDATE ON consultorio.anamnesis FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: antecedentes_paciente trg_ant_paciente_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_ant_paciente_fec_mod BEFORE UPDATE ON consultorio.antecedentes_paciente FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: antecedentes_paciente trg_antecedentes_paciente_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_antecedentes_paciente_fec_mod BEFORE UPDATE ON consultorio.antecedentes_paciente FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: consentimientos_firmados trg_consentimientos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_consentimientos_fec_mod BEFORE UPDATE ON consultorio.consentimientos_firmados FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: contratos_tratamiento trg_contratos_trat_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_contratos_trat_fec_mod BEFORE UPDATE ON consultorio.contratos_tratamiento FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: derivaciones trg_derivaciones_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_derivaciones_fec_mod BEFORE UPDATE ON consultorio.derivaciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: diagnosticos_cie10 trg_diagnosticos_cie10_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_diagnosticos_cie10_fec_mod BEFORE UPDATE ON consultorio.diagnosticos_cie10 FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: diagnosticos_dsm5 trg_diagnosticos_dsm5_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_diagnosticos_dsm5_fec_mod BEFORE UPDATE ON consultorio.diagnosticos_dsm5 FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: documentos_adjuntos trg_documentos_adj_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_documentos_adj_fec_mod BEFORE UPDATE ON consultorio.documentos_adjuntos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: empresa_perfil_clinico trg_empresa_perfil_clinico_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_empresa_perfil_clinico_fec_mod BEFORE UPDATE ON consultorio.empresa_perfil_clinico FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: episodio_procedimientos_insumos trg_ep_insumos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_ep_insumos_fec_mod BEFORE UPDATE ON consultorio.episodio_procedimientos_insumos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: episodio_procedimientos trg_ep_procedimientos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_ep_procedimientos_fec_mod BEFORE UPDATE ON consultorio.episodio_procedimientos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: episodio_diagnosticos trg_episodio_diag_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_episodio_diag_fec_mod BEFORE UPDATE ON consultorio.episodio_diagnosticos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: episodios trg_episodios_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_episodios_fec_mod BEFORE UPDATE ON consultorio.episodios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: diagnosticos_cie10_dsm5_equivalencias trg_equivalencias_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_equivalencias_fec_mod BEFORE UPDATE ON consultorio.diagnosticos_cie10_dsm5_equivalencias FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: fichas_clinicas trg_fichas_clinicas_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_fichas_clinicas_fec_mod BEFORE UPDATE ON consultorio.fichas_clinicas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: fichas_psicologia trg_fichas_psicologia_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_fichas_psicologia_fec_mod BEFORE UPDATE ON consultorio.fichas_psicologia FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: formularios_definicion trg_formulario_def_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_formulario_def_fec_mod BEFORE UPDATE ON consultorio.formularios_definicion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: indicaciones_no_farmacologicas trg_indicaciones_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_indicaciones_fec_mod BEFORE UPDATE ON consultorio.indicaciones_no_farmacologicas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: insumos_empresa trg_insumo_empresa_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_insumo_empresa_fec_mod BEFORE UPDATE ON consultorio.insumos_empresa FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: justificativos trg_justificativos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_justificativos_fec_mod BEFORE UPDATE ON consultorio.justificativos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: medicamentos_empresa trg_med_empresa_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_med_empresa_fec_mod BEFORE UPDATE ON consultorio.medicamentos_empresa FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: contratos_tratamiento_modalidades_pago trg_modalidades_pago_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_modalidades_pago_fec_mod BEFORE UPDATE ON consultorio.contratos_tratamiento_modalidades_pago FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: notas_evolucion trg_notas_evol_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_notas_evol_fec_mod BEFORE UPDATE ON consultorio.notas_evolucion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: ordenes_analisis_detalle trg_ord_ana_det_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_ord_ana_det_fec_mod BEFORE UPDATE ON consultorio.ordenes_analisis_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: ordenes_estudios_detalle trg_ord_est_det_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_ord_est_det_fec_mod BEFORE UPDATE ON consultorio.ordenes_estudios_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: ordenes_analisis trg_ordenes_ana_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_ordenes_ana_fec_mod BEFORE UPDATE ON consultorio.ordenes_analisis FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: ordenes_estudios trg_ordenes_est_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_ordenes_est_fec_mod BEFORE UPDATE ON consultorio.ordenes_estudios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: paciente_tokens trg_paciente_tokens_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_paciente_tokens_fec_mod BEFORE UPDATE ON consultorio.paciente_tokens FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_sesion_actividades trg_pei_actividades_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_actividades_fec_mod BEFORE UPDATE ON consultorio.pei_sesion_actividades FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_calendario_eventos trg_pei_calendario_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_calendario_fec_mod BEFORE UPDATE ON consultorio.pei_calendario_eventos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_estrategias trg_pei_estrategias_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_estrategias_fec_mod BEFORE UPDATE ON consultorio.pei_estrategias FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei trg_pei_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_fec_mod BEFORE UPDATE ON consultorio.pei FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_habilidades_entrenamiento trg_pei_habilidades_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_habilidades_fec_mod BEFORE UPDATE ON consultorio.pei_habilidades_entrenamiento FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_objetivos trg_pei_objetivos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_objetivos_fec_mod BEFORE UPDATE ON consultorio.pei_objetivos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_reunion_recomendaciones trg_pei_recomendaciones_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_recomendaciones_fec_mod BEFORE UPDATE ON consultorio.pei_reunion_recomendaciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_registro_mensual trg_pei_registro_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_registro_fec_mod BEFORE UPDATE ON consultorio.pei_registro_mensual FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_reunion_clinica trg_pei_reunion_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_reunion_fec_mod BEFORE UPDATE ON consultorio.pei_reunion_clinica FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pei_sesion_planificada trg_pei_sesion_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pei_sesion_fec_mod BEFORE UPDATE ON consultorio.pei_sesion_planificada FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: planes_tratamiento trg_planes_trat_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_planes_trat_fec_mod BEFORE UPDATE ON consultorio.planes_tratamiento FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: plantillas_justificativos trg_plantilla_just_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_plantilla_just_fec_mod BEFORE UPDATE ON consultorio.plantillas_justificativos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: procedimientos_empresa trg_proc_empresa_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_proc_empresa_fec_mod BEFORE UPDATE ON consultorio.procedimientos_empresa FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: psicologia_perfil_empresa trg_psicologia_perfil_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_psicologia_perfil_fec_mod BEFORE UPDATE ON consultorio.psicologia_perfil_empresa FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: planes_tratamiento_items trg_pti_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_pti_fec_mod BEFORE UPDATE ON consultorio.planes_tratamiento_items FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: resultados_analisis_detalle trg_rad_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_rad_fec_mod BEFORE UPDATE ON consultorio.resultados_analisis_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: recetas_detalle trg_recetas_det_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_recetas_det_fec_mod BEFORE UPDATE ON consultorio.recetas_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: recetas trg_recetas_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_recetas_fec_mod BEFORE UPDATE ON consultorio.recetas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: resultados_analisis trg_resultados_ana_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_resultados_ana_fec_mod BEFORE UPDATE ON consultorio.resultados_analisis FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: contratos_tratamiento_sesiones trg_sesiones_trat_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_sesiones_trat_fec_mod BEFORE UPDATE ON consultorio.contratos_tratamiento_sesiones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: signos_vitales trg_signos_vitales_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_signos_vitales_fec_mod BEFORE UPDATE ON consultorio.signos_vitales FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: signos_vitales_detalle trg_svd_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_svd_fec_mod BEFORE UPDATE ON consultorio.signos_vitales_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tipos_justificativos trg_tipos_justificativos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_tipos_justificativos_fec_mod BEFORE UPDATE ON consultorio.tipos_justificativos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tipos_procedimientos trg_tipos_procedimientos_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_tipos_procedimientos_fec_mod BEFORE UPDATE ON consultorio.tipos_procedimientos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tipos_signos_vitales trg_tipos_signos_vitales_fec_mod; Type: TRIGGER; Schema: consultorio; Owner: postgres
--

CREATE TRIGGER trg_tipos_signos_vitales_fec_mod BEFORE UPDATE ON consultorio.tipos_signos_vitales FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: agenda_horarios_excepciones trg_agenda_horarios_excepciones_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_agenda_horarios_excepciones_fec_mod BEFORE UPDATE ON core.agenda_horarios_excepciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: agenda_horarios trg_agenda_horarios_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_agenda_horarios_fec_mod BEFORE UPDATE ON core.agenda_horarios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: cargos trg_cargos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_cargos_fec_mod BEFORE UPDATE ON core.cargos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: citas trg_citas_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_citas_fec_mod BEFORE UPDATE ON core.citas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: citas_log_estados trg_citas_log_estados_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_citas_log_estados_fec_mod BEFORE UPDATE ON core.citas_log_estados FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: ciudades trg_ciudades_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_ciudades_fec_mod BEFORE UPDATE ON core.ciudades FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: condiciones_venta trg_condiciones_venta_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_condiciones_venta_fec_mod BEFORE UPDATE ON core.condiciones_venta FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: consultorios trg_consultorios_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_consultorios_fec_mod BEFORE UPDATE ON core.consultorios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: departamentos trg_departamentos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_departamentos_fec_mod BEFORE UPDATE ON core.departamentos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: dias_semana trg_dias_semana_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_dias_semana_fec_mod BEFORE UPDATE ON core.dias_semana FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: empresa_certificados trg_empresa_certificados_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_empresa_certificados_fec_mod BEFORE UPDATE ON core.empresa_certificados FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: empresa_configuracion trg_empresa_configuracion_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_empresa_configuracion_fec_mod BEFORE UPDATE ON core.empresa_configuracion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: empresa_modulos trg_empresa_modulos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_empresa_modulos_fec_mod BEFORE UPDATE ON core.empresa_modulos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: empresas trg_empresas_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_empresas_fec_mod BEFORE UPDATE ON core.empresas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: especialidades trg_especialidades_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_especialidades_fec_mod BEFORE UPDATE ON core.especialidades FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: especialista_especialidades trg_especialista_especialidades_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_especialista_especialidades_fec_mod BEFORE UPDATE ON core.especialista_especialidades FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: especialistas trg_especialistas_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_especialistas_fec_mod BEFORE UPDATE ON core.especialistas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: establecimientos trg_establecimientos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_establecimientos_fec_mod BEFORE UPDATE ON core.establecimientos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: estados_citas trg_estados_citas_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_estados_citas_fec_mod BEFORE UPDATE ON core.estados_citas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: estados_civiles trg_estados_civiles_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_estados_civiles_fec_mod BEFORE UPDATE ON core.estados_civiles FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: estados_factura trg_estados_factura_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_estados_factura_fec_mod BEFORE UPDATE ON core.estados_factura FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: feriados trg_feriados_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_feriados_fec_mod BEFORE UPDATE ON core.feriados FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: formas_cobro trg_formas_cobro_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_formas_cobro_fec_mod BEFORE UPDATE ON core.formas_cobro FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: frecuencias_agendamiento trg_frecuencias_agendamiento_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_frecuencias_agendamiento_fec_mod BEFORE UPDATE ON core.frecuencias_agendamiento FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: funcionarios trg_funcionarios_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_funcionarios_fec_mod BEFORE UPDATE ON core.funcionarios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: generos trg_generos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_generos_fec_mod BEFORE UPDATE ON core.generos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: historial_suscripciones trg_historial_suscripciones_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_historial_suscripciones_fec_mod BEFORE UPDATE ON core.historial_suscripciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: licencias trg_licencias_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_licencias_fec_mod BEFORE UPDATE ON core.licencias FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: lista_espera trg_lista_espera_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_lista_espera_fec_mod BEFORE UPDATE ON core.lista_espera FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: login_attempts trg_login_attempts_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_login_attempts_fec_mod BEFORE UPDATE ON core.login_attempts FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: marcas_tarjeta trg_marcas_tarjeta_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_marcas_tarjeta_fec_mod BEFORE UPDATE ON core.marcas_tarjeta FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: metricas_diarias trg_metricas_diarias_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_metricas_diarias_fec_mod BEFORE UPDATE ON core.metricas_diarias FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: modulos trg_modulos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_modulos_fec_mod BEFORE UPDATE ON core.modulos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: monedas trg_monedas_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_monedas_fec_mod BEFORE UPDATE ON core.monedas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: niveles_instruccion trg_niveles_instruccion_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_niveles_instruccion_fec_mod BEFORE UPDATE ON core.niveles_instruccion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: notificaciones_cola trg_notificaciones_cola_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_notificaciones_cola_fec_mod BEFORE UPDATE ON core.notificaciones_cola FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: notificaciones_config trg_notificaciones_config_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_notificaciones_config_fec_mod BEFORE UPDATE ON core.notificaciones_config FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: notificaciones_plantillas trg_notificaciones_plantillas_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_notificaciones_plantillas_fec_mod BEFORE UPDATE ON core.notificaciones_plantillas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: paciente_profesional trg_paciente_profesional_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_paciente_profesional_fec_mod BEFORE UPDATE ON core.paciente_profesional FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pacientes trg_pacientes_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_pacientes_fec_mod BEFORE UPDATE ON core.pacientes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: pacientes_menores trg_pacientes_menores_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_pacientes_menores_fec_mod BEFORE UPDATE ON core.pacientes_menores FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: paises trg_paises_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_paises_fec_mod BEFORE UPDATE ON core.paises FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: password_history trg_password_history_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_password_history_fec_mod BEFORE UPDATE ON core.password_history FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: password_reset_tokens trg_password_reset_tokens_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_password_reset_tokens_fec_mod BEFORE UPDATE ON core.password_reset_tokens FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: permisos trg_permisos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_permisos_fec_mod BEFORE UPDATE ON core.permisos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: personas trg_personas_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_personas_fec_mod BEFORE UPDATE ON core.personas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: plan_modulos trg_plan_modulos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_plan_modulos_fec_mod BEFORE UPDATE ON core.plan_modulos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: planes trg_planes_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_planes_fec_mod BEFORE UPDATE ON core.planes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: preferencias_ui trg_preferencias_ui_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_preferencias_ui_fec_mod BEFORE UPDATE ON core.preferencias_ui FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: profesiones trg_profesiones_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_profesiones_fec_mod BEFORE UPDATE ON core.profesiones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: puntos_expedicion trg_puntos_expedicion_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_puntos_expedicion_fec_mod BEFORE UPDATE ON core.puntos_expedicion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: recordatorios trg_recordatorios_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_recordatorios_fec_mod BEFORE UPDATE ON core.recordatorios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: reportes_jobs trg_reportes_jobs_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_reportes_jobs_fec_mod BEFORE UPDATE ON core.reportes_jobs FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: roles_base trg_roles_base_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_roles_base_fec_mod BEFORE UPDATE ON core.roles_base FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: roles_empresa trg_roles_empresa_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_roles_empresa_fec_mod BEFORE UPDATE ON core.roles_empresa FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: roles_empresa_permisos trg_roles_empresa_permisos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_roles_empresa_permisos_fec_mod BEFORE UPDATE ON core.roles_empresa_permisos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: sedes trg_sedes_check_limite; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_sedes_check_limite BEFORE INSERT ON core.sedes FOR EACH ROW EXECUTE FUNCTION core.fn_check_limite_sedes();


--
-- Name: sedes trg_sedes_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_sedes_fec_mod BEFORE UPDATE ON core.sedes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: sesiones trg_sesiones_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_sesiones_fec_mod BEFORE UPDATE ON core.sesiones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: slots_agenda trg_slots_agenda_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_slots_agenda_fec_mod BEFORE UPDATE ON core.slots_agenda FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: suscripcion_excedentes trg_suscripcion_excedentes_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_suscripcion_excedentes_fec_mod BEFORE UPDATE ON core.suscripcion_excedentes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: suscripciones trg_suscripciones_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_suscripciones_fec_mod BEFORE UPDATE ON core.suscripciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tipos_comprobantes trg_tipos_comprobantes_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_tipos_comprobantes_fec_mod BEFORE UPDATE ON core.tipos_comprobantes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tipos_documentos_identidad trg_tipos_documentos_identidad_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_tipos_documentos_identidad_fec_mod BEFORE UPDATE ON core.tipos_documentos_identidad FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tipos_impuestos trg_tipos_impuestos_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_tipos_impuestos_fec_mod BEFORE UPDATE ON core.tipos_impuestos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tipos_items trg_tipos_items_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_tipos_items_fec_mod BEFORE UPDATE ON core.tipos_items FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: usuarios trg_usuarios_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_usuarios_fec_mod BEFORE UPDATE ON core.usuarios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: usuarios_roles_base trg_usuarios_roles_base_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_usuarios_roles_base_fec_mod BEFORE UPDATE ON core.usuarios_roles_base FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: usuarios_roles_empresa trg_usuarios_roles_empresa_fec_mod; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_usuarios_roles_empresa_fec_mod BEFORE UPDATE ON core.usuarios_roles_empresa FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: autofactura_detalle trg_af_det_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_af_det_fec_mod BEFORE UPDATE ON facturacion.autofactura_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: aperturas_caja trg_aperturas_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_aperturas_fec_mod BEFORE UPDATE ON facturacion.aperturas_caja FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: arqueos_caja trg_arqueos_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_arqueos_fec_mod BEFORE UPDATE ON facturacion.arqueos_caja FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: autofacturas trg_autofacturas_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_autofacturas_fec_mod BEFORE UPDATE ON facturacion.autofacturas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: cajas trg_cajas_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_cajas_fec_mod BEFORE UPDATE ON facturacion.cajas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: categorias_items trg_categorias_items_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_categorias_items_fec_mod BEFORE UPDATE ON facturacion.categorias_items FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: cuentas_cobrar trg_cc_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_cc_fec_mod BEFORE UPDATE ON facturacion.cuentas_cobrar FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: cheques_recibidos trg_cheques_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_cheques_fec_mod BEFORE UPDATE ON facturacion.cheques_recibidos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: cobranza_detalle trg_cob_det_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_cob_det_fec_mod BEFORE UPDATE ON facturacion.cobranza_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: cobranzas trg_cobranzas_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_cobranzas_fec_mod BEFORE UPDATE ON facturacion.cobranzas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: cuotas_cobrar trg_cuotas_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_cuotas_fec_mod BEFORE UPDATE ON facturacion.cuotas_cobrar FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: documentos_electronicos trg_de_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_de_fec_mod BEFORE UPDATE ON facturacion.documentos_electronicos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: entidades_pagadoras trg_entidades_pag_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_entidades_pag_fec_mod BEFORE UPDATE ON facturacion.entidades_pagadoras FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: sifen_eventos trg_eventos_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_eventos_fec_mod BEFORE UPDATE ON facturacion.sifen_eventos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: factura_detalle trg_factura_det_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_factura_det_fec_mod BEFORE UPDATE ON facturacion.factura_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: factura_medios_pago trg_factura_mp_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_factura_mp_fec_mod BEFORE UPDATE ON facturacion.factura_medios_pago FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: facturas trg_facturas_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_facturas_fec_mod BEFORE UPDATE ON facturacion.facturas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: items trg_items_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_items_fec_mod BEFORE UPDATE ON facturacion.items FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: libro_ventas trg_libro_ventas_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_libro_ventas_fec_mod BEFORE UPDATE ON facturacion.libro_ventas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: sifen_lote_documentos trg_lote_docs_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_lote_docs_fec_mod BEFORE UPDATE ON facturacion.sifen_lote_documentos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: sifen_lotes trg_lotes_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_lotes_fec_mod BEFORE UPDATE ON facturacion.sifen_lotes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: movimientos_caja trg_mov_caja_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_mov_caja_fec_mod BEFORE UPDATE ON facturacion.movimientos_caja FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: nota_credito_detalle trg_nc_det_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_nc_det_fec_mod BEFORE UPDATE ON facturacion.nota_credito_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: notas_credito trg_nc_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_nc_fec_mod BEFORE UPDATE ON facturacion.notas_credito FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: nota_debito_detalle trg_nd_det_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_nd_det_fec_mod BEFORE UPDATE ON facturacion.nota_debito_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: notas_debito trg_nd_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_nd_fec_mod BEFORE UPDATE ON facturacion.notas_debito FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: nota_remision_detalle trg_nr_det_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_nr_det_fec_mod BEFORE UPDATE ON facturacion.nota_remision_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: notas_remision trg_nr_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_nr_fec_mod BEFORE UPDATE ON facturacion.notas_remision FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: recaudacion_detalle trg_rec_det_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_rec_det_fec_mod BEFORE UPDATE ON facturacion.recaudacion_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: recaudaciones trg_recaudaciones_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_recaudaciones_fec_mod BEFORE UPDATE ON facturacion.recaudaciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: secuencias_numeracion trg_secuencias_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_secuencias_fec_mod BEFORE UPDATE ON facturacion.secuencias_numeracion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: sifen_config trg_sifen_config_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_sifen_config_fec_mod BEFORE UPDATE ON facturacion.sifen_config FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: tarifario_precios trg_tarifario_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_tarifario_fec_mod BEFORE UPDATE ON facturacion.tarifario_precios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: timbrado_habilitaciones trg_timbrado_hab_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_timbrado_hab_fec_mod BEFORE UPDATE ON facturacion.timbrado_habilitaciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: timbrados trg_timbrados_fec_mod; Type: TRIGGER; Schema: facturacion; Owner: postgres
--

CREATE TRIGGER trg_timbrados_fec_mod BEFORE UPDATE ON facturacion.timbrados FOR EACH ROW EXECUTE FUNCTION public.fn_set_fec_modificacion();


--
-- Name: acuerdo_monto_historial acuerdo_monto_historial_id_acuerdo_terapeutico_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdo_monto_historial
    ADD CONSTRAINT acuerdo_monto_historial_id_acuerdo_terapeutico_fkey FOREIGN KEY (id_acuerdo_terapeutico) REFERENCES consultorio.acuerdos_terapeuticos(id_acuerdo_terapeutico);


--
-- Name: acuerdo_monto_historial acuerdo_monto_historial_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdo_monto_historial
    ADD CONSTRAINT acuerdo_monto_historial_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: acuerdos_terapeuticos acuerdos_terapeuticos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdos_terapeuticos
    ADD CONSTRAINT acuerdos_terapeuticos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: acuerdos_terapeuticos acuerdos_terapeuticos_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdos_terapeuticos
    ADD CONSTRAINT acuerdos_terapeuticos_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: acuerdos_terapeuticos acuerdos_terapeuticos_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.acuerdos_terapeuticos
    ADD CONSTRAINT acuerdos_terapeuticos_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: anamnesis_adulto_ext anamnesis_adulto_ext_id_anamnesis_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_adulto_ext
    ADD CONSTRAINT anamnesis_adulto_ext_id_anamnesis_fkey FOREIGN KEY (id_anamnesis) REFERENCES consultorio.anamnesis(id_anamnesis);


--
-- Name: anamnesis_adulto_ext anamnesis_adulto_ext_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_adulto_ext
    ADD CONSTRAINT anamnesis_adulto_ext_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: anamnesis anamnesis_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis
    ADD CONSTRAINT anamnesis_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: anamnesis anamnesis_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis
    ADD CONSTRAINT anamnesis_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: anamnesis anamnesis_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis
    ADD CONSTRAINT anamnesis_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: anamnesis_infantil_ext anamnesis_infantil_ext_id_anamnesis_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_infantil_ext
    ADD CONSTRAINT anamnesis_infantil_ext_id_anamnesis_fkey FOREIGN KEY (id_anamnesis) REFERENCES consultorio.anamnesis(id_anamnesis);


--
-- Name: anamnesis_infantil_ext anamnesis_infantil_ext_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.anamnesis_infantil_ext
    ADD CONSTRAINT anamnesis_infantil_ext_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: antecedentes_paciente antecedentes_paciente_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.antecedentes_paciente
    ADD CONSTRAINT antecedentes_paciente_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: antecedentes_paciente antecedentes_paciente_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.antecedentes_paciente
    ADD CONSTRAINT antecedentes_paciente_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: cobros_simples cobros_simples_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.cobros_simples
    ADD CONSTRAINT cobros_simples_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: cobros_simples cobros_simples_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.cobros_simples
    ADD CONSTRAINT cobros_simples_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: consentimientos_firmados consentimientos_firmados_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.consentimientos_firmados
    ADD CONSTRAINT consentimientos_firmados_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: consentimientos_firmados consentimientos_firmados_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.consentimientos_firmados
    ADD CONSTRAINT consentimientos_firmados_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: consentimientos_firmados consentimientos_firmados_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.consentimientos_firmados
    ADD CONSTRAINT consentimientos_firmados_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: contratos_tratamiento_acuerdos_pago contratos_tratamiento_acuerdos_pag_id_contrato_tratamiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_acuerdos_pago
    ADD CONSTRAINT contratos_tratamiento_acuerdos_pag_id_contrato_tratamiento_fkey FOREIGN KEY (id_contrato_tratamiento) REFERENCES consultorio.contratos_tratamiento(id_contrato_tratamiento);


--
-- Name: contratos_tratamiento_acuerdos_pago contratos_tratamiento_acuerdos_pago_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_acuerdos_pago
    ADD CONSTRAINT contratos_tratamiento_acuerdos_pago_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: contratos_tratamiento_acuerdos_pago contratos_tratamiento_acuerdos_pago_id_modalidad_pago_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_acuerdos_pago
    ADD CONSTRAINT contratos_tratamiento_acuerdos_pago_id_modalidad_pago_fkey FOREIGN KEY (id_modalidad_pago) REFERENCES consultorio.contratos_tratamiento_modalidades_pago(id_modalidad_pago);


--
-- Name: contratos_tratamiento contratos_tratamiento_id_contrato_anterior_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento
    ADD CONSTRAINT contratos_tratamiento_id_contrato_anterior_fkey FOREIGN KEY (id_contrato_anterior) REFERENCES consultorio.contratos_tratamiento(id_contrato_tratamiento);


--
-- Name: contratos_tratamiento contratos_tratamiento_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento
    ADD CONSTRAINT contratos_tratamiento_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: contratos_tratamiento contratos_tratamiento_id_episodio_apertura_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento
    ADD CONSTRAINT contratos_tratamiento_id_episodio_apertura_fkey FOREIGN KEY (id_episodio_apertura) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: contratos_tratamiento contratos_tratamiento_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento
    ADD CONSTRAINT contratos_tratamiento_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: contratos_tratamiento contratos_tratamiento_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento
    ADD CONSTRAINT contratos_tratamiento_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: contratos_tratamiento_modalidades_pago contratos_tratamiento_modalidades__id_contrato_tratamiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_modalidades_pago
    ADD CONSTRAINT contratos_tratamiento_modalidades__id_contrato_tratamiento_fkey FOREIGN KEY (id_contrato_tratamiento) REFERENCES consultorio.contratos_tratamiento(id_contrato_tratamiento);


--
-- Name: contratos_tratamiento_modalidades_pago contratos_tratamiento_modalidades_pago_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_modalidades_pago
    ADD CONSTRAINT contratos_tratamiento_modalidades_pago_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: contratos_tratamiento_pagos contratos_tratamiento_pagos_id_acuerdo_pago_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_pagos
    ADD CONSTRAINT contratos_tratamiento_pagos_id_acuerdo_pago_fkey FOREIGN KEY (id_acuerdo_pago) REFERENCES consultorio.contratos_tratamiento_acuerdos_pago(id_acuerdo_pago);


--
-- Name: contratos_tratamiento_pagos contratos_tratamiento_pagos_id_contrato_tratamiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_pagos
    ADD CONSTRAINT contratos_tratamiento_pagos_id_contrato_tratamiento_fkey FOREIGN KEY (id_contrato_tratamiento) REFERENCES consultorio.contratos_tratamiento(id_contrato_tratamiento);


--
-- Name: contratos_tratamiento_pagos contratos_tratamiento_pagos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_pagos
    ADD CONSTRAINT contratos_tratamiento_pagos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: contratos_tratamiento_pagos contratos_tratamiento_pagos_id_factura_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_pagos
    ADD CONSTRAINT contratos_tratamiento_pagos_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesiones_id_cita_anterior_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones
    ADD CONSTRAINT contratos_tratamiento_sesiones_id_cita_anterior_fkey FOREIGN KEY (id_cita_anterior) REFERENCES core.citas(id_cita);


--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesiones_id_cita_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones
    ADD CONSTRAINT contratos_tratamiento_sesiones_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES core.citas(id_cita);


--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesiones_id_contrato_tratamiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones
    ADD CONSTRAINT contratos_tratamiento_sesiones_id_contrato_tratamiento_fkey FOREIGN KEY (id_contrato_tratamiento) REFERENCES consultorio.contratos_tratamiento(id_contrato_tratamiento);


--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesiones_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones
    ADD CONSTRAINT contratos_tratamiento_sesiones_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesiones_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.contratos_tratamiento_sesiones
    ADD CONSTRAINT contratos_tratamiento_sesiones_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: derivaciones derivaciones_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.derivaciones
    ADD CONSTRAINT derivaciones_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: derivaciones derivaciones_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.derivaciones
    ADD CONSTRAINT derivaciones_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: derivaciones derivaciones_id_especialista_destino_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.derivaciones
    ADD CONSTRAINT derivaciones_id_especialista_destino_fkey FOREIGN KEY (id_especialista_destino) REFERENCES core.especialistas(id_especialista);


--
-- Name: derivaciones derivaciones_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.derivaciones
    ADD CONSTRAINT derivaciones_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: derivaciones derivaciones_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.derivaciones
    ADD CONSTRAINT derivaciones_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: diagnosticos_cie10_dsm5_equivalencias diagnosticos_cie10_dsm5_equivalencias_id_diagnostico_cie10_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10_dsm5_equivalencias
    ADD CONSTRAINT diagnosticos_cie10_dsm5_equivalencias_id_diagnostico_cie10_fkey FOREIGN KEY (id_diagnostico_cie10) REFERENCES consultorio.diagnosticos_cie10(id_diagnostico_cie10);


--
-- Name: diagnosticos_cie10_dsm5_equivalencias diagnosticos_cie10_dsm5_equivalencias_id_diagnostico_dsm5_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.diagnosticos_cie10_dsm5_equivalencias
    ADD CONSTRAINT diagnosticos_cie10_dsm5_equivalencias_id_diagnostico_dsm5_fkey FOREIGN KEY (id_diagnostico_dsm5) REFERENCES consultorio.diagnosticos_dsm5(id_diagnostico_dsm5);


--
-- Name: documentos_adjuntos documentos_adjuntos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.documentos_adjuntos
    ADD CONSTRAINT documentos_adjuntos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: empresa_perfil_clinico empresa_perfil_clinico_cod_tipo_clinico_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.empresa_perfil_clinico
    ADD CONSTRAINT empresa_perfil_clinico_cod_tipo_clinico_fkey FOREIGN KEY (cod_tipo_clinico) REFERENCES core.tipos_clinicos(cod_tipo_clinico);


--
-- Name: empresa_perfil_clinico empresa_perfil_clinico_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.empresa_perfil_clinico
    ADD CONSTRAINT empresa_perfil_clinico_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: episodio_diagnosticos episodio_diagnosticos_id_diagnostico_cie10_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_diagnosticos
    ADD CONSTRAINT episodio_diagnosticos_id_diagnostico_cie10_fkey FOREIGN KEY (id_diagnostico_cie10) REFERENCES consultorio.diagnosticos_cie10(id_diagnostico_cie10);


--
-- Name: episodio_diagnosticos episodio_diagnosticos_id_diagnostico_dsm5_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_diagnosticos
    ADD CONSTRAINT episodio_diagnosticos_id_diagnostico_dsm5_fkey FOREIGN KEY (id_diagnostico_dsm5) REFERENCES consultorio.diagnosticos_dsm5(id_diagnostico_dsm5);


--
-- Name: episodio_diagnosticos episodio_diagnosticos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_diagnosticos
    ADD CONSTRAINT episodio_diagnosticos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: episodio_diagnosticos episodio_diagnosticos_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_diagnosticos
    ADD CONSTRAINT episodio_diagnosticos_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: episodio_diagnosticos episodio_diagnosticos_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_diagnosticos
    ADD CONSTRAINT episodio_diagnosticos_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: episodio_procedimientos episodio_procedimientos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos
    ADD CONSTRAINT episodio_procedimientos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: episodio_procedimientos episodio_procedimientos_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos
    ADD CONSTRAINT episodio_procedimientos_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: episodio_procedimientos episodio_procedimientos_id_procedimiento_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos
    ADD CONSTRAINT episodio_procedimientos_id_procedimiento_empresa_fkey FOREIGN KEY (id_procedimiento_empresa) REFERENCES consultorio.procedimientos_empresa(id_procedimiento_empresa);


--
-- Name: episodio_procedimientos_insumos episodio_procedimientos_insumos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos_insumos
    ADD CONSTRAINT episodio_procedimientos_insumos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: episodio_procedimientos_insumos episodio_procedimientos_insumos_id_episodio_procedimiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos_insumos
    ADD CONSTRAINT episodio_procedimientos_insumos_id_episodio_procedimiento_fkey FOREIGN KEY (id_episodio_procedimiento) REFERENCES consultorio.episodio_procedimientos(id_episodio_procedimiento);


--
-- Name: episodio_procedimientos_insumos episodio_procedimientos_insumos_id_insumo_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodio_procedimientos_insumos
    ADD CONSTRAINT episodio_procedimientos_insumos_id_insumo_empresa_fkey FOREIGN KEY (id_insumo_empresa) REFERENCES consultorio.insumos_empresa(id_insumo_empresa);


--
-- Name: episodios episodios_id_cita_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES core.citas(id_cita);


--
-- Name: episodios episodios_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: episodios episodios_id_episodio_origen_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_id_episodio_origen_fkey FOREIGN KEY (id_episodio_origen) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: episodios episodios_id_especialidad_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES core.especialidades(id_especialidad);


--
-- Name: episodios episodios_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: episodios episodios_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.episodios
    ADD CONSTRAINT episodios_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: fichas_clinicas fichas_clinicas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: fichas_clinicas fichas_clinicas_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: fichas_clinicas fichas_clinicas_id_formulario_definicion_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_id_formulario_definicion_fkey FOREIGN KEY (id_formulario_definicion) REFERENCES consultorio.formularios_definicion(id_formulario_definicion);


--
-- Name: fichas_psicologia fichas_psicologia_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_psicologia
    ADD CONSTRAINT fichas_psicologia_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: fichas_psicologia fichas_psicologia_id_ficha_clinica_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.fichas_psicologia
    ADD CONSTRAINT fichas_psicologia_id_ficha_clinica_fkey FOREIGN KEY (id_ficha_clinica) REFERENCES consultorio.fichas_clinicas(id_ficha_clinica);


--
-- Name: formularios_definicion formularios_definicion_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.formularios_definicion
    ADD CONSTRAINT formularios_definicion_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: indicaciones_no_farmacologicas indicaciones_no_farmacologicas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.indicaciones_no_farmacologicas
    ADD CONSTRAINT indicaciones_no_farmacologicas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: indicaciones_no_farmacologicas indicaciones_no_farmacologicas_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.indicaciones_no_farmacologicas
    ADD CONSTRAINT indicaciones_no_farmacologicas_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: insumos_empresa insumos_empresa_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.insumos_empresa
    ADD CONSTRAINT insumos_empresa_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: justificativos justificativos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: justificativos justificativos_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: justificativos justificativos_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: justificativos justificativos_id_justificativo_origen_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_justificativo_origen_fkey FOREIGN KEY (id_justificativo_origen) REFERENCES consultorio.justificativos(id_justificativo);


--
-- Name: justificativos justificativos_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: justificativos justificativos_id_plantilla_justificativo_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_plantilla_justificativo_fkey FOREIGN KEY (id_plantilla_justificativo) REFERENCES consultorio.plantillas_justificativos(id_plantilla_justificativo);


--
-- Name: justificativos justificativos_id_tipo_justificativo_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.justificativos
    ADD CONSTRAINT justificativos_id_tipo_justificativo_fkey FOREIGN KEY (id_tipo_justificativo) REFERENCES consultorio.tipos_justificativos(id_tipo_justificativo);


--
-- Name: medicamentos_empresa medicamentos_empresa_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.medicamentos_empresa
    ADD CONSTRAINT medicamentos_empresa_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: notas_evolucion notas_evolucion_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.notas_evolucion
    ADD CONSTRAINT notas_evolucion_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: notas_evolucion notas_evolucion_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.notas_evolucion
    ADD CONSTRAINT notas_evolucion_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: notas_evolucion notas_evolucion_id_plan_tratamiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.notas_evolucion
    ADD CONSTRAINT notas_evolucion_id_plan_tratamiento_fkey FOREIGN KEY (id_plan_tratamiento) REFERENCES consultorio.planes_tratamiento(id_plan_tratamiento);


--
-- Name: ordenes_analisis_detalle ordenes_analisis_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis_detalle
    ADD CONSTRAINT ordenes_analisis_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: ordenes_analisis_detalle ordenes_analisis_detalle_id_orden_analisis_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis_detalle
    ADD CONSTRAINT ordenes_analisis_detalle_id_orden_analisis_fkey FOREIGN KEY (id_orden_analisis) REFERENCES consultorio.ordenes_analisis(id_orden_analisis);


--
-- Name: ordenes_analisis ordenes_analisis_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis
    ADD CONSTRAINT ordenes_analisis_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: ordenes_analisis ordenes_analisis_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis
    ADD CONSTRAINT ordenes_analisis_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: ordenes_analisis ordenes_analisis_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis
    ADD CONSTRAINT ordenes_analisis_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: ordenes_analisis ordenes_analisis_id_orden_analisis_origen_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis
    ADD CONSTRAINT ordenes_analisis_id_orden_analisis_origen_fkey FOREIGN KEY (id_orden_analisis_origen) REFERENCES consultorio.ordenes_analisis(id_orden_analisis);


--
-- Name: ordenes_analisis ordenes_analisis_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_analisis
    ADD CONSTRAINT ordenes_analisis_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: ordenes_estudios_detalle ordenes_estudios_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios_detalle
    ADD CONSTRAINT ordenes_estudios_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: ordenes_estudios_detalle ordenes_estudios_detalle_id_orden_estudios_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios_detalle
    ADD CONSTRAINT ordenes_estudios_detalle_id_orden_estudios_fkey FOREIGN KEY (id_orden_estudios) REFERENCES consultorio.ordenes_estudios(id_orden_estudios);


--
-- Name: ordenes_estudios ordenes_estudios_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios
    ADD CONSTRAINT ordenes_estudios_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: ordenes_estudios ordenes_estudios_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios
    ADD CONSTRAINT ordenes_estudios_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: ordenes_estudios ordenes_estudios_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios
    ADD CONSTRAINT ordenes_estudios_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: ordenes_estudios ordenes_estudios_id_orden_estudios_origen_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios
    ADD CONSTRAINT ordenes_estudios_id_orden_estudios_origen_fkey FOREIGN KEY (id_orden_estudios_origen) REFERENCES consultorio.ordenes_estudios(id_orden_estudios);


--
-- Name: ordenes_estudios ordenes_estudios_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.ordenes_estudios
    ADD CONSTRAINT ordenes_estudios_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: paciente_tokens paciente_tokens_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.paciente_tokens
    ADD CONSTRAINT paciente_tokens_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: paciente_tokens paciente_tokens_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.paciente_tokens
    ADD CONSTRAINT paciente_tokens_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: pei_calendario_eventos pei_calendario_eventos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_calendario_eventos
    ADD CONSTRAINT pei_calendario_eventos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_calendario_eventos pei_calendario_eventos_id_pei_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_calendario_eventos
    ADD CONSTRAINT pei_calendario_eventos_id_pei_fkey FOREIGN KEY (id_pei) REFERENCES consultorio.pei(id_pei);


--
-- Name: pei_estrategias pei_estrategias_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_estrategias
    ADD CONSTRAINT pei_estrategias_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_estrategias pei_estrategias_id_pei_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_estrategias
    ADD CONSTRAINT pei_estrategias_id_pei_fkey FOREIGN KEY (id_pei) REFERENCES consultorio.pei(id_pei);


--
-- Name: pei_habilidades_entrenamiento pei_habilidades_entrenamiento_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_habilidades_entrenamiento
    ADD CONSTRAINT pei_habilidades_entrenamiento_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_habilidades_entrenamiento pei_habilidades_entrenamiento_id_pei_registro_mensual_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_habilidades_entrenamiento
    ADD CONSTRAINT pei_habilidades_entrenamiento_id_pei_registro_mensual_fkey FOREIGN KEY (id_pei_registro_mensual) REFERENCES consultorio.pei_registro_mensual(id_pei_registro_mensual);


--
-- Name: pei pei_id_cotratante_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei
    ADD CONSTRAINT pei_id_cotratante_fkey FOREIGN KEY (id_cotratante) REFERENCES core.especialistas(id_especialista);


--
-- Name: pei pei_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei
    ADD CONSTRAINT pei_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei pei_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei
    ADD CONSTRAINT pei_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: pei pei_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei
    ADD CONSTRAINT pei_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: pei pei_id_pei_anterior_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei
    ADD CONSTRAINT pei_id_pei_anterior_fkey FOREIGN KEY (id_pei_anterior) REFERENCES consultorio.pei(id_pei);


--
-- Name: pei_objetivos pei_objetivos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_objetivos
    ADD CONSTRAINT pei_objetivos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_objetivos pei_objetivos_id_pei_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_objetivos
    ADD CONSTRAINT pei_objetivos_id_pei_fkey FOREIGN KEY (id_pei) REFERENCES consultorio.pei(id_pei);


--
-- Name: pei_registro_mensual pei_registro_mensual_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_registro_mensual
    ADD CONSTRAINT pei_registro_mensual_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_registro_mensual pei_registro_mensual_id_pei_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_registro_mensual
    ADD CONSTRAINT pei_registro_mensual_id_pei_fkey FOREIGN KEY (id_pei) REFERENCES consultorio.pei(id_pei);


--
-- Name: pei_reunion_clinica pei_reunion_clinica_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_clinica
    ADD CONSTRAINT pei_reunion_clinica_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_reunion_clinica pei_reunion_clinica_id_pei_calendario_evento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_clinica
    ADD CONSTRAINT pei_reunion_clinica_id_pei_calendario_evento_fkey FOREIGN KEY (id_pei_calendario_evento) REFERENCES consultorio.pei_calendario_eventos(id_pei_calendario_evento);


--
-- Name: pei_reunion_clinica pei_reunion_clinica_id_pei_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_clinica
    ADD CONSTRAINT pei_reunion_clinica_id_pei_fkey FOREIGN KEY (id_pei) REFERENCES consultorio.pei(id_pei);


--
-- Name: pei_reunion_participantes pei_reunion_participantes_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_participantes
    ADD CONSTRAINT pei_reunion_participantes_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_reunion_participantes pei_reunion_participantes_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_participantes
    ADD CONSTRAINT pei_reunion_participantes_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: pei_reunion_participantes pei_reunion_participantes_id_pei_reunion_clinica_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_participantes
    ADD CONSTRAINT pei_reunion_participantes_id_pei_reunion_clinica_fkey FOREIGN KEY (id_pei_reunion_clinica) REFERENCES consultorio.pei_reunion_clinica(id_pei_reunion_clinica);


--
-- Name: pei_reunion_recomendaciones pei_reunion_recomendaciones_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_recomendaciones
    ADD CONSTRAINT pei_reunion_recomendaciones_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_reunion_recomendaciones pei_reunion_recomendaciones_id_pei_reunion_clinica_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_reunion_recomendaciones
    ADD CONSTRAINT pei_reunion_recomendaciones_id_pei_reunion_clinica_fkey FOREIGN KEY (id_pei_reunion_clinica) REFERENCES consultorio.pei_reunion_clinica(id_pei_reunion_clinica);


--
-- Name: pei_sesion_actividades pei_sesion_actividades_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_actividades
    ADD CONSTRAINT pei_sesion_actividades_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_sesion_actividades pei_sesion_actividades_id_pei_sesion_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_actividades
    ADD CONSTRAINT pei_sesion_actividades_id_pei_sesion_fkey FOREIGN KEY (id_pei_sesion) REFERENCES consultorio.pei_sesion_planificada(id_pei_sesion);


--
-- Name: pei_sesion_planificada pei_sesion_planificada_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_planificada
    ADD CONSTRAINT pei_sesion_planificada_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: pei_sesion_planificada pei_sesion_planificada_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_planificada
    ADD CONSTRAINT pei_sesion_planificada_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: pei_sesion_planificada pei_sesion_planificada_id_pei_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.pei_sesion_planificada
    ADD CONSTRAINT pei_sesion_planificada_id_pei_fkey FOREIGN KEY (id_pei) REFERENCES consultorio.pei(id_pei);


--
-- Name: planes_tratamiento planes_tratamiento_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento
    ADD CONSTRAINT planes_tratamiento_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: planes_tratamiento planes_tratamiento_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento
    ADD CONSTRAINT planes_tratamiento_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: planes_tratamiento planes_tratamiento_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento
    ADD CONSTRAINT planes_tratamiento_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: planes_tratamiento planes_tratamiento_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento
    ADD CONSTRAINT planes_tratamiento_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: planes_tratamiento_items planes_tratamiento_items_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento_items
    ADD CONSTRAINT planes_tratamiento_items_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: planes_tratamiento_items planes_tratamiento_items_id_plan_tratamiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.planes_tratamiento_items
    ADD CONSTRAINT planes_tratamiento_items_id_plan_tratamiento_fkey FOREIGN KEY (id_plan_tratamiento) REFERENCES consultorio.planes_tratamiento(id_plan_tratamiento);


--
-- Name: plantillas_justificativos plantillas_justificativos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.plantillas_justificativos
    ADD CONSTRAINT plantillas_justificativos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: plantillas_justificativos plantillas_justificativos_id_tipo_justificativo_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.plantillas_justificativos
    ADD CONSTRAINT plantillas_justificativos_id_tipo_justificativo_fkey FOREIGN KEY (id_tipo_justificativo) REFERENCES consultorio.tipos_justificativos(id_tipo_justificativo);


--
-- Name: procedimientos_empresa procedimientos_empresa_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.procedimientos_empresa
    ADD CONSTRAINT procedimientos_empresa_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: procedimientos_empresa procedimientos_empresa_id_tipo_procedimiento_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.procedimientos_empresa
    ADD CONSTRAINT procedimientos_empresa_id_tipo_procedimiento_fkey FOREIGN KEY (id_tipo_procedimiento) REFERENCES consultorio.tipos_procedimientos(id_tipo_procedimiento);


--
-- Name: psicologia_perfil_empresa psicologia_perfil_empresa_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.psicologia_perfil_empresa
    ADD CONSTRAINT psicologia_perfil_empresa_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: psicologia_perfil_empresa psicologia_perfil_empresa_id_empresa_perfil_clinico_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.psicologia_perfil_empresa
    ADD CONSTRAINT psicologia_perfil_empresa_id_empresa_perfil_clinico_fkey FOREIGN KEY (id_empresa_perfil_clinico) REFERENCES consultorio.empresa_perfil_clinico(id_empresa_perfil_clinico);


--
-- Name: recetas_detalle recetas_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas_detalle
    ADD CONSTRAINT recetas_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: recetas_detalle recetas_detalle_id_medicamento_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas_detalle
    ADD CONSTRAINT recetas_detalle_id_medicamento_empresa_fkey FOREIGN KEY (id_medicamento_empresa) REFERENCES consultorio.medicamentos_empresa(id_medicamento_empresa);


--
-- Name: recetas_detalle recetas_detalle_id_receta_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas_detalle
    ADD CONSTRAINT recetas_detalle_id_receta_fkey FOREIGN KEY (id_receta) REFERENCES consultorio.recetas(id_receta);


--
-- Name: recetas recetas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas
    ADD CONSTRAINT recetas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: recetas recetas_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas
    ADD CONSTRAINT recetas_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: recetas recetas_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas
    ADD CONSTRAINT recetas_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: recetas recetas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas
    ADD CONSTRAINT recetas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: recetas recetas_id_receta_origen_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.recetas
    ADD CONSTRAINT recetas_id_receta_origen_fkey FOREIGN KEY (id_receta_origen) REFERENCES consultorio.recetas(id_receta);


--
-- Name: resultados_analisis_detalle resultados_analisis_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis_detalle
    ADD CONSTRAINT resultados_analisis_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: resultados_analisis_detalle resultados_analisis_detalle_id_orden_analisis_detalle_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis_detalle
    ADD CONSTRAINT resultados_analisis_detalle_id_orden_analisis_detalle_fkey FOREIGN KEY (id_orden_analisis_detalle) REFERENCES consultorio.ordenes_analisis_detalle(id_orden_analisis_detalle);


--
-- Name: resultados_analisis_detalle resultados_analisis_detalle_id_resultado_analisis_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis_detalle
    ADD CONSTRAINT resultados_analisis_detalle_id_resultado_analisis_fkey FOREIGN KEY (id_resultado_analisis) REFERENCES consultorio.resultados_analisis(id_resultado_analisis);


--
-- Name: resultados_analisis resultados_analisis_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis
    ADD CONSTRAINT resultados_analisis_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: resultados_analisis resultados_analisis_id_orden_analisis_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.resultados_analisis
    ADD CONSTRAINT resultados_analisis_id_orden_analisis_fkey FOREIGN KEY (id_orden_analisis) REFERENCES consultorio.ordenes_analisis(id_orden_analisis);


--
-- Name: signos_vitales_detalle signos_vitales_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales_detalle
    ADD CONSTRAINT signos_vitales_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: signos_vitales_detalle signos_vitales_detalle_id_signos_vitales_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales_detalle
    ADD CONSTRAINT signos_vitales_detalle_id_signos_vitales_fkey FOREIGN KEY (id_signos_vitales) REFERENCES consultorio.signos_vitales(id_signos_vitales);


--
-- Name: signos_vitales_detalle signos_vitales_detalle_id_tipo_signo_vital_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales_detalle
    ADD CONSTRAINT signos_vitales_detalle_id_tipo_signo_vital_fkey FOREIGN KEY (id_tipo_signo_vital) REFERENCES consultorio.tipos_signos_vitales(id_tipo_signo_vital);


--
-- Name: signos_vitales signos_vitales_id_empresa_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales
    ADD CONSTRAINT signos_vitales_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: signos_vitales signos_vitales_id_episodio_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales
    ADD CONSTRAINT signos_vitales_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: signos_vitales signos_vitales_id_especialista_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales
    ADD CONSTRAINT signos_vitales_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: signos_vitales signos_vitales_id_paciente_fkey; Type: FK CONSTRAINT; Schema: consultorio; Owner: postgres
--

ALTER TABLE ONLY consultorio.signos_vitales
    ADD CONSTRAINT signos_vitales_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: agenda_horarios_excepciones agenda_horarios_excepciones_id_agenda_horario_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios_excepciones
    ADD CONSTRAINT agenda_horarios_excepciones_id_agenda_horario_fkey FOREIGN KEY (id_agenda_horario) REFERENCES core.agenda_horarios(id_agenda_horario);


--
-- Name: agenda_horarios_excepciones agenda_horarios_excepciones_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios_excepciones
    ADD CONSTRAINT agenda_horarios_excepciones_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: agenda_horarios agenda_horarios_id_consultorio_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_consultorio_fkey FOREIGN KEY (id_consultorio) REFERENCES core.consultorios(id_consultorio);


--
-- Name: agenda_horarios agenda_horarios_id_dia_semana_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_dia_semana_fkey FOREIGN KEY (id_dia_semana) REFERENCES core.dias_semana(id_dia_semana);


--
-- Name: agenda_horarios agenda_horarios_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: agenda_horarios agenda_horarios_id_especialidad_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES core.especialidades(id_especialidad);


--
-- Name: agenda_horarios agenda_horarios_id_especialista_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: agenda_horarios agenda_horarios_id_sede_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES core.sedes(id_sede);


--
-- Name: auditoria_sistema auditoria_sistema_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE core.auditoria_sistema
    ADD CONSTRAINT auditoria_sistema_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: auditoria_sistema auditoria_sistema_id_usuario_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE core.auditoria_sistema
    ADD CONSTRAINT auditoria_sistema_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES core.usuarios(id_usuario);


--
-- Name: cargos cargos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.cargos
    ADD CONSTRAINT cargos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: citas citas_id_consultorio_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_consultorio_fkey FOREIGN KEY (id_consultorio) REFERENCES core.consultorios(id_consultorio);


--
-- Name: citas citas_id_contrato_tratamiento_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_contrato_tratamiento_fkey FOREIGN KEY (id_contrato_tratamiento) REFERENCES consultorio.contratos_tratamiento(id_contrato_tratamiento);


--
-- Name: citas citas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: citas citas_id_especialidad_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES core.especialidades(id_especialidad);


--
-- Name: citas citas_id_especialista_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: citas citas_id_estado_cita_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_estado_cita_fkey FOREIGN KEY (id_estado_cita) REFERENCES core.estados_citas(id_estado_cita);


--
-- Name: citas citas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: citas citas_id_sede_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES core.sedes(id_sede);


--
-- Name: citas citas_id_slot_agenda_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas
    ADD CONSTRAINT citas_id_slot_agenda_fkey FOREIGN KEY (id_slot_agenda) REFERENCES core.slots_agenda(id_slot_agenda);


--
-- Name: citas_log_estados citas_log_estados_id_cita_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas_log_estados
    ADD CONSTRAINT citas_log_estados_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES core.citas(id_cita);


--
-- Name: citas_log_estados citas_log_estados_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas_log_estados
    ADD CONSTRAINT citas_log_estados_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: citas_log_estados citas_log_estados_id_estado_anterior_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas_log_estados
    ADD CONSTRAINT citas_log_estados_id_estado_anterior_fkey FOREIGN KEY (id_estado_anterior) REFERENCES core.estados_citas(id_estado_cita);


--
-- Name: citas_log_estados citas_log_estados_id_estado_nuevo_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.citas_log_estados
    ADD CONSTRAINT citas_log_estados_id_estado_nuevo_fkey FOREIGN KEY (id_estado_nuevo) REFERENCES core.estados_citas(id_estado_cita);


--
-- Name: ciudades ciudades_id_departamento_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.ciudades
    ADD CONSTRAINT ciudades_id_departamento_fkey FOREIGN KEY (id_departamento) REFERENCES core.departamentos(id_departamento);


--
-- Name: consultorios consultorios_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.consultorios
    ADD CONSTRAINT consultorios_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: consultorios consultorios_id_sede_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.consultorios
    ADD CONSTRAINT consultorios_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES core.sedes(id_sede);


--
-- Name: departamentos departamentos_id_pais_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.departamentos
    ADD CONSTRAINT departamentos_id_pais_fkey FOREIGN KEY (id_pais) REFERENCES core.paises(id_pais);


--
-- Name: empresa_certificados empresa_certificados_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_certificados
    ADD CONSTRAINT empresa_certificados_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: empresa_configuracion empresa_configuracion_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_configuracion
    ADD CONSTRAINT empresa_configuracion_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: empresa_modulos empresa_modulos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_modulos
    ADD CONSTRAINT empresa_modulos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: empresa_modulos empresa_modulos_id_modulo_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresa_modulos
    ADD CONSTRAINT empresa_modulos_id_modulo_fkey FOREIGN KEY (id_modulo) REFERENCES core.modulos(id_modulo);


--
-- Name: empresas empresas_id_ciudad_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresas
    ADD CONSTRAINT empresas_id_ciudad_fkey FOREIGN KEY (id_ciudad) REFERENCES core.ciudades(id_ciudad);


--
-- Name: empresas empresas_id_departamento_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.empresas
    ADD CONSTRAINT empresas_id_departamento_fkey FOREIGN KEY (id_departamento) REFERENCES core.departamentos(id_departamento);


--
-- Name: especialidades especialidades_cod_tipo_clinico_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialidades
    ADD CONSTRAINT especialidades_cod_tipo_clinico_fkey FOREIGN KEY (cod_tipo_clinico) REFERENCES core.tipos_clinicos(cod_tipo_clinico);


--
-- Name: especialidades especialidades_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialidades
    ADD CONSTRAINT especialidades_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: especialista_especialidades especialista_especialidades_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: especialista_especialidades especialista_especialidades_id_especialidad_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES core.especialidades(id_especialidad);


--
-- Name: especialista_especialidades especialista_especialidades_id_especialista_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES core.especialistas(id_especialista);


--
-- Name: especialistas especialistas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialistas
    ADD CONSTRAINT especialistas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: especialistas especialistas_id_funcionario_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.especialistas
    ADD CONSTRAINT especialistas_id_funcionario_fkey FOREIGN KEY (id_funcionario) REFERENCES core.funcionarios(id_funcionario);


--
-- Name: establecimientos establecimientos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.establecimientos
    ADD CONSTRAINT establecimientos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: establecimientos establecimientos_id_sede_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.establecimientos
    ADD CONSTRAINT establecimientos_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES core.sedes(id_sede);


--
-- Name: mfa_tokens mfa_tokens_id_usuario_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.mfa_tokens
    ADD CONSTRAINT mfa_tokens_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES core.usuarios(id_usuario) ON DELETE CASCADE;


--
-- Name: suscripcion_expansiones suscripcion_expansiones_id_suscripcion_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.suscripcion_expansiones
    ADD CONSTRAINT suscripcion_expansiones_id_suscripcion_fkey FOREIGN KEY (id_suscripcion) REFERENCES core.suscripciones(id_suscripcion);


--
-- Name: aperturas_caja aperturas_caja_id_caja_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.aperturas_caja
    ADD CONSTRAINT aperturas_caja_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES facturacion.cajas(id_caja);


--
-- Name: aperturas_caja aperturas_caja_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.aperturas_caja
    ADD CONSTRAINT aperturas_caja_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: arqueos_caja arqueos_caja_id_apertura_caja_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.arqueos_caja
    ADD CONSTRAINT arqueos_caja_id_apertura_caja_fkey FOREIGN KEY (id_apertura_caja) REFERENCES facturacion.aperturas_caja(id_apertura_caja);


--
-- Name: arqueos_caja arqueos_caja_id_caja_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.arqueos_caja
    ADD CONSTRAINT arqueos_caja_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES facturacion.cajas(id_caja);


--
-- Name: arqueos_caja arqueos_caja_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.arqueos_caja
    ADD CONSTRAINT arqueos_caja_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: autofactura_detalle autofactura_detalle_id_autofactura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofactura_detalle
    ADD CONSTRAINT autofactura_detalle_id_autofactura_fkey FOREIGN KEY (id_autofactura) REFERENCES facturacion.autofacturas(id_autofactura);


--
-- Name: autofactura_detalle autofactura_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofactura_detalle
    ADD CONSTRAINT autofactura_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: autofactura_detalle autofactura_detalle_id_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofactura_detalle
    ADD CONSTRAINT autofactura_detalle_id_item_fkey FOREIGN KEY (id_item) REFERENCES facturacion.items(id_item);


--
-- Name: autofacturas autofacturas_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: autofacturas autofacturas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: autofacturas autofacturas_id_establecimiento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_id_establecimiento_fkey FOREIGN KEY (id_establecimiento) REFERENCES core.establecimientos(id_establecimiento);


--
-- Name: autofacturas autofacturas_id_moneda_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES core.monedas(id_moneda);


--
-- Name: autofacturas autofacturas_id_punto_expedicion_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_id_punto_expedicion_fkey FOREIGN KEY (id_punto_expedicion) REFERENCES core.puntos_expedicion(id_punto_expedicion);


--
-- Name: autofacturas autofacturas_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.autofacturas
    ADD CONSTRAINT autofacturas_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES facturacion.timbrados(id_timbrado);


--
-- Name: cajas cajas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cajas
    ADD CONSTRAINT cajas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: cajas cajas_id_sede_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cajas
    ADD CONSTRAINT cajas_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES core.sedes(id_sede);


--
-- Name: categorias_items categorias_items_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.categorias_items
    ADD CONSTRAINT categorias_items_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: cheques_recibidos cheques_recibidos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cheques_recibidos
    ADD CONSTRAINT cheques_recibidos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: cheques_recibidos cheques_recibidos_id_entidad_bancaria_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cheques_recibidos
    ADD CONSTRAINT cheques_recibidos_id_entidad_bancaria_fkey FOREIGN KEY (id_entidad_bancaria) REFERENCES facturacion.entidades_bancarias(id_entidad_bancaria);


--
-- Name: cobranza_detalle cobranza_detalle_id_cheque_recibido_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_cheque_recibido_fkey FOREIGN KEY (id_cheque_recibido) REFERENCES facturacion.cheques_recibidos(id_cheque_recibido);


--
-- Name: cobranza_detalle cobranza_detalle_id_cobranza_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_cobranza_fkey FOREIGN KEY (id_cobranza) REFERENCES facturacion.cobranzas(id_cobranza);


--
-- Name: cobranza_detalle cobranza_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: cobranza_detalle cobranza_detalle_id_entidad_bancaria_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_entidad_bancaria_fkey FOREIGN KEY (id_entidad_bancaria) REFERENCES facturacion.entidades_bancarias(id_entidad_bancaria);


--
-- Name: cobranza_detalle cobranza_detalle_id_forma_cobro_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_forma_cobro_fkey FOREIGN KEY (id_forma_cobro) REFERENCES core.formas_cobro(id_forma_cobro);


--
-- Name: cobranza_detalle cobranza_detalle_id_marca_tarjeta_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_marca_tarjeta_fkey FOREIGN KEY (id_marca_tarjeta) REFERENCES core.marcas_tarjeta(id_marca_tarjeta);


--
-- Name: cobranzas cobranzas_id_cuenta_cobrar_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT cobranzas_id_cuenta_cobrar_fkey FOREIGN KEY (id_cuenta_cobrar) REFERENCES facturacion.cuentas_cobrar(id_cuenta_cobrar);


--
-- Name: cobranzas cobranzas_id_cuota_cobrar_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT cobranzas_id_cuota_cobrar_fkey FOREIGN KEY (id_cuota_cobrar) REFERENCES facturacion.cuotas_cobrar(id_cuota_cobrar);


--
-- Name: cobranzas cobranzas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT cobranzas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: cobranzas cobranzas_id_entidad_pagadora_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT cobranzas_id_entidad_pagadora_fkey FOREIGN KEY (id_entidad_pagadora) REFERENCES facturacion.entidades_pagadoras(id_entidad_pagadora);


--
-- Name: cobranzas cobranzas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT cobranzas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_entidad_pagadora_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_entidad_pagadora_fkey FOREIGN KEY (id_entidad_pagadora) REFERENCES facturacion.entidades_pagadoras(id_entidad_pagadora);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_factura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_nota_debito_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_nota_debito_fkey FOREIGN KEY (id_nota_debito) REFERENCES facturacion.notas_debito(id_nota_debito);


--
-- Name: cuentas_cobrar cuentas_cobrar_id_paciente_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: cuotas_cobrar cuotas_cobrar_id_cuenta_cobrar_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuotas_cobrar
    ADD CONSTRAINT cuotas_cobrar_id_cuenta_cobrar_fkey FOREIGN KEY (id_cuenta_cobrar) REFERENCES facturacion.cuentas_cobrar(id_cuenta_cobrar);


--
-- Name: cuotas_cobrar cuotas_cobrar_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cuotas_cobrar
    ADD CONSTRAINT cuotas_cobrar_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: documentos_electronicos documentos_electronicos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.documentos_electronicos
    ADD CONSTRAINT documentos_electronicos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: documentos_electronicos documentos_electronicos_id_tipo_comprobante_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.documentos_electronicos
    ADD CONSTRAINT documentos_electronicos_id_tipo_comprobante_fkey FOREIGN KEY (id_tipo_comprobante) REFERENCES core.tipos_comprobantes(id_tipo_comprobante);


--
-- Name: entidades_pagadoras entidades_pagadoras_id_ciudad_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_pagadoras
    ADD CONSTRAINT entidades_pagadoras_id_ciudad_fkey FOREIGN KEY (id_ciudad) REFERENCES core.ciudades(id_ciudad);


--
-- Name: entidades_pagadoras entidades_pagadoras_id_departamento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_pagadoras
    ADD CONSTRAINT entidades_pagadoras_id_departamento_fkey FOREIGN KEY (id_departamento) REFERENCES core.departamentos(id_departamento);


--
-- Name: entidades_pagadoras entidades_pagadoras_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.entidades_pagadoras
    ADD CONSTRAINT entidades_pagadoras_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: factura_detalle factura_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_detalle
    ADD CONSTRAINT factura_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: factura_detalle factura_detalle_id_factura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_detalle
    ADD CONSTRAINT factura_detalle_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: factura_detalle factura_detalle_id_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_detalle
    ADD CONSTRAINT factura_detalle_id_item_fkey FOREIGN KEY (id_item) REFERENCES facturacion.items(id_item);


--
-- Name: factura_medios_pago factura_medios_pago_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_medios_pago
    ADD CONSTRAINT factura_medios_pago_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: factura_medios_pago factura_medios_pago_id_factura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_medios_pago
    ADD CONSTRAINT factura_medios_pago_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: factura_medios_pago factura_medios_pago_id_forma_cobro_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_medios_pago
    ADD CONSTRAINT factura_medios_pago_id_forma_cobro_fkey FOREIGN KEY (id_forma_cobro) REFERENCES core.formas_cobro(id_forma_cobro);


--
-- Name: factura_medios_pago factura_medios_pago_id_moneda_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.factura_medios_pago
    ADD CONSTRAINT factura_medios_pago_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES core.monedas(id_moneda);


--
-- Name: facturas facturas_id_ciudad_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_ciudad_receptor_fkey FOREIGN KEY (id_ciudad_receptor) REFERENCES core.ciudades(id_ciudad);


--
-- Name: facturas facturas_id_condicion_venta_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_condicion_venta_fkey FOREIGN KEY (id_condicion_venta) REFERENCES core.condiciones_venta(id_condicion_venta);


--
-- Name: facturas facturas_id_contrato_tratamiento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_contrato_tratamiento_fkey FOREIGN KEY (id_contrato_tratamiento) REFERENCES consultorio.contratos_tratamiento(id_contrato_tratamiento);


--
-- Name: facturas facturas_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: facturas facturas_id_departamento_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_departamento_receptor_fkey FOREIGN KEY (id_departamento_receptor) REFERENCES core.departamentos(id_departamento);


--
-- Name: facturas facturas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: facturas facturas_id_entidad_pagadora_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_entidad_pagadora_fkey FOREIGN KEY (id_entidad_pagadora) REFERENCES facturacion.entidades_pagadoras(id_entidad_pagadora);


--
-- Name: facturas facturas_id_episodio_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_episodio_fkey FOREIGN KEY (id_episodio) REFERENCES consultorio.episodios(id_episodio);


--
-- Name: facturas facturas_id_establecimiento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_establecimiento_fkey FOREIGN KEY (id_establecimiento) REFERENCES core.establecimientos(id_establecimiento);


--
-- Name: facturas facturas_id_moneda_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES core.monedas(id_moneda);


--
-- Name: facturas facturas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: facturas facturas_id_pais_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_pais_receptor_fkey FOREIGN KEY (id_pais_receptor) REFERENCES core.paises(id_pais);


--
-- Name: facturas facturas_id_plan_tratamiento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_plan_tratamiento_fkey FOREIGN KEY (id_plan_tratamiento) REFERENCES consultorio.planes_tratamiento(id_plan_tratamiento);


--
-- Name: facturas facturas_id_punto_expedicion_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_punto_expedicion_fkey FOREIGN KEY (id_punto_expedicion) REFERENCES core.puntos_expedicion(id_punto_expedicion);


--
-- Name: facturas facturas_id_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_receptor_fkey FOREIGN KEY (id_receptor) REFERENCES core.personas(id_persona);


--
-- Name: facturas facturas_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES facturacion.timbrados(id_timbrado);


--
-- Name: facturas facturas_id_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.facturas
    ADD CONSTRAINT facturas_id_tipo_documento_fkey FOREIGN KEY (id_tipo_documento) REFERENCES core.tipos_documentos_identidad(id_tipo_documento);


--
-- Name: cobranzas fk_cobranzas_apertura; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT fk_cobranzas_apertura FOREIGN KEY (id_apertura_caja) REFERENCES facturacion.aperturas_caja(id_apertura_caja);


--
-- Name: cobranzas fk_cobranzas_caja; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.cobranzas
    ADD CONSTRAINT fk_cobranzas_caja FOREIGN KEY (id_caja) REFERENCES facturacion.cajas(id_caja);


--
-- Name: items items_id_categoria_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items
    ADD CONSTRAINT items_id_categoria_item_fkey FOREIGN KEY (id_categoria_item) REFERENCES facturacion.categorias_items(id_categoria_item);


--
-- Name: items items_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items
    ADD CONSTRAINT items_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: items items_id_procedimiento_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items
    ADD CONSTRAINT items_id_procedimiento_empresa_fkey FOREIGN KEY (id_procedimiento_empresa) REFERENCES consultorio.procedimientos_empresa(id_procedimiento_empresa);


--
-- Name: items items_id_tipo_impuesto_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items
    ADD CONSTRAINT items_id_tipo_impuesto_fkey FOREIGN KEY (id_tipo_impuesto) REFERENCES core.tipos_impuestos(id_tipo_impuesto);


--
-- Name: items items_id_tipo_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.items
    ADD CONSTRAINT items_id_tipo_item_fkey FOREIGN KEY (id_tipo_item) REFERENCES core.tipos_items(id_tipo_item);


--
-- Name: libro_ventas libro_ventas_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: libro_ventas libro_ventas_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: libro_ventas libro_ventas_id_factura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: libro_ventas libro_ventas_id_nota_credito_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_id_nota_credito_fkey FOREIGN KEY (id_nota_credito) REFERENCES facturacion.notas_credito(id_nota_credito);


--
-- Name: libro_ventas libro_ventas_id_nota_debito_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_id_nota_debito_fkey FOREIGN KEY (id_nota_debito) REFERENCES facturacion.notas_debito(id_nota_debito);


--
-- Name: libro_ventas libro_ventas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES core.pacientes(id_paciente);


--
-- Name: libro_ventas libro_ventas_id_tipo_comprobante_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.libro_ventas
    ADD CONSTRAINT libro_ventas_id_tipo_comprobante_fkey FOREIGN KEY (id_tipo_comprobante) REFERENCES core.tipos_comprobantes(id_tipo_comprobante);


--
-- Name: movimientos_caja movimientos_caja_id_apertura_caja_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.movimientos_caja
    ADD CONSTRAINT movimientos_caja_id_apertura_caja_fkey FOREIGN KEY (id_apertura_caja) REFERENCES facturacion.aperturas_caja(id_apertura_caja);


--
-- Name: movimientos_caja movimientos_caja_id_caja_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.movimientos_caja
    ADD CONSTRAINT movimientos_caja_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES facturacion.cajas(id_caja);


--
-- Name: movimientos_caja movimientos_caja_id_cobranza_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.movimientos_caja
    ADD CONSTRAINT movimientos_caja_id_cobranza_fkey FOREIGN KEY (id_cobranza) REFERENCES facturacion.cobranzas(id_cobranza);


--
-- Name: movimientos_caja movimientos_caja_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.movimientos_caja
    ADD CONSTRAINT movimientos_caja_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: nota_credito_detalle nota_credito_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: nota_credito_detalle nota_credito_detalle_id_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_id_item_fkey FOREIGN KEY (id_item) REFERENCES facturacion.items(id_item);


--
-- Name: nota_credito_detalle nota_credito_detalle_id_nota_credito_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_id_nota_credito_fkey FOREIGN KEY (id_nota_credito) REFERENCES facturacion.notas_credito(id_nota_credito);


--
-- Name: nota_debito_detalle nota_debito_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: nota_debito_detalle nota_debito_detalle_id_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_id_item_fkey FOREIGN KEY (id_item) REFERENCES facturacion.items(id_item);


--
-- Name: nota_debito_detalle nota_debito_detalle_id_nota_debito_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_id_nota_debito_fkey FOREIGN KEY (id_nota_debito) REFERENCES facturacion.notas_debito(id_nota_debito);


--
-- Name: nota_remision_detalle nota_remision_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_remision_detalle
    ADD CONSTRAINT nota_remision_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: nota_remision_detalle nota_remision_detalle_id_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_remision_detalle
    ADD CONSTRAINT nota_remision_detalle_id_item_fkey FOREIGN KEY (id_item) REFERENCES facturacion.items(id_item);


--
-- Name: nota_remision_detalle nota_remision_detalle_id_nota_remision_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.nota_remision_detalle
    ADD CONSTRAINT nota_remision_detalle_id_nota_remision_fkey FOREIGN KEY (id_nota_remision) REFERENCES facturacion.notas_remision(id_nota_remision);


--
-- Name: notas_credito notas_credito_id_ciudad_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_ciudad_receptor_fkey FOREIGN KEY (id_ciudad_receptor) REFERENCES core.ciudades(id_ciudad);


--
-- Name: notas_credito notas_credito_id_condicion_venta_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_condicion_venta_fkey FOREIGN KEY (id_condicion_venta) REFERENCES core.condiciones_venta(id_condicion_venta);


--
-- Name: notas_credito notas_credito_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: notas_credito notas_credito_id_departamento_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_departamento_receptor_fkey FOREIGN KEY (id_departamento_receptor) REFERENCES core.departamentos(id_departamento);


--
-- Name: notas_credito notas_credito_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: notas_credito notas_credito_id_establecimiento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_establecimiento_fkey FOREIGN KEY (id_establecimiento) REFERENCES core.establecimientos(id_establecimiento);


--
-- Name: notas_credito notas_credito_id_factura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: notas_credito notas_credito_id_moneda_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES core.monedas(id_moneda);


--
-- Name: notas_credito notas_credito_id_pais_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_pais_receptor_fkey FOREIGN KEY (id_pais_receptor) REFERENCES core.paises(id_pais);


--
-- Name: notas_credito notas_credito_id_punto_expedicion_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_punto_expedicion_fkey FOREIGN KEY (id_punto_expedicion) REFERENCES core.puntos_expedicion(id_punto_expedicion);


--
-- Name: notas_credito notas_credito_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES facturacion.timbrados(id_timbrado);


--
-- Name: notas_credito notas_credito_id_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_credito
    ADD CONSTRAINT notas_credito_id_tipo_documento_fkey FOREIGN KEY (id_tipo_documento) REFERENCES core.tipos_documentos_identidad(id_tipo_documento);


--
-- Name: notas_debito notas_debito_id_ciudad_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_ciudad_receptor_fkey FOREIGN KEY (id_ciudad_receptor) REFERENCES core.ciudades(id_ciudad);


--
-- Name: notas_debito notas_debito_id_condicion_venta_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_condicion_venta_fkey FOREIGN KEY (id_condicion_venta) REFERENCES core.condiciones_venta(id_condicion_venta);


--
-- Name: notas_debito notas_debito_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: notas_debito notas_debito_id_departamento_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_departamento_receptor_fkey FOREIGN KEY (id_departamento_receptor) REFERENCES core.departamentos(id_departamento);


--
-- Name: notas_debito notas_debito_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: notas_debito notas_debito_id_establecimiento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_establecimiento_fkey FOREIGN KEY (id_establecimiento) REFERENCES core.establecimientos(id_establecimiento);


--
-- Name: notas_debito notas_debito_id_factura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: notas_debito notas_debito_id_moneda_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES core.monedas(id_moneda);


--
-- Name: notas_debito notas_debito_id_pais_receptor_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_pais_receptor_fkey FOREIGN KEY (id_pais_receptor) REFERENCES core.paises(id_pais);


--
-- Name: notas_debito notas_debito_id_punto_expedicion_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_punto_expedicion_fkey FOREIGN KEY (id_punto_expedicion) REFERENCES core.puntos_expedicion(id_punto_expedicion);


--
-- Name: notas_debito notas_debito_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES facturacion.timbrados(id_timbrado);


--
-- Name: notas_debito notas_debito_id_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_debito
    ADD CONSTRAINT notas_debito_id_tipo_documento_fkey FOREIGN KEY (id_tipo_documento) REFERENCES core.tipos_documentos_identidad(id_tipo_documento);


--
-- Name: notas_remision notas_remision_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: notas_remision notas_remision_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: notas_remision notas_remision_id_establecimiento_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_id_establecimiento_fkey FOREIGN KEY (id_establecimiento) REFERENCES core.establecimientos(id_establecimiento);


--
-- Name: notas_remision notas_remision_id_factura_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES facturacion.facturas(id_factura);


--
-- Name: notas_remision notas_remision_id_punto_expedicion_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_id_punto_expedicion_fkey FOREIGN KEY (id_punto_expedicion) REFERENCES core.puntos_expedicion(id_punto_expedicion);


--
-- Name: notas_remision notas_remision_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.notas_remision
    ADD CONSTRAINT notas_remision_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES facturacion.timbrados(id_timbrado);


--
-- Name: recaudacion_detalle recaudacion_detalle_id_cobranza_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudacion_detalle
    ADD CONSTRAINT recaudacion_detalle_id_cobranza_fkey FOREIGN KEY (id_cobranza) REFERENCES facturacion.cobranzas(id_cobranza);


--
-- Name: recaudacion_detalle recaudacion_detalle_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudacion_detalle
    ADD CONSTRAINT recaudacion_detalle_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: recaudacion_detalle recaudacion_detalle_id_recaudacion_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudacion_detalle
    ADD CONSTRAINT recaudacion_detalle_id_recaudacion_fkey FOREIGN KEY (id_recaudacion) REFERENCES facturacion.recaudaciones(id_recaudacion);


--
-- Name: recaudaciones recaudaciones_id_caja_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudaciones
    ADD CONSTRAINT recaudaciones_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES facturacion.cajas(id_caja);


--
-- Name: recaudaciones recaudaciones_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudaciones
    ADD CONSTRAINT recaudaciones_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: recaudaciones recaudaciones_id_entidad_bancaria_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.recaudaciones
    ADD CONSTRAINT recaudaciones_id_entidad_bancaria_fkey FOREIGN KEY (id_entidad_bancaria) REFERENCES facturacion.entidades_bancarias(id_entidad_bancaria);


--
-- Name: secuencias_numeracion secuencias_numeracion_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.secuencias_numeracion
    ADD CONSTRAINT secuencias_numeracion_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: secuencias_numeracion secuencias_numeracion_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.secuencias_numeracion
    ADD CONSTRAINT secuencias_numeracion_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES facturacion.timbrados(id_timbrado);


--
-- Name: sifen_config sifen_config_id_empresa_certificado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_config
    ADD CONSTRAINT sifen_config_id_empresa_certificado_fkey FOREIGN KEY (id_empresa_certificado) REFERENCES core.empresa_certificados(id_empresa_certificado);


--
-- Name: sifen_config sifen_config_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_config
    ADD CONSTRAINT sifen_config_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: sifen_eventos sifen_eventos_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_eventos
    ADD CONSTRAINT sifen_eventos_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: sifen_eventos sifen_eventos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_eventos
    ADD CONSTRAINT sifen_eventos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: sifen_eventos sifen_eventos_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_eventos
    ADD CONSTRAINT sifen_eventos_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES facturacion.timbrados(id_timbrado);


--
-- Name: sifen_lote_documentos sifen_lote_documentos_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lote_documentos
    ADD CONSTRAINT sifen_lote_documentos_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: sifen_lote_documentos sifen_lote_documentos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lote_documentos
    ADD CONSTRAINT sifen_lote_documentos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: sifen_lote_documentos sifen_lote_documentos_id_lote_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lote_documentos
    ADD CONSTRAINT sifen_lote_documentos_id_lote_fkey FOREIGN KEY (id_lote) REFERENCES facturacion.sifen_lotes(id_lote);


--
-- Name: sifen_lotes sifen_lotes_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_lotes
    ADD CONSTRAINT sifen_lotes_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: sifen_transmision_log sifen_transmision_log_id_de_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_transmision_log
    ADD CONSTRAINT sifen_transmision_log_id_de_fkey FOREIGN KEY (id_de) REFERENCES facturacion.documentos_electronicos(id_de);


--
-- Name: sifen_transmision_log sifen_transmision_log_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_transmision_log
    ADD CONSTRAINT sifen_transmision_log_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: sifen_transmision_log sifen_transmision_log_id_lote_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.sifen_transmision_log
    ADD CONSTRAINT sifen_transmision_log_id_lote_fkey FOREIGN KEY (id_lote) REFERENCES facturacion.sifen_lotes(id_lote);


--
-- Name: tarifario_precios tarifario_precios_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.tarifario_precios
    ADD CONSTRAINT tarifario_precios_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: tarifario_precios tarifario_precios_id_entidad_pagadora_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.tarifario_precios
    ADD CONSTRAINT tarifario_precios_id_entidad_pagadora_fkey FOREIGN KEY (id_entidad_pagadora) REFERENCES facturacion.entidades_pagadoras(id_entidad_pagadora);


--
-- Name: tarifario_precios tarifario_precios_id_item_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.tarifario_precios
    ADD CONSTRAINT tarifario_precios_id_item_fkey FOREIGN KEY (id_item) REFERENCES facturacion.items(id_item);


--
-- Name: tarifario_precios tarifario_precios_id_moneda_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.tarifario_precios
    ADD CONSTRAINT tarifario_precios_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES core.monedas(id_moneda);


--
-- Name: timbrado_habilitaciones timbrado_habilitaciones_id_empresa_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrado_habilitaciones
    ADD CONSTRAINT timbrado_habilitaciones_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES core.empresas(id_empresa);


--
-- Name: timbrado_habilitaciones timbrado_habilitaciones_id_punto_expedicion_fkey; Type: FK CONSTRAINT; Schema: facturacion; Owner: postgres
--

ALTER TABLE ONLY facturacion.timbrado_habilitaciones
    ADD CONSTRAINT timbrado_habilitaciones_id_punto_expedicion_fkey FOREIGN KEY (id_punto_expedicion) REFERENCES core.puntos_expedicion(id_punto_expedicion);


--
-- Name: acuerdo_monto_historial; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.acuerdo_monto_historial ENABLE ROW LEVEL SECURITY;

--
-- Name: acuerdo_monto_historial acuerdo_monto_historial_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY acuerdo_monto_historial_tenant ON consultorio.acuerdo_monto_historial USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: acuerdos_terapeuticos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.acuerdos_terapeuticos ENABLE ROW LEVEL SECURITY;

--
-- Name: acuerdos_terapeuticos acuerdos_terapeuticos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY acuerdos_terapeuticos_tenant ON consultorio.acuerdos_terapeuticos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: anamnesis; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.anamnesis ENABLE ROW LEVEL SECURITY;

--
-- Name: anamnesis_adulto_ext; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.anamnesis_adulto_ext ENABLE ROW LEVEL SECURITY;

--
-- Name: anamnesis_adulto_ext anamnesis_adulto_ext_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY anamnesis_adulto_ext_tenant ON consultorio.anamnesis_adulto_ext USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: anamnesis_infantil_ext; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.anamnesis_infantil_ext ENABLE ROW LEVEL SECURITY;

--
-- Name: anamnesis_infantil_ext anamnesis_infantil_ext_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY anamnesis_infantil_ext_tenant ON consultorio.anamnesis_infantil_ext USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: anamnesis anamnesis_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY anamnesis_tenant ON consultorio.anamnesis USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: antecedentes_paciente; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.antecedentes_paciente ENABLE ROW LEVEL SECURITY;

--
-- Name: antecedentes_paciente antecedentes_paciente_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY antecedentes_paciente_tenant ON consultorio.antecedentes_paciente USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cobros_simples; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.cobros_simples ENABLE ROW LEVEL SECURITY;

--
-- Name: cobros_simples cobros_simples_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY cobros_simples_tenant ON consultorio.cobros_simples USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: consentimientos_firmados; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.consentimientos_firmados ENABLE ROW LEVEL SECURITY;

--
-- Name: consentimientos_firmados consentimientos_firmados_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY consentimientos_firmados_tenant ON consultorio.consentimientos_firmados USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: contratos_tratamiento; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.contratos_tratamiento ENABLE ROW LEVEL SECURITY;

--
-- Name: contratos_tratamiento_acuerdos_pago; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.contratos_tratamiento_acuerdos_pago ENABLE ROW LEVEL SECURITY;

--
-- Name: contratos_tratamiento_acuerdos_pago contratos_tratamiento_acuerdos_pago_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY contratos_tratamiento_acuerdos_pago_tenant ON consultorio.contratos_tratamiento_acuerdos_pago USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: contratos_tratamiento_modalidades_pago; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.contratos_tratamiento_modalidades_pago ENABLE ROW LEVEL SECURITY;

--
-- Name: contratos_tratamiento_modalidades_pago contratos_tratamiento_modalidades_pago_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY contratos_tratamiento_modalidades_pago_tenant ON consultorio.contratos_tratamiento_modalidades_pago USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: contratos_tratamiento_pagos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.contratos_tratamiento_pagos ENABLE ROW LEVEL SECURITY;

--
-- Name: contratos_tratamiento_pagos contratos_tratamiento_pagos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY contratos_tratamiento_pagos_tenant ON consultorio.contratos_tratamiento_pagos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: contratos_tratamiento_sesiones; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.contratos_tratamiento_sesiones ENABLE ROW LEVEL SECURITY;

--
-- Name: contratos_tratamiento_sesiones contratos_tratamiento_sesiones_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY contratos_tratamiento_sesiones_tenant ON consultorio.contratos_tratamiento_sesiones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: contratos_tratamiento contratos_tratamiento_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY contratos_tratamiento_tenant ON consultorio.contratos_tratamiento USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: derivaciones; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.derivaciones ENABLE ROW LEVEL SECURITY;

--
-- Name: derivaciones derivaciones_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY derivaciones_tenant ON consultorio.derivaciones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: documentos_adjuntos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.documentos_adjuntos ENABLE ROW LEVEL SECURITY;

--
-- Name: documentos_adjuntos documentos_adjuntos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY documentos_adjuntos_tenant ON consultorio.documentos_adjuntos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: empresa_perfil_clinico; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.empresa_perfil_clinico ENABLE ROW LEVEL SECURITY;

--
-- Name: empresa_perfil_clinico empresa_perfil_clinico_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY empresa_perfil_clinico_tenant ON consultorio.empresa_perfil_clinico USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: episodio_diagnosticos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.episodio_diagnosticos ENABLE ROW LEVEL SECURITY;

--
-- Name: episodio_diagnosticos episodio_diagnosticos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY episodio_diagnosticos_tenant ON consultorio.episodio_diagnosticos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: episodio_procedimientos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.episodio_procedimientos ENABLE ROW LEVEL SECURITY;

--
-- Name: episodio_procedimientos_insumos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.episodio_procedimientos_insumos ENABLE ROW LEVEL SECURITY;

--
-- Name: episodio_procedimientos_insumos episodio_procedimientos_insumos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY episodio_procedimientos_insumos_tenant ON consultorio.episodio_procedimientos_insumos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: episodio_procedimientos episodio_procedimientos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY episodio_procedimientos_tenant ON consultorio.episodio_procedimientos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: episodios; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.episodios ENABLE ROW LEVEL SECURITY;

--
-- Name: episodios episodios_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY episodios_tenant ON consultorio.episodios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: fichas_clinicas; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.fichas_clinicas ENABLE ROW LEVEL SECURITY;

--
-- Name: fichas_clinicas fichas_clinicas_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY fichas_clinicas_tenant ON consultorio.fichas_clinicas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: fichas_psicologia; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.fichas_psicologia ENABLE ROW LEVEL SECURITY;

--
-- Name: fichas_psicologia fichas_psicologia_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY fichas_psicologia_tenant ON consultorio.fichas_psicologia USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: formularios_definicion; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.formularios_definicion ENABLE ROW LEVEL SECURITY;

--
-- Name: formularios_definicion formularios_definicion_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY formularios_definicion_tenant ON consultorio.formularios_definicion USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: indicaciones_no_farmacologicas; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.indicaciones_no_farmacologicas ENABLE ROW LEVEL SECURITY;

--
-- Name: indicaciones_no_farmacologicas indicaciones_no_farmacologicas_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY indicaciones_no_farmacologicas_tenant ON consultorio.indicaciones_no_farmacologicas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: insumos_empresa; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.insumos_empresa ENABLE ROW LEVEL SECURITY;

--
-- Name: insumos_empresa insumos_empresa_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY insumos_empresa_tenant ON consultorio.insumos_empresa USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: justificativos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.justificativos ENABLE ROW LEVEL SECURITY;

--
-- Name: justificativos justificativos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY justificativos_tenant ON consultorio.justificativos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: medicamentos_empresa; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.medicamentos_empresa ENABLE ROW LEVEL SECURITY;

--
-- Name: medicamentos_empresa medicamentos_empresa_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY medicamentos_empresa_tenant ON consultorio.medicamentos_empresa USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notas_evolucion; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.notas_evolucion ENABLE ROW LEVEL SECURITY;

--
-- Name: notas_evolucion notas_evolucion_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY notas_evolucion_tenant ON consultorio.notas_evolucion USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: ordenes_analisis; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.ordenes_analisis ENABLE ROW LEVEL SECURITY;

--
-- Name: ordenes_analisis_detalle; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.ordenes_analisis_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: ordenes_analisis_detalle ordenes_analisis_detalle_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY ordenes_analisis_detalle_tenant ON consultorio.ordenes_analisis_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: ordenes_analisis ordenes_analisis_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY ordenes_analisis_tenant ON consultorio.ordenes_analisis USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: ordenes_estudios; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.ordenes_estudios ENABLE ROW LEVEL SECURITY;

--
-- Name: ordenes_estudios_detalle; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.ordenes_estudios_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: ordenes_estudios_detalle ordenes_estudios_detalle_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY ordenes_estudios_detalle_tenant ON consultorio.ordenes_estudios_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: ordenes_estudios ordenes_estudios_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY ordenes_estudios_tenant ON consultorio.ordenes_estudios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: paciente_tokens; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.paciente_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: paciente_tokens paciente_tokens_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY paciente_tokens_tenant ON consultorio.paciente_tokens USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_calendario_eventos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_calendario_eventos ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_calendario_eventos pei_calendario_eventos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_calendario_eventos_tenant ON consultorio.pei_calendario_eventos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_estrategias; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_estrategias ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_estrategias pei_estrategias_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_estrategias_tenant ON consultorio.pei_estrategias USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_habilidades_entrenamiento; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_habilidades_entrenamiento ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_habilidades_entrenamiento pei_habilidades_entrenamiento_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_habilidades_entrenamiento_tenant ON consultorio.pei_habilidades_entrenamiento USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_objetivos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_objetivos ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_objetivos pei_objetivos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_objetivos_tenant ON consultorio.pei_objetivos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_registro_mensual; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_registro_mensual ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_registro_mensual pei_registro_mensual_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_registro_mensual_tenant ON consultorio.pei_registro_mensual USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_reunion_clinica; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_reunion_clinica ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_reunion_clinica pei_reunion_clinica_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_reunion_clinica_tenant ON consultorio.pei_reunion_clinica USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_reunion_participantes; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_reunion_participantes ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_reunion_participantes pei_reunion_participantes_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_reunion_participantes_tenant ON consultorio.pei_reunion_participantes USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_reunion_recomendaciones; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_reunion_recomendaciones ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_reunion_recomendaciones pei_reunion_recomendaciones_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_reunion_recomendaciones_tenant ON consultorio.pei_reunion_recomendaciones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_sesion_actividades; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_sesion_actividades ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_sesion_actividades pei_sesion_actividades_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_sesion_actividades_tenant ON consultorio.pei_sesion_actividades USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei_sesion_planificada; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.pei_sesion_planificada ENABLE ROW LEVEL SECURITY;

--
-- Name: pei_sesion_planificada pei_sesion_planificada_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_sesion_planificada_tenant ON consultorio.pei_sesion_planificada USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pei pei_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY pei_tenant ON consultorio.pei USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: planes_tratamiento; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.planes_tratamiento ENABLE ROW LEVEL SECURITY;

--
-- Name: planes_tratamiento_items; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.planes_tratamiento_items ENABLE ROW LEVEL SECURITY;

--
-- Name: planes_tratamiento_items planes_tratamiento_items_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY planes_tratamiento_items_tenant ON consultorio.planes_tratamiento_items USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: planes_tratamiento planes_tratamiento_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY planes_tratamiento_tenant ON consultorio.planes_tratamiento USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: plantillas_justificativos; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.plantillas_justificativos ENABLE ROW LEVEL SECURITY;

--
-- Name: plantillas_justificativos plantillas_justificativos_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY plantillas_justificativos_tenant ON consultorio.plantillas_justificativos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: procedimientos_empresa; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.procedimientos_empresa ENABLE ROW LEVEL SECURITY;

--
-- Name: procedimientos_empresa procedimientos_empresa_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY procedimientos_empresa_tenant ON consultorio.procedimientos_empresa USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: psicologia_perfil_empresa; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.psicologia_perfil_empresa ENABLE ROW LEVEL SECURITY;

--
-- Name: psicologia_perfil_empresa psicologia_perfil_empresa_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY psicologia_perfil_empresa_tenant ON consultorio.psicologia_perfil_empresa USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: recetas; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.recetas ENABLE ROW LEVEL SECURITY;

--
-- Name: recetas_detalle; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.recetas_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: recetas_detalle recetas_detalle_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY recetas_detalle_tenant ON consultorio.recetas_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: recetas recetas_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY recetas_tenant ON consultorio.recetas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: resultados_analisis; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.resultados_analisis ENABLE ROW LEVEL SECURITY;

--
-- Name: resultados_analisis_detalle; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.resultados_analisis_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: resultados_analisis_detalle resultados_analisis_detalle_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY resultados_analisis_detalle_tenant ON consultorio.resultados_analisis_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: resultados_analisis resultados_analisis_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY resultados_analisis_tenant ON consultorio.resultados_analisis USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: signos_vitales; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.signos_vitales ENABLE ROW LEVEL SECURITY;

--
-- Name: signos_vitales_detalle; Type: ROW SECURITY; Schema: consultorio; Owner: postgres
--

ALTER TABLE consultorio.signos_vitales_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: signos_vitales_detalle signos_vitales_detalle_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY signos_vitales_detalle_tenant ON consultorio.signos_vitales_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: signos_vitales signos_vitales_tenant; Type: POLICY; Schema: consultorio; Owner: postgres
--

CREATE POLICY signos_vitales_tenant ON consultorio.signos_vitales USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: agenda_horarios; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.agenda_horarios ENABLE ROW LEVEL SECURITY;

--
-- Name: agenda_horarios_excepciones; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.agenda_horarios_excepciones ENABLE ROW LEVEL SECURITY;

--
-- Name: agenda_horarios_excepciones agenda_horarios_excepciones_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY agenda_horarios_excepciones_tenant ON core.agenda_horarios_excepciones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: agenda_horarios agenda_horarios_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY agenda_horarios_tenant ON core.agenda_horarios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: auditoria_sistema; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.auditoria_sistema ENABLE ROW LEVEL SECURITY;

--
-- Name: auditoria_sistema auditoria_sistema_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY auditoria_sistema_tenant ON core.auditoria_sistema USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: auditoria_sistema_y2026; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.auditoria_sistema_y2026 ENABLE ROW LEVEL SECURITY;

--
-- Name: auditoria_sistema_y2026 auditoria_sistema_y2026_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY auditoria_sistema_y2026_tenant ON core.auditoria_sistema_y2026 USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: auditoria_sistema_y2027; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.auditoria_sistema_y2027 ENABLE ROW LEVEL SECURITY;

--
-- Name: auditoria_sistema_y2027 auditoria_sistema_y2027_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY auditoria_sistema_y2027_tenant ON core.auditoria_sistema_y2027 USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: auditoria_sistema_y2028; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.auditoria_sistema_y2028 ENABLE ROW LEVEL SECURITY;

--
-- Name: auditoria_sistema_y2028 auditoria_sistema_y2028_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY auditoria_sistema_y2028_tenant ON core.auditoria_sistema_y2028 USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cargos; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.cargos ENABLE ROW LEVEL SECURITY;

--
-- Name: cargos cargos_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY cargos_tenant ON core.cargos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: citas; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.citas ENABLE ROW LEVEL SECURITY;

--
-- Name: citas_log_estados; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.citas_log_estados ENABLE ROW LEVEL SECURITY;

--
-- Name: citas_log_estados citas_log_estados_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY citas_log_estados_tenant ON core.citas_log_estados USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: citas citas_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY citas_tenant ON core.citas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: consultorios; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.consultorios ENABLE ROW LEVEL SECURITY;

--
-- Name: consultorios consultorios_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY consultorios_tenant ON core.consultorios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: empresa_certificados; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.empresa_certificados ENABLE ROW LEVEL SECURITY;

--
-- Name: empresa_certificados empresa_certificados_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY empresa_certificados_tenant ON core.empresa_certificados USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: empresa_configuracion; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.empresa_configuracion ENABLE ROW LEVEL SECURITY;

--
-- Name: empresa_configuracion empresa_configuracion_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY empresa_configuracion_tenant ON core.empresa_configuracion USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: empresa_modulos; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.empresa_modulos ENABLE ROW LEVEL SECURITY;

--
-- Name: empresa_modulos empresa_modulos_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY empresa_modulos_tenant ON core.empresa_modulos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: empresas; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.empresas ENABLE ROW LEVEL SECURITY;

--
-- Name: empresas empresas_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY empresas_tenant ON core.empresas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: especialidades; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.especialidades ENABLE ROW LEVEL SECURITY;

--
-- Name: especialidades especialidades_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY especialidades_tenant ON core.especialidades USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: especialista_especialidades; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.especialista_especialidades ENABLE ROW LEVEL SECURITY;

--
-- Name: especialista_especialidades especialista_especialidades_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY especialista_especialidades_tenant ON core.especialista_especialidades USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: especialistas; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.especialistas ENABLE ROW LEVEL SECURITY;

--
-- Name: especialistas especialistas_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY especialistas_tenant ON core.especialistas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: establecimientos; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.establecimientos ENABLE ROW LEVEL SECURITY;

--
-- Name: establecimientos establecimientos_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY establecimientos_tenant ON core.establecimientos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: estados_citas; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.estados_citas ENABLE ROW LEVEL SECURITY;

--
-- Name: estados_citas estados_citas_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY estados_citas_tenant ON core.estados_citas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: feriados; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.feriados ENABLE ROW LEVEL SECURITY;

--
-- Name: feriados feriados_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY feriados_tenant ON core.feriados USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: funcionarios; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.funcionarios ENABLE ROW LEVEL SECURITY;

--
-- Name: funcionarios funcionarios_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY funcionarios_tenant ON core.funcionarios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: historial_suscripciones; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.historial_suscripciones ENABLE ROW LEVEL SECURITY;

--
-- Name: historial_suscripciones historial_suscripciones_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY historial_suscripciones_tenant ON core.historial_suscripciones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: licencias; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.licencias ENABLE ROW LEVEL SECURITY;

--
-- Name: licencias licencias_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY licencias_tenant ON core.licencias USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: lista_espera; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.lista_espera ENABLE ROW LEVEL SECURITY;

--
-- Name: lista_espera lista_espera_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY lista_espera_tenant ON core.lista_espera USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: login_attempts; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.login_attempts ENABLE ROW LEVEL SECURITY;

--
-- Name: login_attempts login_attempts_system_insert; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY login_attempts_system_insert ON core.login_attempts FOR INSERT WITH CHECK (true);


--
-- Name: login_attempts login_attempts_tenant_select; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY login_attempts_tenant_select ON core.login_attempts FOR SELECT USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: metricas_diarias; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.metricas_diarias ENABLE ROW LEVEL SECURITY;

--
-- Name: metricas_diarias metricas_diarias_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY metricas_diarias_tenant ON core.metricas_diarias USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notificaciones_cola; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.notificaciones_cola ENABLE ROW LEVEL SECURITY;

--
-- Name: notificaciones_cola notificaciones_cola_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY notificaciones_cola_tenant ON core.notificaciones_cola USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notificaciones_config; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.notificaciones_config ENABLE ROW LEVEL SECURITY;

--
-- Name: notificaciones_config notificaciones_config_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY notificaciones_config_tenant ON core.notificaciones_config USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notificaciones_log; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.notificaciones_log ENABLE ROW LEVEL SECURITY;

--
-- Name: notificaciones_log notificaciones_log_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY notificaciones_log_tenant ON core.notificaciones_log USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notificaciones_plantillas; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.notificaciones_plantillas ENABLE ROW LEVEL SECURITY;

--
-- Name: notificaciones_plantillas notificaciones_plantillas_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY notificaciones_plantillas_tenant ON core.notificaciones_plantillas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: paciente_profesional; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.paciente_profesional ENABLE ROW LEVEL SECURITY;

--
-- Name: paciente_profesional paciente_profesional_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY paciente_profesional_tenant ON core.paciente_profesional USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pacientes; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.pacientes ENABLE ROW LEVEL SECURITY;

--
-- Name: pacientes_menores; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.pacientes_menores ENABLE ROW LEVEL SECURITY;

--
-- Name: pacientes_menores pacientes_menores_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY pacientes_menores_tenant ON core.pacientes_menores USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: pacientes pacientes_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY pacientes_tenant ON core.pacientes USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: personas; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.personas ENABLE ROW LEVEL SECURITY;

--
-- Name: personas personas_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY personas_tenant ON core.personas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: preferencias_ui; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.preferencias_ui ENABLE ROW LEVEL SECURITY;

--
-- Name: preferencias_ui preferencias_ui_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY preferencias_ui_tenant ON core.preferencias_ui USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: puntos_expedicion; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.puntos_expedicion ENABLE ROW LEVEL SECURITY;

--
-- Name: puntos_expedicion puntos_expedicion_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY puntos_expedicion_tenant ON core.puntos_expedicion USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: recordatorios; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.recordatorios ENABLE ROW LEVEL SECURITY;

--
-- Name: recordatorios recordatorios_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY recordatorios_tenant ON core.recordatorios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: reportes_jobs; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.reportes_jobs ENABLE ROW LEVEL SECURITY;

--
-- Name: reportes_jobs_log; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.reportes_jobs_log ENABLE ROW LEVEL SECURITY;

--
-- Name: reportes_jobs_log reportes_jobs_log_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY reportes_jobs_log_tenant ON core.reportes_jobs_log USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: reportes_jobs reportes_jobs_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY reportes_jobs_tenant ON core.reportes_jobs USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: roles_empresa; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.roles_empresa ENABLE ROW LEVEL SECURITY;

--
-- Name: roles_empresa_permisos; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.roles_empresa_permisos ENABLE ROW LEVEL SECURITY;

--
-- Name: roles_empresa_permisos roles_empresa_permisos_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY roles_empresa_permisos_tenant ON core.roles_empresa_permisos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: roles_empresa roles_empresa_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY roles_empresa_tenant ON core.roles_empresa USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: sedes; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.sedes ENABLE ROW LEVEL SECURITY;

--
-- Name: sedes sedes_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY sedes_tenant ON core.sedes USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: sesiones; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.sesiones ENABLE ROW LEVEL SECURITY;

--
-- Name: sesiones sesiones_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY sesiones_tenant ON core.sesiones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: slots_agenda; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.slots_agenda ENABLE ROW LEVEL SECURITY;

--
-- Name: slots_agenda slots_agenda_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY slots_agenda_tenant ON core.slots_agenda USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: suscripcion_excedentes; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.suscripcion_excedentes ENABLE ROW LEVEL SECURITY;

--
-- Name: suscripcion_excedentes suscripcion_excedentes_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY suscripcion_excedentes_tenant ON core.suscripcion_excedentes USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: suscripciones; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.suscripciones ENABLE ROW LEVEL SECURITY;

--
-- Name: suscripciones suscripciones_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY suscripciones_tenant ON core.suscripciones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: usuarios; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.usuarios ENABLE ROW LEVEL SECURITY;

--
-- Name: usuarios_roles_empresa; Type: ROW SECURITY; Schema: core; Owner: postgres
--

ALTER TABLE core.usuarios_roles_empresa ENABLE ROW LEVEL SECURITY;

--
-- Name: usuarios_roles_empresa usuarios_roles_empresa_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY usuarios_roles_empresa_tenant ON core.usuarios_roles_empresa USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: usuarios usuarios_tenant; Type: POLICY; Schema: core; Owner: postgres
--

CREATE POLICY usuarios_tenant ON core.usuarios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: aperturas_caja; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.aperturas_caja ENABLE ROW LEVEL SECURITY;

--
-- Name: aperturas_caja aperturas_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY aperturas_tenant ON facturacion.aperturas_caja USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: arqueos_caja; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.arqueos_caja ENABLE ROW LEVEL SECURITY;

--
-- Name: arqueos_caja arqueos_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY arqueos_tenant ON facturacion.arqueos_caja USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: autofactura_detalle; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.autofactura_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: autofactura_detalle autofactura_detalle_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY autofactura_detalle_tenant ON facturacion.autofactura_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: autofacturas; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.autofacturas ENABLE ROW LEVEL SECURITY;

--
-- Name: autofacturas autofacturas_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY autofacturas_tenant ON facturacion.autofacturas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cajas; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.cajas ENABLE ROW LEVEL SECURITY;

--
-- Name: cajas cajas_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY cajas_tenant ON facturacion.cajas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: categorias_items; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.categorias_items ENABLE ROW LEVEL SECURITY;

--
-- Name: categorias_items categorias_items_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY categorias_items_tenant ON facturacion.categorias_items USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cheques_recibidos; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.cheques_recibidos ENABLE ROW LEVEL SECURITY;

--
-- Name: cheques_recibidos cheques_recibidos_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY cheques_recibidos_tenant ON facturacion.cheques_recibidos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cobranza_detalle; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.cobranza_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: cobranza_detalle cobranza_detalle_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY cobranza_detalle_tenant ON facturacion.cobranza_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cobranzas; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.cobranzas ENABLE ROW LEVEL SECURITY;

--
-- Name: cobranzas cobranzas_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY cobranzas_tenant ON facturacion.cobranzas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cuentas_cobrar; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.cuentas_cobrar ENABLE ROW LEVEL SECURITY;

--
-- Name: cuentas_cobrar cuentas_cobrar_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY cuentas_cobrar_tenant ON facturacion.cuentas_cobrar USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: cuotas_cobrar; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.cuotas_cobrar ENABLE ROW LEVEL SECURITY;

--
-- Name: cuotas_cobrar cuotas_cobrar_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY cuotas_cobrar_tenant ON facturacion.cuotas_cobrar USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: documentos_electronicos; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.documentos_electronicos ENABLE ROW LEVEL SECURITY;

--
-- Name: documentos_electronicos documentos_electronicos_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY documentos_electronicos_tenant ON facturacion.documentos_electronicos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: entidades_pagadoras; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.entidades_pagadoras ENABLE ROW LEVEL SECURITY;

--
-- Name: entidades_pagadoras entidades_pagadoras_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY entidades_pagadoras_tenant ON facturacion.entidades_pagadoras USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: factura_detalle; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.factura_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: factura_detalle factura_detalle_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY factura_detalle_tenant ON facturacion.factura_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: factura_medios_pago; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.factura_medios_pago ENABLE ROW LEVEL SECURITY;

--
-- Name: factura_medios_pago factura_medios_pago_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY factura_medios_pago_tenant ON facturacion.factura_medios_pago USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: facturas; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.facturas ENABLE ROW LEVEL SECURITY;

--
-- Name: facturas facturas_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY facturas_tenant ON facturacion.facturas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: items; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.items ENABLE ROW LEVEL SECURITY;

--
-- Name: items items_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY items_tenant ON facturacion.items USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: libro_ventas; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.libro_ventas ENABLE ROW LEVEL SECURITY;

--
-- Name: libro_ventas libro_ventas_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY libro_ventas_tenant ON facturacion.libro_ventas USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: movimientos_caja mov_caja_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY mov_caja_tenant ON facturacion.movimientos_caja USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: movimientos_caja; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.movimientos_caja ENABLE ROW LEVEL SECURITY;

--
-- Name: nota_credito_detalle; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.nota_credito_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: nota_credito_detalle nota_credito_detalle_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY nota_credito_detalle_tenant ON facturacion.nota_credito_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: nota_debito_detalle; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.nota_debito_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: nota_debito_detalle nota_debito_detalle_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY nota_debito_detalle_tenant ON facturacion.nota_debito_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: nota_remision_detalle; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.nota_remision_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: nota_remision_detalle nota_remision_detalle_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY nota_remision_detalle_tenant ON facturacion.nota_remision_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notas_credito; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.notas_credito ENABLE ROW LEVEL SECURITY;

--
-- Name: notas_credito notas_credito_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY notas_credito_tenant ON facturacion.notas_credito USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notas_debito; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.notas_debito ENABLE ROW LEVEL SECURITY;

--
-- Name: notas_debito notas_debito_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY notas_debito_tenant ON facturacion.notas_debito USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: notas_remision; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.notas_remision ENABLE ROW LEVEL SECURITY;

--
-- Name: notas_remision notas_remision_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY notas_remision_tenant ON facturacion.notas_remision USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: recaudacion_detalle; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.recaudacion_detalle ENABLE ROW LEVEL SECURITY;

--
-- Name: recaudacion_detalle recaudacion_detalle_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY recaudacion_detalle_tenant ON facturacion.recaudacion_detalle USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: recaudaciones; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.recaudaciones ENABLE ROW LEVEL SECURITY;

--
-- Name: recaudaciones recaudaciones_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY recaudaciones_tenant ON facturacion.recaudaciones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: secuencias_numeracion; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.secuencias_numeracion ENABLE ROW LEVEL SECURITY;

--
-- Name: secuencias_numeracion secuencias_numeracion_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY secuencias_numeracion_tenant ON facturacion.secuencias_numeracion USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: sifen_config; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.sifen_config ENABLE ROW LEVEL SECURITY;

--
-- Name: sifen_config sifen_config_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY sifen_config_tenant ON facturacion.sifen_config USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: sifen_eventos; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.sifen_eventos ENABLE ROW LEVEL SECURITY;

--
-- Name: sifen_eventos sifen_eventos_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY sifen_eventos_tenant ON facturacion.sifen_eventos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: sifen_lote_documentos; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.sifen_lote_documentos ENABLE ROW LEVEL SECURITY;

--
-- Name: sifen_lote_documentos sifen_lote_documentos_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY sifen_lote_documentos_tenant ON facturacion.sifen_lote_documentos USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: sifen_lotes; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.sifen_lotes ENABLE ROW LEVEL SECURITY;

--
-- Name: sifen_lotes sifen_lotes_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY sifen_lotes_tenant ON facturacion.sifen_lotes USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: sifen_transmision_log; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.sifen_transmision_log ENABLE ROW LEVEL SECURITY;

--
-- Name: sifen_transmision_log sifen_transmision_log_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY sifen_transmision_log_tenant ON facturacion.sifen_transmision_log USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: tarifario_precios; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.tarifario_precios ENABLE ROW LEVEL SECURITY;

--
-- Name: tarifario_precios tarifario_precios_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY tarifario_precios_tenant ON facturacion.tarifario_precios USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: timbrado_habilitaciones; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.timbrado_habilitaciones ENABLE ROW LEVEL SECURITY;

--
-- Name: timbrado_habilitaciones timbrado_habilitaciones_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY timbrado_habilitaciones_tenant ON facturacion.timbrado_habilitaciones USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: timbrados; Type: ROW SECURITY; Schema: facturacion; Owner: postgres
--

ALTER TABLE facturacion.timbrados ENABLE ROW LEVEL SECURITY;

--
-- Name: timbrados timbrados_tenant; Type: POLICY; Schema: facturacion; Owner: postgres
--

CREATE POLICY timbrados_tenant ON facturacion.timbrados USING (public.fn_rls_tenant_match((id_empresa)::bigint));


--
-- Name: SCHEMA consultorio; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA consultorio TO angasys_user;


--
-- Name: SCHEMA core; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA core TO angasys_user;


--
-- Name: SCHEMA facturacion; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA facturacion TO angasys_user;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO angasys_user;


--
-- Name: FUNCTION fn_next_nro_contrato(p_id_empresa integer); Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT ALL ON FUNCTION consultorio.fn_next_nro_contrato(p_id_empresa integer) TO angasys_user;


--
-- Name: FUNCTION fn_next_nro_documento(p_id_empresa integer, p_tipo_doc text); Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT ALL ON FUNCTION consultorio.fn_next_nro_documento(p_id_empresa integer, p_tipo_doc text) TO angasys_user;


--
-- Name: FUNCTION fn_next_nro_episodio(p_id_empresa integer); Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT ALL ON FUNCTION consultorio.fn_next_nro_episodio(p_id_empresa integer) TO angasys_user;


--
-- Name: FUNCTION fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text); Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT ALL ON FUNCTION consultorio.fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text) TO angasys_user;


--
-- Name: FUNCTION fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text); Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT ALL ON FUNCTION consultorio.fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text) TO angasys_user;


--
-- Name: FUNCTION fn_check_limite_sedes(); Type: ACL; Schema: core; Owner: postgres
--

GRANT ALL ON FUNCTION core.fn_check_limite_sedes() TO angasys_user;


--
-- Name: FUNCTION fn_next_nro_de(p_id_empresa integer, p_id_timbrado integer, p_cod_establecimiento character, p_cod_punto_expedicion character, p_cod_tipo_de character, p_cod_serie character); Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT ALL ON FUNCTION facturacion.fn_next_nro_de(p_id_empresa integer, p_id_timbrado integer, p_cod_establecimiento character, p_cod_punto_expedicion character, p_cod_tipo_de character, p_cod_serie character) TO angasys_user;


--
-- Name: FUNCTION app_current_tenant_id(); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.app_current_tenant_id() TO angasys_user;


--
-- Name: FUNCTION app_current_user_id(); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.app_current_user_id() TO angasys_user;


--
-- Name: FUNCTION app_is_super_admin(); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.app_is_super_admin() TO angasys_user;


--
-- Name: FUNCTION fn_rls_tenant_match(p_id_empresa bigint); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.fn_rls_tenant_match(p_id_empresa bigint) TO angasys_user;


--
-- Name: FUNCTION fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.fn_seed_antecedentes_por_tipo(p_id_empresa integer, p_cod_tipo text) TO angasys_user;


--
-- Name: FUNCTION fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.fn_seed_consultorio_por_tipo(p_id_empresa integer, p_cod_tipo text) TO angasys_user;


--
-- Name: FUNCTION fn_set_fec_modificacion(); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.fn_set_fec_modificacion() TO angasys_user;


--
-- Name: TABLE acuerdo_monto_historial; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.acuerdo_monto_historial TO angasys_user;


--
-- Name: SEQUENCE acuerdo_monto_historial_id_acuerdo_monto_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.acuerdo_monto_historial_id_acuerdo_monto_seq TO angasys_user;


--
-- Name: TABLE acuerdos_terapeuticos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.acuerdos_terapeuticos TO angasys_user;


--
-- Name: SEQUENCE acuerdos_terapeuticos_id_acuerdo_terapeutico_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.acuerdos_terapeuticos_id_acuerdo_terapeutico_seq TO angasys_user;


--
-- Name: TABLE anamnesis; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.anamnesis TO angasys_user;


--
-- Name: TABLE anamnesis_adulto_ext; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.anamnesis_adulto_ext TO angasys_user;


--
-- Name: SEQUENCE anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.anamnesis_adulto_ext_id_anamnesis_adulto_ext_seq TO angasys_user;


--
-- Name: SEQUENCE anamnesis_id_anamnesis_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.anamnesis_id_anamnesis_seq TO angasys_user;


--
-- Name: TABLE anamnesis_infantil_ext; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.anamnesis_infantil_ext TO angasys_user;


--
-- Name: SEQUENCE anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.anamnesis_infantil_ext_id_anamnesis_infantil_ext_seq TO angasys_user;


--
-- Name: TABLE antecedentes_paciente; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.antecedentes_paciente TO angasys_user;


--
-- Name: SEQUENCE antecedentes_paciente_id_antecedente_paciente_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.antecedentes_paciente_id_antecedente_paciente_seq TO angasys_user;


--
-- Name: TABLE cobros_simples; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.cobros_simples TO angasys_user;


--
-- Name: SEQUENCE cobros_simples_id_cobro_simple_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.cobros_simples_id_cobro_simple_seq TO angasys_user;


--
-- Name: TABLE consentimientos_firmados; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.consentimientos_firmados TO angasys_user;


--
-- Name: SEQUENCE consentimientos_firmados_id_consentimiento_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.consentimientos_firmados_id_consentimiento_seq TO angasys_user;


--
-- Name: TABLE contratos_tratamiento; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.contratos_tratamiento TO angasys_user;


--
-- Name: TABLE contratos_tratamiento_acuerdos_pago; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.contratos_tratamiento_acuerdos_pago TO angasys_user;


--
-- Name: SEQUENCE contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.contratos_tratamiento_acuerdos_pago_id_acuerdo_pago_seq TO angasys_user;


--
-- Name: SEQUENCE contratos_tratamiento_id_contrato_tratamiento_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.contratos_tratamiento_id_contrato_tratamiento_seq TO angasys_user;


--
-- Name: TABLE contratos_tratamiento_modalidades_pago; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.contratos_tratamiento_modalidades_pago TO angasys_user;


--
-- Name: SEQUENCE contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.contratos_tratamiento_modalidades_pago_id_modalidad_pago_seq TO angasys_user;


--
-- Name: TABLE contratos_tratamiento_pagos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.contratos_tratamiento_pagos TO angasys_user;


--
-- Name: SEQUENCE contratos_tratamiento_pagos_id_pago_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.contratos_tratamiento_pagos_id_pago_seq TO angasys_user;


--
-- Name: TABLE contratos_tratamiento_sesiones; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.contratos_tratamiento_sesiones TO angasys_user;


--
-- Name: SEQUENCE contratos_tratamiento_sesiones_id_contrato_sesion_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.contratos_tratamiento_sesiones_id_contrato_sesion_seq TO angasys_user;


--
-- Name: TABLE derivaciones; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.derivaciones TO angasys_user;


--
-- Name: SEQUENCE derivaciones_id_derivacion_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.derivaciones_id_derivacion_seq TO angasys_user;


--
-- Name: TABLE diagnosticos_cie10; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.diagnosticos_cie10 TO angasys_user;


--
-- Name: TABLE diagnosticos_cie10_dsm5_equivalencias; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.diagnosticos_cie10_dsm5_equivalencias TO angasys_user;


--
-- Name: SEQUENCE diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.diagnosticos_cie10_dsm5_equivalencias_id_equivalencia_seq TO angasys_user;


--
-- Name: SEQUENCE diagnosticos_cie10_id_diagnostico_cie10_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.diagnosticos_cie10_id_diagnostico_cie10_seq TO angasys_user;


--
-- Name: TABLE diagnosticos_dsm5; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.diagnosticos_dsm5 TO angasys_user;


--
-- Name: SEQUENCE diagnosticos_dsm5_id_diagnostico_dsm5_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.diagnosticos_dsm5_id_diagnostico_dsm5_seq TO angasys_user;


--
-- Name: TABLE documentos_adjuntos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.documentos_adjuntos TO angasys_user;


--
-- Name: SEQUENCE documentos_adjuntos_id_documento_adjunto_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.documentos_adjuntos_id_documento_adjunto_seq TO angasys_user;


--
-- Name: TABLE empresa_perfil_clinico; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.empresa_perfil_clinico TO angasys_user;


--
-- Name: SEQUENCE empresa_perfil_clinico_id_empresa_perfil_clinico_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.empresa_perfil_clinico_id_empresa_perfil_clinico_seq TO angasys_user;


--
-- Name: TABLE episodio_diagnosticos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.episodio_diagnosticos TO angasys_user;


--
-- Name: SEQUENCE episodio_diagnosticos_id_episodio_diagnostico_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.episodio_diagnosticos_id_episodio_diagnostico_seq TO angasys_user;


--
-- Name: TABLE episodio_procedimientos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.episodio_procedimientos TO angasys_user;


--
-- Name: SEQUENCE episodio_procedimientos_id_episodio_procedimiento_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.episodio_procedimientos_id_episodio_procedimiento_seq TO angasys_user;


--
-- Name: TABLE episodio_procedimientos_insumos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.episodio_procedimientos_insumos TO angasys_user;


--
-- Name: SEQUENCE episodio_procedimientos_insumos_id_ep_insumo_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.episodio_procedimientos_insumos_id_ep_insumo_seq TO angasys_user;


--
-- Name: TABLE episodios; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.episodios TO angasys_user;


--
-- Name: SEQUENCE episodios_id_episodio_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.episodios_id_episodio_seq TO angasys_user;


--
-- Name: TABLE fichas_clinicas; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.fichas_clinicas TO angasys_user;


--
-- Name: SEQUENCE fichas_clinicas_id_ficha_clinica_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.fichas_clinicas_id_ficha_clinica_seq TO angasys_user;


--
-- Name: TABLE fichas_psicologia; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.fichas_psicologia TO angasys_user;


--
-- Name: SEQUENCE fichas_psicologia_id_ficha_psicologia_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.fichas_psicologia_id_ficha_psicologia_seq TO angasys_user;


--
-- Name: TABLE formularios_definicion; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.formularios_definicion TO angasys_user;


--
-- Name: SEQUENCE formularios_definicion_id_formulario_definicion_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.formularios_definicion_id_formulario_definicion_seq TO angasys_user;


--
-- Name: TABLE indicaciones_no_farmacologicas; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.indicaciones_no_farmacologicas TO angasys_user;


--
-- Name: SEQUENCE indicaciones_no_farmacologicas_id_indicacion_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.indicaciones_no_farmacologicas_id_indicacion_seq TO angasys_user;


--
-- Name: TABLE insumos_empresa; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.insumos_empresa TO angasys_user;


--
-- Name: SEQUENCE insumos_empresa_id_insumo_empresa_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.insumos_empresa_id_insumo_empresa_seq TO angasys_user;


--
-- Name: TABLE justificativos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.justificativos TO angasys_user;


--
-- Name: SEQUENCE justificativos_id_justificativo_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.justificativos_id_justificativo_seq TO angasys_user;


--
-- Name: TABLE medicamentos_empresa; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.medicamentos_empresa TO angasys_user;


--
-- Name: SEQUENCE medicamentos_empresa_id_medicamento_empresa_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.medicamentos_empresa_id_medicamento_empresa_seq TO angasys_user;


--
-- Name: TABLE notas_evolucion; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.notas_evolucion TO angasys_user;


--
-- Name: SEQUENCE notas_evolucion_id_nota_evolucion_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.notas_evolucion_id_nota_evolucion_seq TO angasys_user;


--
-- Name: TABLE ordenes_analisis; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.ordenes_analisis TO angasys_user;


--
-- Name: TABLE ordenes_analisis_detalle; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.ordenes_analisis_detalle TO angasys_user;


--
-- Name: SEQUENCE ordenes_analisis_detalle_id_orden_analisis_detalle_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.ordenes_analisis_detalle_id_orden_analisis_detalle_seq TO angasys_user;


--
-- Name: SEQUENCE ordenes_analisis_id_orden_analisis_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.ordenes_analisis_id_orden_analisis_seq TO angasys_user;


--
-- Name: TABLE ordenes_estudios; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.ordenes_estudios TO angasys_user;


--
-- Name: TABLE ordenes_estudios_detalle; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.ordenes_estudios_detalle TO angasys_user;


--
-- Name: SEQUENCE ordenes_estudios_detalle_id_orden_estudios_detalle_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.ordenes_estudios_detalle_id_orden_estudios_detalle_seq TO angasys_user;


--
-- Name: SEQUENCE ordenes_estudios_id_orden_estudios_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.ordenes_estudios_id_orden_estudios_seq TO angasys_user;


--
-- Name: TABLE paciente_tokens; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.paciente_tokens TO angasys_user;


--
-- Name: SEQUENCE paciente_tokens_id_paciente_token_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.paciente_tokens_id_paciente_token_seq TO angasys_user;


--
-- Name: TABLE pei; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei TO angasys_user;


--
-- Name: TABLE pei_calendario_eventos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_calendario_eventos TO angasys_user;


--
-- Name: SEQUENCE pei_calendario_eventos_id_pei_calendario_evento_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_calendario_eventos_id_pei_calendario_evento_seq TO angasys_user;


--
-- Name: TABLE pei_estrategias; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_estrategias TO angasys_user;


--
-- Name: SEQUENCE pei_estrategias_id_pei_estrategia_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_estrategias_id_pei_estrategia_seq TO angasys_user;


--
-- Name: TABLE pei_habilidades_entrenamiento; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_habilidades_entrenamiento TO angasys_user;


--
-- Name: SEQUENCE pei_habilidades_entrenamiento_id_pei_habilidad_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_habilidades_entrenamiento_id_pei_habilidad_seq TO angasys_user;


--
-- Name: SEQUENCE pei_id_pei_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_id_pei_seq TO angasys_user;


--
-- Name: TABLE pei_objetivos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_objetivos TO angasys_user;


--
-- Name: SEQUENCE pei_objetivos_id_pei_objetivo_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_objetivos_id_pei_objetivo_seq TO angasys_user;


--
-- Name: TABLE pei_registro_mensual; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_registro_mensual TO angasys_user;


--
-- Name: SEQUENCE pei_registro_mensual_id_pei_registro_mensual_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_registro_mensual_id_pei_registro_mensual_seq TO angasys_user;


--
-- Name: TABLE pei_reunion_clinica; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_reunion_clinica TO angasys_user;


--
-- Name: SEQUENCE pei_reunion_clinica_id_pei_reunion_clinica_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_reunion_clinica_id_pei_reunion_clinica_seq TO angasys_user;


--
-- Name: TABLE pei_reunion_participantes; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_reunion_participantes TO angasys_user;


--
-- Name: SEQUENCE pei_reunion_participantes_id_pei_reunion_participante_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_reunion_participantes_id_pei_reunion_participante_seq TO angasys_user;


--
-- Name: TABLE pei_reunion_recomendaciones; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_reunion_recomendaciones TO angasys_user;


--
-- Name: SEQUENCE pei_reunion_recomendaciones_id_pei_recomendacion_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_reunion_recomendaciones_id_pei_recomendacion_seq TO angasys_user;


--
-- Name: TABLE pei_sesion_actividades; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_sesion_actividades TO angasys_user;


--
-- Name: SEQUENCE pei_sesion_actividades_id_pei_sesion_actividad_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_sesion_actividades_id_pei_sesion_actividad_seq TO angasys_user;


--
-- Name: TABLE pei_sesion_planificada; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.pei_sesion_planificada TO angasys_user;


--
-- Name: SEQUENCE pei_sesion_planificada_id_pei_sesion_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.pei_sesion_planificada_id_pei_sesion_seq TO angasys_user;


--
-- Name: TABLE planes_tratamiento; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.planes_tratamiento TO angasys_user;


--
-- Name: SEQUENCE planes_tratamiento_id_plan_tratamiento_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.planes_tratamiento_id_plan_tratamiento_seq TO angasys_user;


--
-- Name: TABLE planes_tratamiento_items; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.planes_tratamiento_items TO angasys_user;


--
-- Name: SEQUENCE planes_tratamiento_items_id_plan_tratamiento_item_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.planes_tratamiento_items_id_plan_tratamiento_item_seq TO angasys_user;


--
-- Name: TABLE plantillas_justificativos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.plantillas_justificativos TO angasys_user;


--
-- Name: SEQUENCE plantillas_justificativos_id_plantilla_justificativo_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.plantillas_justificativos_id_plantilla_justificativo_seq TO angasys_user;


--
-- Name: TABLE procedimientos_empresa; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.procedimientos_empresa TO angasys_user;


--
-- Name: SEQUENCE procedimientos_empresa_id_procedimiento_empresa_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.procedimientos_empresa_id_procedimiento_empresa_seq TO angasys_user;


--
-- Name: TABLE psicologia_perfil_empresa; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.psicologia_perfil_empresa TO angasys_user;


--
-- Name: SEQUENCE psicologia_perfil_empresa_id_psicologia_perfil_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.psicologia_perfil_empresa_id_psicologia_perfil_seq TO angasys_user;


--
-- Name: TABLE recetas; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.recetas TO angasys_user;


--
-- Name: TABLE recetas_detalle; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.recetas_detalle TO angasys_user;


--
-- Name: SEQUENCE recetas_detalle_id_receta_detalle_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.recetas_detalle_id_receta_detalle_seq TO angasys_user;


--
-- Name: SEQUENCE recetas_id_receta_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.recetas_id_receta_seq TO angasys_user;


--
-- Name: TABLE resultados_analisis; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.resultados_analisis TO angasys_user;


--
-- Name: TABLE resultados_analisis_detalle; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.resultados_analisis_detalle TO angasys_user;


--
-- Name: SEQUENCE resultados_analisis_detalle_id_resultado_analisis_det_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.resultados_analisis_detalle_id_resultado_analisis_det_seq TO angasys_user;


--
-- Name: SEQUENCE resultados_analisis_id_resultado_analisis_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.resultados_analisis_id_resultado_analisis_seq TO angasys_user;


--
-- Name: TABLE signos_vitales; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.signos_vitales TO angasys_user;


--
-- Name: TABLE signos_vitales_detalle; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.signos_vitales_detalle TO angasys_user;


--
-- Name: SEQUENCE signos_vitales_detalle_id_signos_vitales_detalle_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.signos_vitales_detalle_id_signos_vitales_detalle_seq TO angasys_user;


--
-- Name: SEQUENCE signos_vitales_id_signos_vitales_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.signos_vitales_id_signos_vitales_seq TO angasys_user;


--
-- Name: TABLE tipos_justificativos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.tipos_justificativos TO angasys_user;


--
-- Name: SEQUENCE tipos_justificativos_id_tipo_justificativo_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.tipos_justificativos_id_tipo_justificativo_seq TO angasys_user;


--
-- Name: TABLE tipos_procedimientos; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.tipos_procedimientos TO angasys_user;


--
-- Name: SEQUENCE tipos_procedimientos_id_tipo_procedimiento_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.tipos_procedimientos_id_tipo_procedimiento_seq TO angasys_user;


--
-- Name: TABLE tipos_signos_vitales; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consultorio.tipos_signos_vitales TO angasys_user;


--
-- Name: SEQUENCE tipos_signos_vitales_id_tipo_signo_vital_seq; Type: ACL; Schema: consultorio; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE consultorio.tipos_signos_vitales_id_tipo_signo_vital_seq TO angasys_user;


--
-- Name: TABLE agenda_horarios; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.agenda_horarios TO angasys_user;


--
-- Name: TABLE agenda_horarios_excepciones; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.agenda_horarios_excepciones TO angasys_user;


--
-- Name: SEQUENCE agenda_horarios_excepciones_id_agenda_horario_excepcion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.agenda_horarios_excepciones_id_agenda_horario_excepcion_seq TO angasys_user;


--
-- Name: SEQUENCE agenda_horarios_id_agenda_horario_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.agenda_horarios_id_agenda_horario_seq TO angasys_user;


--
-- Name: TABLE auditoria_sistema; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.auditoria_sistema TO angasys_user;


--
-- Name: SEQUENCE auditoria_sistema_id_auditoria_sistema_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.auditoria_sistema_id_auditoria_sistema_seq TO angasys_user;


--
-- Name: TABLE auditoria_sistema_y2026; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.auditoria_sistema_y2026 TO angasys_user;


--
-- Name: TABLE auditoria_sistema_y2027; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.auditoria_sistema_y2027 TO angasys_user;


--
-- Name: TABLE auditoria_sistema_y2028; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.auditoria_sistema_y2028 TO angasys_user;


--
-- Name: TABLE cargos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.cargos TO angasys_user;


--
-- Name: SEQUENCE cargos_id_cargo_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.cargos_id_cargo_seq TO angasys_user;


--
-- Name: TABLE citas; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.citas TO angasys_user;


--
-- Name: SEQUENCE citas_id_cita_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.citas_id_cita_seq TO angasys_user;


--
-- Name: TABLE citas_log_estados; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.citas_log_estados TO angasys_user;


--
-- Name: SEQUENCE citas_log_estados_id_cita_log_estado_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.citas_log_estados_id_cita_log_estado_seq TO angasys_user;


--
-- Name: TABLE ciudades; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.ciudades TO angasys_user;


--
-- Name: SEQUENCE ciudades_id_ciudad_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.ciudades_id_ciudad_seq TO angasys_user;


--
-- Name: TABLE condiciones_venta; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.condiciones_venta TO angasys_user;


--
-- Name: SEQUENCE condiciones_venta_id_condicion_venta_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.condiciones_venta_id_condicion_venta_seq TO angasys_user;


--
-- Name: TABLE consultorios; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.consultorios TO angasys_user;


--
-- Name: SEQUENCE consultorios_id_consultorio_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.consultorios_id_consultorio_seq TO angasys_user;


--
-- Name: TABLE departamentos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.departamentos TO angasys_user;


--
-- Name: SEQUENCE departamentos_id_departamento_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.departamentos_id_departamento_seq TO angasys_user;


--
-- Name: TABLE dias_semana; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.dias_semana TO angasys_user;


--
-- Name: SEQUENCE dias_semana_id_dia_semana_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.dias_semana_id_dia_semana_seq TO angasys_user;


--
-- Name: TABLE empresa_certificados; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.empresa_certificados TO angasys_user;


--
-- Name: SEQUENCE empresa_certificados_id_empresa_certificado_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.empresa_certificados_id_empresa_certificado_seq TO angasys_user;


--
-- Name: TABLE empresa_configuracion; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.empresa_configuracion TO angasys_user;


--
-- Name: SEQUENCE empresa_configuracion_id_empresa_configuracion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.empresa_configuracion_id_empresa_configuracion_seq TO angasys_user;


--
-- Name: TABLE empresa_modulos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.empresa_modulos TO angasys_user;


--
-- Name: SEQUENCE empresa_modulos_id_empresa_modulo_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.empresa_modulos_id_empresa_modulo_seq TO angasys_user;


--
-- Name: TABLE empresas; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.empresas TO angasys_user;


--
-- Name: SEQUENCE empresas_id_empresa_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.empresas_id_empresa_seq TO angasys_user;


--
-- Name: TABLE especialidades; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.especialidades TO angasys_user;


--
-- Name: SEQUENCE especialidades_id_especialidad_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.especialidades_id_especialidad_seq TO angasys_user;


--
-- Name: TABLE especialista_especialidades; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.especialista_especialidades TO angasys_user;


--
-- Name: SEQUENCE especialista_especialidades_id_especialista_especialidad_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.especialista_especialidades_id_especialista_especialidad_seq TO angasys_user;


--
-- Name: TABLE especialistas; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.especialistas TO angasys_user;


--
-- Name: SEQUENCE especialistas_id_especialista_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.especialistas_id_especialista_seq TO angasys_user;


--
-- Name: TABLE establecimientos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.establecimientos TO angasys_user;


--
-- Name: SEQUENCE establecimientos_id_establecimiento_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.establecimientos_id_establecimiento_seq TO angasys_user;


--
-- Name: TABLE estados_citas; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.estados_citas TO angasys_user;


--
-- Name: SEQUENCE estados_citas_id_estado_cita_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.estados_citas_id_estado_cita_seq TO angasys_user;


--
-- Name: TABLE estados_civiles; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.estados_civiles TO angasys_user;


--
-- Name: SEQUENCE estados_civiles_id_estado_civil_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.estados_civiles_id_estado_civil_seq TO angasys_user;


--
-- Name: TABLE estados_factura; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.estados_factura TO angasys_user;


--
-- Name: SEQUENCE estados_factura_id_estado_factura_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.estados_factura_id_estado_factura_seq TO angasys_user;


--
-- Name: TABLE feriados; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.feriados TO angasys_user;


--
-- Name: SEQUENCE feriados_id_feriado_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.feriados_id_feriado_seq TO angasys_user;


--
-- Name: TABLE formas_cobro; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.formas_cobro TO angasys_user;


--
-- Name: SEQUENCE formas_cobro_id_forma_cobro_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.formas_cobro_id_forma_cobro_seq TO angasys_user;


--
-- Name: TABLE frecuencias_agendamiento; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.frecuencias_agendamiento TO angasys_user;


--
-- Name: SEQUENCE frecuencias_agendamiento_id_frecuencia_agendamiento_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.frecuencias_agendamiento_id_frecuencia_agendamiento_seq TO angasys_user;


--
-- Name: TABLE funcionarios; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.funcionarios TO angasys_user;


--
-- Name: SEQUENCE funcionarios_id_funcionario_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.funcionarios_id_funcionario_seq TO angasys_user;


--
-- Name: TABLE generos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.generos TO angasys_user;


--
-- Name: SEQUENCE generos_id_genero_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.generos_id_genero_seq TO angasys_user;


--
-- Name: TABLE historial_suscripciones; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.historial_suscripciones TO angasys_user;


--
-- Name: SEQUENCE historial_suscripciones_id_historial_suscripcion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.historial_suscripciones_id_historial_suscripcion_seq TO angasys_user;


--
-- Name: TABLE licencias; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.licencias TO angasys_user;


--
-- Name: SEQUENCE licencias_id_licencia_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.licencias_id_licencia_seq TO angasys_user;


--
-- Name: TABLE lista_espera; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.lista_espera TO angasys_user;


--
-- Name: SEQUENCE lista_espera_id_lista_espera_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.lista_espera_id_lista_espera_seq TO angasys_user;


--
-- Name: TABLE login_attempts; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.login_attempts TO angasys_user;


--
-- Name: SEQUENCE login_attempts_id_login_attempt_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.login_attempts_id_login_attempt_seq TO angasys_user;


--
-- Name: TABLE marcas_tarjeta; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.marcas_tarjeta TO angasys_user;


--
-- Name: SEQUENCE marcas_tarjeta_id_marca_tarjeta_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.marcas_tarjeta_id_marca_tarjeta_seq TO angasys_user;


--
-- Name: TABLE metricas_diarias; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.metricas_diarias TO angasys_user;


--
-- Name: SEQUENCE metricas_diarias_id_metrica_diaria_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.metricas_diarias_id_metrica_diaria_seq TO angasys_user;


--
-- Name: TABLE mfa_tokens; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.mfa_tokens TO angasys_user;


--
-- Name: SEQUENCE mfa_tokens_id_mfa_token_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.mfa_tokens_id_mfa_token_seq TO angasys_user;


--
-- Name: TABLE modulos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.modulos TO angasys_user;


--
-- Name: SEQUENCE modulos_id_modulo_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.modulos_id_modulo_seq TO angasys_user;


--
-- Name: TABLE monedas; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.monedas TO angasys_user;


--
-- Name: SEQUENCE monedas_id_moneda_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.monedas_id_moneda_seq TO angasys_user;


--
-- Name: TABLE niveles_instruccion; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.niveles_instruccion TO angasys_user;


--
-- Name: SEQUENCE niveles_instruccion_id_nivel_instruccion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.niveles_instruccion_id_nivel_instruccion_seq TO angasys_user;


--
-- Name: TABLE notificaciones_cola; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.notificaciones_cola TO angasys_user;


--
-- Name: SEQUENCE notificaciones_cola_id_notificacion_cola_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.notificaciones_cola_id_notificacion_cola_seq TO angasys_user;


--
-- Name: TABLE notificaciones_config; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.notificaciones_config TO angasys_user;


--
-- Name: SEQUENCE notificaciones_config_id_notificacion_config_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.notificaciones_config_id_notificacion_config_seq TO angasys_user;


--
-- Name: TABLE notificaciones_log; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.notificaciones_log TO angasys_user;


--
-- Name: SEQUENCE notificaciones_log_id_notificacion_log_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.notificaciones_log_id_notificacion_log_seq TO angasys_user;


--
-- Name: TABLE notificaciones_plantillas; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.notificaciones_plantillas TO angasys_user;


--
-- Name: SEQUENCE notificaciones_plantillas_id_notificacion_plantilla_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.notificaciones_plantillas_id_notificacion_plantilla_seq TO angasys_user;


--
-- Name: TABLE paciente_profesional; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.paciente_profesional TO angasys_user;


--
-- Name: SEQUENCE paciente_profesional_id_paciente_profesional_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.paciente_profesional_id_paciente_profesional_seq TO angasys_user;


--
-- Name: TABLE pacientes; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.pacientes TO angasys_user;


--
-- Name: SEQUENCE pacientes_id_paciente_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.pacientes_id_paciente_seq TO angasys_user;


--
-- Name: TABLE pacientes_menores; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.pacientes_menores TO angasys_user;


--
-- Name: SEQUENCE pacientes_menores_id_paciente_menor_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.pacientes_menores_id_paciente_menor_seq TO angasys_user;


--
-- Name: TABLE paises; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.paises TO angasys_user;


--
-- Name: SEQUENCE paises_id_pais_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.paises_id_pais_seq TO angasys_user;


--
-- Name: TABLE password_history; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.password_history TO angasys_user;


--
-- Name: SEQUENCE password_history_id_password_history_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.password_history_id_password_history_seq TO angasys_user;


--
-- Name: TABLE password_reset_tokens; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.password_reset_tokens TO angasys_user;


--
-- Name: SEQUENCE password_reset_tokens_id_password_reset_token_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.password_reset_tokens_id_password_reset_token_seq TO angasys_user;


--
-- Name: TABLE permisos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.permisos TO angasys_user;


--
-- Name: SEQUENCE permisos_id_permiso_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.permisos_id_permiso_seq TO angasys_user;


--
-- Name: TABLE personas; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.personas TO angasys_user;


--
-- Name: SEQUENCE personas_id_persona_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.personas_id_persona_seq TO angasys_user;


--
-- Name: TABLE plan_modulos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.plan_modulos TO angasys_user;


--
-- Name: SEQUENCE plan_modulos_id_plan_modulo_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.plan_modulos_id_plan_modulo_seq TO angasys_user;


--
-- Name: TABLE planes; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.planes TO angasys_user;


--
-- Name: SEQUENCE planes_id_plan_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.planes_id_plan_seq TO angasys_user;


--
-- Name: TABLE preferencias_ui; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.preferencias_ui TO angasys_user;


--
-- Name: SEQUENCE preferencias_ui_id_preferencia_ui_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.preferencias_ui_id_preferencia_ui_seq TO angasys_user;


--
-- Name: TABLE profesiones; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.profesiones TO angasys_user;


--
-- Name: SEQUENCE profesiones_id_profesion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.profesiones_id_profesion_seq TO angasys_user;


--
-- Name: TABLE puntos_expedicion; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.puntos_expedicion TO angasys_user;


--
-- Name: SEQUENCE puntos_expedicion_id_punto_expedicion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.puntos_expedicion_id_punto_expedicion_seq TO angasys_user;


--
-- Name: TABLE recordatorios; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.recordatorios TO angasys_user;


--
-- Name: SEQUENCE recordatorios_id_recordatorio_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.recordatorios_id_recordatorio_seq TO angasys_user;


--
-- Name: TABLE reportes_jobs; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.reportes_jobs TO angasys_user;


--
-- Name: SEQUENCE reportes_jobs_id_reporte_job_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.reportes_jobs_id_reporte_job_seq TO angasys_user;


--
-- Name: TABLE reportes_jobs_log; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.reportes_jobs_log TO angasys_user;


--
-- Name: SEQUENCE reportes_jobs_log_id_reporte_job_log_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.reportes_jobs_log_id_reporte_job_log_seq TO angasys_user;


--
-- Name: TABLE roles_base; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.roles_base TO angasys_user;


--
-- Name: SEQUENCE roles_base_id_rol_base_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.roles_base_id_rol_base_seq TO angasys_user;


--
-- Name: TABLE roles_empresa; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.roles_empresa TO angasys_user;


--
-- Name: SEQUENCE roles_empresa_id_rol_empresa_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.roles_empresa_id_rol_empresa_seq TO angasys_user;


--
-- Name: TABLE roles_empresa_permisos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.roles_empresa_permisos TO angasys_user;


--
-- Name: SEQUENCE roles_empresa_permisos_id_rol_empresa_permiso_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.roles_empresa_permisos_id_rol_empresa_permiso_seq TO angasys_user;


--
-- Name: TABLE schema_migrations; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.schema_migrations TO angasys_user;


--
-- Name: SEQUENCE schema_migrations_id_schema_migration_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.schema_migrations_id_schema_migration_seq TO angasys_user;


--
-- Name: TABLE sedes; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.sedes TO angasys_user;


--
-- Name: SEQUENCE sedes_id_sede_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.sedes_id_sede_seq TO angasys_user;


--
-- Name: TABLE sesiones; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.sesiones TO angasys_user;


--
-- Name: SEQUENCE sesiones_id_sesion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.sesiones_id_sesion_seq TO angasys_user;


--
-- Name: TABLE slots_agenda; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.slots_agenda TO angasys_user;


--
-- Name: SEQUENCE slots_agenda_id_slot_agenda_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.slots_agenda_id_slot_agenda_seq TO angasys_user;


--
-- Name: TABLE suscripcion_excedentes; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.suscripcion_excedentes TO angasys_user;


--
-- Name: SEQUENCE suscripcion_excedentes_id_suscripcion_excedente_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.suscripcion_excedentes_id_suscripcion_excedente_seq TO angasys_user;


--
-- Name: TABLE suscripcion_expansiones; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.suscripcion_expansiones TO angasys_user;


--
-- Name: SEQUENCE suscripcion_expansiones_id_expansion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.suscripcion_expansiones_id_expansion_seq TO angasys_user;


--
-- Name: TABLE suscripciones; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.suscripciones TO angasys_user;


--
-- Name: SEQUENCE suscripciones_id_suscripcion_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.suscripciones_id_suscripcion_seq TO angasys_user;


--
-- Name: TABLE tipos_clinicos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.tipos_clinicos TO angasys_user;


--
-- Name: TABLE tipos_comprobantes; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.tipos_comprobantes TO angasys_user;


--
-- Name: SEQUENCE tipos_comprobantes_id_tipo_comprobante_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.tipos_comprobantes_id_tipo_comprobante_seq TO angasys_user;


--
-- Name: TABLE tipos_documentos_identidad; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.tipos_documentos_identidad TO angasys_user;


--
-- Name: SEQUENCE tipos_documentos_identidad_id_tipo_documento_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.tipos_documentos_identidad_id_tipo_documento_seq TO angasys_user;


--
-- Name: TABLE tipos_impuestos; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.tipos_impuestos TO angasys_user;


--
-- Name: SEQUENCE tipos_impuestos_id_tipo_impuesto_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.tipos_impuestos_id_tipo_impuesto_seq TO angasys_user;


--
-- Name: TABLE tipos_items; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.tipos_items TO angasys_user;


--
-- Name: SEQUENCE tipos_items_id_tipo_item_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.tipos_items_id_tipo_item_seq TO angasys_user;


--
-- Name: TABLE usuarios; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.usuarios TO angasys_user;


--
-- Name: SEQUENCE usuarios_id_usuario_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.usuarios_id_usuario_seq TO angasys_user;


--
-- Name: TABLE usuarios_roles_base; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.usuarios_roles_base TO angasys_user;


--
-- Name: SEQUENCE usuarios_roles_base_id_usuario_rol_base_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.usuarios_roles_base_id_usuario_rol_base_seq TO angasys_user;


--
-- Name: TABLE usuarios_roles_empresa; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE core.usuarios_roles_empresa TO angasys_user;


--
-- Name: SEQUENCE usuarios_roles_empresa_id_usuario_rol_empresa_seq; Type: ACL; Schema: core; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE core.usuarios_roles_empresa_id_usuario_rol_empresa_seq TO angasys_user;


--
-- Name: TABLE aperturas_caja; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.aperturas_caja TO angasys_user;


--
-- Name: SEQUENCE aperturas_caja_id_apertura_caja_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.aperturas_caja_id_apertura_caja_seq TO angasys_user;


--
-- Name: TABLE arqueos_caja; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.arqueos_caja TO angasys_user;


--
-- Name: SEQUENCE arqueos_caja_id_arqueo_caja_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.arqueos_caja_id_arqueo_caja_seq TO angasys_user;


--
-- Name: TABLE autofactura_detalle; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.autofactura_detalle TO angasys_user;


--
-- Name: SEQUENCE autofactura_detalle_id_autofactura_detalle_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.autofactura_detalle_id_autofactura_detalle_seq TO angasys_user;


--
-- Name: TABLE autofacturas; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.autofacturas TO angasys_user;


--
-- Name: SEQUENCE autofacturas_id_autofactura_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.autofacturas_id_autofactura_seq TO angasys_user;


--
-- Name: TABLE cajas; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.cajas TO angasys_user;


--
-- Name: SEQUENCE cajas_id_caja_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.cajas_id_caja_seq TO angasys_user;


--
-- Name: TABLE categorias_items; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.categorias_items TO angasys_user;


--
-- Name: SEQUENCE categorias_items_id_categoria_item_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.categorias_items_id_categoria_item_seq TO angasys_user;


--
-- Name: TABLE cheques_recibidos; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.cheques_recibidos TO angasys_user;


--
-- Name: SEQUENCE cheques_recibidos_id_cheque_recibido_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.cheques_recibidos_id_cheque_recibido_seq TO angasys_user;


--
-- Name: TABLE cobranza_detalle; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.cobranza_detalle TO angasys_user;


--
-- Name: SEQUENCE cobranza_detalle_id_cobranza_detalle_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.cobranza_detalle_id_cobranza_detalle_seq TO angasys_user;


--
-- Name: TABLE cobranzas; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.cobranzas TO angasys_user;


--
-- Name: SEQUENCE cobranzas_id_cobranza_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.cobranzas_id_cobranza_seq TO angasys_user;


--
-- Name: TABLE cuentas_cobrar; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.cuentas_cobrar TO angasys_user;


--
-- Name: SEQUENCE cuentas_cobrar_id_cuenta_cobrar_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.cuentas_cobrar_id_cuenta_cobrar_seq TO angasys_user;


--
-- Name: TABLE cuotas_cobrar; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.cuotas_cobrar TO angasys_user;


--
-- Name: SEQUENCE cuotas_cobrar_id_cuota_cobrar_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.cuotas_cobrar_id_cuota_cobrar_seq TO angasys_user;


--
-- Name: TABLE documentos_electronicos; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.documentos_electronicos TO angasys_user;


--
-- Name: SEQUENCE documentos_electronicos_id_de_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.documentos_electronicos_id_de_seq TO angasys_user;


--
-- Name: TABLE entidades_bancarias; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.entidades_bancarias TO angasys_user;


--
-- Name: SEQUENCE entidades_bancarias_id_entidad_bancaria_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.entidades_bancarias_id_entidad_bancaria_seq TO angasys_user;


--
-- Name: TABLE entidades_pagadoras; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.entidades_pagadoras TO angasys_user;


--
-- Name: SEQUENCE entidades_pagadoras_id_entidad_pagadora_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.entidades_pagadoras_id_entidad_pagadora_seq TO angasys_user;


--
-- Name: TABLE factura_detalle; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.factura_detalle TO angasys_user;


--
-- Name: SEQUENCE factura_detalle_id_factura_detalle_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.factura_detalle_id_factura_detalle_seq TO angasys_user;


--
-- Name: TABLE factura_medios_pago; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.factura_medios_pago TO angasys_user;


--
-- Name: SEQUENCE factura_medios_pago_id_factura_medio_pago_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.factura_medios_pago_id_factura_medio_pago_seq TO angasys_user;


--
-- Name: TABLE facturas; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.facturas TO angasys_user;


--
-- Name: SEQUENCE facturas_id_factura_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.facturas_id_factura_seq TO angasys_user;


--
-- Name: TABLE items; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.items TO angasys_user;


--
-- Name: SEQUENCE items_id_item_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.items_id_item_seq TO angasys_user;


--
-- Name: TABLE libro_ventas; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.libro_ventas TO angasys_user;


--
-- Name: SEQUENCE libro_ventas_id_libro_venta_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.libro_ventas_id_libro_venta_seq TO angasys_user;


--
-- Name: TABLE movimientos_caja; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.movimientos_caja TO angasys_user;


--
-- Name: SEQUENCE movimientos_caja_id_movimiento_caja_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.movimientos_caja_id_movimiento_caja_seq TO angasys_user;


--
-- Name: TABLE nota_credito_detalle; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.nota_credito_detalle TO angasys_user;


--
-- Name: SEQUENCE nota_credito_detalle_id_nota_credito_detalle_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.nota_credito_detalle_id_nota_credito_detalle_seq TO angasys_user;


--
-- Name: TABLE nota_debito_detalle; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.nota_debito_detalle TO angasys_user;


--
-- Name: SEQUENCE nota_debito_detalle_id_nota_debito_detalle_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.nota_debito_detalle_id_nota_debito_detalle_seq TO angasys_user;


--
-- Name: TABLE nota_remision_detalle; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.nota_remision_detalle TO angasys_user;


--
-- Name: SEQUENCE nota_remision_detalle_id_nota_remision_detalle_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.nota_remision_detalle_id_nota_remision_detalle_seq TO angasys_user;


--
-- Name: TABLE notas_credito; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.notas_credito TO angasys_user;


--
-- Name: SEQUENCE notas_credito_id_nota_credito_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.notas_credito_id_nota_credito_seq TO angasys_user;


--
-- Name: TABLE notas_debito; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.notas_debito TO angasys_user;


--
-- Name: SEQUENCE notas_debito_id_nota_debito_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.notas_debito_id_nota_debito_seq TO angasys_user;


--
-- Name: TABLE notas_remision; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.notas_remision TO angasys_user;


--
-- Name: SEQUENCE notas_remision_id_nota_remision_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.notas_remision_id_nota_remision_seq TO angasys_user;


--
-- Name: TABLE recaudacion_detalle; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.recaudacion_detalle TO angasys_user;


--
-- Name: SEQUENCE recaudacion_detalle_id_recaudacion_detalle_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.recaudacion_detalle_id_recaudacion_detalle_seq TO angasys_user;


--
-- Name: TABLE recaudaciones; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.recaudaciones TO angasys_user;


--
-- Name: SEQUENCE recaudaciones_id_recaudacion_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.recaudaciones_id_recaudacion_seq TO angasys_user;


--
-- Name: TABLE secuencias_numeracion; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.secuencias_numeracion TO angasys_user;


--
-- Name: SEQUENCE secuencias_numeracion_id_secuencia_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.secuencias_numeracion_id_secuencia_seq TO angasys_user;


--
-- Name: TABLE sifen_config; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.sifen_config TO angasys_user;


--
-- Name: SEQUENCE sifen_config_id_sifen_config_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.sifen_config_id_sifen_config_seq TO angasys_user;


--
-- Name: TABLE sifen_eventos; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.sifen_eventos TO angasys_user;


--
-- Name: SEQUENCE sifen_eventos_id_evento_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.sifen_eventos_id_evento_seq TO angasys_user;


--
-- Name: TABLE sifen_lote_documentos; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.sifen_lote_documentos TO angasys_user;


--
-- Name: SEQUENCE sifen_lote_documentos_id_lote_documento_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.sifen_lote_documentos_id_lote_documento_seq TO angasys_user;


--
-- Name: TABLE sifen_lotes; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.sifen_lotes TO angasys_user;


--
-- Name: SEQUENCE sifen_lotes_id_lote_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.sifen_lotes_id_lote_seq TO angasys_user;


--
-- Name: TABLE sifen_transmision_log; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.sifen_transmision_log TO angasys_user;


--
-- Name: SEQUENCE sifen_transmision_log_id_transmision_log_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.sifen_transmision_log_id_transmision_log_seq TO angasys_user;


--
-- Name: TABLE tarifario_precios; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.tarifario_precios TO angasys_user;


--
-- Name: SEQUENCE tarifario_precios_id_tarifario_precio_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.tarifario_precios_id_tarifario_precio_seq TO angasys_user;


--
-- Name: TABLE timbrado_habilitaciones; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.timbrado_habilitaciones TO angasys_user;


--
-- Name: SEQUENCE timbrado_habilitaciones_id_timbrado_habilitacion_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.timbrado_habilitaciones_id_timbrado_habilitacion_seq TO angasys_user;


--
-- Name: TABLE timbrados; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE facturacion.timbrados TO angasys_user;


--
-- Name: SEQUENCE timbrados_id_timbrado_seq; Type: ACL; Schema: facturacion; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE facturacion.timbrados_id_timbrado_seq TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: consultorio; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA consultorio GRANT SELECT,USAGE ON SEQUENCES TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: consultorio; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA consultorio GRANT ALL ON FUNCTIONS TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: consultorio; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA consultorio GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: core; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA core GRANT SELECT,USAGE ON SEQUENCES TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: core; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA core GRANT ALL ON FUNCTIONS TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: core; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA core GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: facturacion; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA facturacion GRANT SELECT,USAGE ON SEQUENCES TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: facturacion; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA facturacion GRANT ALL ON FUNCTIONS TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: facturacion; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA facturacion GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT,USAGE ON SEQUENCES TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON FUNCTIONS TO angasys_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO angasys_user;


--
-- PostgreSQL database dump complete
--

\unrestrict 2cnVbQwHvvCiihqzcho5z9RUAeFeOqOpMX37EMP6ObPu3AmXZO4wS5jQ6oCtkna

