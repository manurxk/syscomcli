-- 10_ordenes_recetas_certificados.sql — Órdenes, recetas y certificados
-- Generado el 2026-10-19 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: ordenes, orden_detalle, recetas, receta_detalle, certificados_medicos.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/10_ordenes_recetas_certificados.sql

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
-- Name: certificados_medicos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.certificados_medicos (
    id_certificado integer NOT NULL,
    id_consulta integer NOT NULL,
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    id_tipo_certificado_medico integer NOT NULL,
    certificado_numero character varying(20) NOT NULL,
    certificado_fecha date NOT NULL,
    certificado_dias_reposo integer,
    certificado_desde_fecha date,
    certificado_hasta_fecha date,
    certificado_motivo text NOT NULL,
    certificado_diagnostico text,
    certificado_recomendaciones text,
    certificado_estado character varying(20) DEFAULT 'VIGENTE'::character varying NOT NULL,
    est_certificado boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_certificados_estado CHECK (((certificado_estado)::text = ANY ((ARRAY['VIGENTE'::character varying, 'ANULADO'::character varying])::text[])))
);

--
-- Name: TABLE certificados_medicos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.certificados_medicos IS 'Cubre certificado médico y justificativo médico (2 casos de uso de fundamentacion.md) vía id_tipo_certificado_medico = JUSTIFICATIVO, sin tabla aparte (ver decisión 3 en 02_MAPEO_FASES_NUEVA_BD.md).';

--
-- Name: certificados_medicos_id_certificado_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.certificados_medicos_id_certificado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: certificados_medicos_id_certificado_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.certificados_medicos_id_certificado_seq OWNED BY public.certificados_medicos.id_certificado;

--
-- Name: orden_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.orden_detalle (
    id_orden_detalle integer NOT NULL,
    id_orden integer NOT NULL,
    tipo_orden character varying(10) NOT NULL,
    id_tipo_estudio integer,
    id_tipo_analisis integer,
    detalle_resultado text,
    detalle_fecha_realizacion date,
    observaciones text,
    est_orden_detalle boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_orden_detalle_catalogo CHECK (((((tipo_orden)::text = 'ESTUDIO'::text) AND (id_tipo_estudio IS NOT NULL) AND (id_tipo_analisis IS NULL)) OR (((tipo_orden)::text = 'ANALISIS'::text) AND (id_tipo_analisis IS NOT NULL) AND (id_tipo_estudio IS NULL)))),
    CONSTRAINT chk_orden_detalle_tipo CHECK (((tipo_orden)::text = ANY ((ARRAY['ESTUDIO'::character varying, 'ANALISIS'::character varying])::text[])))
);

--
-- Name: COLUMN orden_detalle.detalle_resultado; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.orden_detalle.detalle_resultado IS 'Resultado del estudio o análisis. Reservado: la carga de resultados todavía no tiene pantalla.';

--
-- Name: COLUMN orden_detalle.detalle_fecha_realizacion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.orden_detalle.detalle_fecha_realizacion IS 'Fecha en que se realizó el estudio o análisis. Reservado: la carga de resultados todavía no tiene pantalla.';

--
-- Name: orden_detalle_id_orden_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.orden_detalle_id_orden_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: orden_detalle_id_orden_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.orden_detalle_id_orden_detalle_seq OWNED BY public.orden_detalle.id_orden_detalle;

--
-- Name: ordenes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ordenes (
    id_orden integer NOT NULL,
    id_consulta integer NOT NULL,
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    orden_numero character varying(20) NOT NULL,
    orden_fecha date NOT NULL,
    orden_estado character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    orden_observaciones text,
    orden_indicaciones text,
    est_orden boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_ordenes_estado CHECK (((orden_estado)::text = ANY ((ARRAY['PENDIENTE'::character varying, 'EN_PROCESO'::character varying, 'COMPLETADA'::character varying, 'ANULADA'::character varying])::text[])))
);

--
-- Name: TABLE ordenes; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.ordenes IS 'Cabecera unificada de orden de estudio y orden de análisis (ver decisión 2 en 02_MAPEO_FASES_NUEVA_BD.md). El tipo se define por línea en orden_detalle.tipo_orden, no en la cabecera.';

--
-- Name: ordenes_id_orden_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ordenes_id_orden_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: ordenes_id_orden_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ordenes_id_orden_seq OWNED BY public.ordenes.id_orden;

--
-- Name: receta_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.receta_detalle (
    id_receta_detalle integer NOT NULL,
    id_receta integer NOT NULL,
    id_medicamento integer NOT NULL,
    medicamento_dosis character varying(100) NOT NULL,
    medicamento_frecuencia character varying(100) NOT NULL,
    medicamento_duracion character varying(100),
    medicamento_cantidad numeric(10,2),
    medicamento_indicaciones text,
    est_receta_detalle boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

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
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    receta_numero character varying(20) NOT NULL,
    receta_fecha date NOT NULL,
    receta_validez_dias integer DEFAULT 30 NOT NULL,
    receta_indicaciones_generales text,
    receta_observaciones text,
    est_receta boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

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
-- Name: certificados_medicos id_certificado; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos ALTER COLUMN id_certificado SET DEFAULT nextval('public.certificados_medicos_id_certificado_seq'::regclass);

--
-- Name: orden_detalle id_orden_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_detalle ALTER COLUMN id_orden_detalle SET DEFAULT nextval('public.orden_detalle_id_orden_detalle_seq'::regclass);

--
-- Name: ordenes id_orden; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes ALTER COLUMN id_orden SET DEFAULT nextval('public.ordenes_id_orden_seq'::regclass);

--
-- Name: receta_detalle id_receta_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle ALTER COLUMN id_receta_detalle SET DEFAULT nextval('public.receta_detalle_id_receta_detalle_seq'::regclass);

--
-- Name: recetas id_receta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas ALTER COLUMN id_receta SET DEFAULT nextval('public.recetas_id_receta_seq'::regclass);

--
-- Name: certificados_medicos certificados_medicos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT certificados_medicos_pkey PRIMARY KEY (id_certificado);

--
-- Name: orden_detalle orden_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_detalle
    ADD CONSTRAINT orden_detalle_pkey PRIMARY KEY (id_orden_detalle);

--
-- Name: ordenes ordenes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_pkey PRIMARY KEY (id_orden);

--
-- Name: receta_detalle receta_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT receta_detalle_pkey PRIMARY KEY (id_receta_detalle);

--
-- Name: recetas recetas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_pkey PRIMARY KEY (id_receta);

--
-- Name: certificados_medicos uq_certificados_numero; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT uq_certificados_numero UNIQUE (certificado_numero);

--
-- Name: ordenes uq_ordenes_numero; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT uq_ordenes_numero UNIQUE (orden_numero);

--
-- Name: recetas uq_recetas_numero; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT uq_recetas_numero UNIQUE (receta_numero);

--
-- Name: idx_certificados_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_certificados_consulta ON public.certificados_medicos USING btree (id_consulta);

--
-- Name: idx_certificados_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_certificados_paciente ON public.certificados_medicos USING btree (id_paciente);

--
-- Name: idx_orden_detalle_orden; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_orden_detalle_orden ON public.orden_detalle USING btree (id_orden);

--
-- Name: idx_ordenes_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ordenes_consulta ON public.ordenes USING btree (id_consulta);

--
-- Name: idx_ordenes_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ordenes_paciente ON public.ordenes USING btree (id_paciente);

--
-- Name: idx_receta_detalle_receta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_receta_detalle_receta ON public.receta_detalle USING btree (id_receta);

--
-- Name: idx_recetas_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_recetas_consulta ON public.recetas USING btree (id_consulta);

--
-- Name: idx_recetas_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_recetas_paciente ON public.recetas USING btree (id_paciente);

--
-- Name: certificados_medicos trg_certificados_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_certificados_fecha_mod BEFORE UPDATE ON public.certificados_medicos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: certificados_medicos trg_certificados_medicos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_certificados_medicos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.certificados_medicos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_certificado');

--
-- Name: orden_detalle trg_orden_detalle_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_orden_detalle_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.orden_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_orden_detalle');

--
-- Name: orden_detalle trg_orden_detalle_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_orden_detalle_fecha_mod BEFORE UPDATE ON public.orden_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: ordenes trg_ordenes_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ordenes_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.ordenes FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_orden');

--
-- Name: ordenes trg_ordenes_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ordenes_fecha_mod BEFORE UPDATE ON public.ordenes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: receta_detalle trg_receta_detalle_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_receta_detalle_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.receta_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_receta_detalle');

--
-- Name: receta_detalle trg_receta_detalle_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_receta_detalle_fecha_mod BEFORE UPDATE ON public.receta_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: recetas trg_recetas_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_recetas_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.recetas FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_receta');

--
-- Name: recetas trg_recetas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_recetas_fecha_mod BEFORE UPDATE ON public.recetas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: certificados_medicos certificados_medicos_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT certificados_medicos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT certificados_medicos_id_consulta_fkey ON certificados_medicos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT certificados_medicos_id_consulta_fkey ON public.certificados_medicos IS 'RESTRICT: historia clínica; borrar la consulta no borra sus certificados (migración 107).';

--
-- Name: certificados_medicos certificados_medicos_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT certificados_medicos_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: certificados_medicos certificados_medicos_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT certificados_medicos_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: certificados_medicos certificados_medicos_id_tipo_certificado_medico_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT certificados_medicos_id_tipo_certificado_medico_fkey FOREIGN KEY (id_tipo_certificado_medico) REFERENCES public.tipos_certificados_medicos(id_tipo_certificado_medico);

--
-- Name: certificados_medicos certificados_medicos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT certificados_medicos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: certificados_medicos certificados_medicos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados_medicos
    ADD CONSTRAINT certificados_medicos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: orden_detalle orden_detalle_id_orden_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_detalle
    ADD CONSTRAINT orden_detalle_id_orden_fkey FOREIGN KEY (id_orden) REFERENCES public.ordenes(id_orden) ON DELETE CASCADE;

--
-- Name: orden_detalle orden_detalle_id_tipo_analisis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_detalle
    ADD CONSTRAINT orden_detalle_id_tipo_analisis_fkey FOREIGN KEY (id_tipo_analisis) REFERENCES public.tipos_analisis(id_tipo_analisis);

--
-- Name: orden_detalle orden_detalle_id_tipo_estudio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_detalle
    ADD CONSTRAINT orden_detalle_id_tipo_estudio_fkey FOREIGN KEY (id_tipo_estudio) REFERENCES public.tipos_estudios(id_tipo_estudio);

--
-- Name: orden_detalle orden_detalle_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_detalle
    ADD CONSTRAINT orden_detalle_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: orden_detalle orden_detalle_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orden_detalle
    ADD CONSTRAINT orden_detalle_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: ordenes ordenes_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT ordenes_id_consulta_fkey ON ordenes; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT ordenes_id_consulta_fkey ON public.ordenes IS 'RESTRICT: historia clínica; borrar la consulta no borra sus órdenes (migración 107).';

--
-- Name: ordenes ordenes_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: ordenes ordenes_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: ordenes ordenes_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: ordenes ordenes_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: receta_detalle receta_detalle_id_medicamento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT receta_detalle_id_medicamento_fkey FOREIGN KEY (id_medicamento) REFERENCES public.medicamentos(id_medicamento);

--
-- Name: receta_detalle receta_detalle_id_receta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT receta_detalle_id_receta_fkey FOREIGN KEY (id_receta) REFERENCES public.recetas(id_receta) ON DELETE CASCADE;

--
-- Name: receta_detalle receta_detalle_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT receta_detalle_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: receta_detalle receta_detalle_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receta_detalle
    ADD CONSTRAINT receta_detalle_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: recetas recetas_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT recetas_id_consulta_fkey ON recetas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT recetas_id_consulta_fkey ON public.recetas IS 'RESTRICT: historia clínica; borrar la consulta no borra sus recetas (migración 107).';

--
-- Name: recetas recetas_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: recetas recetas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: recetas recetas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: recetas recetas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
