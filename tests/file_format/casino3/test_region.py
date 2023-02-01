#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.test_casino3.region
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.region` module.
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
from casinotools.file_format.casino3.region import Region
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim):
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    file = open(filepath_sim, 'rb')
    file.seek(6560)
    region = Region()
    region.read(file)

    assert region._version == 30107003
    assert region._carrier_diffusion_length == pytest.approx(50.0)
    assert region._number_elements == 1
    assert region.rho == pytest.approx(2.33)
    assert region._work_function == pytest.approx(-1.0)
    assert region._average_plasmon_energy == pytest.approx(-1.0)
    assert region.id == 1
    assert region.substrate == 0
    assert region.user_density == 0
    assert region.user_composition == 0
    assert region._checked == 0

    assert region.name == "SiSubtrate"

    assert region._number_sample_objects == 1
    assert region._sample_object_ids[0] == 1

    assert region._moller_init == pytest.approx(0.0)
    assert region._triangle_color_x == pytest.approx(0.235)
    assert region._triangle_color_y == pytest.approx(0.235)
    assert region._triangle_color_z == pytest.approx(1.0)

    assert region._chemical_name == "Si"
