"""
    pagination.py

    Provide utility classes for pagination.
"""
from rest_framework.pagination import LimitOffsetPagination


class OneHundredResultsLimitOffsetPagination(LimitOffsetPagination):
    """ Set the page size to 100 """
    default_limit = 100
