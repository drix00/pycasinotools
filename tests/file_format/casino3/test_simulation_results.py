#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_simulation_results
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.simulation_results` module.
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
from casinotools.file_format.casino3.simulation_results import SimulationResults
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

# Local modules.

# Globals and constants variables.


def test_read(filepath_cas):
    if is_bad_file(filepath_cas):  # pragma: no cover
        pytest.skip()
    file = open(filepath_cas, 'rb')
    options = SimulationOptions()
    options.read(file)
    file.close()
    del file

    results = SimulationResults()
    file = open(filepath_cas, 'rb')
    file.seek(12648)
    error = results.read(file, options)

    assert error is None
    assert results._number_simulations == 1

    assert results.version == 20031202

    assert results._initial_energy_keV == pytest.approx(0.8)
    assert results._rko_max == 0.0

    assert results._version_simulation_results == 30107002
    assert results._is_total_energy_density_saved is True
