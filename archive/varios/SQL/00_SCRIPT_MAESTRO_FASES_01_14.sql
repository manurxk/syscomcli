-- ============================================================================
-- SCRIPT MAESTRO: ORGANIZACIÓN DE FASES 00 A 16
-- ============================================================================
-- Este script organiza todas las fases de creación de la base de datos
-- desde la fase 00 hasta la fase 16, en el orden correcto de ejecución.
-- ============================================================================
-- IMPORTANTE: 
-- 1. Ejecutar primero: 00_CREAR_BASE_DATOS.sql (crear la BD)
-- 2. Luego ejecutar este script o las fases individualmente en orden
-- 3. Los inserts de datos están integrados en sus fases correspondientes
-- 4. No es necesario ejecutar FASE 15 (ya no existe, inserts integrados)
-- ============================================================================

\echo '============================================================================'
\echo 'SCRIPT MAESTRO: FASES 00 A 16 - ESTRUCTURA Y DATOS DE BASE DE DATOS'
\echo '============================================================================'
\echo ''

-- ============================================================================
-- FASE 01: REFERENCIALES BÁSICAS
-- ============================================================================
\echo 'FASE 01: Creando tablas referenciales básicas...'
\echo '  - Géneros, Estados Civiles, Ciudades'
\echo '  - Niveles de Instrucción, Profesiones, Especialidades'
\i 01_FASE_1_REFERENCIALES_BASICAS.sql
\echo '✅ FASE 01 completada'
\echo ''

-- ============================================================================
-- FASE 02: SEGURIDAD Y USUARIOS (CON SUPERADMINISTRADOR)
-- ============================================================================
\echo 'FASE 02: Creando tablas de seguridad y usuarios...'
\echo '  - Grupos (incluye Superadministrador), Módulos, Cargos'
\echo '  - Personas, Funcionarios, Usuarios'
\echo '  - Páginas, Permisos, Usuarios_Roles'
\echo '  - Tablas de seguridad avanzada (sesiones, login_attempts, etc.)'
\echo '  - Datos iniciales: Grupos, Módulos, Cargos'
\echo '  - Fix: Configuración de contraseñas sin expiración'
\i 02_FASE_2_SEGURIDAD_USUARIOS.sql
\echo '✅ FASE 02 completada'
\echo ''

-- ============================================================================
-- FASE 03: PERSONAS Y PACIENTES
-- ============================================================================
\echo 'FASE 03: Creando tablas de personas y pacientes...'
\echo '  - Pacientes, Pacientes Menores'
\i 03_FASE_3_PERSONAS_PACIENTES.sql
\echo '✅ FASE 03 completada'
\echo ''

-- ============================================================================
-- FASE 04: ESPECIALISTAS Y AGENDAMIENTO
-- ============================================================================
\echo 'FASE 04: Creando tablas de especialistas y agendamiento...'
\echo '  - Especialistas, Especialista-Especialidades'
\echo '  - Consultorios, Días de la Semana'
\echo '  - Agenda Horarios, Estados de Citas, Citas, Recordatorios'
\i 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql
\echo '✅ FASE 04 completada'
\echo ''

-- ============================================================================
-- FASE 05: CONSULTORIO
-- ============================================================================
\echo 'FASE 05: Creando tablas de consultorio...'
\echo '  - Síntomas, Signos, Diagnósticos'
\echo '  - Tipos de Análisis, Tipos de Estudios, Medicamentos'
\echo '  - Tipos de Procedimientos, Tipos de Tratamientos'
\echo '  - Consultas, Registro de Diagnósticos, Procedimientos'
\echo '  - Tratamientos, Registro de Síntomas/Signos, Anamnesis'
\echo '  - Datos iniciales: Tipos de Procedimientos, Estudios, Tratamientos, Medicamentos'
\i 05_FASE_5_CONSULTORIO.sql
\echo '✅ FASE 05 completada'
\echo ''

-- ============================================================================
-- FASE 06: REFERENCIALES VENTAS
-- ============================================================================
\echo 'FASE 06: Creando tablas referenciales de ventas...'
\echo '  - Formas de Cobro, Marcas de Tarjeta'
\echo '  - Entidades Adheridas, Entidades Emisoras'
\echo '  - Depósitos, Cajas, Tipos de Items'
\echo '  - Tipos de Impuestos, Condiciones de Venta'
\echo '  - Tipos de Comprobantes, Estados de Factura, Monedas'
\echo '  - Datos iniciales: Monedas, Formas de Cobro, Marcas de Tarjeta, Tipos de Items, etc.'
\i 06_FASE_6_REFERENCIALES_VENTAS.sql
\echo '✅ FASE 06 completada'
\echo ''

-- ============================================================================
-- FASE 07: PRINCIPALES VENTAS
-- ============================================================================
\echo 'FASE 07: Creando tablas principales de ventas...'
\echo '  - Aperturas y Cierres de Caja, Arqueos de Caja'
\echo '  - Recaudaciones, Pedidos, Facturas'
\echo '  - Cuentas a Cobrar, Cobranzas'
\echo '  - Notas de Crédito, Notas de Débito, Libro de Ventas'
\echo '  - Fix: Función actualizar_totales_facturas()'
\i 07_FASE_7_PRINCIPALES_VENTAS.sql
\echo '✅ FASE 07 completada'
\echo ''

-- ============================================================================
-- FASE 08: TABLAS NUEVAS
-- ============================================================================
\echo 'FASE 08: Creando tablas nuevas adicionales...'
\echo '  - Presupuestos, Órdenes de Estudios'
\echo '  - Recetas, Certificados Médicos'
\echo '  - Insumos, Informes de Agendamiento y Consultorio'
\echo '  - Items Servicios (tabla adicional)'
\echo '  - Datos iniciales: Tipos de Certificados, Insumos'
\i 08_FASE_8_TABLAS_NUEVAS.sql
\echo '✅ FASE 08 completada'
\echo ''

-- ============================================================================
-- FASE 09: TRIGGERS Y AUDITORÍA
-- ============================================================================
\echo 'FASE 09: Creando triggers y sistema de auditoría...'
\echo '  - Triggers de fecha_modificacion'
\echo '  - Validación de cupos en citas'
\echo '  - Registro automático de confirmaciones'
\i 09_TRIGGERS_AUDITORIA.sql
\echo '✅ FASE 09 completada'
\echo ''

-- ============================================================================
-- FASE 10: DATOS INICIALES (OBSOLETO - DATOS YA INTEGRADOS)
-- ============================================================================
\echo 'FASE 10: Datos iniciales ya integrados en FASE 6'
\echo '  ⏭️  Esta fase está obsoleta. Los datos ya están en FASE 6.'
-- \i 10_DATOS_INICIALES.sql
\echo '⏭️  FASE 10 omitida (datos ya integrados en FASE 6)'
\echo ''

-- ============================================================================
-- FASE 11: MIGRACIONES UNIFICADAS
-- ============================================================================
\echo 'FASE 11: Ejecutando migraciones unificadas...'
\echo '  - Agregar columna per_fecha_inscripcion'
\echo '  - Crear usuario SISTEMA'
\echo '  - Migrar auditoría de VARCHAR a INTEGER'
\i 11_MIGRACIONES_UNIFICADAS.sql
\echo '✅ FASE 11 completada'
\echo ''

-- ============================================================================
-- FASE 12: CREAR USUARIOS BÁSICOS (OPCIONAL)
-- ============================================================================
\echo 'FASE 12: Creando usuarios básicos del sistema (OPCIONAL)...'
\echo '  Usuarios básicos: superadmin, admin, recep1, psico1'
\echo '  NOTA: Esta fase es opcional. Puedes ejecutarla manualmente si necesitas usuarios básicos.'
\echo '  Para ejecutar: \i 12_CREAR_USUARIOS_BASICOS.sql'
\echo '  Para usuarios adicionales: \i 12_CREAR_USUARIOS_EJEMPLO_UNIFICADO.sql'
-- \i 12_CREAR_USUARIOS_BASICOS.sql
\echo '⏭️  FASE 12 omitida (opcional)'
\echo ''

-- ============================================================================
-- FASE 13: OTROS (OBSOLETO - CONTENIDO INTEGRADO)
-- ============================================================================
\echo 'FASE 13: Contenido ya integrado en FASE 8 (items_servicios)'
\echo '  ⏭️  Esta fase está obsoleta. El contenido ya está en FASE 8.'
-- \i 13_OTROS.sql
\echo '⏭️  FASE 13 omitida (contenido ya integrado en FASE 8)'
\echo ''

-- ============================================================================
-- FASE 14: EMPRESA, SEDE Y SIFEN
-- ============================================================================
\echo 'FASE 14: Creando tablas de empresa, sede y SIFEN...'
\echo '  - Empresa (datos SIFEN completos)'
\echo '  - Sedes, Timbrados'
\echo '  - Establecimientos, Puntos de Expedición'
\echo '  - Modificaciones a Consultorios y Facturas'
\echo '  - Datos iniciales de prueba (empresa, sede, timbrado, establecimiento, punto de expedición)'
\i 14_FASE_14_EMPRESA_SEDE_SIFEN.sql
\echo '✅ FASE 14 completada'
\echo ''

-- ============================================================================
-- FASE 16: PACIENTE-PROFESIONAL Y DERIVACIONES
-- ============================================================================
\echo 'FASE 16: Creando tablas de paciente-profesional y derivaciones...'
\echo '  - Paciente-Profesional (vincular pacientes con especialistas)'
\echo '  - Derivaciones (derivar pacientes entre especialistas)'
\echo '  - Notificaciones (sistema de notificaciones)'
\echo '  - Soporte para especialistas externos'
\echo '  - Fix: Función crear_derivacion() mejorada'
\i 16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql
\echo '✅ FASE 16 completada'
\echo ''

-- ============================================================================
-- ASIGNAR PERMISOS A SUPERADMINISTRADOR
-- ============================================================================
\echo 'Asignando permisos al Superadministrador...'
\echo '  NOTA: Esto debe ejecutarse DESPUÉS de crear todas las páginas en la aplicación.'
\echo '  Para ejecutar manualmente: \i ASIGNAR_PERMISOS_SUPERADMIN.sql'
-- \i ASIGNAR_PERMISOS_SUPERADMIN.sql
\echo '⏭️  Asignación de permisos omitida (ejecutar después de crear páginas)'
\echo ''

-- ============================================================================
-- VERIFICACIÓN FINAL
-- ============================================================================
\echo '============================================================================'
\echo 'VERIFICACIÓN FINAL DE ESTRUCTURA'
\echo '============================================================================'

-- Verificar grupos creados
DO $$
DECLARE
    v_grupos_count INTEGER;
    v_superadmin_exists BOOLEAN;
BEGIN
    SELECT COUNT(*) INTO v_grupos_count FROM grupos;
    SELECT EXISTS(SELECT 1 FROM grupos WHERE LOWER(des_grupo) = 'superadministrador') INTO v_superadmin_exists;
    
    RAISE NOTICE '✅ Total de grupos creados: %', v_grupos_count;
    
    IF v_superadmin_exists THEN
        RAISE NOTICE '✅ Grupo Superadministrador encontrado';
    ELSE
        RAISE WARNING '⚠️  Grupo Superadministrador NO encontrado';
    END IF;
END $$;

-- Verificar tablas principales
SELECT 
    COUNT(*) AS total_tablas
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';

-- Verificar tabla usuarios_roles
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'usuarios_roles') THEN
        RAISE NOTICE '✅ Tabla usuarios_roles encontrada';
    ELSE
        RAISE WARNING '⚠️  Tabla usuarios_roles NO encontrada';
    END IF;
END $$;

\echo ''
\echo '============================================================================'
\echo '✅ ESTRUCTURA Y DATOS DE BASE DE DATOS COMPLETADOS (FASES 00-16)'
\echo '============================================================================'
\echo ''
\echo 'PRÓXIMOS PASOS:'
\echo '1. Crear usuario Superadministrador (ver crear_superadministrador_completo.sql)'
\echo '2. Crear todas las páginas desde la aplicación'
\echo '3. Ejecutar: ASIGNAR_PERMISOS_SUPERADMIN.sql (después de crear páginas)'
\echo ''
\echo 'NOTA: Los inserts de datos están integrados en sus fases correspondientes:'
\echo '      - FASE 1: Datos referenciales básicos'
\echo '      - FASE 2: Grupos, Módulos, Cargos'
\echo '      - FASE 4: Días de semana, Estados de citas'
\echo '      - FASE 5: Tipos de procedimientos, estudios, tratamientos, medicamentos'
\echo '      - FASE 6: Datos de ventas (monedas, formas de cobro, etc.)'
\echo '      - FASE 8: Tipos de certificados, insumos'
\echo ''
\echo 'FUNCIONALIDADES INCLUIDAS:'
\echo '  ✅ Generación de cupos (FASE 4: funciones obtener_cupos_por_especialista/especialidad)'
\echo '  ✅ Vinculación paciente-especialista (FASE 16: tabla paciente_profesional)'
\echo '  ✅ Agenda horarios con cupos (FASE 4: tabla agenda_horarios)'
\echo '  ✅ Sistema de derivaciones (FASE 16: tabla derivaciones)'
\echo '  ✅ Sistema de notificaciones (FASE 16: tabla notificaciones)'
\echo '  ✅ Soporte para especialistas externos (FASE 16: derivaciones)'
\echo ''

