#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.exported.energy
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read exported data files related to energy deposition.
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
import numpy as np

# Local modules.

# Project modules.

# Globals and constants variables.


class EnergyCartesian:
    def __init__(self):
        self.maximum_density_keV = 0.0
        self.x_size_nm = 0.0
        self.x_number_divisions = 0
        self.y_size_nm = 0.0
        self.y_number_divisions = 0
        self.z_size_nm = 0.0
        self.z_number_divisions = 0
        self.range_x_nm = [0, 0]
        self.range_y_nm = [0, 0]
        self.range_z_nm = [0, 0]

        self.xs_nm = []
        self.ys_nm = []
        self.zs_nm = []
        self.energies_keV = []
        self.energies2_keV = []

    def read(self, file_path):
        with open(file_path) as data_file:
            for line in data_file:  # pragma: no branch
                if line.startswith("Maximum Energy Density"):
                    self.maximum_density_keV = extract_maximum_density(line)
                elif line.startswith("X :"):
                    self.x_size_nm, self.x_number_divisions = extract_size_divisions(line)
                elif line.startswith("Y :"):
                    self.y_size_nm, self.y_number_divisions = extract_size_divisions(line)
                elif line.startswith("Z :"):
                    self.z_size_nm, self.z_number_divisions = extract_size_divisions(line)
                elif line.startswith("X Range From:"):
                    self.range_x_nm = extract_range(line)
                elif line.startswith("Y Range From:"):
                    self.range_y_nm = extract_range(line)
                elif line.startswith("Z Range From:"):
                    self.range_z_nm = extract_range(line)
                    break

            self.xs_nm = np.linspace(self.range_x_nm[0], self.range_x_nm[1] - self.x_size_nm, self.x_number_divisions)
            self.ys_nm = np.linspace(self.range_y_nm[0], self.range_y_nm[1] - self.y_size_nm, self.y_number_divisions)
            self.zs_nm = np.linspace(self.range_z_nm[0], self.range_z_nm[1] - self.z_size_nm, self.z_number_divisions)

            shape = (self.x_number_divisions, self.y_number_divisions, self.z_number_divisions)
            self.energies_keV = np.zeros(shape, dtype=float)

            skip_next_line = False
            id_y = -1
            for line in data_file:  # pragma: no branch
                if skip_next_line:
                    skip_next_line = False
                    continue
                elif line.startswith("XY planes"):
                    break
                elif line.startswith("XZ plane "):
                    id_y += 1
                    id_z = -1
                    skip_next_line = True
                elif "nm" in line:
                    id_z += 1
                    x_nm, energies = extract_values_array(line)
                    self.energies_keV[:, id_y, id_z] = energies

            self.energies2_keV = np.zeros(shape, dtype=float)
            skip_next_line = False
            id_z = -1
            for line in data_file:
                if skip_next_line:
                    skip_next_line = False
                    continue
                elif line.startswith("XY plane "):
                    id_z += 1
                    id_y = -1
                    skip_next_line = True
                elif "nm" in line:  # pragma: no branch
                    id_y += 1
                    x_nm, energies = extract_values_array(line)
                    self.energies2_keV[:, id_y, id_z] = energies

    def __eq__(self, other):
        return (self.maximum_density_keV == other.maximum_density_keV) and \
               (self.x_size_nm == other.x_size_nm) and \
               (self.x_number_divisions == other.x_number_divisions) and \
               (self.y_size_nm == other.y_size_nm) and \
               (self.y_number_divisions == other.y_number_divisions) and \
               (self.z_size_nm == other.z_size_nm) and \
               (self.z_number_divisions == other.z_number_divisions) and \
               (self.range_x_nm == other.range_x_nm) and \
               (self.range_y_nm == other.range_y_nm) and \
               (self.range_z_nm == other.range_z_nm) and \
               (self.xs_nm == other.xs_nm) and \
               (self.ys_nm == other.ys_nm) and \
               (self.zs_nm == other.zs_nm) and \
               np.all(self.energies_keV == other.energies_keV)

    @property
    def total_energy_keV(self):
        total = np.sum(self.energies_keV)
        return total


class EnergyCylindrical:
    def __init__(self):
        self.maximum_density_keV = 0.0
        self.radius_size_nm = 0.0
        self.radius_number_divisions = 0
        self.z_size_nm = 0.0
        self.z_number_divisions = 0
        self.center_nm = [0, 0]
        self.range_z_nm = [0, 0]

        self.radiuses_nm = []
        self.zs_nm = []
        self.energies_keV = []

    def read(self, file_path):
        with open(file_path) as data_file:
            for line in data_file:
                if line.startswith("Maximum Energy Density"):
                    self.maximum_density_keV = extract_maximum_density(line)
                elif line.startswith("Radius :"):
                    self.radius_size_nm, self.radius_number_divisions = extract_size_divisions(line)
                elif line.startswith("Z :"):
                    self.z_size_nm, self.z_number_divisions = extract_size_divisions(line)
                elif line.startswith("Radius Center :"):
                    self.center_nm = extract_center(line)
                elif line.startswith("Z Range From:"):
                    self.range_z_nm = extract_range(line)
                elif line.startswith(r"Z\Radius"):
                    self.radiuses_nm = extract_values(line)
                elif "nm" in line:
                    z_nm, energies = extract_values_array(line)
                    self.zs_nm.append(z_nm)
                    self.energies_keV.append(energies)

        self.energies_keV = np.array(self.energies_keV)

    def __eq__(self, other):
        return (self.maximum_density_keV == other.maximum_density_keV) and \
               (self.radius_size_nm == other.radius_size_nm) and \
               (self.radius_number_divisions == other.radius_number_divisions) and \
               (self.z_size_nm == other.z_size_nm) and \
               (self.z_number_divisions == other.z_number_divisions) and \
               (self.center_nm == other.center_nm) and \
               (self.range_z_nm == other.range_z_nm) and \
               (self.radiuses_nm == other.radiuses_nm) and \
               (self.zs_nm == other.zs_nm) and \
               np.all(self.energies_keV == other.energies_keV)

    @property
    def total_energy_keV(self):
        total = np.sum(self.energies_keV)
        return total


class EnergySpherical:
    def __init__(self):
        self.maximum_density_keV = 0.0
        self.radius_size_nm = 0.0
        self.radius_number_divisions = 0
        self.center_nm = [0, 0, 0]

        self.radiuses_nm = []
        self.energies_keV = []

    def read(self, file_path):
        with open(file_path) as data_file:
            for line in data_file:
                if line.startswith("Maximum Energy Density"):
                    self.maximum_density_keV = extract_maximum_density(line)
                elif line.startswith("Radius :"):
                    self.radius_size_nm, self.radius_number_divisions = extract_size_divisions(line)
                elif line.startswith("Radius Center :"):
                    self.center_nm = extract_center(line)
                elif "nm" in line:
                    radius, energy = extract_two_values(line)
                    self.radiuses_nm.append(radius)
                    self.energies_keV.append(energy)

        self.energies_keV = np.array(self.energies_keV)

    def __eq__(self, other):
        return (self.maximum_density_keV == other.maximum_density_keV) and \
               (self.radius_size_nm == other.radius_size_nm) and \
               (self.radius_number_divisions == other.radius_number_divisions) and \
               (self.center_nm == other.center_nm) and \
               (self.radiuses_nm == other.radiuses_nm) and \
               np.all(self.energies_keV == other.energies_keV)

    @property
    def total_energy_keV(self):
        total = np.sum(self.energies_keV)
        return total


def extract_maximum_density(line):
    items = line.split(':')
    maximum_density = float(items[-1])
    return maximum_density


def extract_size_divisions(line):
    items = line.split(':')
    radius_size_str = items[-1].split("nm for")[0]
    size_nm = float(radius_size_str)
    number_divisions_str = items[-1].split("nm for")[1].split("divisions")[0]
    number_divisions = int(number_divisions_str)

    return size_nm, number_divisions


def extract_range(line):
    items = line.split(':')
    range_nm = [float(items[1][:-2]), float(items[2][:-3])]
    return range_nm


def extract_center(line):
    items = line.split(':')[-1].split(' ')
    center_nm = []
    for item in items[1:]:
        value = float(item.split('=')[-1])
        center_nm.append(value)

    return center_nm


def extract_values(line):
    values = []

    items = line.split()
    for item in items[1:]:
        radius = float(item[:-2])
        values.append(radius)

    return values


def extract_two_values(line):
    items = line.split()
    radius = float(items[0][:-2])
    energy = float(items[-1])

    return radius, energy


def extract_values_array(line):
    items = line.split()
    z_nm = float(items[0][:-2])
    energies = []
    for item in items[1:]:
        energy = float(item)
        energies.append(energy)

    return z_nm, energies
