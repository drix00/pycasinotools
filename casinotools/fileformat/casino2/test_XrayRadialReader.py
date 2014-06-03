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
__svnId__ = "$Id: test_XrayRadialReader.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import os.path

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.attrib import attr

# Local modules.
import casinotools.fileformat.casino2.XrayRadialReader as XrayRadialReader
import casinotools.fileformat.casino2.XrayRadial as XrayRadial

# Globals and constants variables.

class TestXrayRadialReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        basepath = resource_filename(__name__, "../../testData/casino2.x/exportedData")
        self.filepath_Cu_K = os.path.join(basepath, "XrayRadial_Cu_K.txt")
        self.filepath_Cu_L = os.path.join(basepath, "XrayRadial_Cu_L.txt")
        self.filepath_Au_M = os.path.join(basepath, "XrayRadial_Au_M.txt")
        self.filepath_Cu = os.path.join(basepath, "XrayRadial_Cu.txt")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    @attr('ignore')
    def test_readTextFile(self):
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_K)

        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEquals(XrayRadialReader.K, xrayRadial.getLine())
        self.assertEquals("Cu", xrayRadial.getElementSymbol())

        dataLabelsRef = [XrayRadial.DISTANCE_nm, XrayRadial.INTENSITY, XrayRadial.INTENSITY_ABSORBED]
        self.assertEquals(dataLabelsRef, xrayRadial.getDataLabels())

        distances_nm = xrayRadial.getDistances_nm()
        self.assertEquals(500, len(distances_nm))
        self.assertAlmostEquals(0.0, distances_nm[0])
        self.assertAlmostEquals(953.396625, distances_nm[-1])

        intensities = xrayRadial.getIntensities()
        self.assertEquals(500, len(intensities))
        self.assertAlmostEquals(111.260633, intensities[0])
        self.assertAlmostEquals(0.000128, intensities[-1])

        intensitiesAbsorbed = xrayRadial.getIntensitiesAbsorbed()
        self.assertEquals(500, len(intensitiesAbsorbed))
        self.assertAlmostEquals(111.007526, intensitiesAbsorbed[0])
        self.assertAlmostEquals(0.000127, intensitiesAbsorbed[-1])

        #self.fail("Test if the testcase is working.")

    @attr('ignore')
    def test_getLine(self):
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_K)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEquals(XrayRadialReader.K, xrayRadial.getLine())

        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_L)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.L)
        self.assertEquals(XrayRadialReader.L, xrayRadial.getLine())

        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Au_M)
        xrayRadial = xrayRadialReader.getData('Au', XrayRadialReader.M)
        self.assertEquals(XrayRadialReader.M, xrayRadial.getLine())

        #self.fail("Test if the testcase is working.")

    @attr('ignore')
    def test_getElementSymbol(self):
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_K)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEquals("Cu", xrayRadial.getElementSymbol())

        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu_L)
        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.L)
        self.assertEquals("Cu", xrayRadial.getElementSymbol())

        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Au_M)
        xrayRadial = xrayRadialReader.getData('Au', XrayRadialReader.M)
        self.assertEquals("Au", xrayRadial.getElementSymbol())

        #self.fail("Test if the testcase is working.")

    def NOtestReadElement(self):
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader.readTextFile(self.filepath_Cu)

        self.assertEquals(XrayRadialReader.HEADER_ELEMENT, xrayRadialReader._version)

        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.K)
        self.assertEquals("Cu", xrayRadial.getElementSymbol())
        self.assertEquals(XrayRadialReader.K, xrayRadial.getLine())

        xrayRadial = xrayRadialReader.getData('Cu', XrayRadialReader.L)
        self.assertEquals("Cu", xrayRadial.getElementSymbol())
        self.assertEquals(XrayRadialReader.L, xrayRadial.getLine())

    def test__setTextFileVersion(self):
        line = "Radial XRay Distribution Layer MV of Element Au"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._setTextFileVersion(line)
        self.assertEquals(XrayRadialReader.HEADER_ELEMENT_LINE, xrayRadialReader._version)

        line = "Radial Distribution of Cu"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._setTextFileVersion(line)
        self.assertEquals(XrayRadialReader.HEADER_ELEMENT, xrayRadialReader._version)

        line = "XRay Radial of Cu"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._setTextFileVersion(line)
        self.assertEquals(XrayRadialReader.HEADER_ALL, xrayRadialReader._version)

        #self.fail("Test if the testcase is working.")

    def test__extractDataLabelLineDataElement(self):
        line = "Distance(nm)\tIntensity: K\tIntensity: K ABS\tIntensity: LIII\tIntensity: LIII ABS"
        xrayRadialReader = XrayRadialReader.XrayRadialReader()
        xrayRadialReader._extractDataLabelLineDataElement(line)
        labels = xrayRadialReader._labels
        self.assertEquals(XrayRadial.DISTANCE_nm, labels[0])

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
