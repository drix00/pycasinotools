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
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools
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

        self._maxSize = self.read_double(file)
        self._maxLevel = self.read_int(file)
        self._maximum = self.read_double_list(file, 3)
        self._minimum = self.read_double_list(file, 3)

        self._numberTriangles = self.read_int(file)
        self._triangles = []
        for dummy in range(self._numberTriangles):
            triangle = Triangle.Triangle()
            triangle.read(file)
            self._triangles.append(triangle)

    def export(self, export_file):
        line = "Maximum size: %i" % (self._maxSize)
        self.write_line(export_file, line)

        line = "Maximum level: %i" % (self._maxLevel)
        self.write_line(export_file, line)

        line = "Maximum:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'Z'], self._maximum):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Minimum:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'Z'], self._minimum):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Number triangles: %i" % (self._numberTriangles)
        self.write_line(export_file, line)

        triangleID = 0
        for triangle in self._triangles:
            triangleID += 1

            line = "*"*15
            self.write_line(export_file, line)

            line = "Triangle: %i" % (triangleID)
            self.write_line(export_file, line)

            triangle.export(export_file)
