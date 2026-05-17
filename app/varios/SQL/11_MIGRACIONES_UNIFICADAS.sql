-- ============================================================================
-- FASE 11: MIGRACIONES UNIFICADAS
-- ============================================================================
-- Este script unifica todas las migraciones de la Fase 11:
-- 1. Migración de auditoría VARCHAR a INTEGER (compatible con Fase 2)
-- 2. Migración de per_fecha_inscripcion en tabla personas
-- ============================================================================
-- IMPORTANTE: 
-- 1. Ejecutar DESPUÉS de crear todas las tablas (Fases 1-10)
-- 2. Ejecutar ANTES de crear usuarios de ejemplo (Fase 12)
-- 3. Este script crea el usuario SISTEMA con creacion_usuario = NULL (resuelve auditoría circular)
-- 4. Las tablas funcionarios y usuarios NO se migran (ya están en formato INTEGER)
-- ============================================================================

-- ============================================================================
-- PARTE 1: MIGRACIÓN - Agregar columna per_fecha_inscripcion
-- ============================================================================
-- Esta columna es necesaria para que los DAOs funcionen correctamente
-- ============================================================================

DO $$
BEGIN
    -- Verificar si la columna ya existe
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'personas' 
        AND column_name = 'per_fecha_inscripcion'
    ) THEN
        -- Agregar la columna con valor por defecto
        ALTER TABLE personas 
        ADD COLUMN per_fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        
        -- Actualizar registros existentes que tengan NULL
        UPDATE personas 
        SET per_fecha_inscripcion = COALESCE(fecha_creacion, CURRENT_TIMESTAMP)
        WHERE per_fecha_inscripcion IS NULL;
        
        RAISE NOTICE '✅ Columna per_fecha_inscripcion agregada exitosamente a la tabla personas';
    ELSE
        RAISE NOTICE '⏭️  La columna per_fecha_inscripcion ya existe en la tabla personas';
    END IF;
END $$;

-- ============================================================================
-- PARTE 2: Crear Usuario SISTEMA (si no existe)
-- VERSIÓN CORREGIDA: Usa NULL para resolver auditoría circular
-- ============================================================================
-- Este usuario se usa para migraciones, scripts SQL y casos especiales
-- NO se puede usar para login (usu_estado = FALSE)
-- ============================================================================

DO $$
DECLARE
    v_persona_id INTEGER;
    v_funcionario_id INTEGER;
BEGIN
    -- Crear persona SISTEMA
    INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_telefono, usuario_creacion)
    VALUES ('Sistema', 'Automático', '0000000', '0000000000', 'SISTEMA')
    ON CONFLICT (per_cedula) DO NOTHING
    RETURNING id_persona INTO v_persona_id;
    
    -- Si no existe, obtener el ID
    IF v_persona_id IS NULL THEN
        SELECT id_persona INTO v_persona_id 
        FROM personas 
        WHERE per_cedula = '0000000';
    END IF;
    
    -- Crear funcionario SISTEMA con creacion_usuario = NULL (CORREGIDO)
    INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario)
    VALUES (v_persona_id, 1, TRUE, NULL)  -- ✅ NULL en lugar de 1
    ON CONFLICT (id_persona) DO NOTHING
    RETURNING id_funcionario INTO v_funcionario_id;
    
    -- Si no existe, obtener el ID
    IF v_funcionario_id IS NULL THEN
        SELECT id_funcionario INTO v_funcionario_id
        FROM funcionarios
        WHERE id_persona = v_persona_id;
    END IF;
    
    -- Crear usuario SISTEMA con ID fijo = 1 y creacion_usuario = NULL (CORREGIDO)
    INSERT INTO usuarios (id_usuario, usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, creacion_usuario)
    VALUES (1, 'SISTEMA', 'no_login_allowed', v_funcionario_id, 1, FALSE, NULL)  -- ✅ NULL en lugar de 1
    ON CONFLICT (id_usuario) DO UPDATE 
        SET usu_nick = 'SISTEMA',
            usu_estado = FALSE;
    
    -- Actualizar usuario_creacion_nombre para compatibilidad (CORREGIDO)
    UPDATE funcionarios 
    SET usuario_creacion_nombre = 'SISTEMA'
    WHERE id_funcionario = v_funcionario_id AND usuario_creacion_nombre IS NULL;
    
    UPDATE usuarios 
    SET usuario_creacion_nombre = 'SISTEMA'
    WHERE id_usuario = 1 AND usuario_creacion_nombre IS NULL;
    
    RAISE NOTICE '✅ Usuario SISTEMA creado/actualizado con ID: 1 (creacion_usuario = NULL)';
END $$;

-- ============================================================================
-- PARTE 3: FUNCIÓN - Migrar tabla de VARCHAR a INTEGER
-- VERSIÓN CORREGIDA: No fuerza NOT NULL si la columna ya permite NULL
-- ============================================================================

CREATE OR REPLACE FUNCTION migrar_auditoria_varchar_a_integer(
    p_tabla_nombre TEXT,
    p_columna_creacion TEXT DEFAULT 'usuario_creacion',
    p_columna_modificacion TEXT DEFAULT 'usuario_modificacion'
)
RETURNS VOID AS $$
DECLARE
    v_sql TEXT;
    v_usuario_sistema_id INTEGER := 1;
    v_permite_null BOOLEAN;
BEGIN
    -- Verificar que existe la columna VARCHAR
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = p_tabla_nombre 
        AND column_name = p_columna_creacion 
        AND data_type = 'character varying'
    ) THEN
        RAISE NOTICE 'Iniciando migración de tabla: %', p_tabla_nombre;
        
        -- Paso 1: Crear columnas temporales INTEGER
        v_sql := format('ALTER TABLE %I ADD COLUMN IF NOT EXISTS %I_temp INTEGER', 
                       p_tabla_nombre, p_columna_creacion);
        EXECUTE v_sql;
        
        v_sql := format('ALTER TABLE %I ADD COLUMN IF NOT EXISTS %I_temp INTEGER', 
                       p_tabla_nombre, p_columna_modificacion);
        EXECUTE v_sql;
        
        -- Paso 2: Migrar usuario_creacion
        v_sql := format('
            UPDATE %I t
            SET %I_temp = COALESCE(
                (SELECT id_usuario FROM usuarios WHERE usu_nick = t.%I::TEXT),
                %s
            )
        ', p_tabla_nombre, p_columna_creacion, p_columna_creacion, v_usuario_sistema_id);
        EXECUTE v_sql;
        RAISE NOTICE '  ✓ Migrados datos de %', p_columna_creacion;
        
        -- Paso 3: Migrar usuario_modificacion (puede ser NULL)
        v_sql := format('
            UPDATE %I t
            SET %I_temp = CASE 
                WHEN t.%I IS NULL THEN NULL
                ELSE COALESCE(
                    (SELECT id_usuario FROM usuarios WHERE usu_nick = t.%I::TEXT),
                    %s
                )
            END
        ', p_tabla_nombre, p_columna_modificacion, p_columna_modificacion,
           p_columna_modificacion, v_usuario_sistema_id);
        EXECUTE v_sql;
        RAISE NOTICE '  ✓ Migrados datos de %', p_columna_modificacion;
        
        -- Paso 4: Eliminar columnas VARCHAR
        v_sql := format('ALTER TABLE %I DROP COLUMN IF EXISTS %I CASCADE', 
                       p_tabla_nombre, p_columna_creacion);
        EXECUTE v_sql;
        
        v_sql := format('ALTER TABLE %I DROP COLUMN IF EXISTS %I CASCADE', 
                       p_tabla_nombre, p_columna_modificacion);
        EXECUTE v_sql;
        RAISE NOTICE '  ✓ Eliminadas columnas VARCHAR antiguas';
        
        -- Paso 5: Renombrar columnas temporales
        v_sql := format('ALTER TABLE %I RENAME COLUMN %I_temp TO %I', 
                       p_tabla_nombre, p_columna_creacion, p_columna_creacion);
        EXECUTE v_sql;
        
        v_sql := format('ALTER TABLE %I RENAME COLUMN %I_temp TO %I', 
                       p_tabla_nombre, p_columna_modificacion, p_columna_modificacion);
        EXECUTE v_sql;
        RAISE NOTICE '  ✓ Renombradas columnas temporales';
        
        -- Paso 6: Agregar DEFAULT (CORREGIDO: NO forzar NOT NULL si permite NULL)
        -- Verificar si la tabla permite NULL actualmente
        SELECT is_nullable = 'YES' INTO v_permite_null
        FROM information_schema.columns
        WHERE table_name = p_tabla_nombre
        AND column_name = p_columna_creacion;
        
        -- Agregar DEFAULT siempre
        v_sql := format('ALTER TABLE %I ALTER COLUMN %I SET DEFAULT %s', 
                       p_tabla_nombre, p_columna_creacion, v_usuario_sistema_id);
        EXECUTE v_sql;
        
        -- Solo agregar NOT NULL si la tabla originalmente no permitía NULL
        -- (Para tablas nuevas, permitir NULL para resolver auditoría circular)
        IF v_permite_null IS FALSE THEN
            v_sql := format('ALTER TABLE %I ALTER COLUMN %I SET NOT NULL', 
                           p_tabla_nombre, p_columna_creacion);
            EXECUTE v_sql;
            RAISE NOTICE '  ✓ Configurado NOT NULL (tabla original no permitía NULL)';
        ELSE
            RAISE NOTICE '  ✓ Mantenido NULL permitido (compatible con auditoría circular)';
        END IF;
        
        -- Paso 7: Agregar Foreign Keys
        v_sql := format('
            ALTER TABLE %I
            ADD CONSTRAINT fk_%s_%s 
                FOREIGN KEY (%I) REFERENCES usuarios(id_usuario) 
                ON DELETE RESTRICT ON UPDATE CASCADE
        ', p_tabla_nombre, p_tabla_nombre, p_columna_creacion, p_columna_creacion);
        EXECUTE v_sql;
        
        v_sql := format('
            ALTER TABLE %I
            ADD CONSTRAINT fk_%s_%s 
                FOREIGN KEY (%I) REFERENCES usuarios(id_usuario) 
                ON DELETE SET NULL ON UPDATE CASCADE
        ', p_tabla_nombre, p_tabla_nombre, p_columna_modificacion, p_columna_modificacion);
        EXECUTE v_sql;
        RAISE NOTICE '  ✓ Agregadas Foreign Keys';
        
        RAISE NOTICE '✅ Tabla % migrada exitosamente', p_tabla_nombre;
    ELSE
        RAISE NOTICE '⏭️  Tabla % no tiene columna VARCHAR % o ya está migrada', p_tabla_nombre, p_columna_creacion;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION '❌ Error migrando tabla %: % - %', p_tabla_nombre, SQLERRM, SQLSTATE;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 4: MIGRAR TABLAS REFERENCIALES
-- NOTA: funcionarios y usuarios NO se migran (ya están en formato INTEGER)
-- ============================================================================

-- Iniciando migración de tablas referenciales...

SELECT migrar_auditoria_varchar_a_integer('generos');
SELECT migrar_auditoria_varchar_a_integer('estados_civiles');
SELECT migrar_auditoria_varchar_a_integer('ciudades');
SELECT migrar_auditoria_varchar_a_integer('niveles_instruccion');
SELECT migrar_auditoria_varchar_a_integer('profesiones');
SELECT migrar_auditoria_varchar_a_integer('especialidades');
SELECT migrar_auditoria_varchar_a_integer('grupos');
SELECT migrar_auditoria_varchar_a_integer('modulos');
SELECT migrar_auditoria_varchar_a_integer('cargos');
SELECT migrar_auditoria_varchar_a_integer('personas');
SELECT migrar_auditoria_varchar_a_integer('pacientes');
SELECT migrar_auditoria_varchar_a_integer('pacientes_menores');
SELECT migrar_auditoria_varchar_a_integer('especialistas');
SELECT migrar_auditoria_varchar_a_integer('consultas');
SELECT migrar_auditoria_varchar_a_integer('registro_diagnosticos');
SELECT migrar_auditoria_varchar_a_integer('tratamientos');
SELECT migrar_auditoria_varchar_a_integer('anamnesis');
SELECT migrar_auditoria_varchar_a_integer('sintomas');
SELECT migrar_auditoria_varchar_a_integer('signos');
SELECT migrar_auditoria_varchar_a_integer('diagnosticos');
SELECT migrar_auditoria_varchar_a_integer('tipos_analisis');
SELECT migrar_auditoria_varchar_a_integer('tipos_estudios');
SELECT migrar_auditoria_varchar_a_integer('medicamentos');
SELECT migrar_auditoria_varchar_a_integer('tipos_procedimientos');
SELECT migrar_auditoria_varchar_a_integer('tipos_tratamientos');
SELECT migrar_auditoria_varchar_a_integer('formas_cobro');
SELECT migrar_auditoria_varchar_a_integer('marcas_tarjeta');
SELECT migrar_auditoria_varchar_a_integer('entidades_adheridas');
SELECT migrar_auditoria_varchar_a_integer('entidades_emisoras');
SELECT migrar_auditoria_varchar_a_integer('depositos');
SELECT migrar_auditoria_varchar_a_integer('cajas');
SELECT migrar_auditoria_varchar_a_integer('tipos_items');
SELECT migrar_auditoria_varchar_a_integer('tipos_impuestos');
SELECT migrar_auditoria_varchar_a_integer('condiciones_venta');
SELECT migrar_auditoria_varchar_a_integer('tipos_comprobantes');
SELECT migrar_auditoria_varchar_a_integer('estados_factura');
SELECT migrar_auditoria_varchar_a_integer('monedas');
SELECT migrar_auditoria_varchar_a_integer('aperturas_cierre_caja');
SELECT migrar_auditoria_varchar_a_integer('arqueos_caja');
SELECT migrar_auditoria_varchar_a_integer('recaudaciones');
SELECT migrar_auditoria_varchar_a_integer('pedidos');
SELECT migrar_auditoria_varchar_a_integer('facturas');
SELECT migrar_auditoria_varchar_a_integer('cuentas_cobrar');
SELECT migrar_auditoria_varchar_a_integer('cobranzas');
SELECT migrar_auditoria_varchar_a_integer('notas_credito');
SELECT migrar_auditoria_varchar_a_integer('notas_debito');
SELECT migrar_auditoria_varchar_a_integer('presupuestos');
SELECT migrar_auditoria_varchar_a_integer('ordenes_estudios');
SELECT migrar_auditoria_varchar_a_integer('recetas');
SELECT migrar_auditoria_varchar_a_integer('certificados_medicos');
SELECT migrar_auditoria_varchar_a_integer('tipos_certificados_medicos');
SELECT migrar_auditoria_varchar_a_integer('insumos');

-- Migración de tablas referenciales completada

-- ============================================================================
-- PARTE 5: VERIFICACIONES POST-MIGRACIÓN
-- ============================================================================

-- Verificar columna per_fecha_inscripcion
SELECT 
    column_name,
    data_type,
    column_default,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'personas' 
AND column_name = 'per_fecha_inscripcion';

-- Verificar que los registros tienen la columna poblada
SELECT 
    COUNT(*) AS total_personas,
    COUNT(per_fecha_inscripcion) AS con_fecha_inscripcion,
    COUNT(*) - COUNT(per_fecha_inscripcion) AS sin_fecha_inscripcion
FROM personas;

-- Verificar que todas las tablas tienen las columnas correctas
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
AND column_name IN ('usuario_creacion', 'usuario_modificacion', 'creacion_usuario', 'modificacion_usuario')
ORDER BY table_name, column_name;

-- Verificar Foreign Keys creadas
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name,
    ccu.table_name AS foreign_table_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND kcu.column_name IN ('usuario_creacion', 'usuario_modificacion', 'creacion_usuario', 'modificacion_usuario')
ORDER BY tc.table_name;

-- Verificar usuario SISTEMA
SELECT 
    id_usuario,
    usu_nick,
    usu_estado,
    creacion_usuario,
    usuario_creacion_nombre
FROM usuarios
WHERE id_usuario = 1;

-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================
-- 
-- 1. Este script unifica todas las migraciones de la Fase 11
-- 2. Agrega columna per_fecha_inscripcion a tabla personas (requerida por DAOs)
-- 3. Crea usuario SISTEMA con creacion_usuario = NULL (resuelve auditoría circular)
-- 4. Migra tablas existentes de VARCHAR a INTEGER + Foreign Key
-- 5. Las tablas funcionarios y usuarios NO se migran (ya están en formato INTEGER)
-- 6. Para nuevas tablas, usar directamente INTEGER + FK desde el inicio
-- 7. En la aplicación Flask, siempre pasar session['id_usuario'] para auditoría
-- 8. Si un usuario se elimina, ON DELETE RESTRICT previene eliminación si tiene registros creados
-- 9. Para modificacion_usuario, ON DELETE SET NULL permite NULL si el usuario fue eliminado
-- 10. La función NO fuerza NOT NULL si la tabla originalmente permitía NULL
-- 
-- ORDEN DE EJECUCIÓN:
-- 1. Fases 1-10 (crear tablas)
-- 2. Este script (Fase 11 - migraciones)
-- 3. Fase 12 (crear usuarios de ejemplo)
-- 
-- ============================================================================

-- ============================================================================
-- FIN FASE 11 - MIGRACIONES UNIFICADAS
-- ============================================================================

