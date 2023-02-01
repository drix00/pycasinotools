#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_element

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.file_format.casino2.element`.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
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
from casinotools.file_format.casino2.element import Element, get_atom, compute_k
from casinotools.utilities.path import is_bad_file
from casinotools.file_format.casino2.line import ATOM_LINE_KA1, ATOM_LINE_KA2, ATOM_LINE_KB1
from casinotools.file_format.casino2.version import VERSION_2_45, VERSION_2_51
# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim_26):
    if is_bad_file(filepath_sim_26):  # pragma: no cover
        pytest.skip()
    with open(filepath_sim_26, 'rb') as file:
        _read_tests(file, VERSION_2_45)


def test_read_string_io(filepath_sim_26):
    if is_bad_file(filepath_sim_26):  # pragma: no cover
        pytest.skip()
    f = open(filepath_sim_26, 'rb')
    file = BytesIO(f.read())
    f.close()
    _read_tests(file, VERSION_2_45)


def _read_tests(file, version):
    file.seek(0)
    element = Element()
    element.read(file, 500, version)
    assert file.tell() == 49953

    assert element.Z == 5
    assert element.Nom == 'B'
    assert element.rho == pytest.approx(2.340000000000E+00)
    assert element.A == pytest.approx(1.081000000000E+01)
    assert element.J == pytest.approx(5.750000000000E-02)
    assert element.K == pytest.approx(7.790367583747E-01)
    assert element.ef == pytest.approx(1.0)
    assert element.kf == pytest.approx(7.000000000000E+07)
    assert element.ep == pytest.approx(2.270000000000E+01)


def test_get_atom():
    atomic_number, rho, z, a, ef, kf, ep = get_atom('Ag')
    assert atomic_number == 1
    assert rho == pytest.approx(10.50)
    assert z == 47
    assert a == 107.868
    assert ef == pytest.approx(5.5)
    assert kf * 1.0e-8 == pytest.approx(1.19)
    assert ep == pytest.approx(15)

    atomic_number, rho, z, a, ef, kf, ep = get_atom('ag')
    assert atomic_number == 0
    assert rho == pytest.approx(0.0)
    assert z == 0
    assert a == 0.0
    assert ef == pytest.approx(0.0)
    assert kf == pytest.approx(0.0)
    assert ep == pytest.approx(0.0)

    atomic_number, rho, z, a, ef, kf, ep = get_atom('V')
    assert atomic_number == 1
    assert rho == pytest.approx(5.8)
    assert z == 23
    assert a == 50.9415
    assert ef == pytest.approx(1.0)
    assert kf * 1.0e-7 == pytest.approx(7.0)
    assert ep == pytest.approx(21.8)


def test_compute_k():
    k_ref = 7.790367583747E-01
    k = compute_k(5)
    assert k == pytest.approx(k_ref)

    k_ref = 7.843098263659E-01
    k = compute_k(6)
    assert k == pytest.approx(k_ref)


def test_get_total_xray_intensities_1_esr(filepath_cas_v251):
    if is_bad_file(filepath_cas_v251):  # pragma: no cover
        pytest.skip()

    with open(filepath_cas_v251, 'rb') as file:
        file.seek(0)
        element = Element()
        # read the empty simulation data structure.
        element.read(file, 500, VERSION_2_51)
        assert file.tell() == 50193
        # read the first simulation data structure.
        element.read(file, 500, VERSION_2_51)
        assert file.tell() == 100638

        intensities_ref = {ATOM_LINE_KA1: 9.269059346795805e-07,
                           ATOM_LINE_KA2: 4.662984097246555e-07,
                           ATOM_LINE_KB1: 1.355707793206891e-08}

        intensities = element.get_total_xray_intensities_1_esr()

        assert len(intensities) == len(intensities_ref)

        for atomic_line in intensities:
            value_ref = intensities_ref[atomic_line]*1.0e6
            value = intensities[atomic_line]*1.0e6
            assert value == pytest.approx(value_ref)
