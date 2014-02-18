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
__svnId__ = "$Id: test_GenerateSimFile.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport

# Local modules.
import GenerateSimFile

# Globals and constants variables.

class TestGenerateSimFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathStd = resource_filename(__name__, "../../testData/casino2.x/std_B_04.0keV_40.0TOA.sim")
        self.generate = GenerateSimFile.GenerateSimFile(self.filepathStd)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_setIncidentEnergy_keV(self):
        energyRef_keV = 10.0
        self.generate.setIncidentEnergy_keV(energyRef_keV)

        energy_keV = self.generate.getOptionSimulationData().getSimulationOptions().getIncidentEnergy_keV()
        self.assertAlmostEquals(energyRef_keV, energy_keV)

        #self.fail("Test if the testcase is working.")

    def test_setTOA_deg(self):
        toaRef_deg = 52.5
        self.generate.setTOA_deg(toaRef_deg)

        toa_deg = self.generate.getOptionSimulationData().getSimulationOptions().getTOA_deg()
        self.assertAlmostEquals(toaRef_deg, toa_deg)

        #self.fail("Test if the testcase is working.")

    def test_addElement(self):
        self.generate._removeAllElements()

        symbolRef = 'Cu'
        self.generate._addElement(symbolRef)
        symbol = self.generate.getOptionSimulationData().getRegionOptions().getRegion(0).getElement(0).getSymbol()
        self.assertEquals(symbolRef, symbol)

        self.generate._removeAllElements()
        symbolRef = 'B'
        self.generate._addElement(symbolRef, 0.7981)
        symbolRef = 'C'
        self.generate._addElement(symbolRef, 1.0 - 0.7981)

        element = self.generate.getOptionSimulationData().getRegionOptions().getRegion(0).getElement(0)
        self.assertEquals(5, element.Z)
        self.assertEquals('B', element.Nom)
        self.assertAlmostEquals(2.340000000000E+00, element.Rho)
        self.assertAlmostEquals(1.081000000000E+01, element.A)
        self.assertAlmostEquals(5.750000000000E-02, element.J)
        self.assertAlmostEquals(7.790367583747E-01, element.K)
        self.assertAlmostEquals(1.0, element.ef)
        self.assertAlmostEquals(7.000000000000, element.kf * 1.0e-7)
        self.assertAlmostEquals(2.270000000000E+01, element.ep)

        composition = element.getComposition()
        self.assertEquals(0, composition.NuEl)
        self.assertAlmostEquals(7.981000000000E-01, composition.FWt)
        #self.assertAlmostEquals(8.145442797934E-01, composition.FAt)
        self.assertAlmostEquals(0.0, composition.SigmaT)
        self.assertAlmostEquals(0.0, composition.SigmaTIne)
        self.assertEquals(1, composition.Rep)

        element = self.generate.getOptionSimulationData().getRegionOptions().getRegion(0).getElement(1)
        self.assertEquals(6, element.Z)
        self.assertEquals('C', element.Nom)
        self.assertAlmostEquals(2.620000000000E+00, element.Rho)
        self.assertAlmostEquals(1.201100000000E+01, element.A)
        self.assertAlmostEquals(6.900000000000E-02, element.J)
        self.assertAlmostEquals(7.843098263659E-01, element.K)
        self.assertAlmostEquals(1.0, element.ef)
        self.assertAlmostEquals(7.000000000000, element.kf * 1.0e-7)
        self.assertAlmostEquals(1.500000000000E+01, element.ep)

        composition = element.getComposition()
        self.assertEquals(0, composition.NuEl)
        self.assertAlmostEquals(2.019000000000E-01, composition.FWt)
        #self.assertAlmostEquals(1.854557202066E-01, composition.FAt)
        self.assertAlmostEquals(0.0, composition.SigmaT)
        self.assertAlmostEquals(0.0, composition.SigmaTIne)
        self.assertEquals(1, composition.Rep)

        #self.fail("Test if the testcase is working.")

    def test_addElements(self):
        symbols = ['B']
        self.generate.addElements(symbols)
        element = self.generate.getOptionSimulationData().getRegionOptions().getRegion(0).getElement(0)
        self.assertEquals(5, element.Z)
        composition = element.getComposition()
        self.assertEquals(0, composition.NuEl)
        self.assertAlmostEquals(1.0, composition.FWt)
        self.assertAlmostEquals(1.0, composition.FAt)

        symbols = ['B', 'C']
        weightFractions = [0.7981, 1.0 - 0.7981]
        self.generate.addElements(symbols, weightFractions)

        region = self.generate.getOptionSimulationData().getRegionOptions().getRegion(0)

        self.assertEquals(2, region.getNumberElements())
        self.assertAlmostEquals(2.3916, region.getMeanMassDensity_g_cm3(), 4)
        self.assertAlmostEquals(5.5, region.getMeanAtomicNumber())
        self.assertEquals('BC' , region.getName())

        element = region.getElement(0)
        self.assertEquals(5, element.Z)
        composition = element.getComposition()
        self.assertEquals(0, composition.NuEl)
        self.assertAlmostEquals(7.981000000000E-01, composition.FWt)
        self.assertAlmostEquals(8.145442797934E-01, composition.FAt)

        element = region.getElement(1)
        self.assertEquals(6, element.Z)
        composition = element.getComposition()
        self.assertEquals(0, composition.NuEl)
        self.assertAlmostEquals(2.019000000000E-01, composition.FWt)
        self.assertAlmostEquals(1.854557202066E-01, composition.FAt)

        #self.fail("Test if the testcase is working.")

    def test_removeAllElements(self):
        numberElement = self.generate.getOptionSimulationData().getRegionOptions().getRegion(0).getNumberElements()
        self.assertEquals(1, numberElement)

        self.generate._removeAllElements()
        numberElement = self.generate.getOptionSimulationData().getRegionOptions().getRegion(0).getNumberElements()
        self.assertEquals(0, numberElement)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
