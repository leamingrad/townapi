"""
    import_csv.py

    Simple Django admin command to make importing data from the CSV dataset
    into the database easy
"""
from django.core.management.base import BaseCommand
from ._utils import get_towns_from_csv, save_town_and_parents_to_db


class Command(BaseCommand):
    help = 'Import the town data from the CSV data file'

    def handle(self, *args, **options):
        for town in get_towns_from_csv():
            save_town_and_parents_to_db(town)

            self.stdout.write(self.style.SUCCESS("Successfully added {0}"
                                                 .format(town["town_name"])))
