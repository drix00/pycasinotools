#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest
import os.path

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.attrib import attr

# Local modules.
import IntensityImage

# Globals and constants variables.

class TestIntensityImage(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        resultsPath = resource_filename(__name__, "../../testData/casino3.x/createImage")
        self._casBinnedFilepath = os.path.join(resultsPath, "Au_C_thin_1nm_Inside_100ke_binned.cas")
        self._casAllFilepath = os.path.join(resultsPath, "Au_C_thin_1nm_Inside_100ke_all.cas")

        self._imageBinned = IntensityImage.IntensityImage(self._casBinnedFilepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_init(self):
        image = self._imageBinned
        self.assertEquals(self._casBinnedFilepath, image._filepath)
        self.assertEquals(IntensityImage.INTENSITY_TRANSMITTED_DETECTED, image._intensityType)

        #self.fail("Test if the testcase is working.")

    @attr('ignore')
    def test_extractData(self):
        image = self._imageBinned
        image._extractData()

        self.assertEquals(100, image._numberScanPoints)

        self.assertEquals(100, len(image._positions))
        self.assertEquals(100, len(image._intensities))

        #self.fail("Test if the testcase is working.")

    def test_analyzePositionsXY(self):
        positions = []
        positions.append((-5, -5, 0))
        positions.append((0, -5, 0))
        positions.append((5, -5, 0))
        positions.append((-5, 0, 0))
        positions.append((0, 0, 0))
        positions.append((5, 0, 0))
        positions.append((-5, 5, 0))
        positions.append((0, 5, 0))
        positions.append((5, 5, 0))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("XY", image._imageType)
        #self.fail("Test if the testcase is working.")

    def test_analyzePositionsXZ(self):
        positions = []
        positions.append((-5, 0, -5))
        positions.append((0, 0, -5))
        positions.append((5, 0, -5))
        positions.append((-5, 0, 0))
        positions.append((0, 0, 0))
        positions.append((5, 0, 0))
        positions.append((-5, 0, 5))
        positions.append((0, 0, 5))
        positions.append((5, 0, 5))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("XZ", image._imageType)
        #self.fail("Test if the testcase is working.")

    def test_analyzePositionsYZ(self):
        positions = []
        positions.append((0, -5, -5))
        positions.append((0, 0, -5))
        positions.append((0, 5, -5))
        positions.append((0, -5, 0))
        positions.append((0, 0, 0))
        positions.append((0, 5, 0))
        positions.append((0, -5, 5))
        positions.append((0, 0, 5))
        positions.append((0, 5, 5))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("YZ", image._imageType)
        #self.fail("Test if the testcase is working.")

    def test_analyzePositionsX(self):
        positions = []
        positions.append((-5, 0, 0))
        positions.append((0, 0, 0))
        positions.append((5, 0, 0))
        positions.append((-5, 0, 0))
        positions.append((0, 0, 0))
        positions.append((5, 0, 0))
        positions.append((-5, 0, 0))
        positions.append((0, 0, 0))
        positions.append((5, 0, 0))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("X", image._imageType)
        #self.fail("Test if the testcase is working.")

    def test_analyzePositionsY(self):
        positions = []
        positions.append((0, -5, 0))
        positions.append((0, 0, 0))
        positions.append((0, 5, 0))
        positions.append((0, -5, 0))
        positions.append((0, 0, 0))
        positions.append((0, 5, 0))
        positions.append((0, -5, 0))
        positions.append((0, 0, 0))
        positions.append((0, 5, 0))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("Y", image._imageType)
        #self.fail("Test if the testcase is working.")

    def test_analyzePositionsZ(self):
        positions = []
        positions.append((0, 0, -5))
        positions.append((0, 0, -5))
        positions.append((0, 0, -5))
        positions.append((0, 0, 0))
        positions.append((0, 0, 0))
        positions.append((0, 0, 0))
        positions.append((0, 0, 5))
        positions.append((0, 0, 5))
        positions.append((0, 0, 5))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("Z", image._imageType)
        #self.fail("Test if the testcase is working.")

    def test_analyzePositionsP(self):
        positions = []
        positions.append((0, 0, 0))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("P", image._imageType)
        #self.fail("Test if the testcase is working.")

    def test_analyzePositions3D(self):
        positions = []
        positions.append((-5, -5, -5))
        positions.append((0, -5, -5))
        positions.append((5, -5, -5))
        positions.append((-5, 0, -5))
        positions.append((0, 0, -5))
        positions.append((5, 0, -5))
        positions.append((-5, 5, -5))
        positions.append((0, 5, -5))
        positions.append((5, 5, -5))

        positions.append((-5, -5, 0))
        positions.append((0, -5, 0))
        positions.append((5, -5, 0))
        positions.append((-5, 0, 0))
        positions.append((0, 0, 0))
        positions.append((5, 0, 0))
        positions.append((-5, 5, 0))
        positions.append((0, 5, 0))
        positions.append((5, 5, 0))

        positions.append((-5, -5, 5))
        positions.append((0, -5, 5))
        positions.append((5, -5, 5))
        positions.append((-5, 0, 5))
        positions.append((0, 0, 5))
        positions.append((5, 0, 5))
        positions.append((-5, 5, 5))
        positions.append((0, 5, 5))
        positions.append((5, 5, 5))

        image = self._imageBinned
        image._positions = positions
        image._analyzePositions()

        self.assertEquals("3D", image._imageType)
        #self.fail("Test if the testcase is working.")

    @attr('ignore')
    def test_createImage(self):
        image = self._imageBinned
        image._createImage()

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
