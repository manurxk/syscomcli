#!/bin/sh
set -e

BACKUP_DIR="/backups"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
PUBLIC_KEY="/scripts/keys/backup_pub.asc"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="${DB_NAME}_${TIMESTAMP}.dump.gpg"
TMPFILE="${BACKUP_DIR}/.${FILENAME}.tmp"
# El dump en claro vive solo dentro del contenedor (/tmp), nunca en el volumen de backups
PLAINFILE="/tmp/${DB_NAME}_${TIMESTAMP}.dump"
export GNUPGHOME="/tmp/gnupg"

# Ante cualquier salida (ok o error) no quedan restos en claro ni archivos a medio escribir
trap 'rm -f "${PLAINFILE}" "${TMPFILE}"' EXIT

echo "[$(date -Iseconds)] Iniciando backup cifrado de ${DB_NAME}..."

if [ ! -f "${PUBLIC_KEY}" ]; then
  echo "[$(date -Iseconds)] ERROR: falta la clave publica ${PUBLIC_KEY}, no se crea backup sin cifrar."
  exit 1
fi

# Credenciales de administracion (POSTGRES_*): DB_USER es el rol de la app (sysclin_app), con permisos minimos
if ! PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
  -h "${DB_HOST}" \
  -p "${DB_PORT}" \
  -U "${POSTGRES_USER}" \
  -d "${DB_NAME}" \
  -Fc \
  -f "${PLAINFILE}"; then
  echo "[$(date -Iseconds)] ERROR: pg_dump fallo, no se creo backup."
  exit 1
fi

# Cifrado asimetrico: con la clave publica se cifra; solo la privada (fuera del servidor) descifra
mkdir -p -m 700 "${GNUPGHOME}"
if ! gpg --batch --yes --quiet --trust-model always \
  --recipient-file "${PUBLIC_KEY}" \
  --output "${TMPFILE}" \
  --encrypt "${PLAINFILE}"; then
  echo "[$(date -Iseconds)] ERROR: el cifrado fallo, no se creo backup."
  exit 1
fi

mv "${TMPFILE}" "${BACKUP_DIR}/${FILENAME}"
echo "[$(date -Iseconds)] Backup creado: ${FILENAME} ($(du -h "${BACKUP_DIR}/${FILENAME}" | cut -f1))"

echo "[$(date -Iseconds)] Rotando backups con mas de ${RETENTION_DAYS} dias..."
find "${BACKUP_DIR}" -name "${DB_NAME}_*.dump.gpg" -type f -mtime "+${RETENTION_DAYS}" -print -delete

echo "[$(date -Iseconds)] Backup finalizado. Backups actuales:"
ls -lh "${BACKUP_DIR}"/*.dump.gpg 2>/dev/null || echo "(ninguno)"
