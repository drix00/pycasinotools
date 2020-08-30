#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_composition
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.composition` module.
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
from casinotools.file_format.casino2.composition import Composition
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):
        pytest.skip()

    with open(filepath_sim_2_45, 'rb') as file:
        _read_tests(file)


def test_read_string_io(filepath_sim_2_45):
    if is_bad_file(filepath_sim_2_45):
        pytest.skip()

    f = open(filepath_sim_2_45, 'rb')
    buf = BytesIO(f.read())
    f.close()
    _read_tests(buf)


def _read_tests(file):
    file.seek(1889)
    composition = Composition()
    composition.read(file)

    assert composition.NuEl == 0
    assert composition.FWt == pytest.approx(7.981000000000E-01)
    assert composition.FAt == pytest.approx(8.145442797934E-01)
    assert composition.SigmaT == pytest.approx(0.0)
    assert composition.SigmaTIne == pytest.approx(0.0)
    assert composition.Rep == 1
