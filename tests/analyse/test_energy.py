#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.analyse.test_energy
.. moduleauthor:: Hendrix Demers <Demers.Hendrix@hydro.qc.ca>

Tests for the :py:mod:`casinotools.analyse.energy` module.
"""


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

# Standard library modules.

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.analyse.energy import get_file_type, FileType, read_energy_data

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_get_file_type_cas(file_path_energy_cartesian_cas, file_path_energy_cylindrical_cas,
                           file_path_energy_spherical_cas):
    assert get_file_type(file_path_energy_cartesian_cas) == FileType.CAS
    assert get_file_type(file_path_energy_cylindrical_cas) == FileType.CAS
    assert get_file_type(file_path_energy_spherical_cas) == FileType.CAS


def test_get_file_type_dat(file_path_energy_cartesian_dat, file_path_energy_cylindrical_dat,
                           file_path_energy_spherical_dat):
    assert get_file_type(file_path_energy_cartesian_dat) == FileType.DAT
    assert get_file_type(file_path_energy_cylindrical_dat) == FileType.DAT
    assert get_file_type(file_path_energy_spherical_dat) == FileType.DAT


def test_read_cartesian_cas(file_path_energy_cartesian_cas):
    energy_data = read_energy_data(file_path_energy_cartesian_cas)

    assert energy_data.number_elements == 50 * 50 * 50

    compare_xs_nm(energy_data)
    compare_ys_nm(energy_data)
    compare_zs_nm(energy_data)

    assert energy_data.energies_keV[0, 0, 0] == 1.5688423948687005
    assert energy_data.energies_keV[1, 1, 1] == 2.272354614047501
    assert energy_data.energies_keV[24, 24, 24] == 411.4040703345004
    assert energy_data.energies_keV[-2, -2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1, -1] == 0.0


def test_read_cartesian_dat(file_path_energy_cartesian_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_dat)

    compare_xs_nm(energy_data)
    compare_ys_nm(energy_data)
    compare_zs_nm(energy_data)

    assert energy_data.energies_keV[0, 0, 0] == 1.56884
    assert energy_data.energies_keV[1, 1, 1] == 2.27235
    assert energy_data.energies_keV[24, 24, 24] == 411.404
    assert energy_data.energies_keV[-2, -2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1, -1] == 0.0


def test_cartesian_total_energy_dat(file_path_energy_cartesian_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_dat)

    assert energy_data.total_energy_keV == 9536354.883729976


def test_read_cylindrical_cas(file_path_energy_cylindrical_cas):
    energy_data = read_energy_data(file_path_energy_cylindrical_cas)

    assert energy_data.number_elements == 50 * 50

    compare_zs_nm(energy_data)
    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0, 0] == 32161.668619632866
    assert energy_data.energies_keV[1, 1] == 690.7337287232823
    assert energy_data.energies_keV[24, 24] == 4149.629987349835
    assert energy_data.energies_keV[-2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1] == 0.0


def test_read_cylindrical_dat(file_path_energy_cylindrical_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_dat)

    compare_zs_nm(energy_data)
    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0, 0] == 32161.7
    assert energy_data.energies_keV[1, 1] == 690.734
    assert energy_data.energies_keV[24, 24] == 4149.63
    assert energy_data.energies_keV[-2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1] == 0.0


def test_cylindrical_total_energy_dat(file_path_energy_cylindrical_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_dat)

    assert energy_data.total_energy_keV == 9899162.6705698


def test_read_spherical_cas(file_path_energy_spherical_cas):
    energy_data = read_energy_data(file_path_energy_spherical_cas)

    assert energy_data.number_elements == 50

    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0] == 1582.2293494223532
    assert energy_data.energies_keV[1] == 10978.987229982285
    assert energy_data.energies_keV[24] == 237544.09574357865
    assert energy_data.energies_keV[-2] == 3339.0087554269408
    assert energy_data.energies_keV[-1] == 3119.0176437913647


def test_read_spherical_dat(file_path_energy_spherical_dat):
    energy_data = read_energy_data(file_path_energy_spherical_dat)

    assert energy_data.number_elements == 50

    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0] == 1582.23
    assert energy_data.energies_keV[1] == 10979.0
    assert energy_data.energies_keV[24] == 237544.0
    assert energy_data.energies_keV[-2] == 3339.01
    assert energy_data.energies_keV[-1] == 3119.02


def test_spherical_total_energy_dat(file_path_energy_spherical_dat):
    energy_data = read_energy_data(file_path_energy_spherical_dat)

    assert energy_data.total_energy_keV == 9898224.42


def test_read_bad_file(filepath_sim_3202):
    energy_data = read_energy_data(filepath_sim_3202)

    with pytest.raises(AttributeError):
        assert energy_data.number_elements == 0

    assert energy_data.total_energy_keV is None

    with pytest.raises(TypeError):
        assert energy_data.energies_keV[0] == 0.0


def test_read_no_deposited_energy(file_path_no_deposited_energy_cas):
    energy_data = read_energy_data(file_path_no_deposited_energy_cas)

    with pytest.raises(AttributeError):
        assert energy_data.number_elements == 0

    assert energy_data.total_energy_keV is None

    with pytest.raises(TypeError):
        assert energy_data.energies_keV[0] == 0.0


def compare_xs_nm(energy_data):
    assert energy_data.xs_nm[0] == -250.0
    assert energy_data.xs_nm[1] == -240.0
    assert energy_data.xs_nm[-2] == 230.0
    assert energy_data.xs_nm[-1] == 240.0


def compare_ys_nm(energy_data):
    assert energy_data.ys_nm[0] == -250.0
    assert energy_data.ys_nm[1] == -240.0
    assert energy_data.ys_nm[-2] == 230.0
    assert energy_data.ys_nm[-1] == 240.0


def compare_zs_nm(energy_data):
    assert energy_data.zs_nm[0] == 0.0
    assert energy_data.zs_nm[1] == 10.0
    assert energy_data.zs_nm[-2] == 480.0
    assert energy_data.zs_nm[-1] == 490.0


def compare_radiuses_nm(energy_data):
    assert energy_data.radiuses_nm[0] == 0.0
    assert energy_data.radiuses_nm[1] == 10.0
    assert energy_data.radiuses_nm[24] == 240.0
    assert energy_data.radiuses_nm[-2] == 480.0
    assert energy_data.radiuses_nm[-1] == 490.0
