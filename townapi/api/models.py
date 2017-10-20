"""
    models.py

    Declare models to be used by the api app.

    These models take advantage of the nested nature of the French
    administrative divisions.
"""
from django.db import models

"""
Add the following models here:
- Region: This has an ID (numeric) and name (64 characters). Index on the ID 
- Department: This has an ID (between 1 and 3 numbers followed by and optional
              letter) and a region. Index on ID
- District: This has a code (numeric) and a departement. Will need a separate
            index as the code is repeated across departements
- Town: This has a code (numeric), a district, a name (128 characters?) and a
        population (positive integer - Paris is probably included so not
        small). Will need a separate index as code is repeated across
        departments/regions
 
 The reason for having multiple layers of model are as follows:
 - It should make the aggregation code cleaner and easier to follow
 - It makes it more maintainable for the future - adding names to the
   departments will be a quick operation
 - Adding an extra layer of divisions becomes easy
 - Avoid the god object anti-pattern
 - Danger of falling into the lasagne code antipattern is low (there are only
   5-6 levels of administrative division in France)
"""
