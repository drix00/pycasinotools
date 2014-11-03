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
import casinotools.fileformat.casino3.ScanPointsFile.ImageXZPattern as ImageXZPattern

# Globals and constants variables.

class TestImageXZPattern(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_getScanPoints(self):
        imageXZ = ImageXZPattern.ImageXZPattern()

        imageXZ.setCenterPoint_nm((5.0, -350.0))
        imageXZ.setStepX_nm(10.0)
        imageXZ.setRangeX_nm(20.0)
        imageXZ.setStepZ_nm(200.0)
        imageXZ.setRangeZ_nm(200.0)

        scanPoints = imageXZ.getScanPoints()

        scanPointsRef = [(-5.0, -450.0), (5.0, -450.0), (15.0, -450.0), (-5.0, -250.0), (5.0, -250.0), (15.0, -250.0)]

        self.assertEqual(len(scanPointsRef), len(scanPoints))

        for pointRef, point in zip(scanPointsRef, scanPoints):
                xRef, yRef = pointRef
                x, y = point
                self.assertAlmostEqual(xRef, x)
                self.assertAlmostEqual(yRef, y)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
