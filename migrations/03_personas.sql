-- 03_personas.sql — Personas, funcionarios, pacientes y especialistas
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: personas, funcionarios, pacientes, pacientes_menores, especialidades, especialistas, especialista_especialidades.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/03_personas.sql

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
-- Name: especialidades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.especialidades (
    id_especialidad integer NOT NULL,
    des_especialidad character varying(150) NOT NULL,
    est_especialidad boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
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
-- Name: especialista_especialidades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.especialista_especialidades (
    id_especialista_especialidad integer NOT NULL,
    id_especialista integer NOT NULL,
    id_especialidad integer NOT NULL,
    fecha_asignacion timestamp without time zone DEFAULT now() NOT NULL,
    est_especialista_especialidad boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: especialista_especialidades_id_especialista_especialidad_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.especialista_especialidades_id_especialista_especialidad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: especialista_especialidades_id_especialista_especialidad_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.especialista_especialidades_id_especialista_especialidad_seq OWNED BY public.especialista_especialidades.id_especialista_especialidad;

--
-- Name: especialistas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.especialistas (
    id_especialista integer NOT NULL,
    id_funcionario integer NOT NULL,
    esp_matricula character varying(50) NOT NULL,
    esp_color_agenda character varying(7) DEFAULT '#3498db'::character varying NOT NULL,
    est_especialista boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_especialistas_color CHECK (((esp_color_agenda)::text ~ '^#[0-9A-Fa-f]{6}$'::text))
);

--
-- Name: especialistas_id_especialista_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.especialistas_id_especialista_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: especialistas_id_especialista_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.especialistas_id_especialista_seq OWNED BY public.especialistas.id_especialista;

--
-- Name: funcionarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.funcionarios (
    id_funcionario integer NOT NULL,
    id_persona integer NOT NULL,
    id_cargo integer NOT NULL,
    est_funcionario boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
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
-- Name: pacientes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pacientes (
    id_paciente integer NOT NULL,
    id_persona integer NOT NULL,
    pac_es_menor boolean DEFAULT false NOT NULL,
    pac_historia_clinica text,
    pac_observaciones text,
    est_paciente boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
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
-- Name: pacientes_menores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pacientes_menores (
    id_paciente_menor integer NOT NULL,
    id_paciente integer NOT NULL,
    pam_nom_madre character varying(100),
    pam_tel_madre character varying(20),
    pam_nom_padre character varying(100),
    pam_tel_padre character varying(20),
    pam_educacion character varying(100),
    pam_colegio character varying(150),
    pam_tel_colegio character varying(20),
    est_paciente_menor boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: pacientes_menores_id_paciente_menor_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pacientes_menores_id_paciente_menor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: pacientes_menores_id_paciente_menor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pacientes_menores_id_paciente_menor_seq OWNED BY public.pacientes_menores.id_paciente_menor;

--
-- Name: personas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.personas (
    id_persona integer NOT NULL,
    per_nombre character varying(100) NOT NULL,
    per_apellido character varying(100) NOT NULL,
    per_cedula character varying(20) NOT NULL,
    per_telefono character varying(20) NOT NULL,
    per_correo character varying(100),
    per_domicilio text,
    per_fecha_nacimiento date,
    id_genero integer,
    id_estado_civil integer,
    id_ciudad integer,
    id_ciudad_nacimiento integer,
    id_nivel_instruccion integer,
    id_profesion integer,
    per_fecha_inscripcion timestamp without time zone DEFAULT now() NOT NULL,
    est_persona boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    per_tipo_documento character varying(3) DEFAULT 'CI'::character varying NOT NULL,
    per_ruc character varying(20)
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
-- Name: v_sesiones_activas; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_sesiones_activas AS
 SELECT u.id_usuario,
    u.usu_nick,
    concat(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
    count(s.id_sesion) AS cantidad_sesiones_activas,
    u.max_sesiones_simultaneas,
    max(s.fecha_ultimo_ping) AS ultima_actividad,
    string_agg(DISTINCT (s.ip_address)::text, ', '::text) AS ips_conectadas
   FROM (((public.usuarios u
     LEFT JOIN public.sesiones s ON (((s.id_usuario = u.id_usuario) AND (s.est_sesion = true) AND (s.fecha_expiracion > CURRENT_TIMESTAMP))))
     LEFT JOIN public.funcionarios f ON ((f.id_funcionario = u.id_funcionario)))
     LEFT JOIN public.personas p ON ((p.id_persona = f.id_persona)))
  GROUP BY u.id_usuario, u.usu_nick, p.per_nombre, p.per_apellido, u.max_sesiones_simultaneas
 HAVING ((count(s.id_sesion) > 0) OR (u.max_sesiones_simultaneas > 0));

--
-- Name: VIEW v_sesiones_activas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_sesiones_activas IS 'Resumen de sesiones activas por usuario con cantidad vs límite';

--
-- Name: especialidades id_especialidad; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades ALTER COLUMN id_especialidad SET DEFAULT nextval('public.especialidades_id_especialidad_seq'::regclass);

--
-- Name: especialista_especialidades id_especialista_especialidad; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialista_especialidades ALTER COLUMN id_especialista_especialidad SET DEFAULT nextval('public.especialista_especialidades_id_especialista_especialidad_seq'::regclass);

--
-- Name: especialistas id_especialista; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialistas ALTER COLUMN id_especialista SET DEFAULT nextval('public.especialistas_id_especialista_seq'::regclass);

--
-- Name: funcionarios id_funcionario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios ALTER COLUMN id_funcionario SET DEFAULT nextval('public.funcionarios_id_funcionario_seq'::regclass);

--
-- Name: pacientes id_paciente; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes ALTER COLUMN id_paciente SET DEFAULT nextval('public.pacientes_id_paciente_seq'::regclass);

--
-- Name: pacientes_menores id_paciente_menor; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes_menores ALTER COLUMN id_paciente_menor SET DEFAULT nextval('public.pacientes_menores_id_paciente_menor_seq'::regclass);

--
-- Name: personas id_persona; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas ALTER COLUMN id_persona SET DEFAULT nextval('public.personas_id_persona_seq'::regclass);

--
-- Name: especialidades especialidades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_pkey PRIMARY KEY (id_especialidad);

--
-- Name: especialista_especialidades especialista_especialidades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_pkey PRIMARY KEY (id_especialista_especialidad);

--
-- Name: especialistas especialistas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialistas
    ADD CONSTRAINT especialistas_pkey PRIMARY KEY (id_especialista);

--
-- Name: funcionarios funcionarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_pkey PRIMARY KEY (id_funcionario);

--
-- Name: pacientes_menores pacientes_menores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes_menores
    ADD CONSTRAINT pacientes_menores_pkey PRIMARY KEY (id_paciente_menor);

--
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (id_paciente);

--
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id_persona);

--
-- Name: especialidades uq_especialidades_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT uq_especialidades_des UNIQUE (des_especialidad);

--
-- Name: especialista_especialidades uq_especialista_especialidad; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialista_especialidades
    ADD CONSTRAINT uq_especialista_especialidad UNIQUE (id_especialista, id_especialidad);

--
-- Name: especialistas uq_especialistas_funcionario; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialistas
    ADD CONSTRAINT uq_especialistas_funcionario UNIQUE (id_funcionario);

--
-- Name: especialistas uq_especialistas_matricula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialistas
    ADD CONSTRAINT uq_especialistas_matricula UNIQUE (esp_matricula);

--
-- Name: funcionarios uq_funcionarios_persona; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT uq_funcionarios_persona UNIQUE (id_persona);

--
-- Name: pacientes_menores uq_pacientes_menores_paciente; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes_menores
    ADD CONSTRAINT uq_pacientes_menores_paciente UNIQUE (id_paciente);

--
-- Name: pacientes uq_pacientes_persona; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT uq_pacientes_persona UNIQUE (id_persona);

--
-- Name: personas uq_personas_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT uq_personas_cedula UNIQUE (per_cedula);

--
-- Name: idx_personas_cedula; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_personas_cedula ON public.personas USING btree (per_cedula);

--
-- Name: especialidades trg_especialidades_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_especialidades_fecha_mod BEFORE UPDATE ON public.especialidades FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: especialista_especialidades trg_especialista_especialidades_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_especialista_especialidades_fecha_mod BEFORE UPDATE ON public.especialista_especialidades FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: especialistas trg_especialistas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_especialistas_fecha_mod BEFORE UPDATE ON public.especialistas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: funcionarios trg_funcionarios_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_funcionarios_fecha_mod BEFORE UPDATE ON public.funcionarios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: pacientes trg_pacientes_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pacientes_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('AGENDAMIENTO', 'id_paciente');

--
-- Name: pacientes trg_pacientes_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pacientes_fecha_mod BEFORE UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: pacientes_menores trg_pacientes_menores_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pacientes_menores_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.pacientes_menores FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('AGENDAMIENTO', 'id_paciente_menor');

--
-- Name: pacientes_menores trg_pacientes_menores_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pacientes_menores_fecha_mod BEFORE UPDATE ON public.pacientes_menores FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: personas trg_personas_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_personas_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.personas FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('AGENDAMIENTO', 'id_persona');

--
-- Name: personas trg_personas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_personas_fecha_mod BEFORE UPDATE ON public.personas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: especialidades especialidades_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: especialidades especialidades_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: especialista_especialidades especialista_especialidades_id_especialidad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES public.especialidades(id_especialidad) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: especialista_especialidades especialista_especialidades_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: especialista_especialidades especialista_especialidades_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: especialista_especialidades especialista_especialidades_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialista_especialidades
    ADD CONSTRAINT especialista_especialidades_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: especialistas especialistas_id_funcionario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialistas
    ADD CONSTRAINT especialistas_id_funcionario_fkey FOREIGN KEY (id_funcionario) REFERENCES public.funcionarios(id_funcionario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: especialistas especialistas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialistas
    ADD CONSTRAINT especialistas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: especialistas especialistas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.especialistas
    ADD CONSTRAINT especialistas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: usuarios fk_usuarios_funcionario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_usuarios_funcionario FOREIGN KEY (id_funcionario) REFERENCES public.funcionarios(id_funcionario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: funcionarios funcionarios_id_cargo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_id_cargo_fkey FOREIGN KEY (id_cargo) REFERENCES public.cargos(id_cargo) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: funcionarios funcionarios_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: funcionarios funcionarios_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: funcionarios funcionarios_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pacientes pacientes_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: pacientes_menores pacientes_menores_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes_menores
    ADD CONSTRAINT pacientes_menores_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: pacientes_menores pacientes_menores_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes_menores
    ADD CONSTRAINT pacientes_menores_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pacientes_menores pacientes_menores_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes_menores
    ADD CONSTRAINT pacientes_menores_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pacientes pacientes_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pacientes pacientes_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: personas personas_id_ciudad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_ciudad_fkey FOREIGN KEY (id_ciudad) REFERENCES public.ciudades(id_ciudad) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: personas personas_id_ciudad_nacimiento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_ciudad_nacimiento_fkey FOREIGN KEY (id_ciudad_nacimiento) REFERENCES public.ciudades(id_ciudad) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: personas personas_id_estado_civil_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_estado_civil_fkey FOREIGN KEY (id_estado_civil) REFERENCES public.estados_civiles(id_estado_civil) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: personas personas_id_genero_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_genero_fkey FOREIGN KEY (id_genero) REFERENCES public.generos(id_genero) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: personas personas_id_nivel_instruccion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_nivel_instruccion_fkey FOREIGN KEY (id_nivel_instruccion) REFERENCES public.niveles_instruccion(id_nivel_instruccion) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: personas personas_id_profesion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_profesion_fkey FOREIGN KEY (id_profesion) REFERENCES public.profesiones(id_profesion) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: personas personas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: personas personas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
