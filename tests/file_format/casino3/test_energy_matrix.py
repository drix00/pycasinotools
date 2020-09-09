#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_energy_matrix
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.energy_matrix` module.
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
import os.path

# Third party modules.
import pytest
from pkg_resources import resource_filename

# Local modules.

# Project modules.
from casinotools.file_format.casino3.energy_matrix import EnergyMatrix
from casinotools.file_format.casino3.options_dist import DIST_DEPOS_TYPE_CARTESIAN
from casinotools.file_format.casino3.simulation_options import SimulationOptions
from casinotools.utilities.path import is_bad_file
from casinotools.file_format.casino3.file import File

# Globals and constants variables.


@pytest.fixture()
def file_path_energy_cartesian_cas():
    name = "../../../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cartesian_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cylindrical_cas():
    name = "../../../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cylindrical_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_spherical_cas():
    name = "../../../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_spherical_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_file_path_energy_cartesian_cas(file_path_energy_cartesian_cas):
    assert os.path.isfile(file_path_energy_cartesian_cas)


def test_file_path_energy_cylindrical_cas(file_path_energy_cylindrical_cas):
    assert os.path.isfile(file_path_energy_cylindrical_cas)


def test_file_path_energy_spherical_cas(file_path_energy_spherical_cas):
    assert os.path.isfile(file_path_energy_spherical_cas)


def test_read(filepath_cas):
    options = SimulationOptions()
    options.options_dist.DEpos_Type = DIST_DEPOS_TYPE_CARTESIAN
    results = EnergyMatrix(options, None)
    if is_bad_file(filepath_cas):
        pytest.skip()
    file = open(filepath_cas, 'rb')
    file.seek(4042541)

    error = results.read(file)
    assert error is None
    assert results._number_elements == 125000
    assert results._start_position == 4042541
    assert results._end_position == 4042541 + 125000 * 8


def test_read_cartesian(file_path_energy_cartesian_cas):
    casino_file = File(file_path_energy_cartesian_cas)

    scan_point_results = casino_file.get_scan_point_results()[0]

    assert scan_point_results._isDEnergy_Density is True
    # assert scan_point_results.DEnergy_Density_Max_Energy == 29050.4

    energy_matrix = scan_point_results._DEnergy_Density
    assert energy_matrix._number_elements == 50 * 50 * 50

    data = energy_matrix.get_data()
    assert data[0, 0, 0] == 1.5688423948687005
    assert data[1, 1, 1] == 2.272354614047501
    assert data[24, 24, 24] == 411.4040703345004
    assert data[-2, -2, -2] == 0.0
    assert data[-1, -1, -1] == 0.0


def test_read_cylindrical(file_path_energy_cylindrical_cas):
    casino_file = File(file_path_energy_cylindrical_cas)

    scan_point_results = casino_file.get_scan_point_results()[0]

    assert scan_point_results._isDEnergy_Density is True
    # assert scan_point_results.DEnergy_Density_Max_Energy == 29050.4

    energy_matrix = scan_point_results._DEnergy_Density
    assert energy_matrix._number_elements == 50 * 50

    data = energy_matrix.get_data()
    assert data[0, 0] == 32161.668619632866
    assert data[1, 1] == 690.7337287232823
    assert data[24, 24] == 4149.629987349835
    assert data[-2, -2] == 0.0
    assert data[-1, -1] == 0.0


def test_read_spherical(file_path_energy_spherical_cas):
    casino_file = File(file_path_energy_spherical_cas)

    scan_point_results = casino_file.get_scan_point_results()[0]

    assert scan_point_results._isDEnergy_Density is True
    # assert scan_point_results.DEnergy_Density_Max_Energy == 29050.4

    energy_matrix = scan_point_results._DEnergy_Density
    assert energy_matrix._number_elements == 50

    data = energy_matrix.get_data()
    assert data[0] == 1582.2293494223532
    assert data[1] == 10978.987229982285
    assert data[24] == 237544.09574357865
    assert data[-2] == 3339.0087554269408
    assert data[-1] == 3119.0176437913647
