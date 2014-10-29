#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.Region as Region
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestRegion(test_File.TestFile):

    def test_read(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        region = Region.Region(500)
        region.read(file)

        self.assertEquals(0, region.ID)
        self.assertEquals("BC", region.Name)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
