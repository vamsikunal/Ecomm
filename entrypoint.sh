#!/bin/bash

if [ -z "$DB_NAME" ]; then
    echo "Error: Database Name is not provided" >&2
    exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
    echo "Error: Database Password is not provided" >&2
    exit 1
fi

python3 manage.py makemigrations
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Start Gunicorn to serve your Django application
exec gunicorn ecomm.wsgi:application --bind 0.0.0.0:8000

unlink /etc/nginx/sites-enabled/default

nginx -g "daemon off;"