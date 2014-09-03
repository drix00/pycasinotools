#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class ElementIntensity(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self.Name = self.readStrLength(file, 3)

        self.Size = self.readLong(file)

        if self.Size != 0:
            self.IntensityK = self.readDoubleList(file, self.Size)
            self.IntensityL = self.readDoubleList(file, self.Size)
            self.IntensityM = self.readDoubleList(file, self.Size)
