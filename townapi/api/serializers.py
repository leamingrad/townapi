"""
    serializers.py

    This file decares the serializers for the api app. There is a single
    serializer for each API endpoint.
"""
from rest_framework import serializers
from .models import Department, District, Region, Town
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
    town_code = serializers.CharField(source="code", label="Town Code")
    town_name = serializers.CharField(source="name", label="Town Name")
    district_code = serializers.CharField(source="district.code",
                                          label="District Code")
    department_code = serializers.CharField(
        source="district.department.code",
        label="Department Code")
    region_code = serializers.CharField(
        source="district.department.region.get_code_display",
        label="Region Code")
    region_name = serializers.CharField(
        source="district.department.region.name",
        label="Region Name")

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


class AggsSerializer(serializers.ModelSerializer):
    """
        This serializer returns the aggregates mix/max average population,
        and the identifying information (code) for whatever we are
        aggregating over.

        This is used as a base class for individual model aggregators,
        as you cannot force DRF serializers to work with one model.
    """
    min_population = serializers.IntegerField()
    max_population = serializers.IntegerField()
    avg_population = serializers.IntegerField()
    town_count = serializers.IntegerField()

    class Meta:
        """
            Get the annotated fields from any model..
        """
        fields = ("code",
                  "min_population",
                  "max_population",
                  "avg_population",
                  "town_count")


class RegionAggsSerializer(AggsSerializer):
    """ Regions have a name field, so also return that """
    code = serializers.CharField(source="get_code_display",
                                 label="Code")

    class Meta(AggsSerializer.Meta):
        model = Region
        fields = AggsSerializer.Meta.fields + ("name", )


class DepartmentAggsSerializer(AggsSerializer):
    """ Departments do not have a name """
    region_code = serializers.CharField(source="region.get_code_display",
                                        label="Region Code")

    class Meta(AggsSerializer.Meta):
        model = Department
        fields = AggsSerializer.Meta.fields + ("region_code", )


class DistrictAggsSerializer(AggsSerializer):
    """ Districts do not have a name """
    region_code = serializers.CharField(
        source="department.region.get_code_display",
        label="Region Code")
    department_code = serializers.CharField(source="department.code",
                                            label="Department Code")

    class Meta(AggsSerializer.Meta):
        model = District
        fields = AggsSerializer.Meta.fields + ("region_code",
                                               "department_code")


class TownAggsSerializer(AggsSerializer):
    """ Towns have a name field, so also return that """
    region_code = serializers.CharField(
        source="district.department.region.get_code_display",
        label="Region Code")
    district_code = serializers.CharField(source="district.code",
                                          label="District Code")
    department_code = serializers.CharField(
        source="district.department.code",
        label="Department Code")

    class Meta(AggsSerializer.Meta):
        model = Town
        fields = AggsSerializer.Meta.fields + ("name",
                                               "region_code",
                                               "department_code",
                                               "district_code")
