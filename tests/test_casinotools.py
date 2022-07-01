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
from pathlib import Path

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


def test_tests_layout_matches_source():
    # verify that this file is - itself - in tests/
    this_files_path = Path(__file__)
    tests_dir = this_files_path.parent
    assert tests_dir.name == "tests"

    # get a path to the j_park/ source directory
    j_park_path = Path(tests_dir.parent, "casinotools")

    # loop through all test_*.py files in tests/
    # (and its subdirectories)
    for test_file_path in tests_dir.glob("**/test_*.py"):
        # skip this file: we don't expect there to be a
        # corresponding source file for this layout enforcer
        if test_file_path == this_files_path:
            continue

        # construct the expected source_file_path
        source_rel_dir = test_file_path.relative_to(tests_dir).parent
        source_name = test_file_path.name.split("test_", maxsplit=1)[1]
        source_file_path = Path(j_park_path, source_rel_dir, source_name)
        source_path = source_rel_dir.stem

        error_msg = f"{test_file_path} found, but {source_file_path} missing."

        assert source_file_path.is_file() or source_path == Path(source_name).stem


def test_source_layout_matches_tests():
    # verify that this file is - itself - in tests/
    this_files_path = Path(__file__)
    tests_dir = this_files_path.parent
    assert tests_dir.name == "tests"

    # get a path to the j_park/ source directory
    source_dir = Path(tests_dir.parent, "casinotools")

    # loop through all test_*.py files in tests/
    # (and its subdirectories)
    for file_path in source_dir.glob("**/*.py"):
        # construct the expected source_file_path
        source_rel_dir = file_path.relative_to(source_dir).parent
        source_name = file_path.name.split("test_", maxsplit=1)[1]
        source_file_path = Path(source_dir, source_rel_dir, source_name)
        source_rel_path = source_rel_dir.stem

        error_msg = f"{file_path} found, but {source_file_path} missing."

        assert source_file_path.is_file() or source_rel_path == Path(source_name).stem
