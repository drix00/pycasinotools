#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.ScanPointsFile.ScanPointsFile as ScanPointsFile

# Globals and constants variables.

class TestScanPointsFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self._scanPointsFile = ScanPointsFile.ScanPointsFile()
        self._scanPointsFile.setNumberPoints(100)
        self._scanPointsFile.setWidth_nm(10)
        self._scanPointsFile.setHeight_nm(10)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_computeSeparation_nm(self):
        self.assertEqual(None, self._scanPointsFile._separation_nm)

        self._scanPointsFile._computeSeparation_nm()
        separationRef_nm = 1.0
        self.assertAlmostEqual(separationRef_nm, self._scanPointsFile._separation_nm)

        self._scanPointsFile.setNumberPoints(10000)
        self._scanPointsFile._computeSeparation_nm()
        separationRef_nm = 0.1
        self.assertAlmostEqual(separationRef_nm, self._scanPointsFile._separation_nm)

        self._scanPointsFile.setNumberPoints(10)
        self._scanPointsFile._computeSeparation_nm()
        separationRef_nm = 3.1622776601683795
        self.assertAlmostEqual(separationRef_nm, self._scanPointsFile._separation_nm)

        self._scanPointsFile.setNumberPoints(100)
        self._scanPointsFile.setWidth_nm(50)
        self._scanPointsFile.setHeight_nm(50)
        self._scanPointsFile._computeSeparation_nm()
        separationRef_nm = 5.0
        self.assertAlmostEqual(separationRef_nm, self._scanPointsFile._separation_nm)

        self._scanPointsFile.setNumberPoints(100)
        self._scanPointsFile.setWidth_nm(50)
        self._scanPointsFile.setHeight_nm(10)
        self._scanPointsFile._computeSeparation_nm()
        separationRef_nm = 2.236067977499
        self.assertAlmostEqual(separationRef_nm, self._scanPointsFile._separation_nm)

        #self.fail("Test if the testcase is working.")

    def test_generateScanPoints(self):
        self.assertEqual([], self._scanPointsFile._scanPoints)

        self._scanPointsFile._generateScanPoints()
        self.assertEqual(100, len(self._scanPointsFile._scanPoints))

        firstPointRef_nm = (-4.5, -4.5)
        firstPoint_nm = self._scanPointsFile._scanPoints[0]
        self.assertAlmostEqual(firstPointRef_nm[0], firstPoint_nm[0])
        self.assertAlmostEqual(firstPointRef_nm[1], firstPoint_nm[1])

        lastPointRef_nm = (4.5, 4.5)
        lastPoint_nm = self._scanPointsFile._scanPoints[-1]
        self.assertAlmostEqual(lastPointRef_nm[0], lastPoint_nm[0])
        self.assertAlmostEqual(lastPointRef_nm[1], lastPoint_nm[1])

        #self.fail("Test if the testcase is working.")

    def test_generateLinescan(self):
        self.assertEqual([], self._scanPointsFile._scanPoints)

        self._scanPointsFile.setHeight_nm(100.0)
        self._scanPointsFile.setWidth_nm(0.0)

        self._scanPointsFile._generateScanPoints()
        self.assertEqual(100, len(self._scanPointsFile._scanPoints))

        firstPointRef_nm = (0.0, -49.5)
        firstPoint_nm = self._scanPointsFile._scanPoints[0]
        self.assertAlmostEqual(firstPointRef_nm[0], firstPoint_nm[0])
        self.assertAlmostEqual(firstPointRef_nm[1], firstPoint_nm[1])

        lastPointRef_nm = (0.0, 49.5)
        lastPoint_nm = self._scanPointsFile._scanPoints[-1]
        self.assertAlmostEqual(lastPointRef_nm[0], lastPoint_nm[0])
        self.assertAlmostEqual(lastPointRef_nm[1], lastPoint_nm[1])

        self._scanPointsFile.setHeight_nm(0.0)
        self._scanPointsFile.setWidth_nm(100.0)

        self._scanPointsFile._generateScanPoints()
        self.assertEqual(100, len(self._scanPointsFile._scanPoints))

        firstPointRef_nm = (-49.5, 0.0)
        firstPoint_nm = self._scanPointsFile._scanPoints[0]
        self.assertAlmostEqual(firstPointRef_nm[0], firstPoint_nm[0])
        self.assertAlmostEqual(firstPointRef_nm[1], firstPoint_nm[1])

        lastPointRef_nm = (49.5, 0.0)
        lastPoint_nm = self._scanPointsFile._scanPoints[-1]
        self.assertAlmostEqual(lastPointRef_nm[0], lastPoint_nm[0])
        self.assertAlmostEqual(lastPointRef_nm[1], lastPoint_nm[1])

        #self.fail("Test if the testcase is working.")

    def test_setCenterPoint(self):
        self.assertEqual([], self._scanPointsFile._scanPoints)

        self._scanPointsFile.setHeight_nm(100.0)
        self._scanPointsFile.setWidth_nm(0.0)
        xRef = -23.6
        yRef = 50.0
        self._scanPointsFile.setCenterPoint((xRef, yRef))

        self._scanPointsFile._generateScanPoints()
        self.assertEqual(100, len(self._scanPointsFile._scanPoints))

        firstPointRef_nm = (xRef, -49.5 + yRef)
        firstPoint_nm = self._scanPointsFile._scanPoints[0]
        self.assertAlmostEqual(firstPointRef_nm[0], firstPoint_nm[0])
        self.assertAlmostEqual(firstPointRef_nm[1], firstPoint_nm[1])

        lastPointRef_nm = (xRef, 49.5 + yRef)
        lastPoint_nm = self._scanPointsFile._scanPoints[-1]
        self.assertAlmostEqual(lastPointRef_nm[0], lastPoint_nm[0])
        self.assertAlmostEqual(lastPointRef_nm[1], lastPoint_nm[1])

        self._scanPointsFile.setHeight_nm(0.0)
        self._scanPointsFile.setWidth_nm(100.0)

        self._scanPointsFile._generateScanPoints()
        self.assertEqual(100, len(self._scanPointsFile._scanPoints))

        firstPointRef_nm = (-49.5 + xRef, 0.0 + yRef)
        firstPoint_nm = self._scanPointsFile._scanPoints[0]
        self.assertAlmostEqual(firstPointRef_nm[0], firstPoint_nm[0])
        self.assertAlmostEqual(firstPointRef_nm[1], firstPoint_nm[1])

        lastPointRef_nm = (49.5 + xRef, 0.0 + yRef)
        lastPoint_nm = self._scanPointsFile._scanPoints[-1]
        self.assertAlmostEqual(lastPointRef_nm[0], lastPoint_nm[0])
        self.assertAlmostEqual(lastPointRef_nm[1], lastPoint_nm[1])

        self._scanPointsFile.setWidth_nm(10)
        self._scanPointsFile.setHeight_nm(10)
        self._scanPointsFile.setCenterPoint((xRef, yRef))

        self._scanPointsFile._generateScanPoints()
        self.assertEqual(100, len(self._scanPointsFile._scanPoints))

        firstPointRef_nm = (-4.5 + xRef, -4.5 + yRef)
        firstPoint_nm = self._scanPointsFile._scanPoints[0]
        self.assertAlmostEqual(firstPointRef_nm[0], firstPoint_nm[0])
        self.assertAlmostEqual(firstPointRef_nm[1], firstPoint_nm[1])

        lastPointRef_nm = (4.5 + xRef, 4.5 + yRef)
        lastPoint_nm = self._scanPointsFile._scanPoints[-1]
        self.assertAlmostEqual(lastPointRef_nm[0], lastPoint_nm[0])
        self.assertAlmostEqual(lastPointRef_nm[1], lastPoint_nm[1])

        #self.fail("Test if the testcase is working.")

    def test_generateLines(self):
        lines = self._scanPointsFile._generateLines()
        self.assertEqual(100, len(lines))

        firstLinesRef_nm = "-4.500000, -4.500000\n"
        self.assertEqual(firstLinesRef_nm, lines[0])

        lastLinesRef_nm = "4.500000, 4.500000\n"
        self.assertEqual(lastLinesRef_nm, lines[-1])

        #self.fail("Test if the testcase is working.")

    def test_isLineValid(self):
        spf = self._scanPointsFile
        line = ""
        self.assertFalse(spf._isLineValid(line))

        line = "4.500000, 4.500000\n"
        self.assertTrue(spf._isLineValid(line))
        line = "4.500000, 4.500000\r"
        self.assertTrue(spf._isLineValid(line))
        line = "4.500000, 4.500000\r\n"
        self.assertTrue(spf._isLineValid(line))
        line = "-4.500000, -4.500000"
        self.assertFalse(spf._isLineValid(line))

        line = "-4.500000, -4.500000\n"
        self.assertTrue(spf._isLineValid(line))

        line = "4.500000 4.500000\n"
        self.assertFalse(spf._isLineValid(line))
        line = "-4.as000, -4.500000\n"
        self.assertFalse(spf._isLineValid(line))
        line = "-4.500000, -4.asd000\n"
        self.assertFalse(spf._isLineValid(line))
        line = "-e.500000, -4.500000\n"
        self.assertFalse(spf._isLineValid(line))
        line = "-4.500000, -a.500000\n"
        self.assertFalse(spf._isLineValid(line))

        line = "-4.500000, -4.500000\n"
        self.assertTrue(spf._isLineValid(line))

        line = "-4.50000000000000000000000000000, -4.50000000000000000000000000000\n"
        self.assertFalse(spf._isLineValid(line))

        #self.fail("Test if the testcase is working.")

    def test_DifferentNumberElectronsInYandZ(self):
        numberPointsList = [(300, 250), (300, 100), (300, 25)]
        for numberPointsY, numberPointsZ in numberPointsList:
            scanPointsFile = ScanPointsFile.ScanPointsFile()
            scanPointsFile.setWidth_nm(300, numberPointsY)
            scanPointsFile.setHeight_nm(2500, numberPointsZ)
            scanPointsFile.setCenterPoint((0.0, 500.0))

            self.assertEqual(numberPointsY * numberPointsZ, scanPointsFile.getNumberPoints())

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
