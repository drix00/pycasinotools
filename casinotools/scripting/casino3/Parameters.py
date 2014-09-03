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

class Parameters(object):
    def __init__(self, command, unit="", prefix=''):
        self._command = command
        self._value = None
        self._unit = unit
        self._prefix = prefix
        self._values = {}

    def setValue(self, value):
        self._value = value

    def getValue(self):
        return self._value

    def generateLine(self):
        valueText = self._getString(self._value)
        line = "%s %s;" % (self._command, valueText)
        return line

    def __str__(self):
        text = "%s%s%s" % (self._prefix, self._value, self._unit)
        return text

    def _getString(self, value):
        if float(value) < 0:
            text = "(%s)" % value
        else:
            text = "%s" % value

        return text

    def isValueSet(self):
        if self._value == None and self._values == {}:
            return False
        else:
            return True
