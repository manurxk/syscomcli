-- ============================================================================
-- FASE 12: CREAR USUARIOS BÁSICOS DEL SISTEMA
-- ============================================================================
-- Este script crea los usuarios básicos necesarios para el funcionamiento:
-- 1. Superadministrador (superadmin)
-- 2. Administrador (admin)
-- 3. Recepcionista (recep1)
-- 4. Especialista (psico1)
-- ============================================================================
-- Ejecutar después de: 11_MIGRACIONES_UNIFICADAS.sql
-- ============================================================================
-- IMPORTANTE: 
-- 1. Las contraseñas por defecto son: superadmin123, admin123, recep123, psico123
-- 2. DEBES cambiar estas contraseñas en producción
-- 3. Las contraseñas deben ser hasheadas con werkzeug.security.generate_password_hash
-- 4. Para generar nuevas contraseñas, usar Python:
--    from werkzeug.security import generate_password_hash
--    print(generate_password_hash('tu_contraseña', method='pbkdf2:sha256'))
-- ============================================================================
-- NOTA: Este script asume que ya existen:
-- - Usuario SISTEMA con id_usuario = 1 (creado en Fase 11)
-- - Cargos: 1=Administrador, 2=Recepcionista, 3=Especialista
-- - Grupos: 1=SUPERADMINISTRADOR, 2=ADMINISTRADOR, 3=RECEPCIONISTA, 4=ESPECIALISTA
-- - Especialidades: al menos una especialidad (ej: id_especialidad = 1)
-- ============================================================================

\echo '============================================================================'
\echo 'FASE 12: CREANDO USUARIOS BÁSICOS DEL SISTEMA'
\echo '============================================================================'
\echo ''

-- ============================================================================
-- 1. SUPERADMINISTRADOR
-- ============================================================================

DO $$
DECLARE
    v_persona_superadmin_id INTEGER;
    v_funcionario_superadmin_id INTEGER;
    v_grupo_superadmin_id INTEGER;
BEGIN
    -- Obtener ID del grupo Superadministrador
    SELECT id_grupo INTO v_grupo_superadmin_id
    FROM grupos
    WHERE LOWER(des_grupo) = 'superadministrador';
    
    IF v_grupo_superadmin_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Superadministrador. Ejecutar primero 02_FASE_2_SEGURIDAD_USUARIOS.sql';
    END IF;
    
    -- Crear persona Superadministrador
    INSERT INTO personas (
        per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
        id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
        id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion
    ) VALUES (
        'Super', 'Administrador', '0000001', '1980-01-01',
        1, 1, '0980000001', 'superadmin@clinica.com', NULL,
        1, NULL, NULL, NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_superadmin_id;
    
    IF v_persona_superadmin_id IS NULL THEN
        SELECT id_persona INTO v_persona_superadmin_id
        FROM personas
        WHERE per_cedula = '0000001';
    END IF;
    
    -- Crear funcionario Superadministrador
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_superadmin_id, 1, TRUE, 1)  -- Cargo 1 = Administrador
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = 1,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_superadmin_id;
    
    IF v_funcionario_superadmin_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_superadmin_id
        FROM funcionarios
        WHERE id_persona = v_persona_superadmin_id;
    END IF;
    
    -- Crear usuario Superadministrador
    -- Contraseña: superadmin123
    -- NOTA: Reemplazar 'REEMPLAZAR_CON_HASH_REAL' con el hash generado
    INSERT INTO usuarios (
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, 
        creacion_usuario, creacion_fecha, creacion_hora,
        password_nunca_expira, requiere_cambio_password
    ) VALUES (
        'superadmin',
        'pbkdf2:sha256:1000000$TDvRAIUy1m1y9K0R$3cb1a5f8879ff27b6c43839524f4d4ddbbc545dd6a8045c41f62a290a1c64b58',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_superadmin_id,
        v_grupo_superadmin_id,  -- Grupo Superadministrador
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME,
        TRUE,  -- Password nunca expira
        FALSE
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = v_grupo_superadmin_id,
        usu_estado = TRUE,
        password_nunca_expira = TRUE;
    
    RAISE NOTICE '✅ Usuario Superadministrador creado/actualizado: superadmin (contraseña: superadmin123)';
END $$;

-- ============================================================================
-- 2. ADMINISTRADOR
-- ============================================================================

DO $$
DECLARE
    v_persona_admin_id INTEGER;
    v_funcionario_admin_id INTEGER;
    v_grupo_admin_id INTEGER;
BEGIN
    -- Obtener ID del grupo Administrador
    SELECT id_grupo INTO v_grupo_admin_id
    FROM grupos
    WHERE LOWER(des_grupo) = 'administrador';
    
    IF v_grupo_admin_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Administrador. Ejecutar primero 02_FASE_2_SEGURIDAD_USUARIOS.sql';
    END IF;
    
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
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, 
        creacion_usuario, creacion_fecha, creacion_hora,
        password_nunca_expira, requiere_cambio_password
    ) VALUES (
        'admin',
        'pbkdf2:sha256:1000000$TDvRAIUy1m1y9K0R$3cb1a5f8879ff27b6c43839524f4d4ddbbc545dd6a8045c41f62a290a1c64b58',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_admin_id,
        v_grupo_admin_id,  -- Grupo Administrador
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME,
        TRUE,  -- Password nunca expira
        FALSE
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = v_grupo_admin_id,
        usu_estado = TRUE,
        password_nunca_expira = TRUE;
    
    RAISE NOTICE '✅ Usuario Administrador creado/actualizado: admin (contraseña: admin123)';
END $$;

-- ============================================================================
-- 3. RECEPCIONISTA
-- ============================================================================

DO $$
DECLARE
    v_persona_recep_id INTEGER;
    v_funcionario_recep_id INTEGER;
    v_grupo_recep_id INTEGER;
BEGIN
    -- Obtener ID del grupo Recepcionista
    SELECT id_grupo INTO v_grupo_recep_id
    FROM grupos
    WHERE LOWER(des_grupo) = 'recepcionista';
    
    IF v_grupo_recep_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Recepcionista. Ejecutar primero 02_FASE_2_SEGURIDAD_USUARIOS.sql';
    END IF;
    
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
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, 
        creacion_usuario, creacion_fecha, creacion_hora,
        password_nunca_expira, requiere_cambio_password
    ) VALUES (
        'recep1',
        'pbkdf2:sha256:1000000$TDvRAIUy1m1y9K0R$3cb1a5f8879ff27b6c43839524f4d4ddbbc545dd6a8045c41f62a290a1c64b58',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_recep_id,
        v_grupo_recep_id,  -- Grupo Recepcionista
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME,
        TRUE,  -- Password nunca expira
        FALSE
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = v_grupo_recep_id,
        usu_estado = TRUE,
        password_nunca_expira = TRUE;
    
    RAISE NOTICE '✅ Usuario Recepcionista creado/actualizado: recep1 (contraseña: recep123)';
END $$;

-- ============================================================================
-- 4. ESPECIALISTA (PSICÓLOGO)
-- ============================================================================

DO $$
DECLARE
    v_persona_psico_id INTEGER;
    v_funcionario_psico_id INTEGER;
    v_especialista_id INTEGER;
    v_grupo_especialista_id INTEGER;
BEGIN
    -- Obtener ID del grupo Especialista
    SELECT id_grupo INTO v_grupo_especialista_id
    FROM grupos
    WHERE LOWER(des_grupo) = 'especialista';
    
    IF v_grupo_especialista_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Especialista. Ejecutar primero 02_FASE_2_SEGURIDAD_USUARIOS.sql';
    END IF;
    
    -- Crear persona Especialista (Psicólogo)
    INSERT INTO personas (
        per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
        id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
        id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion
    ) VALUES (
        'Jorge', 'Benítez', '3456789', '1985-08-10',
        1, 2, '0981333333', 'psico@clinica.com', NULL,
        1, NULL, NULL, NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_psico_id;
    
    IF v_persona_psico_id IS NULL THEN
        SELECT id_persona INTO v_persona_psico_id
        FROM personas
        WHERE per_cedula = '3456789';
    END IF;
    
    -- Crear funcionario Especialista
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_psico_id, 3, TRUE, 1)  -- Cargo 3 = Especialista
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = 3,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_psico_id;
    
    IF v_funcionario_psico_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_psico_id
        FROM funcionarios
        WHERE id_persona = v_persona_psico_id;
    END IF;
    
    -- Crear especialista (Psicólogo)
    INSERT INTO especialistas (id_funcionario, esp_matricula, esp_color_agenda)
    VALUES (v_funcionario_psico_id, 'PSI-001', '#3498db')
    ON CONFLICT (esp_matricula) DO UPDATE
    SET id_funcionario = EXCLUDED.id_funcionario,
        esp_color_agenda = EXCLUDED.esp_color_agenda
    RETURNING id_especialista INTO v_especialista_id;
    
    IF v_especialista_id IS NULL THEN
        SELECT id_especialista INTO v_especialista_id
        FROM especialistas
        WHERE esp_matricula = 'PSI-001';
    END IF;
    
    -- Asignar especialidad al especialista (Psicología Clínica)
    INSERT INTO especialista_especialidades (id_especialista, id_especialidad)
    VALUES (v_especialista_id, 1)  -- Especialidad 1 = Psicología Clínica
    ON CONFLICT (id_especialista, id_especialidad) DO NOTHING;
    
    -- Crear usuario Especialista
    -- Contraseña: psico123
    INSERT INTO usuarios (
        usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, 
        creacion_usuario, creacion_fecha, creacion_hora,
        password_nunca_expira, requiere_cambio_password
    ) VALUES (
        'psico1',
        'pbkdf2:sha256:1000000$TDvRAIUy1m1y9K0R$3cb1a5f8879ff27b6c43839524f4d4ddbbc545dd6a8045c41f62a290a1c64b58',  -- ⚠️ REEMPLAZAR con hash real
        v_funcionario_psico_id,
        v_grupo_especialista_id,  -- Grupo Especialista
        TRUE,
        1,  -- Creado por usuario SISTEMA
        CURRENT_DATE,
        CURRENT_TIME,
        TRUE,  -- Password nunca expira
        FALSE
    )
    ON CONFLICT (usu_nick) DO UPDATE
    SET usu_clave = EXCLUDED.usu_clave,
        id_grupo = v_grupo_especialista_id,
        usu_estado = TRUE,
        password_nunca_expira = TRUE;
    
    RAISE NOTICE '✅ Usuario Especialista creado/actualizado: psico1 (contraseña: psico123)';
    RAISE NOTICE '✅ Especialista creado con matrícula: PSI-001';
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
WHERE u.usu_nick IN ('superadmin', 'admin', 'recep1', 'psico1')
ORDER BY 
    CASE g.des_grupo
        WHEN 'SUPERADMINISTRADOR' THEN 1
        WHEN 'ADMINISTRADOR' THEN 2
        WHEN 'RECEPCIONISTA' THEN 3
        WHEN 'ESPECIALISTA' THEN 4
    END;

\echo ''
\echo '============================================================================'
\echo 'RESUMEN DE USUARIOS CREADOS'
\echo '============================================================================'
\echo ''
\echo '1. SUPERADMINISTRADOR'
\echo '   Usuario: superadmin'
\echo '   Contraseña: superadmin123'
\echo '   Grupo: Superadministrador'
\echo '   Cargo: Administrador'
\echo '   Nombre: Super Administrador'
\echo '   Cédula: 0000001'
\echo ''
\echo '2. ADMINISTRADOR'
\echo '   Usuario: admin'
\echo '   Contraseña: admin123'
\echo '   Grupo: Administrador'
\echo '   Cargo: Administrador'
\echo '   Nombre: Carlos Ramírez'
\echo '   Cédula: 1234567'
\echo ''
\echo '3. RECEPCIONISTA'
\echo '   Usuario: recep1'
\echo '   Contraseña: recep123'
\echo '   Grupo: Recepcionista'
\echo '   Cargo: Recepcionista'
\echo '   Nombre: Lucía Gómez'
\echo '   Cédula: 2345678'
\echo ''
\echo '4. ESPECIALISTA'
\echo '   Usuario: psico1'
\echo '   Contraseña: psico123'
\echo '   Grupo: Especialista'
\echo '   Cargo: Especialista'
\echo '   Nombre: Jorge Benítez'
\echo '   Cédula: 3456789'
\echo '   Matrícula: PSI-001'
\echo '   Especialidad: Psicología Clínica'
\echo ''
\echo '============================================================================'
\echo 'IMPORTANTE: GENERAR HASHES DE CONTRASEÑAS'
\echo '============================================================================'
\echo ''
\echo 'ANTES DE EJECUTAR ESTE SCRIPT:'
\echo ''
\echo '1. Ejecutar el script Python para generar los hashes:'
\echo '   python generar_hashes_contraseñas.py'
\echo ''
\echo '2. Copiar los hashes generados y reemplazarlos en este archivo donde dice:'
\echo '   "REEMPLAZAR_CON_HASH_REAL"'
\echo ''
\echo '3. O usar directamente desde Python:'
\echo '   from werkzeug.security import generate_password_hash'
\echo '   print("superadmin:", generate_password_hash("superadmin123", method="pbkdf2:sha256"))'
\echo '   print("admin:", generate_password_hash("admin123", method="pbkdf2:sha256"))'
\echo '   print("recep1:", generate_password_hash("recep123", method="pbkdf2:sha256"))'
\echo '   print("psico1:", generate_password_hash("psico123", method="pbkdf2:sha256"))'
\echo ''
\echo '4. CAMBIAR CONTRASEÑAS EN PRODUCCIÓN después de crear los usuarios'
\echo ''
\echo '============================================================================'
\echo '✅ FASE 12 COMPLETADA - USUARIOS BÁSICOS CREADOS'
\echo '============================================================================'
\echo ''

