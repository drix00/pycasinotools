#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.simulation_results
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
import logging

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_int, read_double, read_bool
from casinotools.file_format.tags import find_tag
from casinotools.file_format.casino3.scan_point_results import ScanPointResults
from casinotools.file_format.casino3.energy_matrix import EnergyMatrix
from casinotools.file_format.casino3.diffused_energy_matrix import DiffusedEnergyMatrix

# Globals and constants variables.


class SimulationResults:
    def __init__(self):
        self._start_position = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._number_simulations = 0

    def read(self, file, options):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        self._number_simulations = read_int(file)

        for dummy in range(self._number_simulations):
            self._read_runtime_state(file)

            self._read_simulation_results(file, options)

            self._read_scan_points(file, options)

        return None

    def _read_runtime_state(self, file):
        tag_id = b"*RUNTIMESTATE%%"
        if find_tag(file, tag_id):
            self.version = read_int(file)

            if self.version == 20031202:
                self._read_simulation_state(file)

    def _read_simulation_state(self, file):
        tag_id = b"*SIMSTATE%%%%%%"
        if find_tag(file, tag_id):
            self._initial_energy_keV = read_double(file)
            self._rko_max = read_double(file)

    def _read_simulation_results(self, file, options):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_read_simulation_results",
                      file.tell())
        tag_id = b"*SIMRESULTS%%%%"
        if find_tag(file, tag_id):
            self._version_simulation_results = read_int(file)

            self._is_total_energy_density_saved = read_bool(file)
            if self._is_total_energy_density_saved:
                self._deposited_energy_density = EnergyMatrix(options, options.options_dist.DEpos_Center)
                self._deposited_energy_density.read(file)

            self._is_diffused_total_energy_density_saved = read_bool(file)
            if self._is_diffused_total_energy_density_saved:
                self._diffused_energy_density = DiffusedEnergyMatrix(options, options.options_dist.DEpos_Center)
                self._diffused_energy_density.read(file)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "_read_simulation_results",
                      file.tell())
        tag_id = b"*SIMRESULTSEND"
        if not find_tag(file, tag_id):
            raise IOError

    def _read_scan_points(self, file, options):
        self._number_scan_points = read_int(file)

        self._scan_points = []
        for dummy in range(self._number_scan_points):
            scan_point = ScanPointResults()
            scan_point.read(file, options)
            self._scan_points.append(scan_point)

    def get_scan_points_results(self):
        return self._scan_points

    def get_scan_points_results_from_index(self, index):
        return self._scan_points[index]

    def get_first_scan_point_results(self):
        return self.get_scan_points_results_from_index(0)

    def get_total_deposited_energies_ke_v(self):
        return self._deposited_energy_density
