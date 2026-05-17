-- ============================================================================
-- FASE 3: TABLAS DE PACIENTES
-- ============================================================================
-- Este script crea las tablas relacionadas con pacientes
-- Ejecutar después de: 02_FASE_2_SEGURIDAD_USUARIOS.sql
-- ============================================================================

-- ============================================================================
-- 1. PACIENTES
-- ============================================================================
CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente SERIAL PRIMARY KEY,
    id_persona INTEGER UNIQUE NOT NULL,
    pac_es_menor BOOLEAN DEFAULT FALSE,
    pac_historia_clinica VARCHAR(50) UNIQUE,
    pac_observaciones TEXT,
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 2. PACIENTES MENORES (Información adicional para menores de edad)
-- ============================================================================
CREATE TABLE IF NOT EXISTS pacientes_menores (
    id_paciente_menor SERIAL PRIMARY KEY,
    id_paciente INTEGER UNIQUE NOT NULL,
    pam_nom_madre VARCHAR(100),
    pam_tel_madre VARCHAR(20),
    pam_nom_padre VARCHAR(100),
    pam_tel_padre VARCHAR(20),
    pam_educacion VARCHAR(100),
    pam_colegio VARCHAR(150),
    pam_tel_colegio VARCHAR(20),
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_pacientes_persona ON pacientes(id_persona);
CREATE INDEX IF NOT EXISTS idx_pacientes_historia ON pacientes(pac_historia_clinica);
CREATE INDEX IF NOT EXISTS idx_pacientes_menor ON pacientes(pac_es_menor);
CREATE INDEX IF NOT EXISTS idx_pacientes_menores_paciente ON pacientes_menores(id_paciente);

-- ============================================================================
-- COMENTARIOS EN TABLAS
-- ============================================================================

COMMENT ON TABLE pacientes IS 'Pacientes del sistema vinculados a personas';
COMMENT ON TABLE pacientes_menores IS 'Información adicional para pacientes menores de edad';
COMMENT ON COLUMN pacientes.pac_es_menor IS 'TRUE si el paciente es menor de edad';
COMMENT ON COLUMN pacientes.pac_historia_clinica IS 'Número único de historia clínica';

-- ============================================================================
-- FIN FASE 3
-- ============================================================================








