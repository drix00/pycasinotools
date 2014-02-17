#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2378 $"
__svnDate__ = "$Date: 2011-06-20 15:45:48 -0400 (Mon, 20 Jun 2011) $"
__svnId__ = "$Id: test_TrajectoryCollision.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.TrajectoryCollision as TrajectoryCollision
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestTrajectoryCollision(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        results = TrajectoryCollision.TrajectoryCollision()
        file = open(self.filepathCas, 'rb')
        file.seek(4042617)

        error = results.read(file)
        self.assertEquals(None, error)
        self.assertAlmostEquals(-9.168622881064E-02, results._positionX)
        self.assertAlmostEquals(-4.931083223782E-01, results._positionY)
        self.assertAlmostEquals(-1.049980000000E+05, results._positionZ)
        self.assertAlmostEquals(8.000000000000E-01, results._energy)
        self.assertAlmostEquals(1.000000000000E+04, results._segmentLength)
        self.assertEquals(3, results._collisionType)
        self.assertEquals(-1, results._regionID)

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
