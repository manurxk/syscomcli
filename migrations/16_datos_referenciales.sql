-- 16_datos_referenciales.sql — Datos referenciales
-- Generado el 2026-10-25 desde sysclin_bd con docs/scripts/generar_esquema_base.py, con todos los
-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una
-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal
-- (manual del administrador, §3.2).
-- Catálogos y configuración del sistema (38 tablas): roles, modulos, acciones, generos, estados_civiles, paises, profesiones, niveles_instruccion, cargos, especialidades, dias_semana, estados_citas, signos, sintomas, diagnosticos, medicamentos, insumos, instrumentos, tipos_analisis, tipos_estudios, tipos_procedimientos, tipos_tratamientos, tipos_certificados_medicos, monedas, condiciones_venta, formas_cobro, tipos_comprobantes, tipos_impuestos, tipos_items, estados_factura, marcas_tarjeta, entidades_adheridas, entidades_emisoras, paginas, roles_permisos, departamentos, roles_paginas, ciudades.
-- No incluye personas, pacientes, funcionarios, usuarios, datos clínicos ni movimientos, ni los datos
-- propios de cada instalación (empresa, sedes, consultorios, cajas, timbrados, puntos de expedición,
-- depósitos, ítems de servicio): se cargan desde las pantallas del sistema.
-- usuario_creacion / usuario_modificacion van vacíos: en una base nueva todavía no hay usuarios.
-- La moneda USD (id 99) trae una tasa de cambio de prueba: corregirla desde el ABM de monedas.
-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/16_datos_referenciales.sql

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

COPY public.roles (id_rol, cod_rol, des_rol, est_rol, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	SUPERADMIN	Super Administrador	t	2026-06-20 21:58:39.936112	\N	\N	\N
2	ADMINISTRADOR	Administrador	t	2026-06-20 21:58:39.936112	\N	\N	\N
3	RECEPCION	Recepción	t	2026-06-20 21:58:39.936112	\N	\N	\N
4	CLINICO	Clínico	t	2026-06-20 21:58:39.936112	\N	\N	\N
5	VENTAS	Ventas	t	2026-06-20 21:58:39.936112	\N	\N	\N
\.

COPY public.modulos (id_modulo, des_modulo, est_modulo, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	MANTENIMIENTO	t	2026-06-20 21:58:39.616198	\N	\N	\N
2	AGENDAMIENTO	t	2026-06-20 21:58:39.616198	\N	\N	\N
3	CONSULTORIO	t	2026-06-20 21:58:39.616198	\N	\N	\N
4	VENTAS	t	2026-06-20 21:58:39.616198	\N	\N	\N
5	REPORTES	t	2026-06-20 21:58:39.616198	\N	\N	\N
\.

COPY public.acciones (id_accion, cod_accion, des_accion, est_accion, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	LEER	Leer / Consultar	t	2026-07-15 21:00:18.259995	\N	\N	\N
2	CREAR	Crear	t	2026-07-15 21:00:18.259995	\N	\N	\N
3	EDITAR	Editar	t	2026-07-15 21:00:18.259995	\N	\N	\N
4	ELIMINAR	Eliminar	t	2026-07-15 21:00:18.259995	\N	\N	\N
\.

COPY public.generos (id_genero, des_genero, est_genero, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	MASCULINO	t	2026-06-20 21:58:39.606775	\N	\N	\N
2	FEMENINO	t	2026-06-20 21:58:39.606775	\N	\N	\N
3	OTRO	t	2026-06-20 21:58:39.606775	\N	\N	\N
\.

COPY public.estados_civiles (id_estado_civil, des_estado_civil, est_estado_civil, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	SOLTERO	t	2026-06-20 21:58:39.608091	\N	\N	\N
2	CASADO	t	2026-06-20 21:58:39.608091	\N	\N	\N
3	DIVORCIADO	t	2026-06-20 21:58:39.608091	\N	\N	\N
4	VIUDO	t	2026-06-20 21:58:39.608091	\N	\N	\N
5	UNION LIBRE	t	2026-06-20 21:58:39.608091	\N	\N	\N
\.

COPY public.paises (id_pais, des_pais, cod_pais, est_pais, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	PARAGUAY	PRY	t	2026-06-20 21:58:39.610177	\N	\N	\N
\.

COPY public.profesiones (id_profesion, des_profesion, est_profesion, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
\.

COPY public.niveles_instruccion (id_nivel_instruccion, des_nivel_instruccion, est_nivel_instruccion, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	SIN INSTRUCCION	t	2026-06-20 21:58:39.608678	\N	\N	\N
2	PRIMARIA	t	2026-06-20 21:58:39.608678	\N	\N	\N
3	SECUNDARIA	t	2026-06-20 21:58:39.608678	\N	\N	\N
4	TECNICO	t	2026-06-20 21:58:39.608678	\N	\N	\N
5	UNIVERSITARIO	t	2026-06-20 21:58:39.608678	\N	\N	\N
6	POSTGRADO	t	2026-06-20 21:58:39.608678	\N	\N	\N
\.

COPY public.cargos (id_cargo, des_cargo, est_cargo, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion, es_clinico) FROM stdin;
11	RECEPCION	t	2026-06-23 17:57:29.586069	\N	2026-09-29 12:53:50.362636	\N	f
12	PSICOLOGO	t	2026-06-23 18:09:18.680754	\N	2026-10-17 23:54:06.964192	\N	t
14	CAJERO	t	2026-10-12 11:37:37.236936	\N	\N	\N	f
15	DIRECTOR CLINICO	t	2026-10-22 16:51:53.117701	\N	\N	\N	t
16	NEUROPSICOLOGO	t	2026-10-22 16:51:53.131964	\N	\N	\N	t
17	FONOAUDIOLOGO	t	2026-10-22 16:51:53.143466	\N	\N	\N	t
18	PSICOPEDAGOGO	t	2026-10-22 16:51:53.155008	\N	\N	\N	t
\.

COPY public.especialidades (id_especialidad, des_especialidad, est_especialidad, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
3	PSICOLOGÍA	t	2026-06-23 18:46:38.652453	\N	2026-10-17 23:40:44.214385	\N
4	PSIQUIATRIA INFANTIL	t	2026-06-24 00:05:02.557718	\N	2026-06-24 00:05:36.194525	\N
5	PSICOLOGIA CLINICA	t	2026-10-22 16:51:53.165605	\N	\N	\N
6	NEUROPSICOLOGIA	t	2026-10-22 16:51:53.175327	\N	\N	\N
7	FONOAUDIOLOGIA	t	2026-10-22 16:51:53.187479	\N	\N	\N
8	PSICOPEDAGOGIA	t	2026-10-22 16:51:53.197664	\N	\N	\N
\.

COPY public.dias_semana (id_dia_semana, nro_dia, des_dia, est_dia, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	1	Lunes	t	2026-06-24 11:44:22.281957	\N	\N	\N
2	2	Martes	t	2026-06-24 11:44:22.281957	\N	\N	\N
3	3	Miércoles	t	2026-06-24 11:44:22.281957	\N	\N	\N
4	4	Jueves	t	2026-06-24 11:44:22.281957	\N	\N	\N
5	5	Viernes	t	2026-06-24 11:44:22.281957	\N	\N	\N
6	6	Sábado	t	2026-06-24 11:44:22.281957	\N	\N	\N
7	7	Domingo	t	2026-06-24 11:44:22.281957	\N	\N	\N
\.

COPY public.estados_citas (id_estado_cita, cod_estado_cita, des_estado_cita, orden, es_final, est_estado_cita, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	AGENDADA	Agendada	1	f	t	2026-06-24 11:44:22.284794	\N	\N	\N
2	CONFIRMADA	Confirmada	2	f	t	2026-06-24 11:44:22.284794	\N	\N	\N
3	EN_CONSULTA	En consulta	3	f	t	2026-06-24 11:44:22.284794	\N	\N	\N
4	COMPLETADA	Completada	4	t	t	2026-06-24 11:44:22.284794	\N	\N	\N
5	AUSENTE	Ausente	5	t	t	2026-06-24 11:44:22.284794	\N	\N	\N
6	CANCELADA	Cancelada	6	t	t	2026-06-24 11:44:22.284794	\N	\N	\N
\.

COPY public.signos (id_signo, des_signo, est_signo, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
6	INQUIETUD PSICOMOTORA	t	2026-10-12 11:37:36.667558	\N	\N	\N
7	LLANTO FACIL	t	2026-10-12 11:37:36.703394	\N	\N	\N
8	CONTACTO VISUAL ESCASO	t	2026-10-12 11:37:36.740538	\N	\N	\N
9	DISCURSO ACELERADO	t	2026-10-12 11:37:36.780504	\N	\N	\N
\.

COPY public.sintomas (id_sintoma, des_sintoma, est_sintoma, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
5	PREOCUPACION EXCESIVA	t	2026-10-12 11:37:36.849135	\N	\N	\N
6	DIFICULTAD PARA DORMIR	t	2026-10-12 11:37:36.888082	\N	\N	\N
7	TRISTEZA PERSISTENTE	t	2026-10-12 11:37:36.925208	\N	\N	\N
8	DIFICULTAD DE CONCENTRACION	t	2026-10-12 11:37:36.96336	\N	\N	\N
9	IRRITABILIDAD	t	2026-10-12 11:37:37.003109	\N	\N	\N
\.

COPY public.diagnosticos (id_diagnostico, cod_cie10, des_diagnostico, est_diagnostico, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
3	F41.1	TRASTORNO DE ANSIEDAD GENERALIZADA	t	2026-10-12 11:37:36.394367	\N	\N	\N
4	F32.1	EPISODIO DEPRESIVO MODERADO	t	2026-10-12 11:37:36.43146	\N	\N	\N
5	F90.0	TRASTORNO DE ACTIVIDAD Y ATENCION	t	2026-10-12 11:37:36.469519	\N	\N	\N
6	F81.0	TRASTORNO ESPECIFICO DE LA LECTURA	t	2026-10-12 11:37:36.506474	\N	\N	\N
7	F43.2	TRASTORNO DE ADAPTACION	t	2026-10-12 11:37:36.549009	\N	\N	\N
8	F51.0	INSOMNIO NO ORGANICO	t	2026-10-12 11:37:36.599921	\N	\N	\N
\.

COPY public.medicamentos (id_medicamento, des_medicamento, est_medicamento, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
4	Ibuprofeno 400mg	f	2026-06-29 19:32:12.795481	\N	2026-10-13 19:19:51.014694	\N
5	METILFENIDATO 10 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
6	ATOMOXETINA 18 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
7	SERTRALINA 50 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
8	FLUOXETINA 20 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
9	ESCITALOPRAM 10 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
10	RISPERIDONA 1 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
11	ARIPIPRAZOL 5 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
12	MELATONINA 3 MG	t	2026-10-13 19:19:51.014694	\N	\N	\N
\.

COPY public.insumos (id_insumo, des_insumo, insumo_unidad_medida, stock_actual, stock_minimo, insumo_precio_unitario, est_insumo, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
\.

COPY public.instrumentos (id_instrumento, des_instrumento, est_instrumento, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
4	WISC V	t	2026-10-13 19:19:51.014694	\N	\N	\N
5	WAIS IV	t	2026-10-13 19:19:51.014694	\N	\N	\N
6	TEST GESTÁLTICO VISOMOTOR DE BENDER	t	2026-10-13 19:19:51.014694	\N	\N	\N
7	HTP CASA ÁRBOL PERSONA	t	2026-10-13 19:19:51.014694	\N	\N	\N
8	CBCL ACHENBACH	t	2026-10-13 19:19:51.014694	\N	\N	\N
9	CONNERS 3	t	2026-10-13 19:19:51.014694	\N	\N	\N
10	BDI II INVENTARIO DE DEPRESIÓN DE BECK	t	2026-10-13 19:19:51.014694	\N	\N	\N
11	ESCALA DE ANSIEDAD DE HAMILTON	t	2026-10-13 19:19:51.014694	\N	\N	\N
\.

COPY public.tipos_analisis (id_tipo_analisis, des_tipo_analisis, est_tipo_analisis, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
4	HEMOGRAMA COMPLETO	t	2026-06-29 19:32:12.795481	\N	2026-10-13 19:19:51.014694	\N
6	PERFIL TIROIDEO TSH Y T4 LIBRE	t	2026-10-13 19:19:51.014694	\N	\N	\N
7	LITEMIA	t	2026-10-13 19:19:51.014694	\N	\N	\N
8	DOSAJE DE ÁCIDO VALPROICO	t	2026-10-13 19:19:51.014694	\N	\N	\N
9	PERFIL HEPÁTICO	t	2026-10-13 19:19:51.014694	\N	\N	\N
10	GLUCEMIA	t	2026-10-13 19:19:51.014694	\N	\N	\N
11	PERFIL LIPÍDICO	t	2026-10-13 19:19:51.014694	\N	\N	\N
12	VITAMINA B12 Y ÁCIDO FÓLICO	t	2026-10-13 19:19:51.014694	\N	\N	\N
\.

COPY public.tipos_estudios (id_tipo_estudio, des_tipo_estudio, est_tipo_estudio, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
4	Radiografía de Tórax	f	2026-06-29 19:32:12.795481	\N	2026-10-13 19:19:51.014694	\N
5	EVALUACIÓN PSICODIAGNÓSTICA	t	2026-10-13 19:19:51.014694	\N	\N	\N
6	EVALUACIÓN NEUROPSICOLÓGICA	t	2026-10-13 19:19:51.014694	\N	\N	\N
7	EVALUACIÓN PSICOPEDAGÓGICA	t	2026-10-13 19:19:51.014694	\N	\N	\N
8	EVALUACIÓN FONOAUDIOLÓGICA	t	2026-10-13 19:19:51.014694	\N	\N	\N
9	ELECTROENCEFALOGRAMA	t	2026-10-13 19:19:51.014694	\N	\N	\N
10	RESONANCIA MAGNÉTICA DE CEREBRO	t	2026-10-13 19:19:51.014694	\N	\N	\N
11	AUDIOMETRÍA	t	2026-10-13 19:19:51.014694	\N	\N	\N
\.

COPY public.tipos_procedimientos (id_tipo_procedimiento, des_tipo_procedimiento, est_tipo_procedimiento, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
5	ENTREVISTA CLINICA	t	2026-10-12 11:37:37.076604	\N	\N	\N
6	APLICACION DE TEST PSICOMETRICO	t	2026-10-12 11:37:37.120571	\N	\N	\N
7	PSICOEDUCACION	t	2026-10-12 11:37:37.162104	\N	\N	\N
\.

COPY public.tipos_tratamientos (id_tipo_tratamiento, des_tipo_tratamiento, est_tipo_tratamiento, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
5	PSICOTERAPIA INDIVIDUAL	t	2026-10-13 19:19:51.014694	\N	\N	\N
6	TERAPIA COGNITIVO CONDUCTUAL	t	2026-10-13 19:19:51.014694	\N	\N	\N
7	TERAPIA FAMILIAR	t	2026-10-13 19:19:51.014694	\N	\N	\N
8	TERAPIA DE JUEGO	t	2026-10-13 19:19:51.014694	\N	\N	\N
9	PSICOPEDAGOGÍA	t	2026-10-13 19:19:51.014694	\N	\N	\N
10	ENTRENAMIENTO A PADRES	t	2026-10-13 19:19:51.014694	\N	\N	\N
\.

COPY public.tipos_certificados_medicos (id_tipo_certificado_medico, des_tipo_certificado_medico, est_tipo_certificado_medico, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	Certificado de Aptitud	t	2026-06-28 18:28:37.036441	\N	\N	\N
2	Certificado de Reposo	t	2026-06-28 18:28:37.036441	\N	\N	\N
3	Certificado de Tratamiento	t	2026-06-28 18:28:37.036441	\N	\N	\N
4	Certificado de Asistencia	t	2026-06-28 18:28:37.036441	\N	\N	\N
5	Certificado de Evaluación	t	2026-06-28 18:28:37.036441	\N	\N	\N
6	Justificativo Médico	t	2026-06-28 18:28:37.036441	\N	\N	\N
\.

COPY public.monedas (id_moneda, des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, es_moneda_local, tasa_cambio, est_moneda, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	GUARANI PARAGUAYO	PYG	Gs.	0	t	1.000000	t	2026-06-30 19:53:52.425054	\N	2026-09-21 11:21:27.798832	\N
99	DOLAR AMERICANO	USD	US$	2	f	7300.000000	t	2026-09-22 10:54:30.315525	\N	\N	\N
\.

COPY public.condiciones_venta (id_condicion_venta, des_condicion_venta, cod_condicion_venta, dias_credito, permite_cuotas, numero_cuotas_max, est_condicion_venta, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	CONTADO	CON	0	f	1	t	2026-07-01 09:25:40.524686	\N	\N	\N
2	CREDITO	CRE	30	f	1	t	2026-07-01 09:25:40.524686	\N	\N	\N
\.

COPY public.formas_cobro (id_forma_cobro, des_forma_cobro, cod_forma_cobro, requiere_entidad, permite_cuotas, est_forma_cobro, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	EFECTIVO	EFECTIVO	f	f	t	2026-06-30 19:46:40.856763	\N	\N	\N
2	CHEQUE	CHEQUE	f	f	f	2026-06-30 19:46:40.856763	\N	2026-09-08 22:22:53.674431	\N
3	TARJETA CREDITO	TARJETA_CREDITO	t	t	t	2026-06-30 19:46:40.856763	\N	2026-06-30 20:06:39.380247	\N
4	TARJETA DÉBITO	TARJETA_DEBITO	t	f	t	2026-06-30 19:46:40.856763	\N	\N	\N
5	TRANSFERENCIA	TRANSFERENCIA	f	f	t	2026-06-30 19:46:40.856763	\N	\N	\N
\.

COPY public.tipos_comprobantes (id_tipo_comprobante, des_tipo_comprobante, cod_tipo_comprobante, codigo_sifen, requiere_timbrado, tipo_documento, est_tipo_comprobante, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
2	FACTURA	FAC	\N	t	\N	t	2026-07-01 09:25:40.524686	\N	\N	\N
\.

COPY public.tipos_impuestos (id_tipo_impuesto, des_tipo_impuesto, cod_tipo_impuesto, porcentaje_impuesto, tipo_calculo, est_tipo_impuesto, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
4	IVA 10%	IVA10	10.00	PORCENTAJE	t	2026-07-01 09:25:40.524686	\N	\N	\N
5	IVA 5%	IVA5	5.00	PORCENTAJE	t	2026-07-01 09:25:40.524686	\N	\N	\N
6	Exento	EXE	0.00	PORCENTAJE	t	2026-07-01 09:25:40.524686	\N	\N	\N
\.

COPY public.tipos_items (id_tipo_item, des_tipo_item, cod_tipo_item, tipo_item_categoria, requiere_stock, est_tipo_item, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	SERVICIO MEDICO	SERV_MED	\N	f	t	2026-06-30 23:03:15.231797	\N	\N	\N
2	MEDICAMENTO	MEDIC	\N	f	t	2026-06-30 23:03:15.231797	\N	\N	\N
3	INSUMO	INSUMO	\N	f	t	2026-06-30 23:03:15.231797	\N	\N	\N
\.

COPY public.estados_factura (id_estado_factura, des_estado_factura, cod_estado_factura, permite_modificacion, permite_anulacion, color_estado, est_estado_factura, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	EMITIDA	EMIT	t	t	secondary	t	2026-07-01 09:25:40.524686	\N	\N	\N
2	ANULADA	ANUL	t	f	secondary	t	2026-07-01 09:25:40.524686	\N	\N	\N
\.

COPY public.marcas_tarjeta (id_marca_tarjeta, des_marca_tarjeta, cod_marca_tarjeta, est_marca_tarjeta, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	Visa	VISA	t	2026-10-24 09:03:47.251964	\N	\N	\N
2	Mastercard	MC	t	2026-10-24 09:03:47.251964	\N	\N	\N
3	Cabal	CABAL	t	2026-10-24 09:03:47.251964	\N	\N	\N
4	Panal	PANAL	t	2026-10-24 09:03:47.251964	\N	\N	\N
5	Credicard	CREDI	t	2026-10-24 09:03:47.251964	\N	\N	\N
6	American Express	AMEX	t	2026-10-24 09:03:47.251964	\N	\N	\N
\.

COPY public.entidades_adheridas (id_entidad_adherida, des_entidad_adherida, cod_entidad_adherida, ruc_entidad, telefono_entidad, email_entidad, est_entidad_adherida, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	Bancard	BANCARD	\N	\N	\N	t	2026-10-24 09:03:47.251964	\N	\N	\N
2	Cabal	CABAL	\N	\N	\N	t	2026-10-24 09:03:47.251964	\N	\N	\N
3	Panal	PANAL	\N	\N	\N	t	2026-10-24 09:03:47.251964	\N	\N	\N
4	Credicard	CREDI	\N	\N	\N	t	2026-10-24 09:03:47.251964	\N	\N	\N
5	Procard	PROCARD	\N	\N	\N	t	2026-10-24 09:03:47.251964	\N	\N	\N
\.

COPY public.entidades_emisoras (id_entidad_emisora, des_entidad_emisora, cod_entidad_emisora, ruc_entidad, telefono_entidad, email_entidad, tipo_entidad, est_entidad_emisora, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	Banco Nacional de Fomento (BNF)	BNF	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
2	Banco Itaú Paraguay	ITAU	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
3	Banco Continental	CONT	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
4	Banco Familiar	FAMI	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
5	Visión Banco	VISI	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
6	Banco BASA	BASA	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
7	Banco GNB Paraguay	GNB	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
8	Sudameris Bank	SUDA	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
9	Banco Atlas	ATLA	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
10	Banco Río	RIO	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
11	Ueno Bank	UENO	\N	\N	\N	BANCO	t	2026-10-24 09:00:09.155604	\N	\N	\N
\.

COPY public.paginas (id_pagina, id_modulo, des_pagina, pag_direccion, est_pagina, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion, icono, orden, grupo_menu, descripcion) FROM stdin;
1	1	Funcionarios	funcionario.funcionarioIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	briefcase	10	Personas	Personal de la clínica y sus datos
2	1	Pacientes	paciente.pacienteIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	users	20	Personas	Registro de pacientes y sus datos personales
3	1	Usuarios	usuario.usuarioIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	user-check	30	Personas	Usuarios que ingresan al sistema y sus roles
4	2	Agenda Medica	agenda_horarios.agendaHorariosIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	calendar	10	Agendamiento	Horarios de atención de cada especialista y turnos disponibles
5	2	Citas	cita.citaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	clipboard	20	Agendamiento	Agendar, confirmar, reprogramar y cancelar citas
6	2	Lista de Espera	lista_espera.listaEsperaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	clock	30	Agendamiento	Pacientes esperando un turno disponible
7	3	Mi Agenda	mi_agenda.miAgendaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	calendar	10	Clinico	Sus citas del día y de la semana (solo lectura)
8	3	Consultas	consulta.consultaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	file-text	20	Clinico	Atención del paciente: anamnesis, registro clínico, órdenes, recetas y certificados
9	3	PEI	pei.peiIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	book-open	30	Clinico	Plan de intervención de cada paciente
10	3	Fichas Medicas	ficha.fichaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	clipboard	40	Clinico	Ficha médica imprimible del paciente
11	4	Pedidos	pedido.pedidoIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	shopping-cart	10	Ventas	Pedidos de servicios solicitados por el paciente
12	4	Presupuestos	presupuesto.presupuestoIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	file-text	20	Ventas	Presupuestos de servicios antes de facturar
13	4	Estado de Caja	apertura_cierre_caja.cajaEstado	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	unlock	30	Ventas	Abrir y cerrar la caja del día
14	4	Historial de Caja	apertura_cierre_caja.cajaHistorial	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	clock	40	Ventas	Aperturas y cierres de caja anteriores
15	4	Arqueos de Caja	arqueo_caja.arqueoIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	check-square	50	Ventas	Conteo de efectivo y diferencias de la caja
16	4	Facturas	factura.facturaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	file-text	60	Ventas	Emitir, imprimir y anular facturas
17	4	Remisiones	remision.remisionIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	truck	70	Ventas	Remisiones de entrega de servicios o insumos
18	4	Notas de Credito	nota_credito.notaCreditoIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	minus-circle	80	Ventas	Notas de crédito sobre facturas emitidas
19	4	Notas de Debito	nota_debito.notaDebitoIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	plus-circle	90	Ventas	Notas de débito sobre facturas emitidas
20	4	Cuentas a Cobrar	cuenta_cobrar.cuentaCobrarIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	credit-card	100	Ventas	Saldos pendientes de cobro de las facturas a crédito
21	4	Cobranzas	cobranza.cobranzaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	dollar-sign	110	Ventas	Registrar los cobros de facturas y cuotas
22	4	Recaudaciones	recaudacion.recaudacionIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	archive	120	Ventas	Resumen de lo recaudado por forma de pago
23	4	Libro de Ventas	libro_ventas.libroVentasIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	book	130	Ventas	Libro de ventas del período para la declaración de impuestos
24	1	Referenciales	referenciales.referencialesIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	sliders	10	Configuracion	Catálogos del sistema: países, ciudades, monedas, impuestos y otros
25	4	Timbrados	timbrado.timbradoIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	award	20	Configuracion	Timbrados fiscales y su numeración vigente
26	4	Puntos de Expedicion	punto_expedicion.puntoExpedicionIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	map-pin	30	Configuracion	Sucursales y puntos de expedición de documentos
27	1	Roles y Permisos	permisos.permisosIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	shield	40	Configuracion	Qué acciones puede realizar cada rol en cada módulo
28	1	Auditoria	auditoria.auditoriaIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	eye	50	Configuracion	Registro de quién hizo qué en el sistema
29	1	Menu	menu.menuIndex	t	2026-07-22 11:06:11.239235	\N	2026-10-20 09:05:03.784468	\N	list	60	Configuracion	Qué páginas ve cada rol en el menú lateral
30	1	Accesos	acceso.accesoIndex	f	2026-07-22 11:06:11.239235	\N	2026-10-19 09:36:15.167869	\N	key	70	Configuracion	\N
31	5	Reportes	reporte.reporteIndex	t	2026-08-12 16:37:36.952627	\N	2026-10-20 09:05:03.784468	\N	bar-chart-2	10	Reportes	Reportes de gestión, clínicos y de ventas según su rol
\.

COPY public.roles_permisos (id_rol_permiso, id_rol, id_modulo, id_accion, permitido, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	1	1	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
2	2	1	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
3	1	1	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
4	2	1	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
5	3	1	3	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
6	1	1	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
7	2	1	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
8	3	1	2	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
9	1	1	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
10	2	1	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
11	3	1	1	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
12	5	1	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
13	1	2	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
14	2	2	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
15	3	2	4	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
16	1	2	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
17	2	2	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
18	3	2	3	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
19	1	2	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
20	2	2	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
21	3	2	2	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
22	1	2	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
23	2	2	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
24	3	2	1	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
25	4	2	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
26	1	3	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
27	2	3	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
28	4	3	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
29	1	3	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
30	2	3	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
31	4	3	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
32	1	3	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
33	2	3	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
34	3	3	2	t	2026-07-15 21:26:56.740719	\N	2026-09-08 22:29:18.775788	\N
35	4	3	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
36	1	3	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
37	2	3	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
38	4	3	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
39	1	4	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
40	2	4	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
41	5	4	4	t	2026-07-15 21:26:56.740719	\N	\N	\N
42	1	4	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
43	2	4	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
44	5	4	3	t	2026-07-15 21:26:56.740719	\N	\N	\N
45	1	4	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
46	2	4	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
47	5	4	2	t	2026-07-15 21:26:56.740719	\N	\N	\N
48	1	4	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
49	2	4	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
50	5	4	1	t	2026-07-15 21:26:56.740719	\N	\N	\N
54	3	1	4	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
59	3	3	1	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
61	3	3	3	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
62	3	3	4	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
63	3	4	1	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
64	3	4	2	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
65	3	4	3	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
66	3	4	4	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
67	3	5	1	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
68	3	5	2	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
69	3	5	3	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
70	3	5	4	f	2026-09-08 22:29:12.165041	\N	2026-09-08 22:29:18.775788	\N
\.

COPY public.departamentos (id_departamento, id_pais, des_departamento, est_departamento, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	1	ASUNCION	t	2026-06-20 21:58:39.611127	\N	\N	\N
2	1	CONCEPCION	t	2026-06-20 21:58:39.611127	\N	\N	\N
3	1	SAN PEDRO	t	2026-06-20 21:58:39.611127	\N	\N	\N
4	1	CORDILLERA	t	2026-06-20 21:58:39.611127	\N	\N	\N
5	1	GUAIRA	t	2026-06-20 21:58:39.611127	\N	\N	\N
6	1	CAAGUAZU	t	2026-06-20 21:58:39.611127	\N	\N	\N
7	1	CAAZAPA	t	2026-06-20 21:58:39.611127	\N	\N	\N
8	1	ITAPUA	t	2026-06-20 21:58:39.611127	\N	\N	\N
9	1	MISIONES	t	2026-06-20 21:58:39.611127	\N	\N	\N
10	1	PARAGUARI	t	2026-06-20 21:58:39.611127	\N	\N	\N
11	1	ALTO PARANA	t	2026-06-20 21:58:39.611127	\N	\N	\N
12	1	CENTRAL	t	2026-06-20 21:58:39.611127	\N	\N	\N
13	1	ÑEEMBUCU	t	2026-06-20 21:58:39.611127	\N	\N	\N
14	1	AMAMBAY	t	2026-06-20 21:58:39.611127	\N	\N	\N
15	1	CANINDEYU	t	2026-06-20 21:58:39.611127	\N	\N	\N
16	1	PRESIDENTE HAYES	t	2026-06-20 21:58:39.611127	\N	\N	\N
17	1	BOQUERON	t	2026-06-20 21:58:39.611127	\N	\N	\N
18	1	ALTO PARAGUAY	t	2026-06-20 21:58:39.611127	\N	\N	\N
\.

COPY public.roles_paginas (id_rol_pagina, id_rol, id_pagina, visible, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	1	1	t	2026-07-22 11:06:11.245656	\N	\N	\N
2	2	1	t	2026-07-22 11:06:11.245656	\N	\N	\N
3	1	2	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
4	2	2	t	2026-07-22 11:06:11.245656	\N	\N	\N
5	3	2	t	2026-07-22 11:06:11.245656	\N	\N	\N
6	1	3	t	2026-07-22 11:06:11.245656	\N	\N	\N
7	2	3	t	2026-07-22 11:06:11.245656	\N	\N	\N
8	1	4	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
9	2	4	t	2026-07-22 11:06:11.245656	\N	\N	\N
10	1	5	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
11	2	5	t	2026-07-22 11:06:11.245656	\N	\N	\N
12	3	5	t	2026-07-22 11:06:11.245656	\N	\N	\N
13	1	6	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
14	2	6	t	2026-07-22 11:06:11.245656	\N	\N	\N
15	3	6	t	2026-07-22 11:06:11.245656	\N	\N	\N
16	1	7	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
17	2	7	t	2026-07-22 11:06:11.245656	\N	\N	\N
18	4	7	t	2026-07-22 11:06:11.245656	\N	\N	\N
19	1	8	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
20	2	8	t	2026-07-22 11:06:11.245656	\N	\N	\N
21	4	8	t	2026-07-22 11:06:11.245656	\N	\N	\N
22	1	9	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
23	2	9	t	2026-07-22 11:06:11.245656	\N	\N	\N
24	4	9	t	2026-07-22 11:06:11.245656	\N	\N	\N
25	1	10	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
26	2	10	t	2026-07-22 11:06:11.245656	\N	\N	\N
27	4	10	t	2026-07-22 11:06:11.245656	\N	\N	\N
28	1	11	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
29	2	11	t	2026-07-22 11:06:11.245656	\N	\N	\N
30	5	11	t	2026-07-22 11:06:11.245656	\N	\N	\N
31	1	12	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
32	2	12	t	2026-07-22 11:06:11.245656	\N	\N	\N
33	5	12	t	2026-07-22 11:06:11.245656	\N	\N	\N
34	1	13	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
35	2	13	t	2026-07-22 11:06:11.245656	\N	\N	\N
36	5	13	t	2026-07-22 11:06:11.245656	\N	\N	\N
37	1	14	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
38	2	14	t	2026-07-22 11:06:11.245656	\N	\N	\N
39	5	14	t	2026-07-22 11:06:11.245656	\N	\N	\N
40	1	15	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
41	2	15	t	2026-07-22 11:06:11.245656	\N	\N	\N
42	5	15	t	2026-07-22 11:06:11.245656	\N	\N	\N
43	1	16	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
44	2	16	t	2026-07-22 11:06:11.245656	\N	\N	\N
45	5	16	t	2026-07-22 11:06:11.245656	\N	\N	\N
46	1	17	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
47	2	17	t	2026-07-22 11:06:11.245656	\N	\N	\N
48	5	17	t	2026-07-22 11:06:11.245656	\N	\N	\N
49	1	18	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
50	2	18	t	2026-07-22 11:06:11.245656	\N	\N	\N
51	5	18	t	2026-07-22 11:06:11.245656	\N	\N	\N
52	1	19	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
53	2	19	t	2026-07-22 11:06:11.245656	\N	\N	\N
54	5	19	t	2026-07-22 11:06:11.245656	\N	\N	\N
55	1	20	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
56	2	20	t	2026-07-22 11:06:11.245656	\N	\N	\N
57	5	20	t	2026-07-22 11:06:11.245656	\N	\N	\N
58	1	21	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
59	2	21	t	2026-07-22 11:06:11.245656	\N	\N	\N
60	5	21	t	2026-07-22 11:06:11.245656	\N	\N	\N
61	1	22	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
62	2	22	t	2026-07-22 11:06:11.245656	\N	\N	\N
63	5	22	t	2026-07-22 11:06:11.245656	\N	\N	\N
64	1	23	f	2026-07-22 11:06:11.245656	\N	2026-10-23 09:29:53.504441	\N
65	2	23	t	2026-07-22 11:06:11.245656	\N	\N	\N
66	5	23	t	2026-07-22 11:06:11.245656	\N	\N	\N
67	1	24	t	2026-07-22 11:06:11.245656	\N	\N	\N
68	2	24	t	2026-07-22 11:06:11.245656	\N	\N	\N
69	1	25	t	2026-07-22 11:06:11.245656	\N	\N	\N
70	2	25	t	2026-07-22 11:06:11.245656	\N	\N	\N
71	5	25	f	2026-07-22 11:06:11.245656	\N	2026-10-13 18:20:33.214414	\N
72	1	26	t	2026-07-22 11:06:11.245656	\N	\N	\N
73	2	26	t	2026-07-22 11:06:11.245656	\N	\N	\N
74	5	26	f	2026-07-22 11:06:11.245656	\N	2026-10-13 18:20:33.214414	\N
75	1	27	t	2026-07-22 11:06:11.245656	\N	\N	\N
76	2	27	t	2026-07-22 11:06:11.245656	\N	\N	\N
77	1	28	t	2026-07-22 11:06:11.245656	\N	\N	\N
78	2	28	t	2026-07-22 11:06:11.245656	\N	\N	\N
79	1	29	t	2026-07-22 11:06:11.245656	\N	\N	\N
80	2	29	t	2026-07-22 11:06:11.245656	\N	\N	\N
81	1	30	t	2026-07-22 11:06:11.245656	\N	\N	\N
82	2	30	t	2026-07-22 11:06:11.245656	\N	\N	\N
83	4	24	f	2026-07-22 11:19:40.186591	\N	2026-07-22 11:19:55.940008	\N
85	1	31	t	2026-08-12 16:37:36.958498	\N	\N	\N
89	2	31	t	2026-08-12 16:37:36.958498	\N	\N	\N
96	3	4	t	2026-09-29 13:15:48.500746	\N	\N	\N
97	4	4	t	2026-10-13 19:23:39.470492	\N	\N	\N
98	3	28	t	2026-10-19 09:36:15.167869	\N	\N	\N
99	4	28	t	2026-10-19 09:36:15.167869	\N	\N	\N
100	5	28	t	2026-10-19 09:36:15.167869	\N	\N	\N
101	3	31	t	2026-10-19 17:37:07.970538	\N	\N	\N
102	4	31	t	2026-10-19 17:37:07.970538	\N	\N	\N
103	5	31	t	2026-10-19 17:37:07.970538	\N	\N	\N
\.

COPY public.ciudades (id_ciudad, id_departamento, des_ciudad, est_ciudad, fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion) FROM stdin;
1	1	ASUNCION	t	2026-06-20 21:58:39.613704	\N	\N	\N
2	12	AREGUA	t	2026-06-20 21:58:39.615418	\N	\N	\N
3	12	CAPIATA	t	2026-06-20 21:58:39.615418	\N	\N	\N
4	12	FERNANDO DE LA MORA	t	2026-06-20 21:58:39.615418	\N	\N	\N
5	12	ITAUGUA	t	2026-06-20 21:58:39.615418	\N	\N	\N
6	12	LAMBARE	t	2026-06-20 21:58:39.615418	\N	\N	\N
7	12	LIMPIO	t	2026-06-20 21:58:39.615418	\N	\N	\N
8	12	LUQUE	t	2026-06-20 21:58:39.615418	\N	\N	\N
9	12	MARIANO ROQUE ALONSO	t	2026-06-20 21:58:39.615418	\N	\N	\N
11	12	SAN ANTONIO	t	2026-06-20 21:58:39.615418	\N	\N	\N
12	12	SAN LORENZO	t	2026-06-20 21:58:39.615418	\N	\N	\N
13	12	VILLA ELISA	t	2026-06-20 21:58:39.615418	\N	\N	\N
14	12	YPACARAI	t	2026-06-20 21:58:39.615418	\N	\N	\N
15	12	ÑEMBY	t	2026-06-20 21:58:39.615418	\N	\N	\N
18	2	CONCEPCION	t	2026-10-22 16:37:18.110939	\N	\N	\N
19	2	BELEN	t	2026-10-22 16:37:18.110939	\N	\N	\N
20	2	HORQUETA	t	2026-10-22 16:37:18.110939	\N	\N	\N
21	2	LORETO	t	2026-10-22 16:37:18.110939	\N	\N	\N
22	2	SAN CARLOS DEL APA	t	2026-10-22 16:37:18.110939	\N	\N	\N
23	2	SAN LAZARO	t	2026-10-22 16:37:18.110939	\N	\N	\N
24	2	YBY YAU	t	2026-10-22 16:37:18.110939	\N	\N	\N
25	2	AZOTEY	t	2026-10-22 16:37:18.110939	\N	\N	\N
26	2	SARGENTO JOSE FELIX LOPEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
27	2	SAN ALFREDO	t	2026-10-22 16:37:18.110939	\N	\N	\N
28	2	PASO BARRETO	t	2026-10-22 16:37:18.110939	\N	\N	\N
29	2	ARROYITO	t	2026-10-22 16:37:18.110939	\N	\N	\N
30	2	PASO HORQUETA	t	2026-10-22 16:37:18.110939	\N	\N	\N
31	3	SAN PEDRO DEL YCUAMANDYYU	t	2026-10-22 16:37:18.110939	\N	\N	\N
32	3	ANTEQUERA	t	2026-10-22 16:37:18.110939	\N	\N	\N
33	3	CHORE	t	2026-10-22 16:37:18.110939	\N	\N	\N
34	3	GENERAL ELIZARDO AQUINO	t	2026-10-22 16:37:18.110939	\N	\N	\N
35	3	ITACURUBI DEL ROSARIO	t	2026-10-22 16:37:18.110939	\N	\N	\N
36	3	LIMA	t	2026-10-22 16:37:18.110939	\N	\N	\N
37	3	NUEVA GERMANIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
38	3	SAN ESTANISLAO	t	2026-10-22 16:37:18.110939	\N	\N	\N
39	3	SAN PABLO	t	2026-10-22 16:37:18.110939	\N	\N	\N
40	3	TACUATI	t	2026-10-22 16:37:18.110939	\N	\N	\N
41	3	UNION	t	2026-10-22 16:37:18.110939	\N	\N	\N
42	3	25 DE DICIEMBRE	t	2026-10-22 16:37:18.110939	\N	\N	\N
43	3	VILLA DEL ROSARIO	t	2026-10-22 16:37:18.110939	\N	\N	\N
44	3	GENERAL FRANCISCO ISIDORO RESQUIN	t	2026-10-22 16:37:18.110939	\N	\N	\N
45	3	YATAITY DEL NORTE	t	2026-10-22 16:37:18.110939	\N	\N	\N
46	3	GUAJAYVI	t	2026-10-22 16:37:18.110939	\N	\N	\N
47	3	CAPIIBARY	t	2026-10-22 16:37:18.110939	\N	\N	\N
48	3	SANTA ROSA DEL AGUARAY	t	2026-10-22 16:37:18.110939	\N	\N	\N
49	3	YRYBUCUA	t	2026-10-22 16:37:18.110939	\N	\N	\N
50	3	LIBERACION	t	2026-10-22 16:37:18.110939	\N	\N	\N
51	3	SAN VICENTE PANCHOLO	t	2026-10-22 16:37:18.110939	\N	\N	\N
52	3	SAN JOSE DEL ROSARIO	t	2026-10-22 16:37:18.110939	\N	\N	\N
53	4	CAACUPE	t	2026-10-22 16:37:18.110939	\N	\N	\N
54	4	ALTOS	t	2026-10-22 16:37:18.110939	\N	\N	\N
55	4	ARROYOS Y ESTEROS	t	2026-10-22 16:37:18.110939	\N	\N	\N
56	4	ATYRA	t	2026-10-22 16:37:18.110939	\N	\N	\N
57	4	CARAGUATAY	t	2026-10-22 16:37:18.110939	\N	\N	\N
58	4	EMBOSCADA	t	2026-10-22 16:37:18.110939	\N	\N	\N
59	4	EUSEBIO AYALA	t	2026-10-22 16:37:18.110939	\N	\N	\N
60	4	ISLA PUCU	t	2026-10-22 16:37:18.110939	\N	\N	\N
61	4	ITACURUBI DE LA CORDILLERA	t	2026-10-22 16:37:18.110939	\N	\N	\N
62	4	JUAN DE MENA	t	2026-10-22 16:37:18.110939	\N	\N	\N
63	4	LOMA GRANDE	t	2026-10-22 16:37:18.110939	\N	\N	\N
64	4	MBOCAYATY DEL YHAGUY	t	2026-10-22 16:37:18.110939	\N	\N	\N
65	4	NUEVA COLOMBIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
66	4	PIRIBEBUY	t	2026-10-22 16:37:18.110939	\N	\N	\N
67	4	PRIMERO DE MARZO	t	2026-10-22 16:37:18.110939	\N	\N	\N
68	4	SAN BERNARDINO	t	2026-10-22 16:37:18.110939	\N	\N	\N
69	4	SANTA ELENA	t	2026-10-22 16:37:18.110939	\N	\N	\N
70	4	TOBATI	t	2026-10-22 16:37:18.110939	\N	\N	\N
71	4	VALENZUELA	t	2026-10-22 16:37:18.110939	\N	\N	\N
72	4	SAN JOSE OBRERO	t	2026-10-22 16:37:18.110939	\N	\N	\N
73	5	VILLARRICA	t	2026-10-22 16:37:18.110939	\N	\N	\N
74	5	BORJA	t	2026-10-22 16:37:18.110939	\N	\N	\N
75	5	CAPITAN MAURICIO JOSE TROCHE	t	2026-10-22 16:37:18.110939	\N	\N	\N
76	5	CORONEL MARTINEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
77	5	FELIX PEREZ CARDOZO	t	2026-10-22 16:37:18.110939	\N	\N	\N
78	5	GRAL EUGENIO A GARAY	t	2026-10-22 16:37:18.110939	\N	\N	\N
79	5	INDEPENDENCIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
80	5	ITAPE	t	2026-10-22 16:37:18.110939	\N	\N	\N
81	5	ITURBE	t	2026-10-22 16:37:18.110939	\N	\N	\N
82	5	JOSE FASSARDI	t	2026-10-22 16:37:18.110939	\N	\N	\N
83	5	MBOCAYATY	t	2026-10-22 16:37:18.110939	\N	\N	\N
84	5	NATALICIO TALAVERA	t	2026-10-22 16:37:18.110939	\N	\N	\N
85	5	ÑUMI	t	2026-10-22 16:37:18.110939	\N	\N	\N
86	5	SAN SALVADOR	t	2026-10-22 16:37:18.110939	\N	\N	\N
87	5	YATAITY	t	2026-10-22 16:37:18.110939	\N	\N	\N
88	5	TEBICUARY	t	2026-10-22 16:37:18.110939	\N	\N	\N
89	6	CORONEL OVIEDO	t	2026-10-22 16:37:18.110939	\N	\N	\N
90	6	CAAGUAZU	t	2026-10-22 16:37:18.110939	\N	\N	\N
91	6	CARAYAO	t	2026-10-22 16:37:18.110939	\N	\N	\N
92	6	DR CECILIO BAEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
93	6	SANTA ROSA DEL MBUTUY	t	2026-10-22 16:37:18.110939	\N	\N	\N
94	6	DR JUAN MANUEL FRUTOS	t	2026-10-22 16:37:18.110939	\N	\N	\N
95	6	REPATRIACION	t	2026-10-22 16:37:18.110939	\N	\N	\N
96	6	NUEVA LONDRES	t	2026-10-22 16:37:18.110939	\N	\N	\N
97	6	SAN JOAQUIN	t	2026-10-22 16:37:18.110939	\N	\N	\N
98	6	SAN JOSE DE LOS ARROYOS	t	2026-10-22 16:37:18.110939	\N	\N	\N
99	6	YHU	t	2026-10-22 16:37:18.110939	\N	\N	\N
100	6	DR J EULOGIO ESTIGARRIBIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
101	6	RI 3 CORRALES	t	2026-10-22 16:37:18.110939	\N	\N	\N
102	6	RAUL ARSENIO OVIEDO	t	2026-10-22 16:37:18.110939	\N	\N	\N
103	6	JOSE DOMINGO OCAMPOS	t	2026-10-22 16:37:18.110939	\N	\N	\N
104	6	MARISCAL FRANCISCO SOLANO LOPEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
105	6	LA PASTORA	t	2026-10-22 16:37:18.110939	\N	\N	\N
106	6	3 DE FEBRERO	t	2026-10-22 16:37:18.110939	\N	\N	\N
107	6	SIMON BOLIVAR	t	2026-10-22 16:37:18.110939	\N	\N	\N
108	6	VAQUERIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
109	6	TEMBIAPORA	t	2026-10-22 16:37:18.110939	\N	\N	\N
110	6	NUEVA TOLEDO	t	2026-10-22 16:37:18.110939	\N	\N	\N
111	7	CAAZAPA	t	2026-10-22 16:37:18.110939	\N	\N	\N
112	7	ABAI	t	2026-10-22 16:37:18.110939	\N	\N	\N
113	7	BUENA VISTA	t	2026-10-22 16:37:18.110939	\N	\N	\N
114	7	DR MOISES S BERTONI	t	2026-10-22 16:37:18.110939	\N	\N	\N
115	7	GRAL HIGINIO MORINIGO	t	2026-10-22 16:37:18.110939	\N	\N	\N
116	7	MACIEL	t	2026-10-22 16:37:18.110939	\N	\N	\N
117	7	SAN JUAN NEPOMUCENO	t	2026-10-22 16:37:18.110939	\N	\N	\N
118	7	TAVAI	t	2026-10-22 16:37:18.110939	\N	\N	\N
119	7	YEGROS	t	2026-10-22 16:37:18.110939	\N	\N	\N
120	7	YUTY	t	2026-10-22 16:37:18.110939	\N	\N	\N
121	7	3 DE MAYO	t	2026-10-22 16:37:18.110939	\N	\N	\N
122	8	ENCARNACION	t	2026-10-22 16:37:18.110939	\N	\N	\N
123	8	BELLA VISTA	t	2026-10-22 16:37:18.110939	\N	\N	\N
124	8	CAMBYRETA	t	2026-10-22 16:37:18.110939	\N	\N	\N
125	8	CAPITAN MEZA	t	2026-10-22 16:37:18.110939	\N	\N	\N
126	8	CAPITAN MIRANDA	t	2026-10-22 16:37:18.110939	\N	\N	\N
127	8	NUEVA ALBORADA	t	2026-10-22 16:37:18.110939	\N	\N	\N
128	8	CARMEN DEL PARANA	t	2026-10-22 16:37:18.110939	\N	\N	\N
129	8	CORONEL BOGADO	t	2026-10-22 16:37:18.110939	\N	\N	\N
130	8	CARLOS ANTONIO LOPEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
131	8	NATALIO	t	2026-10-22 16:37:18.110939	\N	\N	\N
132	8	FRAM	t	2026-10-22 16:37:18.110939	\N	\N	\N
133	8	GENERAL ARTIGAS	t	2026-10-22 16:37:18.110939	\N	\N	\N
134	8	GENERAL DELGADO	t	2026-10-22 16:37:18.110939	\N	\N	\N
135	8	HOHENAU	t	2026-10-22 16:37:18.110939	\N	\N	\N
136	8	JESUS	t	2026-10-22 16:37:18.110939	\N	\N	\N
137	8	JOSE LEANDRO OVIEDO	t	2026-10-22 16:37:18.110939	\N	\N	\N
138	8	OBLIGADO	t	2026-10-22 16:37:18.110939	\N	\N	\N
139	8	MAYOR JULIO DIONISIO OTAÑO	t	2026-10-22 16:37:18.110939	\N	\N	\N
140	8	SAN COSME Y DAMIAN	t	2026-10-22 16:37:18.110939	\N	\N	\N
141	8	SAN PEDRO DEL PARANA	t	2026-10-22 16:37:18.110939	\N	\N	\N
142	8	SAN RAFAEL DEL PARANA	t	2026-10-22 16:37:18.110939	\N	\N	\N
143	8	TRINIDAD	t	2026-10-22 16:37:18.110939	\N	\N	\N
144	8	EDELIRA	t	2026-10-22 16:37:18.110939	\N	\N	\N
145	8	TOMAS ROMERO PEREIRA	t	2026-10-22 16:37:18.110939	\N	\N	\N
146	8	ALTO VERA	t	2026-10-22 16:37:18.110939	\N	\N	\N
147	8	LA PAZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
148	8	YATYTAY	t	2026-10-22 16:37:18.110939	\N	\N	\N
149	8	SAN JUAN DEL PARANA	t	2026-10-22 16:37:18.110939	\N	\N	\N
150	8	PIRAPO	t	2026-10-22 16:37:18.110939	\N	\N	\N
151	8	ITAPUA POTY	t	2026-10-22 16:37:18.110939	\N	\N	\N
152	9	SAN JUAN BAUTISTA DE LAS MISIONES	t	2026-10-22 16:37:18.110939	\N	\N	\N
153	9	AYOLAS	t	2026-10-22 16:37:18.110939	\N	\N	\N
154	9	SAN IGNACIO	t	2026-10-22 16:37:18.110939	\N	\N	\N
155	9	SAN MIGUEL	t	2026-10-22 16:37:18.110939	\N	\N	\N
156	9	SAN PATRICIO	t	2026-10-22 16:37:18.110939	\N	\N	\N
157	9	SANTA MARIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
158	9	SANTA ROSA	t	2026-10-22 16:37:18.110939	\N	\N	\N
159	9	SANTIAGO	t	2026-10-22 16:37:18.110939	\N	\N	\N
160	9	VILLA FLORIDA	t	2026-10-22 16:37:18.110939	\N	\N	\N
161	9	YABEBYRY	t	2026-10-22 16:37:18.110939	\N	\N	\N
162	10	PARAGUARI	t	2026-10-22 16:37:18.110939	\N	\N	\N
163	10	ACAHAY	t	2026-10-22 16:37:18.110939	\N	\N	\N
164	10	CAAPUCU	t	2026-10-22 16:37:18.110939	\N	\N	\N
165	10	CABALLERO	t	2026-10-22 16:37:18.110939	\N	\N	\N
166	10	CARAPEGUA	t	2026-10-22 16:37:18.110939	\N	\N	\N
167	10	ESCOBAR	t	2026-10-22 16:37:18.110939	\N	\N	\N
168	10	LA COLMENA	t	2026-10-22 16:37:18.110939	\N	\N	\N
169	10	MBUYAPEY	t	2026-10-22 16:37:18.110939	\N	\N	\N
170	10	PIRAYU	t	2026-10-22 16:37:18.110939	\N	\N	\N
171	10	QUIINDY	t	2026-10-22 16:37:18.110939	\N	\N	\N
172	10	QUYQUYHO	t	2026-10-22 16:37:18.110939	\N	\N	\N
173	10	ROQUE GONZALEZ DE SANTA CRUZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
174	10	SAPUCAI	t	2026-10-22 16:37:18.110939	\N	\N	\N
175	10	TEBICUARY MI	t	2026-10-22 16:37:18.110939	\N	\N	\N
176	10	YAGUARON	t	2026-10-22 16:37:18.110939	\N	\N	\N
177	10	YBYCUI	t	2026-10-22 16:37:18.110939	\N	\N	\N
178	10	YBYTYMI	t	2026-10-22 16:37:18.110939	\N	\N	\N
179	11	CIUDAD DEL ESTE	t	2026-10-22 16:37:18.110939	\N	\N	\N
180	11	PRESIDENTE FRANCO	t	2026-10-22 16:37:18.110939	\N	\N	\N
181	11	DOMINGO MARTINEZ DE IRALA	t	2026-10-22 16:37:18.110939	\N	\N	\N
182	11	DR JUAN LEON MALLORQUIN	t	2026-10-22 16:37:18.110939	\N	\N	\N
183	11	HERNANDARIAS	t	2026-10-22 16:37:18.110939	\N	\N	\N
184	11	ITAKYRY	t	2026-10-22 16:37:18.110939	\N	\N	\N
185	11	JUAN E OLEARY	t	2026-10-22 16:37:18.110939	\N	\N	\N
186	11	ÑACUNDAY	t	2026-10-22 16:37:18.110939	\N	\N	\N
187	11	YGUAZU	t	2026-10-22 16:37:18.110939	\N	\N	\N
188	11	LOS CEDRALES	t	2026-10-22 16:37:18.110939	\N	\N	\N
189	11	MINGA GUAZU	t	2026-10-22 16:37:18.110939	\N	\N	\N
190	11	SAN CRISTOBAL	t	2026-10-22 16:37:18.110939	\N	\N	\N
191	11	SANTA RITA	t	2026-10-22 16:37:18.110939	\N	\N	\N
192	11	NARANJAL	t	2026-10-22 16:37:18.110939	\N	\N	\N
193	11	SANTA ROSA DEL MONDAY	t	2026-10-22 16:37:18.110939	\N	\N	\N
194	11	MINGA PORA	t	2026-10-22 16:37:18.110939	\N	\N	\N
195	11	MBARACAYU	t	2026-10-22 16:37:18.110939	\N	\N	\N
196	11	SAN ALBERTO	t	2026-10-22 16:37:18.110939	\N	\N	\N
197	11	IRUÑA	t	2026-10-22 16:37:18.110939	\N	\N	\N
198	11	SANTA FE DEL PARANA	t	2026-10-22 16:37:18.110939	\N	\N	\N
199	11	TAVAPY	t	2026-10-22 16:37:18.110939	\N	\N	\N
200	11	DR RAUL PEÑA	t	2026-10-22 16:37:18.110939	\N	\N	\N
204	12	GUARAMBARE	t	2026-10-22 16:37:18.110939	\N	\N	\N
205	12	ITA	t	2026-10-22 16:37:18.110939	\N	\N	\N
211	12	NUEVA ITALIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
216	12	VILLETA	t	2026-10-22 16:37:18.110939	\N	\N	\N
218	12	YPANE	t	2026-10-22 16:37:18.110939	\N	\N	\N
219	12	J AUGUSTO SALDIVAR	t	2026-10-22 16:37:18.110939	\N	\N	\N
220	13	PILAR	t	2026-10-22 16:37:18.110939	\N	\N	\N
221	13	ALBERDI	t	2026-10-22 16:37:18.110939	\N	\N	\N
222	13	CERRITO	t	2026-10-22 16:37:18.110939	\N	\N	\N
223	13	DESMOCHADOS	t	2026-10-22 16:37:18.110939	\N	\N	\N
224	13	GRAL JOSE EDUVIGIS DIAZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
225	13	GUAZU CUA	t	2026-10-22 16:37:18.110939	\N	\N	\N
226	13	HUMAITA	t	2026-10-22 16:37:18.110939	\N	\N	\N
227	13	ISLA UMBU	t	2026-10-22 16:37:18.110939	\N	\N	\N
228	13	LAURELES	t	2026-10-22 16:37:18.110939	\N	\N	\N
229	15	LAUREL	t	2026-10-22 16:37:18.110939	\N	\N	\N
230	13	MAYOR JOSE DEJESUS MARTINEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
231	13	PASO DE PATRIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
232	13	SAN JUAN BAUTISTA DE ÑEEMBUCU	t	2026-10-22 16:37:18.110939	\N	\N	\N
233	13	TACUARAS	t	2026-10-22 16:37:18.110939	\N	\N	\N
234	13	VILLA FRANCA	t	2026-10-22 16:37:18.110939	\N	\N	\N
235	13	VILLA OLIVA	t	2026-10-22 16:37:18.110939	\N	\N	\N
236	13	VILLALBIN	t	2026-10-22 16:37:18.110939	\N	\N	\N
237	14	PEDRO JUAN CABALLERO	t	2026-10-22 16:37:18.110939	\N	\N	\N
238	14	BELLA VISTA	t	2026-10-22 16:37:18.110939	\N	\N	\N
239	14	CAPITAN BADO	t	2026-10-22 16:37:18.110939	\N	\N	\N
240	14	ZANJA PYTA	t	2026-10-22 16:37:18.110939	\N	\N	\N
241	14	KARAPAI	t	2026-10-22 16:37:18.110939	\N	\N	\N
242	14	CERRO CORA	t	2026-10-22 16:37:18.110939	\N	\N	\N
243	15	SALTO DEL GUAIRA	t	2026-10-22 16:37:18.110939	\N	\N	\N
244	15	CORPUS CHRISTI	t	2026-10-22 16:37:18.110939	\N	\N	\N
245	15	VILLA CURUGUATY	t	2026-10-22 16:37:18.110939	\N	\N	\N
246	15	VILLA YGATIMI	t	2026-10-22 16:37:18.110939	\N	\N	\N
247	15	ITANARA	t	2026-10-22 16:37:18.110939	\N	\N	\N
248	15	YPEJHU	t	2026-10-22 16:37:18.110939	\N	\N	\N
249	15	FRANCISCO CABALLERO ALVAREZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
250	15	KATUETE	t	2026-10-22 16:37:18.110939	\N	\N	\N
251	15	LA PALOMA DEL ESPIRITU SANTO	t	2026-10-22 16:37:18.110939	\N	\N	\N
252	15	NUEVA ESPERANZA	t	2026-10-22 16:37:18.110939	\N	\N	\N
253	15	YASY CAÑY	t	2026-10-22 16:37:18.110939	\N	\N	\N
254	15	YBYRAROBANA	t	2026-10-22 16:37:18.110939	\N	\N	\N
255	15	YBY PYTA	t	2026-10-22 16:37:18.110939	\N	\N	\N
256	15	MARACANA	t	2026-10-22 16:37:18.110939	\N	\N	\N
257	15	PUERTO ADELA	t	2026-10-22 16:37:18.110939	\N	\N	\N
258	16	BENJAMIN ACEVAL	t	2026-10-22 16:37:18.110939	\N	\N	\N
259	16	PUERTO PINASCO	t	2026-10-22 16:37:18.110939	\N	\N	\N
260	16	VILLA HAYES	t	2026-10-22 16:37:18.110939	\N	\N	\N
261	16	NANAWA	t	2026-10-22 16:37:18.110939	\N	\N	\N
262	16	JOSE FALCON	t	2026-10-22 16:37:18.110939	\N	\N	\N
263	16	TTE 1 MANUEL IRALA FERNANDEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
264	16	TENIENTE ESTEBAN MARTINEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
265	16	GENERAL JOSE MARIA BRUGUEZ	t	2026-10-22 16:37:18.110939	\N	\N	\N
266	16	CAMPO ACEVAL	t	2026-10-22 16:37:18.110939	\N	\N	\N
267	16	NUEVA ASUNCION	t	2026-10-22 16:37:18.110939	\N	\N	\N
268	17	MARISCAL JOSE FELIX ESTIGARRIBIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
269	17	FILADELFIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
270	17	LOMA PLATA	t	2026-10-22 16:37:18.110939	\N	\N	\N
271	17	BOQUERON	t	2026-10-22 16:37:18.110939	\N	\N	\N
272	18	FUERTE OLIMPO	t	2026-10-22 16:37:18.110939	\N	\N	\N
273	18	PUERTO CASADO	t	2026-10-22 16:37:18.110939	\N	\N	\N
274	18	BAHIA NEGRA	t	2026-10-22 16:37:18.110939	\N	\N	\N
275	18	CARMELO PERALTA	t	2026-10-22 16:37:18.110939	\N	\N	\N
276	2	ITACUA	t	2026-10-22 16:37:18.110939	\N	\N	\N
277	5	DOCTOR BOTTRELL	t	2026-10-22 16:37:18.110939	\N	\N	\N
278	5	PASO YOBAI	t	2026-10-22 16:37:18.110939	\N	\N	\N
279	10	MARIA ANTONIA	t	2026-10-22 16:37:18.110939	\N	\N	\N
\.

SELECT pg_catalog.setval('public.acciones_id_accion_seq', 4, true);

SELECT pg_catalog.setval('public.cargos_id_cargo_seq', 18, true);

SELECT pg_catalog.setval('public.ciudades_id_ciudad_seq', 279, true);

SELECT pg_catalog.setval('public.condiciones_venta_id_condicion_venta_seq', 2, true);

SELECT pg_catalog.setval('public.departamentos_id_departamento_seq', 20, true);

SELECT pg_catalog.setval('public.diagnosticos_id_diagnostico_seq', 8, true);

SELECT pg_catalog.setval('public.dias_semana_id_dia_semana_seq', 7, true);

SELECT pg_catalog.setval('public.entidades_adheridas_id_entidad_adherida_seq', 5, true);

SELECT pg_catalog.setval('public.entidades_emisoras_id_entidad_emisora_seq', 11, true);

SELECT pg_catalog.setval('public.especialidades_id_especialidad_seq', 8, true);

SELECT pg_catalog.setval('public.estados_citas_id_estado_cita_seq', 6, true);

SELECT pg_catalog.setval('public.estados_civiles_id_estado_civil_seq', 7, true);

SELECT pg_catalog.setval('public.estados_factura_id_estado_factura_seq', 2, true);

SELECT pg_catalog.setval('public.formas_cobro_id_forma_cobro_seq', 5, true);

SELECT pg_catalog.setval('public.generos_id_genero_seq', 12, true);

SELECT pg_catalog.setval('public.instrumentos_id_instrumento_seq', 11, true);

SELECT pg_catalog.setval('public.insumos_id_insumo_seq', 1, true);

SELECT pg_catalog.setval('public.marcas_tarjeta_id_marca_tarjeta_seq', 6, true);

SELECT pg_catalog.setval('public.medicamentos_id_medicamento_seq', 12, true);

SELECT pg_catalog.setval('public.modulos_id_modulo_seq', 5, true);

SELECT pg_catalog.setval('public.monedas_id_moneda_seq', 2, true);

SELECT pg_catalog.setval('public.niveles_instruccion_id_nivel_instruccion_seq', 8, true);

SELECT pg_catalog.setval('public.paginas_id_pagina_seq', 34, true);

SELECT pg_catalog.setval('public.paises_id_pais_seq', 3, true);

SELECT pg_catalog.setval('public.profesiones_id_profesion_seq', 2, true);

SELECT pg_catalog.setval('public.roles_id_rol_seq', 6, true);

SELECT pg_catalog.setval('public.roles_paginas_id_rol_pagina_seq', 103, true);

SELECT pg_catalog.setval('public.roles_permisos_id_rol_permiso_seq', 90, true);

SELECT pg_catalog.setval('public.signos_id_signo_seq', 9, true);

SELECT pg_catalog.setval('public.sintomas_id_sintoma_seq', 9, true);

SELECT pg_catalog.setval('public.tipos_analisis_id_tipo_analisis_seq', 12, true);

SELECT pg_catalog.setval('public.tipos_certificados_medicos_id_tipo_certificado_medico_seq', 9, true);

SELECT pg_catalog.setval('public.tipos_comprobantes_id_tipo_comprobante_seq', 2, true);

SELECT pg_catalog.setval('public.tipos_estudios_id_tipo_estudio_seq', 11, true);

SELECT pg_catalog.setval('public.tipos_impuestos_id_tipo_impuesto_seq', 6, true);

SELECT pg_catalog.setval('public.tipos_items_id_tipo_item_seq', 3, true);

SELECT pg_catalog.setval('public.tipos_procedimientos_id_tipo_procedimiento_seq', 7, true);

SELECT pg_catalog.setval('public.tipos_tratamientos_id_tipo_tratamiento_seq', 10, true);
