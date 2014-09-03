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

# Local modules.
import casinotools.fileformat.casino3.EnergyMatrix as EnergyMatrix

# Globals and constants variables.
DIFFUSED_TAG = b"Diffused%Energy"
DIFFUSED_END_TAG = b"Diffused%%End%%"
DIFFUSE_VERSION = 30107000

class DiffusedEnergyMatrix(EnergyMatrix.EnergyMatrix):
    """
    Energy matrix date from casino simulation results file.

    :note: Need to implement the transformation from x, y, z to index of the _values array.

    """

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        tagID = DIFFUSED_TAG
        if self.findTag(file, tagID):
            self._version = self.readInt(file)

            self._numberElements = self._nbPtsX * self._nbPtsY * self._nbPtsZ
            self._startPosition = file.tell()
            #self._values = self.readDoubleList(file, self._numberElements)
            skipOffset = self.getSizeOfDoubleList(self._numberElements)
            file.seek(skipOffset, os.SEEK_CUR)

            logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", file.tell())
            tagID = DIFFUSED_END_TAG
            if not self.findTag(file, tagID):
                raise IOError

        self._endPosition = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)
