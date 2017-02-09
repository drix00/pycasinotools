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
import os
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.File as File
import casinotools.fileformat.casino2.Version as Version
from casinotools.fileformat.casino2.Element import LINE_K, GENERATED, EMITTED
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = resource_filename(__name__, "../../../test_data/wincasino2.45/id475.sim")
        self.filepathCas = resource_filename(__name__, "../../../test_data/wincasino2.45/id475.cas")

        self.filepathStd = resource_filename(__name__, "../../../test_data/casino2.x/std_B_04.0keV_40.0TOA.sim")
        self.filepathWrite = resource_filename(__name__, "../../../test_data/casino2.x/stdTest.sim")

        self.filepathSim_v242 = resource_filename(__name__, "../../../test_data/casino2.x/std_B_3keV_v2.42_23.sim")
        self.filepathCas_v242 = resource_filename(__name__, "../../../test_data/casino2.x/std_B_3keV_v2.42_23.cas")

        self.filepathCas_nicr = resource_filename(__name__, "../../../test_data/casino2.x/nicr.cas")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        if os.path.isfile(self.filepathWrite):
            os.remove(self.filepathWrite)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        file = File.File()
        file.readFromFilepath(self.filepathSim)
        self.assertEqual(self.filepathSim, file._filepath)
        self.assertEqual(0, file._numberSimulations)

        file = File.File()
        file.readFromFilepath(self.filepathCas)
        self.assertEqual(self.filepathCas, file._filepath)
        self.assertEqual(1, file._numberSimulations)

        self.assertEqual(1, len(file._resultSimulationDataList))

        #self.fail("Test if the testcase is working.")

    def test_read_StringIO(self):
        # sim
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        buf = BytesIO(f.read())
        buf.mode = 'rb'
        f.close()

        file = File.File()
        file.readFromFileObject(buf)
        self.assertEqual(0, file._numberSimulations)

        # cas
        f = open(self.filepathCas, 'rb')
        buf = BytesIO(f.read())
        buf.mode = 'rb'
        f.close()

        file = File.File()
        file.readFromFileObject(buf)
        self.assertEqual(1, file._numberSimulations)

        self.assertEqual(1, len(file._resultSimulationDataList))

    def test_isSimulationFilepath(self):
        file = File.File()

        self.assertTrue(file._isSimulationFilepath(self.filepathSim))
        self.assertFalse(file._isSimulationFilepath(self.filepathCas))

        #self.fail("Test if the testcase is working.")

    def test_write(self):
        if is_bad_file(self.filepathStd):
            raise SkipTest

        file = File.File()
        optionSimulationData = self._getOptionSimulationData()
        file.setOptionSimulationData(optionSimulationData)
        file.write(self.filepathWrite)

        with open(self.filepathStd, 'rb') as fp:
            dataRef = fp.read()
        with open(self.filepathWrite, 'rb') as fp:
            data = fp.read()
        index = 0
        for charRef, char in zip(dataRef, data):
            self.assertEqual(charRef, char, index)
            index += 1

        self.assertEqual(len(dataRef), len(data))

        import filecmp
        self.assertTrue(filecmp.cmp(self.filepathStd, self.filepathWrite, shallow=True))

        #self.fail("Test if the testcase is working.")

    def _getOptionSimulationData(self):
        file = File.File()
        file.readFromFilepath(self.filepathStd)

        return file.getOptionSimulationData()

    def test_skipReadingData(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest

        file = File.File()
        file.readFromFilepath(self.filepathCas, isSkipReadingData=False)

        trajectoriesData = file.getResultsFirstSimulation().getTrajectoriesData()
        self.assertEqual(221, trajectoriesData._numberTrajectories)
        self.assertEqual(89, trajectoriesData._trajectories[0].NbElec)
        self.assertEqual(89, len(trajectoriesData._trajectories[0]._scatteringEvents))

        event = trajectoriesData._trajectories[0]._scatteringEvents[0]
        self.assertAlmostEqual(-2.903983831406E+00, event.X)
        self.assertAlmostEqual(-3.020418643951E+00, event.Y)
        self.assertAlmostEqual(0.0, event.Z)
        self.assertAlmostEqual(4.000000000000E+00, event.E)
        self.assertEqual(0, event.Intersect)
        self.assertEqual(0, event.id)

        file = File.File()
        file.readFromFilepath(self.filepathCas, isSkipReadingData=True)

        trajectoriesData = file.getResultsFirstSimulation().getTrajectoriesData()
        self.assertEqual(221, trajectoriesData._numberTrajectories)
        self.assertEqual(89, trajectoriesData._trajectories[0].NbElec)
        self.assertEqual(0, len(trajectoriesData._trajectories[0]._scatteringEvents))

        simulationResults = file.getResultsFirstSimulation().getSimulationResults()

        self.assertEqual(1, simulationResults.BE_Intensity_Size)
        self.assertEqual(3.950000000000E-02, simulationResults.BE_Intensity[0])

        element = simulationResults._elementIntensityList[0]
        self.assertEqual("B", element.Name)
        self.assertAlmostEqual(3.444919288026E+02, element.IntensityK[0])

        element = simulationResults._elementIntensityList[1]
        self.assertEqual("C", element.Name)
        self.assertAlmostEqual(4.687551040349E+01, element.IntensityK[0])

        self.assertEqual(1000, simulationResults.NbPointDZMax)
        self.assertEqual(500, simulationResults.NbPointDENR)
        self.assertEqual(500, simulationResults.NbPointDENT)
        self.assertEqual(500, simulationResults.NbPointDRSR)
        #self.assertEqual(0, simulationResults.NbPointDNCR)
        self.assertEqual(50, simulationResults.NbPointDEpos_X)
        self.assertEqual(50, simulationResults.NbPointDEpos_Y)
        self.assertEqual(50, simulationResults.NbPointDEpos_Z)
        self.assertAlmostEqual(1.608165461510E-02, simulationResults.DEpos_maxE)
        self.assertEqual(91, simulationResults.NbPointDBANG)
        self.assertEqual(91, simulationResults.NbPointDAngleVSEnergie)

        #self.fail("Test if the testcase is working.")

    def test_readv242(self):
        if is_bad_file(self.filepathSim_v242):
            raise SkipTest
        if is_bad_file(self.filepathCas_v242):
            raise SkipTest

        # .sim
        file = File.File()
        file.readFromFilepath(self.filepathSim_v242)
        self.assertEqual(self.filepathSim_v242, file._filepath)
        self.assertEqual(0, file._numberSimulations)

        optionSimulationData = file.getOptionSimulationData()
        version = optionSimulationData.getVersion()
        self.assertEqual(Version.VERSION_2_42, version)

        simulationOptions = optionSimulationData.getSimulationOptions()

        numberElectrons = simulationOptions.getNumberElectrons()
        self.assertEqual(10000, numberElectrons)

        incidentEnergy_keV = simulationOptions.getIncidentEnergy_keV()
        self.assertAlmostEqual(3.0, incidentEnergy_keV)

        toa_deg = simulationOptions.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        numberXRayLayers = simulationOptions.getNumberXRayLayers()
        self.assertEqual(500, numberXRayLayers)

        # .cas
        file = File.File()
        file.readFromFilepath(self.filepathCas_v242)
        self.assertEqual(self.filepathCas_v242, file._filepath)
        self.assertEqual(1, file._numberSimulations)

        self.assertEqual(1, len(file._resultSimulationDataList))

        optionSimulationData = file.getOptionSimulationData()
        version = optionSimulationData.getVersion()
        self.assertEqual(Version.VERSION_2_42, version)

        simulationOptions = optionSimulationData.getSimulationOptions()

        numberElectrons = simulationOptions.getNumberElectrons()
        self.assertEqual(10000, numberElectrons)

        incidentEnergy_keV = simulationOptions.getIncidentEnergy_keV()
        self.assertAlmostEqual(3.0, incidentEnergy_keV)

        toa_deg = simulationOptions.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        numberXRayLayers = simulationOptions.getNumberXRayLayers()
        self.assertEqual(500, numberXRayLayers)

        resultSimulationData = file.getResultsSimulation(0)
        regionOptions = resultSimulationData.getRegionOptions()
        region = regionOptions.getRegion(0)
        element = region.getElement(0)
        intensities = element.getTotalXrayIntensities()

        self.assertAlmostEqual(2164.75, intensities[LINE_K][GENERATED], 2)
        self.assertAlmostEqual(415.81, intensities[LINE_K][EMITTED], 2)

        atomicNumber = element.getAtomicNumber()
        self.assertEqual(5, atomicNumber)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
