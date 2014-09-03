#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.
SHAPE_SUBSTRATE = -1
SHAPE_UNDEFINED = 0
SHAPE_PLANE = 1
SHAPE_BOX = 2
SHAPE_SPHERE = 3
SHAPE_CONE = 4
SHAPE_CYLINDRE = 5
SHAPE_ROUNDREC = 6
SHAPE_TRUNC_PYRAMID = 7
SHAPE_MESHOBJECT = 999

def getString(shape):
    if shape == SHAPE_SUBSTRATE:
        return "substrate"
    elif shape == SHAPE_UNDEFINED:
        return "undefined"
    elif shape == SHAPE_PLANE:
        return "plane"
    elif shape == SHAPE_BOX:
        return "box"
    elif shape == SHAPE_SPHERE:
        return "sphere"
    elif shape == SHAPE_CONE:
        return "cone"
    elif shape == SHAPE_CYLINDRE:
        return "cylinder"
    elif shape == SHAPE_ROUNDREC:
        return "rounded rectangle"
    elif shape == SHAPE_TRUNC_PYRAMID:
        return "truncated pyramid"
    elif shape == SHAPE_MESHOBJECT:
        return "mesh object"
