#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2620 $"
__svnDate__ = "$Date: 2011-12-07 11:01:42 -0500 (Wed, 07 Dec 2011) $"
__svnId__ = "$Id: test_RegionOptions.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.

# Local modules.
import casinotools.fileformat.casino2.RegionOptions as RegionOptions
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestRegionOptions(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        regionOptions = RegionOptions.RegionOptions(500)
        regionOptions.read(file)

        self.assertEquals(1, regionOptions._numberRegions)

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
