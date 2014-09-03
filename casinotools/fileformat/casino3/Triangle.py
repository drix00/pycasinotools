#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2010 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class Triangle(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._point0 = None
        self._point1 = None
        self._point2 = None

        self._normal = None

        self._id = None
        self._insideID = None
        self._outsideID = None

    def read(self, file):
        self._id = self.readInt(file)
        self._point0 = self.readDoubleList(file, 3)
        self._point1 = self.readDoubleList(file, 3)
        self._point2 = self.readDoubleList(file, 3)

        self._normal = self.readDoubleList(file, 3)

        # Obolete.
        self.readFloat(file)

        self._insideID = self.readInt(file)
        self._outsideID = self.readInt(file)

    def export(self, exportFile):
        line = "ID: %i" % (self._id)
        self.writeLine(exportFile, line)

        line = "Point 0:"
        self.writeLine(exportFile, line)
        for label, value in zip(["X", 'Y', 'Z'], self._point0):
            line = "\t%s: %g" % (label, value)
            self.writeLine(exportFile, line)

        line = "Point 1:"
        self.writeLine(exportFile, line)
        for label, value in zip(["X", 'Y', 'Z'], self._point1):
            line = "\t%s: %g" % (label, value)
            self.writeLine(exportFile, line)

        line = "Point 2:"
        self.writeLine(exportFile, line)
        for label, value in zip(["X", 'Y', 'Z'], self._point2):
            line = "\t%s: %g" % (label, value)
            self.writeLine(exportFile, line)

        line = "Normal:"
        self.writeLine(exportFile, line)
        for label, value in zip(["X", 'Y', 'Z'], self._normal):
            line = "\t%s: %g" % (label, value)
            self.writeLine(exportFile, line)

        line = "inside ID: %i" % (self._insideID)
        self.writeLine(exportFile, line)

        line = "outside ID: %i" % (self._outsideID)
        self.writeLine(exportFile, line)
