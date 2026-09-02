#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.1
done

echo "PostgreSQL started"

psql() { PGPASSWORD="$DB_PASSWORD" command psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" "$@"; }

# A database registered on the shared server starts out empty; load the site's prepared
# initial state once, as the site's own role, before migrations move it forward.
if [ -z "$(psql -tAc "select to_regclass('public.django_migrations')")" ]; then
  echo "Empty database, loading docker/init.sql.gz"
  gunzip -c docker/init.sql.gz | psql -v ON_ERROR_STOP=1
fi

python manage.py migrate

python manage.py db_worker &

exec "$@"
