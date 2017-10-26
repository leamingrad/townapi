#!/bin/bash
# Gather static files and then run gunicorn
python townapi/manage.py collectstatic --noinput
gunicorn -c gunicorn_conf.py --chdir townapi townapi.wsgi:application --reload
