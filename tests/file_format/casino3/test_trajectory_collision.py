#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_trajectory_collision
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.trajectory_collision` module.
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
from casinotools.file_format.casino3.trajectory_collision import TrajectoryCollision
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_cas):
    if is_bad_file(filepath_cas):
        pytest.skip()
    file = open(filepath_cas, 'rb')
    file.seek(4042617)
    results = TrajectoryCollision()

    error = results.read(file)
    assert error is None

    assert results._position_x == pytest.approx(-9.168622881064E-02)
    assert results._position_y == pytest.approx(-4.931083223782E-01)
    assert results._position_z == pytest.approx(-1.049980000000E+05)
    assert results._energy == pytest.approx(8.000000000000E-01)
    assert results._segment_length == pytest.approx(1.000000000000E+04)

    assert results._collision_type == 3
    assert results._region_id == -1
