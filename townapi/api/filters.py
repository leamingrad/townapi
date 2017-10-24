"""
    filters.py

    Declare filter classes to give useful functions for our models.
"""
from django_filters import rest_framework as filters

from .constants import FR_REGION_CODES
from .models import Department, District, Town


class TownFilter(filters.FilterSet):
    """ Allow towns to be filtered by parent codes and population """
    min_population = filters.NumberFilter(name="population",
                                          lookup_expr="gte",
                                          label="Minimum Population")
    max_population = filters.NumberFilter(name="population",
                                          lookup_expr="lte",
                                          label="Maximum Population")

    district_code = filters.CharFilter(name="district__code",
                                       label="District Code")
    department_code = filters.CharFilter(name="district__department__code",
                                         label="Department Code")
    region_code = filters.ChoiceFilter(
        name="district__department__region__code",
        label="Region Code",
        choices=FR_REGION_CODES)

    class Meta:
        model = Town
        fields = ('population', )


class DepartmentAggsFilter(filters.FilterSet):
    """ Allow departments to be filtered by region code """
    region_code = filters.ChoiceFilter(name="region__code",
                                       label="Region Code",
                                       choices=FR_REGION_CODES)

    class Meta:
        model = Department
        fields = []


class DistrictAggsFilter(filters.FilterSet):
    """ Allow districts to be filtered by region and department code """
    region_code = filters.ChoiceFilter(name="department__region__code",
                                       label="Region Code",
                                       choices=FR_REGION_CODES)
    department_code = filters.CharFilter(name="department__code",
                                         label="Department Code")

    class Meta:
        model = District
        fields = []


class TownAggsFilter(filters.FilterSet):
    """ Allow towns to be filtered by all of their parents """
    district_code = filters.CharFilter(name="district__code",
                                       label="District Code")
    department_code = filters.CharFilter(name="district__department__code",
                                         label="Department Code")
    region_code = filters.ChoiceFilter(
        name="district__department__region__code",
        label="Region Code",
        choices=FR_REGION_CODES)

    class Meta:
        model = Town
        fields = []
