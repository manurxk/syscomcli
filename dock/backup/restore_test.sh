#!/bin/sh
# Prueba de restauracion de un backup cifrado (PDF 8 - Seguridad).
# Descifra el backup con la clave PRIVADA, lo restaura en una base temporal,
# compara filas de tablas clave contra la base real y borra la base temporal.
#
# Se ejecuta a mano desde la raiz del repo (pide la contrasena de la clave privada):
#   docker run --rm -it --network dock_network-tesis --env-file .env \
#     -v "$PWD/backups:/backups:ro" -v "$PWD/dock/backup:/scripts:ro" \
#     -v "<ruta>/backup_privada.asc:/clave/backup_privada.asc:ro" \
#     postgres:17 sh /scripts/restore_test.sh [nombre_del_backup.dump.gpg]
# Sin argumento usa el backup mas reciente.

BACKUP_DIR="/backups"
PRIVATE_KEY="/clave/backup_privada.asc"
TEST_DB="sysclin_restore_test"
TABLAS="usuarios pacientes citas consultas facturas auditoria_sistema"
PLAINFILE="/tmp/restore_test.dump"
export GNUPGHOME="/tmp/gnupg"
export PGHOST="${DB_HOST}" PGPORT="${DB_PORT}" PGUSER="${POSTGRES_USER}" PGPASSWORD="${POSTGRES_PASSWORD}"

if [ -n "$1" ]; then
  ARCHIVO="${BACKUP_DIR}/$1"
else
  ARCHIVO=$(ls -1t "${BACKUP_DIR}"/"${DB_NAME}"_*.dump.gpg 2>/dev/null | head -1)
fi

fallo() {
  echo "RESTAURACION FALLO: $1"
  exit 1
}

# Al salir (ok o error): se borran el dump en claro, la clave importada y la base temporal
trap 'rm -f "${PLAINFILE}"; rm -rf "${GNUPGHOME}"; psql -d postgres -qc "DROP DATABASE IF EXISTS ${TEST_DB}" >/dev/null 2>&1' EXIT

[ -f "${ARCHIVO}" ] || fallo "no se encontro el backup (${ARCHIVO:-ninguno})"
[ -f "${PRIVATE_KEY}" ] || fallo "falta la clave privada montada en ${PRIVATE_KEY}"

echo "Backup a probar: $(basename "${ARCHIVO}")"

mkdir -p -m 700 "${GNUPGHOME}"
gpg --batch --quiet --import "${PRIVATE_KEY}" 2>/dev/null || fallo "no se pudo importar la clave privada"

echo "Descifrando (se pide la contrasena de la clave privada)..."
gpg --quiet --pinentry-mode loopback --output "${PLAINFILE}" --decrypt "${ARCHIVO}" || fallo "no se pudo descifrar"

psql -d postgres -qc "DROP DATABASE IF EXISTS ${TEST_DB}" >/dev/null 2>&1
psql -d postgres -qc "CREATE DATABASE ${TEST_DB}" || fallo "no se pudo crear la base temporal"

echo "Restaurando en ${TEST_DB}..."
pg_restore --exit-on-error -d "${TEST_DB}" "${PLAINFILE}" || fallo "pg_restore devolvio error"

echo ""
printf "%-20s %12s %12s\n" "tabla" "restaurada" "actual"
for t in ${TABLAS}; do
  restaurada=$(psql -d "${TEST_DB}" -Atc "SELECT count(*) FROM ${t}") || fallo "falta la tabla ${t} en el backup"
  actual=$(psql -d "${DB_NAME}" -Atc "SELECT count(*) FROM ${t}")
  printf "%-20s %12s %12s\n" "${t}" "${restaurada}" "${actual}"
done
echo "(diferencias = actividad posterior al backup)"

[ "$(psql -d "${TEST_DB}" -Atc "SELECT count(*) FROM usuarios")" -gt 0 ] || fallo "usuarios vacia en el backup"

echo ""
echo "RESTAURACION OK"
