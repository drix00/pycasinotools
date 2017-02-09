#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.SimulationData as SimulationData
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.
from casinotools.fileformat.casino2.SimulationData import \
    EMITTED, GENERATED, LINE_K, LINE_L, LINE_M

class TestSimulationData(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file)

        #self.fail("Test if the testcase is working.")

    def test_read_StringIO(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        simulationData = SimulationData.SimulationData()
        simulationData.read(file)

        self.assertEqual("WinCasino Simulation File", simulationData._header)
        self.assertEqual(26, simulationData._version)
        self.assertEqual('n', simulationData._status)
        self.assertEqual(True, simulationData._saveSimulations)
        self.assertEqual(True, simulationData._saveRegions)
        self.assertEqual(False, simulationData._saveTrajectories)
        self.assertEqual(False, simulationData._saveDistributions)

    def testGetTotalXrayIntensities(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        # Single region
        f = open(self.filepathCas, 'rb')
        f.seek(98348)
        simulationData = SimulationData.SimulationData()
        simulationData.read(f)
        f.close()

        intensities = simulationData.getTotalXrayIntensities()

        self.assertAlmostEqual(2538.63, intensities[5][LINE_K][GENERATED], 2)
        self.assertAlmostEqual(344.49, intensities[5][LINE_K][EMITTED], 2)

        self.assertAlmostEqual(111.30, intensities[6][LINE_K][GENERATED], 2)
        self.assertAlmostEqual(46.88, intensities[6][LINE_K][EMITTED], 2)

        # Multiple regions
        if is_bad_file(self.filepathCas_nicr):
            raise SkipTest
        f = open(self.filepathCas_nicr, 'rb')
        f.seek(98348)
        simulationData = SimulationData.SimulationData()
        simulationData.read(f)
        f.close()

        intensities = simulationData.getTotalXrayIntensities()

        self.assertAlmostEqual(0.76, intensities[79][LINE_M][GENERATED], 2)
        self.assertAlmostEqual(0.52, intensities[79][LINE_M][EMITTED], 2)

        self.assertAlmostEqual(293.88, intensities[24][LINE_K][GENERATED], 2)
        self.assertAlmostEqual(290.78, intensities[24][LINE_K][EMITTED], 2)
        self.assertAlmostEqual(712.32, intensities[24][LINE_L][GENERATED], 2)
        self.assertAlmostEqual(430.56, intensities[24][LINE_L][EMITTED], 2)

        self.assertAlmostEqual(6.62, intensities[28][LINE_K][GENERATED], 2)
        self.assertAlmostEqual(6.53, intensities[28][LINE_K][EMITTED], 2)
        self.assertAlmostEqual(1115.51, intensities[28][LINE_L][GENERATED], 2)
        self.assertAlmostEqual(457.79, intensities[28][LINE_L][EMITTED], 2)

        self.assertAlmostEqual(1.57, intensities[14][LINE_K][GENERATED], 2)
        self.assertAlmostEqual(1.22, intensities[14][LINE_K][EMITTED], 2)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
