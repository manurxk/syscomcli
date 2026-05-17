-- ============================================================================
-- SCRIPT MAESTRO: CREAR BASE DE DATOS DESDE CERO - SISTEMA CIN
-- ============================================================================
-- Este script crea la base de datos completa del sistema CIN
-- Ejecutar en el siguiente orden:
-- 1. Este script (crear BD)
-- 2. 01_FASE_1_REFERENCIALES_BASICAS.sql
-- 3. 02_FASE_2_SEGURIDAD_USUARIOS.sql
-- 4. 03_FASE_3_PERSONAS_PACIENTES.sql
-- 5. 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql
-- 6. 05_FASE_5_CONSULTORIO.sql
-- 7. 06_FASE_6_REFERENCIALES_VENTAS.sql
-- 8. 07_FASE_7_PRINCIPALES_VENTAS.sql
-- 9. 08_FASE_8_TABLAS_NUEVAS.sql
-- 10. 09_TRIGGERS_AUDITORIA.sql
-- 11. 10_DATOS_INICIALES.sql
-- ============================================================================

-- ============================================================================
-- CONFIGURACIÓN INICIAL
-- ============================================================================

-- Eliminar base de datos si existe (CUIDADO: Esto borra todos los datos)
-- DROP DATABASE IF EXISTS cin_db;

-- Crear base de datos
CREATE DATABASE cin_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Paraguay.1252'
    LC_CTYPE = 'Spanish_Paraguay.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Conectar a la base de datos creada
\c cin_db

-- ============================================================================
-- EXTENSIONES NECESARIAS
-- ============================================================================

-- Habilitar extensión para UUIDs (si se necesita en el futuro)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Habilitar extensión para funciones adicionales
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- Para búsquedas de texto

-- ============================================================================
-- COMENTARIOS
-- ============================================================================

COMMENT ON DATABASE cin_db IS 'Base de datos del Sistema CIN - Centro Integral de Neurodesarrollo';

-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================
-- 
-- 1. Esta base de datos utiliza PostgreSQL
-- 2. La codificación es UTF-8 para soportar caracteres especiales
-- 3. Todas las tablas siguen convenciones específicas:
--    - IDs: id_tabla (SERIAL PRIMARY KEY)
--    - Descripciones: des_tabla (VARCHAR)
--    - Estados: est_tabla (CHAR(1) 'A'/'I' o BOOLEAN)
--    - Auditoría: fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion
-- 4. Los valores monetarios están en Guaraníes (PYG) como INTEGER (sin decimales)
-- 5. Las fechas de auditoría se manejan automáticamente con triggers
-- 6. El usuario de sesión se captura desde la aplicación Flask (session['id_usuario'])
-- 
-- ============================================================================








