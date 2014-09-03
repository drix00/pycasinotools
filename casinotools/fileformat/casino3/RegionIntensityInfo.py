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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class RegionIntensityInfo(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self._version = self.readInt(file)
        self._energyIntensity = self.readDouble(file)
        self._regionID = self.readInt(file)
        self._normalizedEnergyIntensity = self.readDouble(file)

    def getEnergyIntensity(self):
        return self._energyIntensity

    def getnormalizedEnergyIntensity(self):
        return self._normalizedEnergyIntensity
