"""
    serializers.py

    This file decares the serializers for the api app. There is a single
    serializer for each API endpoint.
"""
from rest_framework import serializers
from .models import Town
"""
Add the following serializers:
- AggsSerializer - Custom serializer to pack the required aggregate data into
                   a JSON object
 """


class TownSerializer(serializers.ModelSerializer):
    """
        The Town model is serialized into a single flat JSON object containing
        both the Town's fields and those of the Town's administrative parents.

        Since we want a flat representation, we have to declare the parent
        fields manually, since DRF does not support the foreign_key__field
        syntax.

        The field logic is fairly simple:
        - All identifying codes are sent as strings (even if they are stored
          as integers)
        - Names are sent as strings
        - Properties are sent as the appropriate type (e.g. population is sent
          as an integer)
    """
    town_code = serializers.CharField(source="code")
    town_name = serializers.CharField(source="name")
    district_code = serializers.CharField(source="district.code")
    department_code = serializers.CharField(
        source="district.department.code")
    region_code = serializers.CharField(
        source="district.department.region.get_code_display")
    region_name = serializers.CharField(
        source="district.department.region.name")

    class Meta:
        """
            Meta class to map serializer's fields with the model fields.

            Manually declare the list of fields in case the models change.
        """
        model = Town
        fields = ("town_code",
                  "town_name",
                  "population",
                  "district_code",
                  "department_code",
                  "region_code",
                  "region_name")
