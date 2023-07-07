#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`module_name` module.
"""


###############################################################################
# Copyright 2023 Hendrix Demers
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
from pathlib import Path

# Third party modules.
import pytest
from pkg_resources import resource_filename

# Local modules.

# Project modules.
from casinotools.analyse.trajectories import is_casino_2_sim_file, is_casino_2_cas_file, is_casino_2_data_file, \
    is_casino_3_sim_file, is_casino_3_cas_file, is_casino_3_data_file

# Globals and constants variables.


@pytest.fixture()
def filepath_analyse_trajectories_sim_2_510():
    file_path = resource_filename(__name__, "../../test_data/casino2.x/v2.5.1.0/test_analyse_trajectories_2.5.1.0.sim")
    return Path(file_path)


@pytest.fixture()
def filepath_analyse_trajectories_cas_2_510():
    file_path = resource_filename(__name__, "../../test_data/casino2.x/v2.5.1.0/test_analyse_trajectories_2.5.1.0.cas")
    return Path(file_path)


@pytest.fixture()
def filepath_analyse_trajectories_dat_2_510():
    file_path = resource_filename(__name__, "../../test_data/casino2.x/v2.5.1.0/test_analyse_trajectories_2.5.1.0.dat")
    return Path(file_path)


@pytest.fixture()
def filepath_analyse_trajectories_sim_3_304():
    file_path = resource_filename(__name__, "../../test_data/casino3.x/v3.3/v3.3.0.4/test_analyse_trajectories_3.3.0.4.sim")
    return Path(file_path)


@pytest.fixture()
def filepath_analyse_trajectories_cas_3_304():
    file_path = resource_filename(__name__, "../../test_data/casino3.x/v3.3/v3.3.0.4/test_analyse_trajectories_3.3.0.4.cas")
    return Path(file_path)


@pytest.fixture()
def filepath_analyse_trajectories_dat_3_304():
    file_path = resource_filename(__name__, "../../test_data/casino3.x/v3.3/v3.3.0.4/test_analyse_trajectories_3.3.0.4.dat")
    return Path(file_path)


@pytest.fixture()
def filepaths_analyse_trajectories(filepath_analyse_trajectories_sim_2_510, filepath_analyse_trajectories_cas_2_510,
                                   filepath_analyse_trajectories_dat_2_510, filepath_analyse_trajectories_sim_3_304,
                                   filepath_analyse_trajectories_cas_3_304, filepath_analyse_trajectories_dat_3_304):
    filepaths = [filepath_analyse_trajectories_sim_2_510, filepath_analyse_trajectories_cas_2_510,
                 filepath_analyse_trajectories_dat_2_510, filepath_analyse_trajectories_sim_3_304,
                 filepath_analyse_trajectories_cas_3_304, filepath_analyse_trajectories_dat_3_304]
    return filepaths


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    assert True


def test_is_filepath_analyse_trajectories_sim_2_510(filepath_analyse_trajectories_sim_2_510):
    assert Path.is_file(filepath_analyse_trajectories_sim_2_510)


def test_is_filepath_analyse_trajectories_cas_2_510(filepath_analyse_trajectories_cas_2_510):
    assert Path.is_file(filepath_analyse_trajectories_cas_2_510)


def test_is_filepath_analyse_trajectories_dat_2_510(filepath_analyse_trajectories_dat_2_510):
    assert Path.is_file(filepath_analyse_trajectories_dat_2_510)


def test_is_filepath_analyse_trajectories_sim_3_304(filepath_analyse_trajectories_sim_3_304):
    assert Path.is_file(filepath_analyse_trajectories_sim_3_304)


def test_is_filepath_analyse_trajectories_cas_3_304(filepath_analyse_trajectories_cas_3_304):
    assert Path.is_file(filepath_analyse_trajectories_cas_3_304)


def test_is_filepath_analyse_trajectories_dat_3_304(filepath_analyse_trajectories_dat_3_304):
    assert Path.is_file(filepath_analyse_trajectories_dat_3_304)


def test_is_casino_2_sim_file(filepath_analyse_trajectories_sim_2_510, filepaths_analyse_trajectories):
    assert is_casino_2_sim_file(filepath_analyse_trajectories_sim_2_510)

    filepaths_analyse_trajectories.remove(filepath_analyse_trajectories_sim_2_510)

    for file_path in filepaths_analyse_trajectories:
        assert is_casino_2_sim_file(file_path) is False


def test_is_casino_2_cas_file(filepath_analyse_trajectories_cas_2_510, filepaths_analyse_trajectories):
    assert is_casino_2_cas_file(filepath_analyse_trajectories_cas_2_510)

    filepaths_analyse_trajectories.remove(filepath_analyse_trajectories_cas_2_510)

    for file_path in filepaths_analyse_trajectories:
        assert is_casino_2_cas_file(file_path) is False


def test_is_casino_2_data_file(filepath_analyse_trajectories_dat_2_510, filepaths_analyse_trajectories):
    assert is_casino_2_data_file(filepath_analyse_trajectories_dat_2_510)

    filepaths_analyse_trajectories.remove(filepath_analyse_trajectories_dat_2_510)

    for file_path in filepaths_analyse_trajectories:
        assert is_casino_2_data_file(file_path) is False


def test_is_casino_3_sim_file(filepath_analyse_trajectories_sim_3_304, filepaths_analyse_trajectories):
    assert is_casino_3_sim_file(filepath_analyse_trajectories_sim_3_304)

    filepaths_analyse_trajectories.remove(filepath_analyse_trajectories_sim_3_304)

    for file_path in filepaths_analyse_trajectories:
        assert is_casino_3_sim_file(file_path) is False


def test_is_casino_3_cas_file(filepath_analyse_trajectories_cas_3_304, filepaths_analyse_trajectories):
    assert is_casino_3_cas_file(filepath_analyse_trajectories_cas_3_304)

    filepaths_analyse_trajectories.remove(filepath_analyse_trajectories_cas_3_304)

    for file_path in filepaths_analyse_trajectories:
        assert is_casino_3_cas_file(file_path) is False


def test_is_casino_3_data_file(filepath_analyse_trajectories_dat_3_304, filepaths_analyse_trajectories):
    assert is_casino_3_data_file(filepath_analyse_trajectories_dat_3_304)

    filepaths_analyse_trajectories.remove(filepath_analyse_trajectories_dat_3_304)

    for file_path in filepaths_analyse_trajectories:
        assert is_casino_3_data_file(file_path) is False
