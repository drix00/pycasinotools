#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_region

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.file_format.casino2.region`.
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
from io import BytesIO

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino2.region import Region
from casinotools.file_format.casino2.version import VERSION_2_45
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

# Local modules.

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):  # pragma: no cover
        pytest.skip()
    with open(filepath_sim_2_45, 'rb') as file:
        _read_tests(file, VERSION_2_45)


def test_read_string_io(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):  # pragma: no cover
        pytest.skip()
    f = open(filepath_sim_2_45, 'rb')
    file = BytesIO(f.read())
    f.close()
    _read_tests(file, VERSION_2_45)


def _read_tests(file, version):
    file.seek(0)
    region = Region(500)
    region.read(file, version)

    assert region.ID == 0
    assert region.Name == "BC"
