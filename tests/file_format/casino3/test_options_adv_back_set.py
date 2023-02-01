#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_options_adv_back_set
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.options_adv_back_set` module.
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
from casinotools.file_format.casino3.options_adv_back_set import OptionsAdvBackSet
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
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    file = open(filepath_sim, 'rb')
    reader = OptionsAdvBackSet()
    error = reader.read(file)

    assert error is None
    assert reader.version == 30107002
    assert reader.UseEnBack is False
    assert reader.WorkDist == pytest.approx(10.0)
    assert reader.DetectScaleX == pytest.approx(1.0)
    assert reader.DetectScaleY == pytest.approx(1.0)
    assert reader.ValidMatrix is False

    assert reader.BEMin_Angle == pytest.approx(0.0)
    assert reader.BEMax_Angle == pytest.approx(0.0)
    assert reader.EFilterMax == pytest.approx(0.0)
    assert reader.EFilterMin == pytest.approx(0.0)

    for i in range(101):
        assert reader.EFilterVal[i] == pytest.approx(1.0)

    assert reader.FEFilter == 0

    reader = OptionsAdvBackSet()
    file = open(filepath_cas, 'rb')
    error = reader.read(file)

    assert error is None
    assert reader.version == 30107002
    assert reader.UseEnBack is False
    assert reader.WorkDist == pytest.approx(10.0)
    assert reader.DetectScaleX == pytest.approx(1.0)
    assert reader.DetectScaleY == pytest.approx(1.0)
    assert reader.ValidMatrix is False

    assert reader.BEMin_Angle == pytest.approx(0.0)
    assert reader.BEMax_Angle == pytest.approx(0.0)
    assert reader.EFilterMax == pytest.approx(0.0)
    assert reader.EFilterMin == pytest.approx(0.0)

    for i in range(101):
        assert reader.EFilterVal[i] == pytest.approx(1.0)

    assert reader.FEFilter == 0
