-- ============================================================================
-- ASIGNAR PERMISOS A SUPERADMINISTRADOR
-- ============================================================================
-- Este script asigna todos los permisos del Administrador al Superadministrador
-- Ejecutar DESPUÉS de crear todas las páginas y asignar permisos al Administrador
-- ============================================================================
-- IMPORTANTE: 
-- 1. Este script debe ejecutarse después de que se hayan creado todas las páginas
-- 2. Debe ejecutarse después de asignar permisos al Administrador
-- 3. Se puede ejecutar múltiples veces sin problemas (usa ON CONFLICT)
-- ============================================================================

-- ============================================================================
-- FUNCIÓN: Asignar permisos al Superadministrador
-- ============================================================================
-- Esta función copia todos los permisos del Administrador al Superadministrador
-- y asigna permisos totales a páginas que no tengan permiso aún
-- ============================================================================

CREATE OR REPLACE FUNCTION asignar_permisos_superadministrador()
RETURNS INTEGER AS $$
DECLARE
    v_id_grupo_superadmin INTEGER;
    v_id_grupo_admin INTEGER;
    v_permisos_copiados INTEGER;
    v_permisos_nuevos INTEGER;
BEGIN
    -- Obtener IDs de grupos
    SELECT id_grupo INTO v_id_grupo_superadmin
    FROM grupos
    WHERE LOWER(des_grupo) = 'superadministrador';
    
    SELECT id_grupo INTO v_id_grupo_admin
    FROM grupos
    WHERE LOWER(des_grupo) = 'administrador';
    
    IF v_id_grupo_superadmin IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Superadministrador. Ejecutar primero 02_FASE_2_SEGURIDAD_USUARIOS.sql';
    END IF;
    
    IF v_id_grupo_admin IS NULL THEN
        RAISE EXCEPTION 'No se encontró el grupo Administrador. Ejecutar primero 02_FASE_2_SEGURIDAD_USUARIOS.sql';
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
    
    GET DIAGNOSTICS v_permisos_nuevos = ROW_COUNT;
    
    RAISE NOTICE '✅ Permisos copiados del Administrador: %', v_permisos_copiados;
    RAISE NOTICE '✅ Permisos nuevos asignados: %', v_permisos_nuevos;
    
    RETURN v_permisos_copiados + v_permisos_nuevos;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION asignar_permisos_superadministrador() IS 
'Asigna todos los permisos del Administrador al Superadministrador y permisos totales a páginas nuevas';

-- ============================================================================
-- EJECUTAR LA FUNCIÓN
-- ============================================================================
-- Ejecutar automáticamente después de crear todas las páginas
-- ============================================================================

DO $$
DECLARE
    v_total_permisos INTEGER;
BEGIN
    -- Verificar que existan páginas antes de asignar permisos
    IF EXISTS (SELECT 1 FROM paginas WHERE est_pagina = TRUE) THEN
        SELECT asignar_permisos_superadministrador() INTO v_total_permisos;
        RAISE NOTICE '✅ Permisos asignados al Superadministrador: %', v_total_permisos;
    ELSE
        RAISE NOTICE '⚠️  No hay páginas creadas aún. Ejecutar este script después de crear las páginas.';
    END IF;
END $$;

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================

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
-- NOTAS
-- ============================================================================
-- 
-- Este script:
-- 1. Crea la función asignar_permisos_superadministrador()
-- 2. Ejecuta la función automáticamente
-- 3. Verifica que los permisos se asignaron correctamente
-- 
-- La función se puede ejecutar manualmente después de crear nuevas páginas:
-- SELECT asignar_permisos_superadministrador();
-- 
-- ============================================================================


