#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_options_physic
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.options_physic` module.
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
from casinotools.file_format.casino3.options_physic import OptionsPhysic, CrossSection
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
    reader = OptionsPhysic()
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.FRan == 3
    assert reader.FDeds == 1
    assert reader.FTotalCross == 5
    assert reader.FPartialCross == 5
    assert reader.FCosDirect == 1
    assert reader.FSecIon == 3
    assert reader.FPotMoy == 0

    assert reader.max_secondary_order == 10
    assert reader.Min_Energy_Nosec == pytest.approx(0.05)
    assert reader.Residual_Energy_Loss == pytest.approx(0.0004)
    assert reader.Min_Energy_With_Sec == pytest.approx(-1)
    assert reader.Min_Gen_Secondary_Energy == pytest.approx(-1)

    reader = OptionsPhysic()
    file = open(filepath_cas, 'rb')
    error = reader.read(file)

    assert error is None
    assert reader._version == 30107002
    assert reader.FRan == 3
    assert reader.FDeds == 1
    assert reader.FTotalCross == 5
    assert reader.FPartialCross == 5
    assert reader.FCosDirect == 1
    assert reader.FSecIon == 3
    assert reader.FPotMoy == 0

    assert reader.max_secondary_order == 10
    assert reader.Min_Energy_Nosec == pytest.approx(0.05)
    assert reader.Residual_Energy_Loss == pytest.approx(0.0004)
    assert reader.Min_Energy_With_Sec == pytest.approx(-1)
    assert reader.Min_Gen_Secondary_Energy == pytest.approx(-1)


def test_modified_cross_section(file_path_sim_tmp_modify_option):
    total_cs_ref = CrossSection.RUTHERFORD.value
    partial_cs_ref = CrossSection.MOTT_FILE.value

    with open(file_path_sim_tmp_modify_option, 'r+b') as file:
        reader = OptionsPhysic()
        error = reader.read(file)

        assert error is None
        assert reader._version == 30300004
        assert reader.FTotalCross == CrossSection.ELSEPA.value
        assert reader.FPartialCross == CrossSection.ELSEPA.value

        reader.FTotalCross = total_cs_ref
        reader.FPartialCross = partial_cs_ref

        reader.modify(file)

    with open(file_path_sim_tmp_modify_option, 'rb') as file:
        reader = OptionsPhysic()
        error = reader.read(file)

        assert error is None
        assert reader._version == 30300004
        assert reader.FTotalCross == total_cs_ref
        assert reader.FPartialCross == partial_cs_ref
