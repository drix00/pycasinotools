#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.point_spread_function_matrix
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

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.


class PointSpreadFunctionMatrix(FileReaderWriterTools):
    """
    Point spread function matrix data from CASINO simulation results file.

    :note: Need to implement the transformation from x, y, z to index of the _values array.

    """
    def __init__(self, options, point_nm):
        if options._options_advanced_psfs_settings.get_use_scan_point_for_center():
            self._center_point_nm = point_nm
        else:
            self._center_point_nm = options._options_advanced_psfs_settings.get_psf_center_nm()

        self._number_points_x = options._options_advanced_psfs_settings.get_number_steps_x()
        self._number_points_y = options._options_advanced_psfs_settings.get_number_steps_y()
        self._number_points_z = options._options_advanced_psfs_settings.get_number_steps_z()

        self._number_elements = 0
        self._values = None
        self._data = None

        self._file = None
        self._start_position = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        self._number_elements = self._number_points_x * self._number_points_y * self._number_points_z
        self._start_position = file.tell()
        # self._values = self.read_double_list(file, self._number_elements)
        skip_offset = self.get_size_of_double_list(self._number_elements)
        file.seek(skip_offset, os.SEEK_CUR)

        self._end_position = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._end_position)

    def _read_values(self):
        if self._file is None:
            self._file = open(self._file_pathname, 'rb')

        self._file.seek(self._start_position)
        self._values = self.read_double_list(self._file, self._number_elements)

    def get_data(self):
        if self._data is None:
            if self._values is None:
                self._read_values()
                index = 0
                self._data = {}
                for x in range(self._number_points_x):
                    for y in range(self._number_points_y):
                        for z in range(self._number_points_z):
                            self._data[(x, y, z)] = self._values[index]
                            index += 1
                del self._values
                self._values = None

        return self._data

    def get_number_points(self):
        return self._number_points_x * self._number_points_y * self._number_points_z

    def get_number_points_x(self):
        return self._number_points_x

    def get_number_points_y(self):
        return self._number_points_y

    def get_number_points_z(self):
        return self._number_points_z
