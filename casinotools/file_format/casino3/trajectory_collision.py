#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.trajectory_collision
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Structure for the trajectory collision data.
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
import struct
import math

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.
COLLISION_TYPE_ATOM = 0
COLLISION_TYPE_REGION = 1
COLLISION_TYPE_NODE = 2
COLLISION_TYPE_RECALC = 3

COLLISION_TYPE_LABELS = {COLLISION_TYPE_ATOM: "Atom",
                         COLLISION_TYPE_REGION: "Region",
                         COLLISION_TYPE_NODE: "Node",
                         COLLISION_TYPE_RECALC: "Recalc"}


def get_size_scattering_event():
    size = struct.calcsize("5d2i")
    return size


class TrajectoryCollision(FileReaderWriterTools):
    def __init__(self, items=None):
        if items is not None:
            self._position_x = items[0]
            self._position_y = items[1]
            self._position_z = items[2]
            self._energy = items[3]
            self._segment_length = items[4]
            self._collision_type = items[5]
            self._region_id = items[6]

    def read(self, file):
        self._read_optimized(file)

    def _read_original(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self._position_x = self.read_double(file)
        self._position_y = self.read_double(file)
        self._position_z = self.read_double(file)
        self._energy = self.read_double(file)
        self._segment_length = self.read_double(file)
        self._collision_type = self.read_int(file)

        self._region_id = self.read_int(file)

    def _read_optimized(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        values_format = "5d2i"
        items = self.read_multiple_values(file, values_format)

        self.set_values(items)

    def set_values(self, items):
        self._position_x = items[0]
        self._position_y = items[1]
        self._position_z = items[2]
        self._energy = items[3]
        self._segment_length = items[4]
        self._collision_type = items[5]
        self._region_id = items[6]

    def get_collision_type(self):
        return self._collision_type

    def get_collision_type_name(self):
        return COLLISION_TYPE_LABELS[self._collision_type]

    def get_x_nm(self):
        return self._position_x

    def get_y_nm(self):
        return self._position_y

    def get_z_nm(self):
        return self._position_z

    def get_position_nm(self):
        position_nm = (self._position_x, self._position_y, self._position_z)

        return position_nm

    def get_radius_xy_nm(self):
        return math.sqrt(self._position_x ** 2 + self._position_y ** 2)

    def get_energy_keV(self):
        return self._energy

    def get_region_id(self):
        return self._region_id
