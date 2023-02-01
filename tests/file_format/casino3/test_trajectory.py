#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_trajectory
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.trajectory` module.
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
from casinotools.file_format.casino3.trajectory import Trajectory
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True

# Local modules.

# Globals and constants variables.


def test_read(filepath_cas):
    if is_bad_file(filepath_cas):  # pragma: no cover
        pytest.skip()
    file = open(filepath_cas, 'rb')
    file.seek(4042541)
    results = Trajectory()

    assert file is not None
    error = results.read(file)
    assert error is None

    version = results.get_version()
    assert version == 30105012

    assert results._type == 256

    assert results._order == 1
    assert results._dir_x == pytest.approx(-3.071803288788E-01)
    assert results._dir_y == pytest.approx(8.927911784036E-02)
    assert results._dir_z == pytest.approx(9.474542124386E-01)
    assert results._number_scattering_events == 28
