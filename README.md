# townapi

This repository is a demonstration of using the Django REST Framework in order to create a simple REST API.

**Table of Contents**

- [Usage](#Usage)
- [Running Tests](#Running-Tests)
- [The Stack](#The-Stack)
- [Available Endpoints](#Available-Endpoints)
    - [/towns](#/towns)
    - [/aggs](#/aggs)
- [Extensions](#Extensions)
    - [Productising](#Productising)
    - [Documentation](#Documentation)
    - [Providing An SDK](#Providing-An-SDK)
    - [Interraction With Other API Types](#Interraction-With-Other-API-Types)
- [Task List](#Task-List)

## Usage

The repository provides a (very simple) Dockerfile to run the API. It can be run using the following commands (from the repository root):

    $> docker-compose build
    $> docker-compose up

This will start to serve requests at `localhost` (port 80).

For details of what endpoints are provided, see [Available Endpoints](#Available-Endpoints).

## Running Tests

**Note:** Running tests is not containerised, so I would suggest doing the following in a virtualenv.

To run unit tests for the different functions of the API, the following commands can be used:

    $> pip3 install -r requirements.txt
    $> cd townapi
    $> python3 manage.py test

For details of this tests are declared, see [the api app tests](testapi/api/tests.py).

## The Stack

This API is built as a Django application, using the Django Rest Framework to provide the REST API. It also makes use of django-filters for filtering, and Markdown for displaying the endpoint help.


The Django application is run using a Gunicorn server as its WSGI host, and an nginx server is used to proxy requests and serve static files. This is all run inside two Docker containers, orchestrated using docker-compose.

This configuration is broadly ready for deployment, but some extra configuration decisions would need to be made depending on the deployment platform, such as:

- What should be done about logging?
- How many worker threads should be used?
- What should be on the 404 page?

Also, a production-ready database would need to be added - probably postgres SQL or similar for this sort of data.

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

### /aggs

Four aggregation endpoints are provided, one for each level of administration. They are accessible at the different sub-domains, as follows:

- `/aggs/regions` - Aggregate by region
- `/aggs/departments` - Aggregate by department
- `/aggs/districts` - Aggregate by district
- `/aggs/towns` - Aggregate by town

For each aggregation, the following JSON record (for example) is provided:

    {
        "code": 1,
        "min_population": 1097,
        "max_population": 56581,
        "avg_population": 12709,
        "town_count": 32,
        "name": "Guadeloupe"
    }

> Note that `name` will be omitted if the administrative level does not have a name in the dataset (at the moment, only Regions and Towns have a name).

For places at lower administrative levels, all parent codes will also be included for reference (for example, Districts will have a `district_code`, a `department_code` and a `code`).

Filtering can be done using the same syntax as the [/towns](#/towns) endpoint, with the following fields available to filter on:
- Region Code
- Department Code
- District Code

Each level of filtering is only available in the lower administrative divisions (for example, Department filtering is only available for District and Town aggregation).

## Extensions

### Productising

This repository contains a very basic API, and some of the code is a bit rough. To get it ready for production, the following would need to be done:

- Tidy up aggregation class code (it should be possible to make use of inheritence more)
    - This may require framework extensions though, so is not urgent
- Add some overview documentation, and link to it

### Documentation

At the moment, the endpoints are documented directly using the DRF's comment-based documentation system. This is good, as it keeps the documentation with the code, so it is harder for them to get out of sync.

To generate more comprehensive human documentation, Sphinx could be used to combine these comments with some handwritten markdown files that give an overview of the API. This could then be served as a static site at a separate location.

Further than that, a Swagger file (and interactive endpoint) could be generated for the API using the django-rest-swagger package with little trouble.

### Providing An SDK

It would be fairly simple to release an SDK for a variety of languages from this endpoint. Once a Swagger file had been generated for the API, then the process of releasing a new SDK language would be:

- Perform basic autogeneration from the Swagger file using swagger-codegen
- Add any additional swagger-codegen classes required to make the output as useful as possible
- Add some unit tests to validate the SDK function against the API (and to make sure the interface does not change too much)
- Add user documentation, including some simple worked examples
- Add compilation and publishing of the above to CI, so that any API changes will cause a new version of the SDK to be built and published

### Interraction With Other API Types

While this repository gives a HTTP REST API, other types of HTTP API could have been used.

Of the most common, a SOAP-XML API would be a viable alternative to REST, as the data that a SOAP API is designed to carry is similar to a REST API. However, doing so would be harder than writing the REST API, as there are fewer frameworks to create them easily (at least few with the ease of use of DRF).

A RPC-based API (XML or JSON) would also be technically possible, but at the size of data object that this repository uses, the benefits of terseness would be minimal.

## Task List

  1. ~~Set up git repository~~
  2. ~~Set up virtualenv for development, and create a new Django/DRF project. Also add the data to be served~~
  3. ~~Flesh out a design for the API application (models, views, serializers etc.)~~
  4. ~~Impliment simple API endpoint to serve town list~~
      - ~~Add a management script to bulk-import the CSV data~~
      - ~~Add tests as objects are added~~
  5. ~~Add enhancements (pagination, filtering etc.)~~
  6. ~~Add aggregation API endpoint~~
  7. ~~Wrap the project in docker for deployment~~
  8. ~~Tidy everything up, and recheck documentation/comments~~
      - ~~Add filtering to the aggs API~~
      - ~~Document possible extensions~~
  9. ~~Move to production ready~~
      - ~~Disable DEBUG~~
