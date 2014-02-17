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
__svnId__ = "$Id: SampleReader.py 2364 2011-05-30 11:15:15Z hdemers $"

# Standard library modules.
import struct
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.Tags as Tags

# Globals and constants variables.

class SampleReader(object):
    def __init__(self):
        self._sample = None

    def read(self, file):
        assert file.mode == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = "*CASINOSAMPLE%%"

        if Tags.searchTag(file, tagID, Tags.TAG_LENGTH):
            format = "i"
            size = struct.calcsize(format)
            buffer = file.read(size)
            items = struct.unpack_from(format, buffer)
            self._version = int(items[0])

        return None

    def getSample(self):
        return self._sample

if __name__ == '__main__':    #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
