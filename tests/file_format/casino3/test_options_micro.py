#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_options_micro
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.options_micro` module.
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
from casinotools.file_format.casino3.options_micro import OptionsMicro
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
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    file = open(filepath_sim, 'rb')
    reader = OptionsMicro()
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.scanning_mode == 0
    assert reader.x_plane_position == pytest.approx(0.0)

    assert reader.scan_point_distribution == pytest.approx(1.0)
    assert reader.keep_simulation_data == 1

    reader = OptionsMicro()
    file = open(filepath_cas, 'rb')
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.scanning_mode == 0
    assert reader.x_plane_position == pytest.approx(0.0)

    assert reader.scan_point_distribution == pytest.approx(1.0)
    assert reader.keep_simulation_data == 1


def test_modified_energy(file_path_sim_tmp_modify_option):
    energy_keV_ref = 3.5

    with open(file_path_sim_tmp_modify_option, 'r+b') as file:
        reader = OptionsMicro()
        error = reader.read(file)

        assert error is None
        assert reader._version == 30300004
        assert reader.KEV_End == pytest.approx(0.0)
        assert reader.KEV_Start == pytest.approx(1.0)

        assert reader.KEV_Step == pytest.approx(1.0)
        assert reader.multiple_scan_energy == 0

        reader.KEV_Start = energy_keV_ref

        reader.modify(file)

    with open(file_path_sim_tmp_modify_option, 'rb') as file:
        reader = OptionsMicro()
        error = reader.read(file)

        assert error is None
        assert reader._version == 30300004
        assert reader.KEV_End == pytest.approx(0.0)
        assert reader.KEV_Start == pytest.approx(energy_keV_ref)

        assert reader.KEV_Step == pytest.approx(1.0)
        assert reader.multiple_scan_energy == 0
