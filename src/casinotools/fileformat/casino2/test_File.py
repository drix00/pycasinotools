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
__svnId__ = "$Id: test_File.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
import unittest
import os
from StringIO import StringIO

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.tools import nottest

# Local modules.
import casinotools.fileformat.casino2.File as File
import Version
from casinotools.fileformat.casino2.Element import LINE_K, GENERATED, EMITTED

# Globals and constants variables.

class TestFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = resource_filename(__name__, "../../testData/wincasino2.45/id475.sim")
        self.filepathCas = resource_filename(__name__, "../../testData/wincasino2.45/id475.cas")

        self.filepathStd = resource_filename(__name__, "../../testData/casino2.x/std_B_04.0keV_40.0TOA.sim")
        self.filepathWrite = resource_filename(__name__, "../../testData/casino2.x/stdTest.sim")

        self.filepathSim_v242 = resource_filename(__name__, "../../testData/casino2.x/std_B_3keV_v2.42_23.sim")
        self.filepathCas_v242 = resource_filename(__name__, "../../testData/casino2.x/std_B_3keV_v2.42_23.cas")

        self.filepathCas_nicr = resource_filename(__name__, "../../testData/casino2.x/nicr.cas")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        if os.path.isfile(self.filepathWrite):
            os.remove(self.filepathWrite)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    @nottest
    def test_read(self):
        file = File.File()
        file.readFromFilepath(self.filepathSim)
        self.assertEquals(self.filepathSim, file._filepath)
        self.assertEquals(0, file._numberSimulations)

        file = File.File()
        file.readFromFilepath(self.filepathCas)
        self.assertEquals(self.filepathCas, file._filepath)
        self.assertEquals(1, file._numberSimulations)

        self.assertEquals(1, len(file._resultSimulationDataList))

        #self.fail("Test if the testcase is working.")

    @nottest
    def test_read_StringIO(self):
        # sim
        f = open(self.filepathSim, 'rb')
        buf = StringIO(f.read())
        buf.mode = 'rb'
        f.close()

        file = File.File()
        file.readFromFileObject(buf)
        self.assertEquals(0, file._numberSimulations)

        # cas
        f = open(self.filepathCas, 'rb')
        buf = StringIO(f.read())
        buf.mode = 'rb'
        f.close()

        file = File.File()
        file.readFromFileObject(buf)
        self.assertEquals(1, file._numberSimulations)

        self.assertEquals(1, len(file._resultSimulationDataList))

    def test_isSimulationFilepath(self):
        file = File.File()

        self.assertTrue(file._isSimulationFilepath(self.filepathSim))
        self.assertFalse(file._isSimulationFilepath(self.filepathCas))

        #self.fail("Test if the testcase is working.")

    @nottest
    def test_write(self):
        file = File.File()
        optionSimulationData = self._getOptionSimulationData()
        file.setOptionSimulationData(optionSimulationData)
        file.write(self.filepathWrite)

        dataRef = open(self.filepathStd).read()
        data = open(self.filepathWrite).read()
        index = 0
        for charRef, char in zip(dataRef, data):
            self.assertEquals(charRef, char, index)
            index += 1

        self.assertEquals(len(dataRef), len(data))

        import filecmp
        self.assertTrue(filecmp.cmp(self.filepathStd, self.filepathWrite, shallow=True))

        #self.fail("Test if the testcase is working.")

    def _getOptionSimulationData(self):
        file = File.File()
        file.readFromFilepath(self.filepathStd)

        return file.getOptionSimulationData()

    @nottest
    def test_skipReadingData(self):
        file = File.File()
        file.readFromFilepath(self.filepathCas, isSkipReadingData=False)

        trajectoriesData = file.getResultsFirstSimulation().getTrajectoriesData()
        self.assertEquals(221, trajectoriesData._numberTrajectories)
        self.assertEquals(89, trajectoriesData._trajectories[0].NbElec)
        self.assertEquals(89, len(trajectoriesData._trajectories[0]._scatteringEvents))

        event = trajectoriesData._trajectories[0]._scatteringEvents[0]
        self.assertAlmostEquals(-2.903983831406E+00, event.X)
        self.assertAlmostEquals(-3.020418643951E+00, event.Y)
        self.assertAlmostEquals(0.0, event.Z)
        self.assertAlmostEquals(4.000000000000E+00, event.E)
        self.assertEquals(0, event.Intersect)
        self.assertEquals(0, event.id)

        file = File.File()
        file.readFromFilepath(self.filepathCas, isSkipReadingData=True)

        trajectoriesData = file.getResultsFirstSimulation().getTrajectoriesData()
        self.assertEquals(221, trajectoriesData._numberTrajectories)
        self.assertEquals(89, trajectoriesData._trajectories[0].NbElec)
        self.assertEquals(0, len(trajectoriesData._trajectories[0]._scatteringEvents))

        simulationResults = file.getResultsFirstSimulation().getSimulationResults()

        self.assertEquals(1, simulationResults.BE_Intensity_Size)
        self.assertEquals(3.950000000000E-02, simulationResults.BE_Intensity[0])

        element = simulationResults._elementIntensityList[0]
        self.assertEquals("B", element.Name)
        self.assertAlmostEquals(3.444919288026E+02, element.IntensityK[0])

        element = simulationResults._elementIntensityList[1]
        self.assertEquals("C", element.Name)
        self.assertAlmostEquals(4.687551040349E+01, element.IntensityK[0])

        self.assertEquals(1000, simulationResults.NbPointDZMax)
        self.assertEquals(500, simulationResults.NbPointDENR)
        self.assertEquals(500, simulationResults.NbPointDENT)
        self.assertEquals(500, simulationResults.NbPointDRSR)
        #self.assertEquals(0, simulationResults.NbPointDNCR)
        self.assertEquals(50, simulationResults.NbPointDEpos_X)
        self.assertEquals(50, simulationResults.NbPointDEpos_Y)
        self.assertEquals(50, simulationResults.NbPointDEpos_Z)
        self.assertAlmostEquals(1.608165461510E-02, simulationResults.DEpos_maxE)
        self.assertEquals(91, simulationResults.NbPointDBANG)
        self.assertEquals(91, simulationResults.NbPointDAngleVSEnergie)

        #self.fail("Test if the testcase is working.")

    @nottest
    def test_readv242(self):
        # .sim
        file = File.File()
        file.readFromFilepath(self.filepathSim_v242)
        self.assertEquals(self.filepathSim_v242, file._filepath)
        self.assertEquals(0, file._numberSimulations)

        optionSimulationData = file.getOptionSimulationData()
        version = optionSimulationData.getVersion()
        self.assertEquals(Version.VERSION_2_42, version)

        simulationOptions = optionSimulationData.getSimulationOptions()

        numberElectrons = simulationOptions.getNumberElectrons()
        self.assertEquals(10000, numberElectrons)

        incidentEnergy_keV = simulationOptions.getIncidentEnergy_keV()
        self.assertAlmostEquals(3.0, incidentEnergy_keV)

        toa_deg = simulationOptions.getTOA_deg()
        self.assertAlmostEquals(40.0, toa_deg)

        numberXRayLayers = simulationOptions.getNumberXRayLayers()
        self.assertEquals(500, numberXRayLayers)

        # .cas
        file = File.File()
        file.readFromFilepath(self.filepathCas_v242)
        self.assertEquals(self.filepathCas_v242, file._filepath)
        self.assertEquals(1, file._numberSimulations)

        self.assertEquals(1, len(file._resultSimulationDataList))

        optionSimulationData = file.getOptionSimulationData()
        version = optionSimulationData.getVersion()
        self.assertEquals(Version.VERSION_2_42, version)

        simulationOptions = optionSimulationData.getSimulationOptions()

        numberElectrons = simulationOptions.getNumberElectrons()
        self.assertEquals(10000, numberElectrons)

        incidentEnergy_keV = simulationOptions.getIncidentEnergy_keV()
        self.assertAlmostEquals(3.0, incidentEnergy_keV)

        toa_deg = simulationOptions.getTOA_deg()
        self.assertAlmostEquals(40.0, toa_deg)

        numberXRayLayers = simulationOptions.getNumberXRayLayers()
        self.assertEquals(500, numberXRayLayers)

        resultSimulationData = file.getResultsSimulation(0)
        regionOptions = resultSimulationData.getRegionOptions()
        region = regionOptions.getRegion(0)
        element = region.getElement(0)
        intensities = element.getTotalXrayIntensities()

        self.assertAlmostEquals(2164.75, intensities[LINE_K][GENERATED], 2)
        self.assertAlmostEquals(415.81, intensities[LINE_K][EMITTED], 2)

        atomicNumber = element.getAtomicNumber()
        self.assertEquals(5, atomicNumber)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
