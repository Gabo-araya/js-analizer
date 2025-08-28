FROM python:3.11-alpine3.19

WORKDIR /app

# Dependencias mínimas del sistema
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    rm -rf /var/cache/apk/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de aplicación
COPY . .

# Crear base de datos
RUN touch analysis.db && chmod 666 analysis.db

# Variables de entorno de producción
ENV FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "dashboard.py"]