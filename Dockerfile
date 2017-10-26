##############################################################################
# townapi
# 
# Simple Dockerfile to run the Django application
#
# VERSION          0.0.2
##############################################################################

# Set the base image as Python 3
FROM python:3-onbuild

LABEL maintainer="leamingrad"

# Set environment variables
ENV DJANGO_CONFIGURATION Docker

# Gather static files
WORKDIR townapi
#RUN ["python", "manage.py", "collectstatic", "--noinput"]

WORKDIR ..

# Running this container will start Gunicorn
#CMD ["gunicorn", "-c", "gunicorn_conf.py", "--chdir", "townapi", "townapi.wsgi:application", "--reload"]
CMD ["./docker-entrypoint.sh"]
