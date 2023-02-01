#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.utilities.test_path

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.utilities.path`.
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
import os.path

# Third party modules.
from pkg_resources import resource_filename
import pytest

# Local modules.

# Project modules.
import casinotools.utilities.path as path


# Globals and constants variables.


@pytest.fixture()
def git_lfs_file(tmpdir):
    git_lfs_file = tmpdir.join("temp_git_lfs_file.dat")

    with open(str(git_lfs_file), 'w') as input_file:
        input_file.write("version https://git-lfs.github.com/spec/v1\n")
        input_file.write("oid sha256:4d7a214614ab2935c943f9e0ff69d22eadbb8f32b1258daaa5e2ca24d17e2393\n")
        input_file.write("size 12345\n")

    return str(git_lfs_file)


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_is_git_lfs_file_bad(git_lfs_file):
    file_path = resource_filename(__name__, "test_path.py")
    if not os.path.isfile(file_path):  # pragma: no cover
        pytest.skip()
    assert path.is_git_lfs_file(file_path) is False


def test_is_git_lfs_file_good(git_lfs_file):
    assert path.is_git_lfs_file(git_lfs_file) is True


def test_is_bad_file():
    file_path = resource_filename(__name__, "test_path.py")
    if not os.path.isfile(file_path):  # pragma: no cover
        pytest.skip()
    assert path.is_bad_file(file_path) is False


def test_is_bad_file_git_lfs(git_lfs_file):
    assert path.is_bad_file(git_lfs_file) is True


def test_is_bad_file_no_file():
    file_path = resource_filename(__name__, "../../test_data/this_file_does_not_exist.txt")
    assert path.is_bad_file(file_path) is True
