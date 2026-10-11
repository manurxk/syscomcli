# Usar una imagen de Python ligera
FROM python:3.12-slim

# Evitar que Python genere archivos .pyc y habilitar unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para psycopg2, weasyprint y reportlab
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    shared-mime-info \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    gettext \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir debugpy

# Copiar el resto del código
COPY . .

# Exponer los puertos de Flask y Debugpy
EXPOSE 5000 5678

# Arranque segun FLASK_DEBUG (.env):
#   1 (desarrollo): debugpy + servidor de desarrollo de Flask con recarga automatica.
#   0 (servidor):   gunicorn. UN solo worker (con hilos): el scheduler de run.py arranca
#                   por proceso, y con mas workers se duplicarian los recordatorios por WhatsApp.
CMD ["sh", "-c", "if [ \"$FLASK_DEBUG\" = \"1\" ]; then exec python -m debugpy --listen 0.0.0.0:5678 run.py; else exec gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 8 --timeout 120 --access-logfile - --error-logfile - run:app; fi"]
