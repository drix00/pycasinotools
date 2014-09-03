#!/usr/bin/env python
"""
.. py:currentmodule:: FileFormat.casino3.PointSpreadFunctionMatrix
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

PointSpreadFunctionMatrix module.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Standard library modules.
import logging
import os

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Project modules

# Globals and constants variables.


class PointSpreadFunctionMatrix(FileReaderWriterTools.FileReaderWriterTools):
    """
    Point spread function matrix data from CASINO simulation results file.

    :note: Need to implement the transformation from x, y, z to index of the _values array.

    """
    def __init__(self, options, point_nm):
        if options._optionsAdvancedPsfsSettings.getUseScanPointForCenter():
            self._centerPoint_nm = point_nm
        else:
            self._centerPoint_nm = options._optionsAdvancedPsfsSettings.getPsfCenter_nm()

        self._nbPtsX = options._optionsAdvancedPsfsSettings.getNumberStepsX()
        self._nbPtsY = options._optionsAdvancedPsfsSettings.getNumberStepsY()
        self._nbPtsZ = options._optionsAdvancedPsfsSettings.getNumberStepsZ()

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
                self._data = {}
                for x in range(self._nbPtsX):
                    for y in range(self._nbPtsY):
                        for z in range(self._nbPtsZ):
                            self._data[(x, y, z)] = self._values[index]
                            index += 1
                del self._values
                self._values = None

        return self._data

    def getNumberPoints(self):
        return self._nbPtsX * self._nbPtsY * self._nbPtsZ

    def getNumberPointsX(self):
        return self._nbPtsX

    def getNumberPointsY(self):
        return self._nbPtsY

    def getNumberPointsZ(self):
        return self._nbPtsZ
