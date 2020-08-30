#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_generate_sim_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.generate_sim_file` module.
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
from casinotools.file_format.casino2.generate_sim_file import GenerateSimFile
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


@pytest.fixture()
def generate_sim_file(filepath_std):
    if is_bad_file(filepath_std):
        pytest.skip()
    generate = GenerateSimFile(filepath_std)
    return generate


def test_set_incident_energy_keV(generate_sim_file):
    energy_ref_keV = 10.0
    generate_sim_file.set_incident_energy_keV(energy_ref_keV)

    energy_keV = generate_sim_file.get_option_simulation_data().get_simulation_options().get_incident_energy_keV()
    assert energy_keV == pytest.approx(energy_ref_keV)


def test_set_toa_deg(generate_sim_file):
    toa_ref_deg = 52.5
    generate_sim_file.set_toa_deg(toa_ref_deg)

    toa_deg = generate_sim_file.get_option_simulation_data().get_simulation_options().get_toa_deg()
    assert toa_deg == pytest.approx(toa_ref_deg)


def test_add_element(generate_sim_file):
    generate_sim_file._remove_all_elements()

    symbol_ref = 'Cu'
    generate_sim_file._add_element(symbol_ref)
    symbol = generate_sim_file.get_option_simulation_data().get_region_options().get_region(0).get_element(0).get_symbol()
    assert symbol == symbol_ref

    generate_sim_file._remove_all_elements()
    symbol_ref = 'B'
    generate_sim_file._add_element(symbol_ref, 0.7981)
    symbol_ref = 'C'
    generate_sim_file._add_element(symbol_ref, 1.0 - 0.7981)

    element = generate_sim_file.get_option_simulation_data().get_region_options().get_region(0).get_element(0)
    assert element.Z == 5
    assert element.Nom == 'B'
    assert element.rho == pytest.approx(2.340000000000E+00)
    assert element.A == pytest.approx(1.081000000000E+01)
    assert element.J == pytest.approx(5.750000000000E-02)
    assert element.K == pytest.approx(7.790367583747E-01)
    assert element.ef == pytest.approx(1.0)
    assert element.kf * 1.0e-7 == pytest.approx(7.000000000000)
    assert element.ep == pytest.approx(2.270000000000E+01)

    composition = element.get_composition()
    assert composition.NuEl == 0
    assert composition.FWt == pytest.approx(7.981000000000E-01)
    # assert composition.FAt == pytest.approx(8.145442797934E-01)
    assert composition.SigmaT == pytest.approx(0.0)
    assert composition.SigmaTIne == pytest.approx(0.0)
    assert composition.Rep == 1

    element = generate_sim_file.get_option_simulation_data().get_region_options().get_region(0).get_element(1)
    assert element.Z == 6
    assert element.Nom == 'C'
    assert element.rho == pytest.approx(2.620000000000E+00)
    assert element.A == pytest.approx(1.201100000000E+01)
    assert element.J == pytest.approx(6.900000000000E-02)
    assert element.K == pytest.approx(7.843098263659E-01)
    assert element.ef == pytest.approx(1.0)
    assert element.kf * 1.0e-7 == pytest.approx(7.000000000000)
    assert element.ep == pytest.approx(1.500000000000E+01)

    composition = element.get_composition()
    assert composition.NuEl == 0
    assert composition.FWt == pytest.approx(2.019000000000E-01)
    # assert composition.FAt == pytest.approx(1.854557202066E-01)
    assert composition.SigmaT == pytest.approx(0.0)
    assert composition.SigmaTIne == pytest.approx(0.0)
    assert composition.Rep == 1


def test_add_elements(generate_sim_file):
    symbols = ['B']
    generate_sim_file.add_elements(symbols)
    element = generate_sim_file.get_option_simulation_data().get_region_options().get_region(0).get_element(0)
    assert element.Z == 5
    composition = element.get_composition()
    assert composition.NuEl == 0
    assert composition.FWt == pytest.approx(1.0)
    assert composition.FAt == pytest.approx(1.0)

    symbols = ['B', 'C']
    weight_fractions = [0.7981, 1.0 - 0.7981]
    generate_sim_file.add_elements(symbols, weight_fractions)

    region = generate_sim_file.get_option_simulation_data().get_region_options().get_region(0)

    assert region.get_number_elements() == 2
    assert region.get_mean_mass_density_g_cm3() == pytest.approx(2.3916, 4)
    assert region.get_mean_atomic_number() == pytest.approx(5.5)
    assert region.get_name() == 'BC'

    element = region.get_element(0)
    assert element.Z == 5
    composition = element.get_composition()
    assert composition.NuEl == 0
    assert composition.FWt == pytest.approx(7.981000000000E-01)
    assert composition.FAt == pytest.approx(8.145442797934E-01)

    element = region.get_element(1)
    assert element.Z == 6
    composition = element.get_composition()
    assert composition.NuEl == 0
    assert composition.FWt == pytest.approx(2.019000000000E-01)
    assert composition.FAt == pytest.approx(1.854557202066E-01)


def test_remove_all_elements(generate_sim_file):
    region = generate_sim_file.get_option_simulation_data().get_region_options().get_region(0)
    number_element = region.get_number_elements()
    assert number_element == 1

    generate_sim_file._remove_all_elements()
    number_element = region.get_number_elements()
    assert number_element == 0
