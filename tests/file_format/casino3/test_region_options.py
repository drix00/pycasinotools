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
import pytest

# Local modules.
import casinotools.file_format.casino3.region_options as RegionOptions
import tests.file_format.test_file_reader_writer_tools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestRegionOptions(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            pytest.skip()
        file = open(self.filepathSim, 'rb')
        file.seek(6536)
        regionOptions = RegionOptions.RegionOptions()
        regionOptions.read(file)

        self.assertEqual(8, regionOptions._numberRegions)
