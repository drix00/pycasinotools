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
__svnId__ = "$Id: ScatteringEvent.py 2364 2011-05-30 11:15:15Z hdemers $"

# Standard library modules.
import struct

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class ScatteringEvent(FileReaderWriterTools.FileReaderWriterTools):
    def getSkipOffset(self):
        format = "4f2i"
        return struct.calcsize(format)

    def read(self, file):
        assert file.mode == 'rb'

        self.X = self.readFloat(file)
        self.Y = self.readFloat(file)
        self.Z = self.readFloat(file)
        self.E = self.readFloat(file)
        self.Intersect = self.readInt(file)
        self.id = self.readInt(file)
