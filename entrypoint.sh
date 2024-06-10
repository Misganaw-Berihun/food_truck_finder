#!/bin/bash
# entrypoint.sh

python manage.py migrate

python manage.py create_superuser

exec "$@"