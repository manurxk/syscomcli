#!/bin/sh

INTERVAL_SECONDS="${BACKUP_INTERVAL_SECONDS:-86400}"

echo "[$(date -Iseconds)] Servicio de backup iniciado. Intervalo: ${INTERVAL_SECONDS}s, retencion: ${BACKUP_RETENTION_DAYS:-14} dias."

# Esperar a que la BD acepte conexiones (tras reiniciar Docker puede tardar mas que el healthcheck)
until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${POSTGRES_USER}" -d "${DB_NAME}" -q; do
  echo "[$(date -Iseconds)] Esperando a la BD..."
  sleep 3
done

# Backup inmediato al arrancar; un fallo no debe matar el loop
sh /scripts/backup.sh || echo "[$(date -Iseconds)] Backup inicial fallo, se reintenta en el proximo intervalo."

while true; do
  sleep "${INTERVAL_SECONDS}"
  sh /scripts/backup.sh || echo "[$(date -Iseconds)] Backup fallo, se reintenta en el proximo intervalo."
done
