-- 12_pedido_presupuesto.sql — Ítems de servicio, pedidos y presupuestos
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: items_servicios, pedidos, pedido_detalle, presupuestos, presupuesto_detalle.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/12_pedido_presupuesto.sql

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
-- Name: items_servicios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.items_servicios (
    id_item_servicio integer NOT NULL,
    des_item_servicio character varying(150) NOT NULL,
    cod_item_servicio character varying(20),
    id_tipo_item integer NOT NULL,
    item_precio_unitario numeric(18,2) DEFAULT 0 NOT NULL,
    id_moneda integer,
    aplica_impuesto boolean DEFAULT false NOT NULL,
    id_tipo_impuesto integer,
    est_item_servicio boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: items_servicios_id_item_servicio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.items_servicios_id_item_servicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: items_servicios_id_item_servicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.items_servicios_id_item_servicio_seq OWNED BY public.items_servicios.id_item_servicio;

--
-- Name: pedido_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pedido_detalle (
    id_pedido_detalle integer NOT NULL,
    id_pedido integer NOT NULL,
    id_item_servicio integer,
    item_descripcion character varying(200) NOT NULL,
    item_cantidad numeric(12,2) DEFAULT 1 NOT NULL,
    item_precio_unitario numeric(18,2) DEFAULT 0 NOT NULL,
    item_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    item_subtotal numeric(18,2) DEFAULT 0 NOT NULL,
    observaciones text,
    est_pedido_detalle boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: pedido_detalle_id_pedido_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pedido_detalle_id_pedido_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: pedido_detalle_id_pedido_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pedido_detalle_id_pedido_detalle_seq OWNED BY public.pedido_detalle.id_pedido_detalle;

--
-- Name: pedidos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pedidos (
    id_pedido integer NOT NULL,
    pedido_numero character varying(20) NOT NULL,
    id_paciente integer NOT NULL,
    id_profesional integer,
    fecha_pedido date NOT NULL,
    fecha_entrega date,
    pedido_subtotal numeric(18,2) DEFAULT 0 NOT NULL,
    pedido_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    pedido_total numeric(18,2) DEFAULT 0 NOT NULL,
    observaciones text,
    pedido_estado character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    est_pedido boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT chk_pedidos_estado CHECK (((pedido_estado)::text = ANY (ARRAY[('PENDIENTE'::character varying)::text, ('CONFIRMADO'::character varying)::text, ('FACTURADO'::character varying)::text, ('CANCELADO'::character varying)::text])))
);

--
-- Name: COLUMN pedidos.id_profesional; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.pedidos.id_profesional IS 'Especialista que solicita el pedido (opcional en el formulario).';

--
-- Name: pedidos_id_pedido_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pedidos_id_pedido_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: pedidos_id_pedido_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pedidos_id_pedido_seq OWNED BY public.pedidos.id_pedido;

--
-- Name: presupuesto_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.presupuesto_detalle (
    id_presupuesto_detalle integer NOT NULL,
    id_presupuesto integer NOT NULL,
    id_item_servicio integer,
    item_descripcion character varying(200) NOT NULL,
    item_cantidad numeric(12,2) DEFAULT 1 NOT NULL,
    item_precio_unitario numeric(18,2) DEFAULT 0 NOT NULL,
    item_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    item_subtotal numeric(18,2) DEFAULT 0 NOT NULL,
    observaciones text,
    est_presupuesto_detalle boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer
);

--
-- Name: presupuesto_detalle_id_presupuesto_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.presupuesto_detalle_id_presupuesto_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: presupuesto_detalle_id_presupuesto_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.presupuesto_detalle_id_presupuesto_detalle_seq OWNED BY public.presupuesto_detalle.id_presupuesto_detalle;

--
-- Name: presupuestos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.presupuestos (
    id_presupuesto integer NOT NULL,
    presupuesto_numero character varying(20) NOT NULL,
    id_paciente integer NOT NULL,
    id_profesional integer,
    fecha_presupuesto date NOT NULL,
    fecha_validez date,
    presupuesto_subtotal numeric(18,2) DEFAULT 0 NOT NULL,
    presupuesto_descuento numeric(18,2) DEFAULT 0 NOT NULL,
    presupuesto_total numeric(18,2) DEFAULT 0 NOT NULL,
    observaciones text,
    presupuesto_estado character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    est_presupuesto boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    id_pei integer,
    CONSTRAINT chk_presupuestos_estado CHECK (((presupuesto_estado)::text = ANY (ARRAY[('PENDIENTE'::character varying)::text, ('APROBADO'::character varying)::text, ('RECHAZADO'::character varying)::text, ('CONVERTIDO'::character varying)::text, ('VENCIDO'::character varying)::text])))
);

--
-- Name: COLUMN presupuestos.id_profesional; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.presupuestos.id_profesional IS 'Especialista que solicita el presupuesto (opcional en el formulario).';

--
-- Name: COLUMN presupuestos.id_pei; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.presupuestos.id_pei IS 'VersiÃ³n del PEI que presupuesta (opcional). Con valor, el PDF es el presupuesto de plan de tratamiento.';

--
-- Name: presupuestos_id_presupuesto_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.presupuestos_id_presupuesto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: presupuestos_id_presupuesto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.presupuestos_id_presupuesto_seq OWNED BY public.presupuestos.id_presupuesto;

--
-- Name: items_servicios id_item_servicio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios ALTER COLUMN id_item_servicio SET DEFAULT nextval('public.items_servicios_id_item_servicio_seq'::regclass);

--
-- Name: pedido_detalle id_pedido_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_detalle ALTER COLUMN id_pedido_detalle SET DEFAULT nextval('public.pedido_detalle_id_pedido_detalle_seq'::regclass);

--
-- Name: pedidos id_pedido; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos ALTER COLUMN id_pedido SET DEFAULT nextval('public.pedidos_id_pedido_seq'::regclass);

--
-- Name: presupuesto_detalle id_presupuesto_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuesto_detalle ALTER COLUMN id_presupuesto_detalle SET DEFAULT nextval('public.presupuesto_detalle_id_presupuesto_detalle_seq'::regclass);

--
-- Name: presupuestos id_presupuesto; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos ALTER COLUMN id_presupuesto SET DEFAULT nextval('public.presupuestos_id_presupuesto_seq'::regclass);

--
-- Name: items_servicios items_servicios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios
    ADD CONSTRAINT items_servicios_pkey PRIMARY KEY (id_item_servicio);

--
-- Name: pedido_detalle pedido_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_detalle
    ADD CONSTRAINT pedido_detalle_pkey PRIMARY KEY (id_pedido_detalle);

--
-- Name: pedidos pedidos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_pkey PRIMARY KEY (id_pedido);

--
-- Name: presupuesto_detalle presupuesto_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuesto_detalle
    ADD CONSTRAINT presupuesto_detalle_pkey PRIMARY KEY (id_presupuesto_detalle);

--
-- Name: presupuestos presupuestos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_pkey PRIMARY KEY (id_presupuesto);

--
-- Name: items_servicios uq_items_servicios_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios
    ADD CONSTRAINT uq_items_servicios_des UNIQUE (des_item_servicio);

--
-- Name: pedidos uq_pedidos_numero; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT uq_pedidos_numero UNIQUE (pedido_numero);

--
-- Name: presupuestos uq_presupuestos_numero; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT uq_presupuestos_numero UNIQUE (presupuesto_numero);

--
-- Name: idx_pedido_detalle_pedido; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pedido_detalle_pedido ON public.pedido_detalle USING btree (id_pedido);

--
-- Name: idx_pedidos_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pedidos_paciente ON public.pedidos USING btree (id_paciente);

--
-- Name: idx_presupuesto_detalle_presupuesto; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_presupuesto_detalle_presupuesto ON public.presupuesto_detalle USING btree (id_presupuesto);

--
-- Name: idx_presupuestos_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_presupuestos_paciente ON public.presupuestos USING btree (id_paciente);

--
-- Name: idx_presupuestos_pei; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_presupuestos_pei ON public.presupuestos USING btree (id_pei);

--
-- Name: items_servicios trg_items_servicios_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_items_servicios_fecha_mod BEFORE UPDATE ON public.items_servicios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: pedido_detalle trg_pedido_detalle_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pedido_detalle_fecha_mod BEFORE UPDATE ON public.pedido_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: pedidos trg_pedidos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pedidos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.pedidos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_pedido');

--
-- Name: pedidos trg_pedidos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_pedidos_fecha_mod BEFORE UPDATE ON public.pedidos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: presupuesto_detalle trg_presupuesto_detalle_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_presupuesto_detalle_fecha_mod BEFORE UPDATE ON public.presupuesto_detalle FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: presupuestos trg_presupuestos_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_presupuestos_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.presupuestos FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_presupuesto');

--
-- Name: presupuestos trg_presupuestos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_presupuestos_fecha_mod BEFORE UPDATE ON public.presupuestos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: items_servicios items_servicios_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios
    ADD CONSTRAINT items_servicios_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: items_servicios items_servicios_id_tipo_impuesto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios
    ADD CONSTRAINT items_servicios_id_tipo_impuesto_fkey FOREIGN KEY (id_tipo_impuesto) REFERENCES public.tipos_impuestos(id_tipo_impuesto);

--
-- Name: items_servicios items_servicios_id_tipo_item_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios
    ADD CONSTRAINT items_servicios_id_tipo_item_fkey FOREIGN KEY (id_tipo_item) REFERENCES public.tipos_items(id_tipo_item);

--
-- Name: items_servicios items_servicios_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios
    ADD CONSTRAINT items_servicios_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: items_servicios items_servicios_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items_servicios
    ADD CONSTRAINT items_servicios_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pedido_detalle pedido_detalle_id_item_servicio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_detalle
    ADD CONSTRAINT pedido_detalle_id_item_servicio_fkey FOREIGN KEY (id_item_servicio) REFERENCES public.items_servicios(id_item_servicio);

--
-- Name: pedido_detalle pedido_detalle_id_pedido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_detalle
    ADD CONSTRAINT pedido_detalle_id_pedido_fkey FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido) ON DELETE CASCADE;

--
-- Name: pedido_detalle pedido_detalle_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_detalle
    ADD CONSTRAINT pedido_detalle_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pedido_detalle pedido_detalle_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_detalle
    ADD CONSTRAINT pedido_detalle_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pedidos pedidos_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: pedidos pedidos_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: pedidos pedidos_id_profesional_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_id_profesional_fkey FOREIGN KEY (id_profesional) REFERENCES public.funcionarios(id_funcionario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: pedidos pedidos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: pedidos pedidos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: presupuesto_detalle presupuesto_detalle_id_item_servicio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuesto_detalle
    ADD CONSTRAINT presupuesto_detalle_id_item_servicio_fkey FOREIGN KEY (id_item_servicio) REFERENCES public.items_servicios(id_item_servicio);

--
-- Name: presupuesto_detalle presupuesto_detalle_id_presupuesto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuesto_detalle
    ADD CONSTRAINT presupuesto_detalle_id_presupuesto_fkey FOREIGN KEY (id_presupuesto) REFERENCES public.presupuestos(id_presupuesto) ON DELETE CASCADE;

--
-- Name: presupuesto_detalle presupuesto_detalle_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuesto_detalle
    ADD CONSTRAINT presupuesto_detalle_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: presupuesto_detalle presupuesto_detalle_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuesto_detalle
    ADD CONSTRAINT presupuesto_detalle_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: presupuestos presupuestos_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: presupuestos presupuestos_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: presupuestos presupuestos_id_pei_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_id_pei_fkey FOREIGN KEY (id_pei) REFERENCES public.pei(id_pei) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: presupuestos presupuestos_id_profesional_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_id_profesional_fkey FOREIGN KEY (id_profesional) REFERENCES public.funcionarios(id_funcionario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: presupuestos presupuestos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: presupuestos presupuestos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
