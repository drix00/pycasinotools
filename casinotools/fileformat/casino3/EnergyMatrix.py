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
import os

# Third party modules.
import numpy as np

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino3.OptionsDist as OptionsDist

# Globals and constants variables.

class EnergyMatrix(FileReaderWriterTools.FileReaderWriterTools):
    """
    Energy matrix date from casino simulation results file.

    :note: Need to implement the transformation from x, y, z to index of the _values array.

    """
    def __init__(self, options, point):
        self._point = point

        if options._optionsDist.DEpos_Type == OptionsDist.DIST_DEPOS_TYPE_CARTESIAN:
            self._nbPtsX = options._optionsDist.NbPointDEpos_X
            self._nbPtsY = options._optionsDist.NbPointDEpos_Y
            self._nbPtsZ = options._optionsDist.NbPointDEpos_Z
        elif options._optionsDist.DEpos_Type == OptionsDist.DIST_DEPOS_TYPE_CYLINDRIC:
            self._nbPtsX = 1
            self._nbPtsY = options._optionsDist.DEposCyl_Rad_Div
            self._nbPtsZ = options._optionsDist.DEposCyl_Z_Div
        elif options._optionsDist.DEpos_Type == OptionsDist.DIST_DEPOS_TYPE_SPHERIC:
            self._nbPtsX = 1
            self._nbPtsY = 1
            self._nbPtsZ = options._optionsDist.DEposSpheric_Rad_Div

        self._numberElements = 0
        self._values = None
        self._data = None

        self._file = None
        self._startPosition = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._numberElements = self._nbPtsX * self._nbPtsY * self._nbPtsZ
        self._startPosition = file.tell()
        #self._values = self.readDoubleList(file, self._numberElements)
        skipOffset = self.getSizeOfDoubleList(self._numberElements)
        file.seek(skipOffset, os.SEEK_CUR)

        self._endPosition = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)

    def _readValues(self):
        if self._file is None:
            self._file = open(self._filePathname, 'rb')

        self._file.seek(self._startPosition)
        self._values = self.readDoubleList(self._file, self._numberElements)

    def getData(self):
        if self._data is None:
            if self._values is None:
                self._readValues()
                index = 0
                shape = (self._nbPtsX, self._nbPtsY, self._nbPtsZ)
                self._data = np.zeros(shape)
                for x in range(self._nbPtsX):
                    for y in range(self._nbPtsY):
                        for z in range(self._nbPtsZ):
                            self._data[x, y, z] = self._values[index]
                            index += 1
                del self._values
                self._values = None

        return self._data

    def getNumberPointsEnergyAbsorbed(self):
        return self._nbPtsX * self._nbPtsY * self._nbPtsZ

    def getNumberPointsEnergyAbsorbedX(self):
        return self._nbPtsX

    def getNumberPointsEnergyAbsorbedY(self):
        return self._nbPtsY

    def getNumberPointsEnergyAbsorbedZ(self):
        return self._nbPtsZ
