-- ============================================================================
-- FASE 16: PACIENTE-PROFESIONAL Y DERIVACIONES
-- ============================================================================
-- Este script crea las tablas y funcionalidades para:
-- 1. Vincular pacientes con especialistas (relación M:M)
-- 2. Sistema de derivaciones entre especialistas
-- 3. Sistema de notificaciones
-- 4. Soporte para especialistas externos
-- ============================================================================
-- Ejecutar después de: 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql
-- IMPORTANTE: Requiere que existan las tablas pacientes y especialistas
-- ============================================================================

-- ============================================================================
-- 1. TABLA PACIENTE_PROFESIONAL (Relación M:M Paciente-Especialista)
-- ============================================================================
-- OBJETIVO: Cada profesional ve SOLO sus pacientes asignados
-- Permite que un paciente tenga múltiples especialistas (histórico y activo)
-- ============================================================================

CREATE TABLE IF NOT EXISTS paciente_profesional (
    id_paciente_profesional SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL,
    id_especialista INTEGER NOT NULL,
    
    -- Tipo de relación
    tipo_relacion VARCHAR(20) DEFAULT 'ASIGNADO' 
        CHECK (tipo_relacion IN ('ASIGNADO', 'DERIVADO', 'TEMPORAL')),
    
    -- Fechas de control
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_finalizacion TIMESTAMP NULL,
    
    -- Estado
    activo BOOLEAN DEFAULT TRUE,
    
    -- Observaciones
    observaciones TEXT,
    
    -- Auditoría
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_paciente_profesional_paciente 
    ON paciente_profesional(id_paciente);
    
CREATE INDEX IF NOT EXISTS idx_paciente_profesional_especialista 
    ON paciente_profesional(id_especialista);
    
CREATE INDEX IF NOT EXISTS idx_paciente_profesional_activo 
    ON paciente_profesional(activo) WHERE activo = TRUE;
    
CREATE INDEX IF NOT EXISTS idx_paciente_profesional_fecha_asignacion 
    ON paciente_profesional(fecha_asignacion DESC);

-- Índice único parcial: Un paciente solo puede estar activo con un especialista a la vez
CREATE UNIQUE INDEX IF NOT EXISTS uk_paciente_especialista_activo 
    ON paciente_profesional(id_paciente, id_especialista) 
    WHERE activo = TRUE;

COMMENT ON TABLE paciente_profesional IS 
    'Relación muchos a muchos entre pacientes y especialistas. Permite asignaciones, derivaciones y relaciones temporales.';
COMMENT ON COLUMN paciente_profesional.tipo_relacion IS 
    'ASIGNADO: Asignación directa, DERIVADO: Por derivación, TEMPORAL: Asignación temporal';
COMMENT ON COLUMN paciente_profesional.activo IS 
    'TRUE: Relación activa, FALSE: Relación finalizada';

-- ============================================================================
-- 2. TABLA DERIVACIONES (Derivar pacientes entre especialistas)
-- ============================================================================
-- OBJETIVO: Permitir que especialistas deriven pacientes a otros especialistas
-- con sistema de notificaciones y aceptación/rechazo
-- ============================================================================

CREATE TABLE IF NOT EXISTS derivaciones (
    id_derivacion SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL,
    id_especialista_origen INTEGER NOT NULL,
    id_especialista_destino INTEGER, -- NULL si es especialista externo
    
    -- Soporte para especialistas externos
    es_externo BOOLEAN DEFAULT FALSE,
    especialista_externo_nombre VARCHAR(200),
    especialista_externo_apellido VARCHAR(200),
    especialista_externo_telefono VARCHAR(20),
    especialista_externo_matricula VARCHAR(50),
    
    -- Información de la derivación
    motivo_derivacion TEXT NOT NULL,
    observaciones TEXT,
    urgencia VARCHAR(20) DEFAULT 'NORMAL' 
        CHECK (urgencia IN ('BAJA', 'NORMAL', 'ALTA', 'URGENTE')),
    
    -- Estado de la derivación
    estado VARCHAR(20) DEFAULT 'PENDIENTE' 
        CHECK (estado IN ('PENDIENTE', 'ACEPTADA', 'RECHAZADA', 'CANCELADA')),
    
    -- Fechas importantes
    fecha_derivacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_respuesta TIMESTAMP NULL,
    fecha_aceptacion TIMESTAMP NULL,
    
    -- Motivo de rechazo (si aplica)
    motivo_rechazo TEXT,
    
    -- Auditoría
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista_origen) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista_destino) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- Constraint: debe tener id_especialista_destino O datos de externo
    CONSTRAINT chk_derivacion_destino 
    CHECK (
        (es_externo = FALSE AND id_especialista_destino IS NOT NULL) OR
        (es_externo = TRUE AND id_especialista_destino IS NULL AND especialista_externo_nombre IS NOT NULL)
    )
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_derivaciones_paciente 
    ON derivaciones(id_paciente);
    
CREATE INDEX IF NOT EXISTS idx_derivaciones_origen 
    ON derivaciones(id_especialista_origen);
    
CREATE INDEX IF NOT EXISTS idx_derivaciones_destino 
    ON derivaciones(id_especialista_destino);
    
CREATE INDEX IF NOT EXISTS idx_derivaciones_estado 
    ON derivaciones(estado);
    
CREATE INDEX IF NOT EXISTS idx_derivaciones_fecha 
    ON derivaciones(fecha_derivacion DESC);

-- Índice único parcial para derivaciones pendientes
CREATE UNIQUE INDEX IF NOT EXISTS uk_derivacion_pendiente 
    ON derivaciones(id_paciente, id_especialista_destino) 
    WHERE estado = 'PENDIENTE' AND es_externo = FALSE;

COMMENT ON TABLE derivaciones IS 
    'Registro de derivaciones de pacientes entre especialistas (internos y externos)';
COMMENT ON COLUMN derivaciones.es_externo IS 
    'TRUE si el especialista destino es externo (no está en el sistema)';
COMMENT ON COLUMN derivaciones.urgencia IS 
    'BAJA: Sin urgencia, NORMAL: Urgencia normal, ALTA: Alta prioridad, URGENTE: Requiere atención inmediata';
COMMENT ON COLUMN derivaciones.estado IS 
    'PENDIENTE: Esperando respuesta, ACEPTADA: Derivación aceptada, RECHAZADA: Derivación rechazada, CANCELADA: Cancelada por origen';

-- ============================================================================
-- 3. TABLA NOTIFICACIONES (Sistema de notificaciones)
-- ============================================================================
-- OBJETIVO: Sistema de notificaciones para usuarios del sistema
-- ============================================================================

CREATE TABLE IF NOT EXISTS notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_derivacion INTEGER,
    
    -- Tipo de notificación
    tipo_notificacion VARCHAR(50) NOT NULL 
        CHECK (tipo_notificacion IN ('DERIVACION_RECIBIDA', 'DERIVACION_ACEPTADA', 'DERIVACION_RECHAZADA', 'OTRA')),
    
    -- Contenido
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    
    -- Estado
    leida BOOLEAN DEFAULT FALSE,
    fecha_leida TIMESTAMP NULL,
    
    -- Fechas
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_derivacion) REFERENCES derivaciones(id_derivacion) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario 
    ON notificaciones(id_usuario, leida);
    
CREATE INDEX IF NOT EXISTS idx_notificaciones_derivacion 
    ON notificaciones(id_derivacion);

COMMENT ON TABLE notificaciones IS 
    'Sistema de notificaciones para usuarios del sistema';
COMMENT ON COLUMN notificaciones.tipo_notificacion IS 
    'DERIVACION_RECIBIDA: Nueva derivación, DERIVACION_ACEPTADA: Derivación aceptada, DERIVACION_RECHAZADA: Derivación rechazada, OTRA: Otras notificaciones';

-- ============================================================================
-- 4. FUNCIONES AUXILIARES
-- ============================================================================

-- Función para crear derivación y asignar paciente automáticamente
CREATE OR REPLACE FUNCTION crear_derivacion(
    p_id_paciente INTEGER,
    p_id_especialista_origen INTEGER,
    p_motivo TEXT, -- Obligatorio
    p_id_especialista_destino INTEGER DEFAULT NULL,
    p_observaciones TEXT DEFAULT NULL,
    p_urgencia VARCHAR(20) DEFAULT 'NORMAL',
    p_es_externo BOOLEAN DEFAULT FALSE,
    p_externo_nombre VARCHAR(200) DEFAULT NULL,
    p_externo_apellido VARCHAR(200) DEFAULT NULL,
    p_externo_telefono VARCHAR(20) DEFAULT NULL,
    p_externo_matricula VARCHAR(50) DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_id_derivacion INTEGER;
    v_usuario_id INTEGER;
BEGIN
    -- Validar que si es externo, tenga datos de externo
    IF p_es_externo = TRUE THEN
        IF p_externo_nombre IS NULL OR p_externo_nombre = '' THEN
            RAISE EXCEPTION 'Si es especialista externo, debe proporcionar al menos el nombre';
        END IF;
    ELSE
        IF p_id_especialista_destino IS NULL THEN
            RAISE EXCEPTION 'Si no es externo, debe proporcionar id_especialista_destino';
        END IF;
    END IF;
    
    -- Crear la derivación
    INSERT INTO derivaciones (
        id_paciente,
        id_especialista_origen,
        id_especialista_destino,
        motivo_derivacion,
        observaciones,
        urgencia,
        estado,
        es_externo,
        especialista_externo_nombre,
        especialista_externo_apellido,
        especialista_externo_telefono,
        especialista_externo_matricula
    ) VALUES (
        p_id_paciente,
        p_id_especialista_origen,
        CASE WHEN p_es_externo THEN NULL ELSE p_id_especialista_destino END,
        p_motivo,
        p_observaciones,
        p_urgencia,
        'PENDIENTE',
        p_es_externo,
        p_externo_nombre,
        p_externo_apellido,
        p_externo_telefono,
        p_externo_matricula
    ) RETURNING id_derivacion INTO v_id_derivacion;
    
    -- Crear notificación solo si NO es externo (los externos no tienen usuario)
    IF p_es_externo = FALSE THEN
        -- Obtener el id_usuario del especialista destino
        SELECT u.id_usuario INTO v_usuario_id
        FROM usuarios u
        JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
        JOIN especialistas e ON f.id_funcionario = e.id_funcionario
        WHERE e.id_especialista = p_id_especialista_destino
            AND u.usu_estado = TRUE;  -- Solo usuarios activos
        
        -- Si se encontró un usuario, crear la notificación
        IF v_usuario_id IS NOT NULL THEN
            INSERT INTO notificaciones (
                id_usuario,
                id_derivacion,
                tipo_notificacion,
                titulo,
                mensaje
            ) VALUES (
                v_usuario_id,
                v_id_derivacion,
                'DERIVACION_RECIBIDA',
                'Nueva Derivación Recibida',
                'Tienes una nueva derivación de paciente pendiente de revisión'
            );
        ELSE
            -- Log warning si no se encontró usuario (pero no fallar)
            RAISE WARNING 'No se encontró usuario activo para el especialista destino %', p_id_especialista_destino;
        END IF;
    END IF;
    
    RETURN v_id_derivacion;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION crear_derivacion IS 
    'Crea una derivación y notificación automática para el especialista destino';

-- Función para aceptar derivación
CREATE OR REPLACE FUNCTION aceptar_derivacion(
    p_id_derivacion INTEGER,
    p_id_usuario INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    v_derivacion RECORD;
BEGIN
    -- Obtener datos de la derivación
    SELECT * INTO v_derivacion
    FROM derivaciones
    WHERE id_derivacion = p_id_derivacion
        AND estado = 'PENDIENTE';
    
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Actualizar estado de derivación
    UPDATE derivaciones
    SET estado = 'ACEPTADA',
        fecha_aceptacion = CURRENT_TIMESTAMP,
        fecha_respuesta = CURRENT_TIMESTAMP,
        usuario_modificacion = (SELECT usu_nick FROM usuarios WHERE id_usuario = p_id_usuario),
        fecha_modificacion = CURRENT_TIMESTAMP
    WHERE id_derivacion = p_id_derivacion;
    
    -- Crear relación en paciente_profesional con tipo DERIVADO (solo si no es externo)
    IF v_derivacion.es_externo = FALSE THEN
        INSERT INTO paciente_profesional (
            id_paciente,
            id_especialista,
            tipo_relacion,
            fecha_asignacion,
            observaciones
        ) VALUES (
            v_derivacion.id_paciente,
            v_derivacion.id_especialista_destino,
            'DERIVADO',
            CURRENT_TIMESTAMP,
            'Derivado desde especialista ' || v_derivacion.id_especialista_origen || 
            '. Motivo: ' || v_derivacion.motivo_derivacion
        )
        ON CONFLICT (id_paciente, id_especialista) WHERE activo = TRUE DO NOTHING;
    END IF;
    
    -- Crear notificación para el especialista origen
    INSERT INTO notificaciones (
        id_usuario,
        id_derivacion,
        tipo_notificacion,
        titulo,
        mensaje
    )
    SELECT 
        u.id_usuario,
        p_id_derivacion,
        'DERIVACION_ACEPTADA',
        'Derivación Aceptada',
        'Tu derivación ha sido aceptada'
    FROM usuarios u
    JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
    JOIN especialistas e ON f.id_funcionario = e.id_funcionario
    WHERE e.id_especialista = v_derivacion.id_especialista_origen
        AND u.usu_estado = TRUE;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION aceptar_derivacion IS 
    'Acepta una derivación pendiente y crea la relación paciente-profesional';

-- Función para rechazar derivación
CREATE OR REPLACE FUNCTION rechazar_derivacion(
    p_id_derivacion INTEGER,
    p_id_usuario INTEGER,
    p_motivo_rechazo TEXT
) RETURNS BOOLEAN AS $$
DECLARE
    v_derivacion RECORD;
BEGIN
    -- Obtener datos de la derivación
    SELECT * INTO v_derivacion
    FROM derivaciones
    WHERE id_derivacion = p_id_derivacion
        AND estado = 'PENDIENTE';
    
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Actualizar estado de derivación
    UPDATE derivaciones
    SET estado = 'RECHAZADA',
        fecha_respuesta = CURRENT_TIMESTAMP,
        motivo_rechazo = p_motivo_rechazo,
        usuario_modificacion = (SELECT usu_nick FROM usuarios WHERE id_usuario = p_id_usuario),
        fecha_modificacion = CURRENT_TIMESTAMP
    WHERE id_derivacion = p_id_derivacion;
    
    -- Crear notificación para el especialista origen
    INSERT INTO notificaciones (
        id_usuario,
        id_derivacion,
        tipo_notificacion,
        titulo,
        mensaje
    )
    SELECT 
        u.id_usuario,
        p_id_derivacion,
        'DERIVACION_RECHAZADA',
        'Derivación Rechazada',
        'Tu derivación ha sido rechazada. Motivo: ' || p_motivo_rechazo
    FROM usuarios u
    JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
    JOIN especialistas e ON f.id_funcionario = e.id_funcionario
    WHERE e.id_especialista = v_derivacion.id_especialista_origen
        AND u.usu_estado = TRUE;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION rechazar_derivacion IS 
    'Rechaza una derivación pendiente y notifica al especialista origen';

-- ============================================================================
-- 5. VISTAS ÚTILES
-- ============================================================================

-- Vista de derivaciones pendientes por especialista
CREATE OR REPLACE VIEW v_derivaciones_pendientes AS
SELECT 
    d.id_derivacion,
    d.id_paciente,
    p.pac_historia_clinica,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
    d.id_especialista_origen,
    CONCAT(po.per_nombre, ' ', po.per_apellido) AS especialista_origen,
    d.id_especialista_destino,
    CASE 
        WHEN d.es_externo = TRUE THEN 
            CONCAT(d.especialista_externo_nombre, ' ', COALESCE(d.especialista_externo_apellido, ''))
        ELSE 
            CONCAT(pd.per_nombre, ' ', pd.per_apellido)
    END AS especialista_destino,
    d.motivo_derivacion,
    d.urgencia,
    d.fecha_derivacion,
    d.es_externo,
    d.especialista_externo_nombre,
    d.especialista_externo_apellido,
    d.especialista_externo_telefono
FROM derivaciones d
JOIN pacientes p ON d.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
JOIN especialistas eo ON d.id_especialista_origen = eo.id_especialista
JOIN funcionarios fo ON eo.id_funcionario = fo.id_funcionario
JOIN personas po ON fo.id_persona = po.id_persona
LEFT JOIN especialistas ed ON d.id_especialista_destino = ed.id_especialista
LEFT JOIN funcionarios fd ON ed.id_funcionario = fd.id_funcionario
LEFT JOIN personas pd ON fd.id_persona = pd.id_persona
WHERE d.estado = 'PENDIENTE'
ORDER BY 
    CASE d.urgencia
        WHEN 'URGENTE' THEN 1
        WHEN 'ALTA' THEN 2
        WHEN 'NORMAL' THEN 3
        WHEN 'BAJA' THEN 4
    END,
    d.fecha_derivacion DESC;

COMMENT ON VIEW v_derivaciones_pendientes IS 
    'Vista de derivaciones pendientes ordenadas por urgencia y fecha';

-- Vista de pacientes por especialista (activos)
CREATE OR REPLACE VIEW v_pacientes_por_especialista AS
SELECT 
    pp.id_paciente_profesional,
    pp.id_paciente,
    p.pac_historia_clinica,
    CONCAT(per.per_nombre, ' ', per.per_apellido) AS paciente_nombre,
    pp.id_especialista,
    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
    pp.tipo_relacion,
    pp.fecha_asignacion,
    pp.activo
FROM paciente_profesional pp
JOIN pacientes p ON pp.id_paciente = p.id_paciente
JOIN personas per ON p.id_persona = per.id_persona
JOIN especialistas e ON pp.id_especialista = e.id_especialista
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas pe ON f.id_persona = pe.id_persona
WHERE pp.activo = TRUE
ORDER BY pp.fecha_asignacion DESC;

COMMENT ON VIEW v_pacientes_por_especialista IS 
    'Vista de pacientes activos por especialista';

-- ============================================================================
-- 6. MIGRACIÓN DE DATOS EXISTENTES (Opcional)
-- ============================================================================
-- Migrar relaciones paciente-especialista desde citas y consultas existentes
-- ============================================================================

-- Migrar desde CITAS (relación más confiable)
INSERT INTO paciente_profesional (id_paciente, id_especialista, tipo_relacion, fecha_asignacion, activo)
SELECT DISTINCT 
    c.id_paciente,
    c.id_especialista,
    'ASIGNADO' AS tipo_relacion,
    MIN(c.cita_creacion_fecha) AS fecha_asignacion,
    TRUE AS activo
FROM citas c
WHERE c.cita_activo = TRUE
    AND c.id_paciente IS NOT NULL
    AND c.id_especialista IS NOT NULL
    -- Evitar duplicados: solo insertar si no existe relación activa
    AND NOT EXISTS (
        SELECT 1 FROM paciente_profesional pp
        WHERE pp.id_paciente = c.id_paciente
            AND pp.id_especialista = c.id_especialista
            AND pp.activo = TRUE
    )
GROUP BY c.id_paciente, c.id_especialista
ON CONFLICT (id_paciente, id_especialista) WHERE activo = TRUE DO NOTHING;

-- Migrar desde CONSULTAS (para pacientes que no tienen citas pero sí consultas)
INSERT INTO paciente_profesional (id_paciente, id_especialista, tipo_relacion, fecha_asignacion, activo)
SELECT DISTINCT 
    c.id_paciente,
    c.id_profesional AS id_especialista,
    'ASIGNADO' AS tipo_relacion,
    MIN(c.fecha_creacion) AS fecha_asignacion,
    TRUE AS activo
FROM consultas c
WHERE c.est_consulta = 'A'
    AND c.id_paciente IS NOT NULL
    AND c.id_profesional IS NOT NULL
    -- Solo insertar si no existe ya en paciente_profesional
    AND NOT EXISTS (
        SELECT 1 FROM paciente_profesional pp
        WHERE pp.id_paciente = c.id_paciente
            AND pp.id_especialista = c.id_profesional
            AND pp.activo = TRUE
    )
GROUP BY c.id_paciente, c.id_profesional
ON CONFLICT (id_paciente, id_especialista) WHERE activo = TRUE DO NOTHING;

-- ============================================================================
-- COMENTARIOS FINALES
-- ============================================================================

COMMENT ON TABLE paciente_profesional IS 
    'Relación muchos a muchos entre pacientes y especialistas. Permite asignaciones, derivaciones y relaciones temporales.';
COMMENT ON TABLE derivaciones IS 
    'Registro de derivaciones de pacientes entre especialistas (internos y externos)';
COMMENT ON TABLE notificaciones IS 
    'Sistema de notificaciones para usuarios del sistema';

-- ============================================================================
-- FIN FASE 16
-- ============================================================================

