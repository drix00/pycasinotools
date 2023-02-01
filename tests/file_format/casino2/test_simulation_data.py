#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_simulation_data

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.file_format.casino2.simulation_data`.
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
from io import BytesIO

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino2.simulation_data import SimulationData
from casinotools.utilities.path import is_bad_file
from casinotools.file_format.casino2.element import EMITTED, GENERATED, LINE_K, LINE_L, LINE_M
from casinotools.file_format.casino2.line import ATOM_LINE_KA1, ATOM_LINE_KA2, ATOM_LINE_KB1

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
    file.seek(0)
    simulation_data = SimulationData()
    simulation_data.read(file)

    assert simulation_data._header == "WinCasino Simulation File"
    assert simulation_data._version == 26
    assert simulation_data._status == 'f'
    assert simulation_data._save_simulations == 1
    assert simulation_data._save_regions == 1
    assert simulation_data._save_trajectories == 1
    assert simulation_data._save_distributions == 1


def test_get_total_xray_intensities(filepath_cas_26, filepath_cas_nicr):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()

    # Single region
    f = open(filepath_cas_26, 'rb')
    f.seek(98348)
    simulation_data = SimulationData()
    simulation_data.read(f)
    f.close()

    intensities = simulation_data.get_total_xray_intensities()

    assert intensities[5][LINE_K][GENERATED] == pytest.approx(2538.63)
    assert intensities[5][LINE_K][EMITTED] == pytest.approx(344.49, 2)

    assert intensities[6][LINE_K][GENERATED] == pytest.approx(111.30, 2)
    assert intensities[6][LINE_K][EMITTED] == pytest.approx(46.88, 2)

    # Multiple regions
    if is_bad_file(filepath_cas_nicr):  # pragma: no cover
        pytest.skip()

    f = open(filepath_cas_nicr, 'rb')
    f.seek(98348)
    simulation_data = SimulationData()
    simulation_data.read(f)
    f.close()

    intensities = simulation_data.get_total_xray_intensities()

    assert intensities[79][LINE_M][GENERATED] == pytest.approx(0.76, 2)
    assert intensities[79][LINE_M][EMITTED] == pytest.approx(0.52, 2)

    assert intensities[24][LINE_K][GENERATED] == pytest.approx(293.88)
    assert intensities[24][LINE_K][EMITTED] == pytest.approx(290.78, 2)
    assert intensities[24][LINE_L][GENERATED] == pytest.approx(712.32, 2)
    assert intensities[24][LINE_L][EMITTED] == pytest.approx(430.56, 2)

    assert intensities[28][LINE_K][GENERATED] == pytest.approx(6.62, 2)
    assert intensities[28][LINE_K][EMITTED] == pytest.approx(6.53, 2)
    assert intensities[28][LINE_L][GENERATED] == pytest.approx(1115.51, 2)
    assert intensities[28][LINE_L][EMITTED] == pytest.approx(457.79, 2)

    assert intensities[14][LINE_K][GENERATED] == pytest.approx(1.57, 2)
    assert intensities[14][LINE_K][EMITTED] == pytest.approx(1.22, 2)


def test_get_total_xray_intensities_1_esr(filepath_cas_26):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()

    with open(filepath_cas_26, 'rb') as file:
        # Single region
        file.seek(50193)
        simulation_data = SimulationData()
        simulation_data.read(file)
        file.close()

        intensities_ref = {5: {}, 6: {}}
        # intensities_ref[5][ATOM_LINE_KA1] = 9.269059346795805e-07
        # intensities_ref[5][ATOM_LINE_KA2] = 4.662984097246555e-07
        # intensities_ref[5][ATOM_LINE_KB1] = 1.355707793206891e-08
        # intensities_ref[6][ATOM_LINE_KA1] = 9.269059346795805e-07
        # intensities_ref[6][ATOM_LINE_KA2] = 4.662984097246555e-07
        # intensities_ref[6][ATOM_LINE_KB1] = 1.355707793206891e-08

        intensities = simulation_data.get_total_xray_intensities_1_esr()

        assert len(intensities) == len(intensities_ref)
        assert len(intensities[5]) == len(intensities_ref[5])

        for atomic_line in intensities[5]:
            value_ref = intensities_ref[5][atomic_line]*1.0e6
            value = intensities[5][atomic_line]*1.0e6
            assert value == pytest.approx(value_ref)
