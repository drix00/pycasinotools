#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2620 $"
__svnDate__ = "$Date: 2011-12-07 11:01:42 -0500 (Wed, 07 Dec 2011) $"
__svnId__ = "$Id: test_SimulationData.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
from StringIO import StringIO

# Third party modules.

# Local modules.
import SimulationData
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.
from SimulationData import EMITTED, GENERATED, LINE_K, LINE_L, LINE_M

class TestSimulationData(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        self._read_tests(file)

        #self.fail("Test if the testcase is working.")

    def test_read_StringIO(self):
        f = open(self.filepathSim, 'rb')
        file = StringIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        simulationData = SimulationData.SimulationData()
        simulationData.read(file)

        self.assertEquals("WinCasino Simulation File", simulationData._header)
        self.assertEquals(26, simulationData._version)
        self.assertEquals('n', simulationData._status)
        self.assertEquals(True, simulationData._saveSimulations)
        self.assertEquals(True, simulationData._saveRegions)
        self.assertEquals(False, simulationData._saveTrajectories)
        self.assertEquals(False, simulationData._saveDistributions)

    def testGetTotalXrayIntensities(self):
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
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
