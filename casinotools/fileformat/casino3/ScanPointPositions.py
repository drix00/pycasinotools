#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class ScanPointPositions(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def reset(self):
        self._positions = []

        self._startPosition = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

    def getNumberPoints(self):
        return len(self._positions)

    def addPosition(self, point):
        self._positions.append(point)

    def getPositions(self):
        return self._positions

    def read(self, file):
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        # Move backward to read the previous tag, which indicate indirectly the start of this section.
        currentPosition = file.tell()
        if currentPosition > 16:
            file.seek(-16, os.SEEK_CUR)

        tagID = b"*SIM_OPT_END%"
        if self.findTag(file, tagID):
            self.reset()

            self._startPosition = file.tell()
            self._filePathname = file.name
            self._fileDescriptor = file.fileno()
            logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)
            numberPoints = self.readInt(file)

            for dummy in range(numberPoints):
                x = self.readDouble(file)
                y = self.readDouble(file)
                z = self.readDouble(file)

                points = (x, y, z)

                self.addPosition(points)

        self._endPosition = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)

        return None

    def export(self, exportFile):
        # todo: implement the export method.
        pass
