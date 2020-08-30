#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.graph_data
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
import math
import logging
import os

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.

# Third party modules.

# Local modules.

# Globals and constants variables.


def index2pos(x_sup, x_inf, number_points, position_index, is_log):
    assert(x_sup >= x_inf)
    assert(number_points > 0)

    if number_points == 1:
        return x_inf

    if position_index <= 0:
        return x_inf

    if is_log:
        assert(x_sup > 0)
        assert(x_inf > 0)

        point = (float(position_index) / float(number_points - 1))
        exp = point * (math.log10(x_sup) - math.log10(x_inf)) + math.log10(x_inf)
        point = pow(10.0, exp)
        return point
    else:
        point = (float(position_index) / float(number_points - 1))
        point = point * (x_sup - x_inf) + x_inf
        return point


class GraphData(FileReaderWriterTools):
    def __init__(self, file):
        self._file = None
        self._startPosition = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

        self._version = 0
        self._size = 0
        self._borneInf = 0.0
        self._borneSup = 0.0
        self._isLog = 0
        self._isUneven = 0

        self._title = ""
        self._xTitle = ""
        self._yTitle = ""

        self._values = None
        self._positions = None

        self.read(file)

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._version = self.read_int(file)
        self._size = self.read_long(file)
        self._borneInf = self.read_double(file)
        self._borneSup = self.read_double(file)
        self._isLog = self.read_int(file)
        self._isUneven = self.read_int(file)

        self._title = self.read_str(file)
        self._xTitle = self.read_str(file)
        self._yTitle = self.read_str(file)

        self._startPosition = file.tell()
        skip_offset = self.get_size_of_double_list(self._size)
        if self._isUneven:
            skip_offset *= 2

        file.seek(skip_offset, os.SEEK_CUR)

        self._endPosition = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)

    def get_values(self):
        if self._values is None:
            self._read_values()

        return self._values

    def _read_values(self):
        self._file.seek(self._startPosition)
        self._values = []
        self._positions = []
        for dummy in range(self._size):
            value = self.read_double(self._file)
            self._values.append(value)

            if self._isUneven:
                position = self.read_double(self._file)
                self._positions.append(position)

        if not self._isUneven:
            for i in range(self._size):
                position = index2pos(self._borneSup, self._borneInf, self._size, i, self._isLog)
                self._positions.append(position)

        assert len(self._values) == len(self._positions)
