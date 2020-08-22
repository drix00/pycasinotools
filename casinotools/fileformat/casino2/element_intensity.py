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
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools

# Globals and constants variables.

class ElementIntensity(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self.Name = self.read_str_length(file, 3)

        self.Size = self.read_long(file)

        if self.Size != 0:
            self.IntensityK = self.read_double_list(file, self.Size)
            self.IntensityL = self.read_double_list(file, self.Size)
            self.IntensityM = self.read_double_list(file, self.Size)
