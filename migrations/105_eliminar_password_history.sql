-- 105_eliminar_password_history.sql
-- PDF 8 (Seguridad): Sysclin NO guarda historial de contraseñas (decisión del usuario, 2026-10-11).
--
-- Por qué se elimina:
--   1. Riesgo: conservar el hash de cada contraseña anterior arma un depósito de contraseñas viejas.
--      Si la base se filtra, esos hashes se pueden atacar sin apuro, y la gente suele reutilizar
--      variantes de sus contraseñas en otros sistemas (correo, banca).
--   2. No protegía nada: la comprobación "no reutilizar las últimas 5" comparaba el hash de la
--      contraseña nueva (con sal aleatoria) contra los guardados, así que nunca coincidía.
--   3. Sin uso: el código que la escribía y leía se quitó el 2026-10-11 (AuthDao y la tarea
--      programada de las 2 AM). Ninguna vista, función, trigger ni clave foránea depende de ella.
-- La defensa contra contraseñas débiles o reutilizadas es: complejidad + vencimiento de 90 días
-- + MFA + bloqueo escalonado (ver 08_politicas_seguridad.md, §3.1).
--
-- Antes de aplicarla se hizo un backup: sysclin_bd_20261011_184100.dump.gpg
--   Get-Content migrations\105_eliminar_password_history.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;
DROP TABLE IF EXISTS public.password_history;   -- su secuencia (id_history) se elimina con ella
COMMIT;
