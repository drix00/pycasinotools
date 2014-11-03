#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino3.RegionOptions as RegionOptions
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestRegionOptions(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        file.seek(6536)
        regionOptions = RegionOptions.RegionOptions()
        regionOptions.read(file)

        self.assertEqual(8, regionOptions._numberRegions)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
