#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2010 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.ScanPointsFile.LineXPattern as LineXPattern

# Globals and constants variables.

class TestLineXPattern(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_getScanPoints(self):
        line = LineXPattern.LineXPattern()

        line.setCenterPoint_nm((5.0, -250.0))
        line.setStep_nm(10.0)
        line.setRange_nm(20.0)

        scanPoints = line.getScanPoints()

        scanPointsRef = [(-5.0, -250.0), (5.0, -250.0), (15.0, -250.0)]

        self.assertEquals(len(scanPointsRef), len(scanPoints))

        for pointRef, point in zip(scanPointsRef, scanPoints):
                xRef, yRef = pointRef
                x, y = point
                self.assertAlmostEquals(xRef, x)
                self.assertAlmostEquals(yRef, y)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
