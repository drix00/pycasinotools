#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2071 $"
__svnDate__ = "$Date: 2010-10-26 16:32:58 -0400 (Tue, 26 Oct 2010) $"
__svnId__ = "$Id: RegionIntensityInfo.py 2071 2010-10-26 20:32:58Z hdemers $"

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