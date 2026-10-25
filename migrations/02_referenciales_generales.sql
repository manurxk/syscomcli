-- 02_referenciales_generales.sql — Referenciales generales
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: generos, estados_civiles, paises, departamentos, ciudades, profesiones, niveles_instruccion, cargos, modulos, paginas.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/02_referenciales_generales.sql

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
-- Name: cargos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cargos (
    id_cargo integer NOT NULL,
    des_cargo character varying(60) NOT NULL,
    est_cargo boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    es_clinico boolean DEFAULT false NOT NULL,
    CONSTRAINT chk_cargos_des CHECK (((des_cargo)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: cargos_id_cargo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cargos_id_cargo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: cargos_id_cargo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cargos_id_cargo_seq OWNED BY public.cargos.id_cargo;

--
-- Name: ciudades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ciudades (
    id_ciudad integer NOT NULL,
    id_departamento integer NOT NULL,
    des_ciudad character varying(100) NOT NULL,
    est_ciudad boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_ciudades_des CHECK (((des_ciudad)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
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
-- Name: departamentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departamentos (
    id_departamento integer NOT NULL,
    id_pais integer NOT NULL,
    des_departamento character varying(100) NOT NULL,
    est_departamento boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_departamentos_des CHECK (((des_departamento)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: departamentos_id_departamento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.departamentos_id_departamento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: departamentos_id_departamento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.departamentos_id_departamento_seq OWNED BY public.departamentos.id_departamento;

--
-- Name: estados_civiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estados_civiles (
    id_estado_civil integer NOT NULL,
    des_estado_civil character varying(50) NOT NULL,
    est_estado_civil boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_estados_civiles_des CHECK (((des_estado_civil)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: estados_civiles_id_estado_civil_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estados_civiles_id_estado_civil_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: estados_civiles_id_estado_civil_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estados_civiles_id_estado_civil_seq OWNED BY public.estados_civiles.id_estado_civil;

--
-- Name: generos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.generos (
    id_genero integer NOT NULL,
    des_genero character varying(50) NOT NULL,
    est_genero boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_generos_des CHECK (((des_genero)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
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
-- Name: modulos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.modulos (
    id_modulo integer NOT NULL,
    des_modulo character varying(60) NOT NULL,
    est_modulo boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: modulos_id_modulo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.modulos_id_modulo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: modulos_id_modulo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.modulos_id_modulo_seq OWNED BY public.modulos.id_modulo;

--
-- Name: niveles_instruccion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.niveles_instruccion (
    id_nivel_instruccion integer NOT NULL,
    des_nivel_instruccion character varying(100) NOT NULL,
    est_nivel_instruccion boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_niveles_instruccion_des CHECK (((des_nivel_instruccion)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: niveles_instruccion_id_nivel_instruccion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.niveles_instruccion_id_nivel_instruccion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: niveles_instruccion_id_nivel_instruccion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.niveles_instruccion_id_nivel_instruccion_seq OWNED BY public.niveles_instruccion.id_nivel_instruccion;

--
-- Name: paginas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paginas (
    id_pagina integer NOT NULL,
    id_modulo integer NOT NULL,
    des_pagina character varying(60) NOT NULL,
    pag_direccion text NOT NULL,
    est_pagina boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    icono character varying(60),
    orden integer DEFAULT 0 NOT NULL,
    grupo_menu character varying(60),
    descripcion character varying(150)
);

--
-- Name: COLUMN paginas.descripcion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.paginas.descripcion IS 'Descripción corta de la página; se muestra como tooltip en el menú lateral';

--
-- Name: paginas_id_pagina_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.paginas_id_pagina_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: paginas_id_pagina_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.paginas_id_pagina_seq OWNED BY public.paginas.id_pagina;

--
-- Name: paises; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paises (
    id_pais integer NOT NULL,
    des_pais character varying(100) NOT NULL,
    cod_pais character varying(3),
    est_pais boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_paises_des CHECK (((des_pais)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: paises_id_pais_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.paises_id_pais_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: paises_id_pais_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.paises_id_pais_seq OWNED BY public.paises.id_pais;

--
-- Name: profesiones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.profesiones (
    id_profesion integer NOT NULL,
    des_profesion character varying(150) NOT NULL,
    est_profesion boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_profesiones_des CHECK (((des_profesion)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: profesiones_id_profesion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.profesiones_id_profesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: profesiones_id_profesion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.profesiones_id_profesion_seq OWNED BY public.profesiones.id_profesion;

--
-- Name: cargos id_cargo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cargos ALTER COLUMN id_cargo SET DEFAULT nextval('public.cargos_id_cargo_seq'::regclass);

--
-- Name: ciudades id_ciudad; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades ALTER COLUMN id_ciudad SET DEFAULT nextval('public.ciudades_id_ciudad_seq'::regclass);

--
-- Name: departamentos id_departamento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos ALTER COLUMN id_departamento SET DEFAULT nextval('public.departamentos_id_departamento_seq'::regclass);

--
-- Name: estados_civiles id_estado_civil; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_civiles ALTER COLUMN id_estado_civil SET DEFAULT nextval('public.estados_civiles_id_estado_civil_seq'::regclass);

--
-- Name: generos id_genero; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos ALTER COLUMN id_genero SET DEFAULT nextval('public.generos_id_genero_seq'::regclass);

--
-- Name: modulos id_modulo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modulos ALTER COLUMN id_modulo SET DEFAULT nextval('public.modulos_id_modulo_seq'::regclass);

--
-- Name: niveles_instruccion id_nivel_instruccion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.niveles_instruccion ALTER COLUMN id_nivel_instruccion SET DEFAULT nextval('public.niveles_instruccion_id_nivel_instruccion_seq'::regclass);

--
-- Name: paginas id_pagina; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paginas ALTER COLUMN id_pagina SET DEFAULT nextval('public.paginas_id_pagina_seq'::regclass);

--
-- Name: paises id_pais; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paises ALTER COLUMN id_pais SET DEFAULT nextval('public.paises_id_pais_seq'::regclass);

--
-- Name: profesiones id_profesion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profesiones ALTER COLUMN id_profesion SET DEFAULT nextval('public.profesiones_id_profesion_seq'::regclass);

--
-- Name: cargos cargos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_pkey PRIMARY KEY (id_cargo);

--
-- Name: ciudades ciudades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades
    ADD CONSTRAINT ciudades_pkey PRIMARY KEY (id_ciudad);

--
-- Name: departamentos departamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_pkey PRIMARY KEY (id_departamento);

--
-- Name: estados_civiles estados_civiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_civiles
    ADD CONSTRAINT estados_civiles_pkey PRIMARY KEY (id_estado_civil);

--
-- Name: generos generos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos
    ADD CONSTRAINT generos_pkey PRIMARY KEY (id_genero);

--
-- Name: modulos modulos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modulos
    ADD CONSTRAINT modulos_pkey PRIMARY KEY (id_modulo);

--
-- Name: niveles_instruccion niveles_instruccion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.niveles_instruccion
    ADD CONSTRAINT niveles_instruccion_pkey PRIMARY KEY (id_nivel_instruccion);

--
-- Name: paginas paginas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paginas
    ADD CONSTRAINT paginas_pkey PRIMARY KEY (id_pagina);

--
-- Name: paises paises_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paises
    ADD CONSTRAINT paises_pkey PRIMARY KEY (id_pais);

--
-- Name: profesiones profesiones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profesiones
    ADD CONSTRAINT profesiones_pkey PRIMARY KEY (id_profesion);

--
-- Name: cargos uq_cargos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT uq_cargos_des UNIQUE (des_cargo);

--
-- Name: ciudades uq_ciudades_depto_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades
    ADD CONSTRAINT uq_ciudades_depto_des UNIQUE (id_departamento, des_ciudad);

--
-- Name: departamentos uq_departamentos_pais_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT uq_departamentos_pais_des UNIQUE (id_pais, des_departamento);

--
-- Name: estados_civiles uq_estados_civiles_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_civiles
    ADD CONSTRAINT uq_estados_civiles_des UNIQUE (des_estado_civil);

--
-- Name: generos uq_generos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos
    ADD CONSTRAINT uq_generos_des UNIQUE (des_genero);

--
-- Name: modulos uq_modulos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modulos
    ADD CONSTRAINT uq_modulos_des UNIQUE (des_modulo);

--
-- Name: niveles_instruccion uq_niveles_instruccion_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.niveles_instruccion
    ADD CONSTRAINT uq_niveles_instruccion_des UNIQUE (des_nivel_instruccion);

--
-- Name: paises uq_paises_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paises
    ADD CONSTRAINT uq_paises_des UNIQUE (des_pais);

--
-- Name: profesiones uq_profesiones_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profesiones
    ADD CONSTRAINT uq_profesiones_des UNIQUE (des_profesion);

--
-- Name: idx_ciudades_departamento; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ciudades_departamento ON public.ciudades USING btree (id_departamento);

--
-- Name: idx_departamentos_pais; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_departamentos_pais ON public.departamentos USING btree (id_pais);

--
-- Name: idx_paginas_modulo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_paginas_modulo ON public.paginas USING btree (id_modulo);

--
-- Name: cargos trg_cargos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_cargos_fecha_mod BEFORE UPDATE ON public.cargos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: ciudades trg_ciudades_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ciudades_fecha_mod BEFORE UPDATE ON public.ciudades FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: departamentos trg_departamentos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_departamentos_fecha_mod BEFORE UPDATE ON public.departamentos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: estados_civiles trg_estados_civiles_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_estados_civiles_fecha_mod BEFORE UPDATE ON public.estados_civiles FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: generos trg_generos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generos_fecha_mod BEFORE UPDATE ON public.generos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: modulos trg_modulos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_modulos_fecha_mod BEFORE UPDATE ON public.modulos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: niveles_instruccion trg_niveles_instruccion_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_niveles_instruccion_fecha_mod BEFORE UPDATE ON public.niveles_instruccion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: paginas trg_paginas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_paginas_fecha_mod BEFORE UPDATE ON public.paginas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: paises trg_paises_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_paises_fecha_mod BEFORE UPDATE ON public.paises FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: profesiones trg_profesiones_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_profesiones_fecha_mod BEFORE UPDATE ON public.profesiones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: cargos cargos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: cargos cargos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: ciudades ciudades_id_departamento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades
    ADD CONSTRAINT ciudades_id_departamento_fkey FOREIGN KEY (id_departamento) REFERENCES public.departamentos(id_departamento) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: ciudades ciudades_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades
    ADD CONSTRAINT ciudades_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: ciudades ciudades_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ciudades
    ADD CONSTRAINT ciudades_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: departamentos departamentos_id_pais_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_id_pais_fkey FOREIGN KEY (id_pais) REFERENCES public.paises(id_pais) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: departamentos departamentos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: departamentos departamentos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: estados_civiles estados_civiles_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_civiles
    ADD CONSTRAINT estados_civiles_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: estados_civiles estados_civiles_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_civiles
    ADD CONSTRAINT estados_civiles_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: generos generos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos
    ADD CONSTRAINT generos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: generos generos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generos
    ADD CONSTRAINT generos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: modulos modulos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modulos
    ADD CONSTRAINT modulos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: modulos modulos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modulos
    ADD CONSTRAINT modulos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: niveles_instruccion niveles_instruccion_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.niveles_instruccion
    ADD CONSTRAINT niveles_instruccion_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: niveles_instruccion niveles_instruccion_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.niveles_instruccion
    ADD CONSTRAINT niveles_instruccion_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: paginas paginas_id_modulo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paginas
    ADD CONSTRAINT paginas_id_modulo_fkey FOREIGN KEY (id_modulo) REFERENCES public.modulos(id_modulo) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: paginas paginas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paginas
    ADD CONSTRAINT paginas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: paginas paginas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paginas
    ADD CONSTRAINT paginas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: paises paises_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paises
    ADD CONSTRAINT paises_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: paises paises_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paises
    ADD CONSTRAINT paises_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: profesiones profesiones_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profesiones
    ADD CONSTRAINT profesiones_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: profesiones profesiones_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profesiones
    ADD CONSTRAINT profesiones_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
