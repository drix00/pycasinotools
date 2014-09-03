#!/usr/bin/env python
""""""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
from casinotools.scripting.casino3.RangedParameters import RangedParameters

# Globals and constants variables.

class RangedSampleParameters(RangedParameters):
    def setValue(self, value, sampleObject):
        self._values[sampleObject] = value
        #self._value = value
        #self._sampleObject =

    def generateLine(self):
        line = ""
        for sampleObject in self._values:
                value = self._values[sampleObject]
                valueText = self._getString(value)
                line += "%s %s %s %s %s;\n" % (self._command, sampleObject, valueText, valueText, 1)

        line = line[:-1]
        return line

    def __str__(self):
        text = ""
        for sampleObject in self._values:
                value = self._values[sampleObject]
                text += "%s_%s%s%s\n" % (sampleObject, self._prefix, value, self._unit)
        text = text[:-1]
        return text
