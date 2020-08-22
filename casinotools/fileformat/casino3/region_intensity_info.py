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
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools

# Globals and constants variables.

class RegionIntensityInfo(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self._version = self.read_int(file)
        self._energyIntensity = self.read_double(file)
        self._regionID = self.read_int(file)
        self._normalizedEnergyIntensity = self.read_double(file)

    def getEnergyIntensity(self):
        return self._energyIntensity

    def getnormalizedEnergyIntensity(self):
        return self._normalizedEnergyIntensity
