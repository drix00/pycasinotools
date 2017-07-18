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
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino3.TrajectoryCollision as TrajectoryCollision
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestTrajectoryCollision(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        file.seek(4042617)
        results = TrajectoryCollision.TrajectoryCollision()

        error = results.read(file)
        self.assertEqual(None, error)
        self.assertAlmostEqual(-9.168622881064E-02, results._positionX)
        self.assertAlmostEqual(-4.931083223782E-01, results._positionY)
        self.assertAlmostEqual(-1.049980000000E+05, results._positionZ)
        self.assertAlmostEqual(8.000000000000E-01, results._energy)
        self.assertAlmostEqual(1.000000000000E+04, results._segmentLength)
        self.assertEqual(3, results._collisionType)
        self.assertEqual(-1, results._regionID)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
