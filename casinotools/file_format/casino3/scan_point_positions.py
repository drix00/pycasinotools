#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.scan_point_positions
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
import os
import logging

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_int, read_double
from casinotools.file_format.tags import find_tag


# Globals and constants variables.

# Third party modules.

# Local modules.

# Globals and constants variables.


class ScanPointPositions:
    def __init__(self):
        self._positions = []

        self._start_position = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self.reset()

    def reset(self):
        self._positions = []

        self._start_position = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

    def get_number_points(self):
        return len(self._positions)

    def add_position(self, point):
        self._positions.append(point)

    def get_positions(self):
        return self._positions

    def read(self, file):
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        # Move backward to read the previous tag, which indicate indirectly the start of this section.
        current_position = file.tell()
        if current_position > 16:
            file.seek(-16, os.SEEK_CUR)

        tag_id = b"*SIM_OPT_END%"
        if find_tag(file, tag_id):
            self.reset()

            self._start_position = file.tell()
            self._file_pathname = file.name
            self._file_descriptor = file.fileno()
            logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read",
                          self._start_position)
            number_points = read_int(file)

            for dummy in range(number_points):
                x = read_double(file)
                y = read_double(file)
                z = read_double(file)

                points = (x, y, z)

                self.add_position(points)

        self._end_position = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._end_position)

        return None

    def export(self, export_file):
        # todo: implement the export method.
        pass
