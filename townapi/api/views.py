"""
    views.py

    This file declares views for the api app.
"""
from django_filters import rest_framework as filters
from rest_framework import generics

from django.db.models import Avg, Count, F, Max, Min, Value
from rest_framework.filters import OrderingFilter

from .filters import TownFilter
from .models import Department, District, Region, Town
from .pagination import OneHundredResultsLimitOffsetPagination
from .serializers import (DepartmentAggsSerializer, DistrictAggsSerializer,
                          RegionAggsSerializer, TownAggsSerializer,
                          TownSerializer, AggsSerializer)

"""
Views to create:
- AggsView - more complicated view that decides queryset to use and then
             uses the AggsSerializer
"""


class TownsView(generics.ListAPIView):
    """
        Simple endpoint to return a list of French towns and cities. For each
        town, a JSON record is provided with information about the town and it
        region, department and district. An example JSON record is as follows:

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

        This will sort by the value of `<FIELD>` (all fields can be used
        here). If the `-` is included, then the ordering will be in descending
        order, and if it is omitted then it will be in ascending order.

        Filtering can be done using the syntax:

            /towns?<FILTER>=<VALUE>

        Multiple filters can be chained using `&` characters. Available filters
        are:

        - Region Code (`region_code`)
        - Department Code (`department_code`)
        - District Code (`district_code`)
        - Exact Population (`population`)
        - Minimum Population (`min_population`)
        - Maximum Population (`max_population`)
    """
    queryset = Town.objects.all() \
                   .select_related('district',
                                   'district__department',
                                   'district__department__region')
    serializer_class = TownSerializer
    pagination_class = OneHundredResultsLimitOffsetPagination
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend, )
    filter_class = TownFilter


class AggsView(generics.ListAPIView):
    """
        Call through to the aggregate serializer to create the response
        but set the queryset based on the requested aggregation.

        This is a common view used for the different types of place
        (to keep routing code simple)
    """
    serializer_class = AggsSerializer


class RegionAggsView(AggsView):
    """ Aggregate across regions """
    serializer_class = RegionAggsSerializer
    queryset = Region.objects.annotate(
        min_population=Min('department__district__town__population'),
        max_population=Max('department__district__town__population'),
        avg_population=Avg('department__district__town__population'),
        town_count=Count('department__district__town'))


class DepartmentAggsView(AggsView):
    """ Aggregate across departments """
    serializer_class = DepartmentAggsSerializer
    queryset = Department.objects.annotate(
        min_population=Min('district__town__population'),
        max_population=Max('district__town__population'),
        avg_population=Avg('district__town__population'),
        town_count=Count('district__town'))


class DistrictAggsView(AggsView):
    """ Aggregate across districts """
    serializer_class = DistrictAggsSerializer
    queryset = District.objects.annotate(
        min_population=Min('town__population'),
        max_population=Max('town__population'),
        avg_population=Avg('town__population'),
        town_count=Count('town'))


class TownAggsView(AggsView):
    """ Aggregate across a single town """
    serializer_class = TownAggsSerializer
    queryset = Town.objects.annotate(
        min_population=F('population'),
        max_population=F('population'),
        avg_population=F('population'),
        town_count=Value(1))
