-- ============================================================================
-- ESTRUCTURA DE BASE DE DATOS POSTGRESQL - SISTEMA CIN
-- ============================================================================
-- Este archivo contiene:
-- 1. Ejemplo de estructura de tabla referencial (ciudades)
-- 2. Scripts CREATE TABLE para tablas faltantes
-- 3. Scripts INSERT para datos iniciales
-- ============================================================================

-- ============================================================================
-- EJEMPLO DE ESTRUCTURA: TABLA CIUDADES (Referencial Simple)
-- ============================================================================
-- Esta es la estructura base que sigue tu sistema para tablas referenciales

CREATE TABLE IF NOT EXISTS ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    des_ciudad VARCHAR(100) NOT NULL UNIQUE,
    est_ciudad BOOLEAN NOT NULL DEFAULT TRUE
);

-- Ejemplo de INSERT para ciudades
INSERT INTO ciudades (des_ciudad, est_ciudad) VALUES
    ('ASUNCIÓN', TRUE),
    ('CIUDAD DEL ESTE', TRUE),
    ('SAN LORENZO', TRUE)
ON CONFLICT (des_ciudad) DO NOTHING;

-- ============================================================================
-- TABLAS FALTANTES PARA COMPLETAR LOS REQUERIMIENTOS
-- ============================================================================

-- ============================================================================
-- 1. PRESUPUESTOS (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS presupuestos (
    id_presupuesto SERIAL PRIMARY KEY,
    id_consulta INTEGER,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    presupuesto_numero VARCHAR(50) UNIQUE NOT NULL,
    presupuesto_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    presupuesto_validez_dias INTEGER DEFAULT 30,
    presupuesto_estado VARCHAR(20) DEFAULT 'PENDIENTE', -- PENDIENTE, APROBADO, RECHAZADO, VENCIDO
    presupuesto_subtotal INTEGER DEFAULT 0,
    presupuesto_descuento INTEGER DEFAULT 0,
    presupuesto_total INTEGER DEFAULT 0,
    presupuesto_observaciones TEXT,
    est_presupuesto CHAR(1) DEFAULT 'A', -- A=Activo, I=Inactivo
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de presupuesto (servicios/procedimientos incluidos)
CREATE TABLE IF NOT EXISTS presupuesto_detalle (
    id_presupuesto_detalle SERIAL PRIMARY KEY,
    id_presupuesto INTEGER NOT NULL,
    id_tipo_procedimiento INTEGER,
    des_item VARCHAR(255) NOT NULL,
    cantidad INTEGER DEFAULT 1,
    precio_unitario INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,
    observaciones TEXT,
    
    FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id_presupuesto) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_procedimiento) REFERENCES tipos_procedimientos(id_tipo_procedimiento) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Índices para presupuestos
CREATE INDEX IF NOT EXISTS idx_presupuesto_paciente ON presupuestos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_presupuesto_consulta ON presupuestos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_presupuesto_fecha ON presupuestos(presupuesto_fecha);
CREATE INDEX IF NOT EXISTS idx_presupuesto_numero ON presupuestos(presupuesto_numero);

-- ============================================================================
-- 2. ÓRDENES DE ESTUDIOS (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ordenes_estudios (
    id_orden_estudio SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    orden_numero VARCHAR(50) UNIQUE NOT NULL,
    orden_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    orden_tipo VARCHAR(50) NOT NULL, -- LABORATORIO, IMAGENOLOGIA, OTROS
    orden_estado VARCHAR(20) DEFAULT 'PENDIENTE', -- PENDIENTE, REALIZADO, CANCELADO
    orden_observaciones TEXT,
    orden_indicaciones TEXT,
    est_orden CHAR(1) DEFAULT 'A', -- A=Activo, I=Inactivo
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de estudios solicitados en la orden
CREATE TABLE IF NOT EXISTS orden_estudio_detalle (
    id_orden_detalle SERIAL PRIMARY KEY,
    id_orden_estudio INTEGER NOT NULL,
    id_tipo_estudio INTEGER,
    id_tipo_analisis INTEGER,
    des_estudio VARCHAR(255) NOT NULL,
    estudio_estado VARCHAR(20) DEFAULT 'PENDIENTE', -- PENDIENTE, REALIZADO, CANCELADO
    estudio_resultado TEXT,
    estudio_fecha_realizacion DATE,
    observaciones TEXT,
    
    FOREIGN KEY (id_orden_estudio) REFERENCES ordenes_estudios(id_orden_estudio) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_estudio) REFERENCES tipos_estudios(id_tipo_estudio) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_analisis) REFERENCES tipos_analisis(id_tipo_analisis) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Índices para órdenes de estudios
CREATE INDEX IF NOT EXISTS idx_orden_paciente ON ordenes_estudios(id_paciente);
CREATE INDEX IF NOT EXISTS idx_orden_consulta ON ordenes_estudios(id_consulta);
CREATE INDEX IF NOT EXISTS idx_orden_fecha ON ordenes_estudios(orden_fecha);
CREATE INDEX IF NOT EXISTS idx_orden_numero ON ordenes_estudios(orden_numero);

-- ============================================================================
-- 3. RECETAS E INDICACIONES (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS recetas (
    id_receta SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    receta_numero VARCHAR(50) UNIQUE NOT NULL,
    receta_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    receta_validez_dias INTEGER DEFAULT 30,
    receta_observaciones TEXT,
    receta_indicaciones_generales TEXT,
    est_receta CHAR(1) DEFAULT 'A', -- A=Activo, I=Inactivo
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de medicamentos en la receta
CREATE TABLE IF NOT EXISTS receta_detalle (
    id_receta_detalle SERIAL PRIMARY KEY,
    id_receta INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    medicamento_dosis VARCHAR(100),
    medicamento_frecuencia VARCHAR(100) NOT NULL, -- Ej: "Cada 8 horas", "2 veces al día"
    medicamento_duracion VARCHAR(100) NOT NULL, -- Ej: "7 días", "Hasta terminar"
    medicamento_cantidad INTEGER,
    medicamento_indicaciones TEXT, -- Instrucciones específicas de administración
    medicamento_posologia TEXT, -- Cómo tomar el medicamento
    est_receta_detalle CHAR(1) DEFAULT 'A',
    
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Índices para recetas
CREATE INDEX IF NOT EXISTS idx_receta_paciente ON recetas(id_paciente);
CREATE INDEX IF NOT EXISTS idx_receta_consulta ON recetas(id_consulta);
CREATE INDEX IF NOT EXISTS idx_receta_fecha ON recetas(receta_fecha);
CREATE INDEX IF NOT EXISTS idx_receta_numero ON recetas(receta_numero);

-- ============================================================================
-- 4. CERTIFICADOS MÉDICOS (Módulo Consultorio)
-- ============================================================================

-- Tabla referencial: Tipos de Certificados Médicos
CREATE TABLE IF NOT EXISTS tipos_certificados_medicos (
    id_tipo_certificado SERIAL PRIMARY KEY,
    des_tipo_certificado VARCHAR(100) NOT NULL UNIQUE,
    est_tipo_certificado CHAR(1) DEFAULT 'A', -- A=Activo, I=Inactivo
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- Tabla principal: Certificados Médicos
CREATE TABLE IF NOT EXISTS certificados_medicos (
    id_certificado SERIAL PRIMARY KEY,
    id_consulta INTEGER,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    certificado_numero VARCHAR(50) UNIQUE NOT NULL,
    certificado_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    id_tipo_certificado INTEGER NOT NULL, -- FK a tipos_certificados_medicos
    certificado_dias_reposo INTEGER,
    certificado_desde_fecha DATE,
    certificado_hasta_fecha DATE,
    certificado_motivo TEXT NOT NULL,
    certificado_diagnostico TEXT,
    certificado_recomendaciones TEXT,
    certificado_estado VARCHAR(20) DEFAULT 'VIGENTE', -- VIGENTE, VENCIDO, ANULADO
    est_certificado CHAR(1) DEFAULT 'A', -- A=Activo, I=Inactivo
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_certificado) REFERENCES tipos_certificados_medicos(id_tipo_certificado)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Índices para certificados
CREATE INDEX IF NOT EXISTS idx_certificado_paciente ON certificados_medicos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_certificado_consulta ON certificados_medicos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_certificado_fecha ON certificados_medicos(certificado_fecha);
CREATE INDEX IF NOT EXISTS idx_certificado_numero ON certificados_medicos(certificado_numero);
CREATE INDEX IF NOT EXISTS idx_certificado_tipo ON certificados_medicos(id_tipo_certificado);

-- ============================================================================
-- 5. INSUMOS DE PROCEDIMIENTOS (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS insumos (
    id_insumo SERIAL PRIMARY KEY,
    des_insumo VARCHAR(255) NOT NULL UNIQUE,
    insumo_unidad_medida VARCHAR(20) DEFAULT 'UNIDAD', -- UNIDAD, CAJA, PAQUETE, etc.
    insumo_stock_actual INTEGER DEFAULT 0,
    insumo_stock_minimo INTEGER DEFAULT 0,
    insumo_precio_unitario INTEGER,
    est_insumo CHAR(1) DEFAULT 'A', -- A=Activo, I=Inactivo
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA'
);

-- Registro de insumos utilizados en procedimientos
CREATE TABLE IF NOT EXISTS registro_insumos (
    id_registro_insumo SERIAL PRIMARY KEY,
    id_registro_procedimiento INTEGER NOT NULL,
    id_insumo INTEGER NOT NULL,
    insumo_cantidad INTEGER NOT NULL DEFAULT 1,
    insumo_costo_unitario INTEGER,
    insumo_costo_total INTEGER,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_registro_procedimiento) REFERENCES registro_procedimientos(id_registro_procedimiento) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_insumo) REFERENCES insumos(id_insumo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Índices para insumos
CREATE INDEX IF NOT EXISTS idx_registro_insumo_procedimiento ON registro_insumos(id_registro_procedimiento);
CREATE INDEX IF NOT EXISTS idx_registro_insumo_insumo ON registro_insumos(id_insumo);

-- ============================================================================
-- 6. INFORMES DE AGENDAMIENTO (Módulo Agenda Médica)
-- ============================================================================
CREATE TABLE IF NOT EXISTS informes_agendamiento (
    id_informe_agendamiento SERIAL PRIMARY KEY,
    informe_tipo VARCHAR(50) NOT NULL, -- DIARIO, SEMANAL, MENSUAL, ANUAL, PERSONALIZADO
    informe_fecha_desde DATE NOT NULL,
    informe_fecha_hasta DATE NOT NULL,
    id_especialista INTEGER,
    id_especialidad INTEGER,
    informe_parametros JSONB, -- Parámetros adicionales del informe en formato JSON
    informe_generado BOOLEAN DEFAULT FALSE,
    informe_fecha_generacion TIMESTAMP,
    usuario_generacion VARCHAR(50),
    est_informe CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Índices para informes de agendamiento
CREATE INDEX IF NOT EXISTS idx_informe_agendamiento_fechas ON informes_agendamiento(informe_fecha_desde, informe_fecha_hasta);
CREATE INDEX IF NOT EXISTS idx_informe_agendamiento_especialista ON informes_agendamiento(id_especialista);

-- ============================================================================
-- 7. INFORMES DE CONSULTORIO (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS informes_consultorio (
    id_informe_consultorio SERIAL PRIMARY KEY,
    informe_tipo VARCHAR(50) NOT NULL, -- CONSULTAS, DIAGNOSTICOS, TRATAMIENTOS, PROCEDIMIENTOS, GENERAL
    informe_fecha_desde DATE NOT NULL,
    informe_fecha_hasta DATE NOT NULL,
    id_profesional INTEGER,
    id_especialidad INTEGER,
    informe_parametros JSONB, -- Parámetros adicionales del informe
    informe_generado BOOLEAN DEFAULT FALSE,
    informe_fecha_generacion TIMESTAMP,
    usuario_generacion VARCHAR(50),
    est_informe CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Índices para informes de consultorio
CREATE INDEX IF NOT EXISTS idx_informe_consultorio_fechas ON informes_consultorio(informe_fecha_desde, informe_fecha_hasta);
CREATE INDEX IF NOT EXISTS idx_informe_consultorio_profesional ON informes_consultorio(id_profesional);
CREATE INDEX IF NOT EXISTS idx_informe_consultorio_tipo ON informes_consultorio(informe_tipo);

-- ============================================================================
-- DATOS INICIALES (INSERTS)
-- ============================================================================

-- Insertar algunos insumos básicos (precios en guaraníes paraguayos - sin decimales)
INSERT INTO insumos (des_insumo, insumo_unidad_medida, insumo_stock_actual, insumo_stock_minimo, insumo_precio_unitario, est_insumo) VALUES
    ('ALGODÓN', 'PAQUETE', 50, 10, 15000, 'A'),
    ('GASA ESTERILIZADA', 'PAQUETE', 30, 5, 25000, 'A'),
    ('AGUJAS DESECHABLES', 'CAJA', 20, 5, 45000, 'A'),
    ('JERINGAS DESECHABLES', 'CAJA', 25, 5, 35000, 'A'),
    ('GUANTES QUIRÚRGICOS', 'CAJA', 40, 10, 55000, 'A'),
    ('ALCOHOL', 'LITRO', 15, 3, 12000, 'A')
ON CONFLICT (des_insumo) DO NOTHING;

-- ============================================================================
-- COMENTARIOS Y NOTAS
-- ============================================================================
-- 
-- ESTRUCTURA GENERAL:
-- - IDs: SERIAL PRIMARY KEY (autoincrementales)
-- - Descripciones: VARCHAR con prefijo 'des_'
-- - Estados: CHAR(1) con prefijo 'est_' (A=Activo, I=Inactivo) o VARCHAR para estados complejos
-- - Fechas: DATE para fechas simples, TIMESTAMP para fecha+hora
-- - Auditoría: fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion
-- - Foreign Keys: ON DELETE RESTRICT ON UPDATE CASCADE (para integridad referencial)
-- - Índices: En campos frecuentemente consultados (FOREIGN KEYS, fechas, números únicos)
--
-- CONVENCIONES DE NOMBRES:
-- - Tablas: snake_case en plural (ej: ciudades, presupuestos)
-- - Campos: snake_case con prefijos descriptivos (id_, des_, est_, fecha_, usuario_)
-- - Foreign Keys: id_tabla_referenciada (ej: id_paciente, id_consulta)
--
-- NOTA IMPORTANTE - MONEDA:
-- - Todos los montos monetarios usan INTEGER (no DECIMAL)
-- - La moneda es el Guaraní Paraguayo (PYG) que no tiene decimales
-- - Ejemplo: 150000 (ciento cincuenta mil guaraníes), no 150000.00
--
-- ============================================================================

