#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.simulation_data

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read one simulation data from a CASINO v2 file.
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
import logging

# Third party modules.

# Local modules.
from casinotools.file_format.file_reader_writer_tools import _read_str_length, read_int, _write_str_length, \
    write_int
from casinotools.file_format.tags import add_tag_old, find_tag
from casinotools.file_format.casino2.simulation_options import SimulationOptions
from casinotools.file_format.casino2.region_options import RegionOptions
from casinotools.file_format.casino2.trajectories_data import TrajectoriesData
from casinotools.file_format.casino2.simulation_results import SimulationResults
from casinotools.file_format.casino2.element import GENERATED, EMITTED
from casinotools.file_format.casino2.version import CURRENT_VERSION

# Globals and constants variables.
HEADER = b"WinCasino Simulation File"
TAG_VERSION = b"*VERSION%%%%%%%"
TAG_STATUS = b"*STATUS%%%%%%%%"
TAG_SAVE_SETUP = b"*SAVESETUP%%%%%"


class SimulationData:
    def __init__(self, is_skip_reading_data=False):
        self._is_skip_reading_data = is_skip_reading_data

        self.header = HEADER
        self.version = CURRENT_VERSION
        self.status = None

        self.save_simulations = None
        self.save_regions = None
        self.save_trajectories = None
        self.save_distributions = None

        self.simulation_options = None
        self.region_options = None

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())
        self.header = _read_str_length(file, 26)

        logging.debug("File pos: %i", file.tell())
        tag_id = TAG_VERSION
        if find_tag(file, tag_id):
            logging.debug("File pos: %i", file.tell())
            self.version = read_int(file)
        else:
            return

        tag_id = TAG_STATUS
        if find_tag(file, tag_id):
            self.status = _read_str_length(file, 1)

        tag_id = TAG_SAVE_SETUP
        if find_tag(file, tag_id):
            self.save_simulations = read_int(file)
            self.save_regions = read_int(file)
            self.save_trajectories = read_int(file)
            self.save_distributions = read_int(file)

        if self.save_simulations:
            self._read_simulation_options(file)

        if self.save_regions:
            self._read_region_options(file)

        if self.save_regions and self.save_trajectories:
            self._read_trajectories(file)

        if self.save_distributions:
            self._read_simulation_results(file)

    def _read_simulation_options(self, file):
        self.simulation_options = SimulationOptions()
        self.simulation_options.read(file, self.version)

    def _read_region_options(self, file):
        if self.simulation_options.FEmissionRX:
            self.region_options = RegionOptions(self.simulation_options.NbreCoucheRX)
        else:
            self.region_options = RegionOptions(0)

        self.region_options.read(file, self.version)

    def _read_trajectories(self, file):
        self._trajectoriesData = TrajectoriesData(self._is_skip_reading_data)
        self._trajectoriesData.read(file)

    def _read_simulation_results(self, file):
        self._simulationResults = SimulationResults(self._is_skip_reading_data)
        self._simulationResults.read(file, self.simulation_options, self.version)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        _write_str_length(file, self.header, 26)

        tag_id = TAG_VERSION
        add_tag_old(file, tag_id)
        write_int(file, self.version)

        tag_id = TAG_STATUS
        add_tag_old(file, tag_id)
        _write_str_length(file, self.status, 1)

        tag_id = TAG_SAVE_SETUP
        add_tag_old(file, tag_id)
        write_int(file, self.save_simulations)
        write_int(file, self.save_regions)
        write_int(file, self.save_trajectories)
        write_int(file, self.save_distributions)

        if self.save_simulations:
            self._write_simulation_options(file)

        if self.save_regions:
            self._write_region_options(file)

        if self.save_regions and self.save_trajectories:
            self._write_trajectories(file)

        if self.save_distributions:
            self._write_simulation_results(file)

    def _write_simulation_options(self, file):
        self.simulation_options.write(file)

    def _write_region_options(self, file):
        self.region_options.write(file)

    def _write_trajectories(self, file):
        raise NotImplementedError

    def _write_simulation_results(self, file):
        raise NotImplementedError

    def get_version(self):
        return self.version

    def get_simulation_options(self):
        return self.simulation_options

    def set_simulation_options(self, simulation_options):
        self.simulation_options = simulation_options

    def get_region_options(self):
        return self.region_options

    def set_regions_options(self, region_options):
        self.region_options = region_options

    def get_simulation_results(self):
        return self._simulationResults

    def get_trajectories_data(self):
        return self._trajectoriesData

    def get_total_xray_intensities(self):
        """
        Returns a :class:`dict` with the intensities (generated and emitted) of
        all the lines and elements in the simulation.
        The dictionary is structured as followed: atomic number, line,
        :const:`EMITTED` or :const:`GENERATED`.
        The lines can either be :const:`LINE_K`, :const:`LINE_L`, :const:`LINE_M`.

        :rtype: class:`dict`
        """
        intensities = {}

        for region in self.get_region_options().get_regions():
            for element in region.get_elements():
                z = element.get_atomic_number()
                delta = element.get_total_xray_intensities()

                intensities.setdefault(z, {})

                for line in delta.keys():
                    if line in intensities[z]:
                        intensities[z][line][GENERATED] += delta[line][GENERATED]
                        intensities[z][line][EMITTED] += delta[line][EMITTED]
                    else:
                        intensities[z].setdefault(line, {})
                        intensities[z][line][GENERATED] = delta[line][GENERATED]
                        intensities[z][line][EMITTED] = delta[line][EMITTED]

        return intensities

    def get_total_xray_intensities_1_esr(self):
        """
        Returns a :class:`dict` with the intensities (emitted) of
        all the lines and elements in the simulation in photon / (electron * steradians).
        The dictionary is structured as followed: atomic number, line.
        The lines can either be :const:`ATOM_LINE_KA1`, :const:`ATOM_LINE_KA2`, :const:`ATOM_LINE_KB1`,
        :const:`ATOM_LINE_KB2`, :const:`ATOM_LINE_LA`, :const:`ATOM_LINE_LB1`, :const:`ATOM_LINE_LB2`,
        :const:`ATOM_LINE_LG`, :const:`ATOM_LINE_MA`.

        :rtype: class:`dict`
        """
        intensities = {}

        for region in self.get_region_options().get_regions():
            for element in region.get_elements():
                z = element.get_atomic_number()
                delta = element.get_total_xray_intensities_1_esr()

                intensities.setdefault(z, {})

                for line in delta.keys():
                    if line in intensities[z]:
                        intensities[z][line] += delta[line]
                    else:
                        intensities[z][line] = delta[line]

        return intensities
