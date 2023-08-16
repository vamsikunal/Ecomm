#!/bin/bash

if [ -z "$DB_CRED" ]; then
    echo "HELL2"
else
    username=$(echo "$DB_CRED" | sed -n 's/.*"username":"\([^"]*\)".*/\1/p')
    password=$(echo "$DB_CRED" | sed -n 's/.*"password":"\([^"]*\)".*/\1/p')

    export DB_USER="$username"
    export DB_PASSWORD="$password"
fi
# Extract username and password using string manipulation

if [ -z "$DB_USER" ]; then
    echo "Error: Database user is not provided" >&2
    exit 1
fi


if [ -z "$DB_PASSWORD" ]; then
    echo "Error: Database Password is not provided" >&2
    exit 1
fi

python3 database_create.py
python3 manage.py makemigrations
python3 manage.py collectstatic --noinput

# Apply database migrations
python3 manage.py migrate --noinput

# Start Gunicorn to serve your Django application
exec gunicorn ecomm.wsgi:application --bind 0.0.0.0:8000

unlink /etc/nginx/sites-enabled/default

nginx -g "daemon off;"