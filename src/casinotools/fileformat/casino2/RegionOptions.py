#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2693 $"
__svnDate__ = "$Date: 2012-02-24 08:37:14 -0500 (Fri, 24 Feb 2012) $"
__svnId__ = "$Id: RegionOptions.py 2693 2012-02-24 13:37:14Z hdemers $"

# Standard library modules.
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.FileReaderWriterTools as FileReaderWriterTools
import Region

# Globals and constants variables.
TAG_REGION_DATA = "*REGIONDATA%%%%"

class RegionOptions(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, numberXRayLayers):
        self._numberXRayLayers = numberXRayLayers
        self._regions = []

    def read(self, file):
        assert file.mode == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = TAG_REGION_DATA
        self.findTag(file, tagID)

        self._numberRegions = self.readInt(file)

        for dummy in xrange(self._numberRegions):
            region = Region.Region(self._numberXRayLayers)
            region.read(file)
            self._regions.append(region)

    def write(self, file):
        assert file.mode == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tagID = TAG_REGION_DATA
        self.addTagOld(file, tagID)

        self.writeInt(file, self._numberRegions)

        assert len(self._regions) == self._numberRegions
        for index in xrange(self._numberRegions):
            region = self._regions[index]
            region.write(file)

    def getRegion(self, index):
        return self._regions[index]

    def getNumberRegions(self):
        return len(self._regions)

    def getRegions(self):
        return self._regions

    def setElement(self, elementSymbol, indexRegion=0):
        self._regions[indexRegion].setElement(elementSymbol, numberXRayLayers=self._numberXRayLayers)

    def setFilmThickness(self, thickness_nm):
        assert len(self._regions) == 2

        parameters = self._regions[0].getParameters()
        parameters[1] = thickness_nm
        self._regions[0].setParameters(parameters)

        parameters = self._regions[1].getParameters()
        parameters[2] = parameters[1]
        parameters[1] = 1.0e10
        parameters[0] = thickness_nm
        self._regions[1].setParameters(parameters)

    def setFilmThicknessInSubstrate(self, layerTopPositionZ_nm, thickness_nm):
        assert len(self._regions) == 3

        parameters = self._regions[0].getParameters()
        parameters[1] = layerTopPositionZ_nm
        self._regions[0].setParameters(parameters)

        parameters = self._regions[1].getParameters()
        #parameters[2] = parameters[1]
        parameters[1] = layerTopPositionZ_nm+thickness_nm
        parameters[0] = layerTopPositionZ_nm
        self._regions[1].setParameters(parameters)

        parameters = self._regions[2].getParameters()
        parameters[0] = layerTopPositionZ_nm + thickness_nm
        self._regions[2].setParameters(parameters)

    def setThinFilmThickness(self, thickness_nm):
        assert len(self._regions) == 1

        parameters = self._regions[0].getParameters()
        parameters[1] = thickness_nm
        self._regions[0].setParameters(parameters)

if __name__ == '__main__':    #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
