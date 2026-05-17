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

# Comando para ejecutar la aplicación con soporte para debug remoto
# El script se encarga de esperar a que la BD esté lista si es necesario, 
# pero aquí usamos el comando directo con debugpy
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "run.py"]
