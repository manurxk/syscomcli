#!/bin/sh
# Certificado autofirmado para HTTPS en desarrollo (localhost). En el servidor se usa Let's Encrypt.
# Se ejecuta desde la raiz del repo (no requiere openssl en Windows):
#   docker run --rm -v "${PWD}\dock\nginx:/nginx" postgres:17 sh /nginx/generar_cert_local.sh
set -e

CERTS_DIR="/nginx/certs"
mkdir -p "${CERTS_DIR}"

openssl req -x509 -nodes -newkey rsa:2048 -days 825 \
  -keyout "${CERTS_DIR}/privkey.pem" \
  -out "${CERTS_DIR}/fullchain.pem" \
  -subj "/CN=localhost/O=Sysclin (desarrollo)" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

echo "Certificado autofirmado creado en dock/nginx/certs/ (valido 825 dias):"
openssl x509 -in "${CERTS_DIR}/fullchain.pem" -noout -subject -enddate
