"""
    urls.py

    Declare the URL scheme used by the api app. We present the following
    endpoints:
    - /towns - Return the full list of towns
"""
from django.conf.urls import url
from .views import (DepartmentAggsView, DistrictAggsView, RegionAggsView,
                    TownAggsView, TownsView)

urlpatterns = [
    url(r'^towns/?$', TownsView.as_view()),
    url(r'^aggs/regions/?$', RegionAggsView.as_view()),
    url(r'^aggs/departments/?$', DepartmentAggsView.as_view()),
    url(r'^aggs/districts/?$', DistrictAggsView.as_view()),
    url(r'^aggs/towns/?$', TownAggsView.as_view()),
]
