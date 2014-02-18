#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2364 $"
__svnDate__ = "$Date: 2011-05-30 07:15:15 -0400 (Mon, 30 May 2011) $"
__svnId__ = "$Id: ElementIntensity.py 2364 2011-05-30 11:15:15Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class ElementIntensity(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file):
        assert file.mode == 'rb'
        self.Name = self.readStrLength(file, 3)

        self.Size = self.readLong(file)

        if self.Size != 0:
            self.IntensityK = self.readDoubleList(file, self.Size)
            self.IntensityL = self.readDoubleList(file, self.Size)
            self.IntensityM = self.readDoubleList(file, self.Size)
