#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.test_casinotools

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools` package.
"""

# Copyright 2019 Hendrix Demers
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
import os.path

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.


def test_structure():
    """
    Test if the testing structure work.
    """

    # assert False
    assert True


def test_file_path_energy_cartesian_cas(file_path_energy_cartesian_cas):
    assert os.path.isfile(file_path_energy_cartesian_cas)


def test_file_path_energy_cylindrical_cas(file_path_energy_cylindrical_cas):
    assert os.path.isfile(file_path_energy_cylindrical_cas)


def test_file_path_energy_spherical_cas(file_path_energy_spherical_cas):
    assert os.path.isfile(file_path_energy_spherical_cas)


def test_file_path_no_deposited_energy_cas(file_path_no_deposited_energy_cas):
    assert os.path.isfile(file_path_no_deposited_energy_cas)


def test_file_path_energy_cartesian_dat(file_path_energy_cartesian_dat):
    assert os.path.isfile(file_path_energy_cartesian_dat)


def test_file_path_energy_cylindrical_dat(file_path_energy_cylindrical_dat):
    assert os.path.isfile(file_path_energy_cylindrical_dat)


def test_file_path_energy_spherical_dat(file_path_energy_spherical_dat):
    assert os.path.isfile(file_path_energy_spherical_dat)


def test_file_path_energy_cartesian_log_cas(file_path_energy_cartesian_cas):
    assert os.path.isfile(file_path_energy_cartesian_cas)


def test_file_path_energy_cylindrical_log_cas(file_path_energy_cylindrical_cas):
    assert os.path.isfile(file_path_energy_cylindrical_cas)


def test_file_path_energy_spherical_log_cas(file_path_energy_spherical_cas):
    assert os.path.isfile(file_path_energy_spherical_cas)


def test_file_path_energy_cartesian_log_dat(file_path_energy_cartesian_dat):
    assert os.path.isfile(file_path_energy_cartesian_dat)


def test_file_path_energy_cylindrical_log_dat(file_path_energy_cylindrical_dat):
    assert os.path.isfile(file_path_energy_cylindrical_dat)


def test_file_path_energy_spherical_log_dat(file_path_energy_spherical_dat):
    assert os.path.isfile(file_path_energy_spherical_dat)
