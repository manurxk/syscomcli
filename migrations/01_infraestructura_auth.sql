-- 01_infraestructura_auth.sql — Infraestructura y autenticación
-- Generado el 2026-10-18 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: usuarios, sesiones, password_reset_tokens, mfa_codigos, mfa_dispositivos_confiables.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/01_infraestructura_auth.sql

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
-- Name: mfa_codigos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mfa_codigos (
    id_mfa_codigo integer NOT NULL,
    id_usuario integer NOT NULL,
    codigo character varying(6) NOT NULL,
    fecha_generacion timestamp without time zone DEFAULT now() NOT NULL,
    fecha_expiracion timestamp without time zone NOT NULL,
    usado boolean DEFAULT false NOT NULL,
    fecha_uso timestamp without time zone,
    intentos_validacion integer DEFAULT 0 NOT NULL,
    ip_solicitud character varying(45),
    user_agent text,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: mfa_codigos_id_mfa_codigo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mfa_codigos_id_mfa_codigo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: mfa_codigos_id_mfa_codigo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mfa_codigos_id_mfa_codigo_seq OWNED BY public.mfa_codigos.id_mfa_codigo;

--
-- Name: mfa_dispositivos_confiables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mfa_dispositivos_confiables (
    id_dispositivo integer NOT NULL,
    id_usuario integer NOT NULL,
    token character varying(100) NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_expiracion timestamp without time zone NOT NULL,
    ip_creacion character varying(45),
    user_agent text,
    revocado boolean DEFAULT false NOT NULL
);

--
-- Name: mfa_dispositivos_confiables_id_dispositivo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mfa_dispositivos_confiables_id_dispositivo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: mfa_dispositivos_confiables_id_dispositivo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mfa_dispositivos_confiables_id_dispositivo_seq OWNED BY public.mfa_dispositivos_confiables.id_dispositivo;

--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.password_reset_tokens (
    id_token integer NOT NULL,
    token uuid DEFAULT gen_random_uuid() NOT NULL,
    id_usuario integer NOT NULL,
    fecha_expiracion timestamp without time zone NOT NULL,
    usado boolean DEFAULT false NOT NULL,
    fecha_uso timestamp without time zone,
    ip_solicitud character varying(45),
    email_destino character varying(100),
    est_token boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: password_reset_tokens_id_token_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.password_reset_tokens_id_token_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: password_reset_tokens_id_token_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.password_reset_tokens_id_token_seq OWNED BY public.password_reset_tokens.id_token;

--
-- Name: sesiones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sesiones (
    id_sesion integer NOT NULL,
    id_usuario integer NOT NULL,
    token_sesion character varying(500) NOT NULL,
    csrf_token character varying(500),
    refresh_token character varying(500),
    fecha_inicio timestamp without time zone DEFAULT now() NOT NULL,
    fecha_ultimo_ping timestamp without time zone DEFAULT now() NOT NULL,
    fecha_expiracion timestamp without time zone NOT NULL,
    fecha_cierre timestamp without time zone,
    tipo_cierre character varying(20),
    ip_address character varying(45),
    user_agent text,
    est_sesion boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_sesiones_tipo_cierre CHECK (((tipo_cierre IS NULL) OR ((tipo_cierre)::text = ANY ((ARRAY['LOGOUT'::character varying, 'TIMEOUT'::character varying, 'ADMIN_FORCE'::character varying, 'SECURITY'::character varying, 'MFA_REVOKE'::character varying])::text[]))))
);

--
-- Name: sesiones_id_sesion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sesiones_id_sesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: sesiones_id_sesion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sesiones_id_sesion_seq OWNED BY public.sesiones.id_sesion;

--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    id_funcionario integer,
    usu_nick character varying(30) NOT NULL,
    usu_clave character varying(300) NOT NULL,
    usu_nro_intentos integer DEFAULT 0 NOT NULL,
    fecha_ultimo_intento_fallido timestamp without time zone,
    fecha_bloqueo timestamp without time zone,
    bloqueado_hasta timestamp without time zone,
    motivo_bloqueo character varying(200),
    fecha_ultimo_login timestamp without time zone,
    ip_ultimo_login character varying(45),
    user_agent_ultimo_login text,
    requiere_cambio_clave boolean DEFAULT false NOT NULL,
    fecha_cambio_clave timestamp without time zone,
    clave_nunca_expira boolean DEFAULT false NOT NULL,
    dias_validez_clave integer DEFAULT 90 NOT NULL,
    max_sesiones_simultaneas integer DEFAULT 1 NOT NULL,
    sesiones_activas integer DEFAULT 0 NOT NULL,
    est_usuario boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    mfa_habilitado boolean DEFAULT false NOT NULL,
    correo character varying(100),
    nivel_escalada_bloqueo integer DEFAULT 0 NOT NULL
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
-- Name: mfa_codigos id_mfa_codigo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_codigos ALTER COLUMN id_mfa_codigo SET DEFAULT nextval('public.mfa_codigos_id_mfa_codigo_seq'::regclass);

--
-- Name: mfa_dispositivos_confiables id_dispositivo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_dispositivos_confiables ALTER COLUMN id_dispositivo SET DEFAULT nextval('public.mfa_dispositivos_confiables_id_dispositivo_seq'::regclass);

--
-- Name: password_reset_tokens id_token; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens ALTER COLUMN id_token SET DEFAULT nextval('public.password_reset_tokens_id_token_seq'::regclass);

--
-- Name: sesiones id_sesion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sesiones ALTER COLUMN id_sesion SET DEFAULT nextval('public.sesiones_id_sesion_seq'::regclass);

--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);

--
-- Name: mfa_codigos mfa_codigos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_codigos
    ADD CONSTRAINT mfa_codigos_pkey PRIMARY KEY (id_mfa_codigo);

--
-- Name: mfa_dispositivos_confiables mfa_dispositivos_confiables_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_dispositivos_confiables
    ADD CONSTRAINT mfa_dispositivos_confiables_pkey PRIMARY KEY (id_dispositivo);

--
-- Name: mfa_dispositivos_confiables mfa_dispositivos_confiables_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_dispositivos_confiables
    ADD CONSTRAINT mfa_dispositivos_confiables_token_key UNIQUE (token);

--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id_token);

--
-- Name: sesiones sesiones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sesiones
    ADD CONSTRAINT sesiones_pkey PRIMARY KEY (id_sesion);

--
-- Name: password_reset_tokens uq_password_reset_token; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT uq_password_reset_token UNIQUE (token);

--
-- Name: usuarios uq_usuarios_nick; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT uq_usuarios_nick UNIQUE (usu_nick);

--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);

--
-- Name: idx_mfa_codigos_usuario; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mfa_codigos_usuario ON public.mfa_codigos USING btree (id_usuario);

--
-- Name: idx_mfa_disp_conf_token; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mfa_disp_conf_token ON public.mfa_dispositivos_confiables USING btree (token);

--
-- Name: idx_password_reset_usuario; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_password_reset_usuario ON public.password_reset_tokens USING btree (id_usuario);

--
-- Name: idx_sesiones_token; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_sesiones_token ON public.sesiones USING btree (token_sesion);

--
-- Name: idx_sesiones_usuario; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_sesiones_usuario ON public.sesiones USING btree (id_usuario);

--
-- Name: mfa_codigos tg_mfa_codigos_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_mfa_codigos_fmod BEFORE UPDATE ON public.mfa_codigos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: sesiones trg_sesiones_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_sesiones_fecha_mod BEFORE UPDATE ON public.sesiones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: usuarios trg_usuarios_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_usuarios_fecha_mod BEFORE UPDATE ON public.usuarios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: mfa_codigos mfa_codigos_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_codigos
    ADD CONSTRAINT mfa_codigos_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: mfa_codigos mfa_codigos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_codigos
    ADD CONSTRAINT mfa_codigos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: mfa_codigos mfa_codigos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_codigos
    ADD CONSTRAINT mfa_codigos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: mfa_dispositivos_confiables mfa_dispositivos_confiables_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_dispositivos_confiables
    ADD CONSTRAINT mfa_dispositivos_confiables_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);

--
-- Name: password_reset_tokens password_reset_tokens_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: password_reset_tokens password_reset_tokens_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: password_reset_tokens password_reset_tokens_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: sesiones sesiones_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sesiones
    ADD CONSTRAINT sesiones_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: sesiones sesiones_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sesiones
    ADD CONSTRAINT sesiones_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: sesiones sesiones_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sesiones
    ADD CONSTRAINT sesiones_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: usuarios usuarios_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: usuarios usuarios_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);


--
-- PostgreSQL database dump complete
--
