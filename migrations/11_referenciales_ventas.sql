-- 11_referenciales_ventas.sql — Referenciales de ventas
-- Generado el 2026-10-18 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: monedas, condiciones_venta, formas_cobro, tipos_comprobantes, tipos_impuestos, tipos_items, marcas_tarjeta, entidades_adheridas, entidades_emisoras, estados_factura.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/11_referenciales_ventas.sql

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
-- Name: condiciones_venta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.condiciones_venta (
    id_condicion_venta integer NOT NULL,
    des_condicion_venta character varying(100) NOT NULL,
    cod_condicion_venta character varying(20),
    dias_credito smallint DEFAULT 0 NOT NULL,
    permite_cuotas boolean DEFAULT false NOT NULL,
    numero_cuotas_max smallint DEFAULT 1 NOT NULL,
    est_condicion_venta boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: condiciones_venta_id_condicion_venta_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.condiciones_venta_id_condicion_venta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: condiciones_venta_id_condicion_venta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.condiciones_venta_id_condicion_venta_seq OWNED BY public.condiciones_venta.id_condicion_venta;

--
-- Name: entidades_adheridas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.entidades_adheridas (
    id_entidad_adherida integer NOT NULL,
    des_entidad_adherida character varying(150) NOT NULL,
    cod_entidad_adherida character varying(20),
    ruc_entidad character varying(20),
    telefono_entidad character varying(30),
    email_entidad character varying(100),
    est_entidad_adherida boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: entidades_adheridas_id_entidad_adherida_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.entidades_adheridas_id_entidad_adherida_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: entidades_adheridas_id_entidad_adherida_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.entidades_adheridas_id_entidad_adherida_seq OWNED BY public.entidades_adheridas.id_entidad_adherida;

--
-- Name: entidades_emisoras; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.entidades_emisoras (
    id_entidad_emisora integer NOT NULL,
    des_entidad_emisora character varying(150) NOT NULL,
    cod_entidad_emisora character varying(20),
    ruc_entidad character varying(20),
    telefono_entidad character varying(30),
    email_entidad character varying(100),
    tipo_entidad character varying(50),
    est_entidad_emisora boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: entidades_emisoras_id_entidad_emisora_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.entidades_emisoras_id_entidad_emisora_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: entidades_emisoras_id_entidad_emisora_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.entidades_emisoras_id_entidad_emisora_seq OWNED BY public.entidades_emisoras.id_entidad_emisora;

--
-- Name: estados_factura; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estados_factura (
    id_estado_factura integer NOT NULL,
    des_estado_factura character varying(100) NOT NULL,
    cod_estado_factura character varying(20),
    permite_modificacion boolean DEFAULT true NOT NULL,
    permite_anulacion boolean DEFAULT true NOT NULL,
    color_estado character varying(30) DEFAULT 'secondary'::character varying NOT NULL,
    est_estado_factura boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: estados_factura_id_estado_factura_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estados_factura_id_estado_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: estados_factura_id_estado_factura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estados_factura_id_estado_factura_seq OWNED BY public.estados_factura.id_estado_factura;

--
-- Name: formas_cobro; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.formas_cobro (
    id_forma_cobro integer NOT NULL,
    des_forma_cobro character varying(100) NOT NULL,
    cod_forma_cobro character varying(30) NOT NULL,
    requiere_entidad boolean DEFAULT false NOT NULL,
    permite_cuotas boolean DEFAULT false NOT NULL,
    est_forma_cobro boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: formas_cobro_id_forma_cobro_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.formas_cobro_id_forma_cobro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: formas_cobro_id_forma_cobro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.formas_cobro_id_forma_cobro_seq OWNED BY public.formas_cobro.id_forma_cobro;

--
-- Name: marcas_tarjeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.marcas_tarjeta (
    id_marca_tarjeta integer NOT NULL,
    des_marca_tarjeta character varying(100) NOT NULL,
    cod_marca_tarjeta character varying(20),
    est_marca_tarjeta boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: marcas_tarjeta_id_marca_tarjeta_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.marcas_tarjeta_id_marca_tarjeta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: marcas_tarjeta_id_marca_tarjeta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.marcas_tarjeta_id_marca_tarjeta_seq OWNED BY public.marcas_tarjeta.id_marca_tarjeta;

--
-- Name: monedas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.monedas (
    id_moneda integer NOT NULL,
    des_moneda character varying(100) NOT NULL,
    cod_moneda character varying(10) NOT NULL,
    simbolo_moneda character varying(10),
    decimales_moneda smallint DEFAULT 0 NOT NULL,
    es_moneda_local boolean DEFAULT false NOT NULL,
    tasa_cambio numeric(18,6) DEFAULT 1.0 NOT NULL,
    est_moneda boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: monedas_id_moneda_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.monedas_id_moneda_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: monedas_id_moneda_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.monedas_id_moneda_seq OWNED BY public.monedas.id_moneda;

--
-- Name: tipos_comprobantes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_comprobantes (
    id_tipo_comprobante integer NOT NULL,
    des_tipo_comprobante character varying(100) NOT NULL,
    cod_tipo_comprobante character varying(20),
    codigo_sifen character varying(20),
    requiere_timbrado boolean DEFAULT true NOT NULL,
    tipo_documento character varying(50),
    est_tipo_comprobante boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: COLUMN tipos_comprobantes.codigo_sifen; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.tipos_comprobantes.codigo_sifen IS 'Código del tipo de documento electrónico en SIFEN. Se completa al conectar la facturación electrónica.';

--
-- Name: tipos_comprobantes_id_tipo_comprobante_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_comprobantes_id_tipo_comprobante_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_comprobantes_id_tipo_comprobante_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_comprobantes_id_tipo_comprobante_seq OWNED BY public.tipos_comprobantes.id_tipo_comprobante;

--
-- Name: tipos_impuestos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_impuestos (
    id_tipo_impuesto integer NOT NULL,
    des_tipo_impuesto character varying(100) NOT NULL,
    cod_tipo_impuesto character varying(20),
    porcentaje_impuesto numeric(5,2) DEFAULT 0 NOT NULL,
    tipo_calculo character varying(20) DEFAULT 'PORCENTAJE'::character varying NOT NULL,
    est_tipo_impuesto boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_tipos_impuestos_calc CHECK (((tipo_calculo)::text = ANY ((ARRAY['PORCENTAJE'::character varying, 'MONTO_FIJO'::character varying])::text[])))
);

--
-- Name: tipos_impuestos_id_tipo_impuesto_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_impuestos_id_tipo_impuesto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_impuestos_id_tipo_impuesto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_impuestos_id_tipo_impuesto_seq OWNED BY public.tipos_impuestos.id_tipo_impuesto;

--
-- Name: tipos_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_items (
    id_tipo_item integer NOT NULL,
    des_tipo_item character varying(100) NOT NULL,
    cod_tipo_item character varying(20),
    tipo_item_categoria character varying(50),
    requiere_stock boolean DEFAULT false NOT NULL,
    est_tipo_item boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: tipos_items_id_tipo_item_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_items_id_tipo_item_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: tipos_items_id_tipo_item_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_items_id_tipo_item_seq OWNED BY public.tipos_items.id_tipo_item;

--
-- Name: condiciones_venta id_condicion_venta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.condiciones_venta ALTER COLUMN id_condicion_venta SET DEFAULT nextval('public.condiciones_venta_id_condicion_venta_seq'::regclass);

--
-- Name: entidades_adheridas id_entidad_adherida; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_adheridas ALTER COLUMN id_entidad_adherida SET DEFAULT nextval('public.entidades_adheridas_id_entidad_adherida_seq'::regclass);

--
-- Name: entidades_emisoras id_entidad_emisora; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_emisoras ALTER COLUMN id_entidad_emisora SET DEFAULT nextval('public.entidades_emisoras_id_entidad_emisora_seq'::regclass);

--
-- Name: estados_factura id_estado_factura; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura ALTER COLUMN id_estado_factura SET DEFAULT nextval('public.estados_factura_id_estado_factura_seq'::regclass);

--
-- Name: formas_cobro id_forma_cobro; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro ALTER COLUMN id_forma_cobro SET DEFAULT nextval('public.formas_cobro_id_forma_cobro_seq'::regclass);

--
-- Name: marcas_tarjeta id_marca_tarjeta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas_tarjeta ALTER COLUMN id_marca_tarjeta SET DEFAULT nextval('public.marcas_tarjeta_id_marca_tarjeta_seq'::regclass);

--
-- Name: monedas id_moneda; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monedas ALTER COLUMN id_moneda SET DEFAULT nextval('public.monedas_id_moneda_seq'::regclass);

--
-- Name: tipos_comprobantes id_tipo_comprobante; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobantes ALTER COLUMN id_tipo_comprobante SET DEFAULT nextval('public.tipos_comprobantes_id_tipo_comprobante_seq'::regclass);

--
-- Name: tipos_impuestos id_tipo_impuesto; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_impuestos ALTER COLUMN id_tipo_impuesto SET DEFAULT nextval('public.tipos_impuestos_id_tipo_impuesto_seq'::regclass);

--
-- Name: tipos_items id_tipo_item; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_items ALTER COLUMN id_tipo_item SET DEFAULT nextval('public.tipos_items_id_tipo_item_seq'::regclass);

--
-- Name: condiciones_venta condiciones_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.condiciones_venta
    ADD CONSTRAINT condiciones_venta_pkey PRIMARY KEY (id_condicion_venta);

--
-- Name: entidades_adheridas entidades_adheridas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_adheridas
    ADD CONSTRAINT entidades_adheridas_pkey PRIMARY KEY (id_entidad_adherida);

--
-- Name: entidades_emisoras entidades_emisoras_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_emisoras
    ADD CONSTRAINT entidades_emisoras_pkey PRIMARY KEY (id_entidad_emisora);

--
-- Name: estados_factura estados_factura_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura
    ADD CONSTRAINT estados_factura_pkey PRIMARY KEY (id_estado_factura);

--
-- Name: formas_cobro formas_cobro_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro
    ADD CONSTRAINT formas_cobro_pkey PRIMARY KEY (id_forma_cobro);

--
-- Name: marcas_tarjeta marcas_tarjeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas_tarjeta
    ADD CONSTRAINT marcas_tarjeta_pkey PRIMARY KEY (id_marca_tarjeta);

--
-- Name: monedas monedas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monedas
    ADD CONSTRAINT monedas_pkey PRIMARY KEY (id_moneda);

--
-- Name: tipos_comprobantes tipos_comprobantes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobantes
    ADD CONSTRAINT tipos_comprobantes_pkey PRIMARY KEY (id_tipo_comprobante);

--
-- Name: tipos_impuestos tipos_impuestos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_impuestos
    ADD CONSTRAINT tipos_impuestos_pkey PRIMARY KEY (id_tipo_impuesto);

--
-- Name: tipos_items tipos_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_items
    ADD CONSTRAINT tipos_items_pkey PRIMARY KEY (id_tipo_item);

--
-- Name: condiciones_venta uq_condiciones_venta_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.condiciones_venta
    ADD CONSTRAINT uq_condiciones_venta_des UNIQUE (des_condicion_venta);

--
-- Name: entidades_adheridas uq_entidades_adheridas_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_adheridas
    ADD CONSTRAINT uq_entidades_adheridas_des UNIQUE (des_entidad_adherida);

--
-- Name: entidades_emisoras uq_entidades_emisoras_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_emisoras
    ADD CONSTRAINT uq_entidades_emisoras_des UNIQUE (des_entidad_emisora);

--
-- Name: estados_factura uq_estados_factura_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura
    ADD CONSTRAINT uq_estados_factura_des UNIQUE (des_estado_factura);

--
-- Name: formas_cobro uq_formas_cobro_cod; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro
    ADD CONSTRAINT uq_formas_cobro_cod UNIQUE (cod_forma_cobro);

--
-- Name: formas_cobro uq_formas_cobro_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro
    ADD CONSTRAINT uq_formas_cobro_des UNIQUE (des_forma_cobro);

--
-- Name: marcas_tarjeta uq_marcas_tarjeta_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas_tarjeta
    ADD CONSTRAINT uq_marcas_tarjeta_des UNIQUE (des_marca_tarjeta);

--
-- Name: monedas uq_monedas_cod; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monedas
    ADD CONSTRAINT uq_monedas_cod UNIQUE (cod_moneda);

--
-- Name: tipos_comprobantes uq_tipos_comprobantes_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobantes
    ADD CONSTRAINT uq_tipos_comprobantes_des UNIQUE (des_tipo_comprobante);

--
-- Name: tipos_impuestos uq_tipos_impuestos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_impuestos
    ADD CONSTRAINT uq_tipos_impuestos_des UNIQUE (des_tipo_impuesto);

--
-- Name: tipos_items uq_tipos_items_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_items
    ADD CONSTRAINT uq_tipos_items_des UNIQUE (des_tipo_item);

--
-- Name: condiciones_venta trg_condiciones_venta_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_condiciones_venta_fecha_mod BEFORE UPDATE ON public.condiciones_venta FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: entidades_adheridas trg_entidades_adheridas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_entidades_adheridas_fecha_mod BEFORE UPDATE ON public.entidades_adheridas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: entidades_emisoras trg_entidades_emisoras_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_entidades_emisoras_fecha_mod BEFORE UPDATE ON public.entidades_emisoras FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: estados_factura trg_estados_factura_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_estados_factura_fecha_mod BEFORE UPDATE ON public.estados_factura FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: formas_cobro trg_formas_cobro_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_formas_cobro_fecha_mod BEFORE UPDATE ON public.formas_cobro FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: marcas_tarjeta trg_marcas_tarjeta_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_marcas_tarjeta_fecha_mod BEFORE UPDATE ON public.marcas_tarjeta FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: monedas trg_monedas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_monedas_fecha_mod BEFORE UPDATE ON public.monedas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_comprobantes trg_tipos_comprobantes_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_comprobantes_fecha_mod BEFORE UPDATE ON public.tipos_comprobantes FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_impuestos trg_tipos_impuestos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_impuestos_fecha_mod BEFORE UPDATE ON public.tipos_impuestos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: tipos_items trg_tipos_items_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_tipos_items_fecha_mod BEFORE UPDATE ON public.tipos_items FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: condiciones_venta condiciones_venta_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.condiciones_venta
    ADD CONSTRAINT condiciones_venta_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: condiciones_venta condiciones_venta_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.condiciones_venta
    ADD CONSTRAINT condiciones_venta_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: entidades_adheridas entidades_adheridas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_adheridas
    ADD CONSTRAINT entidades_adheridas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: entidades_adheridas entidades_adheridas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_adheridas
    ADD CONSTRAINT entidades_adheridas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: entidades_emisoras entidades_emisoras_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_emisoras
    ADD CONSTRAINT entidades_emisoras_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: entidades_emisoras entidades_emisoras_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entidades_emisoras
    ADD CONSTRAINT entidades_emisoras_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: estados_factura estados_factura_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura
    ADD CONSTRAINT estados_factura_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: estados_factura estados_factura_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estados_factura
    ADD CONSTRAINT estados_factura_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: formas_cobro formas_cobro_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro
    ADD CONSTRAINT formas_cobro_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: formas_cobro formas_cobro_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.formas_cobro
    ADD CONSTRAINT formas_cobro_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: marcas_tarjeta marcas_tarjeta_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas_tarjeta
    ADD CONSTRAINT marcas_tarjeta_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: marcas_tarjeta marcas_tarjeta_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas_tarjeta
    ADD CONSTRAINT marcas_tarjeta_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: monedas monedas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monedas
    ADD CONSTRAINT monedas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: monedas monedas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monedas
    ADD CONSTRAINT monedas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_comprobantes tipos_comprobantes_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobantes
    ADD CONSTRAINT tipos_comprobantes_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_comprobantes tipos_comprobantes_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_comprobantes
    ADD CONSTRAINT tipos_comprobantes_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_impuestos tipos_impuestos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_impuestos
    ADD CONSTRAINT tipos_impuestos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_impuestos tipos_impuestos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_impuestos
    ADD CONSTRAINT tipos_impuestos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_items tipos_items_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_items
    ADD CONSTRAINT tipos_items_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: tipos_items tipos_items_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_items
    ADD CONSTRAINT tipos_items_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
