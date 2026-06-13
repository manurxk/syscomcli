-- ============================================================================
-- SCRIPT CORRECTIVO — clinicain
-- Ejecutar para corregir diferencias entre SQL scripts y BD real
-- Orden: PASO 1 → PASO 2 → PASO 3 (verificación)
-- ============================================================================

-- ============================================================================
-- PASO 1: Estado EN_CONSULTA (URGENTE — desbloquea botón "Iniciar Consulta")
-- ============================================================================
INSERT INTO estados_citas (est_cita_nombre, est_cita_descripcion, est_cita_color)
VALUES ('EN_CONSULTA', 'Consulta en curso con el especialista', '#fd7e14')
ON CONFLICT (est_cita_nombre) DO NOTHING;

-- ============================================================================
-- PASO 2: Soporte DSM-5 en tabla diagnosticos
-- ============================================================================
ALTER TABLE diagnosticos
ADD COLUMN IF NOT EXISTS diagnostico_codigo_dsm5 VARCHAR(20);

COMMENT ON COLUMN diagnosticos.diagnostico_codigo_dsm5
IS 'Código DSM-5 (Manual Diagnóstico y Estadístico de Trastornos Mentales)';

-- ============================================================================
-- PASO 3: Crear tablas de Fase 8 si no existen
-- (Certficados, Presupuestos, Órdenes de Estudio, Recetas, Insumos)
-- ============================================================================

-- Tipos de certificados
CREATE TABLE IF NOT EXISTS tipos_certificados_medicos (
    id_tipo_certificado SERIAL PRIMARY KEY,
    des_tipo_certificado VARCHAR(100) NOT NULL UNIQUE,
    est_tipo_certificado CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

INSERT INTO tipos_certificados_medicos (des_tipo_certificado, est_tipo_certificado, usuario_creacion) VALUES
    ('Certificado de Aptitud', 'A', 'SISTEMA'),
    ('Certificado de Reposo', 'A', 'SISTEMA'),
    ('Certificado de Tratamiento', 'A', 'SISTEMA'),
    ('Certificado de Asistencia', 'A', 'SISTEMA'),
    ('Certificado de Evaluación', 'A', 'SISTEMA')
ON CONFLICT (des_tipo_certificado) DO NOTHING;

-- Presupuestos
CREATE TABLE IF NOT EXISTS presupuestos (
    id_presupuesto SERIAL PRIMARY KEY,
    id_consulta INTEGER,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    presupuesto_numero VARCHAR(50) UNIQUE NOT NULL,
    presupuesto_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    presupuesto_validez_dias INTEGER DEFAULT 30,
    presupuesto_estado VARCHAR(20) DEFAULT 'PENDIENTE',
    presupuesto_subtotal INTEGER DEFAULT 0,
    presupuesto_descuento INTEGER DEFAULT 0,
    presupuesto_total INTEGER DEFAULT 0,
    presupuesto_observaciones TEXT,
    est_presupuesto CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS presupuesto_detalle (
    id_presupuesto_detalle SERIAL PRIMARY KEY,
    id_presupuesto INTEGER NOT NULL,
    id_tipo_procedimiento INTEGER,
    des_item VARCHAR(255) NOT NULL,
    cantidad INTEGER DEFAULT 1,
    precio_unitario INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id_presupuesto) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_procedimiento) REFERENCES tipos_procedimientos(id_tipo_procedimiento) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Órdenes de estudios
CREATE TABLE IF NOT EXISTS ordenes_estudios (
    id_orden_estudio SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    orden_numero VARCHAR(50) UNIQUE NOT NULL,
    orden_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    orden_tipo VARCHAR(50) NOT NULL,
    orden_estado VARCHAR(20) DEFAULT 'PENDIENTE',
    orden_observaciones TEXT,
    orden_indicaciones TEXT,
    est_orden CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS orden_estudio_detalle (
    id_orden_detalle SERIAL PRIMARY KEY,
    id_orden_estudio INTEGER NOT NULL,
    id_tipo_estudio INTEGER,
    id_tipo_analisis INTEGER,
    des_estudio VARCHAR(255) NOT NULL,
    estudio_estado VARCHAR(20) DEFAULT 'PENDIENTE',
    estudio_resultado TEXT,
    estudio_fecha_realizacion DATE,
    observaciones TEXT,
    FOREIGN KEY (id_orden_estudio) REFERENCES ordenes_estudios(id_orden_estudio) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_estudio) REFERENCES tipos_estudios(id_tipo_estudio) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_analisis) REFERENCES tipos_analisis(id_tipo_analisis) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Recetas
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
    est_receta CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS receta_detalle (
    id_receta_detalle SERIAL PRIMARY KEY,
    id_receta INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    medicamento_dosis VARCHAR(100),
    medicamento_frecuencia VARCHAR(100) NOT NULL,
    medicamento_duracion VARCHAR(100) NOT NULL,
    medicamento_cantidad INTEGER,
    medicamento_indicaciones TEXT,
    medicamento_posologia TEXT,
    est_receta_detalle CHAR(1) DEFAULT 'A',
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Certificados médicos / Justificativos
CREATE TABLE IF NOT EXISTS certificados_medicos (
    id_certificado SERIAL PRIMARY KEY,
    id_consulta INTEGER,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    certificado_numero VARCHAR(50) UNIQUE NOT NULL,
    certificado_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    id_tipo_certificado INTEGER NOT NULL,
    certificado_dias_reposo INTEGER,
    certificado_desde_fecha DATE,
    certificado_hasta_fecha DATE,
    certificado_motivo TEXT NOT NULL,
    certificado_diagnostico TEXT,
    certificado_recomendaciones TEXT,
    certificado_estado VARCHAR(20) DEFAULT 'VIGENTE',
    est_certificado CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_certificado) REFERENCES tipos_certificados_medicos(id_tipo_certificado) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Insumos (catálogo)
CREATE TABLE IF NOT EXISTS insumos (
    id_insumo SERIAL PRIMARY KEY,
    des_insumo VARCHAR(255) NOT NULL UNIQUE,
    insumo_unidad_medida VARCHAR(20) DEFAULT 'UNIDAD',
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    insumo_precio_unitario INTEGER,
    est_insumo CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA'
);

-- Registro de insumos usados en procedimientos
CREATE TABLE IF NOT EXISTS registro_insumos (
    id_registro_insumo SERIAL PRIMARY KEY,
    id_registro_procedimiento INTEGER NOT NULL,
    id_insumo INTEGER NOT NULL,
    insumo_cantidad INTEGER NOT NULL DEFAULT 1,
    insumo_costo_unitario INTEGER,
    insumo_costo_total INTEGER,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_registro_procedimiento) REFERENCES registro_procedimientos(id_registro_procedimiento) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_insumo) REFERENCES insumos(id_insumo) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- PASO 4: Índices de optimización para tablas nuevas
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_presupuesto_paciente ON presupuestos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_presupuesto_consulta ON presupuestos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_ordenes_paciente ON ordenes_estudios(id_paciente);
CREATE INDEX IF NOT EXISTS idx_ordenes_consulta ON ordenes_estudios(id_consulta);
CREATE INDEX IF NOT EXISTS idx_receta_paciente ON recetas(id_paciente);
CREATE INDEX IF NOT EXISTS idx_receta_consulta ON recetas(id_consulta);
CREATE INDEX IF NOT EXISTS idx_certificado_paciente ON certificados_medicos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_certificado_consulta ON certificados_medicos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_registro_insumo_procedimiento ON registro_insumos(id_registro_procedimiento);

-- ============================================================================
-- PASO 5: Verificaciones finales
-- ============================================================================
SELECT 'estados_citas' AS tabla, COUNT(*) AS registros FROM estados_citas
UNION ALL SELECT 'presupuestos', COUNT(*) FROM presupuestos
UNION ALL SELECT 'ordenes_estudios', COUNT(*) FROM ordenes_estudios
UNION ALL SELECT 'recetas', COUNT(*) FROM recetas
UNION ALL SELECT 'certificados_medicos', COUNT(*) FROM certificados_medicos
UNION ALL SELECT 'insumos', COUNT(*) FROM insumos
UNION ALL SELECT 'registro_insumos', COUNT(*) FROM registro_insumos;

SELECT est_cita_nombre, est_cita_color FROM estados_citas ORDER BY id_estado_cita;
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'diagnosticos' AND column_name LIKE '%codigo%';
