#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 1755 $"
__svnDate__ = "$Date: 2010-01-20 17:06:10 -0500 (Wed, 20 Jan 2010) $"
__svnId__ = "$Id: test_RegionOptions.py 1755 2010-01-20 22:06:10Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import RegionOptions
import casinoTools.FileFormat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestRegionOptions(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        file.seek(6536)
        regionOptions = RegionOptions.RegionOptions()
        regionOptions.read(file)

        self.assertEquals(8, regionOptions._numberRegions)

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
