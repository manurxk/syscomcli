-- ============================================================================
-- FASE 5: TABLAS DE CONSULTORIO
-- ============================================================================
-- Este script crea las tablas del módulo de consultorio
-- Ejecutar después de: 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql
-- ============================================================================

-- ============================================================================
-- TABLAS REFERENCIALES DEL CONSULTORIO
-- ============================================================================

-- 1. SÍNTOMAS
CREATE TABLE IF NOT EXISTS sintomas (
    id_sintoma SERIAL PRIMARY KEY,
    des_sintoma VARCHAR(200) NOT NULL,
    est_sintoma CHAR(1) DEFAULT 'A' CHECK (est_sintoma IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- 2. SIGNOS
CREATE TABLE IF NOT EXISTS signos (
    id_signo SERIAL PRIMARY KEY,
    des_signo VARCHAR(200) NOT NULL,
    est_signo CHAR(1) DEFAULT 'A' CHECK (est_signo IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- 3. DIAGNÓSTICOS
CREATE TABLE IF NOT EXISTS diagnosticos (
    id_diagnostico SERIAL PRIMARY KEY,
    des_diagnostico VARCHAR(500) NOT NULL,
    est_diagnostico CHAR(1) DEFAULT 'A' CHECK (est_diagnostico IN ('A', 'I')),
    diagnostico_codigo_cie10 VARCHAR(10),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- 4. TIPOS DE ANÁLISIS
CREATE TABLE IF NOT EXISTS tipos_analisis (
    id_tipo_analisis SERIAL PRIMARY KEY,
    des_tipo_analisis VARCHAR(200) NOT NULL,
    est_tipo_analisis CHAR(1) DEFAULT 'A' CHECK (est_tipo_analisis IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- 5. TIPOS DE ESTUDIOS
CREATE TABLE IF NOT EXISTS tipos_estudios (
    id_tipo_estudio SERIAL PRIMARY KEY,
    des_tipo_estudio VARCHAR(200) NOT NULL,
    est_tipo_estudio CHAR(1) DEFAULT 'A' CHECK (est_tipo_estudio IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- 6. MEDICAMENTOS
CREATE TABLE IF NOT EXISTS medicamentos (
    id_medicamento SERIAL PRIMARY KEY,
    des_medicamento VARCHAR(200) NOT NULL,
    est_medicamento CHAR(1) DEFAULT 'A' CHECK (est_medicamento IN ('A', 'I')),
    medicamento_concentracion VARCHAR(50),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- 7. TIPOS DE PROCEDIMIENTOS
CREATE TABLE IF NOT EXISTS tipos_procedimientos (
    id_tipo_procedimiento SERIAL PRIMARY KEY,
    des_tipo_procedimiento VARCHAR(200) NOT NULL,
    est_tipo_procedimiento CHAR(1) DEFAULT 'A' CHECK (est_tipo_procedimiento IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- 8. TIPOS DE TRATAMIENTOS
CREATE TABLE IF NOT EXISTS tipos_tratamientos (
    id_tipo_tratamiento SERIAL PRIMARY KEY,
    des_tipo_tratamiento VARCHAR(200) NOT NULL,
    est_tipo_tratamiento CHAR(1) DEFAULT 'A' CHECK (est_tipo_tratamiento IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- ============================================================================
-- TABLAS PRINCIPALES DEL CONSULTORIO
-- ============================================================================

-- 9. CONSULTAS
CREATE TABLE IF NOT EXISTS consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_cita INTEGER, -- Vinculación opcional con citas
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL, -- id_especialista
    des_consulta TEXT,
    est_consulta CHAR(1) DEFAULT 'A' CHECK (est_consulta IN ('A', 'I')),
    consulta_fecha TIMESTAMP NOT NULL,
    consulta_motivo VARCHAR(500),
    consulta_estado VARCHAR(20) DEFAULT 'PENDIENTE', -- PENDIENTE, EN_ATENCION, FINALIZADA
    consulta_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 10. REGISTRO DE DIAGNÓSTICOS
CREATE TABLE IF NOT EXISTS registro_diagnosticos (
    id_registro_diagnostico SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_diagnostico INTEGER NOT NULL,
    des_registro_diagnostico TEXT,
    est_registro_diagnostico CHAR(1) DEFAULT 'A' CHECK (est_registro_diagnostico IN ('A', 'I')),
    registro_tipo VARCHAR(20) DEFAULT 'PRESUNTIVO', -- PRESUNTIVO, DEFINITIVO, DIFERENCIAL
    registro_gravedad VARCHAR(20), -- LEVE, MODERADO, GRAVE
    registro_fecha DATE NOT NULL,
    registro_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_diagnostico) REFERENCES diagnosticos(id_diagnostico) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 11. REGISTRO DE PROCEDIMIENTOS
CREATE TABLE IF NOT EXISTS registro_procedimientos (
    id_registro_procedimiento SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_tipo_procedimiento INTEGER NOT NULL,
    des_registro_procedimiento TEXT NOT NULL,
    est_registro_procedimiento CHAR(1) DEFAULT 'A' CHECK (est_registro_procedimiento IN ('A', 'I')),
    registro_fecha TIMESTAMP NOT NULL,
    registro_duracion INTEGER, -- Duración en minutos
    registro_resultado TEXT,
    registro_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_procedimiento) REFERENCES tipos_procedimientos(id_tipo_procedimiento) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 12. TRATAMIENTOS
CREATE TABLE IF NOT EXISTS tratamientos (
    id_tratamiento SERIAL PRIMARY KEY,
    id_consulta INTEGER,
    id_paciente INTEGER NOT NULL,
    id_registro_diagnostico INTEGER,
    id_tipo_tratamiento INTEGER,
    des_tratamiento TEXT NOT NULL,
    est_tratamiento CHAR(1) DEFAULT 'A' CHECK (est_tratamiento IN ('A', 'I')),
    tratamiento_tipo VARCHAR(100), -- FARMACOLÓGICO, PSICOTERAPÉUTICO, MIXTO
    tratamiento_fecha_inicio DATE NOT NULL,
    tratamiento_fecha_fin DATE,
    tratamiento_estado VARCHAR(20) DEFAULT 'ACTIVO', -- ACTIVO, FINALIZADO, SUSPENDIDO
    tratamiento_objetivos TEXT,
    numero_sesiones INTEGER,
    frecuencia_sesiones VARCHAR(100),
    duracion_sesion INTEGER, -- Duración en minutos
    tratamiento_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_registro_diagnostico) REFERENCES registro_diagnosticos(id_registro_diagnostico) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_tratamiento) REFERENCES tipos_tratamientos(id_tipo_tratamiento) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 13. REGISTRO DE SÍNTOMAS
CREATE TABLE IF NOT EXISTS registro_sintomas (
    id_registro_sintoma SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_sintoma INTEGER NOT NULL,
    registro_intensidad VARCHAR(20), -- LEVE, MODERADO, GRAVE
    registro_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_sintoma) REFERENCES sintomas(id_sintoma) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 14. REGISTRO DE SIGNOS
CREATE TABLE IF NOT EXISTS registro_signos (
    id_registro_signo SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_signo INTEGER NOT NULL,
    registro_descripcion TEXT,
    registro_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_signo) REFERENCES signos(id_signo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 15. ANAMNESIS (Historial clínico detallado)
CREATE TABLE IF NOT EXISTS anamnesis (
    id_anamnesis SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    motivo_consulta TEXT,
    informante VARCHAR(100),
    relacion_informante VARCHAR(100),
    antecedentes_familiares_similares TEXT,
    antecedentes_patologicos_familiares TEXT,
    componentes_familiares TEXT,
    historia_familiar TEXT,
    antecedentes_patologicos_personales TEXT,
    historia_problema_actual TEXT,
    historia_desarrollo TEXT,
    historia_academica TEXT,
    historia_laboral TEXT,
    historia_rehabilitacion TEXT,
    medicacion_actual TEXT,
    medicacion_psiquiatrica_previa TEXT,
    consumo_sustancias TEXT,
    relaciones_interpersonales TEXT,
    actividad_fisica TEXT,
    patron_sueno TEXT,
    patron_alimentacion TEXT,
    actividad_emocional TEXT,
    actividad_sexual TEXT,
    impresion_diagnostica TEXT,
    plan_trabajo TEXT,
    eval_neuropsicologica BOOLEAN DEFAULT FALSE,
    eval_psicologica BOOLEAN DEFAULT FALSE,
    eval_psicopedagogica BOOLEAN DEFAULT FALSE,
    eval_fonoaudiologica BOOLEAN DEFAULT FALSE,
    eval_psicomotora BOOLEAN DEFAULT FALSE,
    terapia_individual BOOLEAN DEFAULT FALSE,
    terapia_familiar BOOLEAN DEFAULT FALSE,
    terapia_grupal BOOLEAN DEFAULT FALSE,
    terapia_ocupacional BOOLEAN DEFAULT FALSE,
    otra_terapia TEXT,
    observaciones TEXT,
    indicaciones TEXT,
    version INTEGER DEFAULT 1,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 16. ANAMNESIS HISTORIAL (Versiones históricas de anamnesis)
CREATE TABLE IF NOT EXISTS anamnesis_historial (
    id_historial SERIAL PRIMARY KEY,
    id_anamnesis INTEGER NOT NULL,
    version INTEGER NOT NULL,
    contenido_json JSONB NOT NULL,
    modificado_por INTEGER,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_anamnesis) REFERENCES anamnesis(id_anamnesis) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_consultas_cita ON consultas(id_cita);
CREATE INDEX IF NOT EXISTS idx_consultas_paciente ON consultas(id_paciente);
CREATE INDEX IF NOT EXISTS idx_consultas_profesional ON consultas(id_profesional);
CREATE INDEX IF NOT EXISTS idx_consultas_fecha ON consultas(consulta_fecha);
CREATE INDEX IF NOT EXISTS idx_consultas_estado ON consultas(consulta_estado);
CREATE INDEX IF NOT EXISTS idx_registro_diagnosticos_consulta ON registro_diagnosticos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_registro_diagnosticos_diagnostico ON registro_diagnosticos(id_diagnostico);
CREATE INDEX IF NOT EXISTS idx_registro_procedimientos_consulta ON registro_procedimientos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_registro_procedimientos_paciente ON registro_procedimientos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_tratamientos_paciente ON tratamientos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_tratamientos_estado ON tratamientos(tratamiento_estado);
CREATE INDEX IF NOT EXISTS idx_anamnesis_consulta ON anamnesis(id_consulta);
CREATE INDEX IF NOT EXISTS idx_anamnesis_paciente ON anamnesis(id_paciente);

-- ============================================================================
-- COMENTARIOS EN TABLAS
-- ============================================================================

COMMENT ON TABLE consultas IS 'Registro de consultas médicas/psicológicas vinculadas a citas';
COMMENT ON TABLE registro_diagnosticos IS 'Diagnósticos registrados en cada consulta';
COMMENT ON TABLE registro_procedimientos IS 'Procedimientos médicos realizados en consulta';
COMMENT ON TABLE tratamientos IS 'Tratamientos asignados a pacientes';
COMMENT ON TABLE anamnesis IS 'Historial clínico detallado del paciente';

-- ============================================================================
-- DATOS INICIALES
-- ============================================================================

-- Tipos de procedimientos
-- NOTA: usuario_creacion usa 1 (ID del usuario SISTEMA) ya que después de FASE 11 se migra a INTEGER
INSERT INTO tipos_procedimientos (des_tipo_procedimiento, est_tipo_procedimiento, usuario_creacion) VALUES
    ('Sesión de Terapia Individual', 'A', 1),
    ('Sesión de Terapia Grupal', 'A', 1),
    ('Sesión de Terapia Familiar', 'A', 1),
    ('Evaluación Psicológica', 'A', 1),
    ('Test Psicológico', 'A', 1),
    ('Consulta de Seguimiento', 'A', 1),
    ('Taller Psicoeducativo', 'A', 1)
ON CONFLICT (des_tipo_procedimiento) DO NOTHING;

-- Tipos de estudios
-- NOTA: usuario_creacion usa 1 (ID del usuario SISTEMA) ya que después de FASE 11 se migra a INTEGER
INSERT INTO tipos_estudios (des_tipo_estudio, est_tipo_estudio, usuario_creacion) VALUES
    ('Evaluación Psicológica Completa', 'A', 1),
    ('Test de Inteligencia (WISC/WAIS)', 'A', 1),
    ('Test de Personalidad (MMPI)', 'A', 1),
    ('Test Proyectivo (Rorschach)', 'A', 1),
    ('Evaluación Neuropsicológica', 'A', 1),
    ('Test de Ansiedad y Depresión', 'A', 1),
    ('Evaluación de Desarrollo', 'A', 1),
    ('Test de Atención y Concentración', 'A', 1)
ON CONFLICT (des_tipo_estudio) DO NOTHING;

-- Tipos de tratamientos
-- NOTA: usuario_creacion usa 1 (ID del usuario SISTEMA) ya que después de FASE 11 se migra a INTEGER
INSERT INTO tipos_tratamientos (des_tipo_tratamiento, est_tipo_tratamiento, usuario_creacion) VALUES
    ('Tratamiento Farmacológico', 'A', 1),
    ('Tratamiento Psicoterapéutico', 'A', 1),
    ('Tratamiento Mixto', 'A', 1),
    ('Terapia Cognitivo-Conductual', 'A', 1),
    ('Terapia Familiar', 'A', 1),
    ('Terapia Grupal', 'A', 1),
    ('Intervención Temprana', 'A', 1)
ON CONFLICT (des_tipo_tratamiento) DO NOTHING;

-- Medicamentos
-- NOTA: usuario_creacion usa 1 (ID del usuario SISTEMA) ya que después de FASE 11 se migra a INTEGER
INSERT INTO medicamentos (des_medicamento, medicamento_concentracion, est_medicamento, usuario_creacion) VALUES
    ('Sertralina', '50mg', 'A', 1),
    ('Fluoxetina', '20mg', 'A', 1),
    ('Paroxetina', '20mg', 'A', 1),
    ('Escitalopram', '10mg', 'A', 1),
    ('Venlafaxina', '75mg', 'A', 1),
    ('Duloxetina', '60mg', 'A', 1),
    ('Alprazolam', '0.5mg', 'A', 1),
    ('Clonazepam', '0.5mg', 'A', 1),
    ('Lorazepam', '1mg', 'A', 1),
    ('Quetiapina', '25mg', 'A', 1),
    ('Olanzapina', '5mg', 'A', 1),
    ('Risperidona', '1mg', 'A', 1),
    ('Valeriana', '500mg', 'A', 1),
    ('Melatonina', '3mg', 'A', 1)
ON CONFLICT (des_medicamento) DO NOTHING;

-- NOTA: Las siguientes tablas se gestionan desde la aplicación (no requieren datos iniciales):
-- - sintomas (se agregan dinámicamente)
-- - signos (se agregan dinámicamente)
-- - diagnosticos (se agregan dinámicamente)
-- - tipos_analisis (se agregan dinámicamente)

-- ============================================================================
-- FIN FASE 5
-- ============================================================================








