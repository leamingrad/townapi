"""
    views.py

    This file declares views for the api app.
"""
from rest_framework import generics

from rest_framework.filters import OrderingFilter

from .pagination import OneHundredResultsLimitOffsetPagination
from .serializers import TownSerializer
from .models import Town

"""
Views to create:
- AggsView - more complicated view that decides queryset to use and then
             uses the AggsSerializer
"""


class TownsView(generics.ListAPIView):
    """ Standard list endpoint to return a list of all Town objects """
    queryset = Town.objects.all() \
                   .select_related('district',
                                   'district__department',
                                   'district__department__region')
    serializer_class = TownSerializer
    pagination_class = OneHundredResultsLimitOffsetPagination
    filter_backends = (OrderingFilter,)
