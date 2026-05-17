#!/bin/bash
set -e

echo "Restoring database from custom dump..."
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" /docker-entrypoint-initdb.d/clinicain.dump || echo "Restoration finished with some warnings (normal for cross-version restores)"
