#!/bin/sh
set -eu

# Aplica migraciones pendientes antes de arrancar el servidor.
python manage.py migrate --noinput

# Reemplaza el proceso del shell por runserver para que Docker reciba señales correctamente.
exec python manage.py runserver 0.0.0.0:8000
