#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_element
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.element` module.
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
from casinotools.file_format.casino3.element import Element, get_atom, compute_k
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
    file.seek(7159)
    element = Element()
    element.read(file)

    assert element.version == 30105010
    assert element._element_id == 0
    assert element._weight_fraction == pytest.approx(0.660569621292935)
    assert element._atomic_fraction == pytest.approx(0.372901678657074)
    assert element._sigma_total_elastic == pytest.approx(0.0)
    assert element._repetition == 311

    assert element.z == 6.0
    assert element.name == 'C'
    assert element.rho == pytest.approx(2.62)
    assert element.A == pytest.approx(12.011)
    assert element.J == pytest.approx(0.0)
    assert element.K_Gauvin == pytest.approx(0.0)
    assert element.K_Monsel == pytest.approx(-9.584629012423031e+36)
    assert element.ef == pytest.approx(1.0)
    assert element.kf == pytest.approx(7.000000000000E+07)
    assert element.ep == pytest.approx(15.0)

    for index in range(3):
        assert element.Int_PRZ[index] == pytest.approx(0.0)
        assert element.Int_PRZ_ABS[index] == pytest.approx(0.0)


def test_atom():
    flag_atom, rho, z, a, ef, kf, ep = get_atom('Ag')
    assert flag_atom == 1
    assert rho == pytest.approx(10.50)
    assert z == 47
    assert a == pytest.approx(107.868)
    assert ef == pytest.approx(5.5)
    assert kf * 1.0e-8 == pytest.approx(1.19)
    assert ep == pytest.approx(15.0)

    flag_atom, rho, z, a, ef, kf, ep = get_atom('ag')
    assert flag_atom == 0
    assert rho == pytest.approx(0.0)
    assert z == 0
    assert a == pytest.approx(0.0)
    assert ef == pytest.approx(0.0)
    assert kf == pytest.approx(0.0)
    assert ep == pytest.approx(0.0)

    flag_atom, rho, z, a, ef, kf, ep = get_atom('V')
    assert flag_atom == 1
    assert rho == pytest.approx(5.8)
    assert z == 23
    assert a == pytest.approx(50.9415)
    assert ef == pytest.approx(1.0)
    assert kf * 1.0e-7 == pytest.approx(7.0)
    assert ep == pytest.approx(21.8)


def test__compute_k():
    k_ref = 7.790367583747E-01
    k = compute_k(5)
    assert k == pytest.approx(k_ref)

    k_ref = 7.843098263659E-01
    k = compute_k(6)
    assert k == pytest.approx(k_ref)
