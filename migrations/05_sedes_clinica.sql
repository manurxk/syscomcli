-- 05_sedes_clinica.sql — Empresa, sedes y consultorios
-- Generado el 2026-10-19 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: empresa, sedes, consultorios.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/05_sedes_clinica.sql

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
-- Name: consultorios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultorios (
    id_consultorio integer NOT NULL,
    id_sede integer NOT NULL,
    des_consultorio character varying(100) NOT NULL,
    est_consultorio boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_consultorios_des CHECK (((des_consultorio)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: consultorios_id_consultorio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consultorios_id_consultorio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: consultorios_id_consultorio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consultorios_id_consultorio_seq OWNED BY public.consultorios.id_consultorio;

--
-- Name: empresa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.empresa (
    id_empresa integer NOT NULL,
    ruc_nit character varying(20) NOT NULL,
    digito_verificador character(1) NOT NULL,
    razon_social character varying(255) NOT NULL,
    nombre_comercial character varying(150),
    tipo_contribuyente character varying(50) DEFAULT 'PERSONA_JURIDICA'::character varying NOT NULL,
    id_ciudad integer,
    direccion text NOT NULL,
    numero_casa character varying(20),
    codigo_postal character varying(10),
    telefono character varying(50) NOT NULL,
    celular character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    sitio_web character varying(255),
    representante_legal_nombre character varying(255),
    representante_legal_apellido character varying(255),
    representante_legal_ci character varying(20),
    representante_legal_cargo character varying(100),
    facturador_electronico boolean DEFAULT false NOT NULL,
    fecha_habilitacion_sifen date,
    grupo_obligatoriedad integer,
    ambiente_sifen character varying(20) DEFAULT 'PRUEBA'::character varying NOT NULL,
    certificado_firma_digital_path text,
    certificado_firma_digital_password_encrypted text,
    certificado_firma_digital_serial character varying(255),
    certificado_firma_digital_fecha_vencimiento date,
    codigo_seguridad_contribuyente character varying(100),
    actividad_economica_principal character varying(255),
    logo_path character varying(255),
    horario_atencion text,
    es_principal boolean DEFAULT false NOT NULL,
    est_empresa boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    horario_atencion_tramos jsonb,
    CONSTRAINT chk_empresa_ambiente_sifen CHECK (((ambiente_sifen)::text = ANY ((ARRAY['PRUEBA'::character varying, 'PRODUCCION'::character varying])::text[]))),
    CONSTRAINT chk_empresa_email CHECK (((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text)),
    CONSTRAINT chk_empresa_horario_tramos CHECK (((horario_atencion_tramos IS NULL) OR (jsonb_typeof(horario_atencion_tramos) = 'object'::text))),
    CONSTRAINT chk_empresa_ruc_len CHECK (((length((ruc_nit)::text) >= 6) AND (length((ruc_nit)::text) <= 20))),
    CONSTRAINT chk_empresa_tipo_contribuyente CHECK (((tipo_contribuyente)::text = ANY ((ARRAY['PERSONA_FISICA'::character varying, 'PERSONA_JURIDICA'::character varying, 'EAS'::character varying])::text[])))
);

--
-- Name: COLUMN empresa.fecha_habilitacion_sifen; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.fecha_habilitacion_sifen IS 'Fecha en que la SET habilita a la empresa como emisora electrónica.';

--
-- Name: COLUMN empresa.grupo_obligatoriedad; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.grupo_obligatoriedad IS 'Grupo de obligatoriedad de facturación electrónica asignado por la SET.';

--
-- Name: COLUMN empresa.certificado_firma_digital_path; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.certificado_firma_digital_path IS 'Ruta del certificado de firma digital para SIFEN. Se carga al habilitar la facturación electrónica.';

--
-- Name: COLUMN empresa.certificado_firma_digital_password_encrypted; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.certificado_firma_digital_password_encrypted IS 'Contraseña cifrada del certificado de firma digital (SIFEN). Se carga al habilitar la facturación electrónica.';

--
-- Name: COLUMN empresa.certificado_firma_digital_serial; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.certificado_firma_digital_serial IS 'Número de serie del certificado de firma digital (SIFEN). Se carga al habilitar la facturación electrónica.';

--
-- Name: COLUMN empresa.certificado_firma_digital_fecha_vencimiento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.certificado_firma_digital_fecha_vencimiento IS 'Vencimiento del certificado de firma digital (SIFEN). Se carga al habilitar la facturación electrónica.';

--
-- Name: COLUMN empresa.codigo_seguridad_contribuyente; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.codigo_seguridad_contribuyente IS 'Código de seguridad del contribuyente (CSC) que entrega la SET para SIFEN.';

--
-- Name: COLUMN empresa.horario_atencion_tramos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.empresa.horario_atencion_tramos IS 'Horario de atencion en tramos por dia: {"<id_dia_semana>": [["HH:MM","HH:MM"], ...]}; dia sin clave = cerrado. Lo usan las alertas de auditoria (fuera de horario). Lo valida EmpresaDao al guardar.';

--
-- Name: empresa_id_empresa_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.empresa_id_empresa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: empresa_id_empresa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.empresa_id_empresa_seq OWNED BY public.empresa.id_empresa;

--
-- Name: sedes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sedes (
    id_sede integer NOT NULL,
    id_empresa integer NOT NULL,
    des_sede character varying(150) NOT NULL,
    codigo_sede character varying(20),
    cod_establecimiento_sifen character(3),
    id_ciudad integer,
    direccion character varying(255),
    codigo_postal character varying(10),
    latitud numeric(10,8),
    longitud numeric(11,8),
    telefono character varying(50),
    email character varying(100),
    horario_atencion text,
    es_principal boolean DEFAULT false NOT NULL,
    est_sede boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_sedes_cod_establecimiento CHECK (((cod_establecimiento_sifen IS NULL) OR (cod_establecimiento_sifen ~ '^[0-9]{3}$'::text))),
    CONSTRAINT chk_sedes_des CHECK (((des_sede)::text ~ '^[A-Za-zÀ-ÿ0-9 ]+$'::text))
);

--
-- Name: sedes_id_sede_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sedes_id_sede_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: sedes_id_sede_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sedes_id_sede_seq OWNED BY public.sedes.id_sede;

--
-- Name: consultorios id_consultorio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorios ALTER COLUMN id_consultorio SET DEFAULT nextval('public.consultorios_id_consultorio_seq'::regclass);

--
-- Name: empresa id_empresa; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresa ALTER COLUMN id_empresa SET DEFAULT nextval('public.empresa_id_empresa_seq'::regclass);

--
-- Name: sedes id_sede; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes ALTER COLUMN id_sede SET DEFAULT nextval('public.sedes_id_sede_seq'::regclass);

--
-- Name: consultorios consultorios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorios
    ADD CONSTRAINT consultorios_pkey PRIMARY KEY (id_consultorio);

--
-- Name: empresa empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresa
    ADD CONSTRAINT empresa_pkey PRIMARY KEY (id_empresa);

--
-- Name: sedes sedes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes
    ADD CONSTRAINT sedes_pkey PRIMARY KEY (id_sede);

--
-- Name: consultorios uq_consultorios_sede_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorios
    ADD CONSTRAINT uq_consultorios_sede_des UNIQUE (id_sede, des_consultorio);

--
-- Name: empresa uq_empresa_ruc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresa
    ADD CONSTRAINT uq_empresa_ruc UNIQUE (ruc_nit);

--
-- Name: sedes uq_sedes_cod_establecimiento; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes
    ADD CONSTRAINT uq_sedes_cod_establecimiento UNIQUE (id_empresa, cod_establecimiento_sifen);

--
-- Name: sedes uq_sedes_empresa_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes
    ADD CONSTRAINT uq_sedes_empresa_des UNIQUE (id_empresa, des_sede);

--
-- Name: idx_consultorios_sede; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_consultorios_sede ON public.consultorios USING btree (id_sede);

--
-- Name: idx_sedes_empresa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_sedes_empresa ON public.sedes USING btree (id_empresa);

--
-- Name: consultorios trg_consultorios_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_consultorios_fecha_mod BEFORE UPDATE ON public.consultorios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: empresa trg_empresa_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_empresa_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.empresa FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('SEGURIDAD', 'id_empresa');

--
-- Name: empresa trg_empresa_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_empresa_fecha_mod BEFORE UPDATE ON public.empresa FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: sedes trg_sedes_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_sedes_fecha_mod BEFORE UPDATE ON public.sedes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: consultorios consultorios_id_sede_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorios
    ADD CONSTRAINT consultorios_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES public.sedes(id_sede) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: consultorios consultorios_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorios
    ADD CONSTRAINT consultorios_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: consultorios consultorios_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultorios
    ADD CONSTRAINT consultorios_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: empresa empresa_id_ciudad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresa
    ADD CONSTRAINT empresa_id_ciudad_fkey FOREIGN KEY (id_ciudad) REFERENCES public.ciudades(id_ciudad) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: empresa empresa_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresa
    ADD CONSTRAINT empresa_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: empresa empresa_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresa
    ADD CONSTRAINT empresa_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: sedes sedes_id_ciudad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes
    ADD CONSTRAINT sedes_id_ciudad_fkey FOREIGN KEY (id_ciudad) REFERENCES public.ciudades(id_ciudad) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: sedes sedes_id_empresa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes
    ADD CONSTRAINT sedes_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES public.empresa(id_empresa) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: sedes sedes_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes
    ADD CONSTRAINT sedes_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: sedes sedes_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sedes
    ADD CONSTRAINT sedes_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
