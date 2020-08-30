#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_options_energy_by_pos
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.options_energy_by_pos` module.
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
from casinotools.file_format.casino3.options_energy_by_pos import OptionsEnergyByPos
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
    reader = OptionsEnergyByPos()
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.diffuse == 0
    assert reader.depos_summation == 1
    assert reader.depos_iso_level == pytest.approx(0.1)
    assert reader.carrier_surface_recombination == pytest.approx(-1.0)
    assert reader.normalize == 1

    reader = OptionsEnergyByPos()
    file = open(filepath_cas, 'rb')
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.diffuse == 0
    assert reader.depos_summation == 1
    assert reader.depos_iso_level == pytest.approx(0.1)
    assert reader.carrier_surface_recombination == pytest.approx(-1.0)
    assert reader.normalize == 1