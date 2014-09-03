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
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.Tags as Tags

# Globals and constants variables.

class SampleReader(object):
    def __init__(self):
        self._sample = None

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = b"*CASINOSAMPLE%%"

        if Tags.searchTag(file, tagID, Tags.TAG_LENGTH):
            format = "i"
            size = struct.calcsize(format)
            buffer = file.read(size)
            items = struct.unpack_from(format, buffer)
            self._version = int(items[0])

        return None

    def getSample(self):
        return self._sample
