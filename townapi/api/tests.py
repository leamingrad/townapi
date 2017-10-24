"""
    tests.py

    This file contains unit tests for the api application. The general testing
    strategy is as follows:

    - Validate the objects, views and serializers at a high-level
    - Do not bother to test Django itself (it is one of the most field-hardened
      packages out there), unless a specific bug has been found. For example,
      there is no need to test that the validation we set on a model's fields
      is obeyed, unless we have written the field class ourselves. Also,
      there is no need to test basic CRUD operations.
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .management.commands._utils import (get_towns_from_csv,
                                         save_town_and_parents_to_db)
from .models import Department, District, Region, Town


class ModelTestCase(TestCase):
    """
        Check that all towns in the CSV list are validated successfully (i.e.
        we haven't made our validation too restrictive).

        We do not need to check basic CRUD function here, as Django is already
        field-hardened.
    """

    def setUp(self):
        """
            Make sure that we are working with a clean database.
        """
        self.assertEqual(Department.objects.count(), 0)
        self.assertEqual(District.objects.count(), 0)
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(Town.objects.count(), 0)

    def test_csv_import(self):
        """
            Check that all towns in the CSV file are valid.
        """
        towns = get_towns_from_csv()

        for town in towns:
            save_town_and_parents_to_db(town)

        self.assertEqual(Town.objects.count(), len(towns))


class TownsViewTestCase(TestCase):
    """ Test suite for the Town api view (available at /towns). """

    def setUp(self):
        """
            Define the test API Client to use and check that we are working
            with a clean database
        """
        self.assertEqual(Department.objects.count(), 0)
        self.assertEqual(District.objects.count(), 0)
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(Town.objects.count(), 0)
        self.client = APIClient()

    def test_api_csv_validate(self):
        """
            Check that all towns in the CSV file can be created using
            the class-based interface and then retrieved over the API
        """
        towns = get_towns_from_csv()

        for i, town in enumerate(towns):
            # Create
            save_town_and_parents_to_db(town)

            # Enumeration is zero-indexed, so add 1 here
            self.assertEqual(Town.objects.count(), i + 1)

            # Retrieve (overriding pagination)
            response = self.client.get("/towns?limit=100000")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["results"][-1], town)
            self.assertEqual(response.json()["count"], i + 1)


class AggsViewTestCase(TestCase):
    """ Test suite for the aggs api views (available at /aggs/*). """

    def setUp(self):
        """
            Define the test API Client to use and check that we are working
            with a clean database.

            Also define some dummy towns to add.
        """
        self.assertEqual(Department.objects.count(), 0)
        self.assertEqual(District.objects.count(), 0)
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(Town.objects.count(), 0)
        self.client = APIClient()

        self.towns = [{"town_code": x,
                       "district_code": x % 2,
                       "department_code": x % 5,
                       "region_code": x % 10,
                       "population": x,
                       "town_name": "Town {0}".format(x),
                       "region_name": "Region {0}".format(x % 10)}
                       for x in range(100)]

    def test_api_aggregations(self):
        """
            Check that the aggregation functions are working as expected by
            adding our dummy towns and validating the API responses.
        """
        for i, town in enumerate(self.towns):
            # Create
            save_town_and_parents_to_db(town)

            # Enumeration is zero-indexed, so add 1 here
            self.assertEqual(Town.objects.count(), i + 1)

        # Check region aggregation. There should be 10 regions, and the first
        # one should have 10 towns in it with a maximum population of 9
        response = self.client.get("/aggs/regions")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 10)
        self.assertEqual(response.json()[0]["town_count"], 10)
        self.assertEqual(response.json()[0]["max_population"], 9)

        # Check department aggregation. There should be 20 departments, and
        # the first one should have 5 towns in it with a maximum population of
        # 4
        response = self.client.get("/aggs/departments")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 20)
        self.assertEqual(response.json()[0]["town_count"], 5)
        self.assertEqual(response.json()[0]["max_population"], 4)

        # Check district aggregation. There should be 50 districts, and the
        # first one should have 2 towns in it with a maximum population of 1
        response = self.client.get("/aggs/districts")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 50)
        self.assertEqual(response.json()[0]["town_count"], 2)
        self.assertEqual(response.json()[0]["max_population"], 1)

        # Check town aggregation. There should be 100 towns, and the first
        # one should have 1 towns in it with a maximum population of 0
        response = self.client.get("/aggs/regions")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 100)
        self.assertEqual(response.json()[0]["town_count"], 1)
        self.assertEqual(response.json()[0]["max_population"], 0)
