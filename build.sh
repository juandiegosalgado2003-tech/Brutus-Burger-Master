#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py makemigrations menu pedidos mesas reportes usuarios
python manage.py collectstatic --no-input
python manage.py migrate
