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
DISTANCE_nm = "Distance (nm)"
INTENSITY = "Intensity"
INTENSITY_ABSORBED = "Intensity Absorbed"

class XrayRadial(object):
    def __init__(self):
        self._line = None
        self._elementSymbol = None
        self._labels = []
        self._data = {}

    def addData(self, label, value):
        self._data.setdefault(label, []).append(value)

    def setLine(self, line):
        self._line = line

    def setElementSymbol(self, symbol):
        self._elementSymbol = symbol

    def setLabels(self, labels):
        self._labels = labels

    def getLine(self):
        return self._line

    def getElementSymbol(self):
        return self._elementSymbol

    def getDataLabels(self):
        return self._labels

    def getDistances_nm(self):
        return self._data[DISTANCE_nm]

    def getIntensities(self):
        return self._data[INTENSITY]

    def getIntensitiesAbsorbed(self):
        return self._data[INTENSITY_ABSORBED]
