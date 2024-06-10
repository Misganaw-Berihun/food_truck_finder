#!/bin/bash
# entrypoint.sh

python manage.py migrate

python manage.py create_superuser

python manage.py upload_csv /code/data/food-truck-data.csv

exec "$@"