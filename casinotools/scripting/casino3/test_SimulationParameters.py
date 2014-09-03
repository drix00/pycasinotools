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

# Project modules
from casinotools.scripting.casino3 import SimulationParameters

# Globals and constants variables.

class TestSimulationParameters(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_setEnegies(self):
        parameters = SimulationParameters.SimulationParameters()

        self.assertRaises(KeyError, parameters.getEnergies)

        energiesRef = [200.0]
        parameters.setEnergies(energiesRef[0])
        energies = parameters.getEnergies()
        self.assertEquals(1, len(energies))
        for energyRef, energy in zip(energiesRef, energies):
            self.assertAlmostEquals(energyRef, energy)

        energiesRef = [100, 200.0, 300.0]
        parameters.setEnergies(energiesRef)
        energies = parameters.getEnergies()
        self.assertEquals(3, len(energies))
        for energyRef, energy in zip(energiesRef, energies):
            self.assertAlmostEquals(energyRef, energy)

        energies = parameters[SimulationParameters.ENERGIES]
        self.assertEquals(3, len(energies))
        for energyRef, energy in zip(energiesRef, energies):
            self.assertAlmostEquals(energyRef, energy)

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

if __name__ == '__main__':    #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.main()
