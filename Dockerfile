# Imagen base liviana con Python para ejecutar Django.
FROM python:3.14-slim

# Evita archivos .pyc y fuerza logs sin buffer para verlos en Docker.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias para compilar/conectar el driver MySQL.
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-libmysqlclient-dev gcc pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias Python antes de copiar todo el proyecto para aprovechar cache.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia el código de la aplicación Django y documentación.
COPY . /app

WORKDIR /app/dcrm

# Puerto expuesto por `python manage.py runserver 0.0.0.0:8000`.
EXPOSE 8000

# El entrypoint aplica migraciones y arranca el servidor de desarrollo.
CMD ["sh", "/app/docker/entrypoint.sh"]
