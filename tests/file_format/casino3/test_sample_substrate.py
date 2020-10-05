#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_sample_substrate
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.sample_substrate` module.
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
from casinotools.file_format.casino3.sample_object_factory import create_object_from_type
from casinotools.file_format.casino3.sample_shape.shape_type import SHAPE_SUBSTRATE
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
    if is_bad_file(filepath_sim):
        pytest.skip()
    file = open(filepath_sim, "rb")
    file.seek(103)
    sample = create_object_from_type(SHAPE_SUBSTRATE)
    sample.read(file)

    assert sample._version == 30105004

    assert sample._name == "Substrate"
    assert sample._region_name == "Substrate"

    assert sample.translation == [0.0, 0.0, 0.0]
    assert sample.rotation == [0.0, 0.0, 0.0]
    assert sample.scale == [100000.0, 100000.0, 100000.0]
    assert sample.color == [0.0, 0.0, 1.0]

    assert sample._numberEdges == 0

    assert sample.shape_type == SHAPE_SUBSTRATE
