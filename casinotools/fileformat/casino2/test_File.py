#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.test_File

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.fileformat.casino2.File`.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import unittest
import os
try:
    from io import BytesIO
except ImportError:  # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.
from pkg_resources import resource_filename  # @UnresolvedImport
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.File as File
import casinotools.fileformat.casino2.Version as Version
from casinotools.fileformat.casino2.Element import LINE_K, GENERATED, EMITTED
from casinotools.utilities.path import is_bad_file
from casinotools.fileformat.casino2.Version import VERSION_2_45, VERSION_2_50, VERSION_2_51, VERSION_2_42, VERSION_2_46

# Globals and constants variables.


class TestFile(unittest.TestCase):
    """
    TestCase class for the module `casinotools.fileformat.casino2.File`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.filepathSim = resource_filename(__name__, "../../../test_data/wincasino2.45/id475_v2.46.sim")
        self.filepathCas = resource_filename(__name__, "../../../test_data/wincasino2.45/id475_v2.46.cas")
        self.version_2_45 = VERSION_2_45

        self.filepathStd = resource_filename(__name__, "../../../test_data/casino2.x/std_B_04.0keV_40.0TOA_v2.42.sim")
        self.filepathWrite = resource_filename(__name__, "../../../test_data/casino2.x/stdTest.sim")

        self.filepathSim_v242 = resource_filename(__name__, "../../../test_data/casino2.x/std_B_3keV_v2.42.sim")
        self.filepathCas_v242 = resource_filename(__name__, "../../../test_data/casino2.x/std_B_3keV_v2.42.cas")

        self.filepathCas_nicr = resource_filename(__name__, "../../../test_data/casino2.x/nicr_v2.46.cas")

        self.filepath_sim_v250 = resource_filename(__name__, "../../../test_data/casino2.x/Al_E2kV_10ke_v2.50.sim")
        self.filepath_cas_v250 = resource_filename(__name__, "../../../test_data/casino2.x/Al_E2kV_10ke_v2.50.cas")
        self.version_2_50 = VERSION_2_50

        self.filepath_sim_v251 = resource_filename(__name__, "../../../test_data/casino2.x/Al_E2kV_10ke_v2.51.sim")
        self.filepath_cas_v251 = resource_filename(__name__, "../../../test_data/casino2.x/Al_E2kV_10ke_v2.51.cas")
        self.version_2_51 = VERSION_2_51

        self.filepath_problem_sim_v250 = resource_filename(__name__, "../../../test_data/casino2.x/VerticalLayers3_v2.50.sim")
        self.filepath_problem_pymontecarlo_sim_v250 = resource_filename(__name__, "../../../test_data/casino2.x/VerticalLayers3_pymontecarlo_v2.50.sim")
        self.filepath_good_sim_v251 = resource_filename(__name__, "../../../test_data/casino2.x/VerticalLayers3_good_v2.51.sim")

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

        if os.path.isfile(self.filepathWrite):
            os.remove(self.filepathWrite)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")
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

        # self.fail("Test if the testcase is working.")

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

        # self.fail("Test if the testcase is working.")

    def test_write(self):
        if is_bad_file(self.filepathStd):
            raise SkipTest

        file = File.File()
        option_simulation_data = self._getOptionSimulationData()
        file.setOptionSimulationData(option_simulation_data)
        file.write(self.filepathWrite)

        with open(self.filepathStd, 'rb') as fp:
            data_ref = fp.read()
        with open(self.filepathWrite, 'rb') as fp:
            data = fp.read()
        index = 0
        for charRef, char in zip(data_ref, data):
            self.assertEqual(charRef, char, index)
            index += 1

        self.assertEqual(len(data_ref), len(data))

        import filecmp
        self.assertTrue(filecmp.cmp(self.filepathStd, self.filepathWrite, shallow=True))

        # self.fail("Test if the testcase is working.")

    def _getOptionSimulationData(self):
        file = File.File()
        file.readFromFilepath(self.filepathStd)

        return file.getOptionSimulationData()

    def test_skipReadingData(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest

        file = File.File()
        file.readFromFilepath(self.filepathCas, isSkipReadingData=False)

        trajectories_data = file.getResultsFirstSimulation().getTrajectoriesData()
        self.assertEqual(221, trajectories_data._numberTrajectories)
        self.assertEqual(89, trajectories_data._trajectories[0].NbElec)
        self.assertEqual(89, len(trajectories_data._trajectories[0]._scatteringEvents))

        event = trajectories_data._trajectories[0]._scatteringEvents[0]
        self.assertAlmostEqual(-2.903983831406E+00, event.X)
        self.assertAlmostEqual(-3.020418643951E+00, event.Y)
        self.assertAlmostEqual(0.0, event.Z)
        self.assertAlmostEqual(4.000000000000E+00, event.E)
        self.assertEqual(0, event.Intersect)
        self.assertEqual(0, event.id)

        file = File.File()
        file.readFromFilepath(self.filepathCas, isSkipReadingData=True)

        trajectories_data = file.getResultsFirstSimulation().getTrajectoriesData()
        self.assertEqual(221, trajectories_data._numberTrajectories)
        self.assertEqual(89, trajectories_data._trajectories[0].NbElec)
        self.assertEqual(0, len(trajectories_data._trajectories[0]._scatteringEvents))

        simulation_results = file.getResultsFirstSimulation().getSimulationResults()

        self.assertEqual(1, simulation_results.BE_Intensity_Size)
        self.assertEqual(3.950000000000E-02, simulation_results.BE_Intensity[0])

        element = simulation_results._elementIntensityList[0]
        self.assertEqual("B", element.Name)
        self.assertAlmostEqual(3.444919288026E+02, element.IntensityK[0])

        element = simulation_results._elementIntensityList[1]
        self.assertEqual("C", element.Name)
        self.assertAlmostEqual(4.687551040349E+01, element.IntensityK[0])

        self.assertEqual(1000, simulation_results.NbPointDZMax)
        self.assertEqual(500, simulation_results.NbPointDENR)
        self.assertEqual(500, simulation_results.NbPointDENT)
        self.assertEqual(500, simulation_results.NbPointDRSR)
        # self.assertEqual(0, simulationResults.NbPointDNCR)
        self.assertEqual(50, simulation_results.NbPointDEpos_X)
        self.assertEqual(50, simulation_results.NbPointDEpos_Y)
        self.assertEqual(50, simulation_results.NbPointDEpos_Z)
        self.assertAlmostEqual(1.608165461510E-02, simulation_results.DEpos_maxE)
        self.assertEqual(91, simulation_results.NbPointDBANG)
        self.assertEqual(91, simulation_results.NbPointDAngleVSEnergie)

        # self.fail("Test if the testcase is working.")

    def test_read_v242(self):
        if is_bad_file(self.filepathSim_v242):
            raise SkipTest
        if is_bad_file(self.filepathCas_v242):
            raise SkipTest

        # .sim
        file = File.File()
        file.readFromFilepath(self.filepathSim_v242)
        self.assertEqual(self.filepathSim_v242, file._filepath)
        self.assertEqual(0, file._numberSimulations)

        option_simulation_data = file.getOptionSimulationData()
        version = option_simulation_data.getVersion()
        self.assertEqual(Version.VERSION_2_42, version)

        simulation_options = option_simulation_data.getSimulationOptions()

        number_electrons = simulation_options.getNumberElectrons()
        self.assertEqual(10000, number_electrons)

        incident_energy_keV = simulation_options.getIncidentEnergy_keV()
        self.assertAlmostEqual(3.0, incident_energy_keV)

        toa_deg = simulation_options.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        number_xray_layers = simulation_options.getNumberXRayLayers()
        self.assertEqual(500, number_xray_layers)

        # .cas
        file = File.File()
        file.readFromFilepath(self.filepathCas_v242)
        self.assertEqual(self.filepathCas_v242, file._filepath)
        self.assertEqual(1, file._numberSimulations)

        self.assertEqual(1, len(file._resultSimulationDataList))

        option_simulation_data = file.getOptionSimulationData()
        version = option_simulation_data.getVersion()
        self.assertEqual(Version.VERSION_2_42, version)

        simulation_options = option_simulation_data.getSimulationOptions()

        number_electrons = simulation_options.getNumberElectrons()
        self.assertEqual(10000, number_electrons)

        incident_energy_keV = simulation_options.getIncidentEnergy_keV()
        self.assertAlmostEqual(3.0, incident_energy_keV)

        toa_deg = simulation_options.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        number_xray_layers = simulation_options.getNumberXRayLayers()
        self.assertEqual(500, number_xray_layers)

        result_simulation_data = file.getResultsSimulation(0)
        region_options = result_simulation_data.getRegionOptions()
        region = region_options.getRegion(0)
        element = region.getElement(0)
        intensities = element.getTotalXrayIntensities()

        self.assertAlmostEqual(2164.75, intensities[LINE_K][GENERATED], 2)
        self.assertAlmostEqual(415.81, intensities[LINE_K][EMITTED], 2)

        atomic_number = element.getAtomicNumber()
        self.assertEqual(5, atomic_number)

        # self.fail("Test if the testcase is working.")

    def test_read_sim_v250(self):
        if is_bad_file(self.filepath_sim_v250):
            raise SkipTest

        # .sim
        file = File.File()
        file.readFromFilepath(self.filepath_sim_v250)
        self.assertEqual(self.filepath_sim_v250, file._filepath)
        self.assertEqual(0, file._numberSimulations)

        option_simulation_data = file.getOptionSimulationData()
        version = option_simulation_data.getVersion()
        self.assertEqual(Version.VERSION_2_50, version)

        simulation_options = option_simulation_data.getSimulationOptions()

        number_electrons = simulation_options.getNumberElectrons()
        self.assertEqual(10000, number_electrons)

        incident_energy_keV = simulation_options.getIncidentEnergy_keV()
        self.assertAlmostEqual(2.0, incident_energy_keV)

        toa_deg = simulation_options.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        number_xray_layers = simulation_options.getNumberXRayLayers()
        self.assertEqual(500, number_xray_layers)

        # self.fail("Test if the testcase is working.")

    def test_read_cas_v250(self):
        if is_bad_file(self.filepath_cas_v250):
            raise SkipTest

        # .cas
        file = File.File()
        file.readFromFilepath(self.filepath_cas_v250)
        self.assertEqual(self.filepath_cas_v250, file._filepath)
        self.assertEqual(1, file._numberSimulations)

        self.assertEqual(1, len(file._resultSimulationDataList))

        option_simulation_data = file.getOptionSimulationData()
        version = option_simulation_data.getVersion()
        self.assertEqual(Version.VERSION_2_50, version)

        simulation_options = option_simulation_data.getSimulationOptions()

        number_electrons = simulation_options.getNumberElectrons()
        self.assertEqual(10000, number_electrons)

        incident_energy_keV = simulation_options.getIncidentEnergy_keV()
        self.assertAlmostEqual(2.0, incident_energy_keV)

        toa_deg = simulation_options.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        number_xray_layers = simulation_options.getNumberXRayLayers()
        self.assertEqual(500, number_xray_layers)

        result_simulation_data = file.getResultsSimulation(0)
        region_options = result_simulation_data.getRegionOptions()
        region = region_options.getRegion(0)
        element = region.getElement(0)
        intensities = element.getTotalXrayIntensities()

        self.assertAlmostEqual(20.99961280822754, intensities[LINE_K][GENERATED], 7)
        self.assertAlmostEqual(20.968143463134766, intensities[LINE_K][EMITTED], 7)

        atomic_number = element.getAtomicNumber()
        self.assertEqual(13, atomic_number)

        # self.fail("Test if the testcase is working.")


    def test_problem_sim_v250(self):
        if is_bad_file(self.filepath_problem_sim_v250):
            raise SkipTest

        # .sim
        file = File.File()
        file.readFromFilepath(self.filepath_problem_sim_v250)
        self.assertEqual(self.filepath_problem_sim_v250, file._filepath)
        self.assertEqual(0, file._numberSimulations)

        option_simulation_data = file.getOptionSimulationData()
        version = option_simulation_data.getVersion()
        self.assertEqual(Version.VERSION_2_50, version)

        simulation_options = option_simulation_data.getSimulationOptions()

        number_electrons = simulation_options.getNumberElectrons()
        self.assertEqual(200, number_electrons)

        incident_energy_keV = simulation_options.getIncidentEnergy_keV()
        self.assertAlmostEqual(1.0, incident_energy_keV)

        toa_deg = simulation_options.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        number_xray_layers = simulation_options.getNumberXRayLayers()
        self.assertEqual(500, number_xray_layers)

        if is_bad_file(self.filepath_good_sim_v251):
            raise SkipTest

        # .sim
        file = File.File()
        file.readFromFilepath(self.filepath_good_sim_v251)
        self.assertEqual(self.filepath_good_sim_v251, file._filepath)
        self.assertEqual(0, file._numberSimulations)

        option_simulation_data = file.getOptionSimulationData()
        version = option_simulation_data.getVersion()
        self.assertEqual(Version.VERSION_2_51, version)

        simulation_options = option_simulation_data.getSimulationOptions()

        number_electrons = simulation_options.getNumberElectrons()
        self.assertEqual(200, number_electrons)

        incident_energy_keV = simulation_options.getIncidentEnergy_keV()
        self.assertAlmostEqual(1.0, incident_energy_keV)

        toa_deg = simulation_options.getTOA_deg()
        self.assertAlmostEqual(40.0, toa_deg)

        number_xray_layers = simulation_options.getNumberXRayLayers()
        self.assertEqual(500, number_xray_layers)

        # self.fail("Test if the testcase is working.")

    def test_extract_version(self):
        """
        Test extract_version method.
        """
        if is_bad_file(self.filepathSim):
            raise SkipTest

        file_paths = []
        file_paths.append((self.filepathSim, VERSION_2_45))
        file_paths.append((self.filepathCas, VERSION_2_45))
        file_paths.append((self.filepathStd, VERSION_2_50))
        file_paths.append((self.filepathSim_v242, VERSION_2_42))
        file_paths.append((self.filepathCas_v242, VERSION_2_42))
        file_paths.append((self.filepathCas_nicr, VERSION_2_46))
        file_paths.append((self.filepath_sim_v250, VERSION_2_50))
        file_paths.append((self.filepath_cas_v250, VERSION_2_50))
        file_paths.append((self.filepath_problem_sim_v250, VERSION_2_50))
        file_paths.append((self.filepath_problem_pymontecarlo_sim_v250, VERSION_2_50))
        file_paths.append((self.filepath_good_sim_v251, VERSION_2_51))

        for file_path, version_ref in file_paths:
            casino_file = File.File()
            version = casino_file.extract_version(file_path)
            self.assertEqual(version_ref, version, msg=file_path)

        # self.fail("Test if the testcase is working.")

if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()
