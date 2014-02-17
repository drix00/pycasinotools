#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2364 $"
__svnDate__ = "$Date: 2011-05-30 07:15:15 -0400 (Mon, 30 May 2011) $"
__svnId__ = "$Id: Vector.py 2364 2011-05-30 11:15:15Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
