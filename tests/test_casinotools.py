#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.test_casinotools

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools` package.
"""

# Copyright 2022 Hendrix Demers
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
from casinotools import get_current_module_path

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
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
    project_path = Path(tests_dir.parent, "casinotools")

    source_name = this_files_path.name.split("test_", maxsplit=1)[1]
    assert source_name[:-3] == "casinotools"

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
        source_file_path = Path(project_path, source_rel_dir, source_name)
        source_path = source_rel_dir.stem

        error_msg = f"{test_file_path} found, but {source_file_path} missing."
        assert source_file_path.is_file() or source_path == Path(source_name).stem, error_msg


def test_source_layout_matches_tests():
    # verify that this file is - itself - in tests/
    this_files_path = Path(__file__)
    source_path = this_files_path.parent.parent / "casinotools"
    assert source_path.name == "casinotools"

    # get a path to the j_park/ source directory
    tests_path = Path(source_path.parent, "tests")

    # loop through all test_*.py files in tests/
    # (and its subdirectories)
    for file_path in source_path.glob("**/*.py"):
        # construct the expected source_file_path
        tests_rel_dir = file_path.relative_to(source_path).parent
        if file_path.name == '__init__.py':
            tests_name = "test_" + file_path.parent.name + ".py"
        else:
            tests_name = "test_" + file_path.name
        tests_file_path = Path(tests_path, tests_rel_dir, tests_name)

        error_msg = f"{file_path} found, but {tests_file_path} missing."
        assert tests_file_path.is_file(), error_msg


def test_required_project_files():
    required_files = [".gitignore", "AUTHORS.rst", "CONTRIBUTING.rst", "HISTORY.rst", "LICENSE", "MANIFEST.in",
                      "pytest.ini", "README.rst", "requirements.txt", "setup.cfg", "setup.py"]

    project_path = get_current_module_path(__file__, "../")

    for required_file in required_files:
        file_path = project_path / required_file
        assert file_path.is_file()


def test_required_tests_files():
    required_files = ["__init__.py", "conftest.py"]

    project_path = get_current_module_path(__file__, "../")

    for required_file in required_files:
        file_path = project_path / "tests" / required_file
        assert file_path.is_file()


def test_required_docs_files():
    project_doc_path = get_current_module_path(__file__, "../") / "docs"
    assert project_doc_path.is_dir()

    required_files = ["readme.rst", "conf.py"]

    for required_file in required_files:
        file_path = project_doc_path / required_file
        assert file_path.is_file()

    required_paths = ["api"]

    for required_path in required_paths:
        path = project_doc_path / required_path
        assert path.is_dir()
