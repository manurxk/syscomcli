-- 14_caja.sql — Caja, depósitos y recaudaciones
-- Generado el 2026-10-19 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: cajas, depositos, aperturas_cierre_caja, arqueos_caja, recaudaciones.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/14_caja.sql

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
-- Name: aperturas_cierre_caja; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aperturas_cierre_caja (
    id_apertura_cierre integer NOT NULL,
    id_caja integer NOT NULL,
    id_usuario integer NOT NULL,
    tipo_operacion character varying(10) DEFAULT 'APERTURA'::character varying NOT NULL,
    fecha_operacion timestamp without time zone DEFAULT now() NOT NULL,
    saldo_inicial numeric(18,2) DEFAULT 0 NOT NULL,
    saldo_final numeric(18,2),
    monto_efectivo numeric(18,2) DEFAULT 0 NOT NULL,
    monto_cheques numeric(18,2) DEFAULT 0 NOT NULL,
    monto_tarjetas numeric(18,2) DEFAULT 0 NOT NULL,
    monto_transferencias numeric(18,2) DEFAULT 0 NOT NULL,
    observaciones text,
    est_apertura_cierre character varying(1) DEFAULT 'A'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT chk_acc_estado CHECK (((est_apertura_cierre)::text = ANY ((ARRAY['A'::character varying, 'C'::character varying])::text[]))),
    CONSTRAINT chk_acc_tipo_op CHECK (((tipo_operacion)::text = ANY ((ARRAY['APERTURA'::character varying, 'CIERRE'::character varying])::text[])))
);

--
-- Name: aperturas_cierre_caja_id_apertura_cierre_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.aperturas_cierre_caja_id_apertura_cierre_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: aperturas_cierre_caja_id_apertura_cierre_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.aperturas_cierre_caja_id_apertura_cierre_seq OWNED BY public.aperturas_cierre_caja.id_apertura_cierre;

--
-- Name: arqueos_caja; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.arqueos_caja (
    id_arqueo integer NOT NULL,
    id_apertura_cierre integer NOT NULL,
    id_caja integer NOT NULL,
    arqueo_numero character varying(20) NOT NULL,
    fecha_arqueo timestamp without time zone DEFAULT now() NOT NULL,
    monto_esperado numeric(18,2) DEFAULT 0 NOT NULL,
    monto_real numeric(18,2) DEFAULT 0 NOT NULL,
    diferencia numeric(18,2) DEFAULT 0 NOT NULL,
    observaciones text,
    est_arqueo character varying(20) DEFAULT 'CONCILIADO'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_arqueos_estado CHECK (((est_arqueo)::text = ANY ((ARRAY['CONCILIADO'::character varying, 'CON_DIFERENCIA'::character varying])::text[])))
);

--
-- Name: arqueos_caja_id_arqueo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.arqueos_caja_id_arqueo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: arqueos_caja_id_arqueo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.arqueos_caja_id_arqueo_seq OWNED BY public.arqueos_caja.id_arqueo;

--
-- Name: cajas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cajas (
    id_caja integer NOT NULL,
    des_caja character varying(100) NOT NULL,
    cod_caja character varying(20),
    caja_saldo_inicial numeric(18,2) DEFAULT 0 NOT NULL,
    caja_saldo_actual numeric(18,2) DEFAULT 0 NOT NULL,
    caja_estado character varying(10) DEFAULT 'CERRADA'::character varying NOT NULL,
    est_caja boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT chk_cajas_estado CHECK (((caja_estado)::text = ANY ((ARRAY['ABIERTA'::character varying, 'CERRADA'::character varying])::text[]))),
    CONSTRAINT chk_cajas_saldo_inicial CHECK ((caja_saldo_inicial >= (0)::numeric))
);

--
-- Name: cajas_id_caja_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cajas_id_caja_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: cajas_id_caja_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cajas_id_caja_seq OWNED BY public.cajas.id_caja;

--
-- Name: depositos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.depositos (
    id_deposito integer NOT NULL,
    des_deposito character varying(150) NOT NULL,
    cod_deposito character varying(20),
    tipo_deposito character varying(20) DEFAULT 'BANCO'::character varying NOT NULL,
    numero_cuenta character varying(50),
    banco_deposito character varying(100),
    ruc_banco character varying(20),
    moneda_deposito character varying(10) DEFAULT 'PYG'::character varying NOT NULL,
    est_deposito boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_depositos_tipo CHECK (((tipo_deposito)::text = ANY ((ARRAY['BANCO'::character varying, 'CUENTA_CORRIENTE'::character varying, 'CAJA_AHORRO'::character varying, 'BILLETERA_DIGITAL'::character varying])::text[])))
);

--
-- Name: depositos_id_deposito_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.depositos_id_deposito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: depositos_id_deposito_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.depositos_id_deposito_seq OWNED BY public.depositos.id_deposito;

--
-- Name: recaudaciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recaudaciones (
    id_recaudacion integer NOT NULL,
    recaudacion_numero character varying(20) NOT NULL,
    id_caja integer NOT NULL,
    id_deposito integer NOT NULL,
    id_usuario integer,
    fecha_recaudacion timestamp without time zone DEFAULT now() NOT NULL,
    fecha_deposito date,
    monto_total numeric(18,2) DEFAULT 0 NOT NULL,
    monto_efectivo numeric(18,2) DEFAULT 0 NOT NULL,
    monto_cheques numeric(18,2) DEFAULT 0 NOT NULL,
    monto_tarjetas numeric(18,2) DEFAULT 0 NOT NULL,
    observaciones text,
    est_recaudacion character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    id_moneda integer DEFAULT 1 NOT NULL,
    CONSTRAINT recaudaciones_est_recaudacion_check CHECK (((est_recaudacion)::text = ANY ((ARRAY['PENDIENTE'::character varying, 'DEPOSITADA'::character varying, 'ANULADA'::character varying])::text[])))
);

--
-- Name: recaudaciones_id_recaudacion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.recaudaciones_id_recaudacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: recaudaciones_id_recaudacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.recaudaciones_id_recaudacion_seq OWNED BY public.recaudaciones.id_recaudacion;

--
-- Name: aperturas_cierre_caja id_apertura_cierre; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aperturas_cierre_caja ALTER COLUMN id_apertura_cierre SET DEFAULT nextval('public.aperturas_cierre_caja_id_apertura_cierre_seq'::regclass);

--
-- Name: arqueos_caja id_arqueo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.arqueos_caja ALTER COLUMN id_arqueo SET DEFAULT nextval('public.arqueos_caja_id_arqueo_seq'::regclass);

--
-- Name: cajas id_caja; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas ALTER COLUMN id_caja SET DEFAULT nextval('public.cajas_id_caja_seq'::regclass);

--
-- Name: depositos id_deposito; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.depositos ALTER COLUMN id_deposito SET DEFAULT nextval('public.depositos_id_deposito_seq'::regclass);

--
-- Name: recaudaciones id_recaudacion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones ALTER COLUMN id_recaudacion SET DEFAULT nextval('public.recaudaciones_id_recaudacion_seq'::regclass);

--
-- Name: aperturas_cierre_caja aperturas_cierre_caja_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aperturas_cierre_caja
    ADD CONSTRAINT aperturas_cierre_caja_pkey PRIMARY KEY (id_apertura_cierre);

--
-- Name: arqueos_caja arqueos_caja_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.arqueos_caja
    ADD CONSTRAINT arqueos_caja_pkey PRIMARY KEY (id_arqueo);

--
-- Name: cajas cajas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT cajas_pkey PRIMARY KEY (id_caja);

--
-- Name: depositos depositos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.depositos
    ADD CONSTRAINT depositos_pkey PRIMARY KEY (id_deposito);

--
-- Name: recaudaciones recaudaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_pkey PRIMARY KEY (id_recaudacion);

--
-- Name: recaudaciones recaudaciones_recaudacion_numero_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_recaudacion_numero_key UNIQUE (recaudacion_numero);

--
-- Name: arqueos_caja uq_arqueos_numero; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.arqueos_caja
    ADD CONSTRAINT uq_arqueos_numero UNIQUE (arqueo_numero);

--
-- Name: cajas uq_cajas_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT uq_cajas_des UNIQUE (des_caja);

--
-- Name: depositos uq_depositos_des; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.depositos
    ADD CONSTRAINT uq_depositos_des UNIQUE (des_deposito);

--
-- Name: recaudaciones tg_recaudaciones_fmod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_recaudaciones_fmod BEFORE UPDATE ON public.recaudaciones FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: aperturas_cierre_caja trg_aperturas_cierre_caja_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_aperturas_cierre_caja_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.aperturas_cierre_caja FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_apertura_cierre');

--
-- Name: aperturas_cierre_caja trg_aperturas_cierre_caja_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_aperturas_cierre_caja_fecha_mod BEFORE UPDATE ON public.aperturas_cierre_caja FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: arqueos_caja trg_arqueos_caja_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_arqueos_caja_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.arqueos_caja FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_arqueo');

--
-- Name: arqueos_caja trg_arqueos_caja_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_arqueos_caja_fecha_mod BEFORE UPDATE ON public.arqueos_caja FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: cajas trg_cajas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_cajas_fecha_mod BEFORE UPDATE ON public.cajas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: depositos trg_depositos_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_depositos_fecha_mod BEFORE UPDATE ON public.depositos FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: recaudaciones trg_recaudaciones_auditoria; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_recaudaciones_auditoria AFTER INSERT OR DELETE OR UPDATE ON public.recaudaciones FOR EACH ROW EXECUTE FUNCTION public.fn_auditar_cambios('VENTAS', 'id_recaudacion');

--
-- Name: aperturas_cierre_caja aperturas_cierre_caja_id_caja_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aperturas_cierre_caja
    ADD CONSTRAINT aperturas_cierre_caja_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES public.cajas(id_caja);

--
-- Name: aperturas_cierre_caja aperturas_cierre_caja_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aperturas_cierre_caja
    ADD CONSTRAINT aperturas_cierre_caja_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: aperturas_cierre_caja aperturas_cierre_caja_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aperturas_cierre_caja
    ADD CONSTRAINT aperturas_cierre_caja_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);

--
-- Name: aperturas_cierre_caja aperturas_cierre_caja_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aperturas_cierre_caja
    ADD CONSTRAINT aperturas_cierre_caja_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: aperturas_cierre_caja aperturas_cierre_caja_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aperturas_cierre_caja
    ADD CONSTRAINT aperturas_cierre_caja_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: arqueos_caja arqueos_caja_id_apertura_cierre_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.arqueos_caja
    ADD CONSTRAINT arqueos_caja_id_apertura_cierre_fkey FOREIGN KEY (id_apertura_cierre) REFERENCES public.aperturas_cierre_caja(id_apertura_cierre);

--
-- Name: arqueos_caja arqueos_caja_id_caja_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.arqueos_caja
    ADD CONSTRAINT arqueos_caja_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES public.cajas(id_caja);

--
-- Name: arqueos_caja arqueos_caja_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.arqueos_caja
    ADD CONSTRAINT arqueos_caja_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: arqueos_caja arqueos_caja_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.arqueos_caja
    ADD CONSTRAINT arqueos_caja_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: cajas cajas_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT cajas_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: cajas cajas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT cajas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: cajas cajas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT cajas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: depositos depositos_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.depositos
    ADD CONSTRAINT depositos_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: depositos depositos_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.depositos
    ADD CONSTRAINT depositos_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: recaudaciones recaudaciones_id_caja_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_id_caja_fkey FOREIGN KEY (id_caja) REFERENCES public.cajas(id_caja);

--
-- Name: recaudaciones recaudaciones_id_deposito_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_id_deposito_fkey FOREIGN KEY (id_deposito) REFERENCES public.depositos(id_deposito);

--
-- Name: recaudaciones recaudaciones_id_moneda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_id_moneda_fkey FOREIGN KEY (id_moneda) REFERENCES public.monedas(id_moneda);

--
-- Name: recaudaciones recaudaciones_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);

--
-- Name: recaudaciones recaudaciones_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: recaudaciones recaudaciones_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recaudaciones
    ADD CONSTRAINT recaudaciones_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
