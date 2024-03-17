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
import os

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_int, get_size_of_double_list, get_size_of_int_list, \
    read_double_list, read_int_list

# Globals and constants variables.


# Third party modules.

# Local modules.

# Globals and constants variables.


class TransmittedAngles:
    def __init__(self):
        self._file = None
        self._start_position = 0
        self._start_position_collisions = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._angles = None
        self._binned_angles = None

        self._number_transmitted_electrons = 0
        self._number_transmitted_detected_electrons = 0
        self._number_angles = 0
        self._number_binned_angles = 0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        self._number_transmitted_electrons = read_int(file)
        self._number_transmitted_detected_electrons = read_int(file)

        self._number_angles = read_int(file)
        self._start_position = file.tell()
        skip_offset = get_size_of_double_list(self._number_angles)
        file.seek(skip_offset, os.SEEK_CUR)

        self._number_binned_angles = read_int(file)
        skip_offset = get_size_of_int_list(self._number_binned_angles)
        file.seek(skip_offset, os.SEEK_CUR)

        self._end_position = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._end_position)

    def _read_angle_values(self):
        self._file.seek(self._start_position)
        self._angles = read_double_list(self._file, self._number_angles)

        self._number_binned_angles = read_int(self._file)
        self._binned_angles = read_int_list(self._file, self._number_binned_angles)

    def get_angles(self):
        if self._angles is None:
            self._read_angle_values()

        return self._angles

    def get_binned_angles(self):
        if self._binned_angles is None:
            self._read_angle_values()

        return self._binned_angles

    def get_transmitted_detected_electrons(self, beta_min, beta_max):
        if self._number_angles > 0:
            return self.get_transmitted_detected_electrons_by_angles(beta_min, beta_max)
        elif self._number_binned_angles > 0:
            return self.get_transmitted_detected_electrons_by_binned_angles(beta_min, beta_max)

    def get_transmitted_detected_electrons_by_angles(self, beta_min_mrad, beta_max_mrad):
        if self._angles is None:
            self._read_angle_values()

        if beta_min_mrad is None:
            beta_min_rad = min(self._angles)
        else:
            beta_min_rad = beta_min_mrad * 1.0e-3

        if beta_max_mrad is None:
            beta_max_rad = max(self._angles)
        else:
            beta_max_rad = beta_max_mrad * 1.0e-3

        angles = np.array(self._angles)
        number_detected_electrons = np.ma.masked_outside(angles, beta_min_rad, beta_max_rad).count()

        return number_detected_electrons

    def get_transmitted_detected_electrons_by_binned_angles(self, beta_min, beta_max):
        if self._binned_angles is None:
            self._read_angle_values()

        start_angle_mrad = 0.0
        stop_angle_mrad = (np.pi / 2.0) * 1.0e3
        number_angles = self._number_binned_angles
        angles = np.linspace(start_angle_mrad, stop_angle_mrad, number_angles)
        assert len(angles) == len(self._binned_angles)

        index_min = 0
        index_max = 0
        for index, angle in enumerate(angles):
            if angle >= beta_min:
                index_min = index
                break

        for index, angle in enumerate(angles):
            if angle <= beta_max:
                index_max = index

        number_electrons = sum(self._binned_angles[index_min:index_max + 1])
        return number_electrons
