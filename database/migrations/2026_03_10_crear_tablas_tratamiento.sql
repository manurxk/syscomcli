-- Migración: Crear tabla de feriados y log de estados de cita
-- Creado: 2026-03-10

-- 1. Tabla de Feriados
CREATE TABLE IF NOT EXISTS feriados (
    id_feriado SERIAL PRIMARY KEY,
    fecha_feriado DATE NOT NULL UNIQUE,
    des_feriado VARCHAR(255) NOT NULL,
    est_feriado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Frecuencias de Agendamiento (Normalización)
CREATE TABLE IF NOT EXISTS frecuencias_agendamiento (
    id_frecuencia SERIAL PRIMARY KEY,
    des_frecuencia VARCHAR(100) NOT NULL UNIQUE, -- Ej: 'SEMANAL', 'QUINCENAL', 'MENSUAL'
    est_frecuencia BOOLEAN DEFAULT TRUE
);

-- Insertar frecuencias base
INSERT INTO frecuencias_agendamiento (des_frecuencia) VALUES 
('DIARIO'), 
('SEMANAL'), 
('QUINCENAL'), 
('MENSUAL') 
ON CONFLICT (des_frecuencia) DO NOTHING;

-- 3. Tabla de Log de Estados de Cita
CREATE TABLE IF NOT EXISTS citas_log_estados (
    id_cita_log SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50) NOT NULL,
    motivo_cambio TEXT,
    usuario_cambio VARCHAR(100),
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cita_log FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON DELETE CASCADE
);

-- 4. Modificar tabla presupuestos para vincular frecuencia normalizada
-- Nota: Primero agregamos la columna, luego el FK
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='presupuestos' AND column_name='id_frecuencia') THEN
        ALTER TABLE presupuestos ADD COLUMN id_frecuencia INTEGER;
        ALTER TABLE presupuestos ADD CONSTRAINT fk_presupuesto_frecuencia FOREIGN KEY (id_frecuencia) REFERENCES frecuencias_agendamiento(id_frecuencia);
    END IF;
END $$;
