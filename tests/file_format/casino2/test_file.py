#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_file

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.file_format.casino2.file`.
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
from casinotools.file_format.casino2.file import File
from casinotools.file_format.casino2.element import LINE_K, GENERATED, EMITTED
from casinotools.utilities.path import is_bad_file
from casinotools.file_format.casino2.version import VERSION_2_45, VERSION_2_50, VERSION_2_51, VERSION_2_42, \
    VERSION_2_46, VERSION_26

# if os.path.isfile(self.filepathWrite):
#     os.remove(self.filepathWrite)


def test_read(filepath_sim_2_45, filepath_cas_26):
    if is_bad_file(filepath_sim_2_45):
        pytest.skip()
    file = File()
    file.read_from_filepath(filepath_sim_2_45)
    assert file._filepath == filepath_sim_2_45
    assert file._numberSimulations == 0

    file = File()
    file.read_from_filepath(filepath_cas_26)
    assert file._filepath == filepath_cas_26
    assert file._numberSimulations == 1

    assert len(file._resultSimulationDataList) == 1


def test_read_string_io(filepath_sim_2_45, filepath_cas_26):
    # sim
    if is_bad_file(filepath_sim_2_45):
        pytest.skip()
    f = open(filepath_sim_2_45, 'rb')
    buf = BytesIO(f.read())
    f.close()

    file = File()
    file.read_from_file_object(buf)
    assert file._numberSimulations == 0

    # cas
    f = open(filepath_cas_26, 'rb')
    buf = BytesIO(f.read())
    f.close()

    file = File()
    file.read_from_file_object(buf)
    assert file._numberSimulations == 1

    assert len(file._resultSimulationDataList) == 1


def test_is_simulation_filepath(filepath_sim_2_45, filepath_cas_2_45):
    file = File()

    assert file._is_simulation_filepath(filepath_sim_2_45) is True
    assert file._is_simulation_filepath(filepath_cas_2_45) is False


def test_write(filepath_std, filepath_write):
    if is_bad_file(filepath_std):
        pytest.skip()

    file = File()
    option_simulation_data = _get_option_simulation_data(filepath_std)
    file.set_option_simulation_data(option_simulation_data)
    file.write(filepath_write)

    with open(filepath_std, 'rb') as fp:
        data_ref = fp.read()
    with open(filepath_write, 'rb') as fp:
        data = fp.read()
    index = 0
    for charRef, char in zip(data_ref, data):
        assert char == charRef, index
        index += 1

    assert len(data) == len(data_ref)

    import filecmp
    assert filecmp.cmp(filepath_std, filepath_write, shallow=True) is True


def _get_option_simulation_data(filepath_std):
    file = File()
    file.read_from_filepath(filepath_std)

    return file.get_option_simulation_data()


def test_skip_reading_data(filepath_cas_26):
    if is_bad_file(filepath_cas_26):
        pytest.skip()

    file = File()
    file.read_from_filepath(filepath_cas_26, is_skip_reading_data=False)

    trajectories_data = file.get_results_first_simulation().get_trajectories_data()
    assert trajectories_data._number_trajectories == 221
    assert trajectories_data._trajectories[0].NbElec == 89
    assert len(trajectories_data._trajectories[0]._scatteringEvents) == 89

    event = trajectories_data._trajectories[0]._scatteringEvents[0]
    assert event.X == pytest.approx(-2.903983831406E+00)
    assert event.Y == pytest.approx(-3.020418643951E+00)
    assert event.z == pytest.approx(0.0)
    assert event.E == pytest.approx(4.000000000000E+00)
    assert event.Intersect == 0
    assert event.id == 0

    file = File()
    file.read_from_filepath(filepath_cas_26, is_skip_reading_data=True)

    trajectories_data = file.get_results_first_simulation().get_trajectories_data()
    assert trajectories_data._number_trajectories == 221
    assert trajectories_data._trajectories[0].NbElec == 89
    assert len(trajectories_data._trajectories[0]._scatteringEvents) == 0

    simulation_results = file.get_results_first_simulation().get_simulation_results()

    assert simulation_results.BE_Intensity_Size == 1
    assert simulation_results.BE_Intensity[0] == 3.950000000000E-02

    element = simulation_results._elementIntensityList[0]
    assert element.name == "B"
    assert element.IntensityK[0] == pytest.approx(3.444919288026E+02)

    element = simulation_results._elementIntensityList[1]
    assert element.name == "C"
    assert element.IntensityK[0] == pytest.approx(4.687551040349E+01)

    assert simulation_results.NbPointDZMax == 1000
    assert simulation_results.NbPointDENR == 500
    assert simulation_results.NbPointDENT == 500
    assert simulation_results.NbPointDRSR == 500
    # assert simulationResults.NbPointDNCR == 0
    assert simulation_results.NbPointDEpos_X == 50
    assert simulation_results.NbPointDEpos_Y == 50
    assert simulation_results.NbPointDEpos_Z == 50
    assert simulation_results.DEpos_maxE == pytest.approx(1.608165461510E-02)
    assert simulation_results.NbPointDBANG == 91
    assert simulation_results.NbPointDAngleVSEnergie == 91


def test_read_v242(filepath_sim_v242, filepath_cas_v242):
    if is_bad_file(filepath_sim_v242):
        pytest.skip()
    if is_bad_file(filepath_cas_v242):
        pytest.skip()

    # .sim
    file = File()
    file.read_from_filepath(filepath_sim_v242)
    assert file._filepath == filepath_sim_v242
    assert file._numberSimulations == 0

    option_simulation_data = file.get_option_simulation_data()
    version = option_simulation_data.get_version()
    assert version == VERSION_2_42

    simulation_options = option_simulation_data.get_simulation_options()

    number_electrons = simulation_options.get_number_electrons()
    assert number_electrons == 10000

    incident_energy_keV = simulation_options.get_incident_energy_keV()
    assert incident_energy_keV == pytest.approx(3.0)

    toa_deg = simulation_options.get_toa_deg()
    assert toa_deg == pytest.approx(40.0)

    number_xray_layers = simulation_options.get_number_x_ray_layers()
    assert number_xray_layers == 500

    # .cas
    file = File()
    file.read_from_filepath(filepath_cas_v242)
    assert file._filepath == filepath_cas_v242
    assert file._numberSimulations == 1

    assert len(file._resultSimulationDataList) == 1

    option_simulation_data = file.get_option_simulation_data()
    version = option_simulation_data.get_version()
    assert version == VERSION_2_42

    simulation_options = option_simulation_data.get_simulation_options()

    number_electrons = simulation_options.get_number_electrons()
    assert number_electrons == 10000

    incident_energy_keV = simulation_options.get_incident_energy_keV()
    assert incident_energy_keV == pytest.approx(3.0)

    toa_deg = simulation_options.get_toa_deg()
    assert toa_deg == pytest.approx(40.0)

    number_xray_layers = simulation_options.get_number_x_ray_layers()
    assert number_xray_layers == 500

    result_simulation_data = file.get_results_simulation(0)
    region_options = result_simulation_data.get_region_options()
    region = region_options.get_region(0)
    element = region.get_element(0)
    intensities = element.get_total_xray_intensities()

    assert intensities[LINE_K][GENERATED] == pytest.approx(2164.75)
    assert intensities[LINE_K][EMITTED] == pytest.approx(415.81, 2)

    atomic_number = element.get_atomic_number()
    assert atomic_number == 5


def test_read_sim_v250(filepath_sim_v250):
    if is_bad_file(filepath_sim_v250):
        pytest.skip()

    # .sim
    file = File()
    file.read_from_filepath(filepath_sim_v250)
    assert file._filepath == filepath_sim_v250
    assert file._numberSimulations == 0

    option_simulation_data = file.get_option_simulation_data()
    version = option_simulation_data.get_version()
    assert version == VERSION_2_50

    simulation_options = option_simulation_data.get_simulation_options()

    number_electrons = simulation_options.get_number_electrons()
    assert number_electrons == 10000

    incident_energy_keV = simulation_options.get_incident_energy_keV()
    assert incident_energy_keV == pytest.approx(2.0)

    toa_deg = simulation_options.get_toa_deg()
    assert toa_deg == pytest.approx(40.0)

    number_xray_layers = simulation_options.get_number_x_ray_layers()
    assert number_xray_layers == 500


def test_read_cas_v26(filepath_cas_26):
    if is_bad_file(filepath_cas_26):
        pytest.skip()

    # .cas
    file = File()
    file.read_from_filepath(filepath_cas_26)
    assert file._filepath == filepath_cas_26
    assert file._numberSimulations == 1

    assert len(file._resultSimulationDataList) == 1

    option_simulation_data = file.get_option_simulation_data()
    version = option_simulation_data.get_version()
    assert version == VERSION_26

    simulation_options = option_simulation_data.get_simulation_options()

    number_electrons = simulation_options.get_number_electrons()
    assert number_electrons == 10000

    incident_energy_keV = simulation_options.get_incident_energy_keV()
    assert incident_energy_keV == pytest.approx(4.0)

    toa_deg = simulation_options.get_toa_deg()
    assert toa_deg == pytest.approx(40.0)

    number_xray_layers = simulation_options.get_number_x_ray_layers()
    assert number_xray_layers == 500

    result_simulation_data = file.get_results_simulation(0)
    region_options = result_simulation_data.get_region_options()
    region = region_options.get_region(0)
    element = region.get_element(0)
    intensities = element.get_total_xray_intensities()

    assert intensities[LINE_K][GENERATED] == pytest.approx(2538.630615234375)
    assert intensities[LINE_K][EMITTED] == pytest.approx(344.491943359375)

    atomic_number = element.get_atomic_number()
    assert atomic_number == 5


def test_problem_sim_v250(filepath_problem_sim_v250, filepath_good_sim_v251):
    if is_bad_file(filepath_problem_sim_v250):
        pytest.skip()

    # .sim
    file = File()
    file.read_from_filepath(filepath_problem_sim_v250)
    assert file._filepath == filepath_problem_sim_v250
    assert file._numberSimulations == 0

    option_simulation_data = file.get_option_simulation_data()
    version = option_simulation_data.get_version()
    assert version == VERSION_2_50

    simulation_options = option_simulation_data.get_simulation_options()

    number_electrons = simulation_options.get_number_electrons()
    assert number_electrons == 200

    incident_energy_keV = simulation_options.get_incident_energy_keV()
    assert incident_energy_keV == pytest.approx(1.0)

    toa_deg = simulation_options.get_toa_deg()
    assert toa_deg == pytest.approx(40.0)

    number_xray_layers = simulation_options.get_number_x_ray_layers()
    assert number_xray_layers == 500

    if is_bad_file(filepath_good_sim_v251):
        pytest.skip()

    # .sim
    file = File()
    file.read_from_filepath(filepath_good_sim_v251)
    assert file._filepath == filepath_good_sim_v251
    assert file._numberSimulations == 0

    option_simulation_data = file.get_option_simulation_data()
    version = option_simulation_data.get_version()
    assert version == VERSION_2_51

    simulation_options = option_simulation_data.get_simulation_options()

    number_electrons = simulation_options.get_number_electrons()
    assert number_electrons == 200

    incident_energy_keV = simulation_options.get_incident_energy_keV()
    assert incident_energy_keV == pytest.approx(1.0)

    toa_deg = simulation_options.get_toa_deg()
    assert toa_deg == pytest.approx(40.0)

    number_xray_layers = simulation_options.get_number_x_ray_layers()
    assert number_xray_layers == 500


def test_extract_version(filepath_sim_2_45, filepath_cas_2_45, filepath_sim_26, filepath_cas_26, filepath_std, filepath_sim_v242, filepath_cas_v242,
                         filepath_cas_nicr, filepath_sim_v250, filepath_cas_v250, filepath_problem_sim_v250,
                         filepath_problem_pymontecarlo_sim_v250, filepath_good_sim_v251):
    """
    Test extract_version method.
    """
    if is_bad_file(filepath_sim_2_45):
        pytest.skip()

    file_paths = [(filepath_sim_2_45, VERSION_2_46),
                  (filepath_cas_2_45, VERSION_2_46),
                  (filepath_sim_26, VERSION_26),
                  (filepath_cas_26, VERSION_26),
                  (filepath_std, VERSION_2_50),
                  (filepath_sim_v242, VERSION_2_42),
                  (filepath_cas_v242, VERSION_2_42),
                  (filepath_cas_nicr, VERSION_2_46),
                  (filepath_sim_v250, VERSION_2_50),
                  (filepath_cas_v250, VERSION_2_50),
                  (filepath_problem_sim_v250, VERSION_2_50),
                  (filepath_problem_pymontecarlo_sim_v250, VERSION_2_50),
                  (filepath_good_sim_v251, VERSION_2_51)]

    for file_path, version_ref in file_paths:
        casino_file = File()
        version = casino_file.extract_version(file_path)
        assert version == version_ref, file_path
