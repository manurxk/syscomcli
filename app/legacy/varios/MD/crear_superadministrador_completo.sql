-- ============================================================================
-- SCRIPT COMPLETO: CREAR SUPERADMINISTRADOR
-- ============================================================================
-- Este script crea el grupo Superadministrador, la tabla usuarios_roles,
-- migra los datos existentes y crea el usuario Superadministrador con
-- TODOS los permisos del Administrador
-- ============================================================================
-- IMPORTANTE: 
-- 1. Hacer BACKUP de la base de datos antes de ejecutar
-- 2. Reemplazar <HASH_CONTRASEÑA> con el hash real generado
-- 3. Ajustar los IDs según tu base de datos (ciudades, cargos, etc.)
-- ============================================================================

-- ============================================================================
-- PASO 1: CREAR GRUPO SUPERADMINISTRADOR
-- ============================================================================

-- Verificar si ya existe
SELECT id_grupo, des_grupo 
FROM grupos 
WHERE LOWER(des_grupo) = 'superadministrador';

-- Crear el grupo Superadministrador
INSERT INTO grupos (des_grupo, est_grupo, usuario_creacion) 
VALUES ('Superadministrador', TRUE, 'SISTEMA')
ON CONFLICT (des_grupo) DO UPDATE
SET est_grupo = TRUE
RETURNING id_grupo;

-- Guardar el id_grupo que retorna (ejemplo: si retorna 5, usar 5 en los siguientes pasos)
-- ⚠️ IMPORTANTE: Anotar este ID para usarlo después
-- Ejemplo: Si retorna id_grupo = 5, entonces usar 5 en lugar de <ID_GRUPO_SUPERADMIN>

-- Verificar el ID creado
DO $$
DECLARE
    v_id_grupo_superadmin INTEGER;
BEGIN
    SELECT id_grupo INTO v_id_grupo_superadmin
    FROM grupos
    WHERE LOWER(des_grupo) = 'superadministrador';
    
    RAISE NOTICE '✅ Grupo Superadministrador creado con ID: %', v_id_grupo_superadmin;
END $$;

-- ============================================================================
-- PASO 2: CREAR TABLA usuarios_roles (si no existe)
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

-- Crear índices para optimización
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_usuario ON usuarios_roles(id_usuario);
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_grupo ON usuarios_roles(id_grupo);
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_activo ON usuarios_roles(id_usuario, activo) WHERE activo = TRUE;
CREATE INDEX IF NOT EXISTS idx_usuarios_roles_principal ON usuarios_roles(id_usuario, es_rol_principal) WHERE es_rol_principal = TRUE;

DO $$
BEGIN
    RAISE NOTICE '✅ Tabla usuarios_roles creada/verificada';
END $$;

-- ============================================================================
-- PASO 3: MIGRAR DATOS EXISTENTES A usuarios_roles
-- ============================================================================

-- Migrar usuarios existentes a la nueva tabla
INSERT INTO usuarios_roles (
    id_usuario, 
    id_grupo, 
    es_rol_principal, 
    activo, 
    asignado_por,
    fecha_asignacion
)
SELECT 
    id_usuario, 
    id_grupo, 
    TRUE,  -- Todos los roles actuales son principales
    COALESCE(usu_estado, TRUE),  -- Estado del usuario
    1,  -- Asignado por sistema (ajustar si tienes un usuario sistema)
    CURRENT_TIMESTAMP
FROM usuarios
WHERE id_grupo IS NOT NULL
ON CONFLICT (id_usuario, id_grupo) DO NOTHING;

-- Verificar la migración
DO $$
DECLARE
    v_total_migrados INTEGER;
    v_usuarios_originales INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_total_migrados FROM usuarios_roles;
    SELECT COUNT(*) INTO v_usuarios_originales FROM usuarios WHERE id_grupo IS NOT NULL;
    
    RAISE NOTICE '✅ Migración completada: % usuarios migrados de % usuarios originales', 
        v_total_migrados, v_usuarios_originales;
END $$;

-- ============================================================================
-- PASO 4: COPIAR PERMISOS DEL ADMINISTRADOR AL SUPERADMINISTRADOR
-- ============================================================================

-- Obtener el ID del grupo Superadministrador
DO $$
DECLARE
    v_id_grupo_admin INTEGER;
    v_id_grupo_superadmin INTEGER;
    v_permisos_copiados INTEGER;
BEGIN
    -- Obtener IDs de grupos
    SELECT id_grupo INTO v_id_grupo_admin
    FROM grupos
    WHERE LOWER(des_grupo) = 'administrador';
    
    SELECT id_grupo INTO v_id_grupo_superadmin
    FROM grupos
    WHERE LOWER(des_grupo) = 'superadministrador';
    
    IF v_id_grupo_admin IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Administrador';
    END IF;
    
    IF v_id_grupo_superadmin IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Superadministrador';
    END IF;
    
    -- Copiar TODOS los permisos del Administrador al Superadministrador
    INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
    SELECT 
        id_pagina,
        v_id_grupo_superadmin,  -- ID del grupo Superadministrador
        leer,      -- Copiar permiso de leer
        insertar,  -- Copiar permiso de insertar
        editar,    -- Copiar permiso de editar
        borrar     -- Copiar permiso de borrar
    FROM permisos
    WHERE id_grupo = v_id_grupo_admin  -- Permisos del Administrador
    ON CONFLICT (id_pagina, id_grupo) DO UPDATE
    SET leer = EXCLUDED.leer,
        insertar = EXCLUDED.insertar,
        editar = EXCLUDED.editar,
        borrar = EXCLUDED.borrar;
    
    GET DIAGNOSTICS v_permisos_copiados = ROW_COUNT;
    
    RAISE NOTICE '✅ Permisos copiados: % permisos del Administrador al Superadministrador', 
        v_permisos_copiados;
    
    -- Si el Administrador tiene acceso TOTAL (todas las páginas), asegurar que Superadmin también
    -- Asignar permisos TOTALES a todas las páginas activas que no tengan permiso aún
    INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
    SELECT 
        id_pagina,
        v_id_grupo_superadmin,
        TRUE,  -- Leer: SÍ
        TRUE,  -- Insertar: SÍ
        TRUE,  -- Editar: SÍ
        TRUE   -- Borrar: SÍ
    FROM paginas
    WHERE est_pagina = TRUE
      AND id_pagina NOT IN (
          SELECT id_pagina 
          FROM permisos 
          WHERE id_grupo = v_id_grupo_superadmin
      )
    ON CONFLICT (id_pagina, id_grupo) DO NOTHING;
    
    RAISE NOTICE '✅ Permisos totales asignados a todas las páginas activas';
END $$;

-- ============================================================================
-- PASO 5: CREAR USUARIO SUPERADMINISTRADOR
-- ============================================================================
-- IMPORTANTE: Ajustar los valores según tu base de datos
-- ============================================================================

DO $$
DECLARE
    v_persona_superadmin_id INTEGER;
    v_funcionario_superadmin_id INTEGER;
    v_usuario_superadmin_id INTEGER;
    v_id_grupo_superadmin INTEGER;
    v_id_cargo_admin INTEGER;
    v_id_ciudad INTEGER;
    v_id_genero INTEGER;
    v_hash_password VARCHAR(300);
BEGIN
    -- Obtener IDs necesarios
    SELECT id_grupo INTO v_id_grupo_superadmin
    FROM grupos
    WHERE LOWER(des_grupo) = 'superadministrador';
    
    SELECT id_cargo INTO v_id_cargo_admin
    FROM cargos
    WHERE LOWER(des_cargo) = 'administrador'
    LIMIT 1;
    
    -- Obtener primera ciudad disponible (ajustar según tu BD)
    SELECT id_ciudad INTO v_id_ciudad
    FROM ciudades
    WHERE est_ciudad = TRUE
    LIMIT 1;
    
    -- Obtener primer género disponible (ajustar según tu BD)
    SELECT id_genero INTO v_id_genero
    FROM generos
    LIMIT 1;
    
    -- ⚠️ IMPORTANTE: Reemplazar este hash con el generado desde Python
    -- Generar con: from werkzeug.security import generate_password_hash
    -- print(generate_password_hash('tu_contraseña_segura', method='pbkdf2:sha256'))
    v_hash_password := '<HASH_CONTRASEÑA_AQUI>';  -- ⚠️ REEMPLAZAR
    
    IF v_id_grupo_superadmin IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Superadministrador';
    END IF;
    
    -- 1. Crear persona Superadministrador
    INSERT INTO personas (
        per_nombre, 
        per_apellido, 
        per_cedula, 
        per_fecha_nacimiento, 
        id_genero, 
        id_estado_civil, 
        per_telefono, 
        per_correo, 
        per_domicilio,
        id_ciudad, 
        id_ciudad_nacimiento, 
        id_nivel_instruccion, 
        id_profesion
    ) VALUES (
        'Super', 
        'Administrador', 
        '0000000',  -- Cédula especial para superadmin
        '1980-01-01', 
        v_id_genero,  -- Ajustar según tu BD
        NULL, 
        '0980000000', 
        'superadmin@clinica.com', 
        NULL,
        v_id_ciudad,  -- Ajustar según tu BD
        NULL, 
        NULL, 
        NULL
    )
    ON CONFLICT (per_cedula) DO UPDATE
    SET per_nombre = EXCLUDED.per_nombre,
        per_apellido = EXCLUDED.per_apellido
    RETURNING id_persona INTO v_persona_superadmin_id;
    
    IF v_persona_superadmin_id IS NULL THEN
        SELECT id_persona INTO v_persona_superadmin_id
        FROM personas
        WHERE per_cedula = '0000000';
    END IF;
    
    RAISE NOTICE '✅ Persona Superadministrador creada/actualizada con ID: %', v_persona_superadmin_id;
    
    -- 2. Crear funcionario Superadministrador
    -- Usar el cargo Administrador o crear uno nuevo si no existe
    IF v_id_cargo_admin IS NULL THEN
        -- Crear cargo Administrador si no existe
        INSERT INTO cargos (des_cargo, est_cargo, usuario_creacion)
        VALUES ('Administrador', TRUE, 'SISTEMA')
        ON CONFLICT (des_cargo) DO UPDATE SET est_cargo = TRUE
        RETURNING id_cargo INTO v_id_cargo_admin;
        
        IF v_id_cargo_admin IS NULL THEN
            SELECT id_cargo INTO v_id_cargo_admin
            FROM cargos
            WHERE LOWER(des_cargo) = 'administrador';
        END IF;
    END IF;
    
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_superadmin_id, v_id_cargo_admin, TRUE, NULL)  -- NULL porque es creación manual
    ON CONFLICT (id_persona) DO UPDATE
    SET id_cargo = v_id_cargo_admin,
        fun_estado = TRUE
    RETURNING id_funcionario INTO v_funcionario_superadmin_id;
    
    IF v_funcionario_superadmin_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_superadmin_id
        FROM funcionarios
        WHERE id_persona = v_persona_superadmin_id;
    END IF;
    
    RAISE NOTICE '✅ Funcionario Superadministrador creado/actualizado con ID: %', v_funcionario_superadmin_id;
    
    -- 3. Verificar si ya existe un usuario 'superadmin'
    SELECT id_usuario INTO v_usuario_superadmin_id
    FROM usuarios
    WHERE usu_nick = 'superadmin';
    
    -- 3.1 Si no existe usuario 'superadmin', verificar si el funcionario ya tiene usuario
    IF v_usuario_superadmin_id IS NULL THEN
        SELECT id_usuario INTO v_usuario_superadmin_id
        FROM usuarios
        WHERE id_funcionario = v_funcionario_superadmin_id;
        
        -- Si el funcionario ya tiene un usuario, actualizarlo para que sea superadmin
        IF v_usuario_superadmin_id IS NOT NULL THEN
            UPDATE usuarios
            SET usu_nick = 'superadmin',
                usu_clave = v_hash_password,
                id_grupo = v_id_grupo_superadmin,
                usu_estado = TRUE,
                password_nunca_expira = TRUE,
                requiere_cambio_password = FALSE,
                fecha_cambio_password = CURRENT_TIMESTAMP
            WHERE id_usuario = v_usuario_superadmin_id;
            
            RAISE NOTICE '✅ Usuario existente actualizado para Superadministrador con ID: %', v_usuario_superadmin_id;
        ELSE
            -- Si no existe ningún usuario, crear uno nuevo
            INSERT INTO usuarios (
                usu_nick,
                usu_clave,
                id_funcionario,
                id_grupo,
                usu_estado,
                creacion_usuario,
                creacion_fecha,
                creacion_hora,
                password_nunca_expira,
                requiere_cambio_password,
                fecha_cambio_password
            ) VALUES (
                'superadmin',
                v_hash_password,
                v_funcionario_superadmin_id,
                v_id_grupo_superadmin,
                TRUE,
                NULL,
                CURRENT_DATE,
                CURRENT_TIME,
                TRUE,
                FALSE,
                CURRENT_TIMESTAMP
            )
            RETURNING id_usuario INTO v_usuario_superadmin_id;
            
            RAISE NOTICE '✅ Usuario Superadministrador creado con ID: %', v_usuario_superadmin_id;
        END IF;
    ELSE
        -- Si ya existe usuario 'superadmin', actualizarlo
        UPDATE usuarios
        SET usu_clave = v_hash_password,
            id_funcionario = v_funcionario_superadmin_id,
            id_grupo = v_id_grupo_superadmin,
            usu_estado = TRUE,
            password_nunca_expira = TRUE,
            requiere_cambio_password = FALSE,
            fecha_cambio_password = CURRENT_TIMESTAMP
        WHERE id_usuario = v_usuario_superadmin_id;
        
        RAISE NOTICE '✅ Usuario Superadministrador actualizado con ID: %', v_usuario_superadmin_id;
    END IF;
    
    RAISE NOTICE '✅ Usuario Superadministrador creado/actualizado con ID: %', v_usuario_superadmin_id;
    
    -- 4. Asignar rol en usuarios_roles
    INSERT INTO usuarios_roles (
        id_usuario,
        id_grupo,
        es_rol_principal,
        activo,
        asignado_por,
        fecha_asignacion
    ) VALUES (
        v_usuario_superadmin_id,
        v_id_grupo_superadmin,
        TRUE,  -- Es el rol principal
        TRUE,  -- Activo
        NULL,  -- Asignado manualmente desde BD
        CURRENT_TIMESTAMP
    )
    ON CONFLICT (id_usuario, id_grupo) DO UPDATE
    SET es_rol_principal = TRUE,
        activo = TRUE;
    
    RAISE NOTICE '✅ Rol Superadministrador asignado al usuario';
    RAISE NOTICE '';
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ SUPERADMINISTRADOR CREADO EXITOSAMENTE';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Username: superadmin';
    RAISE NOTICE 'ID Usuario: %', v_usuario_superadmin_id;
    RAISE NOTICE 'ID Grupo: %', v_id_grupo_superadmin;
    RAISE NOTICE '========================================';
    
END $$;

-- ============================================================================
-- PASO 6: VERIFICACIONES FINALES
-- ============================================================================

-- Verificar usuario Superadministrador creado
SELECT 
    u.id_usuario,
    u.usu_nick,
    p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
    g.des_grupo AS grupo,
    c.des_cargo AS cargo,
    CASE WHEN u.usu_estado THEN 'Activo' ELSE 'Inactivo' END AS estado,
    u.password_nunca_expira,
    COUNT(ur.id_usuario_rol) AS cantidad_roles
FROM usuarios u
JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
JOIN personas p ON f.id_persona = p.id_persona
JOIN grupos g ON u.id_grupo = g.id_grupo
JOIN cargos c ON f.id_cargo = c.id_cargo
LEFT JOIN usuarios_roles ur ON u.id_usuario = ur.id_usuario AND ur.activo = TRUE
WHERE u.usu_nick = 'superadmin'
GROUP BY u.id_usuario, u.usu_nick, p.per_nombre, p.per_apellido, g.des_grupo, c.des_cargo, u.usu_estado, u.password_nunca_expira;

-- Verificar permisos del Superadministrador
SELECT 
    m.des_modulo AS "Módulo",
    COUNT(*) AS "Total Páginas",
    SUM(CASE WHEN p.leer THEN 1 ELSE 0 END) AS "Ver",
    SUM(CASE WHEN p.insertar THEN 1 ELSE 0 END) AS "Crear",
    SUM(CASE WHEN p.editar THEN 1 ELSE 0 END) AS "Editar",
    SUM(CASE WHEN p.borrar THEN 1 ELSE 0 END) AS "Eliminar"
FROM permisos p
INNER JOIN grupos g ON p.id_grupo = g.id_grupo
INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
WHERE LOWER(g.des_grupo) = 'superadministrador'
  AND pg.est_pagina = TRUE
GROUP BY m.des_modulo
ORDER BY m.des_modulo;

-- Comparar permisos Administrador vs Superadministrador
SELECT 
    m.des_modulo AS "Módulo",
    COUNT(DISTINCT CASE WHEN g.des_grupo = 'ADMINISTRADOR' THEN p.id_pagina END) AS "Páginas Admin",
    COUNT(DISTINCT CASE WHEN g.des_grupo = 'Superadministrador' THEN p.id_pagina END) AS "Páginas Superadmin"
FROM permisos p
INNER JOIN grupos g ON p.id_grupo = g.id_grupo
INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
WHERE g.des_grupo IN ('ADMINISTRADOR', 'Superadministrador')
  AND pg.est_pagina = TRUE
GROUP BY m.des_modulo
ORDER BY m.des_modulo;

-- ============================================================================
-- RESUMEN FINAL
-- ============================================================================
-- 
-- ✅ Grupo Superadministrador creado
-- ✅ Tabla usuarios_roles creada
-- ✅ Datos existentes migrados
-- ✅ Permisos del Administrador copiados al Superadministrador
-- ✅ Usuario Superadministrador creado
-- ✅ Rol asignado en usuarios_roles
-- 
-- ⚠️ IMPORTANTE: 
-- 1. Reemplazar <HASH_CONTRASEÑA_AQUI> con el hash real
-- 2. Verificar que todos los permisos se copiaron correctamente
-- 3. Probar login con el usuario superadmin
-- 4. Cambiar la contraseña después del primer login
-- 
-- ============================================================================

