"""
    constants.py

    This file contains various constants used by the api application. In
    general, these are mostly lists of choices for use in field validation.

    When using this file, you MUST import constants directly by name (rather
    than importing *)
"""
FR_OVERSEAS_REGION_CODES = list(range(1, 6))
FR_EU_REGION_CODES = [11, 24, 27, 28, 32, 44, 52, 53, 75, 76, 84, 93, 94]

FR_REGION_CODES = tuple([(x, "{:0>2}".format(x)) for x
                         in FR_OVERSEAS_REGION_CODES + FR_EU_REGION_CODES])
