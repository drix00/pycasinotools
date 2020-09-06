#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_scattering_event
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.scattering_event` module.
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
from io import BytesIO

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino2.scattering_event import ScatteringEvent
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_cas_26):
    if is_bad_file(filepath_cas_26):
        pytest.skip()
    with open(filepath_cas_26, 'rb') as file:
        _read_tests(file)


def test_read_string_io(filepath_cas_26):
    if is_bad_file(filepath_cas_26):
        pytest.skip()
    f = open(filepath_cas_26, 'rb')
    file = BytesIO(f.read())
    f.close()
    _read_tests(file)


def _read_tests(file):
    file.seek(196552)
    event = ScatteringEvent()
    event.read(file)

    assert event.X == pytest.approx(-2.903983831406E+00)
    assert event.Y == pytest.approx(-3.020418643951E+00)
    assert event.z == pytest.approx(0.0)
    assert event.E == pytest.approx(4.000000000000E+00)
    assert event.Intersect == 0
    assert event.id == 0
