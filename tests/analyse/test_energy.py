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


def test_cartesian_energies_keV_e_cas(file_path_energy_cartesian_cas):
    energy_data = read_energy_data(file_path_energy_cartesian_cas)

    assert energy_data.number_electrons == 1000000

    assert energy_data.energies_keV_e[0, 0, 0] == 1.5688423948687005 * 1.0e-6
    assert energy_data.energies_keV_e[1, 1, 1] == 2.272354614047501 * 1.0e-6
    assert energy_data.energies_keV_e[24, 24, 24] == 411.4040703345004 * 1.0e-6
    assert energy_data.energies_keV_e[-2, -2, -2] == 0.0
    assert energy_data.energies_keV_e[-1, -1, -1] == 0.0


def test_cartesian_total_energy_cas(file_path_energy_cartesian_cas):
    energy_data = read_energy_data(file_path_energy_cartesian_cas)

    assert energy_data.total_energy_keV == 9536354.738660647


def test_cartesian_region_energy_cas(file_path_energy_cartesian_cas):
    energy_data = read_energy_data(file_path_energy_cartesian_cas)

    assert len(energy_data.regions_keV) == 6
    assert energy_data.regions_keV[0] == 70496.22496831052
    assert energy_data.regions_keV[1] == 0
    assert energy_data.regions_keV[2] == 465069.32524816366
    assert energy_data.regions_keV[3] == 0
    assert energy_data.regions_keV[4] == 9419760.151760759
    assert energy_data.regions_keV[5] == 0

    assert len(energy_data.regions_keV_e) == 6
    assert energy_data.regions_keV_e[0] == pytest.approx(70496.22496831052 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[1] == 0
    assert energy_data.regions_keV_e[2] == pytest.approx(465069.32524816366 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[3] == 0
    assert energy_data.regions_keV_e[4] == pytest.approx(9419760.151760759 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[5] == 0


def test_read_cartesian_dat(file_path_energy_cartesian_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_dat)

    compare_dat_xs_nm(energy_data)
    compare_dat_ys_nm(energy_data)
    compare_dat_zs_nm(energy_data)

    assert energy_data.energies_keV[0, 0, 0] == 1.56884
    assert energy_data.energies_keV[1, 1, 1] == 2.27235
    assert energy_data.energies_keV[24, 24, 24] == 411.404
    assert energy_data.energies_keV[-2, -2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1, -1] == 0.0


def test_cartesian_energies_keV_e_dat(file_path_energy_cartesian_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_dat)

    assert energy_data.number_electrons is None

    with pytest.raises(AttributeError):
        assert energy_data.energies_keV_e[0, 0, 0] == 1.5688423948687005 * 1.0e-6


def test_cartesian_total_energy_dat(file_path_energy_cartesian_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_dat)

    assert energy_data.total_energy_keV == 9536354.883729976


def test_cartesian_region_energy_dat(file_path_energy_cartesian_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_dat)

    assert len(energy_data.regions_keV) == 0
    assert len(energy_data.regions_keV_e) == 0


def test_read_cylindrical_cas(file_path_energy_cylindrical_cas):
    energy_data = read_energy_data(file_path_energy_cylindrical_cas)

    assert energy_data.number_elements == 50 * 50

    compare_zs_nm_dat(energy_data)
    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0, 0] == 32161.668619632866
    assert energy_data.energies_keV[1, 1] == 690.7337287232823
    assert energy_data.energies_keV[24, 24] == 4149.629987349835
    assert energy_data.energies_keV[-2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1] == 0.0


def test_cylindrical_energies_keV_e_cas(file_path_energy_cylindrical_cas):
    energy_data = read_energy_data(file_path_energy_cylindrical_cas)

    assert energy_data.number_electrons == 1000000

    assert energy_data.energies_keV_e[0, 0] == 32161.668619632866 * 1.0e-6
    assert energy_data.energies_keV_e[1, 1] == 690.7337287232823 * 1.0e-6
    assert energy_data.energies_keV_e[24, 24] == 4149.629987349835 * 1.0e-6
    assert energy_data.energies_keV_e[-2, -2] == 0.0
    assert energy_data.energies_keV_e[-1, -1] == 0.0


def test_cylindrical_total_energy_cas(file_path_energy_cylindrical_cas):
    energy_data = read_energy_data(file_path_energy_cylindrical_cas)

    assert energy_data.total_energy_keV == 9899161.88358982


def test_cylindrical_region_energy_cas(file_path_energy_cylindrical_cas):
    energy_data = read_energy_data(file_path_energy_cylindrical_cas)

    assert len(energy_data.regions_keV) == 6
    assert energy_data.regions_keV[0] == 70449.16458856294
    assert energy_data.regions_keV[1] == 0
    assert energy_data.regions_keV[2] == 464514.8447485271
    assert energy_data.regions_keV[3] == 0
    assert energy_data.regions_keV[4] == 9416317.211490775
    assert energy_data.regions_keV[5] == 0

    assert len(energy_data.regions_keV_e) == 6
    assert energy_data.regions_keV_e[0] == pytest.approx(70449.16458856294 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[1] == 0
    assert energy_data.regions_keV_e[2] == pytest.approx(464514.8447485271 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[3] == 0
    assert energy_data.regions_keV_e[4] == pytest.approx(9416317.211490775 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[5] == 0


def test_read_cylindrical_dat(file_path_energy_cylindrical_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_dat)

    compare_zs_nm_dat(energy_data)
    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0, 0] == 32161.7
    assert energy_data.energies_keV[1, 1] == 690.734
    assert energy_data.energies_keV[24, 24] == 4149.63
    assert energy_data.energies_keV[-2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1] == 0.0


def test_cylindrical_energies_keV_e_dat(file_path_energy_cylindrical_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_dat)

    assert energy_data.number_electrons is None

    with pytest.raises(AttributeError):
        assert energy_data.energies_keV_e[0, 0, 0] == 1.5688423948687005 * 1.0e-6


def test_cylindrical_total_energy_dat(file_path_energy_cylindrical_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_dat)

    assert energy_data.total_energy_keV == 9899162.6705698


def test_cylindrical_region_energy_dat(file_path_energy_cylindrical_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_dat)

    assert len(energy_data.regions_keV) == 0
    assert len(energy_data.regions_keV_e) == 0


def test_read_spherical_cas(file_path_energy_spherical_cas):
    energy_data = read_energy_data(file_path_energy_spherical_cas)

    assert energy_data.number_elements == 50

    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0] == 1582.2293494223532
    assert energy_data.energies_keV[1] == 10978.987229982285
    assert energy_data.energies_keV[24] == 237544.09574357865
    assert energy_data.energies_keV[-2] == 3339.0087554269408
    assert energy_data.energies_keV[-1] == 3119.0176437913647


def test_spherical_energies_keV_e_cas(file_path_energy_spherical_cas):
    energy_data = read_energy_data(file_path_energy_spherical_cas)

    assert energy_data.number_electrons == 1000000

    assert energy_data.energies_keV_e[0] == 1582.2293494223532 * 1.0e-6
    assert energy_data.energies_keV_e[1] == 10978.987229982285 * 1.0e-6
    assert energy_data.energies_keV_e[24] == 237544.09574357865 * 1.0e-6
    assert energy_data.energies_keV_e[-2] == 3339.0087554269408 * 1.0e-6
    assert energy_data.energies_keV_e[-1] == 3119.017643791365 * 1.0e-6


def test_spherical_total_energy_cas(file_path_energy_spherical_cas):
    energy_data = read_energy_data(file_path_energy_spherical_cas)

    assert energy_data.total_energy_keV == 9898225.278373864


def test_spherical_region_energy_cas(file_path_energy_spherical_cas):
    energy_data = read_energy_data(file_path_energy_spherical_cas)

    assert len(energy_data.regions_keV) == 6
    assert energy_data.regions_keV[0] == 70378.35032948921
    assert energy_data.regions_keV[1] == 0
    assert energy_data.regions_keV[2] == 463863.2550332439
    assert energy_data.regions_keV[3] == 0
    assert energy_data.regions_keV[4] == 9422198.587173153
    assert energy_data.regions_keV[5] == 0

    assert len(energy_data.regions_keV_e) == 6
    assert energy_data.regions_keV_e[0] == pytest.approx(70378.35032948921 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[1] == 0
    assert energy_data.regions_keV_e[2] == pytest.approx(463863.2550332439 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[3] == 0
    assert energy_data.regions_keV_e[4] == pytest.approx(9422198.587173153 * 1.0e-6, 12)
    assert energy_data.regions_keV_e[5] == 0


def test_read_spherical_dat(file_path_energy_spherical_dat):
    energy_data = read_energy_data(file_path_energy_spherical_dat)

    assert energy_data.number_elements == 50

    compare_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0] == 1582.23
    assert energy_data.energies_keV[1] == 10979.0
    assert energy_data.energies_keV[24] == 237544.0
    assert energy_data.energies_keV[-2] == 3339.01
    assert energy_data.energies_keV[-1] == 3119.02


def test_spherical_energies_keV_e_dat(file_path_energy_spherical_dat):
    energy_data = read_energy_data(file_path_energy_spherical_dat)

    assert energy_data.number_electrons is None

    with pytest.raises(AttributeError):
        assert energy_data.energies_keV_e[0, 0, 0] == 1.5688423948687005 * 1.0e-6


def test_spherical_total_energy_dat(file_path_energy_spherical_dat):
    energy_data = read_energy_data(file_path_energy_spherical_dat)

    assert energy_data.total_energy_keV == 9898224.42


def test_spherical_region_energy_dat(file_path_energy_spherical_dat):
    energy_data = read_energy_data(file_path_energy_spherical_dat)

    assert len(energy_data.regions_keV) == 0
    assert len(energy_data.regions_keV_e) == 0


def test_read_cartesian_log_cas(file_path_energy_cartesian_log_cas):
    energy_data = read_energy_data(file_path_energy_cartesian_log_cas)

    assert energy_data.number_elements == 50 * 50 * 50

    compare_xs_nm(energy_data)
    compare_ys_nm(energy_data)
    compare_zs_nm(energy_data)

    assert energy_data.energies_keV[0, 0, 0] == 2.0876775811210173
    assert energy_data.energies_keV[1, 1, 1] == 1.7060901002452047
    assert energy_data.energies_keV[24, 24, 24] == 404.20891939843676
    assert energy_data.energies_keV[-2, -2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1, -1] == 0.0


def test_cartesian_total_energy_log_cas(file_path_energy_cartesian_log_cas):
    energy_data = read_energy_data(file_path_energy_cartesian_log_cas)

    assert energy_data.total_energy_keV == 9522341.342891479


def test_read_cartesian_log_dat(file_path_energy_cartesian_log_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_log_dat)

    compare_dat_xs_nm(energy_data)
    compare_dat_ys_nm(energy_data)
    compare_dat_zs_nm(energy_data)

    assert energy_data.energies_keV[0, 0, 0] == 2.08768
    assert energy_data.energies_keV[1, 1, 1] == 1.70609
    assert energy_data.energies_keV[24, 24, 24] == 404.209
    assert energy_data.energies_keV[-2, -2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1, -1] == 0.0


def test_cartesian_total_energy_log_dat(file_path_energy_cartesian_log_dat):
    energy_data = read_energy_data(file_path_energy_cartesian_log_dat)

    assert energy_data.total_energy_keV == 9522341.177130042


def test_read_cylindrical_log_cas(file_path_energy_cylindrical_log_cas):
    energy_data = read_energy_data(file_path_energy_cylindrical_log_cas)

    assert energy_data.number_elements == 50 * 50

    compare_zs_nm_dat(energy_data)
    compare_log_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0, 0] == 32163.283594180775
    assert energy_data.energies_keV[1, 1] == 679.9492457467027
    assert energy_data.energies_keV[24, 24] == 4026.5526508481285
    assert energy_data.energies_keV[-2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1] == 0.0


def test_cylindrical_total_energy_log_cas(file_path_energy_cylindrical_log_cas):
    energy_data = read_energy_data(file_path_energy_cylindrical_log_cas)

    assert energy_data.total_energy_keV == 9911381.408432323


def test_read_cylindrical_log_dat(file_path_energy_cylindrical_log_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_log_dat)

    compare_dat_zs_nm(energy_data)
    compare_log_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0, 0] == 32163.3
    assert energy_data.energies_keV[1, 1] == 679.949
    assert energy_data.energies_keV[24, 24] == 4026.55
    assert energy_data.energies_keV[-2, -2] == 0.0
    assert energy_data.energies_keV[-1, -1] == 0.0


def test_cylindrical_total_energy_log_dat(file_path_energy_cylindrical_log_dat):
    energy_data = read_energy_data(file_path_energy_cylindrical_log_dat)

    assert energy_data.total_energy_keV == 9911381.701784529


def test_read_spherical_log_cas(file_path_energy_spherical_log_cas):
    energy_data = read_energy_data(file_path_energy_spherical_log_cas)

    assert energy_data.number_elements == 50

    compare_log_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0] == 1561.262589166787
    assert energy_data.energies_keV[1] == 10938.12819789883
    assert energy_data.energies_keV[24] == 238640.1759343048
    assert energy_data.energies_keV[-2] == 3358.121421067252
    assert energy_data.energies_keV[-1] == 3182.2921562739857


def test_spherical_total_energy_log_cas(file_path_energy_spherical_log_cas):
    energy_data = read_energy_data(file_path_energy_spherical_log_cas)

    assert energy_data.total_energy_keV == 9897975.042269977


def test_read_spherical_log_dat(file_path_energy_spherical_log_dat):
    energy_data = read_energy_data(file_path_energy_spherical_log_dat)

    assert energy_data.number_elements == 50

    compare_log_radiuses_nm(energy_data)

    assert energy_data.energies_keV[0] == 1561.26
    assert energy_data.energies_keV[1] == 10938.1
    assert energy_data.energies_keV[24] == 238640.0
    assert energy_data.energies_keV[-2] == 3358.12
    assert energy_data.energies_keV[-1] == 3182.29


def test_spherical_total_energy_log_dat(file_path_energy_spherical_log_dat):
    energy_data = read_energy_data(file_path_energy_spherical_log_dat)

    assert energy_data.total_energy_keV == 9897971.179999998


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
    assert energy_data.xs_nm[0] == -245.0
    assert energy_data.xs_nm[1] == -235.0
    assert energy_data.xs_nm[-2] == 235.0
    assert energy_data.xs_nm[-1] == 245.0


def compare_ys_nm(energy_data):
    assert energy_data.ys_nm[0] == -245.0
    assert energy_data.ys_nm[1] == -235.0
    assert energy_data.ys_nm[-2] == 235.0
    assert energy_data.ys_nm[-1] == 245.0


def compare_zs_nm(energy_data):
    assert energy_data.zs_nm[0] == 5.0
    assert energy_data.zs_nm[1] == 15.0
    assert energy_data.zs_nm[-2] == 485.0
    assert energy_data.zs_nm[-1] == 495.0


def compare_zs_nm_dat(energy_data):
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


def compare_dat_xs_nm(energy_data):
    assert energy_data.xs_nm[0] == -250.0
    assert energy_data.xs_nm[1] == -240.0
    assert energy_data.xs_nm[-2] == 230.0
    assert energy_data.xs_nm[-1] == 240.0


def compare_dat_ys_nm(energy_data):
    assert energy_data.ys_nm[0] == -250.0
    assert energy_data.ys_nm[1] == -240.0
    assert energy_data.ys_nm[-2] == 230.0
    assert energy_data.ys_nm[-1] == 240.0


def compare_dat_zs_nm(energy_data):
    assert energy_data.zs_nm[0] == 0.0
    assert energy_data.zs_nm[1] == 10.0
    assert energy_data.zs_nm[-2] == 480.0
    assert energy_data.zs_nm[-1] == 490.0


def compare_log_radiuses_nm(energy_data):
    assert energy_data.radiuses_nm[0] == 0.0
    assert energy_data.radiuses_nm[1] == 10.0
    assert energy_data.radiuses_nm[24] == 240.0
    assert energy_data.radiuses_nm[-2] == 480.0
    assert energy_data.radiuses_nm[-1] == 490.0
