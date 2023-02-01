#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_element_intensity
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.element_intensity` module.
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
from casinotools.file_format.casino2.element_intensity import ElementIntensity
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


def test_read(filepath_cas_26):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()

    with open(filepath_cas_26, 'rb') as casino_file:
        _read_tests(casino_file)


def test_read_string_io(filepath_cas_26):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()

    f = open(filepath_cas_26, 'rb')
    casino_file = BytesIO(f.read())
    f.close()
    _read_tests(casino_file)


def _read_tests(casino_file):
    casino_file.seek(696872)
    element = ElementIntensity()
    element.read(casino_file)

    assert element.name == "B"
    assert element.IntensityK[0] == pytest.approx(3.444919288026E+02)
