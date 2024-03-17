#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_simulation_results
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.simulation_results` module.
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
from casinotools.file_format.casino2.simulation_results import SimulationResults
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


def test_read(filepath_cas_26):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()
    with open(filepath_cas_26, 'rb') as file:
        _read_tests(file)


def test_read_string_io(filepath_cas_26):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()
    f = open(filepath_cas_26, 'rb')
    file = BytesIO(f.read())
    f.close()
    _read_tests(file)


def _read_tests(file):
    version = 26
    options = SimulationOptions()
    options.read(file, version)
    file.seek(696824)
    simulation_results = SimulationResults()
    simulation_results.read(file, options, version)

    assert simulation_results.BE_Intensity_Size == 1
    assert simulation_results.BE_Intensity[0] == 3.950000000000E-02

    element = simulation_results.element_intensity_list[0]
    assert element.name == "B"
    assert element.IntensityK[0] == pytest.approx(3.444919288026E+02)

    element = simulation_results.element_intensity_list[1]
    assert element.name == "C"
    assert element.IntensityK[0] == pytest.approx(4.687551040349E+01)

    assert simulation_results.NbPointDZMax == 1000
    assert simulation_results.NbPointDENR == 500
    assert simulation_results.NbPointDENT == 500
    assert simulation_results.NbPointDRSR == 500
    # assert simulation_results.NbPointDNCR == 0
    assert simulation_results.NbPointDEpos_X == 50
    assert simulation_results.NbPointDEpos_Y == 50
    assert simulation_results.NbPointDEpos_Z == 50
    assert simulation_results.DEpos_maxE == pytest.approx(1.608165461510E-02)
    assert simulation_results.NbPointDBANG == 91
    assert simulation_results.NbPointDAngleVSEnergie == 91
