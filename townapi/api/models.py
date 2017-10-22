"""
    models.py

    Declare models to be used by the api app.

    These models take advantage of the nested nature of the French
    administrative divisions. There is one model for each level of division,
    and each has a reference to it's parent in the layer above.

     The reason for having multiple layers of model are as follows:
     - It should make the aggregation code cleaner and easier to follow
     - It makes it more maintainable for the future - for example, adding
       names to the departments will be a quick operation
     - Adding an extra layer of divisions becomes easy
     - Avoid the god object anti-pattern
     - Danger of falling into the lasagne code antipattern is low (there are
       only 5-6 levels of administrative division in France)
"""
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from .constants import FR_REGION_CODES


class Place(models.Model):
    """
        This abscract model contains utility functions for calculating
        aggregate data from towns.
    """
    def get_towns(self):
        """
            Method to get a QuerySet that will give all the towns in this
            place.

            This method MUST be overriden by children
            TODO: Enforce overriding.

            :returns: A QuerySet of Town objects
        """
        pass

    def get_max_population(self):
        """ Using the QuerySet of towns, get the maximum population """
        return self.get_towns().aggregate(models.Max('population'))

    def get_min_population(self):
        """ Using the QuerySet of towns, get the minimum population """
        return self.get_towns().aggregate(models.Min('population'))

    def get_avg_population(self):
        """ Using the QuerySet of towns, get the average population """
        return self.get_towns().aggregate(models.Avg('population'))

    class Meta:
        abstract = True


class Region(models.Model):
    """
        This represents a region in France, of which there are exactly 18 (13
        in Europe and 5 overseas). Each region is represented by its INSEE
        code, which is always a two-digit integer.
    """
    code = models.PositiveSmallIntegerField(choices=FR_REGION_CODES,
                                            primary_key=True)
    name = models.CharField(max_length=64,
                            validators=[MinLengthValidator(1), ])


class Department(models.Model):
    """
        This represents a department in France. Each region contains multiple
        departments (there are 101 in total - 96 in Europe and 5 overseas).

        Each department is uniquely identified by its code, which consists of
        between one and three digits with an optional letter after.
    """
    code = models.CharField(primary_key=True,
                            max_length=3,
                            validators=[MinLengthValidator(1),
                                        RegexValidator(r'\d{1,3}[ABM]?')])
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class District(models.Model):
    """
        This represents a District. Each Department contains multiple
        districts, which are uniquely numbered within the department (but not
        globally unique).
    """
    code = models.PositiveSmallIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("code", "department", )


class Town(models.Model):
    """
        This represents a Town (or city). Each District contains multiple
        districts, which are uniquely numbered within the district (but not
        globally unique).
    """
    code = models.PositiveSmallIntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,
                            validators=[MinLengthValidator(1), ])
    population = models.PositiveIntegerField()

    class Meta:
        unique_together = ("code", "district", )
