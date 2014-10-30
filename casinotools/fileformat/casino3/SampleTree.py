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
import casinotools.fileformat.casino3.Triangle as Triangle

# Globals and constants variables.

class SampleTree(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        pass

    def read(self, file):
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._maxSize = self.readDouble(file)
        self._maxLevel = self.readInt(file)
        self._maximum = self.readDoubleList(file, 3)
        self._minimum = self.readDoubleList(file, 3)

        self._numberTriangles = self.readInt(file)
        self._triangles = []
        for dummy in range(self._numberTriangles):
            triangle = Triangle.Triangle()
            triangle.read(file)
            self._triangles.append(triangle)

    def export(self, exportFile):
        line = "Maximum size: %i" % (self._maxSize)
        self.writeLine(exportFile, line)

        line = "Maximum level: %i" % (self._maxLevel)
        self.writeLine(exportFile, line)

        line = "Maximum:"
        self.writeLine(exportFile, line)
        for label, value in zip(["X", 'Y', 'Z'], self._maximum):
            line = "\t%s: %g" % (label, value)
            self.writeLine(exportFile, line)

        line = "Minimum:"
        self.writeLine(exportFile, line)
        for label, value in zip(["X", 'Y', 'Z'], self._minimum):
            line = "\t%s: %g" % (label, value)
            self.writeLine(exportFile, line)

        line = "Number triangles: %i" % (self._numberTriangles)
        self.writeLine(exportFile, line)

        triangleID = 0
        for triangle in self._triangles:
            triangleID += 1

            line = "*"*15
            self.writeLine(exportFile, line)

            line = "Triangle: %i" % (triangleID)
            self.writeLine(exportFile, line)

            triangle.export(exportFile)
