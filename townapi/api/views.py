"""
    views.py
    
    This file declares views for the api app.
"""
from django.shortcuts import render

"""
Views to create:
- TownsView - make use of inbuilt DRF classes to give a list of towns,
              serialised with TownSerializer
- AggsView - more complicated view that decides queryset to use and then
             uses the AggsSerializer
"""
