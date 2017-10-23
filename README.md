# townapi

This repository is a demonstration of using the Django REST Framework in order to create a simple REST API.

## Usage

The repository provides a (very simple) Dockerfile to run the API. It can be run using the following commands:

    $> docker build -t leamingrad/townapi .
    $> docker run -p 8000:8000 leamingrad/townapi

For details of what endpoints are provided, see [Available Endpoints](#Available-Endpoints).

## Running Tests

To run unit tests for the different functions of the API, the following commands can be used

## Available Endpoints

The API provides two endpoints that can be queried (every other URL will return a 404). Visiting the endpoint in the browser will give a version of the below documentation.

### /towns

A list of French towns and cities is available at `/towns`. For each town, a JSON record is provided with information about the town and its region, department and district. An example JSON record is as follows:

    {
        "town_code": "1",
        "town_name": "L' Abergement-Clémenciat",
        "population": 785,
        "district_code": "2",
        "department_code": "1",
        "region_code": "84",
        "region_name": "Auvergne-Rhône-Alpes"
    }

Limit-offset pagination is provided, with the following syntax:

    /towns?limit=<LIMIT>&offset=<OFFSET>

(`<LIMIT>` is set to 100 by default).

Ordering can be set using the syntax:

    /towns?ordering=[-]<FIELD>

This will sort by the value of `<FIELD>` (all fields can be used here). If the `-` is included, then the ordering will be in descending order, and if it is omitted then it will be in ascending order.

Filtering can be done using the syntax:

    /towns?<FILTER>=<VALUE>

Multiple filters can be chained using `&` characters. Available filters are:

- Region Code (`region_code`)
- Department Code (`department_code`)
- District Code (`district_code`)
- Exact Population (`population`)
- Minimum Population (`min_population`)
- Maximum Population (`max_population`)

Pagination, ordering and filtering can be accessed using the browser GUI.

## Task List

  1. ~~Set up git repository~~
  2. ~~Set up virtualenv for development, and create a new Django/DRF project. Also add the data to be served~~
  3. ~~Flesh out a design for the API application (models, views, serializers etc.)~~
  4. ~~Impliment simple API endpoint to serve town list~~
      - ~~Add a management script to bulk-import the CSV data~~
      - ~~Add tests as objects are added~~
  5. Add enhancements (pagination, filtering etc.)
  6. ~~Add aggregation API endpoint~~
  7. ~~Wrap the project in docker for deployment~~
  8. Tidy everything up, and recheck documentation/comments
