#!/bin/bash

if [ -z "$DB_NAME" ]; then
    echo "Error: Database Name is not provided" >&2
    exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
    echo "Error: Database Password is not provided" >&2
    exit 1
fi

# Run Django database migrations
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
# Start the Django development server
python3 manage.py runserver 0.0.0.0:8000
