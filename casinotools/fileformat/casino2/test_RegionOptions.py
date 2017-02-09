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

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.RegionOptions as RegionOptions
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestRegionOptions(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        regionOptions = RegionOptions.RegionOptions(500)
        regionOptions.read(file)

        self.assertEqual(1, regionOptions._numberRegions)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
