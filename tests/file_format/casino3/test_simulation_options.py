#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_simulation_options
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.simulation_options` module.
"""

###############################################################################
# Copyright 2020 Hendrix Demers
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

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino3.simulation_options import SimulationOptions
from casinotools.file_format.casino3.options_dist import DIST_DEPOS_POSITION_ABSOLUTE, autoFlag
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim, filepath_cas):

    for filepath in [filepath_sim, filepath_cas]:
        if is_bad_file(filepath):
            pytest.skip()
        file = open(filepath, 'rb')
        simulation_options = SimulationOptions()
        error = simulation_options.read(file)

        assert error is None
        assert simulation_options._version == 30107002

        # ADF
        assert simulation_options._options_adf._version == 30107002
        assert simulation_options._options_adf.DQE == pytest.approx(1.0)
        assert simulation_options._options_adf.Enabled == 1
        assert simulation_options._options_adf.keepData == 0
        assert simulation_options._options_adf.MaxAngle == pytest.approx(0.5)
        assert simulation_options._options_adf.MinAngle == pytest.approx(0.2)
        assert simulation_options._options_adf.MaxPoints == 0

        # AdvBackSet
        assert simulation_options._options_adv_back_set._version == 30107002
        assert simulation_options._options_adv_back_set.UseEnBack is False
        assert simulation_options._options_adv_back_set.WorkDist == pytest.approx(10.0)
        assert simulation_options._options_adv_back_set.DetectScaleX == pytest.approx(1.0)
        assert simulation_options._options_adv_back_set.DetectScaleY == pytest.approx(1.0)
        assert simulation_options._options_adv_back_set.ValidMatrix is False

        assert simulation_options._options_adv_back_set.BEMin_Angle == pytest.approx(0.0)
        assert simulation_options._options_adv_back_set.BEMax_Angle == pytest.approx(0.0)
        assert simulation_options._options_adv_back_set.EFilterMax == pytest.approx(0.0)
        assert simulation_options._options_adv_back_set.EFilterMin == pytest.approx(0.0)

        for i in range(101):
            assert simulation_options._options_adv_back_set.EFilterVal[i] == pytest.approx(1.0)

        assert simulation_options._options_adv_back_set.FEFilter == 0

        # Dist
        assert simulation_options.options_dist._version == 30107002
        assert simulation_options.options_dist.DenrMax / autoFlag == pytest.approx(1.0)

        assert simulation_options.options_dist.DEposCyl_Z == pytest.approx(1000.0)
        assert simulation_options.options_dist.DEposCyl_Z_Log == 0
        assert simulation_options.options_dist.DEpos_Position == DIST_DEPOS_POSITION_ABSOLUTE

        # EnergyByPos
        assert simulation_options._options_energy_by_pos._version == 30107002
        assert simulation_options._options_energy_by_pos.diffuse == 0
        assert simulation_options._options_energy_by_pos.depos_summation == 1
        assert simulation_options._options_energy_by_pos.depos_iso_level == pytest.approx(0.1)
        assert simulation_options._options_energy_by_pos.carrier_surface_recombination == pytest.approx(-1.0)
        assert simulation_options._options_energy_by_pos.normalize == 1

        # Micro
        assert simulation_options.options_microscope._version == 30107002
        assert simulation_options.options_microscope.scanning_mode == 0
        assert simulation_options.options_microscope.x_plane_position == pytest.approx(0.0)

        assert simulation_options.options_microscope.scan_point_distribution == pytest.approx(1.0)
        assert simulation_options.options_microscope.keep_simulation_data == 1

        # Physic
        assert simulation_options.options_physic._version == 30107002
        assert simulation_options.options_physic.FRan == 3
        assert simulation_options.options_physic.FDeds == 1
        assert simulation_options.options_physic.FTotalCross == 5
        assert simulation_options.options_physic.FPartialCross == 5
        assert simulation_options.options_physic.FCosDirect == 1
        assert simulation_options.options_physic.FSecIon == 3
        assert simulation_options.options_physic.FPotMoy == 0

        assert simulation_options.options_physic.max_secondary_order == 10
        assert simulation_options.options_physic.Min_Energy_Nosec == pytest.approx(0.05)
        assert simulation_options.options_physic.Residual_Energy_Loss == pytest.approx(0.0004)
        assert simulation_options.options_physic.Min_Energy_With_Sec == pytest.approx(-1)
        assert simulation_options.options_physic.Min_Gen_Secondary_Energy == pytest.approx(-1)

        # Xray
        assert simulation_options._options_xray._version == 30107002
        assert simulation_options._options_xray.toa == pytest.approx(40.0)
        assert simulation_options._options_xray.phi_rx == pytest.approx(0.0)
