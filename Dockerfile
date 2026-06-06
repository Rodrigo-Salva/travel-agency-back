FROM python:3.11-slim

# Seguridad: usuario no-root
RUN useradd --create-home appuser

WORKDIR /app

# Dependencias del sistema para psycopg2 y Pillow
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn "uvicorn[standard]"

# Copiar código (sin venv, sin .env, gracias a .dockerignore)
COPY . .

# Permisos al usuario no-root
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
ENTRYPOINT ["sh", "entrypoint.sh"]
