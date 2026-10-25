-- 09_registro_clinico.sql — Registro clínico
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: insumos, registro_diagnosticos, registro_signos, registro_sintomas, registro_procedimientos, registro_insumos, tratamientos.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/09_registro_clinico.sql

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
-- Name: insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.insumos (
    id_insumo integer NOT NULL,
    des_insumo character varying(150) NOT NULL,
    insumo_unidad_medida character varying(20) DEFAULT 'UNIDAD'::character varying NOT NULL,
    stock_actual numeric(10,2) DEFAULT 0 NOT NULL,
    stock_minimo numeric(10,2) DEFAULT 0 NOT NULL,
    insumo_precio_unitario numeric(10,2),
    est_insumo boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_insumos_des CHECK (((des_insumo)::text ~ '^[A-Za-zÀ-ÿ0-9 .]+$'::text)),
    CONSTRAINT chk_insumos_precio CHECK (((insumo_precio_unitario IS NULL) OR (insumo_precio_unitario >= (0)::numeric))),
    CONSTRAINT chk_insumos_stock CHECK (((stock_actual >= (0)::numeric) AND (stock_minimo >= (0)::numeric)))
);

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
-- Name: registro_diagnosticos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registro_diagnosticos (
    id_registro_diagnostico integer NOT NULL,
    id_consulta integer NOT NULL,
    id_diagnostico integer NOT NULL,
    registro_tipo character varying(20) DEFAULT 'PRESUNTIVO'::character varying NOT NULL,
    registro_gravedad character varying(20),
    des_registro_diagnostico text,
    registro_observaciones text,
    est_registro_diagnostico boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_registro_diagnosticos_gravedad CHECK (((registro_gravedad IS NULL) OR ((registro_gravedad)::text = ANY (ARRAY[('LEVE'::character varying)::text, ('MODERADO'::character varying)::text, ('GRAVE'::character varying)::text])))),
    CONSTRAINT chk_registro_diagnosticos_tipo CHECK (((registro_tipo)::text = ANY (ARRAY[('PRESUNTIVO'::character varying)::text, ('DEFINITIVO'::character varying)::text, ('DIFERENCIAL'::character varying)::text])))
);

--
-- Name: TABLE registro_diagnosticos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.registro_diagnosticos IS 'Detalle de consultas (C.3), sin cabecera propia. ON DELETE CASCADE vía id_consulta.';

--
-- Name: registro_diagnosticos_id_registro_diagnostico_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registro_diagnosticos_id_registro_diagnostico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: registro_diagnosticos_id_registro_diagnostico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registro_diagnosticos_id_registro_diagnostico_seq OWNED BY public.registro_diagnosticos.id_registro_diagnostico;

--
-- Name: registro_insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registro_insumos (
    id_registro_insumo integer NOT NULL,
    id_consulta integer NOT NULL,
    id_insumo integer NOT NULL,
    registro_cantidad numeric(10,2) NOT NULL,
    registro_observaciones text,
    est_registro_insumo boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_registro_insumos_cantidad CHECK ((registro_cantidad > (0)::numeric))
);

--
-- Name: TABLE registro_insumos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.registro_insumos IS 'Detalle de consultas (C.3), sin cabecera propia. Descuenta stock_actual de insumos al registrar (y lo repone al desactivar). ON DELETE CASCADE vía id_consulta.';

--
-- Name: registro_insumos_id_registro_insumo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registro_insumos_id_registro_insumo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: registro_insumos_id_registro_insumo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registro_insumos_id_registro_insumo_seq OWNED BY public.registro_insumos.id_registro_insumo;

--
-- Name: registro_procedimientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registro_procedimientos (
    id_registro_procedimiento integer NOT NULL,
    id_consulta integer NOT NULL,
    id_tipo_procedimiento integer NOT NULL,
    des_registro_procedimiento text,
    registro_duracion integer,
    registro_resultado text,
    registro_observaciones text,
    est_registro_procedimiento boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: TABLE registro_procedimientos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.registro_procedimientos IS 'Detalle de consultas (C.3), sin cabecera propia. ON DELETE CASCADE vía id_consulta.';

--
-- Name: registro_procedimientos_id_registro_procedimiento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registro_procedimientos_id_registro_procedimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: registro_procedimientos_id_registro_procedimiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registro_procedimientos_id_registro_procedimiento_seq OWNED BY public.registro_procedimientos.id_registro_procedimiento;

--
-- Name: registro_signos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registro_signos (
    id_registro_signo integer NOT NULL,
    id_consulta integer NOT NULL,
    id_signo integer NOT NULL,
    registro_intensidad character varying(20),
    registro_observaciones text,
    est_registro_signo boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_registro_signos_intensidad CHECK (((registro_intensidad IS NULL) OR ((registro_intensidad)::text = ANY (ARRAY[('LEVE'::character varying)::text, ('MODERADO'::character varying)::text, ('GRAVE'::character varying)::text]))))
);

--
-- Name: TABLE registro_signos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.registro_signos IS 'Detalle de consultas (C.3), sin cabecera propia. ON DELETE CASCADE vía id_consulta.';

--
-- Name: registro_signos_id_registro_signo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registro_signos_id_registro_signo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: registro_signos_id_registro_signo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registro_signos_id_registro_signo_seq OWNED BY public.registro_signos.id_registro_signo;

--
-- Name: registro_sintomas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registro_sintomas (
    id_registro_sintoma integer NOT NULL,
    id_consulta integer NOT NULL,
    id_sintoma integer NOT NULL,
    registro_intensidad character varying(20),
    registro_observaciones text,
    est_registro_sintoma boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_registro_sintomas_intensidad CHECK (((registro_intensidad IS NULL) OR ((registro_intensidad)::text = ANY (ARRAY[('LEVE'::character varying)::text, ('MODERADO'::character varying)::text, ('GRAVE'::character varying)::text]))))
);

--
-- Name: TABLE registro_sintomas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.registro_sintomas IS 'Detalle de consultas (C.3), sin cabecera propia. ON DELETE CASCADE vía id_consulta.';

--
-- Name: registro_sintomas_id_registro_sintoma_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registro_sintomas_id_registro_sintoma_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: registro_sintomas_id_registro_sintoma_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registro_sintomas_id_registro_sintoma_seq OWNED BY public.registro_sintomas.id_registro_sintoma;

--
-- Name: tratamientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tratamientos (
    id_tratamiento integer NOT NULL,
    id_consulta integer NOT NULL,
    id_tipo_tratamiento integer NOT NULL,
    des_tratamiento text NOT NULL,
    tratamiento_objetivos text,
    numero_sesiones integer,
    frecuencia_sesiones character varying(50),
    duracion_sesion integer,
    tratamiento_fecha_inicio date NOT NULL,
    tratamiento_fecha_fin date,
    tratamiento_estado character varying(20) DEFAULT 'ACTIVO'::character varying NOT NULL,
    tratamiento_observaciones text,
    est_tratamiento boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_tratamientos_estado CHECK (((tratamiento_estado)::text = ANY (ARRAY[('ACTIVO'::character varying)::text, ('FINALIZADO'::character varying)::text, ('SUSPENDIDO'::character varying)::text])))
);

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
-- Name: v_consultas_resumen; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_consultas_resumen AS
 SELECT c.id_consulta,
    (c.consulta_fecha)::date AS fecha,
    c.consulta_fecha,
    c.consulta_estado,
    c.id_paciente,
    c.id_especialista,
    concat(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
    COALESCE(cit.id_especialidad, ( SELECT min(ee.id_especialidad) AS min
           FROM public.especialista_especialidades ee
          WHERE ((ee.id_especialista = c.id_especialista) AND (ee.est_especialista_especialidad = true)))) AS id_especialidad,
    cit.cita_es_primera_vez,
    rd.id_diagnostico,
    d.cod_cie10,
    d.des_diagnostico
   FROM ((((((public.consultas c
     JOIN public.especialistas e ON ((e.id_especialista = c.id_especialista)))
     JOIN public.funcionarios f ON ((f.id_funcionario = e.id_funcionario)))
     JOIN public.personas pe ON ((pe.id_persona = f.id_persona)))
     LEFT JOIN public.citas cit ON ((cit.id_cita = c.id_cita)))
     LEFT JOIN public.registro_diagnosticos rd ON (((rd.id_consulta = c.id_consulta) AND (rd.est_registro_diagnostico = true))))
     LEFT JOIN public.diagnosticos d ON ((d.id_diagnostico = rd.id_diagnostico)))
  WHERE (c.est_consulta = true);

--
-- Name: VIEW v_consultas_resumen; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_consultas_resumen IS 'Una fila por consulta activa y por diagnóstico registrado (una consulta sin diagnóstico aparece una vez, con diagnóstico nulo). Para contar consultas usar COUNT(DISTINCT id_consulta). Filtrar por fecha y, según el rol, por id_especialista. Fuente de la pestaña Consultorio. No expone nombres de pacientes.';

--
-- Name: insumos id_insumo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos ALTER COLUMN id_insumo SET DEFAULT nextval('public.insumos_id_insumo_seq'::regclass);

--
-- Name: registro_diagnosticos id_registro_diagnostico; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_diagnosticos ALTER COLUMN id_registro_diagnostico SET DEFAULT nextval('public.registro_diagnosticos_id_registro_diagnostico_seq'::regclass);

--
-- Name: registro_insumos id_registro_insumo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_insumos ALTER COLUMN id_registro_insumo SET DEFAULT nextval('public.registro_insumos_id_registro_insumo_seq'::regclass);

--
-- Name: registro_procedimientos id_registro_procedimiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_procedimientos ALTER COLUMN id_registro_procedimiento SET DEFAULT nextval('public.registro_procedimientos_id_registro_procedimiento_seq'::regclass);

--
-- Name: registro_signos id_registro_signo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_signos ALTER COLUMN id_registro_signo SET DEFAULT nextval('public.registro_signos_id_registro_signo_seq'::regclass);

--
-- Name: registro_sintomas id_registro_sintoma; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_sintomas ALTER COLUMN id_registro_sintoma SET DEFAULT nextval('public.registro_sintomas_id_registro_sintoma_seq'::regclass);

--
-- Name: tratamientos id_tratamiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos ALTER COLUMN id_tratamiento SET DEFAULT nextval('public.tratamientos_id_tratamiento_seq'::regclass);

--
-- Name: insumos insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_pkey PRIMARY KEY (id_insumo);

--
-- Name: registro_diagnosticos registro_diagnosticos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_diagnosticos
    ADD CONSTRAINT registro_diagnosticos_pkey PRIMARY KEY (id_registro_diagnostico);

--
-- Name: registro_insumos registro_insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_insumos
    ADD CONSTRAINT registro_insumos_pkey PRIMARY KEY (id_registro_insumo);

--
-- Name: registro_procedimientos registro_procedimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_procedimientos
    ADD CONSTRAINT registro_procedimientos_pkey PRIMARY KEY (id_registro_procedimiento);

--
-- Name: registro_signos registro_signos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_signos
    ADD CONSTRAINT registro_signos_pkey PRIMARY KEY (id_registro_signo);

--
-- Name: registro_sintomas registro_sintomas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_sintomas
    ADD CONSTRAINT registro_sintomas_pkey PRIMARY KEY (id_registro_sintoma);

--
-- Name: tratamientos tratamientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT tratamientos_pkey PRIMARY KEY (id_tratamiento);

--
-- Name: insumos uq_insumos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT uq_insumos_des UNIQUE (des_insumo);

--
-- Name: idx_registro_diagnosticos_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registro_diagnosticos_consulta ON public.registro_diagnosticos USING btree (id_consulta);

--
-- Name: idx_registro_insumos_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registro_insumos_consulta ON public.registro_insumos USING btree (id_consulta);

--
-- Name: idx_registro_procedimientos_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registro_procedimientos_consulta ON public.registro_procedimientos USING btree (id_consulta);

--
-- Name: idx_registro_signos_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registro_signos_consulta ON public.registro_signos USING btree (id_consulta);

--
-- Name: idx_registro_sintomas_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registro_sintomas_consulta ON public.registro_sintomas USING btree (id_consulta);

--
-- Name: idx_tratamientos_consulta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tratamientos_consulta ON public.tratamientos USING btree (id_consulta);

--
-- Name: insumos trg_insumos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_insumos_fecha_mod BEFORE UPDATE ON public.insumos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: registro_diagnosticos trg_registro_diagnosticos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_diagnosticos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.registro_diagnosticos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_registro_diagnostico');

--
-- Name: registro_diagnosticos trg_registro_diagnosticos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_diagnosticos_fecha_mod BEFORE UPDATE ON public.registro_diagnosticos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: registro_insumos trg_registro_insumos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_insumos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.registro_insumos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_registro_insumo');

--
-- Name: registro_insumos trg_registro_insumos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_insumos_fecha_mod BEFORE UPDATE ON public.registro_insumos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: registro_procedimientos trg_registro_procedimientos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_procedimientos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.registro_procedimientos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_registro_procedimiento');

--
-- Name: registro_procedimientos trg_registro_procedimientos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_procedimientos_fecha_mod BEFORE UPDATE ON public.registro_procedimientos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: registro_signos trg_registro_signos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_signos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.registro_signos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_registro_signo');

--
-- Name: registro_signos trg_registro_signos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_signos_fecha_mod BEFORE UPDATE ON public.registro_signos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: registro_sintomas trg_registro_sintomas_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_sintomas_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.registro_sintomas FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_registro_sintoma');

--
-- Name: registro_sintomas trg_registro_sintomas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registro_sintomas_fecha_mod BEFORE UPDATE ON public.registro_sintomas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tratamientos trg_tratamientos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tratamientos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.tratamientos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('CLINICO', 'id_tratamiento');

--
-- Name: tratamientos trg_tratamientos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tratamientos_fecha_mod BEFORE UPDATE ON public.tratamientos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: insumos insumos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: insumos insumos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_diagnosticos registro_diagnosticos_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_diagnosticos
    ADD CONSTRAINT registro_diagnosticos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT registro_diagnosticos_id_consulta_fkey ON registro_diagnosticos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT registro_diagnosticos_id_consulta_fkey ON public.registro_diagnosticos IS 'RESTRICT: historia clínica; borrar la consulta no borra sus diagnósticos (migración 107).';

--
-- Name: registro_diagnosticos registro_diagnosticos_id_diagnostico_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_diagnosticos
    ADD CONSTRAINT registro_diagnosticos_id_diagnostico_fkey FOREIGN KEY (id_diagnostico) REFERENCES public.diagnosticos(id_diagnostico);

--
-- Name: registro_diagnosticos registro_diagnosticos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_diagnosticos
    ADD CONSTRAINT registro_diagnosticos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_diagnosticos registro_diagnosticos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_diagnosticos
    ADD CONSTRAINT registro_diagnosticos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_insumos registro_insumos_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_insumos
    ADD CONSTRAINT registro_insumos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT registro_insumos_id_consulta_fkey ON registro_insumos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT registro_insumos_id_consulta_fkey ON public.registro_insumos IS 'RESTRICT: historia clínica; borrar la consulta no borra sus insumos (migración 107).';

--
-- Name: registro_insumos registro_insumos_id_insumo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_insumos
    ADD CONSTRAINT registro_insumos_id_insumo_fkey FOREIGN KEY (id_insumo) REFERENCES public.insumos(id_insumo);

--
-- Name: registro_insumos registro_insumos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_insumos
    ADD CONSTRAINT registro_insumos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_insumos registro_insumos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_insumos
    ADD CONSTRAINT registro_insumos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_procedimientos registro_procedimientos_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_procedimientos
    ADD CONSTRAINT registro_procedimientos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT registro_procedimientos_id_consulta_fkey ON registro_procedimientos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT registro_procedimientos_id_consulta_fkey ON public.registro_procedimientos IS 'RESTRICT: historia clínica; borrar la consulta no borra sus procedimientos (migración 107).';

--
-- Name: registro_procedimientos registro_procedimientos_id_tipo_procedimiento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_procedimientos
    ADD CONSTRAINT registro_procedimientos_id_tipo_procedimiento_fkey FOREIGN KEY (id_tipo_procedimiento) REFERENCES public.tipos_procedimientos(id_tipo_procedimiento);

--
-- Name: registro_procedimientos registro_procedimientos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_procedimientos
    ADD CONSTRAINT registro_procedimientos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_procedimientos registro_procedimientos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_procedimientos
    ADD CONSTRAINT registro_procedimientos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_signos registro_signos_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_signos
    ADD CONSTRAINT registro_signos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT registro_signos_id_consulta_fkey ON registro_signos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT registro_signos_id_consulta_fkey ON public.registro_signos IS 'RESTRICT: historia clínica; borrar la consulta no borra sus signos (migración 107).';

--
-- Name: registro_signos registro_signos_id_signo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_signos
    ADD CONSTRAINT registro_signos_id_signo_fkey FOREIGN KEY (id_signo) REFERENCES public.signos(id_signo);

--
-- Name: registro_signos registro_signos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_signos
    ADD CONSTRAINT registro_signos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_signos registro_signos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_signos
    ADD CONSTRAINT registro_signos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_sintomas registro_sintomas_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_sintomas
    ADD CONSTRAINT registro_sintomas_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT registro_sintomas_id_consulta_fkey ON registro_sintomas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT registro_sintomas_id_consulta_fkey ON public.registro_sintomas IS 'RESTRICT: historia clínica; borrar la consulta no borra sus síntomas (migración 107).';

--
-- Name: registro_sintomas registro_sintomas_id_sintoma_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_sintomas
    ADD CONSTRAINT registro_sintomas_id_sintoma_fkey FOREIGN KEY (id_sintoma) REFERENCES public.sintomas(id_sintoma);

--
-- Name: registro_sintomas registro_sintomas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_sintomas
    ADD CONSTRAINT registro_sintomas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: registro_sintomas registro_sintomas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registro_sintomas
    ADD CONSTRAINT registro_sintomas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tratamientos tratamientos_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT tratamientos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta) ON DELETE RESTRICT;

--
-- Name: CONSTRAINT tratamientos_id_consulta_fkey ON tratamientos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT tratamientos_id_consulta_fkey ON public.tratamientos IS 'RESTRICT: historia clínica; borrar la consulta no borra sus tratamientos (migración 107).';

--
-- Name: tratamientos tratamientos_id_tipo_tratamiento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT tratamientos_id_tipo_tratamiento_fkey FOREIGN KEY (id_tipo_tratamiento) REFERENCES public.tipos_tratamientos(id_tipo_tratamiento);

--
-- Name: tratamientos tratamientos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT tratamientos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tratamientos tratamientos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT tratamientos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
