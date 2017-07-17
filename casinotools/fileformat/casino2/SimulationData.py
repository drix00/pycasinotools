#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.SimulationData

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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.SimulationOptions as SimulationOptions
import casinotools.fileformat.casino2.RegionOptions as RegionOptions
import casinotools.fileformat.casino2.TrajectoriesData as TrajectoriesData
import casinotools.fileformat.casino2.SimulationResults as SimulationResults

from casinotools.fileformat.casino2.Element import \
    LINE_K, LINE_L, LINE_M, GENERATED, EMITTED  # @UnusedImport

from casinotools.fileformat.casino2.line import ATOMLINE_KA1, ATOMLINE_KA2, ATOMLINE_KB1, ATOMLINE_KB2, ATOMLINE_LA, \
    ATOMLINE_LB1, ATOMLINE_LB2, ATOMLINE_LG, ATOMLINE_MA

from casinotools.fileformat.casino2.Version import CURRENT_VERSION

# Globals and constants variables.
HEADER = b"WinCasino Simulation File"
TAG_VERSION = b"*VERSION%%%%%%%"
TAG_STATUS = b"*STATUS%%%%%%%%"
TAG_SAVE_SETUP = b"*SAVESETUP%%%%%"


class SimulationData(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, is_skip_reading_data=False):
        self._is_skip_reading_data = is_skip_reading_data

        self._header = HEADER
        self._version = CURRENT_VERSION
        self._status = None

        self._save_simulations = None
        self._save_regions = None
        self._save_trajectories = None
        self._save_distributions = None

        self._simulation_options = None
        self._region_options = None

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())
        self._header = self.readStrLength(file, 26)

        logging.debug("File pos: %i", file.tell())
        tag_id = TAG_VERSION
        if self.findTag(file, tag_id):
            logging.debug("File pos: %i", file.tell())
            self._version = self.readInt(file)

        tag_id = TAG_STATUS
        if self.findTag(file, tag_id):
            self._status = self.readStrLength(file, 1)

        tag_id = TAG_SAVE_SETUP
        if self.findTag(file, tag_id):
            self._save_simulations = self.readInt(file)
            self._save_regions = self.readInt(file)
            self._save_trajectories = self.readInt(file)
            self._save_distributions = self.readInt(file)

        if self._save_simulations:
            self._read_simulation_options(file)

        if self._save_regions:
            self._read_region_options(file)

        if self._save_regions and self._save_trajectories:
            self._read_trajectories(file)

        if self._save_distributions:
            self._read_simulation_results(file)

    def _read_simulation_options(self, file):
        self._simulation_options = SimulationOptions.SimulationOptions()
        self._simulation_options.read(file, self._version)

    def _read_region_options(self, file):
        if self._simulation_options.FEmissionRX:
            self._region_options = RegionOptions.RegionOptions(self._simulation_options.NbreCoucheRX)
        else:
            self._region_options = RegionOptions.RegionOptions(0)

        self._region_options.read(file, self._version)

    def _read_trajectories(self, file):
        self._trajectoriesData = TrajectoriesData.TrajectoriesData(self._is_skip_reading_data)
        self._trajectoriesData.read(file)

    def _read_simulation_results(self, file):
        self._simulationResults = SimulationResults.SimulationResults(self._is_skip_reading_data)
        self._simulationResults.read(file, self._simulation_options, self._version)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        self.writeStrLength(file, self._header, 26)

        tag_id = TAG_VERSION
        self.addTagOld(file, tag_id)
        self.writeInt(file, self._version)

        tag_id = TAG_STATUS
        self.addTagOld(file, tag_id)
        self.writeStrLength(file, self._status, 1)

        tag_id = TAG_SAVE_SETUP
        self.addTagOld(file, tag_id)
        self.writeInt(file, self._save_simulations)
        self.writeInt(file, self._save_regions)
        self.writeInt(file, self._save_trajectories)
        self.writeInt(file, self._save_distributions)

        if self._save_simulations:
            self._write_simulation_options(file)

        if self._save_regions:
            self._write_region_options(file)

        if self._save_regions and self._save_trajectories:
            self._write_trajectories(file)

        if self._save_distributions:
            self._write_simulation_results(file)

    def _write_simulation_options(self, file):
        self._simulation_options.write(file)

    def _write_region_options(self, file):
        self._region_options.write(file)

    def _write_trajectories(self, file):
        raise NotImplementedError

    def _write_simulation_results(self, file):
        raise NotImplementedError

    def getVersion(self):
        return self._version

    def getSimulationOptions(self):
        return self._simulation_options

    def setSimulationOptions(self, simulation_options):
        self._simulation_options = simulation_options

    def getRegionOptions(self):
        return self._region_options

    def setRegionsOptions(self, region_options):
        self._region_options = region_options

    def getSimulationResults(self):
        return self._simulationResults

    def getTrajectoriesData(self):
        return self._trajectoriesData

    def getTotalXrayIntensities(self):
        """
        Returns a :class:`dict` with the intensities (generated and emitted) of
        all the lines and elements in the simulation.
        The dictionary is structured as followed: atomic number, line,
        :const:`EMITTED` or :const:`GENERATED`.
        The lines can either be :const:`LINE_K`, :const:`LINE_L`, :const:`LINE_M`.

        :rtype: class:`dict`
        """
        intensities = {}

        for region in self.getRegionOptions().getRegions():
            for element in region.getElements():
                z = element.getAtomicNumber()
                delta = element.getTotalXrayIntensities()

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
        all the lines and elements in the simulation in photon / (electron * steradian).
        The dictionary is structured as followed: atomic number, line.
        The lines can either be :const:`ATOMLINE_KA1`, :const:`ATOMLINE_KA2`, :const:`ATOMLINE_KB1`,
        :const:`ATOMLINE_KB2`, :const:`ATOMLINE_LA`, :const:`ATOMLINE_LB1`, :const:`ATOMLINE_LB2`,
        :const:`ATOMLINE_LG`, :const:`ATOMLINE_MA`.

        :rtype: class:`dict`
        """
        intensities = {}

        for region in self.getRegionOptions().getRegions():
            for element in region.getElements():
                z = element.getAtomicNumber()
                delta = element.get_total_xray_intensities_1_esr()

                intensities.setdefault(z, {})

                for line in delta.keys():
                    if line in intensities[z]:
                        intensities[z][line] += delta[line]
                    else:
                        intensities[z][line] = delta[line]

        return intensities

