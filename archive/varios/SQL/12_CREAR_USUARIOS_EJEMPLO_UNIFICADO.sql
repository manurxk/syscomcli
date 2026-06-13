-- ============================================================================
-- FASE 12: CREAR USUARIOS DE EJEMPLO - UNIFICADO
-- ============================================================================
-- Este script crea usuarios de ejemplo para el sistema:
-- 1. Administrador (admin)
-- 2. Recepcionista (recep1)
-- 3. Psicólogo 1 (psico1)
-- 4. Psicólogo 2 (psico2)
-- 5. Vendedor (ventas1)
-- ============================================================================
-- Ejecutar después de: 11_MIGRACIONES_UNIFICADAS.sql
-- ============================================================================
-- IMPORTANTE: 
-- 1. Las contraseñas por defecto son: admin123, recep123, psico123, psico2123, ventas123
-- 2. DEBES cambiar estas contraseñas en producción
-- 3. Las contraseñas están hasheadas con werkzeug.security.generate_password_hash
-- 4. Para generar nuevas contraseñas, usar Python:
--    python generar_hashes_contraseñas.py
--    O desde Python:
--    from werkzeug.security import generate_password_hash
--    print(generate_password_hash('tu_contraseña', method='pbkdf2:sha256'))
-- ============================================================================
-- NOTA: Este script asume que ya existen:
-- - Usuario SISTEMA con id_usuario = 1 (creado en Fase 11)
-- - Cargos: 1=Administrador, 2=Recepcionista, 3=Especialista, 4=Ventas
-- - Grupos: 1=Administrador, 2=Recepcionista, 3=Especialista, 4=Ventas
-- - Especialidades: al menos una especialidad (ej: id_especialidad = 1)
-- ============================================================================

-- ============================================================================
-- 1. ADMINISTRADOR
-- ============================================================================

DO $$
DECLARE
    v_persona_admin_id INTEGER;
    v_funcionario_admin_id INTEGER;
BEGIN
    -- Crear persona Administrador
    INSERT INTO personas (
        per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
        id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
        id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion
    ) VALUES (
        'Carlos', 'Ramírez', '1234567', '1980-01-15',
        1, 1, '0981111111', 'admin@clinica.com', NULL,
        1, NULL, NULL, NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_admin_id;
    
    IF v_persona_admin_id IS NULL THEN
        SELECT id_persona INTO v_persona_admin_id
        FROM personas
        WHERE per_cedula = '1234567';
    END IF;
    
    -- Crear funcionario Administrador
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_admin_id, 1, TRUE, 1)  -- Cargo 1 = Administrador
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = 1,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_admin_id;
    
    IF v_funcionario_admin_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_admin_id
        FROM funcionarios
        WHERE id_persona = v_persona_admin_id;
    END IF;
    
    -- Crear usuario Administrador
    -- Contraseña: admin123
    INSERT INTO usuarios (
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, creacion_usuario, creacion_fecha, creacion_hora
    ) VALUES (
        'admin',
        'pbkdf2:sha256:600000$REEMPLAZAR_CON_HASH_REAL$REEMPLAZAR_CON_HASH_REAL',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_admin_id,
        1,  -- Grupo 1 = Administrador
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = 1,
        usu_estado = TRUE;
    
    RAISE NOTICE '✅ Usuario Administrador creado/actualizado: admin (contraseña: admin123)';
END $$;

-- ============================================================================
-- 2. RECEPCIONISTA
-- ============================================================================

DO $$
DECLARE
    v_persona_recep_id INTEGER;
    v_funcionario_recep_id INTEGER;
BEGIN
    -- Crear persona Recepcionista
    INSERT INTO personas (
        per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
        id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
        id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion
    ) VALUES (
        'Lucía', 'Gómez', '2345678', '1990-05-20',
        2, 1, '0981222222', 'recep@clinica.com', NULL,
        1, NULL, NULL, NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_recep_id;
    
    IF v_persona_recep_id IS NULL THEN
        SELECT id_persona INTO v_persona_recep_id
        FROM personas
        WHERE per_cedula = '2345678';
    END IF;
    
    -- Crear funcionario Recepcionista
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_recep_id, 2, TRUE, 1)  -- Cargo 2 = Recepcionista
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = 2,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_recep_id;
    
    IF v_funcionario_recep_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_recep_id
        FROM funcionarios
        WHERE id_persona = v_persona_recep_id;
    END IF;
    
    -- Crear usuario Recepcionista
    -- Contraseña: recep123
    INSERT INTO usuarios (
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, creacion_usuario, creacion_fecha, creacion_hora
    ) VALUES (
        'recep1',
        'pbkdf2:sha256:600000$REEMPLAZAR_CON_HASH_REAL$REEMPLAZAR_CON_HASH_REAL',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_recep_id,
        2,  -- Grupo 2 = Recepcionista
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = 2,
        usu_estado = TRUE;
    
    RAISE NOTICE '✅ Usuario Recepcionista creado/actualizado: recep1 (contraseña: recep123)';
END $$;

-- ============================================================================
-- 3. PSICÓLOGO 1
-- ============================================================================

DO $$
DECLARE
    v_persona_psico1_id INTEGER;
    v_funcionario_psico1_id INTEGER;
    v_especialista1_id INTEGER;
BEGIN
    -- Crear persona Psicólogo 1
    INSERT INTO personas (
        per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
        id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
        id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion
    ) VALUES (
        'Jorge', 'Benítez', '3456789', '1985-08-10',
        1, 2, '0981333333', 'psico1@clinica.com', NULL,
        1, NULL, NULL, NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_psico1_id;
    
    IF v_persona_psico1_id IS NULL THEN
        SELECT id_persona INTO v_persona_psico1_id
        FROM personas
        WHERE per_cedula = '3456789';
    END IF;
    
    -- Crear funcionario Especialista (Psicólogo 1)
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_psico1_id, 3, TRUE, 1)  -- Cargo 3 = Especialista
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = 3,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_psico1_id;
    
    IF v_funcionario_psico1_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_psico1_id
        FROM funcionarios
        WHERE id_persona = v_persona_psico1_id;
    END IF;
    
    -- Crear especialista (Psicólogo 1)
    INSERT INTO especialistas (id_funcionario, esp_matricula, esp_color_agenda)
    VALUES (v_funcionario_psico1_id, 'PSI-001', '#3498db')
    ON CONFLICT (esp_matricula) DO UPDATE
    SET id_funcionario = EXCLUDED.id_funcionario,
        esp_color_agenda = EXCLUDED.esp_color_agenda
    RETURNING id_especialista INTO v_especialista1_id;
    
    IF v_especialista1_id IS NULL THEN
        SELECT id_especialista INTO v_especialista1_id
        FROM especialistas
        WHERE esp_matricula = 'PSI-001';
    END IF;
    
    -- Asignar especialidad al especialista (Psicología Clínica)
    INSERT INTO especialista_especialidades (id_especialista, id_especialidad)
    VALUES (v_especialista1_id, 1)  -- Especialidad 1 = Psicología Clínica
    ON CONFLICT (id_especialista, id_especialidad) DO NOTHING;
    
    -- Crear usuario Psicólogo 1
    -- Contraseña: psico123
    INSERT INTO usuarios (
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, creacion_usuario, creacion_fecha, creacion_hora
    ) VALUES (
        'psico1',
        'pbkdf2:sha256:600000$REEMPLAZAR_CON_HASH_REAL$REEMPLAZAR_CON_HASH_REAL',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_psico1_id,
        3,  -- Grupo 3 = Especialista
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = 3,
        usu_estado = TRUE;
    
    RAISE NOTICE '✅ Usuario Psicólogo 1 creado/actualizado: psico1 (contraseña: psico123)';
    RAISE NOTICE '✅ Especialista creado con matrícula: PSI-001';
END $$;

-- ============================================================================
-- 4. PSICÓLOGO 2
-- ============================================================================

DO $$
DECLARE
    v_persona_psico2_id INTEGER;
    v_funcionario_psico2_id INTEGER;
    v_especialista2_id INTEGER;
BEGIN
    -- Crear persona Psicólogo 2
    INSERT INTO personas (
        per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
        id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
        id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion
    ) VALUES (
        'María', 'Fernández', '4567890', '1988-03-25',
        2, 1, '0981444444', 'psico2@clinica.com', NULL,
        1, NULL, NULL, NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_psico2_id;
    
    IF v_persona_psico2_id IS NULL THEN
        SELECT id_persona INTO v_persona_psico2_id
        FROM personas
        WHERE per_cedula = '4567890';
    END IF;
    
    -- Crear funcionario Especialista (Psicólogo 2)
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_psico2_id, 3, TRUE, 1)  -- Cargo 3 = Especialista
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = 3,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_psico2_id;
    
    IF v_funcionario_psico2_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_psico2_id
        FROM funcionarios
        WHERE id_persona = v_persona_psico2_id;
    END IF;
    
    -- Crear especialista (Psicólogo 2)
    INSERT INTO especialistas (id_funcionario, esp_matricula, esp_color_agenda)
    VALUES (v_funcionario_psico2_id, 'PSI-002', '#e74c3c')
    ON CONFLICT (esp_matricula) DO UPDATE
    SET id_funcionario = EXCLUDED.id_funcionario,
        esp_color_agenda = EXCLUDED.esp_color_agenda
    RETURNING id_especialista INTO v_especialista2_id;
    
    IF v_especialista2_id IS NULL THEN
        SELECT id_especialista INTO v_especialista2_id
        FROM especialistas
        WHERE esp_matricula = 'PSI-002';
    END IF;
    
    -- Asignar especialidad al especialista (Psicología Clínica)
    INSERT INTO especialista_especialidades (id_especialista, id_especialidad)
    VALUES (v_especialista2_id, 1)  -- Especialidad 1 = Psicología Clínica
    ON CONFLICT (id_especialista, id_especialidad) DO NOTHING;
    
    -- Crear usuario Psicólogo 2
    -- Contraseña: psico2123
    INSERT INTO usuarios (
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, creacion_usuario, creacion_fecha, creacion_hora
    ) VALUES (
        'psico2',
        'pbkdf2:sha256:600000$REEMPLAZAR_CON_HASH_REAL$REEMPLAZAR_CON_HASH_REAL',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_psico2_id,
        3,  -- Grupo 3 = Especialista
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = 3,
        usu_estado = TRUE;
    
    RAISE NOTICE '✅ Usuario Psicólogo 2 creado/actualizado: psico2 (contraseña: psico2123)';
    RAISE NOTICE '✅ Especialista creado con matrícula: PSI-002';
END $$;

-- ============================================================================
-- 5. VENDEDOR
-- ============================================================================

DO $$
DECLARE
    v_persona_ventas_id INTEGER;
    v_funcionario_ventas_id INTEGER;
BEGIN
    -- Crear persona Vendedor
    INSERT INTO personas (
        per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
        id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
        id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion
    ) VALUES (
        'Roberto', 'Torres', '5678901', '1992-07-15',
        1, 1, '0981555555', 'ventas@clinica.com', NULL,
        1, NULL, NULL, NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_ventas_id;
    
    IF v_persona_ventas_id IS NULL THEN
        SELECT id_persona INTO v_persona_ventas_id
        FROM personas
        WHERE per_cedula = '5678901';
    END IF;
    
    -- Crear funcionario Vendedor
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_ventas_id, 4, TRUE, 1)  -- Cargo 4 = Vendedor
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = 4,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_ventas_id;
    
    IF v_funcionario_ventas_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_ventas_id
        FROM funcionarios
        WHERE id_persona = v_persona_ventas_id;
    END IF;
    
    -- Crear usuario Vendedor
    -- Contraseña: ventas123
    INSERT INTO usuarios (
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, creacion_usuario, creacion_fecha, creacion_hora
    ) VALUES (
        'ventas1',
        'pbkdf2:sha256:600000$REEMPLAZAR_CON_HASH_REAL$REEMPLAZAR_CON_HASH_REAL',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_ventas_id,
        4,  -- Grupo 4 = Ventas
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = 4,
        usu_estado = TRUE;
    
    RAISE NOTICE '✅ Usuario Vendedor creado/actualizado: ventas1 (contraseña: ventas123)';
END $$;

-- ============================================================================
-- VERIFICAR USUARIOS CREADOS
-- ============================================================================

SELECT 
    u.id_usuario,
    u.usu_nick,
    p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
    c.des_cargo AS cargo,
    g.des_grupo AS grupo,
    CASE WHEN u.usu_estado THEN 'Activo' ELSE 'Inactivo' END AS estado,
    CASE 
        WHEN EXISTS (SELECT 1 FROM especialistas e WHERE e.id_funcionario = f.id_funcionario) 
        THEN (SELECT esp_matricula FROM especialistas WHERE id_funcionario = f.id_funcionario)
        ELSE NULL
    END AS matricula_especialista
FROM usuarios u
JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
JOIN personas p ON f.id_persona = p.id_persona
JOIN cargos c ON f.id_cargo = c.id_cargo
JOIN grupos g ON u.id_grupo = g.id_grupo
WHERE u.usu_nick IN ('admin', 'recep1', 'psico1', 'psico2', 'ventas1')
ORDER BY u.id_usuario;

-- ============================================================================
-- RESUMEN DE USUARIOS CREADOS
-- ============================================================================
-- 
-- 1. ADMINISTRADOR
--    Usuario: admin
--    Contraseña: admin123
--    Grupo: Administrador (id_grupo = 1)
--    Cargo: Administrador (id_cargo = 1)
--    Nombre: Carlos Ramírez
--    Cédula: 1234567
--    Email: admin@clinica.com
--    Teléfono: 0981111111
-- 
-- 2. RECEPCIONISTA
--    Usuario: recep1
--    Contraseña: recep123
--    Grupo: Recepcionista (id_grupo = 2)
--    Cargo: Recepcionista (id_cargo = 2)
--    Nombre: Lucía Gómez
--    Cédula: 2345678
--    Email: recep@clinica.com
--    Teléfono: 0981222222
-- 
-- 3. PSICÓLOGO 1
--    Usuario: psico1
--    Contraseña: psico123
--    Grupo: Especialista (id_grupo = 3)
--    Cargo: Especialista (id_cargo = 3)
--    Nombre: Jorge Benítez
--    Cédula: 3456789
--    Email: psico1@clinica.com
--    Teléfono: 0981333333
--    Matrícula: PSI-001
--    Especialidad: Psicología Clínica (id_especialidad = 1)
--    Color Agenda: #3498db (azul)
-- 
-- 4. PSICÓLOGO 2
--    Usuario: psico2
--    Contraseña: psico2123
--    Grupo: Especialista (id_grupo = 3)
--    Cargo: Especialista (id_cargo = 3)
--    Nombre: María Fernández
--    Cédula: 4567890
--    Email: psico2@clinica.com
--    Teléfono: 0981444444
--    Matrícula: PSI-002
--    Especialidad: Psicología Clínica (id_especialidad = 1)
--    Color Agenda: #e74c3c (rojo)
-- 
-- 5. VENDEDOR
--    Usuario: ventas1
--    Contraseña: ventas123
--    Grupo: Ventas (id_grupo = 4)
--    Cargo: Vendedor (id_cargo = 4)
--    Nombre: Roberto Torres
--    Cédula: 5678901
--    Email: ventas@clinica.com
--    Teléfono: 0981555555
-- 
-- ============================================================================
-- IMPORTANTE: GENERAR HASHES DE CONTRASEÑAS
-- ============================================================================
-- 
-- ANTES DE EJECUTAR ESTE SCRIPT:
-- 
-- 1. Ejecutar el script Python para generar los hashes:
--    python generar_hashes_contraseñas.py
-- 
-- 2. Copiar los hashes generados y reemplazarlos en este archivo donde dice:
--    'REEMPLAZAR_CON_HASH_REAL'
-- 
-- 3. O usar directamente desde Python:
--    from werkzeug.security import generate_password_hash
--    print("admin:", generate_password_hash('admin123', method='pbkdf2:sha256'))
--    print("recep1:", generate_password_hash('recep123', method='pbkdf2:sha256'))
--    print("psico1:", generate_password_hash('psico123', method='pbkdf2:sha256'))
--    print("psico2:", generate_password_hash('psico2123', method='pbkdf2:sha256'))
--    print("ventas1:", generate_password_hash('ventas123', method='pbkdf2:sha256'))
-- 
-- 4. CAMBIAR CONTRASEÑAS EN PRODUCCIÓN después de crear los usuarios
-- 
-- ============================================================================
-- FIN FASE 12 - CREAR USUARIOS DE EJEMPLO
-- ============================================================================









