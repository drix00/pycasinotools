#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino3.Region as Region

# Globals and constants variables.
TAG_REGION_DATA = b"*REGIONDATA%%%%"

class RegionOptions(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._regions = []

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = TAG_REGION_DATA
        self.findTag(file, tagID)

        self._numberRegions = self.readInt(file)

        for dummy in range(self._numberRegions):
            region = Region.Region()
            region.read(file)
            self._regions.append(region)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tagID = TAG_REGION_DATA
        self.addTag(file, tagID)

        self.writeInt(file, self._numberRegions)

        assert len(self._regions) == self._numberRegions
        for index in range(self._numberRegions):
            region = self._regions[index]
            region.write(file)

    def getRegion(self, index):
        return self._regions[index]
