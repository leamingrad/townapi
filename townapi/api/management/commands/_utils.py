"""
    utils.py

    Provides utility functions and constants for management commands in the api
    application. Some of these functions are also used by unit tests.
"""
import csv
import os
from api.models import Department, District, Region, Town

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__),
                             "..",
                             "..",
                             "..",
                             "..",
                             "data",
                             "towns.csv")
CSV_INT_FIELDS = ["population", ]


def get_towns_from_csv():
    """
        Vanity method for getting a list of dictionaries for each line of the
        towns.csv data file, and cleaning up any data found there

        :returns: A list of dictionaries, where each one is keyed by the
                  API names of town properties
    """
    def clean_record(record):
        """
            Clean CSV records by converting textual numbers with commas into
            integers for known integer fields
        """
        c_record = {}

        for key, value in record.items():
            if key in CSV_INT_FIELDS:
                value = int('0' + value.replace(',', ''))
            c_record[key] = value

        return c_record

    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csv_file:
        towns = [clean_record(record) for record in csv.DictReader(csv_file)]

    return towns


def save_town_and_parents_to_db(town):
    """
        Given a JSON object containing information about a Town, add it and
        all of it's parent objects to the DB (after fully validating them)
    """
    region, created = Region.objects.get_or_create(code=town["region_code"],
                                                   name=town["region_name"])
    if created:
        region.full_clean()

    department, created = Department.objects.get_or_create(
        code=town["department_code"],
        region=region)
    if created:
        department.full_clean(validate_unique=False)

    district, created = District.objects.get_or_create(
        code=town["district_code"],
        department=department)
    if created:
        district.full_clean(validate_unique=False)

    town = Town(code=town["town_code"],
                district=district,
                name=town["town_name"],
                population=town["population"])
    town.full_clean()
    town.save()
