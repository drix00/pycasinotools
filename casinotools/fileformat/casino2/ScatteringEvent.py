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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class ScatteringEvent(FileReaderWriterTools.FileReaderWriterTools):
    def getSkipOffset(self):
        format = "4f2i"
        return struct.calcsize(format)

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self.X = self.readFloat(file)
        self.Y = self.readFloat(file)
        self.Z = self.readFloat(file)
        self.E = self.readFloat(file)
        self.Intersect = self.readInt(file)
        self.id = self.readInt(file)
