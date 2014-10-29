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

# Third party modules.

# Local modules.
from casinotools.analysis.casino3 import simulation

# Globals and constants variables.

class TestAnalyzeCasinoSimulation(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.analyze = simulation.AnalyzeCasinoSimulation()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_extractBeamDistribution(self):
        text = "bG"
        valueRef = "G"
        value = self.analyze._extractBeamDistribution(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractNumberPoints(self):
        text = "201pts"
        valueRef = "201"
        value = self.analyze._extractNumberPoints(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractEnergy(self):
        text = "E200.0keV"
        valueRef = "200.0"
        value = self.analyze._extractEnergy(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractBeamDiameter(self):
        text = "db0.1nm"
        valueRef = "0.1"
        value = self.analyze._extractBeamDiameter(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractSemiAngle(self):
        text = "a0.0mrad"
        valueRef = "0.0"
        value = self.analyze._extractSemiAngle(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractSphereRadius(self):
        text = "sr0.5nm"
        valueRef = "0.5"
        value = self.analyze._extractSphereRadius(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractNumberElectrons(self):
        text = "N1ke"
        valueRef = "1k"
        value = self.analyze._extractNumberElectrons(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractSampleRotation(self):
        text = "t-45deg"
        valueRef = "-45"
        value = self.analyze._extractSampleRotation(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

    def test_extractDistance(self):
        text = "d800nm"
        valueRef = "800"
        value = self.analyze._extractDistance(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':    #pragma: no cover
    import nose
    nose.main()
