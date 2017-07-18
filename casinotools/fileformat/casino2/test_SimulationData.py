#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.test_SimulationData

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.fileformat.casino2.SimulationData`.
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
from casinotools.fileformat.casino2.line import ATOMLINE_KA1, ATOMLINE_KA2, ATOMLINE_KB1, ATOMLINE_KB2, ATOMLINE_LA, \
    ATOMLINE_LB1, ATOMLINE_LB2, ATOMLINE_LG, ATOMLINE_MA


class TestSimulationData(test_File.TestFile):
    """
    TestCase class for the module `casinotools.fileformat.casino2.SimulationData`.
    """

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file)

        # self.fail("Test if the testcase is working.")

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
        simulation_data = SimulationData.SimulationData()
        simulation_data.read(file)

        self.assertEqual("WinCasino Simulation File", simulation_data._header)
        self.assertEqual(26, simulation_data._version)
        self.assertEqual('n', simulation_data._status)
        self.assertEqual(True, simulation_data._save_simulations)
        self.assertEqual(True, simulation_data._save_regions)
        self.assertEqual(False, simulation_data._save_trajectories)
        self.assertEqual(False, simulation_data._save_distributions)

    def testGetTotalXrayIntensities(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        # Single region
        f = open(self.filepathCas, 'rb')
        f.seek(98348)
        simulation_data = SimulationData.SimulationData()
        simulation_data.read(f)
        f.close()

        intensities = simulation_data.getTotalXrayIntensities()

        self.assertAlmostEqual(2538.63, intensities[5][LINE_K][GENERATED], 2)
        self.assertAlmostEqual(344.49, intensities[5][LINE_K][EMITTED], 2)

        self.assertAlmostEqual(111.30, intensities[6][LINE_K][GENERATED], 2)
        self.assertAlmostEqual(46.88, intensities[6][LINE_K][EMITTED], 2)

        # Multiple regions
        if is_bad_file(self.filepathCas_nicr):
            raise SkipTest
        f = open(self.filepathCas_nicr, 'rb')
        f.seek(98348)
        simulation_data = SimulationData.SimulationData()
        simulation_data.read(f)
        f.close()

        intensities = simulation_data.getTotalXrayIntensities()

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

    def test_get_total_xray_intensities_1_esr(self):
        if is_bad_file(self.filepath_cas_v251):
            raise SkipTest
        with open(self.filepath_cas_v251, 'rb') as file:
            # Single region
            file.seek(50193)
            simulation_data = SimulationData.SimulationData()
            simulation_data.read(file)
            file.close()

            intensities_ref = {}
            intensities_ref[13] = {}
            intensities_ref[13][ATOMLINE_KA1] = 9.269059346795805e-07
            intensities_ref[13][ATOMLINE_KA2] = 4.662984097246555e-07
            intensities_ref[13][ATOMLINE_KB1] = 1.355707793206891e-08

            intensities = simulation_data.get_total_xray_intensities_1_esr()

            self.assertEqual(len(intensities_ref), len(intensities))
            self.assertEqual(len(intensities_ref[13]), len(intensities[13]))

            for atomic_line in intensities[13]:
                with self.subTest(atomic_line=atomic_line):
                    self.assertAlmostEqual(intensities_ref[13][atomic_line]*1.0e6, intensities[13][atomic_line]*1.0e6)

        # self.fail("Test if the testcase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()
