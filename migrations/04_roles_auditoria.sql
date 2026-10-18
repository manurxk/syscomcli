-- 04_roles_auditoria.sql — Roles, permisos, accesos y auditoría
-- Generado el 2026-10-18 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: roles, usuarios_roles, acciones, roles_permisos, roles_paginas, accesos_sistema, auditoria_sistema.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/04_roles_auditoria.sql

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
-- Name: accesos_sistema; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accesos_sistema (
    id_acceso integer NOT NULL,
    id_usuario integer,
    usuario_intentado character varying(30) NOT NULL,
    resultado character varying(30) NOT NULL,
    ip_origen inet,
    user_agent text,
    csrf_valido boolean,
    fecha_intento timestamp without time zone DEFAULT now() NOT NULL,
    est_acceso boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_accesos_resultado CHECK (((resultado)::text = ANY ((ARRAY['EXITOSO'::character varying, 'FALLIDO_CLAVE'::character varying, 'FALLIDO_BLOQUEADO'::character varying, 'FALLIDO_USUARIO_INEXISTENTE'::character varying, 'FALLIDO_SESIONES_MAXIMAS'::character varying])::text[])))
);

--
-- Name: COLUMN accesos_sistema.csrf_valido; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.accesos_sistema.csrf_valido IS 'Resultado de la validación CSRF del intento. Parámetro de registrar_intento_login; hoy la app no lo informa (queda NULL).';

--
-- Name: accesos_sistema_id_acceso_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.accesos_sistema_id_acceso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: accesos_sistema_id_acceso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.accesos_sistema_id_acceso_seq OWNED BY public.accesos_sistema.id_acceso;

--
-- Name: acciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.acciones (
    id_accion integer NOT NULL,
    cod_accion character varying(20) NOT NULL,
    des_accion character varying(60) NOT NULL,
    est_accion boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_acciones_cod CHECK (((cod_accion)::text = ANY ((ARRAY['LEER'::character varying, 'CREAR'::character varying, 'EDITAR'::character varying, 'ELIMINAR'::character varying])::text[])))
);

--
-- Name: acciones_id_accion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.acciones_id_accion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: acciones_id_accion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.acciones_id_accion_seq OWNED BY public.acciones.id_accion;

--
-- Name: auditoria_sistema; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auditoria_sistema (
    id_auditoria integer NOT NULL,
    id_usuario integer,
    accion character varying(30) NOT NULL,
    detalle text,
    ip_origen inet,
    fecha_evento timestamp without time zone DEFAULT now() NOT NULL,
    est_auditoria boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_auditoria_accion CHECK (((accion)::text = ANY ((ARRAY['LOGIN'::character varying, 'LOGOUT'::character varying, 'LOGIN_FAILED'::character varying, 'PROFILE_UPDATE'::character varying, 'RECORD_CREATE'::character varying, 'RECORD_UPDATE'::character varying, 'RECORD_DELETE'::character varying, 'PASSWORD_CHANGE'::character varying, 'REPORT_VIEW'::character varying, 'RATE_LIMIT'::character varying, 'ACCOUNT_LOCKED'::character varying, 'ACCOUNT_UNLOCKED'::character varying])::text[])))
);

--
-- Name: TABLE auditoria_sistema; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.auditoria_sistema IS 'Bitácora de acciones auditables del usuario (login/logout y eventos de negocio). Valores de accion definidos en app/utils/auditoria_constantes.py:AuditAccion.';

--
-- Name: auditoria_sistema_id_auditoria_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auditoria_sistema_id_auditoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: auditoria_sistema_id_auditoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auditoria_sistema_id_auditoria_seq OWNED BY public.auditoria_sistema.id_auditoria;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id_rol integer NOT NULL,
    cod_rol character varying(20) NOT NULL,
    des_rol character varying(60) NOT NULL,
    est_rol boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_roles_cod CHECK (((cod_rol)::text = ANY ((ARRAY['SUPERADMIN'::character varying, 'ADMINISTRADOR'::character varying, 'RECEPCION'::character varying, 'CLINICO'::character varying, 'VENTAS'::character varying])::text[])))
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
-- Name: roles_paginas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles_paginas (
    id_rol_pagina integer NOT NULL,
    id_rol integer NOT NULL,
    id_pagina integer NOT NULL,
    visible boolean DEFAULT false NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: roles_paginas_id_rol_pagina_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_paginas_id_rol_pagina_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: roles_paginas_id_rol_pagina_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_paginas_id_rol_pagina_seq OWNED BY public.roles_paginas.id_rol_pagina;

--
-- Name: roles_permisos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles_permisos (
    id_rol_permiso integer NOT NULL,
    id_rol integer NOT NULL,
    id_modulo integer NOT NULL,
    id_accion integer NOT NULL,
    permitido boolean DEFAULT false NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: roles_permisos_id_rol_permiso_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_permisos_id_rol_permiso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: roles_permisos_id_rol_permiso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_permisos_id_rol_permiso_seq OWNED BY public.roles_permisos.id_rol_permiso;

--
-- Name: usuarios_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios_roles (
    id_usuario_rol integer NOT NULL,
    id_usuario integer NOT NULL,
    id_rol integer NOT NULL,
    es_rol_principal boolean DEFAULT false NOT NULL,
    est_usuario_rol boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: usuarios_roles_id_usuario_rol_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_roles_id_usuario_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: usuarios_roles_id_usuario_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_roles_id_usuario_rol_seq OWNED BY public.usuarios_roles.id_usuario_rol;

--
-- Name: v_usuarios_seguridad; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_usuarios_seguridad AS
 SELECT u.id_usuario,
    u.usu_nick,
    u.usu_clave,
    u.est_usuario,
    u.id_funcionario,
    rp.id_rol,
    concat(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
    rp.cod_rol AS grupo_nombre,
    c.des_cargo AS cargo_nombre,
    u.fecha_ultimo_login,
    u.ip_ultimo_login,
    u.fecha_bloqueo,
    u.bloqueado_hasta,
    u.motivo_bloqueo,
    u.requiere_cambio_clave,
    u.fecha_cambio_clave,
    u.clave_nunca_expira,
    u.dias_validez_clave,
    u.max_sesiones_simultaneas,
    u.sesiones_activas,
        CASE
            WHEN u.clave_nunca_expira THEN false
            WHEN (u.fecha_cambio_clave IS NULL) THEN true
            ELSE ((CURRENT_DATE - (u.fecha_cambio_clave)::date) > u.dias_validez_clave)
        END AS password_expirada,
        CASE
            WHEN u.clave_nunca_expira THEN NULL::integer
            WHEN (u.fecha_cambio_clave IS NULL) THEN u.dias_validez_clave
            ELSE GREATEST(0, (u.dias_validez_clave - (CURRENT_DATE - (u.fecha_cambio_clave)::date)))
        END AS dias_hasta_expiracion,
    public.esta_usuario_bloqueado(u.id_usuario) AS esta_bloqueado,
    u.mfa_habilitado,
    COALESCE(p.per_correo, u.correo) AS correo
   FROM (((((public.usuarios u
     LEFT JOIN public.funcionarios f ON ((f.id_funcionario = u.id_funcionario)))
     LEFT JOIN public.personas p ON ((p.id_persona = f.id_persona)))
     LEFT JOIN public.cargos c ON ((c.id_cargo = f.id_cargo)))
     LEFT JOIN public.usuarios_roles ur_p ON (((ur_p.id_usuario = u.id_usuario) AND (ur_p.es_rol_principal = true))))
     LEFT JOIN public.roles rp ON ((rp.id_rol = ur_p.id_rol)));

--
-- Name: VIEW v_usuarios_seguridad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_usuarios_seguridad IS 'Vista con información completa de usuarios para login y seguridad (incluye usu_clave). grupo_nombre/id_rol reflejan el rol principal del usuario.';

--
-- Name: accesos_sistema id_acceso; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accesos_sistema ALTER COLUMN id_acceso SET DEFAULT nextval('public.accesos_sistema_id_acceso_seq'::regclass);

--
-- Name: acciones id_accion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.acciones ALTER COLUMN id_accion SET DEFAULT nextval('public.acciones_id_accion_seq'::regclass);

--
-- Name: auditoria_sistema id_auditoria; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_sistema ALTER COLUMN id_auditoria SET DEFAULT nextval('public.auditoria_sistema_id_auditoria_seq'::regclass);

--
-- Name: roles id_rol; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id_rol SET DEFAULT nextval('public.roles_id_rol_seq'::regclass);

--
-- Name: roles_paginas id_rol_pagina; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_paginas ALTER COLUMN id_rol_pagina SET DEFAULT nextval('public.roles_paginas_id_rol_pagina_seq'::regclass);

--
-- Name: roles_permisos id_rol_permiso; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos ALTER COLUMN id_rol_permiso SET DEFAULT nextval('public.roles_permisos_id_rol_permiso_seq'::regclass);

--
-- Name: usuarios_roles id_usuario_rol; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_roles ALTER COLUMN id_usuario_rol SET DEFAULT nextval('public.usuarios_roles_id_usuario_rol_seq'::regclass);

--
-- Name: accesos_sistema accesos_sistema_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accesos_sistema
    ADD CONSTRAINT accesos_sistema_pkey PRIMARY KEY (id_acceso);

--
-- Name: acciones acciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.acciones
    ADD CONSTRAINT acciones_pkey PRIMARY KEY (id_accion);

--
-- Name: auditoria_sistema auditoria_sistema_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_sistema
    ADD CONSTRAINT auditoria_sistema_pkey PRIMARY KEY (id_auditoria);

--
-- Name: roles_paginas roles_paginas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_paginas
    ADD CONSTRAINT roles_paginas_pkey PRIMARY KEY (id_rol_pagina);

--
-- Name: roles_permisos roles_permisos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_pkey PRIMARY KEY (id_rol_permiso);

--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_rol);

--
-- Name: acciones uq_acciones_cod; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.acciones
    ADD CONSTRAINT uq_acciones_cod UNIQUE (cod_accion);

--
-- Name: roles uq_roles_cod; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT uq_roles_cod UNIQUE (cod_rol);

--
-- Name: roles_paginas uq_roles_paginas; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_paginas
    ADD CONSTRAINT uq_roles_paginas UNIQUE (id_rol, id_pagina);

--
-- Name: roles_permisos uq_roles_permisos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT uq_roles_permisos UNIQUE (id_rol, id_modulo, id_accion);

--
-- Name: usuarios_roles uq_usuarios_roles; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_roles
    ADD CONSTRAINT uq_usuarios_roles UNIQUE (id_usuario, id_rol);

--
-- Name: usuarios_roles usuarios_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_roles
    ADD CONSTRAINT usuarios_roles_pkey PRIMARY KEY (id_usuario_rol);

--
-- Name: idx_accesos_sistema_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accesos_sistema_fecha ON public.accesos_sistema USING btree (fecha_intento);

--
-- Name: idx_accesos_sistema_ip; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accesos_sistema_ip ON public.accesos_sistema USING btree (ip_origen);

--
-- Name: idx_accesos_sistema_usuario; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accesos_sistema_usuario ON public.accesos_sistema USING btree (id_usuario);

--
-- Name: idx_auditoria_sistema_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_auditoria_sistema_fecha ON public.auditoria_sistema USING btree (fecha_evento);

--
-- Name: idx_auditoria_sistema_usuario; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_auditoria_sistema_usuario ON public.auditoria_sistema USING btree (id_usuario);

--
-- Name: idx_roles_paginas_rol; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_roles_paginas_rol ON public.roles_paginas USING btree (id_rol);

--
-- Name: idx_roles_permisos_rol; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_roles_permisos_rol ON public.roles_permisos USING btree (id_rol);

--
-- Name: idx_usuarios_roles_usuario; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_usuarios_roles_usuario ON public.usuarios_roles USING btree (id_usuario);

--
-- Name: uq_usuarios_roles_principal; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_usuarios_roles_principal ON public.usuarios_roles USING btree (id_usuario) WHERE (es_rol_principal = true);

--
-- Name: acciones tg_acciones_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_acciones_fmod BEFORE UPDATE ON public.acciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: roles_paginas tg_roles_paginas_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_roles_paginas_fmod BEFORE UPDATE ON public.roles_paginas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: roles_permisos tg_roles_permisos_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_roles_permisos_fmod BEFORE UPDATE ON public.roles_permisos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: auditoria_sistema trg_auditoria_sistema_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_auditoria_sistema_fecha_mod BEFORE UPDATE ON public.auditoria_sistema FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: roles trg_roles_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_roles_fecha_mod BEFORE UPDATE ON public.roles FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: usuarios_roles trg_usuarios_roles_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_usuarios_roles_fecha_mod BEFORE UPDATE ON public.usuarios_roles FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: accesos_sistema accesos_sistema_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accesos_sistema
    ADD CONSTRAINT accesos_sistema_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: accesos_sistema accesos_sistema_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accesos_sistema
    ADD CONSTRAINT accesos_sistema_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: accesos_sistema accesos_sistema_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accesos_sistema
    ADD CONSTRAINT accesos_sistema_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: acciones acciones_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.acciones
    ADD CONSTRAINT acciones_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: acciones acciones_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.acciones
    ADD CONSTRAINT acciones_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: auditoria_sistema auditoria_sistema_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_sistema
    ADD CONSTRAINT auditoria_sistema_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: auditoria_sistema auditoria_sistema_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_sistema
    ADD CONSTRAINT auditoria_sistema_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: auditoria_sistema auditoria_sistema_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auditoria_sistema
    ADD CONSTRAINT auditoria_sistema_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: roles_paginas roles_paginas_id_pagina_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_paginas
    ADD CONSTRAINT roles_paginas_id_pagina_fkey FOREIGN KEY (id_pagina) REFERENCES public.paginas(id_pagina) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: roles_paginas roles_paginas_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_paginas
    ADD CONSTRAINT roles_paginas_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: roles_paginas roles_paginas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_paginas
    ADD CONSTRAINT roles_paginas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: roles_paginas roles_paginas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_paginas
    ADD CONSTRAINT roles_paginas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: roles_permisos roles_permisos_id_accion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_id_accion_fkey FOREIGN KEY (id_accion) REFERENCES public.acciones(id_accion) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: roles_permisos roles_permisos_id_modulo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_id_modulo_fkey FOREIGN KEY (id_modulo) REFERENCES public.modulos(id_modulo) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: roles_permisos roles_permisos_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: roles_permisos roles_permisos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: roles_permisos roles_permisos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: roles roles_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: roles roles_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: usuarios_roles usuarios_roles_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_roles
    ADD CONSTRAINT usuarios_roles_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: usuarios_roles usuarios_roles_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_roles
    ADD CONSTRAINT usuarios_roles_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: usuarios_roles usuarios_roles_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_roles
    ADD CONSTRAINT usuarios_roles_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: usuarios_roles usuarios_roles_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_roles
    ADD CONSTRAINT usuarios_roles_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
