#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import math
import logging
import os

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.
class GraphData(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, file):
        self._file = None
        self._startPosition = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

        self._values = None
        self._positions = None

        self.read(file)

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._version = self.readInt(file)
        self._size = self.readLong(file)
        self._borneInf = self.readDouble(file)
        self._borneSup = self.readDouble(file)
        self._isLog = self.readInt(file)
        self._isUneven = self.readInt(file)

        self._title = self.readStr(file)
        self._xTitle = self.readStr(file)
        self._yTitle = self.readStr(file)

        self._startPosition = file.tell()
        skipOffset = self.getSizeOfDoubleList(self._size)
        if self._isUneven:
            skipOffset *= 2

        file.seek(skipOffset, os.SEEK_CUR)

        self._endPosition = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)

    def getValues(self):
        if self._values is None:
            self._readValues()

        return self._values

    def _readValues(self):
        self._file.seek(self._startPosition)
        self._values = []
        self._positions = []
        for dummy in range(self._size):
            value = self.readDouble(self._file)
            self._values.append(value)

            if self._isUneven:
                position = self.readDouble(self._file)
                self._positions.append(position)

        if not self._isUneven:
            for i in range(self._size):
                position = self.index2pos(self._borneSup, self._borneInf, self._size, i, self._isLog)
                self._positions.append(position)

        assert len(self._values) == len(self._positions)

    def index2pos(self, XSup, XInf, nbPoints, Index, FLog):
        assert(XSup >= XInf)
        assert(nbPoints > 0)

        if nbPoints == 1:
            return XInf

        if Index <= 0:
            return XInf

        if FLog:
            assert(XSup > 0)
            assert(XInf > 0)

            Point = (float(Index) / float(nbPoints - 1))
            exp = Point * (math.log10(XSup) - math.log10(XInf)) + math.log10(XInf)
            Point = pow(10.0, exp)
            return Point
        else:
            Point = (float(Index) / float(nbPoints - 1))
            Point = Point * (XSup - XInf) + XInf
            return Point
