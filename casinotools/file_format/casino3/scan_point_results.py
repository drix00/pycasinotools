#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
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
from casinotools.file_format.casino3.transmitted_angles import TransmittedAngles
from casinotools.file_format.casino3.region_intensity_info import RegionIntensityInfo
from casinotools.file_format.casino3.trajectory import Trajectory
from casinotools.file_format.casino3.graph_data import GraphData
from casinotools.file_format.casino3.energy_matrix import EnergyMatrix
from casinotools.file_format.casino3.diffused_energy_matrix import DiffusedEnergyMatrix
from casinotools.file_format.casino3.version import SIM_OPTIONS_VERSION_3_3_0_0, SIM_OPTIONS_VERSION_3_3_0_4
from casinotools.file_format.casino3.point_spread_function_matrix import PointSpreadFunctionMatrix

# Globals and constants variables.


class ScanPointResults:
    def __init__(self):
        self._version = 0

        self._x = 0.0
        self._y = 0.0
        self._z = 0.0

        self._initial_energy_keV = 0.0
        self._rko_max = 0.0
        self._rko_max_w = 0.0

        self._number_simulated_trajectories = 0
        self._being_processed = 0

        self._backscattered_coefficient = 0.0
        self._backscattered_detected_coefficient = 0.0
        self._secondary_coefficient = 0.0
        self._transmitted_coefficient = 0.0
        self._transmitted_detected_coefficient = 0.0
        self._number_backscattered_electrons = 0
        self._number_backscattered_electrons_detected = 0.0
        self._number_secondary_electrons = 0

        self._transmitted_angles = TransmittedAngles()

        self._number_results = 0
        self._region_intensity_infos = []

        self._is_dz_max = False
        self.dz_max = None

        self._isDZMaxRetro = False
        self.dzMaxRetro = None

        self._isDENR = False
        self.DENR = None

        self._isDENT = False
        self.DENT = None

        self._isDrasRetro = False
        self.DrasRetro = None

        self._isDrasRetroEnr = False
        self.DrasRetroEnr = None

        self.is_deposited_energy = False
        self.DEnergy_Density_Max_Energy = 0.0
        self.deposited_energy = None

        self._isDDiffusedEnergy_Density = False
        self._DDiffusedEnergy_Density = None

        self._isDbang = False
        self.Dbang = None

        self._isDEnBang = False
        self.DEnBang = None

        self._isPsf = False
        self._pointSpreadFunctionMatrix = None

        self._numberTrajectories = 0
        self._trajectories = []

    def read(self, file, options):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = b"*SCANPTRUNTIME%"
        if find_tag(file, tag_id):
            self._version = read_int(file)

            self._x = read_double(file)
            self._y = read_double(file)
            self._z = read_double(file)

            self._initial_energy_keV = read_double(file)
            self._rko_max = read_double(file)
            self._rko_max_w = read_double(file)

            self._number_simulated_trajectories = read_int(file)
            self._being_processed = read_int(file)

            self._backscattered_coefficient = read_double(file)
            self._backscattered_detected_coefficient = read_double(file)
            self._secondary_coefficient = read_double(file)
            self._transmitted_coefficient = read_double(file)
            self._transmitted_detected_coefficient = read_double(file)
            self._number_backscattered_electrons = read_int(file)
            self._number_backscattered_electrons_detected = read_double(file)
            self._number_secondary_electrons = read_int(file)

            self._transmitted_angles = TransmittedAngles()
            self._transmitted_angles.read(file)

            self._number_results = read_int(file)
            self._region_intensity_infos = []
            for dummy in range(self._number_results):
                region_intensity_info = RegionIntensityInfo()
                region_intensity_info.read(file)
                self._region_intensity_infos.append(region_intensity_info)

            self._is_dz_max = read_bool(file)
            if self._is_dz_max:
                self.dz_max = GraphData(file)

            self._isDZMaxRetro = read_bool(file)
            if self._isDZMaxRetro:
                self.dzMaxRetro = GraphData(file)

            self._isDENR = read_bool(file)
            if self._isDENR:
                self.DENR = GraphData(file)

            self._isDENT = read_bool(file)
            if self._isDENT:
                self.DENT = GraphData(file)

            self._isDrasRetro = read_bool(file)
            if self._isDrasRetro:
                self.DrasRetro = GraphData(file)

            self._isDrasRetroEnr = read_bool(file)
            if self._isDrasRetroEnr:
                self.DrasRetroEnr = GraphData(file)

            self.is_deposited_energy = read_bool(file)
            if self.is_deposited_energy:
                self.DEnergy_Density_Max_Energy = read_double(file)
                self.deposited_energy = EnergyMatrix(options, self.get_position())
                self.deposited_energy.read(file)

            self._isDDiffusedEnergy_Density = read_bool(file)
            if self._isDDiffusedEnergy_Density:
                self._DDiffusedEnergy_Density = DiffusedEnergyMatrix(options, self.get_position())
                self._DDiffusedEnergy_Density.read(file)

            self._isDbang = read_bool(file)
            if self._isDbang:
                self.Dbang = GraphData(file)

            self._isDEnBang = read_bool(file)
            if self._isDEnBang:
                self.DEnBang = GraphData(file)

            if SIM_OPTIONS_VERSION_3_3_0_0 <= self._version < SIM_OPTIONS_VERSION_3_3_0_4:
                self._isPsf = read_bool(file)
                if self._isPsf:
                    self._pointSpreadFunctionMatrix = PointSpreadFunctionMatrix(options, self.get_position())
                    self._pointSpreadFunctionMatrix.read(file)
                else:
                    self._pointSpreadFunctionMatrix = None
            else:
                self._isPsf = False

            self._numberTrajectories = read_int(file)
            self._trajectories = []
            for dummy in range(self._numberTrajectories):
                trajectory = Trajectory()
                trajectory.read(file)
                self._trajectories.append(trajectory)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", file.tell())

    def get_position(self):
        return self._x, self._y, self._z

    def get_transmitted_coefficient(self):
        return self._transmitted_coefficient

    def get_transmitted_detected_coefficient(self):
        return self._transmitted_detected_coefficient

    def get_transmitted_detected_electrons(self, beta_min=None, beta_max=None):
        if beta_min is None and beta_max is None:
            return self._transmitted_detected_coefficient * self._number_simulated_trajectories
        else:
            return self._transmitted_angles.get_transmitted_detected_electrons(beta_min, beta_max)

    def get_transmitted_angles(self):
        return self._transmitted_angles.get_angles()

    def get_transmitted_binned_angles(self):
        return self._transmitted_angles.get_binned_angles()

    def get_number_simulated_trajectories(self):
        return self._number_simulated_trajectories

    def get_initial_energy_keV(self):
        return self._initial_energy_keV

    def get_backscattered_coefficient(self):
        return self._backscattered_coefficient

    def get_backscattered_detected_coefficient(self):
        return self._backscattered_detected_coefficient

    def get_number_backscattered_detected_electrons(self):
        return self._number_backscattered_electrons_detected

    def get_number_backscattered_electrons(self):
        return self._number_backscattered_electrons

    def get_secondary_electron_coefficient(self):
        return self._secondary_coefficient

    def get_deposited_energies_keV(self, region_info_index):
        try:
            region_intensity_info = self._region_intensity_infos[region_info_index]
            return region_intensity_info.get_energy_intensity()
        except IndexError as message:
            logging.debug(message)
            return 0.0

    def get_number_saved_trajectories(self):
        return self._numberTrajectories

    def get_saved_trajectory(self, index):
        return self._trajectories[index]

    def get_saved_trajectories(self):
        return self._trajectories

    def get_maximum_energy_absorbed_keV(self):
        return self.DEnergy_Density_Max_Energy

    def get_energy_absorbed_keV(self):
        return self.deposited_energy

    def is_psfs(self):
        return self._isPsf

    def get_point_spread_function_matrix(self):
        return self._pointSpreadFunctionMatrix
