#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.analyse.energy
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Helper to extract and use deposited energy from CASINO.

.. todo:: Add same helper for CASINO 2.
.. todo:: Implement log scale range and tests.
"""

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

# Standard library modules.
from enum import Enum
import os.path

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from casinotools.file_format.casino3.file import File
from casinotools.file_format.casino3.exported import energy as exported_energy

# Globals and constants variables.


class FileType(Enum):
    SIM = 1
    CAS = 2
    DAT = 3


FILE_TYPE_LABELS = {"sim": FileType.SIM, "cas":  FileType.CAS, "dat":  FileType.DAT}


class EnergyType(Enum):
    CARTESIAN = 0
    CYLINDRICAL = 1
    SPHERICAL = 2


def read_energy_data(file_path, scan_point_id=0):
    file_type = get_file_type(file_path)

    if file_type == FileType.CAS:
        energy = get_energy_type_cas(file_path, scan_point_id)
        return energy
    elif file_type == FileType.DAT:
        energy = get_energy_type_dat(file_path)
        return energy

    return Energy()


def get_file_type(file_path):
    extension = os.path.splitext(file_path)[-1]
    extension = extension[1:].lower()

    file_type = FILE_TYPE_LABELS[extension]
    return file_type


def get_energy_type_dat(file_path):
    energy_type_labels = {"Cartesian": EnergyCartesian(),
                          "Cylindric": EnergyCylindrical(),
                          "Spheric": EnergySpherical()}
    with open(file_path, "rt") as data_file:
        for line in data_file:  # pragma: no branch
            if line.startswith("Distribution Type"):
                items = line.split(':')
                energy_type_str = items[-1].strip()
                energy = energy_type_labels[energy_type_str]
                energy.from_dat(file_path)
                return energy


def get_energy_type_cas(file_path, scan_point_id):
    casino_file = File(file_path)
    options = casino_file.get_options()
    options_distributions = options.options_dist

    scan_point_results = casino_file.get_scan_point_results()[scan_point_id]
    if scan_point_results.is_deposited_energy:
        data = scan_point_results.deposited_energy.get_data()

        energy_type_values_cas = {0: EnergyCartesian(), 1: EnergyCylindrical(), 2: EnergySpherical()}
        energy = energy_type_values_cas[options_distributions.DEpos_Type]
        energy.from_cas(options_distributions, data)
        return energy
    else:
        return Energy()


class Energy:
    def __init__(self):
        self.energies_keV = None

    @property
    def total_energy_keV(self):
        total = np.sum(self.energies_keV)
        return total

    @property
    def number_elements(self):
        size = self.energies_keV.size
        return size


class EnergyCartesian(Energy):
    def __init__(self):
        super().__init__()

        self.xs_nm = None
        self.ys_nm = None
        self.zs_nm = None

    def from_cas(self, options_distributions, data):
        center_nm = options_distributions.DEpos_Center

        x_number_divisions = options_distributions.NbPointDEpos_X
        x_size_nm = options_distributions.DEpos_Size.x
        # x_is_log_scale = options_distributions.DEposCyl_Z_Log
        # .. todo:: Check if x log scale value is saved in the .cas file.

        x_min = center_nm.x - x_size_nm / 2.0
        x_max = center_nm.x + x_size_nm / 2.0
        x_step_size_nm = (x_max - x_min) / x_number_divisions
        self.xs_nm = np.linspace(x_min, x_max - x_step_size_nm, x_number_divisions)

        y_number_divisions = options_distributions.NbPointDEpos_Y
        y_size_nm = options_distributions.DEpos_Size.y
        # y_is_log_scale = options_distributions.DEposCyl_Z_Log
        # .. todo:: Check if x log scale value is saved in the .cas file.

        y_min = center_nm.y - y_size_nm / 2.0
        y_max = center_nm.y + y_size_nm / 2.0
        y_step_size_nm = (y_max - y_min) / y_number_divisions
        self.ys_nm = np.linspace(y_min, y_max - y_step_size_nm, y_number_divisions)

        z_number_divisions = options_distributions.NbPointDEpos_Z
        z_size_nm = options_distributions.DEpos_Size.z
        # self.z_is_log_scale = options_distributions.DEposCyl_Z_Log
        # .. todo:: Check if x log scale value is saved in the .cas file.

        z_min = center_nm.z - z_size_nm / 2.0
        z_max = center_nm.z + z_size_nm / 2.0
        z_step_size_nm = (z_max - z_min) / z_number_divisions
        self.zs_nm = np.linspace(z_min, z_max - z_step_size_nm, z_number_divisions)

        self.energies_keV = data

    def from_dat(self, file_path):
        energy_dat = exported_energy.EnergyCartesian()
        energy_dat.read(file_path)

        self.xs_nm = np.array(energy_dat.xs_nm)
        self.ys_nm = np.array(energy_dat.ys_nm)
        self.zs_nm = np.array(energy_dat.zs_nm)

        self.energies_keV = np.array(energy_dat.energies_keV)


class EnergyCylindrical(Energy):
    def __init__(self):
        super().__init__()

        self.zs_nm = None
        self.radiuses_nm = None

    def from_cas(self, options_distributions, data):
        center_nm = options_distributions.DEpos_Center

        z_number_divisions = options_distributions.DEposCyl_Z_Div
        z_size_nm = options_distributions.DEposCyl_Z
        # z_is_log_scale = options_distributions.DEposCyl_Z_Log

        z_min = center_nm.z - z_size_nm / 2.0
        z_max = center_nm.z + z_size_nm / 2.0
        z_step_size_nm = (z_max - z_min) / z_number_divisions
        self.zs_nm = np.linspace(z_min, z_max - z_step_size_nm, z_number_divisions)

        radius_number_divisions = options_distributions.DEposCyl_Rad_Div
        radius_size_nm = options_distributions.DEposCyl_Rad
        # radius_is_log_scale = options_distributions.DEposCyl_Rad_Log

        radius_min = 0.0
        radius_max = radius_size_nm
        radius_step_size_nm = (radius_max - radius_min) / radius_number_divisions
        self.radiuses_nm = np.linspace(radius_min, radius_max - radius_step_size_nm, radius_number_divisions)

        self.energies_keV = data

    def from_dat(self, file_path):
        energy_dat = exported_energy.EnergyCylindrical()
        energy_dat.read(file_path)

        self.radiuses_nm = np.array(energy_dat.radiuses_nm)
        self.zs_nm = np.array(energy_dat.zs_nm)

        self.energies_keV = np.array(energy_dat.energies_keV)


class EnergySpherical(Energy):
    def __init__(self):
        super().__init__()

        self.radiuses_nm = None

    def from_cas(self, options_distributions, data):
        # center_nm = options_distributions.DEpos_Center

        radius_number_divisions = options_distributions.DEposSpheric_Rad_Div
        radius_size_nm = options_distributions.DEposSpheric_Rad
        # radius_is_log_scale = options_distributions.DEposSpheric_Rad_Log

        radius_min = 0.0
        radius_max = radius_size_nm
        radius_step_size_nm = (radius_max - radius_min) / radius_number_divisions
        self.radiuses_nm = np.linspace(radius_min, radius_max - radius_step_size_nm, radius_number_divisions)

        self.energies_keV = data

    def from_dat(self, file_path):
        energy_dat = exported_energy.EnergySpherical()
        energy_dat.read(file_path)

        self.radiuses_nm = np.array(energy_dat.radiuses_nm)

        self.energies_keV = np.array(energy_dat.energies_keV)
