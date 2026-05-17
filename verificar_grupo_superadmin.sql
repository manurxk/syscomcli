-- ============================================================================
-- SCRIPT: Verificar Grupo Superadministrador
-- ============================================================================
-- Ejecutar este script para verificar el ID del grupo Superadministrador
-- y el usuario superadmin
-- ============================================================================

-- 1. Verificar todos los grupos
SELECT 
    id_grupo,
    des_grupo,
    est_grupo
FROM grupos
ORDER BY id_grupo;

-- 2. Verificar específicamente el grupo Superadministrador
SELECT 
    id_grupo,
    des_grupo,
    est_grupo
FROM grupos
WHERE LOWER(des_grupo) = 'superadministrador';

-- 3. Verificar usuario superadmin y su grupo
SELECT 
    u.id_usuario,
    u.usu_nick,
    u.id_grupo,
    g.des_grupo AS nombre_grupo,
    u.usu_estado
FROM usuarios u
JOIN grupos g ON u.id_grupo = g.id_grupo
WHERE u.usu_nick = 'superadmin';

-- 4. Verificar roles del usuario superadmin en usuarios_roles
SELECT 
    ur.id_usuario_rol,
    ur.id_usuario,
    ur.id_grupo,
    g.des_grupo,
    ur.es_rol_principal,
    ur.activo
FROM usuarios_roles ur
JOIN grupos g ON ur.id_grupo = g.id_grupo
JOIN usuarios u ON ur.id_usuario = u.id_usuario
WHERE u.usu_nick = 'superadmin';

-- 5. Comparar: ¿El usuario tiene id_grupo = 1 o = 5?
SELECT 
    CASE 
        WHEN u.id_grupo = 1 THEN 'El usuario superadmin tiene id_grupo = 1 (Administrador)'
        WHEN u.id_grupo = 5 THEN 'El usuario superadmin tiene id_grupo = 5 (Superadministrador)'
        ELSE CONCAT('El usuario superadmin tiene id_grupo = ', u.id_grupo, ' (Verificar)')
    END AS estado
FROM usuarios u
WHERE u.usu_nick = 'superadmin';


