#!/bin/bash
# Quick bash script to get django ready and then run it behind Gunicorn
# (this is required for static file serving to work)
python manage.py collectstatic --noinput

# Setup logging
touch /var/log/srv/gunicorn.log
touch /var/log/srv/access.log
tail -n 0 -f /var/log/srv/*.log &

echo Starting Gunicorn server
exec gunicorn townapi.wsgi:application \
    --name townapi \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/var/log/srv/gunicorn.log \
    --access-logfile=/var/log/srv/access.log \
    "$@"
