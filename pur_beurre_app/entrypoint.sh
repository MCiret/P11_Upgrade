#!/bin/sh

if [ "$DB_CHOICE" = "postgres" ]
then
    echo "Waiting for postgres test..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py migrate

exec "$@"
