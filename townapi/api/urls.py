"""
    urls.py

    Declare the URL scheme used by the api app. We present the following
    endpoints:
    - /towns - Return the full list of towns
"""
from django.conf.urls import url
from .views import TownsView

urlpatterns = [
    url(r'^towns/?$', TownsView.as_view())
]
