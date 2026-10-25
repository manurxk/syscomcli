-- 15_cobranza_cxc.sql — Cuentas a cobrar, cobranzas y libro de ventas
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: cuentas_cobrar, libro_ventas, cobranzas, cobranza_detalle.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/15_cobranza_cxc.sql

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
-- Name: cobranza_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cobranza_detalle (
    id_cobranza_detalle integer NOT NULL,
    id_cobranza integer NOT NULL,
    id_forma_cobro integer NOT NULL,
    id_marca_tarjeta integer,
    id_entidad_adherida integer,
    id_entidad_emisora integer,
    numero_cheque character varying(50),
    numero_tarjeta character varying(20),
    numero_cuotas smallint DEFAULT 1,
    monto_cobrado numeric(18,2) NOT NULL,
    observaciones text,
    numero_transferencia character varying(50)
);

--
-- Name: cobranza_detalle_id_cobranza_detalle_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cobranza_detalle_id_cobranza_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: cobranza_detalle_id_cobranza_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cobranza_detalle_id_cobranza_detalle_seq OWNED BY public.cobranza_detalle.id_cobranza_detalle;

--
-- Name: cobranzas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cobranzas (
    id_cobranza integer NOT NULL,
    cobranza_numero character varying(20) NOT NULL,
    id_cuenta_cobrar integer NOT NULL,
    id_factura integer NOT NULL,
    id_caja integer NOT NULL,
    fecha_cobranza timestamp without time zone DEFAULT now() NOT NULL,
    monto_cobrado numeric(18,2) NOT NULL,
    observaciones text,
    est_cobranza character varying(20) DEFAULT 'REGISTRADA'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT cobranzas_est_cobranza_check CHECK (((est_cobranza)::text = ANY (ARRAY[('REGISTRADA'::character varying)::text, ('ANULADA'::character varying)::text])))
);

--
-- Name: cobranzas_id_cobranza_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cobranzas_id_cobranza_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: cobranzas_id_cobranza_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cobranzas_id_cobranza_seq OWNED BY public.cobranzas.id_cobranza;

--
-- Name: cuentas_cobrar; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cuentas_cobrar (
    id_cuenta_cobrar integer NOT NULL,
    cuenta_numero character varying(20) NOT NULL,
    id_factura integer,
    id_paciente integer,
    fecha_emision timestamp without time zone DEFAULT now() NOT NULL,
    fecha_vencimiento date,
    monto_total numeric(18,2) DEFAULT 0 NOT NULL,
    monto_pagado numeric(18,2) DEFAULT 0 NOT NULL,
    monto_pendiente numeric(18,2) DEFAULT 0 NOT NULL,
    numero_cuotas integer DEFAULT 1 NOT NULL,
    cuota_actual integer DEFAULT 1 NOT NULL,
    est_cuenta_cobrar character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT cuentas_cobrar_est_cuenta_cobrar_check CHECK (((est_cuenta_cobrar)::text = ANY (ARRAY['PENDIENTE'::text, 'PARCIAL'::text, 'COBRADA'::text, 'VENCIDA'::text, 'ANULADA'::text])))
);

--
-- Name: cuentas_cobrar_id_cuenta_cobrar_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cuentas_cobrar_id_cuenta_cobrar_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: cuentas_cobrar_id_cuenta_cobrar_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cuentas_cobrar_id_cuenta_cobrar_seq OWNED BY public.cuentas_cobrar.id_cuenta_cobrar;

--
-- Name: libro_ventas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.libro_ventas (
    id_libro_ventas integer NOT NULL,
    libro_fecha date NOT NULL,
    tipo_comprobante character varying(20) NOT NULL,
    numero_comprobante character varying(30) NOT NULL,
    id_paciente integer,
    id_factura integer,
    id_nota_credito integer,
    id_nota_debito integer,
    monto_gravado numeric(18,2) DEFAULT 0 NOT NULL,
    monto_exento numeric(18,2) DEFAULT 0 NOT NULL,
    monto_iva numeric(18,2) DEFAULT 0 NOT NULL,
    monto_total numeric(18,2) DEFAULT 0 NOT NULL,
    codigo_sifen character varying(44),
    numero_timbrado character varying(8),
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT libro_ventas_tipo_comprobante_check CHECK (((tipo_comprobante)::text = ANY (ARRAY[('FACTURA'::character varying)::text, ('NOTA_CREDITO'::character varying)::text, ('NOTA_DEBITO'::character varying)::text])))
);

--
-- Name: COLUMN libro_ventas.codigo_sifen; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.libro_ventas.codigo_sifen IS 'CDC del comprobante en SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';

--
-- Name: libro_ventas_id_libro_ventas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.libro_ventas_id_libro_ventas_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: libro_ventas_id_libro_ventas_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.libro_ventas_id_libro_ventas_seq OWNED BY public.libro_ventas.id_libro_ventas;

--
-- Name: v_caja_movimientos; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_caja_movimientos AS
 SELECT ac.fecha_operacion AS fecha_movimiento,
    ac.id_caja,
    ca.cod_caja,
    ca.des_caja,
    ac.id_moneda,
    m.cod_moneda,
    m.simbolo_moneda,
    m.decimales_moneda,
    ac.tipo_operacion AS tipo_movimiento,
    NULL::character varying AS referencia,
        CASE ac.tipo_operacion
            WHEN 'APERTURA'::text THEN ac.saldo_inicial
            ELSE ac.saldo_final
        END AS monto,
    ac.est_apertura_cierre AS estado
   FROM ((public.aperturas_cierre_caja ac
     JOIN public.cajas ca ON ((ca.id_caja = ac.id_caja)))
     JOIN public.monedas m ON ((m.id_moneda = ac.id_moneda)))
UNION ALL
 SELECT co.fecha_cobranza AS fecha_movimiento,
    co.id_caja,
    ca.cod_caja,
    ca.des_caja,
    co.id_moneda,
    m.cod_moneda,
    m.simbolo_moneda,
    m.decimales_moneda,
    'COBRANZA'::character varying AS tipo_movimiento,
    co.cobranza_numero AS referencia,
    co.monto_cobrado AS monto,
    co.est_cobranza AS estado
   FROM ((public.cobranzas co
     JOIN public.cajas ca ON ((ca.id_caja = co.id_caja)))
     JOIN public.monedas m ON ((m.id_moneda = co.id_moneda)));

--
-- Name: VIEW v_caja_movimientos; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_caja_movimientos IS 'Línea de tiempo de cada caja: APERTURA (saldo inicial), COBRANZA (monto cobrado; excluir estado ANULADA) y CIERRE (saldo final). La moneda es la de la apertura de la caja; no sumar monedas distintas.';

--
-- Name: v_facturacion_mensual; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_facturacion_mensual AS
 SELECT (date_trunc('month'::text, (lv.libro_fecha)::timestamp with time zone))::date AS mes,
    lv.id_moneda,
    m.cod_moneda,
    m.simbolo_moneda,
    m.decimales_moneda,
    m.es_moneda_local,
    count(*) FILTER (WHERE ((lv.tipo_comprobante)::text = 'FACTURA'::text)) AS cantidad_facturas,
    count(*) FILTER (WHERE ((lv.tipo_comprobante)::text = 'NOTA_CREDITO'::text)) AS cantidad_notas_credito,
    count(*) AS cantidad_comprobantes,
    sum(
        CASE
            WHEN ((lv.tipo_comprobante)::text = 'NOTA_CREDITO'::text) THEN (- lv.monto_gravado)
            ELSE lv.monto_gravado
        END) AS total_gravado,
    sum(
        CASE
            WHEN ((lv.tipo_comprobante)::text = 'NOTA_CREDITO'::text) THEN (- lv.monto_iva)
            ELSE lv.monto_iva
        END) AS total_iva,
    sum(
        CASE
            WHEN ((lv.tipo_comprobante)::text = 'NOTA_CREDITO'::text) THEN (- lv.monto_total)
            ELSE lv.monto_total
        END) AS total_neto,
    COALESCE(sum(lv.monto_total) FILTER (WHERE ((lv.tipo_comprobante)::text = 'NOTA_CREDITO'::text)), (0)::numeric) AS total_notas_credito
   FROM (public.libro_ventas lv
     JOIN public.monedas m ON ((m.id_moneda = lv.id_moneda)))
  GROUP BY (date_trunc('month'::text, (lv.libro_fecha)::timestamp with time zone)), lv.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda, m.es_moneda_local;

--
-- Name: VIEW v_facturacion_mensual; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_facturacion_mensual IS 'Totales del libro de ventas por mes y moneda. En el libro la nota de crédito se guarda en positivo: aquí resta de gravado, IVA y total_neto, y total_notas_credito la muestra aparte. No sumar monedas distintas.';

--
-- Name: v_saldo_cuentas_cobrar; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_saldo_cuentas_cobrar AS
 SELECT cc.id_cuenta_cobrar,
    cc.cuenta_numero,
    cc.id_factura,
    f.factura_numero,
    cc.id_paciente,
    concat(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
    cc.fecha_emision,
    cc.fecha_vencimiento,
    cc.id_moneda,
    m.cod_moneda,
    m.simbolo_moneda,
    m.decimales_moneda,
    m.es_moneda_local,
    cc.monto_total,
    cc.monto_pagado,
    cc.monto_pendiente,
    cc.est_cuenta_cobrar,
    ((((cc.est_cuenta_cobrar)::text = 'PENDIENTE'::text) OR ((cc.est_cuenta_cobrar)::text = 'PARCIAL'::text)) AND (cc.fecha_vencimiento < CURRENT_DATE)) AS esta_vencida,
        CASE
            WHEN ((((cc.est_cuenta_cobrar)::text = 'PENDIENTE'::text) OR ((cc.est_cuenta_cobrar)::text = 'PARCIAL'::text)) AND (cc.fecha_vencimiento < CURRENT_DATE)) THEN (CURRENT_DATE - cc.fecha_vencimiento)
            ELSE 0
        END AS dias_atraso
   FROM ((((public.cuentas_cobrar cc
     JOIN public.facturas f ON ((f.id_factura = cc.id_factura)))
     JOIN public.monedas m ON ((m.id_moneda = cc.id_moneda)))
     LEFT JOIN public.pacientes pa ON ((pa.id_paciente = cc.id_paciente)))
     LEFT JOIN public.personas pp ON ((pp.id_persona = pa.id_persona)))
  WHERE (f.fecha_anulacion IS NULL);

--
-- Name: VIEW v_saldo_cuentas_cobrar; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_saldo_cuentas_cobrar IS 'Cuentas por cobrar de facturas no anuladas, con moneda, saldo pendiente y días de atraso. Para el saldo por cobrar filtrar est_cuenta_cobrar IN (PENDIENTE, PARCIAL); no sumar monedas distintas. Fuente de Resumen y Ventas en Reportes.';

--
-- Name: cobranza_detalle id_cobranza_detalle; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranza_detalle ALTER COLUMN id_cobranza_detalle SET DEFAULT nextval('public.cobranza_detalle_id_cobranza_detalle_seq'::regclass);

--
-- Name: cobranzas id_cobranza; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas ALTER COLUMN id_cobranza SET DEFAULT nextval('public.cobranzas_id_cobranza_seq'::regclass);

--
-- Name: cuentas_cobrar id_cuenta_cobrar; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar ALTER COLUMN id_cuenta_cobrar SET DEFAULT nextval('public.cuentas_cobrar_id_cuenta_cobrar_seq'::regclass);

--
-- Name: libro_ventas id_libro_ventas; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas ALTER COLUMN id_libro_ventas SET DEFAULT nextval('public.libro_ventas_id_libro_ventas_seq'::regclass);

--
-- Name: cobranza_detalle cobranza_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_pkey PRIMARY KEY (id_cobranza_detalle);

--
-- Name: cobranzas cobranzas_cobranza_numero_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_cobranza_numero_key UNIQUE (cobranza_numero);

--
-- Name: cobranzas cobranzas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_pkey PRIMARY KEY (id_cobranza);

--
-- Name: cuentas_cobrar cuentas_cobrar_cuenta_numero_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_cuenta_numero_key UNIQUE (cuenta_numero);

--
-- Name: cuentas_cobrar cuentas_cobrar_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_pkey PRIMARY KEY (id_cuenta_cobrar);

--
-- Name: libro_ventas libro_ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas
    ADD CONSTRAINT libro_ventas_pkey PRIMARY KEY (id_libro_ventas);

--
-- Name: idx_cobranzas_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cobranzas_fecha ON public.cobranzas USING btree (((fecha_cobranza)::date));

--
-- Name: idx_libro_ventas_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_libro_ventas_fecha ON public.libro_ventas USING btree (libro_fecha);

--
-- Name: cuentas_cobrar tg_cuentas_cobrar_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_cuentas_cobrar_fmod BEFORE UPDATE ON public.cuentas_cobrar FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: cobranzas trg_cobranzas_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_cobranzas_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.cobranzas FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_cobranza');

--
-- Name: cobranzas trg_cobranzas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_cobranzas_fecha_mod BEFORE UPDATE ON public.cobranzas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: cuentas_cobrar trg_cuentas_cobrar_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_cuentas_cobrar_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.cuentas_cobrar FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_cuenta_cobrar');

--
-- Name: cobranza_detalle cobranza_detalle_id_cobranza_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_cobranza_fkey FOREIGN KEY (id_cobranza) REFERENCES public.cobranzas(id_cobranza);

--
-- Name: cobranza_detalle cobranza_detalle_id_entidad_adherida_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_entidad_adherida_fkey FOREIGN KEY (id_entidad_adherida) REFERENCES public.entidades_adheridas(id_entidad_adherida);

--
-- Name: cobranza_detalle cobranza_detalle_id_entidad_emisora_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_entidad_emisora_fkey FOREIGN KEY (id_entidad_emisora) REFERENCES public.entidades_emisoras(id_entidad_emisora);

--
-- Name: cobranza_detalle cobranza_detalle_id_forma_cobro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_forma_cobro_fkey FOREIGN KEY (id_forma_cobro) REFERENCES public.formas_cobro(id_forma_cobro);

--
-- Name: cobranza_detalle cobranza_detalle_id_marca_tarjeta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranza_detalle
    ADD CONSTRAINT cobranza_detalle_id_marca_tarjeta_fkey FOREIGN KEY (id_marca_tarjeta) REFERENCES public.marcas_tarjeta(id_marca_tarjeta);

--
-- Name: cobranzas cobranzas_id_caja_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES public.cajas(id_caja);

--
-- Name: cobranzas cobranzas_id_cuenta_cobrar_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_id_cuenta_cobrar_fkey FOREIGN KEY (id_cuenta_cobrar) REFERENCES public.cuentas_cobrar(id_cuenta_cobrar);

--
-- Name: cobranzas cobranzas_id_factura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);

--
-- Name: cobranzas cobranzas_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: cobranzas cobranzas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: cobranzas cobranzas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cobranzas
    ADD CONSTRAINT cobranzas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: cuentas_cobrar cuentas_cobrar_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: cuentas_cobrar cuentas_cobrar_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente);

--
-- Name: cuentas_cobrar cuentas_cobrar_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: cuentas_cobrar cuentas_cobrar_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar
    ADD CONSTRAINT cuentas_cobrar_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: cuentas_cobrar fk_cc_factura; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cuentas_cobrar
    ADD CONSTRAINT fk_cc_factura FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);

--
-- Name: libro_ventas fk_lv_factura; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas
    ADD CONSTRAINT fk_lv_factura FOREIGN KEY (id_factura) REFERENCES public.facturas(id_factura);

--
-- Name: libro_ventas fk_lv_nota_credito; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas
    ADD CONSTRAINT fk_lv_nota_credito FOREIGN KEY (id_nota_credito) REFERENCES public.notas_credito(id_nota_credito);

--
-- Name: libro_ventas fk_lv_nota_debito; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas
    ADD CONSTRAINT fk_lv_nota_debito FOREIGN KEY (id_nota_debito) REFERENCES public.notas_debito(id_nota_debito);

--
-- Name: libro_ventas libro_ventas_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas
    ADD CONSTRAINT libro_ventas_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: libro_ventas libro_ventas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas
    ADD CONSTRAINT libro_ventas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente);

--
-- Name: libro_ventas libro_ventas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libro_ventas
    ADD CONSTRAINT libro_ventas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);
