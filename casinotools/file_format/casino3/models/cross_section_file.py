#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.models.cross_section_file
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
import math

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.
VERSION_30107002 = 30107002
VERSION_LAST = VERSION_30107002


def generate_raw_binary_files(filepath, atomic_number, energies_grid_eV, totals_nm2,
                              polar_angles_grid_deg, partials_list_nm2_sr):
    logging.info(filepath)

    file = open(filepath, 'wb')

    binary_writer = FileReaderWriterTools()

    for energy_eV, total_nm2 in zip(energies_grid_eV, totals_nm2):
        binary_writer.write_int(file, VERSION_LAST)
        binary_writer.write_double(file, atomic_number)
        energy_keV = energy_eV / 1000.0
        binary_writer.write_double(file, energy_keV)
        binary_writer.write_double(file, total_nm2)

        size = len(polar_angles_grid_deg)
        binary_writer.write_long(file, size)

        partials_nm2_sr = partials_list_nm2_sr[energy_eV]
        partial_sin_thetas_nm2_sr = []
        polar_angle_grid_rad = []
        for angle_deg, partial_nm2_sr in zip(polar_angles_grid_deg, partials_nm2_sr):
            angle_rad = math.radians(angle_deg)
            polar_angle_grid_rad.append(angle_rad)
            partial_sin_thetas_nm2_sr.append(partial_nm2_sr * math.sin(angle_rad) * 2.0 * math.pi)

        ratio_list = []
        computed_total_nm2 = np.trapz(partial_sin_thetas_nm2_sr, polar_angle_grid_rad)
        for index in range(1, len(partial_sin_thetas_nm2_sr) + 1):
            x = polar_angle_grid_rad[:index]
            y = partial_sin_thetas_nm2_sr[:index]
            ratio = np.trapz(y, x) / computed_total_nm2
            ratio_list.append(ratio)

        for ratio, angle_rad in zip(ratio_list, polar_angle_grid_rad):
            binary_writer.write_double(file, ratio)
            binary_writer.write_double(file, angle_rad)

    file.close()
