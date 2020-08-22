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
import pytest

# Local modules.
import casinotools.file_format.casino2.trajectories_data as TrajectoriesData
import tests.file_format.casino2.test_file as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestTrajectoriesData(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            pytest.skip()
        with open(self.filepathCas, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathCas):
            pytest.skip()
        f = open(self.filepathCas, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        trajectoriesData = TrajectoriesData.TrajectoriesData()
        trajectoriesData.read(file)

        file.seek(98348)
        trajectoriesData = TrajectoriesData.TrajectoriesData()
        trajectoriesData.read(file)
        self.assertEqual(221, trajectoriesData._numberTrajectories)
