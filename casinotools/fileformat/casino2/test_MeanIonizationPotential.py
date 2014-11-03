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
import casinotools.fileformat.casino2.MeanIonizationPotential as MeanIonizationPotential

# Globals and constants variables.

class TestMeanIonizationPotential(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_computeJ(self):
        meanIonizationPotential = MeanIonizationPotential.MeanIonizationPotential(MeanIonizationPotential.MODEL_JOY)

        jRef = 5.75e-2
        j = meanIonizationPotential.computeJ(5)
        self.assertAlmostEqual(jRef, j)

        jRef = 6.9e-2
        j = meanIonizationPotential.computeJ(6)
        self.assertAlmostEqual(jRef, j)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
