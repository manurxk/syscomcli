-- Migración: Crear tabla de multas de pacientes
-- Creado: 2026-03-10

CREATE TABLE IF NOT EXISTS paciente_multas (
    id_multa SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL,
    id_cita INTEGER, -- Opcional, por si la multa es por ausencia a una cita
    monto_multa NUMERIC(15, 2) NOT NULL,
    motivo_multa VARCHAR(255) NOT NULL,
    estado_multa VARCHAR(20) DEFAULT 'PENDIENTE', -- PENDIENTE, PAGADA, ANULADA
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_pago TIMESTAMP,
    id_factura INTEGER, -- Vínculo si la multa se factura al pagarse
    observaciones TEXT,
    CONSTRAINT fk_multa_paciente FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    CONSTRAINT fk_multa_cita FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON DELETE SET NULL
);

-- Si se necesita un estado específico en citas para 'AUSENTE'
-- Intentamos insertarlo de forma segura
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM estados_citas WHERE est_cita_nombre IN ('AUSENTE', 'NO SHOW')) THEN
        -- Normalmente 1=Agendada, 2=Confirmada, 3=Atendida, 4=Cancelada
        -- Agregamos el estado 5 para Ausente
        INSERT INTO estados_citas (id_estado_cita, est_cita_nombre, est_cita_color) 
        VALUES (5, 'AUSENTE', '#ef4444')
        ON CONFLICT (id_estado_cita) DO NOTHING;
    END IF;
END $$;
