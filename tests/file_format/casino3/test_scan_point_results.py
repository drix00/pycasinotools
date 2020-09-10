#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`module_name` module.
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
from casinotools.file_format.casino3.scan_point_results import ScanPointResults
from casinotools.file_format.casino3.simulation_options import SimulationOptions
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_cas):
    if is_bad_file(filepath_cas):
        pytest.skip()
    file = open(filepath_cas, 'rb')
    options = SimulationOptions()
    options.read(file)
    file.close()
    del file

    results = ScanPointResults()
    file = open(filepath_cas, 'rb')
    # file.seek(12648)
    error = results.read(file, options)

    assert error is None

    assert results._version == 30107002

    assert results._initial_energy_keV == pytest.approx(0.8)
    assert results._rko_max == pytest.approx(0.0)
    assert results._rko_max_w == pytest.approx(24.04826155663)

    assert results._number_simulated_trajectories == 1000000
    assert results._being_processed == 2

    assert results._backscattered_coefficient == pytest.approx(5.468900000000E-02)
    assert results._backscattered_detected_coefficient == pytest.approx(0.0)
    assert results._secondary_coefficient == pytest.approx(0.0)
    assert results._transmitted_coefficient == pytest.approx(0.0)
    assert results._transmitted_detected_coefficient == pytest.approx(0.0)
    assert results._number_backscattered_electrons == 54689
    assert results._number_backscattered_electrons_detected == pytest.approx(0.0)
    assert results._number_secondary_electrons == 0

    assert results._number_results == 8

    for i in range(1, 8 + 1):
        assert results._region_intensity_infos[i - 1]._region_id == i

    # DZMax distribution results.
    assert results._is_dz_max is True
    assert results.dz_max._version == 30105020

    assert results.dz_max._size == 1000
    assert results.dz_max._borneInf == pytest.approx(0.0)
    assert results.dz_max._borneSup == pytest.approx(8.900000000000E+01)
    assert results.dz_max._isLog == 0
    assert results.dz_max._isUneven == 0

    assert results.dz_max._title == "Z Max"
    assert results.dz_max._xTitle == "Depth (nm)"
    assert results.dz_max._yTitle == "Hits (Normalized)"

    values = results.dz_max.get_values()
    assert values[0] == pytest.approx(1.0)
    assert values[-1] == pytest.approx(0.0)

    assert results.is_deposited_energy is True
    assert results.DEnergy_Density_Max_Energy == pytest.approx(1.518294795870E-01)

    assert results.get_number_saved_trajectories() == 199
