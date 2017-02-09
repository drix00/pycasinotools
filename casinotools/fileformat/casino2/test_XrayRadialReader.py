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
import os.path

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.XrayRadialReader as XrayRadialReader
import casinotools.fileformat.casino2.XrayRadial as XrayRadial
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestXrayRadialReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        basepath = resource_filename(__name__, "../../../test_data/casino2.x/exportedData")
        self.filepath_Cu_K = os.path.join(basepath, "XrayRadial_Cu_K.txt")
        self.filepath_Cu_L = os.path.join(basepath, "XrayRadial_Cu_L.txt")
        self.filepath_Au_M = os.path.join(basepath, "XrayRadial_Au_M.txt")
        self.filepath_Cu = os.path.join(basepath, "XrayRadial_Cu.txt")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_readTextFile(self):
        if is_bad_file(self.filepath_Cu_K):
            raise SkipTest
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_K)

        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEqual(XrayRadialReader.K, xrayRadial.getLine())
        self.assertEqual("Cu", xrayRadial.getElementSymbol())

        dataLabelsRef = [XrayRadial.DISTANCE_nm, XrayRadial.INTENSITY, XrayRadial.INTENSITY_ABSORBED]
        self.assertEqual(dataLabelsRef, xrayRadial.getDataLabels())

        distances_nm = xrayRadial.getDistances_nm()
        self.assertEqual(500, len(distances_nm))
        self.assertAlmostEqual(0.0, distances_nm[0])
        self.assertAlmostEqual(953.396625, distances_nm[-1])

        intensities = xrayRadial.getIntensities()
        self.assertEqual(500, len(intensities))
        self.assertAlmostEqual(111.260633, intensities[0])
        self.assertAlmostEqual(0.000128, intensities[-1])

        intensitiesAbsorbed = xrayRadial.getIntensitiesAbsorbed()
        self.assertEqual(500, len(intensitiesAbsorbed))
        self.assertAlmostEqual(111.007526, intensitiesAbsorbed[0])
        self.assertAlmostEqual(0.000127, intensitiesAbsorbed[-1])

        #self.fail("Test if the testcase is working.")

    def test_getLine(self):
        if is_bad_file(self.filepath_Cu_K):
            raise SkipTest
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_K)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEqual(XrayRadialReader.K, xrayRadial.getLine())

        if is_bad_file(self.filepath_Cu_L):
            raise SkipTest
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_L)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.L)
        self.assertEqual(XrayRadialReader.L, xrayRadial.getLine())

        if is_bad_file(self.filepath_Au_M):
            raise SkipTest
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Au_M)
        xrayRadial = xrayRadialReader.getData('Au', XrayRadialReader.M)
        self.assertEqual(XrayRadialReader.M, xrayRadial.getLine())

        #self.fail("Test if the testcase is working.")

    def test_getElementSymbol(self):
        if is_bad_file(self.filepath_Cu_K):
            raise SkipTest
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_K)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEqual("Cu", xrayRadial.getElementSymbol())

        if is_bad_file(self.filepath_Cu_L):
            raise SkipTest
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_L)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.L)
        self.assertEqual("Cu", xrayRadial.getElementSymbol())

        if is_bad_file(self.filepath_Au_M):
            raise SkipTest
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Au_M)
        xrayRadial = xrayRadialReader.getData('Au', XrayRadialReader.M)
        self.assertEqual("Au", xrayRadial.getElementSymbol())

        #self.fail("Test if the testcase is working.")

    def NOtestReadElement(self):
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu)

        self.assertEqual(XrayRadialReader.HEADER_ELEMENT, xrayRadialReader._version)

        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEqual("Cu", xrayRadial.getElementSymbol())
        self.assertEqual(XrayRadialReader.K, xrayRadial.getLine())

        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.L)
        self.assertEqual("Cu", xrayRadial.getElementSymbol())
        self.assertEqual(XrayRadialReader.L, xrayRadial.getLine())

    def test__setTextFileVersion(self):
        line = "Radial XRay Distribution Layer MV of Element Au"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._setTextFileVersion(line)
        self.assertEqual(XrayRadialReader.HEADER_ELEMENT_LINE, xrayRadialReader._version)

        line = "Radial Distribution of Cu"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._setTextFileVersion(line)
        self.assertEqual(XrayRadialReader.HEADER_ELEMENT, xrayRadialReader._version)

        line = "XRay Radial of Cu"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._setTextFileVersion(line)
        self.assertEqual(XrayRadialReader.HEADER_ALL, xrayRadialReader._version)

        #self.fail("Test if the testcase is working.")

    def test__extractDataLabelLineDataElement(self):
        line = "Distance(nm)\tIntensity: K\tIntensity: K ABS\tIntensity: LIII\tIntensity: LIII ABS"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._extractDataLabelLineDataElement(line)
        labels = xrayRadialReader._labels
        self.assertEqual(XrayRadial.DISTANCE_nm, labels[0])

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
