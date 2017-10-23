##############################################################################
# townapi
# 
# Simple Dockerfile to run the inbuilt Django web server
#
# VERSION          0.0.1
##############################################################################

# Set the base image as Python 3
FROM python:3

LABEL maintainer="leamingrad"

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT=/townapi/
ENV DJANGO_DIR=./townapi

# Move to the directory we are going to use
RUN mkdir $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

COPY . $PROJECT_ROOT

# Install the required Python packages
ADD requirements.txt $PROJECT_ROOT
RUN pip install -r requirements.txt

# Copy in the Django code
ADD $DJANGO_DIR $PROJECT_ROOT

# Expose a port to listen on
EXPOSE 8000

# Add an entry point that will run the Django development server
ENTRYPOINT ["python", "townapi/manage.py", "runserver", "0.0.0.0:8000"]
