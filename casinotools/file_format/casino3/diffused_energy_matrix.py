#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.diffused_energy_matrix
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
from casinotools.file_format.casino3.energy_matrix import EnergyMatrix
from casinotools.file_format.file_reader_writer_tools import read_int, get_size_of_double_list
from casinotools.file_format.tags import find_tag

# Globals and constants variables.
DIFFUSED_TAG = b"Diffused%Energy"
DIFFUSED_END_TAG = b"Diffused%%End%%"
DIFFUSE_VERSION = 30107000


class DiffusedEnergyMatrix(EnergyMatrix):
    """
    Energy matrix date from casino simulation results file.

    :note: Need to implement the transformation from x, y, z to index of the _values array.

    """
    def __init__(self, options, point):
        super().__init__(options, point)

        self.version = 0
        self._number_elements = 0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        tag_id = DIFFUSED_TAG
        if find_tag(file, tag_id):
            self.version = read_int(file)

            self._number_elements = self._number_points_x * self._number_points_y * self._number_points_z
            self._start_position = file.tell()
            # self._values = read_double_list(file, self._number_elements)
            skip_offset = get_size_of_double_list(self._number_elements)
            file.seek(skip_offset, os.SEEK_CUR)

            logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", file.tell())
            tag_id = DIFFUSED_END_TAG
            if not find_tag(file, tag_id):
                raise IOError

        self._end_position = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._end_position)
