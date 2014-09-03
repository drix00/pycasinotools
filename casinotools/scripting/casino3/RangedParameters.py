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
from casinotools.scripting.casino3.Parameters import Parameters

# Globals and constants variables.

class RangedParameters(Parameters):
    def generateLine(self):
        valueText = self._getString(self._value)
        line = "%s %s %s %s;" % (self._command, valueText, valueText, 1)
        return line
