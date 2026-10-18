-- 07_agenda_citas.sql — Agenda y citas
-- Generado el 2026-10-18 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Tablas: agenda_horarios, slots_agenda, citas, citas_log_estados, lista_espera, recordatorios.
-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/07_agenda_citas.sql

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
-- Name: agenda_horarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.agenda_horarios (
    id_agenda_horario integer NOT NULL,
    id_especialista integer NOT NULL,
    id_sede integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_dia_semana integer NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fin time without time zone NOT NULL,
    duracion_turno_min smallint DEFAULT 30 NOT NULL,
    cupos_totales smallint DEFAULT 1 NOT NULL,
    modalidad_default character varying(20) DEFAULT 'PRESENCIAL'::character varying NOT NULL,
    porcentaje_overbooking smallint DEFAULT 0 NOT NULL,
    fec_desde date DEFAULT CURRENT_DATE NOT NULL,
    fec_hasta date,
    est_agenda_horario boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_agenda_horarios_duracion CHECK ((duracion_turno_min = ANY (ARRAY[10, 15, 20, 30, 45, 60, 90]))),
    CONSTRAINT chk_agenda_horarios_modalidad CHECK (((modalidad_default)::text = ANY ((ARRAY['PRESENCIAL'::character varying, 'TELEMEDICINA'::character varying, 'DOMICILIO'::character varying])::text[]))),
    CONSTRAINT chk_agenda_horarios_overbooking CHECK (((porcentaje_overbooking >= 0) AND (porcentaje_overbooking <= 100))),
    CONSTRAINT chk_agenda_horarios_rango_fecha CHECK (((fec_hasta IS NULL) OR (fec_hasta >= fec_desde))),
    CONSTRAINT chk_agenda_horarios_rango_hora CHECK ((hora_fin > hora_inicio))
);

--
-- Name: TABLE agenda_horarios; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.agenda_horarios IS 'Configuración semanal recurrente de atención. No se valida solapamiento de (id_consultorio, id_dia_semana) con un EXCLUDE de BD: se valida en el DAO al guardar/editar (validarConflictoHorario), igual criterio que el resto del sistema.';

--
-- Name: agenda_horarios_id_agenda_horario_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.agenda_horarios_id_agenda_horario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: agenda_horarios_id_agenda_horario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.agenda_horarios_id_agenda_horario_seq OWNED BY public.agenda_horarios.id_agenda_horario;

--
-- Name: citas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.citas (
    id_cita integer NOT NULL,
    id_paciente integer NOT NULL,
    id_especialista integer NOT NULL,
    id_especialidad integer,
    id_sede integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_slot_agenda integer,
    id_estado_cita integer NOT NULL,
    cita_inicio timestamp without time zone NOT NULL,
    cita_fin timestamp without time zone NOT NULL,
    modalidad character varying(20) DEFAULT 'PRESENCIAL'::character varying NOT NULL,
    cita_es_primera_vez boolean DEFAULT true NOT NULL,
    cita_numero_sesion smallint,
    motivo text,
    observaciones text,
    motivo_cancelacion text,
    est_cita boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_citas_modalidad CHECK (((modalidad)::text = ANY ((ARRAY['PRESENCIAL'::character varying, 'TELEMEDICINA'::character varying, 'DOMICILIO'::character varying])::text[]))),
    CONSTRAINT chk_citas_rango CHECK ((cita_fin > cita_inicio))
);

--
-- Name: TABLE citas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.citas IS 'Paciente y especialista quedan fijos al reprogramar (decisión de diseño: cambiarlos complicaría paciente_profesional/recordatorios/historial). Reprogramar libera el slot viejo y reserva el nuevo. cod_origen_cita (MANUAL/DERIVACION) se agrega en Fase C cuando exista derivaciones, vía ALTER TABLE — no se agrega ahora para no anticipar una dependencia que todavía no existe.';

--
-- Name: citas_id_cita_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.citas_id_cita_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: citas_id_cita_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.citas_id_cita_seq OWNED BY public.citas.id_cita;

--
-- Name: citas_log_estados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.citas_log_estados (
    id_cita_log_estado integer NOT NULL,
    id_cita integer NOT NULL,
    id_estado_anterior integer,
    id_estado_nuevo integer NOT NULL,
    motivo_cambio text,
    usuario_cambio integer,
    fecha_cambio timestamp without time zone DEFAULT now() NOT NULL
);

--
-- Name: TABLE citas_log_estados; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.citas_log_estados IS 'Solo INSERT — sin trigger de fecha_modificacion ni columna est_*: una fila de auditoría no se edita ni se da de baja.';

--
-- Name: citas_log_estados_id_cita_log_estado_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.citas_log_estados_id_cita_log_estado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: citas_log_estados_id_cita_log_estado_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.citas_log_estados_id_cita_log_estado_seq OWNED BY public.citas_log_estados.id_cita_log_estado;

--
-- Name: lista_espera; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lista_espera (
    id_lista_espera integer NOT NULL,
    id_agenda_horario integer NOT NULL,
    id_paciente integer NOT NULL,
    estado character varying(20) DEFAULT 'PENDIENTE'::character varying NOT NULL,
    prioridad smallint DEFAULT 0 NOT NULL,
    motivo text,
    fec_ultima_notificacion timestamp without time zone,
    est_lista_espera boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_lista_espera_estado CHECK (((estado)::text = ANY ((ARRAY['PENDIENTE'::character varying, 'NOTIFICADO'::character varying, 'ACEPTADO'::character varying, 'EXPIRADO'::character varying, 'CANCELADO'::character varying])::text[])))
);

--
-- Name: TABLE lista_espera; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.lista_espera IS 'Sin automatización: el staff anota al paciente y cuando detecta un cupo libre lo contacta por fuera del sistema, reflejando el resultado a mano (PENDIENTE->NOTIFICADO->ACEPTADO/EXPIRADO, o PENDIENTE->CANCELADO). Se descartó un productor automático por sobre-ingeniería.';

--
-- Name: lista_espera_id_lista_espera_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lista_espera_id_lista_espera_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: lista_espera_id_lista_espera_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lista_espera_id_lista_espera_seq OWNED BY public.lista_espera.id_lista_espera;

--
-- Name: recordatorios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recordatorios (
    id_recordatorio integer NOT NULL,
    id_cita integer NOT NULL,
    canal character varying(20) NOT NULL,
    minutos_antes integer NOT NULL,
    est_recordatorio boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_recordatorios_canal CHECK (((canal)::text = ANY ((ARRAY['WHATSAPP'::character varying, 'SMS'::character varying, 'EMAIL'::character varying, 'PUSH'::character varying])::text[]))),
    CONSTRAINT chk_recordatorios_minutos CHECK ((minutos_antes > 0))
);

--
-- Name: TABLE recordatorios; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.recordatorios IS 'Reglas default (WHATSAPP,1440min)+(WHATSAPP,120min) creadas al confirmar una cita. Sin notificaciones_cola/notificaciones_log separadas (esa cola es complejidad multi-tenant que no aplica aquí): el envío real se resuelve en el mismo job que evalúa la ventana de la regla.';

--
-- Name: recordatorios_id_recordatorio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.recordatorios_id_recordatorio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: recordatorios_id_recordatorio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.recordatorios_id_recordatorio_seq OWNED BY public.recordatorios.id_recordatorio;

--
-- Name: slots_agenda; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.slots_agenda (
    id_slot_agenda integer NOT NULL,
    id_agenda_horario integer NOT NULL,
    id_sede integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_especialista integer NOT NULL,
    slot_inicio timestamp without time zone NOT NULL,
    slot_fin timestamp without time zone NOT NULL,
    estado_slot character varying(20) DEFAULT 'DISPONIBLE'::character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    usuario_creacion integer,
    fecha_modificacion timestamp without time zone,
    usuario_modificacion integer,
    CONSTRAINT chk_slots_agenda_estado CHECK (((estado_slot)::text = ANY ((ARRAY['DISPONIBLE'::character varying, 'RESERVADO'::character varying, 'BLOQUEADO'::character varying, 'OBSOLETO'::character varying])::text[]))),
    CONSTRAINT chk_slots_agenda_rango CHECK ((slot_fin > slot_inicio))
);

--
-- Name: TABLE slots_agenda; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.slots_agenda IS 'Turno concreto materializado a partir de agenda_horarios. La reserva de un slot usa SELECT...FOR UPDATE en CitaDao para evitar doble-booking por carrera. Un slot RESERVADO nunca lo toca el job de regeneración.';

--
-- Name: slots_agenda_id_slot_agenda_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.slots_agenda_id_slot_agenda_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: slots_agenda_id_slot_agenda_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.slots_agenda_id_slot_agenda_seq OWNED BY public.slots_agenda.id_slot_agenda;

--
-- Name: agenda_horarios id_agenda_horario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios ALTER COLUMN id_agenda_horario SET DEFAULT nextval('public.agenda_horarios_id_agenda_horario_seq'::regclass);

--
-- Name: citas id_cita; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas ALTER COLUMN id_cita SET DEFAULT nextval('public.citas_id_cita_seq'::regclass);

--
-- Name: citas_log_estados id_cita_log_estado; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas_log_estados ALTER COLUMN id_cita_log_estado SET DEFAULT nextval('public.citas_log_estados_id_cita_log_estado_seq'::regclass);

--
-- Name: lista_espera id_lista_espera; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lista_espera ALTER COLUMN id_lista_espera SET DEFAULT nextval('public.lista_espera_id_lista_espera_seq'::regclass);

--
-- Name: recordatorios id_recordatorio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recordatorios ALTER COLUMN id_recordatorio SET DEFAULT nextval('public.recordatorios_id_recordatorio_seq'::regclass);

--
-- Name: slots_agenda id_slot_agenda; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda ALTER COLUMN id_slot_agenda SET DEFAULT nextval('public.slots_agenda_id_slot_agenda_seq'::regclass);

--
-- Name: agenda_horarios agenda_horarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios
    ADD CONSTRAINT agenda_horarios_pkey PRIMARY KEY (id_agenda_horario);

--
-- Name: citas_log_estados citas_log_estados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas_log_estados
    ADD CONSTRAINT citas_log_estados_pkey PRIMARY KEY (id_cita_log_estado);

--
-- Name: citas citas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_pkey PRIMARY KEY (id_cita);

--
-- Name: lista_espera lista_espera_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lista_espera
    ADD CONSTRAINT lista_espera_pkey PRIMARY KEY (id_lista_espera);

--
-- Name: recordatorios recordatorios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recordatorios
    ADD CONSTRAINT recordatorios_pkey PRIMARY KEY (id_recordatorio);

--
-- Name: slots_agenda slots_agenda_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT slots_agenda_pkey PRIMARY KEY (id_slot_agenda);

--
-- Name: lista_espera uq_lista_espera_agenda_paciente; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lista_espera
    ADD CONSTRAINT uq_lista_espera_agenda_paciente UNIQUE (id_agenda_horario, id_paciente);

--
-- Name: recordatorios uq_recordatorios_cita_canal_minutos; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recordatorios
    ADD CONSTRAINT uq_recordatorios_cita_canal_minutos UNIQUE (id_cita, canal, minutos_antes);

--
-- Name: slots_agenda uq_slots_agenda_horario_inicio; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT uq_slots_agenda_horario_inicio UNIQUE (id_agenda_horario, slot_inicio);

--
-- Name: idx_agenda_horarios_consultorio_dia; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_agenda_horarios_consultorio_dia ON public.agenda_horarios USING btree (id_consultorio, id_dia_semana);

--
-- Name: idx_agenda_horarios_especialista; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_agenda_horarios_especialista ON public.agenda_horarios USING btree (id_especialista);

--
-- Name: idx_citas_especialista_inicio; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_citas_especialista_inicio ON public.citas USING btree (id_especialista, cita_inicio);

--
-- Name: idx_citas_estado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_citas_estado ON public.citas USING btree (id_estado_cita);

--
-- Name: idx_citas_log_estados_cita; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_citas_log_estados_cita ON public.citas_log_estados USING btree (id_cita);

--
-- Name: idx_citas_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_citas_paciente ON public.citas USING btree (id_paciente);

--
-- Name: idx_citas_slot; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_citas_slot ON public.citas USING btree (id_slot_agenda);

--
-- Name: idx_lista_espera_agenda; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_lista_espera_agenda ON public.lista_espera USING btree (id_agenda_horario);

--
-- Name: idx_lista_espera_paciente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_lista_espera_paciente ON public.lista_espera USING btree (id_paciente);

--
-- Name: idx_recordatorios_cita; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_recordatorios_cita ON public.recordatorios USING btree (id_cita);

--
-- Name: idx_slots_agenda_especialista_inicio; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_slots_agenda_especialista_inicio ON public.slots_agenda USING btree (id_especialista, slot_inicio);

--
-- Name: idx_slots_agenda_estado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_slots_agenda_estado ON public.slots_agenda USING btree (estado_slot);

--
-- Name: uq_citas_especialista_inicio; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_citas_especialista_inicio ON public.citas USING btree (id_especialista, cita_inicio) WHERE (id_slot_agenda IS NOT NULL);

--
-- Name: INDEX uq_citas_especialista_inicio; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.uq_citas_especialista_inicio IS 'Un especialista no puede tener dos citas a la misma hora. Solo cuenta las citas con turno (id_slot_agenda no nulo): una cita cancelada libera su turno y no impide reservarlo de nuevo (migración 110).';

--
-- Name: agenda_horarios trg_agenda_horarios_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_agenda_horarios_fecha_mod BEFORE UPDATE ON public.agenda_horarios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: citas trg_citas_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_citas_fecha_mod BEFORE UPDATE ON public.citas FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: lista_espera trg_lista_espera_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_lista_espera_fecha_mod BEFORE UPDATE ON public.lista_espera FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: recordatorios trg_recordatorios_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_recordatorios_fecha_mod BEFORE UPDATE ON public.recordatorios FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: slots_agenda trg_slots_agenda_fecha_mod; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_slots_agenda_fecha_mod BEFORE UPDATE ON public.slots_agenda FOR EACH ROW EXECUTE FUNCTION public.fn_set_fecha_modificacion();

--
-- Name: agenda_horarios agenda_horarios_id_consultorio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_consultorio_fkey FOREIGN KEY (id_consultorio) REFERENCES public.consultorios(id_consultorio) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: agenda_horarios agenda_horarios_id_dia_semana_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_dia_semana_fkey FOREIGN KEY (id_dia_semana) REFERENCES public.dias_semana(id_dia_semana) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: agenda_horarios agenda_horarios_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: agenda_horarios agenda_horarios_id_sede_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios
    ADD CONSTRAINT agenda_horarios_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES public.sedes(id_sede) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: agenda_horarios agenda_horarios_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios
    ADD CONSTRAINT agenda_horarios_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: agenda_horarios agenda_horarios_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agenda_horarios
    ADD CONSTRAINT agenda_horarios_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: citas citas_id_consultorio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_consultorio_fkey FOREIGN KEY (id_consultorio) REFERENCES public.consultorios(id_consultorio) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas citas_id_especialidad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES public.especialidades(id_especialidad) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas citas_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas citas_id_estado_cita_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_estado_cita_fkey FOREIGN KEY (id_estado_cita) REFERENCES public.estados_citas(id_estado_cita) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas citas_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas citas_id_sede_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES public.sedes(id_sede) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas citas_id_slot_agenda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_id_slot_agenda_fkey FOREIGN KEY (id_slot_agenda) REFERENCES public.slots_agenda(id_slot_agenda) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas_log_estados citas_log_estados_id_cita_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas_log_estados
    ADD CONSTRAINT citas_log_estados_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES public.citas(id_cita) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: CONSTRAINT citas_log_estados_id_cita_fkey ON citas_log_estados; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT citas_log_estados_id_cita_fkey ON public.citas_log_estados IS 'RESTRICT: historial de estados de la cita; borrar la cita no borra su historial (migración 107).';

--
-- Name: citas_log_estados citas_log_estados_id_estado_anterior_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas_log_estados
    ADD CONSTRAINT citas_log_estados_id_estado_anterior_fkey FOREIGN KEY (id_estado_anterior) REFERENCES public.estados_citas(id_estado_cita) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas_log_estados citas_log_estados_id_estado_nuevo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas_log_estados
    ADD CONSTRAINT citas_log_estados_id_estado_nuevo_fkey FOREIGN KEY (id_estado_nuevo) REFERENCES public.estados_citas(id_estado_cita) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: citas_log_estados citas_log_estados_usuario_cambio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas_log_estados
    ADD CONSTRAINT citas_log_estados_usuario_cambio_fkey FOREIGN KEY (usuario_cambio) REFERENCES public.usuarios(id_usuario);

--
-- Name: citas citas_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: citas citas_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: lista_espera lista_espera_id_agenda_horario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lista_espera
    ADD CONSTRAINT lista_espera_id_agenda_horario_fkey FOREIGN KEY (id_agenda_horario) REFERENCES public.agenda_horarios(id_agenda_horario) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: lista_espera lista_espera_id_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lista_espera
    ADD CONSTRAINT lista_espera_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.pacientes(id_paciente) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: lista_espera lista_espera_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lista_espera
    ADD CONSTRAINT lista_espera_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: lista_espera lista_espera_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lista_espera
    ADD CONSTRAINT lista_espera_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: recordatorios recordatorios_id_cita_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recordatorios
    ADD CONSTRAINT recordatorios_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES public.citas(id_cita) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: recordatorios recordatorios_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recordatorios
    ADD CONSTRAINT recordatorios_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: recordatorios recordatorios_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recordatorios
    ADD CONSTRAINT recordatorios_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: slots_agenda slots_agenda_id_agenda_horario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT slots_agenda_id_agenda_horario_fkey FOREIGN KEY (id_agenda_horario) REFERENCES public.agenda_horarios(id_agenda_horario) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: slots_agenda slots_agenda_id_consultorio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT slots_agenda_id_consultorio_fkey FOREIGN KEY (id_consultorio) REFERENCES public.consultorios(id_consultorio) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: slots_agenda slots_agenda_id_especialista_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT slots_agenda_id_especialista_fkey FOREIGN KEY (id_especialista) REFERENCES public.especialistas(id_especialista) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: slots_agenda slots_agenda_id_sede_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT slots_agenda_id_sede_fkey FOREIGN KEY (id_sede) REFERENCES public.sedes(id_sede) ON UPDATE CASCADE ON DELETE RESTRICT;

--
-- Name: slots_agenda slots_agenda_usuario_creacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT slots_agenda_usuario_creacion_fkey FOREIGN KEY (usuario_creacion) REFERENCES public.usuarios(id_usuario);

--
-- Name: slots_agenda slots_agenda_usuario_modificacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slots_agenda
    ADD CONSTRAINT slots_agenda_usuario_modificacion_fkey FOREIGN KEY (usuario_modificacion) REFERENCES public.usuarios(id_usuario);
