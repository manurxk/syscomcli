-- 06_referenciales_agendamiento_clinico.sql — Referenciales de agendamiento y clínicos
-- Generado el 2026-10-19 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: dias_semana, estados_citas, signos, sintomas, diagnosticos, medicamentos, tipos_analisis, tipos_estudios, tipos_procedimientos, tipos_tratamientos, tipos_certificados_medicos, instrumentos.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/06_referenciales_agendamiento_clinico.sql

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
-- Name: diagnosticos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.diagnosticos (
    id_diagnostico integer NOT NULL,
    cod_cie10 character varying(10),
    des_diagnostico character varying(255) NOT NULL,
    est_diagnostico boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: diagnosticos_id_diagnostico_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.diagnosticos_id_diagnostico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: diagnosticos_id_diagnostico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.diagnosticos_id_diagnostico_seq OWNED BY public.diagnosticos.id_diagnostico;

--
-- Name: dias_semana; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dias_semana (
    id_dia_semana integer NOT NULL,
    nro_dia smallint NOT NULL,
    des_dia character varying(20) NOT NULL,
    est_dia boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_dias_semana_nro CHECK (((nro_dia >= 1) AND (nro_dia <= 7)))
);

--
-- Name: dias_semana_id_dia_semana_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dias_semana_id_dia_semana_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: dias_semana_id_dia_semana_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dias_semana_id_dia_semana_seq OWNED BY public.dias_semana.id_dia_semana;

--
-- Name: estados_citas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estados_citas (
    id_estado_cita integer NOT NULL,
    cod_estado_cita character varying(20) NOT NULL,
    des_estado_cita character varying(60) NOT NULL,
    orden smallint NOT NULL,
    es_final boolean DEFAULT false NOT NULL,
    est_estado_cita boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_estados_citas_cod CHECK (((cod_estado_cita)::text = ANY ((ARRAY['AGENDADA'::character varying, 'CONFIRMADA'::character varying, 'EN_CONSULTA'::character varying, 'COMPLETADA'::character varying, 'AUSENTE'::character varying, 'CANCELADA'::character varying])::text[])))
);

--
-- Name: estados_citas_id_estado_cita_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estados_citas_id_estado_cita_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: estados_citas_id_estado_cita_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estados_citas_id_estado_cita_seq OWNED BY public.estados_citas.id_estado_cita;

--
-- Name: instrumentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.instrumentos (
    id_instrumento integer NOT NULL,
    des_instrumento character varying(150) NOT NULL,
    est_instrumento boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: instrumentos_id_instrumento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.instrumentos_id_instrumento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: instrumentos_id_instrumento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.instrumentos_id_instrumento_seq OWNED BY public.instrumentos.id_instrumento;

--
-- Name: medicamentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medicamentos (
    id_medicamento integer NOT NULL,
    des_medicamento character varying(150) NOT NULL,
    est_medicamento boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

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
-- Name: signos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.signos (
    id_signo integer NOT NULL,
    des_signo character varying(150) NOT NULL,
    est_signo boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: signos_id_signo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.signos_id_signo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: signos_id_signo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.signos_id_signo_seq OWNED BY public.signos.id_signo;

--
-- Name: sintomas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sintomas (
    id_sintoma integer NOT NULL,
    des_sintoma character varying(150) NOT NULL,
    est_sintoma boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: sintomas_id_sintoma_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sintomas_id_sintoma_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: sintomas_id_sintoma_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sintomas_id_sintoma_seq OWNED BY public.sintomas.id_sintoma;

--
-- Name: tipos_analisis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_analisis (
    id_tipo_analisis integer NOT NULL,
    des_tipo_analisis character varying(150) NOT NULL,
    est_tipo_analisis boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: tipos_analisis_id_tipo_analisis_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_analisis_id_tipo_analisis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_analisis_id_tipo_analisis_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_analisis_id_tipo_analisis_seq OWNED BY public.tipos_analisis.id_tipo_analisis;

--
-- Name: tipos_certificados_medicos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_certificados_medicos (
    id_tipo_certificado_medico integer NOT NULL,
    des_tipo_certificado_medico character varying(150) NOT NULL,
    est_tipo_certificado_medico boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: tipos_certificados_medicos_id_tipo_certificado_medico_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_certificados_medicos_id_tipo_certificado_medico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_certificados_medicos_id_tipo_certificado_medico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_certificados_medicos_id_tipo_certificado_medico_seq OWNED BY public.tipos_certificados_medicos.id_tipo_certificado_medico;

--
-- Name: tipos_estudios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_estudios (
    id_tipo_estudio integer NOT NULL,
    des_tipo_estudio character varying(150) NOT NULL,
    est_tipo_estudio boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: tipos_estudios_id_tipo_estudio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_estudios_id_tipo_estudio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_estudios_id_tipo_estudio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_estudios_id_tipo_estudio_seq OWNED BY public.tipos_estudios.id_tipo_estudio;

--
-- Name: tipos_procedimientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_procedimientos (
    id_tipo_procedimiento integer NOT NULL,
    des_tipo_procedimiento character varying(150) NOT NULL,
    est_tipo_procedimiento boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: tipos_procedimientos_id_tipo_procedimiento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_procedimientos_id_tipo_procedimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_procedimientos_id_tipo_procedimiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_procedimientos_id_tipo_procedimiento_seq OWNED BY public.tipos_procedimientos.id_tipo_procedimiento;

--
-- Name: tipos_tratamientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_tratamientos (
    id_tipo_tratamiento integer NOT NULL,
    des_tipo_tratamiento character varying(150) NOT NULL,
    est_tipo_tratamiento boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: tipos_tratamientos_id_tipo_tratamiento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_tratamientos_id_tipo_tratamiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_tratamientos_id_tipo_tratamiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_tratamientos_id_tipo_tratamiento_seq OWNED BY public.tipos_tratamientos.id_tipo_tratamiento;

--
-- Name: diagnosticos id_diagnostico; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diagnosticos ALTER COLUMN id_diagnostico SET DEFAULT nextval('public.diagnosticos_id_diagnostico_seq'::regclass);

--
-- Name: dias_semana id_dia_semana; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias_semana ALTER COLUMN id_dia_semana SET DEFAULT nextval('public.dias_semana_id_dia_semana_seq'::regclass);

--
-- Name: estados_citas id_estado_cita; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_citas ALTER COLUMN id_estado_cita SET DEFAULT nextval('public.estados_citas_id_estado_cita_seq'::regclass);

--
-- Name: instrumentos id_instrumento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.instrumentos ALTER COLUMN id_instrumento SET DEFAULT nextval('public.instrumentos_id_instrumento_seq'::regclass);

--
-- Name: medicamentos id_medicamento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicamentos ALTER COLUMN id_medicamento SET DEFAULT nextval('public.medicamentos_id_medicamento_seq'::regclass);

--
-- Name: signos id_signo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos ALTER COLUMN id_signo SET DEFAULT nextval('public.signos_id_signo_seq'::regclass);

--
-- Name: sintomas id_sintoma; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas ALTER COLUMN id_sintoma SET DEFAULT nextval('public.sintomas_id_sintoma_seq'::regclass);

--
-- Name: tipos_analisis id_tipo_analisis; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_analisis ALTER COLUMN id_tipo_analisis SET DEFAULT nextval('public.tipos_analisis_id_tipo_analisis_seq'::regclass);

--
-- Name: tipos_certificados_medicos id_tipo_certificado_medico; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_certificados_medicos ALTER COLUMN id_tipo_certificado_medico SET DEFAULT nextval('public.tipos_certificados_medicos_id_tipo_certificado_medico_seq'::regclass);

--
-- Name: tipos_estudios id_tipo_estudio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_estudios ALTER COLUMN id_tipo_estudio SET DEFAULT nextval('public.tipos_estudios_id_tipo_estudio_seq'::regclass);

--
-- Name: tipos_procedimientos id_tipo_procedimiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_procedimientos ALTER COLUMN id_tipo_procedimiento SET DEFAULT nextval('public.tipos_procedimientos_id_tipo_procedimiento_seq'::regclass);

--
-- Name: tipos_tratamientos id_tipo_tratamiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_tratamientos ALTER COLUMN id_tipo_tratamiento SET DEFAULT nextval('public.tipos_tratamientos_id_tipo_tratamiento_seq'::regclass);

--
-- Name: diagnosticos diagnosticos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diagnosticos
    ADD CONSTRAINT diagnosticos_pkey PRIMARY KEY (id_diagnostico);

--
-- Name: dias_semana dias_semana_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias_semana
    ADD CONSTRAINT dias_semana_pkey PRIMARY KEY (id_dia_semana);

--
-- Name: estados_citas estados_citas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_citas
    ADD CONSTRAINT estados_citas_pkey PRIMARY KEY (id_estado_cita);

--
-- Name: instrumentos instrumentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.instrumentos
    ADD CONSTRAINT instrumentos_pkey PRIMARY KEY (id_instrumento);

--
-- Name: medicamentos medicamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicamentos
    ADD CONSTRAINT medicamentos_pkey PRIMARY KEY (id_medicamento);

--
-- Name: signos signos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos
    ADD CONSTRAINT signos_pkey PRIMARY KEY (id_signo);

--
-- Name: sintomas sintomas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas
    ADD CONSTRAINT sintomas_pkey PRIMARY KEY (id_sintoma);

--
-- Name: tipos_analisis tipos_analisis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_analisis
    ADD CONSTRAINT tipos_analisis_pkey PRIMARY KEY (id_tipo_analisis);

--
-- Name: tipos_certificados_medicos tipos_certificados_medicos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_certificados_medicos
    ADD CONSTRAINT tipos_certificados_medicos_pkey PRIMARY KEY (id_tipo_certificado_medico);

--
-- Name: tipos_estudios tipos_estudios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_estudios
    ADD CONSTRAINT tipos_estudios_pkey PRIMARY KEY (id_tipo_estudio);

--
-- Name: tipos_procedimientos tipos_procedimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_procedimientos
    ADD CONSTRAINT tipos_procedimientos_pkey PRIMARY KEY (id_tipo_procedimiento);

--
-- Name: tipos_tratamientos tipos_tratamientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_tratamientos
    ADD CONSTRAINT tipos_tratamientos_pkey PRIMARY KEY (id_tipo_tratamiento);

--
-- Name: diagnosticos uq_diagnosticos_cie10; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diagnosticos
    ADD CONSTRAINT uq_diagnosticos_cie10 UNIQUE (cod_cie10);

--
-- Name: diagnosticos uq_diagnosticos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diagnosticos
    ADD CONSTRAINT uq_diagnosticos_des UNIQUE (des_diagnostico);

--
-- Name: dias_semana uq_dias_semana_nro; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias_semana
    ADD CONSTRAINT uq_dias_semana_nro UNIQUE (nro_dia);

--
-- Name: estados_citas uq_estados_citas_cod; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_citas
    ADD CONSTRAINT uq_estados_citas_cod UNIQUE (cod_estado_cita);

--
-- Name: instrumentos uq_instrumentos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.instrumentos
    ADD CONSTRAINT uq_instrumentos_des UNIQUE (des_instrumento);

--
-- Name: medicamentos uq_medicamentos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicamentos
    ADD CONSTRAINT uq_medicamentos_des UNIQUE (des_medicamento);

--
-- Name: signos uq_signos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos
    ADD CONSTRAINT uq_signos_des UNIQUE (des_signo);

--
-- Name: sintomas uq_sintomas_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas
    ADD CONSTRAINT uq_sintomas_des UNIQUE (des_sintoma);

--
-- Name: tipos_analisis uq_tipos_analisis_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_analisis
    ADD CONSTRAINT uq_tipos_analisis_des UNIQUE (des_tipo_analisis);

--
-- Name: tipos_certificados_medicos uq_tipos_certificados_medicos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_certificados_medicos
    ADD CONSTRAINT uq_tipos_certificados_medicos_des UNIQUE (des_tipo_certificado_medico);

--
-- Name: tipos_estudios uq_tipos_estudios_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_estudios
    ADD CONSTRAINT uq_tipos_estudios_des UNIQUE (des_tipo_estudio);

--
-- Name: tipos_procedimientos uq_tipos_procedimientos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_procedimientos
    ADD CONSTRAINT uq_tipos_procedimientos_des UNIQUE (des_tipo_procedimiento);

--
-- Name: tipos_tratamientos uq_tipos_tratamientos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_tratamientos
    ADD CONSTRAINT uq_tipos_tratamientos_des UNIQUE (des_tipo_tratamiento);

--
-- Name: diagnosticos trg_diagnosticos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_diagnosticos_fecha_mod BEFORE UPDATE ON public.diagnosticos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: dias_semana trg_dias_semana_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_dias_semana_fecha_mod BEFORE UPDATE ON public.dias_semana FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: estados_citas trg_estados_citas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_estados_citas_fecha_mod BEFORE UPDATE ON public.estados_citas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: instrumentos trg_instrumentos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_instrumentos_fecha_mod BEFORE UPDATE ON public.instrumentos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: medicamentos trg_medicamentos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_medicamentos_fecha_mod BEFORE UPDATE ON public.medicamentos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: signos trg_signos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_signos_fecha_mod BEFORE UPDATE ON public.signos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: sintomas trg_sintomas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_sintomas_fecha_mod BEFORE UPDATE ON public.sintomas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_analisis trg_tipos_analisis_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_analisis_fecha_mod BEFORE UPDATE ON public.tipos_analisis FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_certificados_medicos trg_tipos_certificados_medicos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_certificados_medicos_fecha_mod BEFORE UPDATE ON public.tipos_certificados_medicos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_estudios trg_tipos_estudios_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_estudios_fecha_mod BEFORE UPDATE ON public.tipos_estudios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_procedimientos trg_tipos_procedimientos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_procedimientos_fecha_mod BEFORE UPDATE ON public.tipos_procedimientos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_tratamientos trg_tipos_tratamientos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_tratamientos_fecha_mod BEFORE UPDATE ON public.tipos_tratamientos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: diagnosticos diagnosticos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diagnosticos
    ADD CONSTRAINT diagnosticos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: diagnosticos diagnosticos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diagnosticos
    ADD CONSTRAINT diagnosticos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: dias_semana dias_semana_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias_semana
    ADD CONSTRAINT dias_semana_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: dias_semana dias_semana_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dias_semana
    ADD CONSTRAINT dias_semana_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: estados_citas estados_citas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_citas
    ADD CONSTRAINT estados_citas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: estados_citas estados_citas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_citas
    ADD CONSTRAINT estados_citas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: instrumentos instrumentos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.instrumentos
    ADD CONSTRAINT instrumentos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: instrumentos instrumentos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.instrumentos
    ADD CONSTRAINT instrumentos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: medicamentos medicamentos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicamentos
    ADD CONSTRAINT medicamentos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: medicamentos medicamentos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicamentos
    ADD CONSTRAINT medicamentos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: signos signos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos
    ADD CONSTRAINT signos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: signos signos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos
    ADD CONSTRAINT signos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: sintomas sintomas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas
    ADD CONSTRAINT sintomas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: sintomas sintomas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas
    ADD CONSTRAINT sintomas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_analisis tipos_analisis_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_analisis
    ADD CONSTRAINT tipos_analisis_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_analisis tipos_analisis_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_analisis
    ADD CONSTRAINT tipos_analisis_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_certificados_medicos tipos_certificados_medicos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_certificados_medicos
    ADD CONSTRAINT tipos_certificados_medicos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_certificados_medicos tipos_certificados_medicos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_certificados_medicos
    ADD CONSTRAINT tipos_certificados_medicos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_estudios tipos_estudios_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_estudios
    ADD CONSTRAINT tipos_estudios_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_estudios tipos_estudios_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_estudios
    ADD CONSTRAINT tipos_estudios_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_procedimientos tipos_procedimientos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_procedimientos
    ADD CONSTRAINT tipos_procedimientos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_procedimientos tipos_procedimientos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_procedimientos
    ADD CONSTRAINT tipos_procedimientos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_tratamientos tipos_tratamientos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_tratamientos
    ADD CONSTRAINT tipos_tratamientos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_tratamientos tipos_tratamientos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_tratamientos
    ADD CONSTRAINT tipos_tratamientos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
