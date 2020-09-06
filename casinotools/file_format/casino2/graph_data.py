#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.graph_data
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

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_double, read_long, read_int, read_str
from casinotools.file_format.casino2.version import VERSION_2040601
# Globals and constants variables.


class GraphData:
    def __init__(self, size=0, borne_inf=0.0, borne_sup=0.0, is_log=False, is_uneven=False, title="", x_title="",
                 y_title="", file=None, version=None):
        if version is not None:
            self._version = version
        else:
            self._version = 0

        if file is not None:
            self.read(file)
        else:
            self._size = size
            self._borneInf = borne_inf
            self._borneSup = borne_sup
            self._isLog = is_log
            self._isUneven = is_uneven
            self._title = title
            self._xTitle = x_title
            self._yTitle = y_title
            self._values = []
            self._positions = None

    def add(self, value):
        self._values.append(value)

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        if self._version >= VERSION_2040601:
            self._version = read_long(file)

            self._size = read_long(file)
            self._borneInf = read_double(file)
            self._borneSup = read_double(file)
            self._isLog = read_int(file)
            self._isUneven = read_int(file)

            self._title = read_str(file)
            self._xTitle = read_str(file)
            self._yTitle = read_str(file)

            self._values = []
            self._positions = []
            for dummy in range(self._size):
                value = read_double(file)
                self._values.append(value)

                if self._isUneven:
                    position = read_double(file)
                    self._positions.append(position)

            if not self._isUneven:
                for i in range(self._size):
                    position = self.index2pos(i)
                    self._positions.append(position)

            assert len(self._values) == len(self._positions)

    def index2pos(self, index):
        x_sup = self._borneSup
        x_inf = self._borneInf
        number_points = self._size
        is_log = self._isLog

        assert(x_sup >= x_inf)
        assert(number_points > 0)

        if number_points == 1:
            return x_inf

        if index <= 0:
            return x_inf

        if is_log:
            assert(x_sup > 0)
            assert(x_inf > 0)

            point = (float(index) / float(number_points - 1))
            exp = point * (math.log10(x_sup) - math.log10(x_inf)) + math.log10(x_inf)
            point = pow(10.0, exp)
            return point
        else:
            point = (float(index) / float(number_points - 1))
            point = point * (x_sup - x_inf) + x_inf
            return point

    def get_positions(self):
        if self._positions is None:
            self._positions = [self.index2pos(i) for i in range(self._size)]

        return self._positions

    def get_values(self):
        return self._values
