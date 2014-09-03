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

class StringParameters(Parameters):
    def generateLine(self):
        line = '%s "%s";' % (self._command, self._value)
        return line

    def _getString(self, value):
        return value
