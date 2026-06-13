-- ============================================================================
-- FASE 4: TABLAS DE ESPECIALISTAS Y AGENDAMIENTO
-- ============================================================================
-- Este script crea las tablas de especialistas, consultorios y agendamiento
-- Ejecutar después de: 03_FASE_3_PERSONAS_PACIENTES.sql
-- ============================================================================

-- ============================================================================
-- 1. ESPECIALISTAS
-- ============================================================================
CREATE TABLE IF NOT EXISTS especialistas (
    id_especialista SERIAL PRIMARY KEY,
    id_funcionario INTEGER UNIQUE NOT NULL,
    esp_matricula VARCHAR(50) UNIQUE NOT NULL,
    esp_color_agenda VARCHAR(7) DEFAULT '#3498db',
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 2. ESPECIALISTA ESPECIALIDADES (Relación muchos a muchos)
-- ============================================================================
CREATE TABLE IF NOT EXISTS especialista_especialidades (
    id SERIAL PRIMARY KEY,
    id_especialista INTEGER NOT NULL,
    id_especialidad INTEGER NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(id_especialista, id_especialidad),
    
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 3. CONSULTORIOS
-- ============================================================================
CREATE TABLE IF NOT EXISTS consultorios (
    id_consultorio SERIAL PRIMARY KEY,
    des_consultorio VARCHAR(100) NOT NULL UNIQUE,
    est_consultorio BOOLEAN DEFAULT TRUE,
    
    -- Auditoría (patrón antiguo)
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INTEGER
);

-- ============================================================================
-- 4. DÍAS DE LA SEMANA
-- ============================================================================
CREATE TABLE IF NOT EXISTS dias_semana (
    id_dia_semana SERIAL PRIMARY KEY,
    des_dia_semana VARCHAR(15) NOT NULL UNIQUE,
    dia_orden INTEGER NOT NULL UNIQUE,
    est_dia_semana BOOLEAN DEFAULT TRUE
);

-- ============================================================================
-- 5. AGENDA HORARIOS (Configuración de horarios de atención)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agenda_horarios (
    id_agenda_horario SERIAL PRIMARY KEY,
    id_consultorio INTEGER NOT NULL,
    id_especialista INTEGER NOT NULL,
    id_especialidad INTEGER NOT NULL,
    id_dia_semana INTEGER NOT NULL,
    
    agen_hora_inicio TIME NOT NULL,
    agen_hora_fin TIME NOT NULL,
    agen_duracion_turno INTEGER NOT NULL DEFAULT 60 CHECK (agen_duracion_turno IN (30, 45, 60)), -- Duración en minutos: 30, 45, 60
    agen_turno VARCHAR(10), -- Calculado: MAÑANA, TARDE, NOCHE
    agen_cupos_totales INTEGER NOT NULL, -- Calculado automáticamente
    agen_fecha_desde DATE NOT NULL,
    agen_fecha_hasta DATE, -- NULL = vigencia indefinida
    agen_observaciones TEXT,
    est_agenda BOOLEAN DEFAULT TRUE,
    
    -- Auditoría (patrón antiguo)
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INTEGER,
    
    FOREIGN KEY (id_consultorio) REFERENCES consultorios(id_consultorio) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_dia_semana) REFERENCES dias_semana(id_dia_semana) 
        ON DELETE RESTRICT ON UPDATE CASCADE
    
    -- NOTA: La restricción UNIQUE se reemplaza por un índice único parcial
    -- que solo aplica a agendas activas, permitiendo múltiples agendas desactivadas
    -- en el mismo horario. Ver índice más abajo.
);

-- ============================================================================
-- 6. ESTADOS DE CITAS
-- ============================================================================
CREATE TABLE IF NOT EXISTS estados_citas (
    id_estado_cita SERIAL PRIMARY KEY,
    est_cita_nombre VARCHAR(50) UNIQUE NOT NULL,
    est_cita_descripcion TEXT,
    est_cita_color VARCHAR(7),
    est_cita_activo BOOLEAN DEFAULT TRUE
);

-- ============================================================================
-- 7. CITAS
-- ============================================================================
CREATE TABLE IF NOT EXISTS citas (
    id_cita SERIAL PRIMARY KEY,
    
    -- Referencias principales
    id_paciente INTEGER NOT NULL,
    id_agenda_horario INTEGER NOT NULL,
    id_especialista INTEGER NOT NULL,
    id_especialidad INTEGER NOT NULL,
    id_estado_cita INTEGER NOT NULL DEFAULT 1,
    
    -- Fecha y hora específicas
    cita_fecha DATE NOT NULL,
    cita_hora_inicio TIME NOT NULL,
    cita_hora_fin TIME NOT NULL,
    
    -- Tipo de cita
    cita_es_primera_vez BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Información de agendamiento
    cita_motivo TEXT,
    cita_observaciones TEXT,
    
    -- Control de confirmación
    cita_fecha_confirmacion TIMESTAMP,
    cita_usuario_confirmacion INTEGER,
    
    -- Para tratamientos futuros (opcional)
    id_contrato INTEGER,
    cita_numero_sesion INTEGER,
    
    -- Control
    cita_activo BOOLEAN DEFAULT TRUE,
    
    -- Auditoría (patrón antiguo)
    cita_creacion_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cita_creacion_usuario INTEGER NOT NULL,
    cita_modificacion_fecha TIMESTAMP,
    cita_modificacion_usuario INTEGER,
    
    -- Foreign Keys
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_agenda_horario) REFERENCES agenda_horarios(id_agenda_horario)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_estado_cita) REFERENCES estados_citas(id_estado_cita)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- Validaciones
    CONSTRAINT chk_hora_fin_mayor CHECK (cita_hora_fin > cita_hora_inicio),
    CONSTRAINT chk_numero_sesion_positivo CHECK (cita_numero_sesion IS NULL OR cita_numero_sesion > 0),
    
    -- Evitar duplicados
    CONSTRAINT uk_especialista_fecha_hora UNIQUE (id_especialista, cita_fecha, cita_hora_inicio)
);

-- ============================================================================
-- 8. RECORDATORIOS (Recordatorios de citas)
-- ============================================================================
-- ============================================================================
-- 8. RECORDATORIOS (Nueva estructura simplificada UltraMsg)
-- ============================================================================
-- Estructura: Una fila por cita con columnas booleanas para cada tipo
-- Integración con UltraMsg para envío de notificaciones WhatsApp
-- ============================================================================
CREATE TABLE IF NOT EXISTS recordatorios (
    id_recordatorio SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL UNIQUE,
    
    -- Datos de la cita (cache para evitar JOINs)
    recordatorio_cita_fecha DATE NOT NULL,
    recordatorio_cita_hora_inicio TIME NOT NULL,
    recordatorio_telefono VARCHAR(20),
    recordatorio_paciente_nombre VARCHAR(200),
    
    -- Recordatorio inmediato (creación/actualización de cita)
    recordatorio_inmediato_enviado BOOLEAN DEFAULT FALSE,
    recordatorio_inmediato_fecha_enviado TIMESTAMP,
    recordatorio_inmediato_ultramsg_id VARCHAR(100),
    recordatorio_inmediato_mensaje TEXT,
    
    -- Recordatorio 24 horas antes
    recordatorio_24h_enviado BOOLEAN DEFAULT FALSE,
    recordatorio_24h_fecha_programada TIMESTAMP,
    recordatorio_24h_fecha_enviado TIMESTAMP,
    recordatorio_24h_ultramsg_id VARCHAR(100),
    recordatorio_24h_mensaje TEXT,
    
    -- Recordatorio 12 horas antes
    recordatorio_12h_enviado BOOLEAN DEFAULT FALSE,
    recordatorio_12h_fecha_programada TIMESTAMP,
    recordatorio_12h_fecha_enviado TIMESTAMP,
    recordatorio_12h_ultramsg_id VARCHAR(100),
    recordatorio_12h_mensaje TEXT,
    
    -- Auditoría
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion INTEGER DEFAULT 1,
    
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON DELETE CASCADE
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_especialistas_funcionario ON especialistas(id_funcionario);
CREATE INDEX IF NOT EXISTS idx_especialista_especialidades_esp ON especialista_especialidades(id_especialista);
CREATE INDEX IF NOT EXISTS idx_especialista_especialidades_esp2 ON especialista_especialidades(id_especialidad);
CREATE INDEX IF NOT EXISTS idx_consultorios_estado ON consultorios(est_consultorio);
CREATE INDEX IF NOT EXISTS idx_agenda_horarios_especialista ON agenda_horarios(id_especialista);
CREATE INDEX IF NOT EXISTS idx_agenda_horarios_consultorio ON agenda_horarios(id_consultorio);
CREATE INDEX IF NOT EXISTS idx_agenda_horarios_dia ON agenda_horarios(id_dia_semana, est_agenda);
CREATE INDEX IF NOT EXISTS idx_agenda_horarios_vigencia ON agenda_horarios(agen_fecha_desde, agen_fecha_hasta);

-- Índices para recordatorios (nueva estructura UltraMsg)
CREATE INDEX IF NOT EXISTS idx_recordatorios_cita ON recordatorios(id_cita);
CREATE INDEX IF NOT EXISTS idx_recordatorios_24h_pendiente 
    ON recordatorios(recordatorio_24h_fecha_programada) 
    WHERE recordatorio_24h_enviado = FALSE;
CREATE INDEX IF NOT EXISTS idx_recordatorios_12h_pendiente 
    ON recordatorios(recordatorio_12h_fecha_programada) 
    WHERE recordatorio_12h_enviado = FALSE;

-- ============================================================================
-- ÍNDICE ÚNICO PARCIAL PARA AGENDAS ACTIVAS
-- ============================================================================
-- Este índice garantiza que solo puede haber una agenda ACTIVA por combinación
-- de consultorio, especialista, día y hora. Permite múltiples agendas 
-- desactivadas con los mismos valores, facilitando la reactivación.
-- ============================================================================
CREATE UNIQUE INDEX IF NOT EXISTS idx_agenda_horarios_activos_unique 
ON agenda_horarios(id_consultorio, id_especialista, id_dia_semana, agen_hora_inicio)
WHERE est_agenda = TRUE;

COMMENT ON INDEX idx_agenda_horarios_activos_unique IS 
'Índice único parcial que garantiza que solo puede haber una agenda activa por combinación de consultorio, especialista, día y hora. Permite múltiples agendas desactivadas con los mismos valores.';

CREATE INDEX IF NOT EXISTS idx_citas_paciente ON citas(id_paciente);
CREATE INDEX IF NOT EXISTS idx_citas_agenda ON citas(id_agenda_horario);

-- ============================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ============================================================================

COMMENT ON TABLE recordatorios IS 'Tabla simplificada de recordatorios UltraMsg: una fila por cita con columnas booleanas para cada tipo de recordatorio (inmediato, 24h, 12h)';
COMMENT ON COLUMN recordatorios.id_cita IS 'Referencia única a la cita (UNIQUE garantiza una sola fila por cita)';
COMMENT ON COLUMN recordatorios.recordatorio_inmediato_enviado IS 'TRUE si se envió notificación inmediata al crear/editar la cita vía UltraMsg';
COMMENT ON COLUMN recordatorios.recordatorio_24h_enviado IS 'TRUE si se envió recordatorio 24 horas antes de la cita vía UltraMsg';
COMMENT ON COLUMN recordatorios.recordatorio_12h_enviado IS 'TRUE si se envió recordatorio 12 horas antes de la cita vía UltraMsg';
COMMENT ON COLUMN recordatorios.recordatorio_inmediato_ultramsg_id IS 'ID del mensaje en UltraMsg para el recordatorio inmediato';
COMMENT ON COLUMN recordatorios.recordatorio_24h_ultramsg_id IS 'ID del mensaje en UltraMsg para el recordatorio 24h';
COMMENT ON COLUMN recordatorios.recordatorio_12h_ultramsg_id IS 'ID del mensaje en UltraMsg para el recordatorio 12h';
CREATE INDEX IF NOT EXISTS idx_citas_especialista ON citas(id_especialista);
CREATE INDEX IF NOT EXISTS idx_citas_fecha ON citas(cita_fecha);
CREATE INDEX IF NOT EXISTS idx_citas_estado ON citas(id_estado_cita);
CREATE INDEX IF NOT EXISTS idx_citas_fecha_hora ON citas(cita_fecha, cita_hora_inicio);
CREATE INDEX IF NOT EXISTS idx_citas_activa ON citas(cita_activo) WHERE cita_activo = TRUE;

-- ============================================================================
-- FUNCIONES DE BASE DE DATOS
-- ============================================================================

-- Función para obtener cupos disponibles por especialista
CREATE OR REPLACE FUNCTION obtener_cupos_por_especialista(
    p_id_especialista INT,
    p_fecha_inicio DATE,
    p_fecha_fin DATE
)
RETURNS TABLE (
    dia_semana VARCHAR,
    fecha_especifica DATE,
    hora_inicio TIME,
    hora_fin TIME,
    turno VARCHAR,
    cupos_totales INT,
    cupos_ocupados BIGINT,
    cupos_disponibles BIGINT,
    id_agenda_horario INT,
    duracion_minutos INT
) AS $$
DECLARE
    v_estado_cancelada INT;
BEGIN
    -- Obtener ID del estado CANCELADA
    SELECT id_estado_cita INTO v_estado_cancelada
    FROM estados_citas WHERE est_cita_nombre = 'CANCELADA';
    
    -- Si no existe el estado CANCELADA, usar NULL (no filtrar canceladas)
    IF v_estado_cancelada IS NULL THEN
        v_estado_cancelada := -1; -- Valor que nunca coincidirá
    END IF;
    
    RETURN QUERY
    SELECT 
        ds.des_dia_semana,
        d.fecha_especifica,
        bloque.hora_inicio_bloque,
        bloque.hora_fin_bloque,
        ah.agen_turno,
        bloque.cupos_totales_bloque,
        -- Si hay una cita en este horario exacto, el bloque está completamente ocupado
        -- La restricción UNIQUE (id_especialista, cita_fecha, cita_hora_inicio) garantiza que solo puede haber una cita
        CASE 
            WHEN COALESCE(cupos_ocupados.cantidad, 0) > 0 THEN bloque.cupos_totales_bloque
            ELSE 0
        END::BIGINT as cupos_ocupados,
        -- Los cupos disponibles son 0 si hay una cita, o el total si no hay
        CASE 
            WHEN COALESCE(cupos_ocupados.cantidad, 0) > 0 THEN 0
            ELSE bloque.cupos_totales_bloque
        END::BIGINT as cupos_disponibles,
        ah.id_agenda_horario,
        COALESCE(ah.agen_duracion_turno, 60) as duracion_minutos
    FROM agenda_horarios ah
    JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
    -- Generar fechas específicas del rango
    CROSS JOIN LATERAL (
        SELECT fecha::DATE as fecha_especifica
        FROM generate_series(p_fecha_inicio, p_fecha_fin, '1 day'::interval) fecha
        WHERE (
            CASE 
                WHEN EXTRACT(DOW FROM fecha) = 0 THEN 7  -- Domingo: DOW=0 pero id_dia_semana=7
                ELSE EXTRACT(DOW FROM fecha)              -- Lunes-Sábado: DOW coincide con id_dia_semana
            END
        ) = ah.id_dia_semana
    ) d
    -- Generar bloques individuales según la duración configurada (30, 45, o 60 minutos)
    CROSS JOIN LATERAL (
        SELECT 
            ((('2000-01-01'::DATE + ah.agen_hora_inicio)::TIMESTAMP + 
              (n * (COALESCE(ah.agen_duracion_turno, 60) || ' minutes')::INTERVAL))::TIME) as hora_inicio_bloque,
            ((('2000-01-01'::DATE + ah.agen_hora_inicio)::TIMESTAMP + 
              ((n + 1) * (COALESCE(ah.agen_duracion_turno, 60) || ' minutes')::INTERVAL))::TIME) as hora_fin_bloque,
            CASE 
                WHEN COALESCE(ah.agen_duracion_turno, 60) = 30 THEN 
                    (ah.agen_cupos_totales / GREATEST(1, (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 1800)::INTEGER))
                WHEN COALESCE(ah.agen_duracion_turno, 60) = 45 THEN 
                    (ah.agen_cupos_totales / GREATEST(1, (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 2700)::INTEGER))
                ELSE 
                    (ah.agen_cupos_totales / GREATEST(1, (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 3600)::INTEGER))
            END as cupos_totales_bloque
        FROM generate_series(
            0, 
            CASE 
                WHEN COALESCE(ah.agen_duracion_turno, 60) = 30 THEN 
                    (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 1800)::INTEGER - 1
                WHEN COALESCE(ah.agen_duracion_turno, 60) = 45 THEN 
                    (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 2700)::INTEGER - 1
                ELSE 
                    (EXTRACT(EPOCH FROM (ah.agen_hora_fin - ah.agen_hora_inicio)) / 3600)::INTEGER - 1
            END
        ) n
        WHERE ((('2000-01-01'::DATE + ah.agen_hora_inicio)::TIMESTAMP + 
                (n * (COALESCE(ah.agen_duracion_turno, 60) || ' minutes')::INTERVAL))::TIME) < ah.agen_hora_fin
    ) bloque
    -- Contar citas ocupadas para cada bloque específico
    -- IMPORTANTE: Si hay una cita en este horario exacto, el bloque está completamente ocupado
    LEFT JOIN LATERAL (
        SELECT COUNT(*)::INTEGER as cantidad
        FROM citas c
        WHERE c.id_especialista = ah.id_especialista
            AND c.cita_fecha = d.fecha_especifica
            AND c.cita_hora_inicio = bloque.hora_inicio_bloque
            AND (v_estado_cancelada = -1 OR c.id_estado_cita != v_estado_cancelada)
            AND c.cita_activo = TRUE
    ) cupos_ocupados ON TRUE
    WHERE ah.id_especialista = p_id_especialista
        AND ah.est_agenda = TRUE
        AND ah.agen_fecha_desde <= d.fecha_especifica
        AND (ah.agen_fecha_hasta IS NULL OR ah.agen_fecha_hasta >= d.fecha_especifica)
        AND bloque.cupos_totales_bloque > 0
    ORDER BY d.fecha_especifica, bloque.hora_inicio_bloque;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION obtener_cupos_por_especialista IS 
'Retorna todos los cupos (disponibles y ocupados) para un especialista específico en un rango de fechas. Solo considera agendas activas (est_agenda = TRUE). La función respeta la duración configurada en agen_duracion_turno (30, 45, o 60 minutos) para generar los bloques.';

-- Función para obtener cupos disponibles por especialidad
CREATE OR REPLACE FUNCTION obtener_cupos_por_especialidad(
    p_id_especialidad INT,
    p_fecha_inicio DATE,
    p_fecha_fin DATE
)
RETURNS TABLE (
    id_especialista INT,
    especialista_nombre VARCHAR,
    especialista_color VARCHAR,
    dia_semana VARCHAR,
    fecha_especifica DATE,
    hora_inicio TIME,
    hora_fin TIME,
    turno VARCHAR,
    cupos_totales INT,
    cupos_ocupados BIGINT,
    cupos_disponibles BIGINT,
    id_agenda_horario INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        cupo_esp.id_especialista,
        CONCAT(pe.per_nombre, ' ', pe.per_apellido) as especialista_nombre,
        COALESCE(esp.esp_color, '#3b82f6') as especialista_color,
        cupo_esp.dia_semana,
        cupo_esp.fecha_especifica,
        cupo_esp.hora_inicio,
        cupo_esp.hora_fin,
        cupo_esp.turno,
        cupo_esp.cupos_totales,
        cupo_esp.cupos_ocupados,
        cupo_esp.cupos_disponibles,
        cupo_esp.id_agenda_horario
    FROM (
        SELECT DISTINCT ah.id_especialista
        FROM agenda_horarios ah
        WHERE ah.id_especialidad = p_id_especialidad
            AND ah.est_agenda = TRUE
    ) especialistas_activos
    CROSS JOIN LATERAL obtener_cupos_por_especialista(especialistas_activos.id_especialista, p_fecha_inicio, p_fecha_fin) cupo_esp
    JOIN especialistas e ON cupo_esp.id_especialista = e.id_especialista
    JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
    JOIN personas pe ON f.id_persona = pe.id_persona
    LEFT JOIN especialidades esp ON p_id_especialidad = esp.id_especialidad
    ORDER BY cupo_esp.fecha_especifica, cupo_esp.hora_inicio, especialista_nombre;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION obtener_cupos_por_especialidad IS 
'Retorna todos los cupos (disponibles y ocupados) para una especialidad específica en un rango de fechas, agrupando por especialista. Usa internamente obtener_cupos_por_especialista.';

-- ============================================================================
-- COMENTARIOS EN TABLAS
-- ============================================================================

COMMENT ON TABLE especialistas IS 'Especialistas médicos/psicológicos del sistema';
COMMENT ON TABLE especialista_especialidades IS 'Relación muchos a muchos entre especialistas y especialidades';
COMMENT ON TABLE consultorios IS 'Consultorios físicos del sistema';
COMMENT ON TABLE dias_semana IS 'Días de la semana para configuración de agendas';
COMMENT ON TABLE agenda_horarios IS 'Configuración de horarios de atención por especialista';
COMMENT ON TABLE estados_citas IS 'Estados posibles de las citas';
COMMENT ON TABLE citas IS 'Citas médicas agendadas';
COMMENT ON TABLE recordatorios IS 'Recordatorios automáticos de citas';

-- ============================================================================
-- DATOS INICIALES
-- ============================================================================
-- Datos
INSERT INTO dias_semana (des_dia_semana, dia_orden, est_dia_semana) VALUES
('LUNES', 1, TRUE),
('MARTES', 2, TRUE),
('MIERCOLES', 3, TRUE),
('JUEVES', 4, TRUE),
('VIERNES', 5, TRUE),
('SABADO', 6, TRUE),
('DOMINGO', 7, TRUE)
ON CONFLICT (des_dia_semana) DO NOTHING;

-- Estados de citas
INSERT INTO estados_citas (est_cita_nombre, est_cita_descripcion, est_cita_color) VALUES
    ('AGENDADA', 'Cita agendada, pendiente de confirmación', '#ffc107'),
    ('CONFIRMADA', 'Cita confirmada por el paciente', '#28a745'),
    ('COMPLETADA', 'Cita realizada exitosamente', '#17a2b8'),
    ('CANCELADA', 'Cita cancelada con anticipación', '#6c757d'),
    ('INASISTENCIA', 'Paciente no asistió sin avisar', '#dc3545'),
    ('REPROGRAMADA', 'Cita movida a otra fecha', '#fd7e14')
ON CONFLICT (est_cita_nombre) DO NOTHING;

-- ============================================================================
-- FIN FASE 4
-- ============================================================================








