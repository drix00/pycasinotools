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
import casinotools.fileformat.casino3.Trajectory as Trajectory
import tests.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestTrajectory(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            pytest.skip()
        file = open(self.filepathCas, 'rb')
        file.seek(4042541)
        results = Trajectory.Trajectory()

        self.assertTrue(file is not None)
        error = results.read(file)
        self.assertEqual(None, error)
        version = results.getVersion()
        self.assertEqual(30105012, version)

        self.assertEqual(256, results._type)

        self.assertEqual(1, results._order)
        self.assertAlmostEqual(-3.071803288788E-01, results._dirX)
        self.assertAlmostEqual(8.927911784036E-02, results._dirY)
        self.assertAlmostEqual(9.474542124386E-01, results._dirZ)
        self.assertEqual(28, results._numberScatteringEvents)
