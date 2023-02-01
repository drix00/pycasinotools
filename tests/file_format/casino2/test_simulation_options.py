#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_simulation_options
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.simulation_options` module.
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
from io import BytesIO

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino2.simulation_options import SimulationOptions
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):  # pragma: no cover
        pytest.skip()
    with open(filepath_sim_2_45, 'rb') as file:
        _read_tests(file)


def test_read_string_io(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):  # pragma: no cover
        pytest.skip()
    f = open(filepath_sim_2_45, 'rb')
    file = BytesIO(f.read())
    f.close()
    _read_tests(file)


def _read_tests(file):
    file.seek(0)
    simulation_options = SimulationOptions()
    simulation_options.read(file, 26)

    assert simulation_options._bseCoefficient == pytest.approx(0.0)

    assert simulation_options.Beam_Diameter == pytest.approx(10.0)
    assert simulation_options.Electron_Number == 10000

    assert simulation_options.UseEnBack is False
    assert simulation_options.WorkDist == pytest.approx(10.0)
    assert simulation_options.DetectScaleX == pytest.approx(1.0)
    assert simulation_options.DetectScaleY == pytest.approx(1.0)

    assert simulation_options.FEmissionRX == 1
    assert simulation_options.NbreCoucheRX == 500
    assert simulation_options.EpaisCouche == pytest.approx(10.0)
    assert simulation_options.TOA == pytest.approx(40.0)
    assert simulation_options.PhieRX == pytest.approx(0.0)
    assert simulation_options.RkoMax == pytest.approx(0.0)
    assert simulation_options.RkoMaxW == pytest.approx(0.0)

    assert simulation_options.Eminimum == pytest.approx(0.050)
    assert simulation_options.Electron_Display == 200
    assert simulation_options.Electron_Save == 5
    assert simulation_options.Memory_Keep == 2
    assert simulation_options.First == 0
    assert simulation_options.Keep_Sim == 1

    assert simulation_options.Display_Colision == 0
    assert simulation_options.Display_Color == 0
    assert simulation_options.Display_Projection == 0
    assert simulation_options.Display_Back == 1
    assert simulation_options.Display_Refresh == 1
    assert simulation_options.Minimum_Trajectory_Display_Distance == pytest.approx(0.60)

    assert simulation_options.FForme == 0
    assert simulation_options.Total_Thickness / 1.0e10 == pytest.approx(1.0)
    assert simulation_options.Half_Width / 1.0e10 == pytest.approx(1.0)

    assert simulation_options.ShowFadedSqr == 1
    assert simulation_options.ShowRegions == 1
    assert simulation_options.SetPointstoRelativePosition == 1
    assert simulation_options.Summation == 1
    assert simulation_options.XZorXY == 0
    assert simulation_options.Yplane == 0
    assert simulation_options.Zplane == 0

    assert simulation_options.EFilterMax == pytest.approx(30.0)
    assert simulation_options.EFilterMin == pytest.approx(0.0)

    assert simulation_options.RatioX == pytest.approx(1.648000000000E+02)
    assert simulation_options.RatioY == pytest.approx(1.340000000000E+02)
    assert simulation_options.RatioZ == pytest.approx(1.648000000000E+02)
    assert simulation_options.Tot_Ret_En == pytest.approx(0.0)

    assert simulation_options.NumVtabs == 5
    assert simulation_options.NumHtabs == 5


def test_set_line_scan_parameters(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):  # pragma: no cover
        pytest.skip()
    f = open(filepath_sim_2_45, 'rb')
    f.seek(0)
    simulation_options = SimulationOptions()
    simulation_options.read(f, 26)
    f.close()

    simulation_options.set_linescan_parameters(0, 100, 10)

    # Values were also verified inside the GUI
    assert simulation_options.Scan_Image == 1
    assert simulation_options._positionStart_nm == pytest.approx(0)
    assert simulation_options._positionEnd_nm == pytest.approx(100)
    assert simulation_options._positionStep_nm == pytest.approx(10)
    assert simulation_options._positionNumberStep == 10


def test_set_position(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):  # pragma: no cover
        pytest.skip()
    f = open(filepath_sim_2_45, 'rb')
    f.seek(0)
    simulation_options = SimulationOptions()
    simulation_options.read(f, 26)
    f.close()

    simulation_options.set_position(50)

    # Values were also verified inside the GUI
    assert simulation_options.Scan_Image == 0
    assert simulation_options._positionStart_nm == pytest.approx(50)
    assert simulation_options._positionEnd_nm == pytest.approx(50)
    assert simulation_options._positionStep_nm == pytest.approx(1.0)
    assert simulation_options._positionNumberStep == 1
