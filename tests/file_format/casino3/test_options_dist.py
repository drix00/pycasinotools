#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_options_dist
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.options_dist` module.
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
from casinotools.file_format.casino3.options_dist import OptionsDist, autoFlag, DIST_DEPOS_POSITION_ABSOLUTE
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim, filepath_cas):
    if is_bad_file(filepath_sim):
        pytest.skip()
    file = open(filepath_sim, 'rb')
    reader = OptionsDist()
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.DenrMax / autoFlag == pytest.approx(1.0)

    assert reader.DEposCyl_Z == pytest.approx(1000.0)
    assert reader.DEposCyl_Z_Log == 0
    assert reader.DEpos_Position == DIST_DEPOS_POSITION_ABSOLUTE

    reader = OptionsDist()
    file = open(filepath_cas, 'rb')
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.DenrMax / autoFlag == pytest.approx(1.0)

    assert reader.DEposCyl_Z == pytest.approx(1000.0)
    assert reader.DEposCyl_Z_Log == 0
    assert reader.DEpos_Position == DIST_DEPOS_POSITION_ABSOLUTE
