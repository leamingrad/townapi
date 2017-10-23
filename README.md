# townapi

This repository is a demonstration of using the Django REST Framework in order to create a simple REST API.

## Usage

The repository provides a (very simple) Dockerfile to run the API. It can be run using the following commands:

    $> docker build -t leamingrad/townapi .
    $> docker run -p 8000:8000 leamingrad/townapi

For details of what endpoints are provided, see [Available Endpoints][Available Endpoints].

## Available Endpoints

The API provides two endpoints that can be queried (every other URL will return a 404).

### /towns

A list of French towns and cities is available at `/towns`.

## Tasks

  1. ~~Set up git repository~~
  2. ~~Set up virtualenv for development, and create a new Django/DRF project. Also add the data to be served~~
  3. ~~Flesh out a design for the API application (models, views, serializers etc.)~~
  4. ~~Impliment simple API endpoint to serve town list~~
      - ~~Add a management script to bulk-import the CSV data~~
      - ~~Add tests as objects are added~~
  5. Add enhancements (pagination, filtering etc.)
  6. Add aggregation API endpoint
  7. Wrap the project in docker for deployment
  8. Tidy everything up, and recheck documentation/comments
