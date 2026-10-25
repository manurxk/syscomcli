-- ============================================================================
--  ESTRUCTURA DEL SISTEMA - PODOLOGIA BARRETO (base ATENCION_MEDICA_DB)
--  Script de creacion desde cero: solo estructura, sin datos.
--  Generado el 2026-10-23 a partir de la base actual (PostgreSQL 14).
--
--  Contenido: 59 tablas, 82 relaciones (FK),
--             10 vistas, 2 funciones. Triggers: ninguno en uso.
--  No incluye (sin uso en el sistema): ocupaciones, fichas, notificaciones,
--             vw_consulta_completa, vw_ficha_paciente, vw_ficha_podologica, vw_historial_clinico.
--  FK duplicadas en la base actual (se omiten aqui, se deja una sola):
--     consultas.consultas_id_cita_fkey (igual a fk_consultas_cita)
--     consultas.consultas_id_tipo_orden_analisis_fkey (igual a fk_consultas_tipo_analisis)
--     consultas.consultas_id_tipo_orden_estudio_fkey (igual a fk_consultas_tipo_estudio)
--
--  Las tablas estan ordenadas para que cada una se cree despues de las
--  tablas a las que referencia. Cada tabla indica sus relaciones:
--     ->  tabla a la que apunta (FK de esta tabla)
--     <-  tablas que apuntan a esta
--
--  USO:  createdb -U postgres ATENCION_MEDICA_DB
--        psql -U postgres -d ATENCION_MEDICA_DB -f estructura_sistema_podologia.sql
-- ============================================================================

SET client_encoding = 'UTF8';

-- ----------------------------------------------------------------------------
--  MAPA DE TABLAS POR MODULO
-- ----------------------------------------------------------------------------
--  SEGURIDAD Y USUARIOS: roles, permisos_rol, usuarios, auditoria_accesos
--  REFERENCIALES GENERALES: ciudades, generos, estado_civiles, estado_laborales, dias, turnos, especialidades, sala_atenciones, consultorio
--  PERSONAS: PACIENTES, MEDICOS Y FUNCIONARIOS: personas, pacientes, medicos, funcionarios
--  AGENDA MEDICA Y CITAS: agenda_medicas, disponibilidad_horaria, estado_citas, citas, avisos_recordatorios
--  FICHA MEDICA: grupos_sanguineos, tipos_alergia, medicamentos, ficha_medica, alergias_paciente, ficha_antecedentes_familiares, ficha_medicacion_habitual
--  INSUMOS, SERVICIOS E IVA: tipos_iva, insumos, servicios_facturables
--  CONSULTA: enfermedades, tratamientos, tipo_orden_analisis, tipo_orden_estudio, consultas, anamnesis_podologica, signos_vitales, consulta_diagnosticos, consulta_procedimientos, consulta_ordenes, orden_analisis, orden_estudio, recetas, receta_detalle, justificativos, consulta_insumos, stock_insumos
--  FACTURACION Y CAJA: datos_emisor, estados_factura, tipos_comprobante, formas_cobro, cajas, facturas, factura_detalle, cobranzas, motivos_nota, notas


-- ============================================================================
--  MODULO: SEGURIDAD Y USUARIOS
-- ============================================================================

-- Tabla: roles
--   <-  funcionarios, permisos_rol, usuarios
CREATE TABLE roles (
    id_rol SERIAL,
    descripcion character varying(50) NOT NULL,
    CONSTRAINT roles_pkey PRIMARY KEY (id_rol),
    CONSTRAINT roles_descripcion_key UNIQUE (descripcion)
);

-- Tabla: permisos_rol
--   ->  roles
CREATE TABLE permisos_rol (
    id_rol integer NOT NULL,
    modulo character varying(40) NOT NULL,
    puede_modificar boolean NOT NULL DEFAULT false,
    CONSTRAINT permisos_rol_pkey PRIMARY KEY (id_rol, modulo),
    CONSTRAINT permisos_rol_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE
);

-- Tabla: usuarios
--   ->  roles
--   <-  auditoria_accesos, cajas, funcionarios, notas, stock_insumos
CREATE TABLE usuarios (
    id_usuario SERIAL,
    nickname text NOT NULL,
    clave text NOT NULL,
    estado boolean NOT NULL,
    id_rol integer,
    totp_secreto character varying(64),
    totp_activo boolean NOT NULL DEFAULT false,
    totp_ultimo_paso bigint,
    CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario),
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- Tabla: auditoria_accesos
--   ->  usuarios
CREATE TABLE auditoria_accesos (
    id_auditoria SERIAL,
    fecha timestamp without time zone NOT NULL DEFAULT now(),
    id_usuario integer,
    usuario character varying(60),
    evento character varying(30) NOT NULL,
    detalle text,
    ip character varying(45),
    navegador character varying(255),
    CONSTRAINT auditoria_accesos_pkey PRIMARY KEY (id_auditoria),
    CONSTRAINT auditoria_accesos_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================================
--  MODULO: REFERENCIALES GENERALES
-- ============================================================================

-- Tabla: ciudades
--   <-  consultorio, personas
CREATE TABLE ciudades (
    id_ciudad SERIAL,
    descripcion character varying(60),
    CONSTRAINT ciudades_pkey PRIMARY KEY (id_ciudad),
    CONSTRAINT ciudades_descripcion_key UNIQUE (descripcion)
);

-- Tabla: generos
--   <-  personas
CREATE TABLE generos (
    id_genero SERIAL,
    descripcion character varying(60),
    CONSTRAINT generos_pkey PRIMARY KEY (id_genero),
    CONSTRAINT generos_descripcion_key UNIQUE (descripcion)
);

-- Tabla: estado_civiles
--   <-  personas
CREATE TABLE estado_civiles (
    id_estado_civil SERIAL,
    descripcion character varying(60),
    CONSTRAINT estado_civiles_pkey PRIMARY KEY (id_estado_civil),
    CONSTRAINT estado_civiles_descripcion_key UNIQUE (descripcion)
);

-- Tabla: estado_laborales
--   <-  agenda_medicas
CREATE TABLE estado_laborales (
    id_estado_laboral SERIAL,
    descripcion character varying(60),
    CONSTRAINT estado_laborales_pkey PRIMARY KEY (id_estado_laboral),
    CONSTRAINT estado_laborales_descripcion_key UNIQUE (descripcion)
);

-- Tabla: dias
--   <-  agenda_medicas
CREATE TABLE dias (
    id_dia SERIAL,
    descripcion character varying(60),
    CONSTRAINT dias_pkey PRIMARY KEY (id_dia),
    CONSTRAINT dias_descripcion_key UNIQUE (descripcion)
);

-- Tabla: turnos
--   <-  agenda_medicas
CREATE TABLE turnos (
    id_turno SERIAL,
    descripcion character varying(60),
    CONSTRAINT turnos_pkey PRIMARY KEY (id_turno),
    CONSTRAINT turnos_descripcion_key UNIQUE (descripcion)
);

-- Tabla: especialidades
--   <-  agenda_medicas
CREATE TABLE especialidades (
    id_especialidad SERIAL,
    descripcion character varying(60),
    CONSTRAINT especialidades_pkey PRIMARY KEY (id_especialidad),
    CONSTRAINT especialidades_descripcion_key UNIQUE (descripcion)
);

-- Tabla: sala_atenciones
--   <-  agenda_medicas
CREATE TABLE sala_atenciones (
    id_sala_atencion SERIAL,
    nombre character varying(60),
    CONSTRAINT sala_atenciones_pkey PRIMARY KEY (id_sala_atencion),
    CONSTRAINT sala_atenciones_nombre_key UNIQUE (nombre)
);

-- Tabla: consultorio
--   ->  ciudades
--   <-  consultas, funcionarios
CREATE TABLE consultorio (
    id_consultorio SERIAL,
    nombre character varying(200) NOT NULL,
    ruc character varying(20),
    direccion character varying(300),
    telefono character varying(50),
    email character varying(150),
    id_ciudad integer,
    estado boolean DEFAULT true,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT consultorio_pkey PRIMARY KEY (id_consultorio),
    CONSTRAINT fk_consultorio_ciudad FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad)
);

-- ============================================================================
--  MODULO: PERSONAS: PACIENTES, MEDICOS Y FUNCIONARIOS
-- ============================================================================

-- Tabla: personas
--   ->  ciudades, estado_civiles, generos
--   <-  funcionarios, medicos, pacientes
CREATE TABLE personas (
    id_persona SERIAL,
    nombre character varying(255),
    apellido character varying(255),
    cedula text NOT NULL,
    id_genero integer NOT NULL,
    id_estado_civil integer NOT NULL,
    telefono_emergencia text NOT NULL,
    id_ciudad integer NOT NULL,
    gmail character varying(255),
    CONSTRAINT personas_pkey PRIMARY KEY (id_persona),
    CONSTRAINT personas_id_ciudad_fkey FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT personas_id_estado_civil_fkey FOREIGN KEY (id_estado_civil) REFERENCES estado_civiles(id_estado_civil) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT personas_id_genero_fkey FOREIGN KEY (id_genero) REFERENCES generos(id_genero) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla: pacientes
--   ->  personas
--   <-  citas, ficha_medica
CREATE TABLE pacientes (
    id_paciente SERIAL,
    id_persona integer NOT NULL,
    fecha_nacimiento date NOT NULL,
    peso numeric,
    altura numeric,
    CONSTRAINT pacientes_pkey PRIMARY KEY (id_paciente),
    CONSTRAINT pacientes_altura_check CHECK ((altura >= (0)::numeric)),
    CONSTRAINT pacientes_peso_check CHECK ((peso >= (0)::numeric)),
    CONSTRAINT pacientes_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES personas(id_persona) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla: medicos
--   ->  personas
--   <-  agenda_medicas
CREATE TABLE medicos (
    id_medico SERIAL,
    id_persona integer NOT NULL,
    matricula character varying(255),
    CONSTRAINT medicos_pkey PRIMARY KEY (id_medico),
    CONSTRAINT medicos_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES personas(id_persona) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla: funcionarios
--   ->  consultorio, personas, roles, usuarios
--   <-  agenda_medicas, avisos_recordatorios, citas, consultas, facturas
CREATE TABLE funcionarios (
    id_funcionario SERIAL,
    id_persona integer NOT NULL,
    id_usuario integer NOT NULL,
    id_consultorio integer NOT NULL,
    id_rol integer NOT NULL,
    cargo character varying(100),
    fecha_ingreso date NOT NULL DEFAULT CURRENT_DATE,
    estado boolean DEFAULT true,
    CONSTRAINT funcionarios_pkey PRIMARY KEY (id_funcionario),
    CONSTRAINT funcionarios_id_usuario_key UNIQUE (id_usuario),
    CONSTRAINT fk_func_consultorio FOREIGN KEY (id_consultorio) REFERENCES consultorio(id_consultorio),
    CONSTRAINT fk_func_persona FOREIGN KEY (id_persona) REFERENCES personas(id_persona),
    CONSTRAINT fk_func_rol FOREIGN KEY (id_rol) REFERENCES roles(id_rol),
    CONSTRAINT fk_func_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- ============================================================================
--  MODULO: AGENDA MEDICA Y CITAS
-- ============================================================================

-- Tabla: agenda_medicas
--   ->  dias, especialidades, estado_laborales, funcionarios, medicos, sala_atenciones, turnos
--   <-  disponibilidad_horaria
CREATE TABLE agenda_medicas (
    id_agenda_medica SERIAL,
    id_medico integer NOT NULL,
    id_especialidad integer NOT NULL,
    id_turno integer NOT NULL,
    id_dia integer NOT NULL,
    id_estado_laboral integer NOT NULL,
    id_sala_atencion integer NOT NULL,
    id_funcionario integer,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    hora_inicio time without time zone,
    hora_fin time without time zone,
    fecha_desde date,
    fecha_hasta date,
    CONSTRAINT agenda_medicas_pkey PRIMARY KEY (id_agenda_medica),
    CONSTRAINT fk_agenda_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario),
    CONSTRAINT agenda_medicas_id_dia_fkey FOREIGN KEY (id_dia) REFERENCES dias(id_dia) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT agenda_medicas_id_especialidad_fkey FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT agenda_medicas_id_estado_laboral_fkey FOREIGN KEY (id_estado_laboral) REFERENCES estado_laborales(id_estado_laboral) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT agenda_medicas_id_medico_fkey FOREIGN KEY (id_medico) REFERENCES medicos(id_medico) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT agenda_medicas_id_sala_atencion_fkey FOREIGN KEY (id_sala_atencion) REFERENCES sala_atenciones(id_sala_atencion) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT agenda_medicas_id_turno_fkey FOREIGN KEY (id_turno) REFERENCES turnos(id_turno) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla: disponibilidad_horaria
--   ->  agenda_medicas
--   <-  citas
CREATE TABLE disponibilidad_horaria (
    id_disponibilidad_horaria SERIAL,
    id_agenda_medica integer NOT NULL,
    fecha date NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fin time without time zone NOT NULL,
    estado boolean DEFAULT true,
    bloqueado boolean NOT NULL DEFAULT false,
    CONSTRAINT disponibilidad_horaria_pkey PRIMARY KEY (id_disponibilidad_horaria),
    CONSTRAINT uq_disponibilidad UNIQUE (id_agenda_medica, fecha, hora_inicio, hora_fin),
    CONSTRAINT disponibilidad_horaria_id_agenda_medica_fkey FOREIGN KEY (id_agenda_medica) REFERENCES agenda_medicas(id_agenda_medica) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Tabla: estado_citas
--   <-  citas
CREATE TABLE estado_citas (
    id_estado_cita SERIAL,
    descripcion character varying(60) NOT NULL,
    CONSTRAINT estado_citas_pkey PRIMARY KEY (id_estado_cita),
    CONSTRAINT estado_citas_descripcion_key UNIQUE (descripcion)
);

-- Tabla: citas
--   ->  disponibilidad_horaria, estado_citas, funcionarios, pacientes
--   <-  avisos_recordatorios, consultas
CREATE TABLE citas (
    id_cita SERIAL,
    id_disponibilidad_horaria integer NOT NULL,
    id_paciente integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    observacion character varying(200),
    id_estado_cita integer NOT NULL,
    id_funcionario integer,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT citas_pkey PRIMARY KEY (id_cita),
    CONSTRAINT uq_cita UNIQUE (id_disponibilidad_horaria),
    CONSTRAINT fk_cita_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario),
    CONSTRAINT citas_id_disponibilidad_horaria_fkey FOREIGN KEY (id_disponibilidad_horaria) REFERENCES disponibilidad_horaria(id_disponibilidad_horaria) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT citas_id_estado_cita_fkey FOREIGN KEY (id_estado_cita) REFERENCES estado_citas(id_estado_cita) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT citas_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla: avisos_recordatorios
--   ->  citas, funcionarios
CREATE TABLE avisos_recordatorios (
    id_aviso SERIAL,
    id_cita integer NOT NULL,
    fecha_programada timestamp without time zone NOT NULL,
    fecha_envio timestamp without time zone,
    metodo_envio character varying(50) DEFAULT 'whatsapp'::character varying,
    mensaje text,
    estado character varying(20) DEFAULT 'pendiente'::character varying,
    destinatario character varying(255),
    intentos_envio integer DEFAULT 0,
    observacion text,
    respuesta character varying(20),
    fecha_respuesta timestamp without time zone,
    id_funcionario integer,
    CONSTRAINT avisos_recordatorios_pkey PRIMARY KEY (id_aviso),
    CONSTRAINT avisos_recordatorios_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES citas(id_cita),
    CONSTRAINT avisos_recordatorios_id_funcionario_fkey FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);

-- ============================================================================
--  MODULO: FICHA MEDICA
-- ============================================================================

-- Tabla: grupos_sanguineos
--   <-  ficha_medica
CREATE TABLE grupos_sanguineos (
    id_grupo_sanguineo SERIAL,
    descripcion character varying(10) NOT NULL,
    CONSTRAINT grupos_sanguineos_pkey PRIMARY KEY (id_grupo_sanguineo)
);

-- Tabla: tipos_alergia
--   <-  alergias_paciente
CREATE TABLE tipos_alergia (
    id_tipo_alergia SERIAL,
    descripcion character varying(100) NOT NULL,
    estado boolean DEFAULT true,
    CONSTRAINT tipos_alergia_pkey PRIMARY KEY (id_tipo_alergia)
);

-- Tabla: medicamentos
--   <-  ficha_medicacion_habitual, receta_detalle
CREATE TABLE medicamentos (
    id_medicamento SERIAL,
    nombre character varying(200) NOT NULL,
    principio_activo character varying(200),
    presentacion character varying(100),
    concentracion character varying(100),
    via_administracion character varying(80),
    estado boolean DEFAULT true,
    CONSTRAINT pk_medicamentos PRIMARY KEY (id_medicamento)
);

-- Tabla: ficha_medica
--   ->  grupos_sanguineos, pacientes
--   <-  alergias_paciente, ficha_antecedentes_familiares, ficha_medicacion_habitual
CREATE TABLE ficha_medica (
    id_ficha SERIAL,
    id_paciente integer NOT NULL,
    id_grupo_sanguineo integer,
    peso_habitual numeric(5,2),
    talla numeric(5,2),
    enfermedades_cronicas text,
    antecedentes_quirurgicos text,
    antecedentes_familiares text,
    medicacion_habitual text,
    tabaquismo boolean DEFAULT false,
    alcoholismo boolean DEFAULT false,
    actividad_fisica boolean DEFAULT false,
    detalle_habitos text,
    observaciones text,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ocupacion character varying(150),
    numero_calzado character varying(10),
    toma_medicamento boolean DEFAULT false,
    alergia_medicamento boolean DEFAULT false,
    padece_diabetes boolean DEFAULT false,
    padece_hta boolean DEFAULT false,
    padece_artritis boolean DEFAULT false,
    padece_artrosis boolean DEFAULT false,
    padece_osteoporosis boolean DEFAULT false,
    padece_otro character varying(300),
    fam_diabetes boolean DEFAULT false,
    fam_diabetes_esp character varying(200),
    fam_hta boolean DEFAULT false,
    fam_hta_esp character varying(200),
    fam_psoriasis boolean DEFAULT false,
    fam_psoriasis_esp character varying(200),
    CONSTRAINT pk_ficha_medica PRIMARY KEY (id_ficha),
    CONSTRAINT uix_ficha_paciente UNIQUE (id_paciente),
    CONSTRAINT fk_ficha_grupo_sang FOREIGN KEY (id_grupo_sanguineo) REFERENCES grupos_sanguineos(id_grupo_sanguineo),
    CONSTRAINT fk_ficha_paciente FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
);

-- Tabla: alergias_paciente
--   ->  ficha_medica, tipos_alergia
CREATE TABLE alergias_paciente (
    id_alergia_paciente SERIAL,
    id_ficha integer NOT NULL,
    id_tipo_alergia integer NOT NULL,
    descripcion character varying(300) NOT NULL,
    gravedad character varying(50),
    CONSTRAINT pk_alergias_paciente PRIMARY KEY (id_alergia_paciente),
    CONSTRAINT fk_alergia_ficha FOREIGN KEY (id_ficha) REFERENCES ficha_medica(id_ficha),
    CONSTRAINT fk_alergia_tipo FOREIGN KEY (id_tipo_alergia) REFERENCES tipos_alergia(id_tipo_alergia)
);

-- Tabla: ficha_antecedentes_familiares
--   ->  ficha_medica
CREATE TABLE ficha_antecedentes_familiares (
    id_antecedente_familiar SERIAL,
    id_ficha integer NOT NULL,
    enfermedad character varying(150) NOT NULL,
    parentesco character varying(150),
    CONSTRAINT ficha_antecedentes_familiares_pkey PRIMARY KEY (id_antecedente_familiar),
    CONSTRAINT ficha_antecedentes_familiares_id_ficha_fkey FOREIGN KEY (id_ficha) REFERENCES ficha_medica(id_ficha) ON DELETE CASCADE
);

-- Tabla: ficha_medicacion_habitual
--   ->  ficha_medica, medicamentos
CREATE TABLE ficha_medicacion_habitual (
    id_ficha_medicacion SERIAL,
    id_ficha integer NOT NULL,
    id_medicamento integer,
    descripcion character varying(200) NOT NULL,
    CONSTRAINT ficha_medicacion_habitual_pkey PRIMARY KEY (id_ficha_medicacion),
    CONSTRAINT ficha_medicacion_habitual_id_ficha_fkey FOREIGN KEY (id_ficha) REFERENCES ficha_medica(id_ficha) ON DELETE CASCADE,
    CONSTRAINT ficha_medicacion_habitual_id_medicamento_fkey FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento)
);

-- ============================================================================
--  MODULO: INSUMOS, SERVICIOS E IVA
-- ============================================================================

-- Tabla: tipos_iva
--   <-  factura_detalle, insumos, servicios_facturables
CREATE TABLE tipos_iva (
    id_tipo_iva SERIAL,
    descripcion character varying(40) NOT NULL,
    porcentaje numeric(5,2) NOT NULL,
    CONSTRAINT tipos_iva_pkey PRIMARY KEY (id_tipo_iva),
    CONSTRAINT tipos_iva_descripcion_key UNIQUE (descripcion)
);

-- Tabla: insumos
--   ->  tipos_iva
--   <-  consulta_insumos, stock_insumos
CREATE TABLE insumos (
    id_insumo SERIAL,
    nombre character varying(200) NOT NULL,
    descripcion character varying(300),
    unidad_medida character varying(50),
    estado boolean DEFAULT true,
    precio_venta numeric(12,2) NOT NULL DEFAULT 0,
    id_tipo_iva integer,
    stock_actual numeric(10,2) NOT NULL DEFAULT 0,
    stock_minimo numeric(10,2) NOT NULL DEFAULT 0,
    CONSTRAINT pk_insumos PRIMARY KEY (id_insumo),
    CONSTRAINT fk_insumo_tipo_iva FOREIGN KEY (id_tipo_iva) REFERENCES tipos_iva(id_tipo_iva)
);

-- Tabla: servicios_facturables
--   ->  tipos_iva
--   <-  consulta_procedimientos, factura_detalle
CREATE TABLE servicios_facturables (
    id_servicio SERIAL,
    descripcion character varying(200) NOT NULL,
    precio_unitario numeric(12,2) NOT NULL DEFAULT 0,
    id_tipo_iva integer NOT NULL,
    estado boolean DEFAULT true,
    CONSTRAINT servicios_facturables_pkey PRIMARY KEY (id_servicio),
    CONSTRAINT fk_servicio_iva FOREIGN KEY (id_tipo_iva) REFERENCES tipos_iva(id_tipo_iva)
);

-- ============================================================================
--  MODULO: CONSULTA
-- ============================================================================

-- Tabla: enfermedades
--   <-  consulta_diagnosticos, consultas, tratamientos
CREATE TABLE enfermedades (
    id_enfermedad SERIAL,
    codigo_cie character varying(10),
    descripcion character varying(200) NOT NULL,
    estado boolean DEFAULT true,
    CONSTRAINT pk_enfermedades PRIMARY KEY (id_enfermedad)
);

-- Tabla: tratamientos
--   ->  enfermedades
--   <-  consulta_diagnosticos, consultas
CREATE TABLE tratamientos (
    id_tratamiento SERIAL,
    id_enfermedad integer NOT NULL,
    descripcion character varying(300) NOT NULL,
    indicaciones text,
    estado boolean DEFAULT true,
    CONSTRAINT pk_tratamientos PRIMARY KEY (id_tratamiento),
    CONSTRAINT fk_tratamientos_enfermedad FOREIGN KEY (id_enfermedad) REFERENCES enfermedades(id_enfermedad)
);

-- Tabla: tipo_orden_analisis
--   <-  consultas, orden_analisis
CREATE TABLE tipo_orden_analisis (
    id_tipo_orden_analisis SERIAL,
    descripcion character varying(100) NOT NULL,
    estado boolean DEFAULT true,
    CONSTRAINT tipo_orden_analisis_pkey PRIMARY KEY (id_tipo_orden_analisis),
    CONSTRAINT tipo_orden_analisis_descripcion_key UNIQUE (descripcion)
);

-- Tabla: tipo_orden_estudio
--   <-  consultas, orden_estudio
CREATE TABLE tipo_orden_estudio (
    id_tipo_orden_estudio SERIAL,
    descripcion character varying(100) NOT NULL,
    estado boolean DEFAULT true,
    CONSTRAINT tipo_orden_estudio_pkey PRIMARY KEY (id_tipo_orden_estudio),
    CONSTRAINT tipo_orden_estudio_descripcion_key UNIQUE (descripcion)
);

-- Tabla: consultas
--   ->  citas, consultorio, enfermedades, funcionarios, tipo_orden_analisis, tipo_orden_estudio, tratamientos
--   <-  anamnesis_podologica, consulta_diagnosticos, consulta_insumos, consulta_ordenes, consulta_procedimientos, facturas, justificativos, orden_analisis, orden_estudio, recetas, signos_vitales, stock_insumos
CREATE TABLE consultas (
    id_consulta SERIAL,
    id_cita integer NOT NULL,
    id_tipo_orden_estudio integer,
    fecha_emision_estudio date,
    fecha_vencimiento_estudio date,
    id_tipo_orden_analisis integer,
    fecha_emision_analisis date,
    fecha_vencimiento_analisis date,
    motivo_consulta text NOT NULL,
    diagnostico text,
    tratamiento text,
    observaciones text,
    fecha_consulta timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_enfermedad integer,
    id_tratamiento integer,
    requiere_orden_estudio boolean DEFAULT false,
    requiere_orden_analisis boolean DEFAULT false,
    id_funcionario integer,
    id_consultorio integer,
    diagnostico_presuntivo text,
    CONSTRAINT consultas_pkey PRIMARY KEY (id_consulta),
    CONSTRAINT uq_consulta_cita UNIQUE (id_cita),
    CONSTRAINT fk_consulta_consultorio FOREIGN KEY (id_consultorio) REFERENCES consultorio(id_consultorio),
    CONSTRAINT fk_consulta_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario),
    CONSTRAINT fk_consultas_cita FOREIGN KEY (id_cita) REFERENCES citas(id_cita),
    CONSTRAINT fk_consultas_enfermedad FOREIGN KEY (id_enfermedad) REFERENCES enfermedades(id_enfermedad),
    CONSTRAINT fk_consultas_tipo_analisis FOREIGN KEY (id_tipo_orden_analisis) REFERENCES tipo_orden_analisis(id_tipo_orden_analisis),
    CONSTRAINT fk_consultas_tipo_estudio FOREIGN KEY (id_tipo_orden_estudio) REFERENCES tipo_orden_estudio(id_tipo_orden_estudio),
    CONSTRAINT fk_consultas_tratamiento FOREIGN KEY (id_tratamiento) REFERENCES tratamientos(id_tratamiento)
);

-- Tabla: anamnesis_podologica
--   ->  consultas
CREATE TABLE anamnesis_podologica (
    id_anamnesis SERIAL,
    id_consulta integer NOT NULL,
    tipo_pie character varying(150),
    alteracion_de character varying(300),
    onicopatias character varying(300),
    area_trabajo text,
    diagnostico_podologico text,
    proxima_cita date,
    CONSTRAINT pk_anamnesis_podologica PRIMARY KEY (id_anamnesis),
    CONSTRAINT uix_anamnesis_consulta UNIQUE (id_consulta),
    CONSTRAINT fk_anamnesis_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta)
);

-- Tabla: signos_vitales
--   ->  consultas
CREATE TABLE signos_vitales (
    id_signos_vitales SERIAL,
    id_consulta integer NOT NULL,
    peso numeric(5,2),
    talla numeric(5,2),
    presion_sistolica integer,
    presion_diastolica integer,
    temperatura numeric(4,1),
    frecuencia_cardiaca integer,
    frecuencia_resp integer,
    saturacion_oxigeno numeric(4,1),
    glucemia numeric(5,1),
    observaciones text,
    pulso_pedio_izq character varying(10),
    pulso_pedio_der character varying(10),
    pulso_tibial_izq character varying(10),
    pulso_tibial_der character varying(10),
    temperatura_pie character varying(20),
    CONSTRAINT pk_signos_vitales PRIMARY KEY (id_signos_vitales),
    CONSTRAINT uix_signos_consulta UNIQUE (id_consulta),
    CONSTRAINT fk_signos_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta)
);

-- Tabla: consulta_diagnosticos
--   ->  consultas, enfermedades, tratamientos
CREATE TABLE consulta_diagnosticos (
    id_consulta_diagnostico SERIAL,
    id_consulta integer NOT NULL,
    id_enfermedad integer,
    id_tratamiento integer,
    diagnostico text,
    tratamiento text,
    orden smallint NOT NULL DEFAULT 1,
    CONSTRAINT consulta_diagnosticos_pkey PRIMARY KEY (id_consulta_diagnostico),
    CONSTRAINT chk_diag_con_contenido CHECK (((id_enfermedad IS NOT NULL) OR (COALESCE(TRIM(BOTH FROM diagnostico), ''::text) <> ''::text))),
    CONSTRAINT consulta_diagnosticos_id_consulta_fkey FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
    CONSTRAINT consulta_diagnosticos_id_enfermedad_fkey FOREIGN KEY (id_enfermedad) REFERENCES enfermedades(id_enfermedad),
    CONSTRAINT consulta_diagnosticos_id_tratamiento_fkey FOREIGN KEY (id_tratamiento) REFERENCES tratamientos(id_tratamiento)
);

-- Tabla: consulta_procedimientos
--   ->  consultas, servicios_facturables
CREATE TABLE consulta_procedimientos (
    id_consulta_procedimiento SERIAL,
    id_consulta integer NOT NULL,
    id_servicio integer NOT NULL,
    cantidad numeric(10,2) NOT NULL DEFAULT 1,
    observacion character varying(300),
    CONSTRAINT consulta_procedimientos_pkey PRIMARY KEY (id_consulta_procedimiento),
    CONSTRAINT fk_cp_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT fk_cp_servicio FOREIGN KEY (id_servicio) REFERENCES servicios_facturables(id_servicio)
);

-- Tabla: consulta_ordenes
--   ->  consultas
CREATE TABLE consulta_ordenes (
    id_consulta_orden SERIAL,
    id_consulta integer NOT NULL,
    tipo character varying(10) NOT NULL,
    id_tipo_orden integer NOT NULL,
    fecha_emision date DEFAULT CURRENT_DATE,
    fecha_vencimiento date,
    observacion character varying(300),
    CONSTRAINT consulta_ordenes_pkey PRIMARY KEY (id_consulta_orden),
    CONSTRAINT chk_tipo CHECK (((tipo)::text = ANY ((ARRAY['estudio'::character varying, 'analisis'::character varying])::text[]))),
    CONSTRAINT fk_cord_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta)
);

-- Tabla: orden_analisis
--   ->  consultas, tipo_orden_analisis
CREATE TABLE orden_analisis (
    id_orden_analisis SERIAL,
    id_tipo_orden_analisis integer NOT NULL,
    fecha_emision date NOT NULL DEFAULT CURRENT_DATE,
    observacion text,
    estado character varying(20) DEFAULT 'pendiente'::character varying,
    id_consulta integer,
    CONSTRAINT orden_analisis_pkey PRIMARY KEY (id_orden_analisis),
    CONSTRAINT fk_orden_analisis_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT orden_analisis_id_tipo_orden_analisis_fkey FOREIGN KEY (id_tipo_orden_analisis) REFERENCES tipo_orden_analisis(id_tipo_orden_analisis) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla: orden_estudio
--   ->  consultas, tipo_orden_estudio
CREATE TABLE orden_estudio (
    id_orden_estudio SERIAL,
    id_tipo_orden_estudio integer NOT NULL,
    fecha_emision date NOT NULL DEFAULT CURRENT_DATE,
    observacion text,
    estado character varying(20) DEFAULT 'pendiente'::character varying,
    id_consulta integer,
    CONSTRAINT orden_estudio_pkey PRIMARY KEY (id_orden_estudio),
    CONSTRAINT fk_orden_estudio_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT orden_estudio_id_tipo_orden_estudio_fkey FOREIGN KEY (id_tipo_orden_estudio) REFERENCES tipo_orden_estudio(id_tipo_orden_estudio) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla: recetas
--   ->  consultas
--   <-  receta_detalle
CREATE TABLE recetas (
    id_receta SERIAL,
    id_consulta integer NOT NULL,
    fecha_emision date NOT NULL DEFAULT CURRENT_DATE,
    observaciones text,
    CONSTRAINT pk_recetas PRIMARY KEY (id_receta),
    CONSTRAINT uix_recetas_consulta UNIQUE (id_consulta),
    CONSTRAINT fk_recetas_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta)
);

-- Tabla: receta_detalle
--   ->  medicamentos, recetas
CREATE TABLE receta_detalle (
    id_receta_detalle SERIAL,
    id_receta integer NOT NULL,
    id_medicamento integer NOT NULL,
    dosis character varying(100) NOT NULL,
    frecuencia character varying(100) NOT NULL,
    duracion character varying(100),
    indicaciones text,
    cantidad integer DEFAULT 1,
    CONSTRAINT pk_receta_detalle PRIMARY KEY (id_receta_detalle),
    CONSTRAINT fk_receta_detalle_medicamento FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento),
    CONSTRAINT fk_receta_detalle_receta FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

-- Tabla: justificativos
--   ->  consultas
CREATE TABLE justificativos (
    id_justificativo SERIAL,
    id_consulta integer NOT NULL,
    fecha_emision date NOT NULL DEFAULT CURRENT_DATE,
    motivo text NOT NULL,
    dias_reposo integer,
    fecha_desde date,
    fecha_hasta date,
    observaciones text,
    CONSTRAINT pk_justificativos PRIMARY KEY (id_justificativo),
    CONSTRAINT uix_justificativos_consulta UNIQUE (id_consulta),
    CONSTRAINT fk_justificativos_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta)
);

-- Tabla: consulta_insumos
--   ->  consultas, insumos
CREATE TABLE consulta_insumos (
    id_consulta_insumo SERIAL,
    id_consulta integer NOT NULL,
    id_insumo integer NOT NULL,
    cantidad numeric(10,2) NOT NULL DEFAULT 1,
    observacion text,
    CONSTRAINT pk_consulta_insumos PRIMARY KEY (id_consulta_insumo),
    CONSTRAINT fk_consulta_insumos_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT fk_consulta_insumos_insumo FOREIGN KEY (id_insumo) REFERENCES insumos(id_insumo)
);

-- Tabla: stock_insumos
--   ->  consultas, insumos, usuarios
CREATE TABLE stock_insumos (
    id_movimiento SERIAL,
    id_insumo integer NOT NULL,
    tipo_movimiento character varying(10) NOT NULL,
    cantidad numeric(10,2) NOT NULL,
    stock_anterior numeric(10,2) NOT NULL,
    stock_nuevo numeric(10,2) NOT NULL,
    motivo character varying(200),
    id_consulta integer,
    id_usuario integer,
    fecha_movimiento timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT stock_insumos_pkey PRIMARY KEY (id_movimiento),
    CONSTRAINT chk_tipo_movimiento CHECK (((tipo_movimiento)::text = ANY ((ARRAY['ENTRADA'::character varying, 'SALIDA'::character varying])::text[]))),
    CONSTRAINT fk_stock_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT fk_stock_insumo FOREIGN KEY (id_insumo) REFERENCES insumos(id_insumo),
    CONSTRAINT fk_stock_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- ============================================================================
--  MODULO: FACTURACION Y CAJA
-- ============================================================================

-- Tabla: datos_emisor
--   <-  facturas
CREATE TABLE datos_emisor (
    id_emisor SERIAL,
    razon_social character varying(200) NOT NULL,
    nombre_fantasia character varying(200),
    ruc character varying(20) NOT NULL,
    timbrado character varying(20) NOT NULL,
    fecha_inicio_vigencia date NOT NULL,
    fecha_fin_vigencia date NOT NULL,
    punto_expedicion character varying(3) NOT NULL DEFAULT '001'::character varying,
    establecimiento character varying(3) NOT NULL DEFAULT '001'::character varying,
    direccion character varying(300),
    telefono character varying(50),
    estado boolean DEFAULT true,
    codigo_control character varying(20),
    modalidad character varying(30) DEFAULT 'Factura Virtual'::character varying,
    CONSTRAINT datos_emisor_pkey PRIMARY KEY (id_emisor)
);

-- Tabla: estados_factura
--   <-  facturas
CREATE TABLE estados_factura (
    id_estado_factura SERIAL,
    descripcion character varying(40) NOT NULL,
    CONSTRAINT estados_factura_pkey PRIMARY KEY (id_estado_factura),
    CONSTRAINT estados_factura_descripcion_key UNIQUE (descripcion)
);

-- Tabla: tipos_comprobante
--   <-  motivos_nota, notas
CREATE TABLE tipos_comprobante (
    id_tipo_comprobante SERIAL,
    descripcion character varying(60) NOT NULL,
    prefijo character varying(5),
    CONSTRAINT tipos_comprobante_pkey PRIMARY KEY (id_tipo_comprobante),
    CONSTRAINT tipos_comprobante_descripcion_key UNIQUE (descripcion)
);

-- Tabla: formas_cobro
--   <-  cobranzas
CREATE TABLE formas_cobro (
    id_forma_cobro SERIAL,
    descripcion character varying(60) NOT NULL,
    requiere_referencia boolean DEFAULT false,
    CONSTRAINT formas_cobro_pkey PRIMARY KEY (id_forma_cobro),
    CONSTRAINT formas_cobro_descripcion_key UNIQUE (descripcion)
);

-- Tabla: cajas
--   ->  usuarios
--   <-  cobranzas, facturas
CREATE TABLE cajas (
    id_caja SERIAL,
    id_usuario integer NOT NULL,
    fecha_apertura timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto_apertura numeric(12,2) NOT NULL DEFAULT 0,
    fecha_cierre timestamp without time zone,
    monto_cierre_declarado numeric(12,2),
    monto_cierre_sistema numeric(12,2),
    diferencia numeric(12,2),
    observaciones_cierre text,
    estado character varying(20) NOT NULL DEFAULT 'Abierta'::character varying,
    CONSTRAINT pk_cajas PRIMARY KEY (id_caja),
    CONSTRAINT fk_caja_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla: facturas
--   ->  cajas, consultas, datos_emisor, estados_factura, funcionarios
--   <-  cobranzas, factura_detalle, notas
CREATE TABLE facturas (
    id_factura SERIAL,
    id_consulta integer NOT NULL,
    id_caja integer,
    id_emisor integer NOT NULL,
    establecimiento character varying(3) NOT NULL,
    punto_expedicion character varying(3) NOT NULL,
    numero_factura character varying(7) NOT NULL,
    timbrado character varying(20) NOT NULL,
    ruc_ci_cliente character varying(20) NOT NULL,
    nombre_cliente character varying(300) NOT NULL,
    fecha_emision date NOT NULL DEFAULT CURRENT_DATE,
    condicion_venta character varying(20) NOT NULL DEFAULT 'Contado'::character varying,
    numero_nota_remision character varying(20),
    subtotal_exento numeric(12,2) NOT NULL DEFAULT 0,
    subtotal_5 numeric(12,2) NOT NULL DEFAULT 0,
    subtotal_10 numeric(12,2) NOT NULL DEFAULT 0,
    iva_5 numeric(12,2) NOT NULL DEFAULT 0,
    iva_10 numeric(12,2) NOT NULL DEFAULT 0,
    total numeric(12,2) NOT NULL DEFAULT 0,
    saldo_pendiente numeric(12,2) NOT NULL DEFAULT 0,
    id_estado_factura integer NOT NULL,
    observaciones text,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_funcionario integer,
    CONSTRAINT pk_facturas PRIMARY KEY (id_factura),
    CONSTRAINT uix_factura_consulta UNIQUE (id_consulta),
    CONSTRAINT uix_factura_numeracion UNIQUE (establecimiento, punto_expedicion, numero_factura),
    CONSTRAINT fk_factura_caja FOREIGN KEY (id_caja) REFERENCES cajas(id_caja),
    CONSTRAINT fk_factura_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT fk_factura_emisor FOREIGN KEY (id_emisor) REFERENCES datos_emisor(id_emisor),
    CONSTRAINT fk_factura_estado FOREIGN KEY (id_estado_factura) REFERENCES estados_factura(id_estado_factura),
    CONSTRAINT fk_factura_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);

-- Tabla: factura_detalle
--   ->  facturas, servicios_facturables, tipos_iva
CREATE TABLE factura_detalle (
    id_factura_detalle SERIAL,
    id_factura integer NOT NULL,
    id_servicio integer,
    descripcion character varying(300) NOT NULL,
    cantidad numeric(10,2) NOT NULL DEFAULT 1,
    precio_unitario numeric(12,2) NOT NULL,
    id_tipo_iva integer NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    CONSTRAINT pk_factura_detalle PRIMARY KEY (id_factura_detalle),
    CONSTRAINT fk_detalle_factura FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
    CONSTRAINT fk_detalle_iva FOREIGN KEY (id_tipo_iva) REFERENCES tipos_iva(id_tipo_iva),
    CONSTRAINT fk_detalle_servicio FOREIGN KEY (id_servicio) REFERENCES servicios_facturables(id_servicio)
);

-- Tabla: cobranzas
--   ->  cajas, facturas, formas_cobro
CREATE TABLE cobranzas (
    id_cobranza SERIAL,
    id_factura integer NOT NULL,
    id_caja integer NOT NULL,
    id_forma_cobro integer NOT NULL,
    monto numeric(12,2) NOT NULL,
    referencia character varying(100),
    banco character varying(100),
    fecha_cobro timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    numero_recibo character varying(20) NOT NULL,
    observaciones text,
    CONSTRAINT pk_cobranzas PRIMARY KEY (id_cobranza),
    CONSTRAINT fk_cobranza_caja FOREIGN KEY (id_caja) REFERENCES cajas(id_caja),
    CONSTRAINT fk_cobranza_factura FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
    CONSTRAINT fk_cobranza_forma FOREIGN KEY (id_forma_cobro) REFERENCES formas_cobro(id_forma_cobro)
);

-- Tabla: motivos_nota
--   ->  tipos_comprobante
--   <-  notas
CREATE TABLE motivos_nota (
    id_motivo_nota SERIAL,
    descripcion character varying(150) NOT NULL,
    id_tipo_comprobante integer NOT NULL,
    CONSTRAINT motivos_nota_pkey PRIMARY KEY (id_motivo_nota),
    CONSTRAINT fk_motivo_tipo FOREIGN KEY (id_tipo_comprobante) REFERENCES tipos_comprobante(id_tipo_comprobante)
);

-- Tabla: notas
--   ->  facturas, motivos_nota, tipos_comprobante, usuarios
CREATE TABLE notas (
    id_nota SERIAL,
    id_tipo_comprobante integer NOT NULL,
    id_factura integer NOT NULL,
    id_motivo_nota integer NOT NULL,
    establecimiento character varying(3) NOT NULL,
    punto_expedicion character varying(3) NOT NULL,
    numero_nota character varying(7) NOT NULL,
    timbrado character varying(20) NOT NULL,
    fecha_emision date NOT NULL DEFAULT CURRENT_DATE,
    monto numeric(12,2) NOT NULL,
    detalle_motivo text,
    id_usuario integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_notas PRIMARY KEY (id_nota),
    CONSTRAINT uix_nota_numeracion UNIQUE (establecimiento, punto_expedicion, numero_nota, id_tipo_comprobante),
    CONSTRAINT fk_nota_factura FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
    CONSTRAINT fk_nota_motivo FOREIGN KEY (id_motivo_nota) REFERENCES motivos_nota(id_motivo_nota),
    CONSTRAINT fk_nota_tipo FOREIGN KEY (id_tipo_comprobante) REFERENCES tipos_comprobante(id_tipo_comprobante),
    CONSTRAINT fk_nota_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- ============================================================================
--  INDICES ADICIONALES
-- ============================================================================
CREATE INDEX ix_auditoria_accesos_fecha ON auditoria_accesos USING btree (fecha);
CREATE INDEX idx_cajas_usuario_estado ON cajas USING btree (id_usuario, estado);
CREATE INDEX idx_cobranzas_caja ON cobranzas USING btree (id_caja);
CREATE INDEX idx_cobranzas_factura ON cobranzas USING btree (id_factura);
CREATE INDEX idx_consulta_diagnosticos_consulta ON consulta_diagnosticos USING btree (id_consulta);
CREATE INDEX idx_cord_consulta ON consulta_ordenes USING btree (id_consulta);
CREATE INDEX idx_cp_consulta ON consulta_procedimientos USING btree (id_consulta);
CREATE INDEX idx_consultas_cita ON consultas USING btree (id_cita);
CREATE INDEX idx_consultas_fecha ON consultas USING btree (fecha_consulta);
CREATE UNIQUE INDEX uix_consultas_cita ON consultas USING btree (id_cita);
CREATE INDEX idx_facturas_estado ON facturas USING btree (id_estado_factura);
CREATE INDEX idx_facturas_fecha ON facturas USING btree (fecha_emision);
CREATE INDEX idx_ficha_antecedentes_ficha ON ficha_antecedentes_familiares USING btree (id_ficha);
CREATE INDEX idx_ficha_medicacion_ficha ON ficha_medicacion_habitual USING btree (id_ficha);
CREATE INDEX idx_stock_consulta ON stock_insumos USING btree (id_consulta);
CREATE INDEX idx_stock_fecha ON stock_insumos USING btree (fecha_movimiento DESC);
CREATE INDEX idx_stock_insumo ON stock_insumos USING btree (id_insumo);

-- ============================================================================
--  FUNCIONES (control de stock de insumos)
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_descontar_stock(p_id_insumo integer, p_cantidad numeric, p_id_consulta integer, p_id_usuario integer, p_motivo character varying DEFAULT 'Consulta'::character varying)
 RETURNS boolean
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_stock_anterior numeric;
    v_stock_nuevo    numeric;
BEGIN
    SELECT stock_actual INTO v_stock_anterior
    FROM insumos
    WHERE id_insumo = p_id_insumo
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Insumo % no encontrado', p_id_insumo;
    END IF;

    v_stock_nuevo := v_stock_anterior - p_cantidad;

    -- Permitir stock negativo con advertencia (no bloqueamos la consulta)
    UPDATE insumos
    SET stock_actual = v_stock_nuevo
    WHERE id_insumo = p_id_insumo;

    INSERT INTO stock_insumos (
        id_insumo, tipo_movimiento, cantidad,
        stock_anterior, stock_nuevo,
        motivo, id_consulta, id_usuario
    ) VALUES (
        p_id_insumo, 'SALIDA', p_cantidad,
        v_stock_anterior, v_stock_nuevo,
        p_motivo || ' #' || COALESCE(p_id_consulta::text, '?'),
        p_id_consulta, p_id_usuario
    );

    RETURN TRUE;
END;
$function$;

CREATE OR REPLACE FUNCTION fn_reponer_stock(p_id_insumo integer, p_cantidad numeric, p_id_usuario integer, p_motivo character varying DEFAULT 'Reposición'::character varying)
 RETURNS boolean
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_stock_anterior numeric;
    v_stock_nuevo    numeric;
BEGIN
    SELECT stock_actual INTO v_stock_anterior
    FROM insumos
    WHERE id_insumo = p_id_insumo
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Insumo % no encontrado', p_id_insumo;
    END IF;

    v_stock_nuevo := v_stock_anterior + p_cantidad;

    UPDATE insumos
    SET stock_actual = v_stock_nuevo
    WHERE id_insumo = p_id_insumo;

    INSERT INTO stock_insumos (
        id_insumo, tipo_movimiento, cantidad,
        stock_anterior, stock_nuevo,
        motivo, id_consulta, id_usuario
    ) VALUES (
        p_id_insumo, 'ENTRADA', p_cantidad,
        v_stock_anterior, v_stock_nuevo,
        p_motivo, NULL, p_id_usuario
    );

    RETURN TRUE;
END;
$function$;

-- ============================================================================
--  VISTAS (solo las que usa el sistema)
-- ============================================================================

CREATE VIEW vw_funcionarios AS
 SELECT f.id_funcionario,
    (p.nombre::text || ' '::text) || p.apellido::text AS nombre_completo,
    p.cedula,
    u.nickname,
    r.descripcion AS rol,
    f.cargo,
    c.nombre AS consultorio,
    f.fecha_ingreso,
    f.estado
   FROM funcionarios f
     JOIN personas p ON p.id_persona = f.id_persona
     JOIN usuarios u ON u.id_usuario = f.id_usuario
     JOIN roles r ON r.id_rol = f.id_rol
     JOIN consultorio c ON c.id_consultorio = f.id_consultorio;

CREATE VIEW vw_trazabilidad AS
 WITH mov AS (
         SELECT 'Agenda'::text AS proceso,
            am.id_agenda_medica AS id_registro,
            am.fecha_registro,
            (('Prof. '::text || pm.nombre::text) || ' '::text) || pm.apellido::text AS paciente,
            am.id_funcionario
           FROM agenda_medicas am
             JOIN medicos m ON m.id_medico = am.id_medico
             JOIN personas pm ON pm.id_persona = m.id_persona
        UNION ALL
         SELECT 'Cita'::text,
            c.id_cita,
            c.fecha_registro,
            (p.nombre::text || ' '::text) || p.apellido::text,
            c.id_funcionario
           FROM citas c
             JOIN pacientes pa ON pa.id_paciente = c.id_paciente
             JOIN personas p ON p.id_persona = pa.id_persona
        UNION ALL
         SELECT 'Consulta'::text,
            co.id_consulta,
            co.fecha_consulta,
            (p.nombre::text || ' '::text) || p.apellido::text,
            co.id_funcionario
           FROM consultas co
             JOIN citas c ON c.id_cita = co.id_cita
             JOIN pacientes pa ON pa.id_paciente = c.id_paciente
             JOIN personas p ON p.id_persona = pa.id_persona
        UNION ALL
         SELECT 'Factura'::text,
            f.id_factura,
            f.fecha_creacion,
            f.nombre_cliente,
            f.id_funcionario
           FROM facturas f
        UNION ALL
         SELECT 'Respuesta aviso'::text,
            ar.id_aviso,
            ar.fecha_respuesta,
            (p.nombre::text || ' '::text) || p.apellido::text,
            ar.id_funcionario
           FROM avisos_recordatorios ar
             JOIN citas c ON c.id_cita = ar.id_cita
             JOIN pacientes pa ON pa.id_paciente = c.id_paciente
             JOIN personas p ON p.id_persona = pa.id_persona
          WHERE ar.respuesta IS NOT NULL
        )
 SELECT mov.proceso,
    mov.id_registro,
    mov.fecha_registro,
    mov.paciente,
    vf.nombre_completo AS funcionario,
    vf.rol AS rol_funcionario,
    vf.consultorio
   FROM mov
     LEFT JOIN vw_funcionarios vf ON vf.id_funcionario = mov.id_funcionario;

CREATE VIEW vw_alerta_stock AS
 SELECT i.id_insumo,
    i.nombre,
    i.unidad_medida,
    i.stock_actual,
    i.stock_minimo,
    i.precio_venta,
    t.descripcion AS tipo_iva,
    t.porcentaje AS porcentaje_iva,
        CASE
            WHEN i.stock_actual = 0::numeric THEN 'SIN STOCK'::text
            WHEN i.stock_actual <= i.stock_minimo THEN 'STOCK MÍNIMO'::text
            ELSE 'OK'::text
        END AS estado_stock
   FROM insumos i
     LEFT JOIN tipos_iva t ON t.id_tipo_iva = i.id_tipo_iva
  WHERE i.estado = true
  ORDER BY (
        CASE
            WHEN i.stock_actual = 0::numeric THEN 1
            WHEN i.stock_actual <= i.stock_minimo THEN 2
            ELSE 3
        END), i.nombre;

CREATE VIEW vw_historial_stock AS
 SELECT sm.id_movimiento,
    i.nombre AS insumo,
    i.unidad_medida,
    sm.tipo_movimiento,
    sm.cantidad,
    sm.stock_anterior,
    sm.stock_nuevo,
    sm.motivo,
    sm.fecha_movimiento,
    u.nickname AS usuario,
    COALESCE('Consulta #'::text || sm.id_consulta::text, '—'::text) AS consulta_ref
   FROM stock_insumos sm
     JOIN insumos i ON i.id_insumo = sm.id_insumo
     LEFT JOIN usuarios u ON u.id_usuario = sm.id_usuario
  ORDER BY sm.fecha_movimiento DESC;

CREATE VIEW vw_consultas_sin_facturar AS
 SELECT co.id_consulta,
    co.fecha_consulta,
    co.motivo_consulta,
    (p.nombre::text || ' '::text) || p.apellido::text AS paciente,
    p.cedula,
    (pm.nombre::text || ' '::text) || pm.apellido::text AS medico,
    e.descripcion AS especialidad,
    ( SELECT count(*) AS count
           FROM consulta_procedimientos cp
          WHERE cp.id_consulta = co.id_consulta) AS total_procedimientos,
    ( SELECT count(*) AS count
           FROM consulta_insumos ci_1
             JOIN insumos i ON i.id_insumo = ci_1.id_insumo
          WHERE ci_1.id_consulta = co.id_consulta AND i.precio_venta > 0::numeric) AS total_insumos
   FROM consultas co
     JOIN citas ci ON ci.id_cita = co.id_cita
     JOIN pacientes pa ON pa.id_paciente = ci.id_paciente
     JOIN personas p ON p.id_persona = pa.id_persona
     JOIN disponibilidad_horaria dh ON dh.id_disponibilidad_horaria = ci.id_disponibilidad_horaria
     JOIN agenda_medicas am ON am.id_agenda_medica = dh.id_agenda_medica
     JOIN medicos m ON m.id_medico = am.id_medico
     JOIN personas pm ON pm.id_persona = m.id_persona
     JOIN especialidades e ON e.id_especialidad = am.id_especialidad
  WHERE NOT (co.id_consulta IN ( SELECT facturas.id_consulta
           FROM facturas));

CREATE VIEW vw_items_factura_por_consulta AS
 SELECT co.id_consulta,
    'procedimiento'::text AS tipo,
    cp.id_consulta_procedimiento AS id_item,
    sf.id_servicio AS id_referencia,
    sf.descripcion,
    cp.cantidad,
    sf.precio_unitario,
    round(cp.cantidad * sf.precio_unitario, 2) AS subtotal,
    sf.id_tipo_iva,
    ti.porcentaje AS pct_iva,
    cp.observacion
   FROM consulta_procedimientos cp
     JOIN consultas co ON co.id_consulta = cp.id_consulta
     JOIN servicios_facturables sf ON sf.id_servicio = cp.id_servicio
     JOIN tipos_iva ti ON ti.id_tipo_iva = sf.id_tipo_iva
UNION ALL
 SELECT co.id_consulta,
    'insumo'::text AS tipo,
    ci.id_consulta_insumo AS id_item,
    i.id_insumo AS id_referencia,
    ((i.nombre::text || ' ('::text) || i.unidad_medida::text) || ')'::text AS descripcion,
    ci.cantidad,
    i.precio_venta AS precio_unitario,
    round(ci.cantidad * i.precio_venta, 2) AS subtotal,
    i.id_tipo_iva,
    COALESCE(ti.porcentaje, 0::numeric) AS pct_iva,
    ci.observacion
   FROM consulta_insumos ci
     JOIN consultas co ON co.id_consulta = ci.id_consulta
     JOIN insumos i ON i.id_insumo = ci.id_insumo
     LEFT JOIN tipos_iva ti ON ti.id_tipo_iva = i.id_tipo_iva
  WHERE i.precio_venta > 0::numeric;

CREATE VIEW vw_cuentas_a_cobrar AS
 SELECT f.id_factura,
    (((f.establecimiento::text || '-'::text) || f.punto_expedicion::text) || '-'::text) || f.numero_factura::text AS nro_factura,
    f.fecha_emision,
    f.nombre_cliente,
    f.ruc_ci_cliente,
    f.total,
    f.saldo_pendiente,
    ef.descripcion AS estado_factura
   FROM facturas f
     JOIN estados_factura ef ON ef.id_estado_factura = f.id_estado_factura
  WHERE f.saldo_pendiente > 0::numeric AND ef.descripcion::text <> 'Anulada'::text
  ORDER BY f.fecha_emision;

CREATE VIEW vw_informe_servicios AS
 SELECT fd.id_servicio,
    s.descripcion AS servicio,
    count(*) AS cantidad_facturada,
    sum(fd.subtotal) AS monto_total,
    f.fecha_emision
   FROM factura_detalle fd
     JOIN facturas f ON f.id_factura = fd.id_factura
     LEFT JOIN servicios_facturables s ON s.id_servicio = fd.id_servicio
  WHERE f.id_estado_factura <> (( SELECT estados_factura.id_estado_factura
           FROM estados_factura
          WHERE estados_factura.descripcion::text = 'Anulada'::text))
  GROUP BY fd.id_servicio, s.descripcion, f.fecha_emision
  ORDER BY f.fecha_emision DESC;

CREATE VIEW vw_arqueo_caja AS
 SELECT c.id_caja,
    u.nickname AS usuario,
    c.fecha_apertura,
    c.fecha_cierre,
    c.monto_apertura,
    COALESCE(sum(
        CASE
            WHEN fc.descripcion::text = 'Efectivo'::text THEN cob.monto
            ELSE 0::numeric
        END), 0::numeric) AS total_efectivo,
    COALESCE(sum(
        CASE
            WHEN fc.descripcion::text = 'Cheque'::text THEN cob.monto
            ELSE 0::numeric
        END), 0::numeric) AS total_cheque,
    COALESCE(sum(
        CASE
            WHEN fc.descripcion::text = 'Tarjeta de Crédito'::text THEN cob.monto
            ELSE 0::numeric
        END), 0::numeric) AS total_tarjeta_credito,
    COALESCE(sum(
        CASE
            WHEN fc.descripcion::text = 'Tarjeta de Débito'::text THEN cob.monto
            ELSE 0::numeric
        END), 0::numeric) AS total_tarjeta_debito,
    COALESCE(sum(cob.monto), 0::numeric) AS total_cobrado,
    c.monto_apertura + COALESCE(sum(
        CASE
            WHEN fc.descripcion::text = 'Efectivo'::text THEN cob.monto
            ELSE 0::numeric
        END), 0::numeric) AS efectivo_esperado,
    c.monto_cierre_declarado,
    c.diferencia,
    c.estado
   FROM cajas c
     JOIN usuarios u ON u.id_usuario = c.id_usuario
     LEFT JOIN cobranzas cob ON cob.id_caja = c.id_caja
     LEFT JOIN formas_cobro fc ON fc.id_forma_cobro = cob.id_forma_cobro
  GROUP BY c.id_caja, u.nickname, c.fecha_apertura, c.fecha_cierre, c.monto_apertura, c.monto_cierre_declarado, c.diferencia, c.estado
  ORDER BY c.fecha_apertura DESC;

CREATE VIEW vw_recaudacion_depositar AS
 SELECT c.id_caja,
    u.nickname AS usuario,
    c.fecha_cierre,
    COALESCE(sum(
        CASE
            WHEN fc.descripcion::text = 'Efectivo'::text THEN cob.monto
            ELSE 0::numeric
        END), 0::numeric) AS efectivo_a_depositar
   FROM cajas c
     JOIN usuarios u ON u.id_usuario = c.id_usuario
     LEFT JOIN cobranzas cob ON cob.id_caja = c.id_caja
     LEFT JOIN formas_cobro fc ON fc.id_forma_cobro = cob.id_forma_cobro
  WHERE c.estado::text = 'Cerrada'::text
  GROUP BY c.id_caja, u.nickname, c.fecha_cierre
 HAVING COALESCE(sum(
        CASE
            WHEN fc.descripcion::text = 'Efectivo'::text THEN cob.monto
            ELSE 0::numeric
        END), 0::numeric) > 0::numeric
  ORDER BY c.fecha_cierre DESC;

-- ============================================================================
--  TRIGGERS: el sistema no tiene triggers definidos actualmente.
-- ============================================================================
