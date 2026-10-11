-- 103_rol_sysclin_app.sql
-- PDF 8 (Seguridad): rol de aplicacion SIN superusuario y con permisos minimos (solo DML).
-- La app (DB_USER en .env) se conecta con sysclin_app; postgres queda solo para
-- administracion, migraciones y backup (POSTGRES_USER/POSTGRES_PASSWORD en .env).
--
-- La contrasena NO se escribe en este archivo (se versiona en git): se pasa como variable de psql.
--   docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1 \
--     -v app_password='<la de DB_PASSWORD en .env>' < migrations/103_rol_sysclin_app.sql
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
