-- 18_superadmin_inicial.sql — Primer usuario del sistema
-- PDF 3 (Base de datos), paso 6 / decisión D1: primer usuario de una base nueva, con rol SUPERADMIN.
-- Es el último paso al crear una base nueva (después de 00 a 17). Se escribe a mano, no lo genera
-- generar_esquema_base.py.
--
-- La contraseña NO se escribe en este archivo (se versiona en git): se pasa ya convertida en hash,
-- como variable de psql (mismo criterio que 17_rol_sysclin_app.sql). El hash se genera con el
-- mismo método que usa el sistema (pbkdf2:sha256); pide la contraseña sin mostrarla:
--   docker exec -it syscomcli_app python -c "import getpass; from werkzeug.security import generate_password_hash as g; print(g(getpass.getpass('Contraseña: '), method='pbkdf2:sha256'))"
-- Después:
--   docker cp migrations\18_superadmin_inicial.sql syscomcli_bd:/tmp/
--   docker exec syscomcli_bd psql -U postgres -d <base_nueva> -v ON_ERROR_STOP=1 -v nick=<usuario> -v clave_hash='<hash>' -f /tmp/18_superadmin_inicial.sql
-- El usuario queda obligado a cambiar la contraseña en el primer ingreso. No tiene funcionario
-- asociado (igual que el superadministrador actual); el MFA se activa después desde el sistema.

\if :{?nick}
\else
  \echo 'ERROR: falta -v nick=... (ver cabecera del archivo)'
  \quit
\endif
\if :{?clave_hash}
\else
  \echo 'ERROR: falta -v clave_hash=... (ver cabecera del archivo)'
  \quit
\endif

BEGIN;

INSERT INTO usuarios (usu_nick, usu_clave, requiere_cambio_clave)
VALUES (:'nick', :'clave_hash', TRUE);

INSERT INTO usuarios_roles (id_usuario, id_rol, es_rol_principal)
SELECT currval('usuarios_id_usuario_seq'), id_rol, TRUE
FROM roles
WHERE cod_rol = 'SUPERADMIN';

COMMIT;
