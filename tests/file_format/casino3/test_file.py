#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.file` module.
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
from casinotools.file_format.casino3.file import File, SIMULATION_CONFIGURATIONS, SIMULATION_RESULTS
from casinotools.file_format.casino3.file import modify_energy, modify_cross_section
from casinotools.utilities.path import is_bad_file
from casinotools.file_format.casino3.options_physic import CrossSection

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


def test_init(filepath_sim):
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()

    casino_file = File(filepath_sim)

    assert casino_file.get_filepath() == filepath_sim


def test_get_file_type(filepath_sim):
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    casino_file = File(filepath_sim)

    file_type = casino_file.get_file_type()
    assert file_type == SIMULATION_CONFIGURATIONS

#        casino_file = File.File(self.filepathCas)
#        shape_type = casino_file.get_file_type()
#        assert File.SIMULATION_RESULTS == shape_type


def test__read_extension(filepath_sim, filepath_cas):
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    casino_file = File(filepath_sim)
    file = casino_file._open(filepath_sim)
    extension = casino_file._read_extension(file)
    assert extension == SIMULATION_CONFIGURATIONS

    file = open(filepath_cas, 'rb')
    extension = casino_file._read_extension(file)
    assert extension == SIMULATION_RESULTS


def test__read_version(filepath_sim):
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    casino_file = File(filepath_sim)
    file = casino_file._open(filepath_sim)
    version = casino_file._read_version(file)
    assert version == 30107002


def test_open(filepath_sim):
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    casino_file = File(filepath_sim)
    casino_file.open()

    assert casino_file.version == 30107002
    assert casino_file.number_simulations == 1


def test_read_cas_file(filepath_cas):
    if is_bad_file(filepath_cas):  # pragma: no cover
        pytest.skip()
    casino_file = File(filepath_cas)
    casino_file.open()

    assert casino_file.version == 30107002
    assert casino_file.number_simulations == 1


def test_modified_energy(file_path_sim_tmp_modify_option):
    energy_keV_ref = 3.5

    sim_file = File(file_path_sim_tmp_modify_option, is_modifiable=True)
    options_microscope = sim_file.get_options().options_microscope

    assert options_microscope.KEV_End == pytest.approx(0.0)
    assert options_microscope.KEV_Start == pytest.approx(1.0)
    assert options_microscope.KEV_Step == pytest.approx(1.0)
    assert options_microscope.multiple_scan_energy == 0

    options_microscope.KEV_Start = energy_keV_ref

    sim_file.modify()
    sim_file.close_file()

    sim_file = File(file_path_sim_tmp_modify_option)
    options_microscope = sim_file.get_options().options_microscope

    assert options_microscope.KEV_End == pytest.approx(0.0)
    assert options_microscope.KEV_Start == pytest.approx(energy_keV_ref)
    assert options_microscope.KEV_Step == pytest.approx(1.0)
    assert options_microscope.multiple_scan_energy == 0


def test_modified_energy_not_modifiable(file_path_sim_tmp_modify_option):
    energy_keV_ref = 3.5

    sim_file = File(file_path_sim_tmp_modify_option, is_modifiable=False)
    options_microscope = sim_file.get_options().options_microscope

    assert options_microscope.KEV_End == pytest.approx(0.0)
    assert options_microscope.KEV_Start == pytest.approx(1.0)
    assert options_microscope.KEV_Step == pytest.approx(1.0)
    assert options_microscope.multiple_scan_energy == 0

    options_microscope.KEV_Start = energy_keV_ref

    sim_file.modify()
    sim_file.close_file()

    sim_file = File(file_path_sim_tmp_modify_option)
    options_microscope = sim_file.get_options().options_microscope

    assert options_microscope.KEV_End == pytest.approx(0.0)
    assert options_microscope.KEV_Start != pytest.approx(energy_keV_ref)
    assert options_microscope.KEV_Start == pytest.approx(1.0)
    assert options_microscope.KEV_Step == pytest.approx(1.0)
    assert options_microscope.multiple_scan_energy == 0


def test_modify_energy(file_path_sim_tmp_modify_option):
    energy_keV_ref = 3.5
    modify_energy(file_path_sim_tmp_modify_option, energy_keV_ref)

    sim_file = File(file_path_sim_tmp_modify_option)
    options_microscope = sim_file.get_options().options_microscope

    assert options_microscope.KEV_End == pytest.approx(0.0)
    assert options_microscope.KEV_Start == pytest.approx(energy_keV_ref)
    assert options_microscope.KEV_Step == pytest.approx(1.0)
    assert options_microscope.multiple_scan_energy == 0


def test_modified_cross_section(file_path_sim_tmp_modify_option):
    total_cs_ref = CrossSection.RUTHERFORD.value
    partial_cs_ref = CrossSection.MOTT_FILE.value

    sim_file = File(file_path_sim_tmp_modify_option, is_modifiable=True)
    options_physic = sim_file.get_options().options_physic

    assert options_physic.FTotalCross == CrossSection.ELSEPA.value
    assert options_physic.FPartialCross == CrossSection.ELSEPA.value

    options_physic.FTotalCross = total_cs_ref
    options_physic.FPartialCross = partial_cs_ref

    sim_file.modify()
    sim_file.close_file()

    sim_file = File(file_path_sim_tmp_modify_option)
    options_physic = sim_file.get_options().options_physic

    assert options_physic.FTotalCross == total_cs_ref
    assert options_physic.FPartialCross == partial_cs_ref


def test_modified_cross_section_not_modifiable(file_path_sim_tmp_modify_option):
    total_cs_ref = CrossSection.RUTHERFORD.value
    partial_cs_ref = CrossSection.MOTT_FILE.value

    sim_file = File(file_path_sim_tmp_modify_option, is_modifiable=False)
    options_physic = sim_file.get_options().options_physic

    assert options_physic.FTotalCross == CrossSection.ELSEPA.value
    assert options_physic.FPartialCross == CrossSection.ELSEPA.value

    options_physic.FTotalCross = total_cs_ref
    options_physic.FPartialCross = partial_cs_ref

    sim_file.modify()
    sim_file.close_file()

    sim_file = File(file_path_sim_tmp_modify_option)
    options_physic = sim_file.get_options().options_physic

    assert options_physic.FTotalCross == CrossSection.ELSEPA.value
    assert options_physic.FTotalCross != total_cs_ref
    assert options_physic.FPartialCross == CrossSection.ELSEPA.value
    assert options_physic.FPartialCross != partial_cs_ref


def test_modify_cross_section(file_path_sim_tmp_modify_option):
    cs_ref = CrossSection.RUTHERFORD.value
    modify_cross_section(file_path_sim_tmp_modify_option, cs_ref)

    sim_file = File(file_path_sim_tmp_modify_option)
    options_physic = sim_file.get_options().options_physic

    assert options_physic.FTotalCross == cs_ref
    assert options_physic.FPartialCross == cs_ref
