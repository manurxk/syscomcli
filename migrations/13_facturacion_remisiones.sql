-- 13_facturacion_remisiones.sql — Facturación, notas de crédito/débito y remisiones
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: timbrados, puntos_expedicion, facturas, factura_detalle, facturas_borrador, notas_credito, nota_credito_detalle, notas_debito, nota_debito_detalle, remisiones, remision_detalle.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/13_facturacion_remisiones.sql

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
-- Name: factura_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.factura_detalle (
    id_factura_detalle integer NOT NULL,
    id_factura integer NOT NULL,
    id_item_servicio integer,
    id_tipo_item integer,
    id_consulta integer,
    item_descripcion character varying(200) NOT NULL,
    item_cantidad integer DEFAULT 1 NOT NULL,
    item_precio_unitario numeric(18,2) DEFAULT 0 NOT NULL,
    item_precio_con_iva numeric(18,2) DEFAULT 0 NOT NULL,
    item_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    item_subtotal numeric(18,2) DEFAULT 0 NOT NULL,
    id_tipo_impuesto integer,
    impuesto_porcentaje numeric(5,2) DEFAULT 0 NOT NULL,
    impuesto_monto numeric(18,2) DEFAULT 0 NOT NULL,
    item_total numeric(18,2) DEFAULT 0 NOT NULL
);

--
-- Name: factura_detalle_id_factura_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.factura_detalle_id_factura_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: factura_detalle_id_factura_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.factura_detalle_id_factura_detalle_seq OWNED BY public.factura_detalle.id_factura_detalle;

--
-- Name: facturas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facturas (
    id_factura integer NOT NULL,
    factura_numero character varying(30) NOT NULL,
    id_paciente integer NOT NULL,
    id_pedido integer,
    id_timbrado integer,
    id_punto_expedicion integer,
    id_tipo_comprobante integer,
    id_condicion_venta integer,
    id_moneda integer,
    id_estado_factura integer,
    fecha_factura date NOT NULL,
    fecha_vencimiento date,
    factura_subtotal numeric(18,2) DEFAULT 0 NOT NULL,
    factura_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    factura_impuestos numeric(18,2) DEFAULT 0 NOT NULL,
    factura_total numeric(18,2) DEFAULT 0 NOT NULL,
    factura_total_letras text,
    codigo_sifen character varying(44),
    numero_timbrado character varying(8),
    observaciones text,
    fecha_anulacion timestamp without time zone,
    usuario_anulacion integer,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    motivo_anulacion text
);

--
-- Name: COLUMN facturas.id_pedido; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.facturas.id_pedido IS 'Pedido de origen, si la factura se emitió desde un pedido (opcional en el formulario).';

--
-- Name: COLUMN facturas.codigo_sifen; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.facturas.codigo_sifen IS 'CDC devuelto por SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';

--
-- Name: COLUMN facturas.motivo_anulacion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.facturas.motivo_anulacion IS 'Motivo con el que se anulo la factura (lo carga sp_anular_factura; obligatorio). Vacio en las anuladas antes del 2026-10-20.';

--
-- Name: facturas_borrador; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facturas_borrador (
    id_factura_borrador integer NOT NULL,
    id_paciente integer,
    datos jsonb NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: facturas_borrador_id_factura_borrador_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.facturas_borrador_id_factura_borrador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: facturas_borrador_id_factura_borrador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.facturas_borrador_id_factura_borrador_seq OWNED BY public.facturas_borrador.id_factura_borrador;

--
-- Name: facturas_id_factura_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.facturas_id_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: facturas_id_factura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.facturas_id_factura_seq OWNED BY public.facturas.id_factura;

--
-- Name: nota_credito_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nota_credito_detalle (
    id_nota_credito_detalle integer NOT NULL,
    id_nota_credito integer NOT NULL,
    id_factura_detalle integer,
    item_descripcion character varying(200) NOT NULL,
    item_cantidad numeric(10,2) DEFAULT 1 NOT NULL,
    item_precio_unitario numeric(18,2) DEFAULT 0 NOT NULL,
    monto_total numeric(18,2) DEFAULT 0 NOT NULL
);

--
-- Name: nota_credito_detalle_id_nota_credito_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nota_credito_detalle_id_nota_credito_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: nota_credito_detalle_id_nota_credito_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nota_credito_detalle_id_nota_credito_detalle_seq OWNED BY public.nota_credito_detalle.id_nota_credito_detalle;

--
-- Name: nota_debito_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nota_debito_detalle (
    id_nota_debito_detalle integer NOT NULL,
    id_nota_debito integer NOT NULL,
    id_factura_detalle integer,
    item_descripcion character varying(200) NOT NULL,
    item_cantidad numeric(10,2) DEFAULT 1 NOT NULL,
    item_precio_unitario numeric(18,2) DEFAULT 0 NOT NULL,
    monto_total numeric(18,2) DEFAULT 0 NOT NULL
);

--
-- Name: nota_debito_detalle_id_nota_debito_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nota_debito_detalle_id_nota_debito_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: nota_debito_detalle_id_nota_debito_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nota_debito_detalle_id_nota_debito_detalle_seq OWNED BY public.nota_debito_detalle.id_nota_debito_detalle;

--
-- Name: notas_credito; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notas_credito (
    id_nota_credito integer NOT NULL,
    nota_credito_numero character varying(20) NOT NULL,
    id_factura integer NOT NULL,
    id_tipo_comprobante integer,
    fecha_nota_credito timestamp without time zone DEFAULT now() NOT NULL,
    motivo_nota_credito text NOT NULL,
    monto_total numeric(18,2) DEFAULT 0 NOT NULL,
    codigo_sifen character varying(44),
    numero_timbrado character varying(8),
    observaciones text,
    est_nota_credito character varying(20) DEFAULT 'REGISTRADA'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT notas_credito_est_nota_credito_check CHECK (((est_nota_credito)::text = ANY (ARRAY[('REGISTRADA'::character varying)::text, ('ANULADA'::character varying)::text])))
);

--
-- Name: COLUMN notas_credito.codigo_sifen; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notas_credito.codigo_sifen IS 'CDC devuelto por SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';

--
-- Name: notas_credito_id_nota_credito_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notas_credito_id_nota_credito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: notas_credito_id_nota_credito_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notas_credito_id_nota_credito_seq OWNED BY public.notas_credito.id_nota_credito;

--
-- Name: notas_debito; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notas_debito (
    id_nota_debito integer NOT NULL,
    nota_debito_numero character varying(20) NOT NULL,
    id_factura integer NOT NULL,
    id_tipo_comprobante integer,
    fecha_nota_debito timestamp without time zone DEFAULT now() NOT NULL,
    motivo_nota_debito text NOT NULL,
    monto_total numeric(18,2) DEFAULT 0 NOT NULL,
    codigo_sifen character varying(44),
    numero_timbrado character varying(8),
    observaciones text,
    est_nota_debito character varying(20) DEFAULT 'REGISTRADA'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT notas_debito_est_nota_debito_check CHECK (((est_nota_debito)::text = ANY (ARRAY[('REGISTRADA'::character varying)::text, ('ANULADA'::character varying)::text])))
);

--
-- Name: COLUMN notas_debito.codigo_sifen; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notas_debito.codigo_sifen IS 'CDC devuelto por SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';

--
-- Name: notas_debito_id_nota_debito_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notas_debito_id_nota_debito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: notas_debito_id_nota_debito_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notas_debito_id_nota_debito_seq OWNED BY public.notas_debito.id_nota_debito;

--
-- Name: puntos_expedicion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.puntos_expedicion (
    id_punto_expedicion integer NOT NULL,
    id_timbrado integer NOT NULL,
    codigo_punto_expedicion character varying(3) NOT NULL,
    nombre_punto_expedicion character varying(100) NOT NULL,
    ultimo_numero_usado integer DEFAULT 0 NOT NULL,
    est_punto_expedicion boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_puntos_expedicion_codigo CHECK (((codigo_punto_expedicion)::text ~ '^[0-9]{3}$'::text))
);

--
-- Name: puntos_expedicion_id_punto_expedicion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.puntos_expedicion_id_punto_expedicion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: puntos_expedicion_id_punto_expedicion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.puntos_expedicion_id_punto_expedicion_seq OWNED BY public.puntos_expedicion.id_punto_expedicion;

--
-- Name: remision_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.remision_detalle (
    id_remision_detalle integer NOT NULL,
    id_remision integer NOT NULL,
    id_item_servicio integer,
    item_descripcion character varying(300) NOT NULL,
    item_cantidad numeric(10,2) DEFAULT 1 NOT NULL,
    item_unidad character varying(50),
    observaciones text,
    CONSTRAINT remision_detalle_item_cantidad_check CHECK ((item_cantidad > (0)::numeric))
);

--
-- Name: remision_detalle_id_remision_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.remision_detalle_id_remision_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: remision_detalle_id_remision_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.remision_detalle_id_remision_detalle_seq OWNED BY public.remision_detalle.id_remision_detalle;

--
-- Name: remisiones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.remisiones (
    id_remision integer NOT NULL,
    remision_numero character varying(20) NOT NULL,
    id_pedido integer,
    id_factura integer,
    id_paciente integer NOT NULL,
    fecha_remision date NOT NULL,
    fecha_entrega date,
    observaciones text,
    est_remision character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    usuario_creacion integer,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion integer,
    fecha_modificacion timestamp without time zone,
    CONSTRAINT remisiones_est_remision_check CHECK (((est_remision)::text = ANY (ARRAY[('PENDIENTE'::character varying)::text, ('ENTREGADA'::character varying)::text, ('ANULADA'::character varying)::text])))
);

--
-- Name: TABLE remisiones; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.remisiones IS 'Notas de remisión (entrega de servicios/insumos), número REM-AAAA-MM-NNNN. fecha_modificacion la mantiene el trigger trg_remisiones_fecha_mod (migración 108).';

--
-- Name: COLUMN remisiones.id_pedido; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.remisiones.id_pedido IS 'Pedido asociado a la remisión (opcional en el formulario).';

--
-- Name: COLUMN remisiones.id_factura; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.remisiones.id_factura IS 'Factura asociada a la remisión (opcional en el formulario).';

--
-- Name: remisiones_id_remision_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.remisiones_id_remision_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: remisiones_id_remision_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.remisiones_id_remision_seq OWNED BY public.remisiones.id_remision;

--
-- Name: timbrados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timbrados (
    id_timbrado integer NOT NULL,
    numero_timbrado character varying(8) NOT NULL,
    codigo_establecimiento character varying(3) DEFAULT '001'::character varying NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_vencimiento date NOT NULL,
    observaciones text,
    est_timbrado boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_timbrados_codigo_establecimiento CHECK (((codigo_establecimiento)::text ~ '^[0-9]{3}$'::text)),
    CONSTRAINT chk_timbrados_numero CHECK (((numero_timbrado)::text ~ '^[0-9]{8}$'::text))
);

--
-- Name: timbrados_id_timbrado_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timbrados_id_timbrado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: timbrados_id_timbrado_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timbrados_id_timbrado_seq OWNED BY public.timbrados.id_timbrado;

--
-- Name: factura_detalle id_factura_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle ALTER COLUMN id_factura_detalle SET DEFAULT nextval('public.factura_detalle_id_factura_detalle_seq'::regclass);

--
-- Name: facturas id_factura; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas ALTER COLUMN id_factura SET DEFAULT nextval('public.facturas_id_factura_seq'::regclass);

--
-- Name: facturas_borrador id_factura_borrador; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas_borrador ALTER COLUMN id_factura_borrador SET DEFAULT nextval('public.facturas_borrador_id_factura_borrador_seq'::regclass);

--
-- Name: nota_credito_detalle id_nota_credito_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_credito_detalle ALTER COLUMN id_nota_credito_detalle SET DEFAULT nextval('public.nota_credito_detalle_id_nota_credito_detalle_seq'::regclass);

--
-- Name: nota_debito_detalle id_nota_debito_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_debito_detalle ALTER COLUMN id_nota_debito_detalle SET DEFAULT nextval('public.nota_debito_detalle_id_nota_debito_detalle_seq'::regclass);

--
-- Name: notas_credito id_nota_credito; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito ALTER COLUMN id_nota_credito SET DEFAULT nextval('public.notas_credito_id_nota_credito_seq'::regclass);

--
-- Name: notas_debito id_nota_debito; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito ALTER COLUMN id_nota_debito SET DEFAULT nextval('public.notas_debito_id_nota_debito_seq'::regclass);

--
-- Name: puntos_expedicion id_punto_expedicion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puntos_expedicion ALTER COLUMN id_punto_expedicion SET DEFAULT nextval('public.puntos_expedicion_id_punto_expedicion_seq'::regclass);

--
-- Name: remision_detalle id_remision_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remision_detalle ALTER COLUMN id_remision_detalle SET DEFAULT nextval('public.remision_detalle_id_remision_detalle_seq'::regclass);

--
-- Name: remisiones id_remision; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones ALTER COLUMN id_remision SET DEFAULT nextval('public.remisiones_id_remision_seq'::regclass);

--
-- Name: timbrados id_timbrado; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timbrados ALTER COLUMN id_timbrado SET DEFAULT nextval('public.timbrados_id_timbrado_seq'::regclass);

--
-- Name: factura_detalle factura_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT factura_detalle_pkey PRIMARY KEY (id_factura_detalle);

--
-- Name: facturas_borrador facturas_borrador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas_borrador
    ADD CONSTRAINT facturas_borrador_pkey PRIMARY KEY (id_factura_borrador);

--
-- Name: facturas facturas_factura_numero_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_factura_numero_key UNIQUE (factura_numero);

--
-- Name: facturas facturas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_pkey PRIMARY KEY (id_factura);

--
-- Name: nota_credito_detalle nota_credito_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_pkey PRIMARY KEY (id_nota_credito_detalle);

--
-- Name: nota_debito_detalle nota_debito_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_pkey PRIMARY KEY (id_nota_debito_detalle);

--
-- Name: notas_credito notas_credito_nota_credito_numero_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito
    ADD CONSTRAINT notas_credito_nota_credito_numero_key UNIQUE (nota_credito_numero);

--
-- Name: notas_credito notas_credito_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito
    ADD CONSTRAINT notas_credito_pkey PRIMARY KEY (id_nota_credito);

--
-- Name: notas_debito notas_debito_nota_debito_numero_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito
    ADD CONSTRAINT notas_debito_nota_debito_numero_key UNIQUE (nota_debito_numero);

--
-- Name: notas_debito notas_debito_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito
    ADD CONSTRAINT notas_debito_pkey PRIMARY KEY (id_nota_debito);

--
-- Name: puntos_expedicion puntos_expedicion_id_timbrado_codigo_punto_expedicion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puntos_expedicion
    ADD CONSTRAINT puntos_expedicion_id_timbrado_codigo_punto_expedicion_key UNIQUE (id_timbrado, codigo_punto_expedicion);

--
-- Name: puntos_expedicion puntos_expedicion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puntos_expedicion
    ADD CONSTRAINT puntos_expedicion_pkey PRIMARY KEY (id_punto_expedicion);

--
-- Name: remision_detalle remision_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remision_detalle
    ADD CONSTRAINT remision_detalle_pkey PRIMARY KEY (id_remision_detalle);

--
-- Name: remisiones remisiones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones
    ADD CONSTRAINT remisiones_pkey PRIMARY KEY (id_remision);

--
-- Name: remisiones remisiones_remision_numero_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones
    ADD CONSTRAINT remisiones_remision_numero_key UNIQUE (remision_numero);

--
-- Name: timbrados timbrados_numero_timbrado_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timbrados
    ADD CONSTRAINT timbrados_numero_timbrado_key UNIQUE (numero_timbrado);

--
-- Name: timbrados timbrados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timbrados
    ADD CONSTRAINT timbrados_pkey PRIMARY KEY (id_timbrado);

--
-- Name: facturas_borrador tg_facturas_borrador_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_facturas_borrador_fmod BEFORE UPDATE ON public.facturas_borrador FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: facturas tg_facturas_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_facturas_fmod BEFORE UPDATE ON public.facturas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: notas_credito tg_notas_credito_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_notas_credito_fmod BEFORE UPDATE ON public.notas_credito FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: notas_debito tg_notas_debito_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_notas_debito_fmod BEFORE UPDATE ON public.notas_debito FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: puntos_expedicion tg_puntos_expedicion_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_puntos_expedicion_fmod BEFORE UPDATE ON public.puntos_expedicion FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: timbrados tg_timbrados_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_timbrados_fmod BEFORE UPDATE ON public.timbrados FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: facturas trg_facturas_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_facturas_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.facturas FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_factura');

--
-- Name: facturas trg_facturas_proteger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_facturas_proteger BEFORE DELETE OR UPDATE ON public.facturas FOR EACH ROW EXECUTE FUNCTION public.fn_proteger_factura();

--
-- Name: TRIGGER trg_facturas_proteger ON facturas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TRIGGER trg_facturas_proteger ON public.facturas IS 'Protege la factura emitida: solo se puede anular; no se edita ni se borra (fn_proteger_factura).';

--
-- Name: notas_credito trg_notas_credito_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_notas_credito_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.notas_credito FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_nota_credito');

--
-- Name: notas_debito trg_notas_debito_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_notas_debito_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.notas_debito FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_nota_debito');

--
-- Name: puntos_expedicion trg_puntos_expedicion_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_puntos_expedicion_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.puntos_expedicion FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('SEGURIDAD', 'id_punto_expedicion');

--
-- Name: remisiones trg_remisiones_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_remisiones_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.remisiones FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_remision');

--
-- Name: remisiones trg_remisiones_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_remisiones_fecha_mod BEFORE UPDATE ON public.remisiones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: timbrados trg_timbrados_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_timbrados_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.timbrados FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('SEGURIDAD', 'id_timbrado');

--
-- Name: factura_detalle factura_detalle_id_consulta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT factura_detalle_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES public.consultas(id_consulta);

--
-- Name: factura_detalle factura_detalle_id_factura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT factura_detalle_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura) ON DELETE CASCADE;

--
-- Name: factura_detalle factura_detalle_id_item_servicio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT factura_detalle_id_item_servicio_fkey FOREIGN KEY (id_item_servicio) REFERENCES public.items_servicios(id_item_servicio);

--
-- Name: factura_detalle factura_detalle_id_tipo_impuesto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT factura_detalle_id_tipo_impuesto_fkey FOREIGN KEY (id_tipo_impuesto) REFERENCES public.tipos_impuestos(id_tipo_impuesto);

--
-- Name: factura_detalle factura_detalle_id_tipo_item_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.factura_detalle
    ADD CONSTRAINT factura_detalle_id_tipo_item_fkey FOREIGN KEY (id_tipo_item) REFERENCES public.tipos_items(id_tipo_item);

--
-- Name: facturas_borrador facturas_borrador_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas_borrador
    ADD CONSTRAINT facturas_borrador_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente);

--
-- Name: facturas_borrador facturas_borrador_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas_borrador
    ADD CONSTRAINT facturas_borrador_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: facturas_borrador facturas_borrador_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas_borrador
    ADD CONSTRAINT facturas_borrador_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: facturas facturas_id_condicion_venta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_condicion_venta_fkey FOREIGN KEY (id_condicion_venta) REFERENCES public.condiciones_venta(id_condicion_venta);

--
-- Name: facturas facturas_id_estado_factura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_estado_factura_fkey FOREIGN KEY (id_estado_factura) REFERENCES public.estados_factura(id_estado_factura);

--
-- Name: facturas facturas_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: facturas facturas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente);

--
-- Name: facturas facturas_id_pedido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_pedido_fkey FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido);

--
-- Name: facturas facturas_id_punto_expedicion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_punto_expedicion_fkey FOREIGN KEY (id_punto_expedicion) REFERENCES public.puntos_expedicion(id_punto_expedicion);

--
-- Name: facturas facturas_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES public.timbrados(id_timbrado);

--
-- Name: facturas facturas_id_tipo_comprobante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_id_tipo_comprobante_fkey FOREIGN KEY (id_tipo_comprobante) REFERENCES public.tipos_comprobantes(id_tipo_comprobante);

--
-- Name: facturas facturas_usuario_anulacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_usuario_anulacion_fkey FOREIGN KEY (usuario_anulacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: facturas facturas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: facturas facturas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: nota_credito_detalle nota_credito_detalle_id_factura_detalle_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_id_factura_detalle_fkey FOREIGN KEY (id_factura_detalle) REFERENCES public.factura_detalle(id_factura_detalle);

--
-- Name: nota_credito_detalle nota_credito_detalle_id_nota_credito_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_credito_detalle
    ADD CONSTRAINT nota_credito_detalle_id_nota_credito_fkey FOREIGN KEY (id_nota_credito) REFERENCES public.notas_credito(id_nota_credito) ON DELETE CASCADE;

--
-- Name: nota_debito_detalle nota_debito_detalle_id_factura_detalle_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_id_factura_detalle_fkey FOREIGN KEY (id_factura_detalle) REFERENCES public.factura_detalle(id_factura_detalle);

--
-- Name: nota_debito_detalle nota_debito_detalle_id_nota_debito_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nota_debito_detalle
    ADD CONSTRAINT nota_debito_detalle_id_nota_debito_fkey FOREIGN KEY (id_nota_debito) REFERENCES public.notas_debito(id_nota_debito) ON DELETE CASCADE;

--
-- Name: notas_credito notas_credito_id_factura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito
    ADD CONSTRAINT notas_credito_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);

--
-- Name: notas_credito notas_credito_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito
    ADD CONSTRAINT notas_credito_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: notas_credito notas_credito_id_tipo_comprobante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito
    ADD CONSTRAINT notas_credito_id_tipo_comprobante_fkey FOREIGN KEY (id_tipo_comprobante) REFERENCES public.tipos_comprobantes(id_tipo_comprobante);

--
-- Name: notas_credito notas_credito_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito
    ADD CONSTRAINT notas_credito_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: notas_credito notas_credito_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_credito
    ADD CONSTRAINT notas_credito_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: notas_debito notas_debito_id_factura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito
    ADD CONSTRAINT notas_debito_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);

--
-- Name: notas_debito notas_debito_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito
    ADD CONSTRAINT notas_debito_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: notas_debito notas_debito_id_tipo_comprobante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito
    ADD CONSTRAINT notas_debito_id_tipo_comprobante_fkey FOREIGN KEY (id_tipo_comprobante) REFERENCES public.tipos_comprobantes(id_tipo_comprobante);

--
-- Name: notas_debito notas_debito_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito
    ADD CONSTRAINT notas_debito_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: notas_debito notas_debito_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notas_debito
    ADD CONSTRAINT notas_debito_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: puntos_expedicion puntos_expedicion_id_timbrado_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puntos_expedicion
    ADD CONSTRAINT puntos_expedicion_id_timbrado_fkey FOREIGN KEY (id_timbrado) REFERENCES public.timbrados(id_timbrado);

--
-- Name: puntos_expedicion puntos_expedicion_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puntos_expedicion
    ADD CONSTRAINT puntos_expedicion_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: puntos_expedicion puntos_expedicion_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puntos_expedicion
    ADD CONSTRAINT puntos_expedicion_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: remision_detalle remision_detalle_id_item_servicio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remision_detalle
    ADD CONSTRAINT remision_detalle_id_item_servicio_fkey FOREIGN KEY (id_item_servicio) REFERENCES public.items_servicios(id_item_servicio);

--
-- Name: remision_detalle remision_detalle_id_remision_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remision_detalle
    ADD CONSTRAINT remision_detalle_id_remision_fkey FOREIGN KEY (id_remision) REFERENCES public.remisiones(id_remision) ON DELETE CASCADE;

--
-- Name: remisiones remisiones_id_factura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones
    ADD CONSTRAINT remisiones_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);

--
-- Name: remisiones remisiones_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones
    ADD CONSTRAINT remisiones_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente);

--
-- Name: remisiones remisiones_id_pedido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones
    ADD CONSTRAINT remisiones_id_pedido_fkey FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido);

--
-- Name: remisiones remisiones_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones
    ADD CONSTRAINT remisiones_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: remisiones remisiones_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.remisiones
    ADD CONSTRAINT remisiones_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: timbrados timbrados_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timbrados
    ADD CONSTRAINT timbrados_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: timbrados timbrados_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timbrados
    ADD CONSTRAINT timbrados_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
