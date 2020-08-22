#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import struct

# Third party modules.

# Local modules.
import casinotools.file_format.file_reader_writer_tools as FileReaderWriterTools

# Globals and constants variables.

class ScatteringEvent(FileReaderWriterTools.FileReaderWriterTools):
    def getSkipOffset(self):
        format = "4f2i"
        return struct.calcsize(format)

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self.X = self.read_float(file)
        self.Y = self.read_float(file)
        self.Z = self.read_float(file)
        self.E = self.read_float(file)
        self.Intersect = self.read_int(file)
        self.id = self.read_int(file)
