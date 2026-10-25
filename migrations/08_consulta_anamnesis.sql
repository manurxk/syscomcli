-- 08_consulta_anamnesis.sql — Consulta, anamnesis, PEI, notas clínicas y derivaciones
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: consultas, anamnesis, pei, notas_clinicas, derivaciones.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/08_consulta_anamnesis.sql

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
-- Name: anamnesis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.anamnesis (
    id_anamnesis integer NOT NULL,
    id_paciente integer NOT NULL,
    nro_version integer DEFAULT 1 NOT NULL,
    es_version_actual boolean DEFAULT true NOT NULL,
    informante character varying(20),
    relacion_informante character varying(50),
    motivo_consulta text NOT NULL,
    antecedentes_familiares_similares text,
    antecedentes_patologicos_familiares text,
    componentes_familiares text,
    historia_familiar text,
    antecedentes_patologicos_personales text,
    historia_problema_actual text,
    historia_desarrollo text,
    historia_academica text,
    historia_laboral text,
    historia_rehabilitacion text,
    medicacion_actual text,
    medicacion_psiquiatrica_previa text,
    consumo_sustancias text,
    relaciones_interpersonales text,
    actividad_fisica text,
    patron_sueno text,
    patron_alimentacion text,
    actividad_emocional text,
    actividad_sexual text,
    impresion_diagnostica text,
    plan_trabajo text,
    eval_neuropsicologica boolean DEFAULT false NOT NULL,
    eval_psicologica boolean DEFAULT false NOT NULL,
    eval_psicopedagogica boolean DEFAULT false NOT NULL,
    eval_fonoaudiologica boolean DEFAULT false NOT NULL,
    eval_psicomotora boolean DEFAULT false NOT NULL,
    terapia_individual boolean DEFAULT false NOT NULL,
    terapia_familiar boolean DEFAULT false NOT NULL,
    terapia_grupal boolean DEFAULT false NOT NULL,
    terapia_ocupacional boolean DEFAULT false NOT NULL,
    otra_terapia character varying(100),
    observaciones text,
    indicaciones text,
    est_anamnesis boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_anamnesis_informante CHECK (((informante IS NULL) OR ((informante)::text = ANY (ARRAY[('PACIENTE'::character varying)::text, ('MADRE'::character varying)::text, ('PADRE'::character varying)::text, ('TUTOR'::character varying)::text, ('OTRO'::character varying)::text]))))
);

--
-- Name: TABLE anamnesis; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.anamnesis IS 'Versionado insert-only: cada edición inserta nro_version+1 y marca es_version_actual=TRUE, la fila anterior pasa a es_version_actual=FALSE (UPDATE de un solo campo, nunca se pisa contenido clínico). uq_anamnesis_paciente_version_actual garantiza que solo una fila por paciente sea la vigente. Sin tabla de historial separada (decisión de diseño, ver 02_MAPEO_FASES_NUEVA_BD.md).';

--
-- Name: anamnesis_id_anamnesis_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.anamnesis_id_anamnesis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: anamnesis_id_anamnesis_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.anamnesis_id_anamnesis_seq OWNED BY public.anamnesis.id_anamnesis;

--
-- Name: consultas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultas (
    id_consulta integer NOT NULL,
    id_cita integer NOT NULL,
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    consulta_fecha timestamp without time zone NOT NULL,
    consulta_motivo text NOT NULL,
    consulta_estado character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    des_consulta text,
    consulta_observaciones text,
    est_consulta boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_consultas_estado CHECK (((consulta_estado)::text = ANY (ARRAY[('PENDIENTE'::character varying)::text, ('EN_ATENCION'::character varying)::text, ('FINALIZADA'::character varying)::text])))
);

--
-- Name: TABLE consultas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.consultas IS 'Cabecera de atención clínica. Es la tabla de la que cuelgan, sin cabecera propia, el registro de diagnóstico/signos/síntomas/procedimientos (C.3) y los tratamientos (C.4). id_cita nullable: una consulta puede originarse fuera del flujo de agendamiento.';

--
-- Name: COLUMN consultas.id_cita; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.consultas.id_cita IS 'Obligatorio: toda consulta nace de una cita agendada (recepción confirma/el especialista la inicia desde su agenda). No existe alta manual de consulta sin cita.';

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
-- Name: derivaciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.derivaciones (
    id_derivacion integer NOT NULL,
    id_consulta integer NOT NULL,
    id_especialidad_destino integer NOT NULL,
    motivo_derivacion text NOT NULL,
    derivacion_observaciones text,
    est_derivacion boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: TABLE derivaciones; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.derivaciones IS 'Derivaci??n entre especialistas como detalle de una consulta. Registra la especialidad destino y el motivo; el paciente y el especialista origen se heredan de la consulta asociada.';

--
-- Name: derivaciones_id_derivacion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.derivaciones_id_derivacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: derivaciones_id_derivacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.derivaciones_id_derivacion_seq OWNED BY public.derivaciones.id_derivacion;

--
-- Name: notas_clinicas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notas_clinicas (
    id_nota integer NOT NULL,
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    nota_contenido text NOT NULL,
    nota_fecha timestamp without time zone DEFAULT now() NOT NULL,
    est_nota boolean DEFAULT true NOT NULL,
    usuario_creacion integer,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: TABLE notas_clinicas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.notas_clinicas IS 'Notas libres por PACIENTE en su ficha clínica (seguimiento entre consultas, observaciones del especialista). No duplica a registro_diagnosticos/signos/sintomas/procedimientos/insumos, que son datos estructurados por CONSULTA. Baja lógica con est_nota; fecha_modificacion/usuario_modificacion registran quién y cuándo la anuló (migración 108).';

--
-- Name: notas_clinicas_id_nota_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notas_clinicas_id_nota_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: notas_clinicas_id_nota_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notas_clinicas_id_nota_seq OWNED BY public.notas_clinicas.id_nota;

--
-- Name: pei; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pei (
    id_pei integer NOT NULL,
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    nro_version integer DEFAULT 1 NOT NULL,
    es_version_actual boolean DEFAULT true NOT NULL,
    pei_objetivos text,
    pei_areas_intervencion text,
    pei_estrategias text,
    pei_cronograma_seguimiento text,
    pei_estado character varying(10) DEFAULT 'ACTIVO'::character varying NOT NULL,
    est_pei boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_pei_estado CHECK (((pei_estado)::text = ANY (ARRAY[('ACTIVO'::character varying)::text, ('CERRADO'::character varying)::text])))
);

--
-- Name: TABLE pei; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.pei IS 'Plan Educativo Individual (PEI) — entidad propia versionada (igual que anamnesis). Insert-only: cada edición inserta nro_version+1 y marca es_version_actual=TRUE, la fila anterior pasa a FALSE. uq_pei_paciente_version_actual garantiza una sola versión vigente por paciente.';

--
-- Name: pei_id_pei_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pei_id_pei_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: pei_id_pei_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pei_id_pei_seq OWNED BY public.pei.id_pei;

--
-- Name: anamnesis id_anamnesis; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis ALTER COLUMN id_anamnesis SET DEFAULT nextval('public.anamnesis_id_anamnesis_seq'::regclass);

--
-- Name: consultas id_consulta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas ALTER COLUMN id_consulta SET DEFAULT nextval('public.consultas_id_consulta_seq'::regclass);

--
-- Name: derivaciones id_derivacion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivaciones ALTER COLUMN id_derivacion SET DEFAULT nextval('public.derivaciones_id_derivacion_seq'::regclass);

--
-- Name: notas_clinicas id_nota; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_clinicas ALTER COLUMN id_nota SET DEFAULT nextval('public.notas_clinicas_id_nota_seq'::regclass);

--
-- Name: pei id_pei; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pei ALTER COLUMN id_pei SET DEFAULT nextval('public.pei_id_pei_seq'::regclass);

--
-- Name: anamnesis anamnesis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis
    ADD CONSTRAINT anamnesis_pkey PRIMARY KEY (id_anamnesis);

--
-- Name: consultas consultas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_pkey PRIMARY KEY (id_consulta);

--
-- Name: derivaciones derivaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivaciones
    ADD CONSTRAINT derivaciones_pkey PRIMARY KEY (id_derivacion);

--
-- Name: notas_clinicas notas_clinicas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_clinicas
    ADD CONSTRAINT notas_clinicas_pkey PRIMARY KEY (id_nota);

--
-- Name: pei pei_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pei
    ADD CONSTRAINT pei_pkey PRIMARY KEY (id_pei);

--
-- Name: anamnesis uq_anamnesis_paciente_version; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis
    ADD CONSTRAINT uq_anamnesis_paciente_version UNIQUE (id_paciente, nro_version);

--
-- Name: consultas uq_consultas_cita; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT uq_consultas_cita UNIQUE (id_cita);

--
-- Name: pei uq_pei_paciente_version; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pei
    ADD CONSTRAINT uq_pei_paciente_version UNIQUE (id_paciente, nro_version);

--
-- Name: idx_anamnesis_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anamnesis_paciente ON public.anamnesis USING btree (id_paciente);

--
-- Name: idx_consultas_cita; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consultas_cita ON public.consultas USING btree (id_cita);

--
-- Name: idx_consultas_especialista_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consultas_especialista_fecha ON public.consultas USING btree (id_especialista, consulta_fecha);

--
-- Name: idx_consultas_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consultas_fecha ON public.consultas USING btree (((consulta_fecha)::date)) WHERE (est_consulta = true);

--
-- Name: idx_consultas_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consultas_paciente ON public.consultas USING btree (id_paciente);

--
-- Name: idx_derivaciones_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_derivaciones_consulta ON public.derivaciones USING btree (id_consulta) WHERE (est_derivacion = true);

--
-- Name: idx_notas_clinicas_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notas_clinicas_paciente ON public.notas_clinicas USING btree (id_paciente) WHERE (est_nota = true);

--
-- Name: idx_pei_especialista; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pei_especialista ON public.pei USING btree (id_especialista);

--
-- Name: idx_pei_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pei_paciente ON public.pei USING btree (id_paciente);

--
-- Name: uq_anamnesis_paciente_version_actual; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_anamnesis_paciente_version_actual ON public.anamnesis USING btree (id_paciente) WHERE es_version_actual;

--
-- Name: uq_pei_paciente_version_actual; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_pei_paciente_version_actual ON public.pei USING btree (id_paciente) WHERE es_version_actual;

--
-- Name: anamnesis trg_anamnesis_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_anamnesis_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.anamnesis FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_anamnesis');

--
-- Name: anamnesis trg_anamnesis_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_anamnesis_fecha_mod BEFORE UPDATE ON public.anamnesis FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: consultas trg_consultas_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_consultas_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.consultas FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_consulta');

--
-- Name: consultas trg_consultas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_consultas_fecha_mod BEFORE UPDATE ON public.consultas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: derivaciones trg_derivaciones_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_derivaciones_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.derivaciones FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_derivacion');

--
-- Name: derivaciones trg_derivaciones_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_derivaciones_fecha_mod BEFORE UPDATE ON public.derivaciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: notas_clinicas trg_notas_clinicas_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_notas_clinicas_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.notas_clinicas FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_nota');

--
-- Name: notas_clinicas trg_notas_clinicas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_notas_clinicas_fecha_mod BEFORE UPDATE ON public.notas_clinicas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: pei trg_pei_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pei_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.pei FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_pei');

--
-- Name: pei trg_pei_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pei_fecha_mod BEFORE UPDATE ON public.pei FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: anamnesis anamnesis_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis
    ADD CONSTRAINT anamnesis_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: anamnesis anamnesis_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis
    ADD CONSTRAINT anamnesis_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: anamnesis anamnesis_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anamnesis
    ADD CONSTRAINT anamnesis_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: consultas consultas_id_cita_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES public.citas(id_cita) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: consultas consultas_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: consultas consultas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: consultas consultas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: consultas consultas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: derivaciones derivaciones_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivaciones
    ADD CONSTRAINT derivaciones_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: derivaciones derivaciones_id_especialidad_destino_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivaciones
    ADD CONSTRAINT derivaciones_id_especialidad_destino_fkey FOREIGN KEY (id_especialidad_destino) REFERENCES public.especialidades(id_especialidad) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: derivaciones derivaciones_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivaciones
    ADD CONSTRAINT derivaciones_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: derivaciones derivaciones_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivaciones
    ADD CONSTRAINT derivaciones_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: notas_clinicas notas_clinicas_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_clinicas
    ADD CONSTRAINT notas_clinicas_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista);

--
-- Name: notas_clinicas notas_clinicas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_clinicas
    ADD CONSTRAINT notas_clinicas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente);

--
-- Name: notas_clinicas notas_clinicas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_clinicas
    ADD CONSTRAINT notas_clinicas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: notas_clinicas notas_clinicas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_clinicas
    ADD CONSTRAINT notas_clinicas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pei pei_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pei
    ADD CONSTRAINT pei_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: pei pei_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pei
    ADD CONSTRAINT pei_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: pei pei_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pei
    ADD CONSTRAINT pei_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pei pei_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pei
    ADD CONSTRAINT pei_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
