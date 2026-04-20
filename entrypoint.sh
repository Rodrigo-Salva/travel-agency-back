#!/bin/bash
set -e

echo "Esperando base de datos..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recopilando archivos estaticos..."
python manage.py collectstatic --noinput

# Cargar datos de prueba solo si la BD esta vacia
USER_COUNT=$(python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.count())" 2>/dev/null || echo "0")
if [ "$USER_COUNT" = "0" ]; then
  echo "Cargando datos de prueba..."
  PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f datos_prueba.sql
  echo "Datos de prueba cargados."
else
  echo "Base de datos ya tiene datos, omitiendo carga inicial."
fi

echo "Iniciando servidor Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
