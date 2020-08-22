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
import casinotools.file_format.casino3.region_intensity_info as RegionIntensityInfo
import tests.file_format.test_file_reader_writer_tools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestRegionIntensityInfo(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            pytest.skip()
        file = open(self.filepathCas, 'rb')
        file.seek(2012986)
        results = RegionIntensityInfo.RegionIntensityInfo()
        error = results.read(file)

        self.assertEqual(None, error)

        self.assertEqual(30105022, results._version)
        self.assertAlmostEqual(0.0, results._energyIntensity)
        self.assertEqual(1, results._regionID)
        self.assertAlmostEqual(0.0, results._normalizedEnergyIntensity)

        error = results.read(file)
        self.assertEqual(None, error)
        self.assertEqual(30105022, results._version)
        self.assertAlmostEqual(0.0, results._energyIntensity)
        self.assertEqual(2, results._regionID)
        self.assertAlmostEqual(0.0, results._normalizedEnergyIntensity)

        error = results.read(file)
        self.assertEqual(None, error)
        self.assertEqual(30105022, results._version)
        self.assertAlmostEqual(7.268071702406E+05, results._energyIntensity)
        self.assertEqual(3, results._regionID)
        self.assertAlmostEqual(7.268071702406E-01, results._normalizedEnergyIntensity)
