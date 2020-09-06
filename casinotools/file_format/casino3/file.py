#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
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
import os.path
import struct
import logging

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.tags import limited_search_tag, TAG_LENGTH, add_tag
from casinotools.file_format.casino3.simulation_data import SimulationData
from casinotools.file_format.file_reader_writer_tools import read_int, _write_str_length, write_int, \
    _extract_version_string, write_line
from casinotools import get_current_module_path

# Globals and constants variables.
SIMULATION_CONFIGURATIONS = "sim"
SIMULATION_RESULTS = "cas"

SAVEFILE_HEADER_MAXCHAR = 1024

V30103040 = 30103040
V30103070 = 30103070
V30104060 = 30104060
V30107002 = 30107002


class SaveContent:
    def __init__(self):
        self.sample = False
        self.options = False
        self.scanPointPositions = False
        self.results = False
        self.runtime = False


class File:
    def __init__(self, filepath, is_modifiable=False):
        self._filepath = filepath
        self._is_modifiable = is_modifiable

        self._simulation_list = []
        self._save_content = SaveContent()
        self._file = None

        self._version = 0
        self._type = ""

        self.open()

    def _open(self, filepath):
        logging.debug("Filepath to be open in %s: %s", self.__class__.__name__, filepath)
        if self._is_modifiable:
            file = open(filepath, 'r+b')
        else:
            file = open(filepath, 'rb')
        return file

    def _open_writing(self, filepath):
        logging.debug("Filepath to be open in %s: %s", self.__class__.__name__, filepath)
        file = open(filepath, 'wb')
        return file

    def get_file_type(self):
        file_type = self._get_file_type_from_file_tag()

        self.reset()

        if file_type is None:
            file_type = self._get_file_type_from_extension()

        return file_type

    def _get_file_type_from_file_tag(self):
        extension = self._read_extension(self._file)

        if extension.lower() == SIMULATION_CONFIGURATIONS:
            return SIMULATION_CONFIGURATIONS
        elif extension.lower() == SIMULATION_RESULTS:
            return SIMULATION_RESULTS

    def _get_file_type_from_extension(self):
        extension = os.path.splitext(self._filepath)[-1]

        if extension.lower() == '.' + SIMULATION_CONFIGURATIONS:
            return SIMULATION_CONFIGURATIONS
        elif extension.lower() == '.' + SIMULATION_RESULTS:
            return SIMULATION_RESULTS

    def reset(self):
        self._file.seek(0)

    def get_filepath(self):
        return self._filepath

    def set_filepath(self, filepath):
        self._filepath = filepath

    def open(self):
        self._file = self._open(self._filepath)

        self._type = self.get_file_type()

        if self._type == SIMULATION_CONFIGURATIONS:
            self._open_sim()
        elif self._type == SIMULATION_RESULTS:
            self._open_cas()

    def _open_sim(self):
        self._save_content.sample = True
        self._save_content.options = True
        self._save_content.scanPointPositions = True

        self._read_casino_file(self._file)

    def _open_cas(self):
        self._save_content.sample = True
        self._save_content.options = True
        self._save_content.scanPointPositions = True
        self._save_content.results = True

        self._read_casino_file(self._file)

    def _read_casino_file(self, file):
        self._fileVersion = self._extract_file_version(file)

        self._read_with_file_version(file, self._fileVersion)

    @staticmethod
    def _extract_file_version(file):
        if limited_search_tag(file, b"V3.1.3.4", SAVEFILE_HEADER_MAXCHAR, TAG_LENGTH):
            return V30103040
        elif limited_search_tag(file, b"V3.1.3.7", SAVEFILE_HEADER_MAXCHAR, TAG_LENGTH):
            return V30103070
        elif limited_search_tag(file, b"%SAVE_HEADER%", SAVEFILE_HEADER_MAXCHAR, TAG_LENGTH):
            return V30104060

    def _read_with_file_version(self, file, file_version):
        if file_version >= V30104060:
            self.reset()
            self._version = self._read_version(file)

        self._numberSimulations = 1
        if self._version >= 30107002:
            self._numberSimulations = read_int(file)

        self._simulation_list = []
        for i in range(self._numberSimulations):
            logging.debug("Read simulation %i", i)
            simulation = self._read_one_simulation(file)
            self._simulation_list.append(simulation)

    def _read_one_simulation(self, file):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_read_one_simulation",
                      file.tell())
        simulation_data = SimulationData()

        if self._save_content.sample:
            simulation_data.read_sample(file)

        if self._save_content.options:
            simulation_data.read_options(file)

        if self._save_content.scanPointPositions:
            simulation_data.read_scan_point_positions(file)

        if self._save_content.results:
            simulation_data.read_results(file)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "_read_one_simulation",
                      file.tell())
        return simulation_data

    def open_file(self):
        if self._file.closed:
            self._file = open(self._filepath, 'rb')

    def close_file(self):
        if self._file is not None:
            self._file.close()

    @staticmethod
    def _read_extension(file):
        logging.debug("File position: %i", file.tell())
        extension = ""

        tag_id = b"ext="
        if limited_search_tag(file, tag_id, SAVEFILE_HEADER_MAXCHAR, TAG_LENGTH):
            logging.debug("File position: %i", file.tell())
            value_format = "3s"
            size = struct.calcsize(value_format)
            buffer = file.read(size)
            items = struct.unpack_from(value_format, buffer)
            extension = items[0].decode('ascii')

        return extension

    def _read_version(self, file):
        version = 0

        tag_id = b"%SAVE_HEADER%"
        if limited_search_tag(file, tag_id, SAVEFILE_HEADER_MAXCHAR, TAG_LENGTH):
            version = read_int(file)

        return version

    def save(self, filepath):
        file = self._open_writing(filepath)
        self.write(file)

    def write(self, file):
        self._write_sim(file)

    def _write_sim(self, file):
        self._save_content.sample = True
        self._save_content.options = True
        self._save_content.scanPointPositions = True

        self._write_casino_file(file)

    def _write_casino_file(self, file):
        self._write_extension(file, SIMULATION_CONFIGURATIONS)
        self._write_version(file, V30107002)
        self._write_number_simulations(file)

        for simulationData in self._simulation_list:
            self._write_one_simulation(file, simulationData)

    def _write_extension(self, file, extension):
        add_tag(file, "ext=")
        size = len(extension)
        _write_str_length(file, extension, size)

    def _write_version(self, file, version):
        add_tag(file, "%SAVE_HEADER%")
        write_int(file, version)

    def _write_number_simulations(self, file):
        assert self._numberSimulations == 1
        assert self._numberSimulations == len(self._simulation_list)

        write_int(file, self._numberSimulations)

    def _write_one_simulation(self, file, simulation_data):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_write_one_simulation",
                      file.tell())

        write_int(file, V30107002)

        if self._save_content.sample:
            simulation_data.write_sample(file)

        if self._save_content.options:
            simulation_data.write_options(file)

        if self._save_content.scanPointPositions:
            simulation_data.write_scan_point_positions(file)

        if self._save_content.results:
            simulation_data.write_results(file)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "_write_one_simulation",
                      file.tell())

    def get_number_simulations(self):
        return self._numberSimulations

    def get_simulations(self):
        return self._simulation_list

    def get_first_simulation(self):
        return self._simulation_list[0]

    def get_options(self):
        return self._simulation_list[0].get_options()

    def get_results(self):
        return self._simulation_list[0].get_result_list()

    def get_scan_point_results(self):
        return self._simulation_list[0].get_result_list().get_scan_points_results()

    def get_first_sphere_shape(self):
        sample = self._simulation_list[0].get_sample()
        first_sphere_shape = sample.get_first_sphere_shape()
        return first_sphere_shape

    def get_all_shapes(self):
        sample = self._simulation_list[0].get_sample()
        shapes = sample.get_shapes()
        return shapes

    def get_all_regions(self):
        sample = self._simulation_list[0].get_sample()
        regions = sample.get_regions()
        return regions

    def get_version(self):
        if self._version is None:
            return self._fileVersion
        else:
            return self._version

    def export(self, export_file):
        self._export_filename(export_file)
        self._export_file_type(export_file)
        self._export_file_version(export_file)

        self._export_header(export_file)
        self._export_number_simulations(export_file)
        self._export_simulations(export_file)

    def _export_filename(self, export_file):
        filename = os.path.basename(self._filepath)
        line = "Filename: {}".format(filename)
        write_line(export_file, line)

        line = "Filepath: {}".format(self._filepath)
        write_line(export_file, line)

    def _export_file_type(self, export_file):
        line = "File shape_type: {}".format(self._type)
        write_line(export_file, line)

    def _export_file_version(self, export_file):
        version = self.get_version()
        version_string = _extract_version_string(version)
        line = "File version: {} ({:d})".format(version_string, version)
        write_line(export_file, line)

    def _export_header(self, export_file):
        line = "-"*80
        write_line(export_file, line)

        line = "{}".format("Simulations")
        write_line(export_file, line)

        line = "-"*40
        write_line(export_file, line)

    def _export_number_simulations(self, export_file):
        line = "Number of simulations: {}".format(self._numberSimulations)
        write_line(export_file, line)

    def _export_simulations(self, export_file):
        simulation_id = 0
        for simulation in self._simulation_list:
            simulation_id += 1
            line = "Simulation: {:d}".format(simulation_id)
            write_line(export_file, line)

            simulation.export(export_file)


def _run():
    from pkg_resources import resource_filename  # @UnresolvedImport
    filepath_cas = get_current_module_path(__file__, "../../test_data/casino3.x/v3.1/v3.1.7.2/WaterAuTop_wSE.cas")

    file = File(filepath_cas)
    print("File name: {}".format(file._file.name))
    print("File descriptor: {:d}".format(file._file.fileno()))
    print("File shape_type: {}".format(file.get_file_type()))
    print("File version: {:d}".format(file._version))
    print("Number of simualtions: {:d}".format(file._numberSimulations))
    scan_point_results = file.get_results().get_scan_points_results_from_index(0)
    print("Number of saved trajectories: {:d}".format(scan_point_results.get_number_saved_trajectories()))
    first_trajectory = scan_point_results.get_saved_trajectory(0)
    number_events = first_trajectory.get_number_scattering_events()
    print("Number of collisions in first saved trajectory: {:d}".format(number_events))
    scattering_event = first_trajectory.get_scattering_event(-1)
    print("Last collision shape_type: {}".format(scattering_event.get_collision_type()))
    file.close_file()


def run_profile():
    import cProfile
    cProfile.run('_run()', 'Casino3.x_File.prof')


def run_debug():
    logging.getLogger().setLevel(logging.DEBUG)
    _run()


if __name__ == '__main__':  # pragma: no cover
    run_profile()
