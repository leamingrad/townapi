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
