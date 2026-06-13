-- ============================================================================
-- FASE 2: TABLAS DE SEGURIDAD Y USUARIOS + MEJORAS AVANZADAS
-- ============================================================================
-- Este script crea las tablas del sistema de seguridad, usuarios y permisos
-- Incluye mejoras avanzadas de seguridad (compatibles hacia atrás)
-- Ejecutar después de: 01_FASE_1_REFERENCIALES_BASICAS.sql
-- ============================================================================

-- ============================================================================
-- 1. GRUPOS (Roles de usuario)
-- ============================================================================
CREATE TABLE IF NOT EXISTS grupos (
    id_grupo SERIAL PRIMARY KEY,
    des_grupo VARCHAR(60) UNIQUE NOT NULL,
    est_grupo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 2. MÓDULOS (Módulos del sistema)
-- ============================================================================
CREATE TABLE IF NOT EXISTS modulos (
    id_modulo SERIAL PRIMARY KEY,
    des_modulo VARCHAR(60) UNIQUE NOT NULL,
    est_modulo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 3. CARGOS (Cargos de funcionarios)
-- ============================================================================
CREATE TABLE IF NOT EXISTS cargos (
    id_cargo SERIAL PRIMARY KEY,
    des_cargo VARCHAR(60) UNIQUE NOT NULL,
    est_cargo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 4. PERSONAS (Tabla base para pacientes y funcionarios)
-- ============================================================================
CREATE TABLE IF NOT EXISTS personas (
    id_persona SERIAL PRIMARY KEY,
    per_nombre VARCHAR(100) NOT NULL,
    per_apellido VARCHAR(100) NOT NULL,
    per_cedula VARCHAR(20) UNIQUE NOT NULL,
    per_telefono VARCHAR(20) NOT NULL,
    per_correo VARCHAR(100),
    per_domicilio TEXT,
    per_fecha_nacimiento DATE,
    
    -- Referencias a tablas referenciales
    id_genero INTEGER,
    id_estado_civil INTEGER,
    id_ciudad INTEGER,
    id_ciudad_nacimiento INTEGER,
    id_nivel_instruccion INTEGER,
    id_profesion INTEGER,
    
    -- Fecha de inscripción (usada por los DAOs)
    per_fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Auditoría
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    -- Foreign Keys
    FOREIGN KEY (id_genero) REFERENCES generos(id_genero) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_estado_civil) REFERENCES estados_civiles(id_estado_civil) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_ciudad_nacimiento) REFERENCES ciudades(id_ciudad) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_nivel_instruccion) REFERENCES niveles_instruccion(id_nivel_instruccion) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesion) REFERENCES profesiones(id_profesion) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 5. FUNCIONARIOS (Empleados del sistema)
-- ============================================================================
CREATE TABLE IF NOT EXISTS funcionarios (
    id_funcionario SERIAL PRIMARY KEY,
    id_persona INTEGER UNIQUE NOT NULL,
    id_cargo INTEGER NOT NULL,
    fun_estado BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Auditoría (patrón antiguo mantenido para compatibilidad)
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INTEGER,
    
    -- Foreign Keys
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_cargo) REFERENCES cargos(id_cargo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 6. USUARIOS (Acceso al sistema)
-- ============================================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    usu_nick VARCHAR(30) UNIQUE NOT NULL,
    usu_clave VARCHAR(300) NOT NULL,
    usu_nro_intentos INTEGER NOT NULL DEFAULT 0,
    id_funcionario INTEGER UNIQUE NOT NULL,
    id_grupo INTEGER NOT NULL,
    usu_estado BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Auditoría (patrón antiguo mantenido para compatibilidad)
    creacion_fecha DATE DEFAULT CURRENT_DATE,
    creacion_hora TIME DEFAULT CURRENT_TIME,
    creacion_usuario INTEGER,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INTEGER,
    
    -- Foreign Keys
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- Foreign Keys para auditoría (auto-referencia)
    CONSTRAINT fk_usuarios_creacion_usuario 
        FOREIGN KEY (creacion_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_usuarios_modificacion_usuario 
        FOREIGN KEY (modificacion_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================================
-- 7. PÁGINAS (Páginas del sistema)
-- ============================================================================
CREATE TABLE IF NOT EXISTS paginas (
    id_pagina SERIAL PRIMARY KEY,
    des_pagina VARCHAR(60) UNIQUE NOT NULL,
    pag_direcc TEXT NOT NULL,
    est_pagina BOOLEAN NOT NULL DEFAULT TRUE,
    id_modulo INTEGER NOT NULL,
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 8. PERMISOS (Permisos por grupo y página)
-- ============================================================================
CREATE TABLE IF NOT EXISTS permisos (
    id_pagina INTEGER NOT NULL,
    id_grupo INTEGER NOT NULL,
    leer BOOLEAN NOT NULL DEFAULT FALSE,
    insertar BOOLEAN NOT NULL DEFAULT FALSE,
    editar BOOLEAN NOT NULL DEFAULT FALSE,
    borrar BOOLEAN NOT NULL DEFAULT FALSE,
    
    PRIMARY KEY (id_pagina, id_grupo),
    
    FOREIGN KEY (id_pagina) REFERENCES paginas(id_pagina) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 9. USUARIOS_ROLES (Tabla para roles múltiples por usuario)
-- ============================================================================
CREATE TABLE IF NOT EXISTS usuarios_roles (
    id_usuario_rol SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_grupo INTEGER NOT NULL REFERENCES grupos(id_grupo) ON DELETE CASCADE,
    es_rol_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asignado_por INTEGER REFERENCES usuarios(id_usuario),
    CONSTRAINT unique_usuario_grupo UNIQUE(id_usuario, id_grupo)
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_usuario ON usuarios_roles(id_usuario);
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_grupo ON usuarios_roles(id_grupo);
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_activo ON usuarios_roles(id_usuario, activo) WHERE activo = TRUE;
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_principal ON usuarios_roles(id_usuario, es_rol_principal) WHERE es_rol_principal = TRUE;

COMMENT ON TABLE usuarios_roles IS 'Tabla de relación para roles múltiples por usuario';
COMMENT ON COLUMN usuarios_roles.es_rol_principal IS 'Indica si este es el rol principal del usuario';
COMMENT ON COLUMN usuarios_roles.activo IS 'Indica si el rol está activo para el usuario';
COMMENT ON COLUMN usuarios_roles.asignado_por IS 'ID del usuario que asignó este rol (auditoría)';

-- ============================================================================
-- 10. FUNCIONARIO_GRUPOS (Grupos/Roles asignados a funcionarios)
-- ============================================================================
-- Esta tabla permite pre-asignar grupos/roles a funcionarios antes de crear su usuario
-- Cuando se cree el usuario, se pueden usar estos grupos como sugerencia o asignación automática
CREATE TABLE IF NOT EXISTS funcionario_grupos (
    id_funcionario_grupo SERIAL PRIMARY KEY,
    id_funcionario INTEGER NOT NULL REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE,
    id_grupo INTEGER NOT NULL REFERENCES grupos(id_grupo) ON DELETE CASCADE,
    es_rol_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asignado_por INTEGER REFERENCES usuarios(id_usuario),
    CONSTRAINT unique_funcionario_grupo UNIQUE(id_funcionario, id_grupo)
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_funcionario_grupos_funcionario ON funcionario_grupos(id_funcionario);
CREATE INDEX IF NOT EXISTS idx_funcionario_grupos_grupo ON funcionario_grupos(id_grupo);
CREATE INDEX IF NOT EXISTS idx_funcionario_grupos_activo ON funcionario_grupos(id_funcionario, activo) WHERE activo = TRUE;
CREATE INDEX IF NOT EXISTS idx_funcionario_grupos_principal ON funcionario_grupos(id_funcionario, es_rol_principal) WHERE es_rol_principal = TRUE;

COMMENT ON TABLE funcionario_grupos IS 'Tabla de relación para grupos/roles pre-asignados a funcionarios';
COMMENT ON COLUMN funcionario_grupos.es_rol_principal IS 'Indica si este es el rol principal sugerido para cuando se cree el usuario';
COMMENT ON COLUMN funcionario_grupos.activo IS 'Indica si el grupo está activo para el funcionario';
COMMENT ON COLUMN funcionario_grupos.asignado_por IS 'ID del usuario que asignó este grupo (auditoría)';

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN (BÁSICOS)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_personas_cedula ON personas(per_cedula);
CREATE INDEX IF NOT EXISTS idx_personas_nombre ON personas(per_nombre, per_apellido);
CREATE INDEX IF NOT EXISTS idx_funcionarios_persona ON funcionarios(id_persona);
CREATE INDEX IF NOT EXISTS idx_funcionarios_cargo ON funcionarios(id_cargo);
CREATE INDEX IF NOT EXISTS idx_funcionarios_estado ON funcionarios(fun_estado);
CREATE INDEX IF NOT EXISTS idx_usuarios_nick ON usuarios(usu_nick);
CREATE INDEX IF NOT EXISTS idx_usuarios_funcionario ON usuarios(id_funcionario);
CREATE INDEX IF NOT EXISTS idx_usuarios_grupo ON usuarios(id_grupo);
CREATE INDEX IF NOT EXISTS idx_usuarios_estado ON usuarios(usu_estado);
CREATE INDEX IF NOT EXISTS idx_paginas_modulo ON paginas(id_modulo);
CREATE INDEX IF NOT EXISTS idx_permisos_pagina ON permisos(id_pagina);
CREATE INDEX IF NOT EXISTS idx_permisos_grupo ON permisos(id_grupo);

-- ============================================================================
-- COMENTARIOS EN TABLAS (BÁSICAS)
-- ============================================================================

COMMENT ON TABLE grupos IS 'Grupos de usuarios (roles) del sistema';
COMMENT ON TABLE modulos IS 'Módulos funcionales del sistema';
COMMENT ON TABLE cargos IS 'Cargos de funcionarios';
COMMENT ON TABLE personas IS 'Tabla base de personas (pacientes y funcionarios)';
COMMENT ON TABLE funcionarios IS 'Funcionarios/empleados del sistema';
COMMENT ON TABLE usuarios IS 'Usuarios con acceso al sistema';
COMMENT ON TABLE paginas IS 'Páginas/rutas del sistema';
COMMENT ON TABLE permisos IS 'Permisos de acceso por grupo y página';

-- ============================================================================
-- MEJORAS DE SEGURIDAD AVANZADA
-- ============================================================================
-- Estas mejoras son COMPATIBLES HACIA ATRÁS - no rompen código Python actual
-- ============================================================================

-- ============================================================================
-- PASO 1.1: RESOLVER AUDITORÍA CIRCULAR
-- ============================================================================
-- Problema: ¿Cómo crear el primer usuario si creacion_usuario requiere un usuario existente?
-- Solución: Permitir NULL para registros SISTEMA y agregar campo legible
-- ============================================================================

-- Modificar FUNCIONARIOS para permitir NULL en creacion_usuario
ALTER TABLE funcionarios 
    ALTER COLUMN creacion_usuario DROP NOT NULL;

-- Agregar campo legible para compatibilidad
ALTER TABLE funcionarios 
    ADD COLUMN IF NOT EXISTS usuario_creacion_nombre VARCHAR(50);

-- Actualizar registros existentes con usuario_creacion_nombre
UPDATE funcionarios 
SET usuario_creacion_nombre = COALESCE(
    (SELECT usu_nick FROM usuarios WHERE id_usuario = funcionarios.creacion_usuario),
    'SISTEMA'
)
WHERE usuario_creacion_nombre IS NULL;

-- Modificar USUARIOS para permitir NULL en creacion_usuario
ALTER TABLE usuarios 
    ALTER COLUMN creacion_usuario DROP NOT NULL;

-- Agregar campo legible para compatibilidad
ALTER TABLE usuarios 
    ADD COLUMN IF NOT EXISTS usuario_creacion_nombre VARCHAR(50);

-- Actualizar registros existentes con usuario_creacion_nombre
UPDATE usuarios 
SET usuario_creacion_nombre = COALESCE(
    (SELECT usu_nick FROM usuarios u2 WHERE u2.id_usuario = usuarios.creacion_usuario),
    'SISTEMA'
)
WHERE usuario_creacion_nombre IS NULL;

-- Comentarios
COMMENT ON COLUMN funcionarios.creacion_usuario IS 'ID del usuario que creó el registro (NULL para registros SISTEMA)';
COMMENT ON COLUMN funcionarios.usuario_creacion_nombre IS 'Nombre legible del usuario creador (para compatibilidad)';
COMMENT ON COLUMN usuarios.creacion_usuario IS 'ID del usuario que creó el registro (NULL para registros SISTEMA)';
COMMENT ON COLUMN usuarios.usuario_creacion_nombre IS 'Nombre legible del usuario creador (para compatibilidad)';

-- ============================================================================
-- PASO 1.2: AGREGAR CAMPOS DE SEGURIDAD EN USUARIOS
-- ============================================================================

ALTER TABLE usuarios 
    ADD COLUMN IF NOT EXISTS fecha_ultimo_login TIMESTAMP,
    ADD COLUMN IF NOT EXISTS ip_ultimo_login VARCHAR(45),
    ADD COLUMN IF NOT EXISTS user_agent_ultimo_login TEXT,
    ADD COLUMN IF NOT EXISTS fecha_bloqueo TIMESTAMP,
    ADD COLUMN IF NOT EXISTS motivo_bloqueo VARCHAR(200),
    ADD COLUMN IF NOT EXISTS bloqueado_hasta TIMESTAMP,
    ADD COLUMN IF NOT EXISTS fecha_ultimo_intento_fallido TIMESTAMP,
    ADD COLUMN IF NOT EXISTS requiere_cambio_password BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS fecha_cambio_password TIMESTAMP,
    ADD COLUMN IF NOT EXISTS password_nunca_expira BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS dias_validez_password INTEGER DEFAULT 90,
    ADD COLUMN IF NOT EXISTS max_sesiones_simultaneas INTEGER DEFAULT 3,
    ADD COLUMN IF NOT EXISTS sesiones_activas INTEGER DEFAULT 0;

-- Comentarios
COMMENT ON COLUMN usuarios.fecha_ultimo_login IS 'Fecha y hora del último login exitoso';
COMMENT ON COLUMN usuarios.ip_ultimo_login IS 'Dirección IP de la última conexión';
COMMENT ON COLUMN usuarios.user_agent_ultimo_login IS 'Navegador/dispositivo de la última conexión';
COMMENT ON COLUMN usuarios.fecha_bloqueo IS 'Fecha y hora en que se bloqueó la cuenta';
COMMENT ON COLUMN usuarios.motivo_bloqueo IS 'Razón del bloqueo de la cuenta';
COMMENT ON COLUMN usuarios.bloqueado_hasta IS 'Fecha hasta la cual está bloqueada (bloqueo temporal)';
COMMENT ON COLUMN usuarios.fecha_ultimo_intento_fallido IS 'Fecha del último intento de login fallido';
COMMENT ON COLUMN usuarios.requiere_cambio_password IS 'Forzar cambio de contraseña en próximo login';
COMMENT ON COLUMN usuarios.fecha_cambio_password IS 'Fecha de la última vez que cambió la contraseña';
COMMENT ON COLUMN usuarios.password_nunca_expira IS 'Indica si la contraseña nunca expira (cuentas especiales)';
COMMENT ON COLUMN usuarios.dias_validez_password IS 'Días de validez de la contraseña (default 90)';
COMMENT ON COLUMN usuarios.max_sesiones_simultaneas IS 'Límite de sesiones simultáneas permitidas (default 3)';
COMMENT ON COLUMN usuarios.sesiones_activas IS 'Contador de sesiones activas en tiempo real';

-- ============================================================================
-- PASO 1.3: CREAR TABLA SESIONES
-- ============================================================================
-- Tracking de todas las conexiones activas de usuarios
-- ============================================================================

CREATE TABLE IF NOT EXISTS sesiones (
    id_sesion SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    token_sesion VARCHAR(500) UNIQUE NOT NULL,
    csrf_token VARCHAR(500),
    refresh_token VARCHAR(500),
    fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_ultimo_ping TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    fecha_cierre TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    sesion_activa BOOLEAN NOT NULL DEFAULT TRUE,
    tipo_cierre VARCHAR(20) CHECK (tipo_cierre IN ('logout', 'timeout', 'admin_force', 'security')),
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sesiones_usuario ON sesiones(id_usuario);
CREATE INDEX IF NOT EXISTS idx_sesiones_token ON sesiones(token_sesion);
CREATE INDEX IF NOT EXISTS idx_sesiones_activa ON sesiones(sesion_activa);
CREATE INDEX IF NOT EXISTS idx_sesiones_expiracion ON sesiones(fecha_expiracion);

COMMENT ON TABLE sesiones IS 'Tracking de todas las conexiones activas de usuarios';
COMMENT ON COLUMN sesiones.token_sesion IS 'JWT o session ID de Python';
COMMENT ON COLUMN sesiones.csrf_token IS 'Token CSRF de Flask-WTF';
COMMENT ON COLUMN sesiones.refresh_token IS 'Token para renovar sesión';
COMMENT ON COLUMN sesiones.tipo_cierre IS 'Tipo de cierre: logout, timeout, admin_force, security';

-- ============================================================================
-- PASO 1.4: CREAR TABLA PASSWORD_RESET_TOKENS
-- ============================================================================
-- Recuperación segura de contraseñas (olvidé mi contraseña)
-- ============================================================================

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id_token SERIAL PRIMARY KEY,
    token UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    id_usuario INTEGER NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    usado BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_uso TIMESTAMP,
    ip_solicitud VARCHAR(45),
    email_destino VARCHAR(100),
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_password_reset_token ON password_reset_tokens(token);
CREATE INDEX IF NOT EXISTS idx_password_reset_usuario ON password_reset_tokens(id_usuario);
CREATE INDEX IF NOT EXISTS idx_password_reset_usado ON password_reset_tokens(usado);
CREATE INDEX IF NOT EXISTS idx_password_reset_expiracion ON password_reset_tokens(fecha_expiracion);

COMMENT ON TABLE password_reset_tokens IS 'Tokens para recuperación segura de contraseñas';
COMMENT ON COLUMN password_reset_tokens.token IS 'Token único UUID para recuperación';
COMMENT ON COLUMN password_reset_tokens.fecha_expiracion IS 'Expiración típicamente 24 horas';

-- ============================================================================
-- PASO 1.5: CREAR TABLA PASSWORD_HISTORY
-- ============================================================================
-- Evitar que usuarios reutilicen contraseñas recientes
-- ============================================================================

CREATE TABLE IF NOT EXISTS password_history (
    id_history SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    password_hash VARCHAR(300) NOT NULL,
    fecha_cambio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cambiado_por INTEGER,
    motivo_cambio VARCHAR(50) CHECK (motivo_cambio IN ('usuario', 'admin_reset', 'expiracion', 'recuperacion')),
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cambiado_por) REFERENCES usuarios(id_usuario) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_password_history_usuario ON password_history(id_usuario);
CREATE INDEX IF NOT EXISTS idx_password_history_fecha ON password_history(fecha_cambio DESC);

COMMENT ON TABLE password_history IS 'Historial de contraseñas para evitar reutilización';
COMMENT ON COLUMN password_history.password_hash IS 'Hash de la contraseña anterior';
COMMENT ON COLUMN password_history.motivo_cambio IS 'Razón del cambio: usuario, admin_reset, expiracion, recuperacion';

-- ============================================================================
-- PASO 1.6: CREAR TABLA LOGIN_ATTEMPTS
-- ============================================================================
-- Auditoría detallada de TODOS los intentos de login (exitosos y fallidos)
-- ============================================================================

CREATE TABLE IF NOT EXISTS login_attempts (
    id_attempt SERIAL PRIMARY KEY,
    usuario_intentado VARCHAR(30) NOT NULL,
    id_usuario INTEGER,
    exitoso BOOLEAN NOT NULL DEFAULT FALSE,
    motivo_fallo VARCHAR(50) CHECK (motivo_fallo IN ('password_invalido', 'usuario_no_existe', 'cuenta_bloqueada', 'sesiones_maximas')),
    fecha_intento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    csrf_valido BOOLEAN,
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_login_attempts_usuario ON login_attempts(usuario_intentado);
CREATE INDEX IF NOT EXISTS idx_login_attempts_id_usuario ON login_attempts(id_usuario);
CREATE INDEX IF NOT EXISTS idx_login_attempts_exitoso ON login_attempts(exitoso);
CREATE INDEX IF NOT EXISTS idx_login_attempts_fecha ON login_attempts(fecha_intento DESC);
CREATE INDEX IF NOT EXISTS idx_login_attempts_ip ON login_attempts(ip_address);

COMMENT ON TABLE login_attempts IS 'Auditoría de todos los intentos de login (exitosos y fallidos)';
COMMENT ON COLUMN login_attempts.usuario_intentado IS 'Username ingresado (puede no existir)';
COMMENT ON COLUMN login_attempts.motivo_fallo IS 'Razón del fallo: password_invalido, usuario_no_existe, cuenta_bloqueada, sesiones_maximas';

-- ============================================================================
-- PASO 1.7: CREAR FUNCIONES POSTGRESQL ÚTILES
-- ============================================================================

-- Función: Verificar si un usuario está bloqueado
CREATE OR REPLACE FUNCTION esta_usuario_bloqueado(p_id_usuario INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    v_bloqueado_hasta TIMESTAMP;
    v_fecha_bloqueo TIMESTAMP;
BEGIN
    SELECT bloqueado_hasta, fecha_bloqueo
    INTO v_bloqueado_hasta, v_fecha_bloqueo
    FROM usuarios
    WHERE id_usuario = p_id_usuario;
    
    -- Si no tiene fecha de bloqueo, no está bloqueado
    IF v_fecha_bloqueo IS NULL THEN
        RETURN FALSE;
    END IF;
    
    -- Si tiene bloqueo temporal y ya expiró, no está bloqueado
    IF v_bloqueado_hasta IS NOT NULL AND v_bloqueado_hasta < CURRENT_TIMESTAMP THEN
        -- Desbloquear automáticamente
        UPDATE usuarios 
        SET fecha_bloqueo = NULL, 
            motivo_bloqueo = NULL, 
            bloqueado_hasta = NULL
        WHERE id_usuario = p_id_usuario;
        RETURN FALSE;
    END IF;
    
    -- Está bloqueado
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION esta_usuario_bloqueado(INTEGER) IS 'Verifica si un usuario está bloqueado y si el bloqueo sigue vigente';

-- Función: Registrar intento de login
CREATE OR REPLACE FUNCTION registrar_intento_login(
    p_usuario_intentado VARCHAR(30),
    p_id_usuario INTEGER,
    p_exitoso BOOLEAN,
    p_motivo_fallo VARCHAR(50),
    p_ip_address VARCHAR(45),
    p_user_agent TEXT,
    p_csrf_valido BOOLEAN DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_attempt_id INTEGER;
    v_intentos_fallidos INTEGER;
BEGIN
    -- Insertar registro de intento
    INSERT INTO login_attempts (
        usuario_intentado, id_usuario, exitoso, motivo_fallo,
        ip_address, user_agent, csrf_valido
    ) VALUES (
        p_usuario_intentado, p_id_usuario, p_exitoso, p_motivo_fallo,
        p_ip_address, p_user_agent, p_csrf_valido
    ) RETURNING id_attempt INTO v_attempt_id;
    
    -- Si el login fue exitoso, resetear contador de intentos
    IF p_exitoso AND p_id_usuario IS NOT NULL THEN
        UPDATE usuarios 
        SET usu_nro_intentos = 0,
            fecha_ultimo_intento_fallido = NULL
        WHERE id_usuario = p_id_usuario;
    -- Si fue fallido y existe el usuario, incrementar contador
    ELSIF NOT p_exitoso AND p_id_usuario IS NOT NULL THEN
        UPDATE usuarios 
        SET usu_nro_intentos = usu_nro_intentos + 1,
            fecha_ultimo_intento_fallido = CURRENT_TIMESTAMP
        WHERE id_usuario = p_id_usuario
        RETURNING usu_nro_intentos INTO v_intentos_fallidos;
        
        -- Bloquear automáticamente después de 5 intentos fallidos (30 minutos)
        IF v_intentos_fallidos >= 5 THEN
            UPDATE usuarios 
            SET fecha_bloqueo = CURRENT_TIMESTAMP,
                motivo_bloqueo = 'Múltiples intentos fallidos',
                bloqueado_hasta = CURRENT_TIMESTAMP + INTERVAL '30 minutes'
            WHERE id_usuario = p_id_usuario;
        END IF;
    END IF;
    
    RETURN v_attempt_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION registrar_intento_login(VARCHAR, INTEGER, BOOLEAN, VARCHAR, VARCHAR, TEXT, BOOLEAN) IS 
'Registra un intento de login, incrementa contador de fallos y bloquea automáticamente después de 5 intentos';

-- Función: Crear nueva sesión
CREATE OR REPLACE FUNCTION crear_sesion(
    p_id_usuario INTEGER,
    p_token_sesion VARCHAR(500),
    p_csrf_token VARCHAR(500),
    p_refresh_token VARCHAR(500),
    p_fecha_expiracion TIMESTAMP,
    p_ip_address VARCHAR(45),
    p_user_agent TEXT
)
RETURNS INTEGER AS $$
DECLARE
    v_sesion_id INTEGER;
    v_sesiones_activas INTEGER;
    v_max_sesiones INTEGER;
    v_sesion_antigua INTEGER;
BEGIN
    -- Obtener límite de sesiones
    SELECT max_sesiones_simultaneas INTO v_max_sesiones
    FROM usuarios
    WHERE id_usuario = p_id_usuario;
    
    -- Contar sesiones activas
    SELECT COUNT(*) INTO v_sesiones_activas
    FROM sesiones
    WHERE id_usuario = p_id_usuario 
      AND sesion_activa = TRUE
      AND fecha_expiracion > CURRENT_TIMESTAMP;
    
    -- Si alcanzó el límite, cerrar la sesión más antigua
    IF v_sesiones_activas >= v_max_sesiones THEN
        SELECT id_sesion INTO v_sesion_antigua
        FROM sesiones
        WHERE id_usuario = p_id_usuario 
          AND sesion_activa = TRUE
        ORDER BY fecha_inicio ASC
        LIMIT 1;
        
        IF v_sesion_antigua IS NOT NULL THEN
            UPDATE sesiones 
            SET sesion_activa = FALSE,
                fecha_cierre = CURRENT_TIMESTAMP,
                tipo_cierre = 'sesiones_maximas'
            WHERE id_sesion = v_sesion_antigua;
        END IF;
    END IF;
    
    -- Crear nueva sesión
    INSERT INTO sesiones (
        id_usuario, token_sesion, csrf_token, refresh_token,
        fecha_expiracion, ip_address, user_agent
    ) VALUES (
        p_id_usuario, p_token_sesion, p_csrf_token, p_refresh_token,
        p_fecha_expiracion, p_ip_address, p_user_agent
    ) RETURNING id_sesion INTO v_sesion_id;
    
    -- Actualizar contador de sesiones activas
    UPDATE usuarios 
    SET sesiones_activas = (
        SELECT COUNT(*) 
        FROM sesiones 
        WHERE id_usuario = p_id_usuario 
          AND sesion_activa = TRUE 
          AND fecha_expiracion > CURRENT_TIMESTAMP
    )
    WHERE id_usuario = p_id_usuario;
    
    RETURN v_sesion_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION crear_sesion(INTEGER, VARCHAR, VARCHAR, VARCHAR, TIMESTAMP, VARCHAR, TEXT) IS 
'Crea una nueva sesión, verifica límite y cierra sesión más antigua si es necesario';

-- Función: Cerrar sesión
CREATE OR REPLACE FUNCTION cerrar_sesion(
    p_token_sesion VARCHAR(500),
    p_tipo_cierre VARCHAR(20) DEFAULT 'logout'
)
RETURNS BOOLEAN AS $$
DECLARE
    v_id_usuario INTEGER;
BEGIN
    -- Obtener id_usuario antes de cerrar
    SELECT id_usuario INTO v_id_usuario
    FROM sesiones
    WHERE token_sesion = p_token_sesion
      AND sesion_activa = TRUE;
    
    -- Cerrar sesión
    UPDATE sesiones 
    SET sesion_activa = FALSE,
        fecha_cierre = CURRENT_TIMESTAMP,
        tipo_cierre = p_tipo_cierre
    WHERE token_sesion = p_token_sesion
      AND sesion_activa = TRUE;
    
    -- Actualizar contador de sesiones activas
    IF v_id_usuario IS NOT NULL THEN
        UPDATE usuarios 
        SET sesiones_activas = (
            SELECT COUNT(*) 
            FROM sesiones 
            WHERE id_usuario = v_id_usuario 
              AND sesion_activa = TRUE 
              AND fecha_expiracion > CURRENT_TIMESTAMP
        )
        WHERE id_usuario = v_id_usuario;
    END IF;
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION cerrar_sesion(VARCHAR, VARCHAR) IS 
'Marca una sesión como inactiva y actualiza contador de sesiones activas';

-- Función: Limpiar sesiones expiradas
CREATE OR REPLACE FUNCTION limpiar_sesiones_expiradas()
RETURNS INTEGER AS $$
DECLARE
    v_cerradas INTEGER;
BEGIN
    -- Cerrar sesiones expiradas
    UPDATE sesiones 
    SET sesion_activa = FALSE,
        fecha_cierre = CURRENT_TIMESTAMP,
        tipo_cierre = 'timeout'
    WHERE sesion_activa = TRUE
      AND fecha_expiracion < CURRENT_TIMESTAMP;
    
    GET DIAGNOSTICS v_cerradas = ROW_COUNT;
    
    -- Actualizar contadores de sesiones activas para todos los usuarios afectados
    UPDATE usuarios 
    SET sesiones_activas = (
        SELECT COUNT(*) 
        FROM sesiones 
        WHERE sesiones.id_usuario = usuarios.id_usuario 
          AND sesiones.sesion_activa = TRUE 
          AND sesiones.fecha_expiracion > CURRENT_TIMESTAMP
    )
    WHERE id_usuario IN (
        SELECT DISTINCT id_usuario 
        FROM sesiones 
        WHERE fecha_expiracion < CURRENT_TIMESTAMP
    );
    
    RETURN v_cerradas;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION limpiar_sesiones_expiradas() IS 
'Cierra sesiones cuya fecha_expiracion < NOW(). Ejecutar cada 15 minutos con cron/scheduler';

-- ============================================================================
-- PASO 1.8: CREAR VISTAS ÚTILES
-- ============================================================================

-- Vista: Usuarios con información completa de seguridad
CREATE OR REPLACE VIEW v_usuarios_seguridad AS
SELECT 
    u.id_usuario,
    u.usu_nick,
    u.usu_clave,  -- ✅ Agregado: necesario para validación de contraseña en login
    u.usu_estado,
    u.id_funcionario,
    u.id_grupo,
    CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
    g.des_grupo AS grupo_nombre,
    c.des_cargo AS cargo_nombre,
    u.fecha_ultimo_login,
    u.ip_ultimo_login,
    u.fecha_bloqueo,
    u.bloqueado_hasta,
    u.motivo_bloqueo,
    u.requiere_cambio_password,
    u.fecha_cambio_password,
    u.password_nunca_expira,
    u.dias_validez_password,
    u.max_sesiones_simultaneas,
    u.sesiones_activas,
    -- Campos calculados
    CASE 
        WHEN u.password_nunca_expira THEN FALSE
        WHEN u.fecha_cambio_password IS NULL THEN TRUE
        ELSE (CURRENT_DATE - u.fecha_cambio_password::DATE) > u.dias_validez_password
    END AS password_expirada,
    CASE 
        WHEN u.password_nunca_expira THEN NULL
        WHEN u.fecha_cambio_password IS NULL THEN u.dias_validez_password
        ELSE GREATEST(0, u.dias_validez_password - (CURRENT_DATE - u.fecha_cambio_password::DATE))
    END AS dias_hasta_expiracion,
    esta_usuario_bloqueado(u.id_usuario) AS esta_bloqueado
FROM usuarios u
LEFT JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
LEFT JOIN personas p ON p.id_persona = f.id_persona
LEFT JOIN grupos g ON g.id_grupo = u.id_grupo
LEFT JOIN cargos c ON c.id_cargo = f.id_cargo;

COMMENT ON VIEW v_usuarios_seguridad IS 'Vista con información completa de usuarios para login y seguridad (incluye usu_clave)';

-- ============================================================================
-- CONFIGURAR CONTRASEÑAS SIN EXPIRACIÓN (FIX INTEGRADO)
-- ============================================================================
-- Actualizar todos los usuarios para que las contraseñas no expiren
UPDATE usuarios 
SET 
    password_nunca_expira = TRUE,
    requiere_cambio_password = FALSE,
    fecha_cambio_password = COALESCE(fecha_cambio_password, NOW())
WHERE password_nunca_expira IS NULL OR password_nunca_expira = FALSE;

-- Vista: Resumen de sesiones activas por usuario
CREATE OR REPLACE VIEW v_sesiones_activas AS
SELECT 
    u.id_usuario,
    u.usu_nick,
    CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
    COUNT(s.id_sesion) AS cantidad_sesiones_activas,
    u.max_sesiones_simultaneas,
    MAX(s.fecha_ultimo_ping) AS ultima_actividad,
    STRING_AGG(DISTINCT s.ip_address, ', ') AS ips_conectadas
FROM usuarios u
LEFT JOIN sesiones s ON s.id_usuario = u.id_usuario 
    AND s.sesion_activa = TRUE 
    AND s.fecha_expiracion > CURRENT_TIMESTAMP
LEFT JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
LEFT JOIN personas p ON p.id_persona = f.id_persona
GROUP BY u.id_usuario, u.usu_nick, p.per_nombre, p.per_apellido, u.max_sesiones_simultaneas
HAVING COUNT(s.id_sesion) > 0 OR u.max_sesiones_simultaneas > 0;

COMMENT ON VIEW v_sesiones_activas IS 'Resumen de sesiones activas por usuario con cantidad vs límite';

-- ============================================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN (SEGURIDAD)
-- ============================================================================

-- Índices para consultas frecuentes de seguridad
CREATE INDEX IF NOT EXISTS idx_usuarios_bloqueado ON usuarios(fecha_bloqueo) WHERE fecha_bloqueo IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_usuarios_ultimo_login ON usuarios(fecha_ultimo_login DESC);
CREATE INDEX IF NOT EXISTS idx_login_attempts_fecha_ip ON login_attempts(fecha_intento DESC, ip_address);

-- ============================================================================
-- DATOS INICIALES
-- ============================================================================
-- Grupos (IMPORTANTE: El orden importa - Superadministrador debe ser el primero)
INSERT INTO grupos (des_grupo, est_grupo, usuario_creacion) VALUES 
    ('SUPERADMINISTRADOR', TRUE, 'SISTEMA'),
    ('ADMINISTRADOR', TRUE, 'SISTEMA'),
    ('RECEPCIONISTA', TRUE, 'SISTEMA'),
    ('ESPECIALISTA', TRUE, 'SISTEMA'),
    ('VENTAS', TRUE, 'SISTEMA')
ON CONFLICT (des_grupo) DO NOTHING;

-- Módulos
INSERT INTO modulos (des_modulo, est_modulo, usuario_creacion) VALUES
    ('GESTIÓN DE USUARIO', TRUE, 'SISTEMA'),
    ('AGENDAMIENTO', TRUE, 'SISTEMA'),
    ('CONSULTORIOS', TRUE, 'SISTEMA'),
    ('REPORTES', TRUE, 'SISTEMA'),
    ('VENTAS', TRUE, 'SISTEMA'),
    ('CONFIGURACIÓN', TRUE, 'SISTEMA')
ON CONFLICT (des_modulo) DO NOTHING;

-- Cargos
INSERT INTO cargos (des_cargo, est_cargo, usuario_creacion) VALUES
    ('ADMINISTRADOR', TRUE, 'SISTEMA'),
    ('RECEPCIONISTA', TRUE, 'SISTEMA'),
    ('ESPECIALISTA', TRUE, 'SISTEMA'),
    ('VENTAS', TRUE, 'SISTEMA')
ON CONFLICT (des_cargo) DO NOTHING;
-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================
-- 
-- ESTRUCTURA BÁSICA:
-- 1. La tabla PERSONAS es la base para PACIENTES y FUNCIONARIOS
-- 2. Un FUNCIONARIO puede tener un USUARIO (relación 1:1)
-- 3. Los USUARIOS tienen un GRUPO que define sus permisos
-- 4. Los PERMISOS se asignan por GRUPO y PÁGINA
-- 
-- AUDITORÍA:
-- 5. El campo creacion_usuario y modificacion_usuario en FUNCIONARIOS 
--    y USUARIOS hace referencia a usuarios.id_usuario
-- 6. Para la primera creación, se permite NULL (resuelve auditoría circular)
-- 7. El campo usuario_creacion_nombre mantiene compatibilidad legible
-- 
-- MEJORAS DE SEGURIDAD:
-- 8. Las mejoras son COMPATIBLES HACIA ATRÁS - no rompen código Python actual
-- 9. Los campos nuevos tienen valores por defecto (NULL o DEFAULT)
-- 10. Las funciones pueden usarse opcionalmente desde Python
-- 11. Las vistas facilitan consultas complejas desde Python
-- 
-- INTEGRACIÓN FUTURA EN PYTHON:
-- 12. Modificar login_routes.py para llamar registrar_intento_login()
-- 13. Usar esta_usuario_bloqueado() antes de permitir login
-- 14. Crear registros en sesiones al hacer login exitoso
-- 15. Actualizar fecha_ultimo_login, ip_ultimo_login en usuarios
-- 
-- ============================================================================

-- ============================================================================
-- FIN FASE 2
-- ============================================================================


