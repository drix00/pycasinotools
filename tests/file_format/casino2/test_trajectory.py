#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_trajectory
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.trajectory` module.
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
from casinotools.file_format.casino2.trajectory import Trajectory
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_cas_26):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()
    with open(filepath_cas_26, 'rb') as file:
        _read_tests(file)


def test_read_string_io(filepath_cas_26):
    if is_bad_file(filepath_cas_26):  # pragma: no cover
        pytest.skip()
    f = open(filepath_cas_26, 'rb')
    file = BytesIO(f.read())
    f.close()
    _read_tests(file)


def _read_tests(file):
    file.seek(196464)
    trajectory = Trajectory()
    trajectory.read(file)

    assert trajectory.FRetro == 0
    assert trajectory.FTrans == 0
    assert trajectory.FDetec == 0
    assert trajectory.NbColl == 88

    assert trajectory.Zmax == pytest.approx(1.373841228321E+02)
    assert trajectory.LPM == pytest.approx(0.0)
    assert trajectory.DedsM == pytest.approx(-2.794824207165E-02)
    assert trajectory.PhiM == pytest.approx(3.281595883225E+00)
    assert trajectory.ThetaM == pytest.approx(2.596906806472E-01)
    assert trajectory.MoyenX == pytest.approx(-3.785237138949E+01)
    assert trajectory.MoyenY == pytest.approx(-2.676401848051E+01)
    assert trajectory.MoyenZ == pytest.approx(1.070857314139E+02)

    assert trajectory.Display == 1
    assert trajectory.NbElec == 89
