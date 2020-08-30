#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_energy_matrix
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.energy_matrix` module.
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
from casinotools.file_format.casino3.energy_matrix import EnergyMatrix
from casinotools.file_format.casino3.options_dist import DIST_DEPOS_TYPE_CARTESIAN
from casinotools.file_format.casino3.simulation_options import SimulationOptions
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
    options = SimulationOptions()
    options._options_dist.DEpos_Type = DIST_DEPOS_TYPE_CARTESIAN
    results = EnergyMatrix(options, None)
    if is_bad_file(filepath_cas):
        pytest.skip()
    file = open(filepath_cas, 'rb')
    file.seek(4042541)

    error = results.read(file)
    assert error is None
    assert results._number_elements == 125000
    assert results._start_position == 4042541
    assert results._end_position == 4042541 + 125000 * 8