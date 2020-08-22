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
import casinotools.file_format.file_reader_writer_tools as FileReaderWriterTools

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
        self._id = self.read_int(file)
        self._point0 = self.read_double_list(file, 3)
        self._point1 = self.read_double_list(file, 3)
        self._point2 = self.read_double_list(file, 3)

        self._normal = self.read_double_list(file, 3)

        # Obolete.
        self.read_float(file)

        self._insideID = self.read_int(file)
        self._outsideID = self.read_int(file)

    def export(self, export_file):
        line = "ID: %i" % (self._id)
        self.write_line(export_file, line)

        line = "Point 0:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'Z'], self._point0):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Point 1:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'Z'], self._point1):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Point 2:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'Z'], self._point2):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Normal:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'Z'], self._normal):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "inside ID: %i" % (self._insideID)
        self.write_line(export_file, line)

        line = "outside ID: %i" % (self._outsideID)
        self.write_line(export_file, line)
