-- 17_rol_sysclin_app.sql - Rol de la aplicacion y sus permisos
-- (antes migracion 103; PDF 8, Seguridad). Se escribe a mano, no lo genera generar_esquema_base.py.
-- Sin acentos a proposito: se puede aplicar con Get-Content de PowerShell 5.1 sin romper nada.
-- Rol de aplicacion SIN superusuario y con permisos minimos (solo DML).
-- La app (DB_USER en .env) se conecta con sysclin_app; postgres queda solo para
-- administracion, migraciones y backup (POSTGRES_USER/POSTGRES_PASSWORD en .env).
--
-- La contrasena NO se escribe en este archivo (se versiona en git): se pasa como variable de psql.
--   docker cp migrations\17_rol_sysclin_app.sql syscomcli_bd:/tmp/
--   docker exec syscomcli_bd psql -U postgres -d <base> -v ON_ERROR_STOP=1 -v app_password='<DB_PASSWORD del .env>' -f /tmp/17_rol_sysclin_app.sql
-- OJO: sysclin_app es un rol de TODO el servidor PostgreSQL. Si en el servidor hay otra base del sistema,
-- usar la misma contrasena del .env (si no, esa base deja de poder conectarse).
-- Idempotente: se puede volver a ejecutar (por ejemplo, para rotar la contrasena).

\if :{?app_password}
\else
  \echo 'ERROR: falta -v app_password=... (ver cabecera del archivo)'
  \quit
\endif

-- 1. Rol de login sin privilegios de administracion
SELECT 'CREATE ROLE sysclin_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'sysclin_app') \gexec

ALTER ROLE sysclin_app PASSWORD :'app_password';

COMMENT ON ROLE sysclin_app IS
    'Rol de la aplicacion Sysclin: solo SELECT/INSERT/UPDATE/DELETE, uso de secuencias y ejecucion de funciones. Sin DDL, TRUNCATE ni superusuario. La administracion usa postgres.';

-- 2. Conexion a la base: solo la app (postgres es superusuario y no necesita GRANT)
SELECT format('REVOKE CONNECT, TEMPORARY ON DATABASE %I FROM PUBLIC', current_database()) \gexec
SELECT format('GRANT CONNECT ON DATABASE %I TO sysclin_app', current_database()) \gexec

-- 3. Permisos minimos sobre los objetos existentes (sin CREATE, TRUNCATE, REFERENCES ni TRIGGER)
GRANT USAGE ON SCHEMA public TO sysclin_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO sysclin_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO sysclin_app;
GRANT EXECUTE ON ALL ROUTINES IN SCHEMA public TO sysclin_app;

-- 4. Mismos permisos para lo que postgres cree despues (vistas, procedimientos, auditoria: PDF 4, 5, 9)
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sysclin_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO sysclin_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT EXECUTE ON ROUTINES TO sysclin_app;

-- 5. Hora de Paraguay en la base (PDF 9 + 6, paso 1b). pg_dump no guarda esta configuracion, por eso va aca.
--    Sin esto la base trabaja en UTC y now() / CURRENT_TIMESTAMP guardan la hora 3 h adelantada.
--    Vale para todas las conexiones nuevas a esta base (sysclin_app y postgres).
SELECT format('ALTER DATABASE %I SET timezone = %L', current_database(), 'America/Asuncion') \gexec

-- 6. Auditoria inmutable (PDF 9 + 6, paso 2). Va despues del punto 3 porque ese da UPDATE/DELETE en todas las tablas.
--    auditoria_transacciones: la app solo LEE; la escribe el trigger fn_auditar_cambios (SECURITY DEFINER).
--    auditoria_sistema: la app inserta eventos, pero no puede modificarlos ni borrarlos.
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON auditoria_transacciones FROM sysclin_app;
REVOKE UPDATE, DELETE, TRUNCATE ON auditoria_sistema FROM sysclin_app;
REVOKE ALL ON FUNCTION fn_auditar_cambios() FROM PUBLIC, sysclin_app;
