#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.

# Project modules
from casinotools.scripting.casino3.Parameters import Parameters

# Globals and constants variables.

class StringArrayParameters(Parameters):
    def generateLine(self):
        line = '%s' % (self._command)

        for item in self._value:
            line += ' %s' % (item)
        line += ';'

        return line

    def _getString(self, value):
        return value
