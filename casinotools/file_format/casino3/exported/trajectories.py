#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.exported.trajectories
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

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.
X_nm = "X (nm)"
Y_nm = "Y (nm)"
Z_nm = "z (nm)"

KEYWORD_TRAJECTORY = '"Trajectory"'
KEYWORD_NUMBER_COLLISIONS = '"NbCollisions"'
KEYWORD_SCAN_POINT_X = '"X"'
KEYWORD_SCAN_POINT_Y = '"Y"'


class ExportedTrajectories(object):
    def __init__(self, filepath):
        self._filepath = filepath

        self._trajectories = None

    def get_positions_at_z_nm(self, z_nm):
        if self._trajectories is None:
            self._read_data_file()

        positions = []
        for trajectory in self._trajectories:
            for collision in trajectory:
                if collision[Z_nm] == z_nm:
                    position = (collision[X_nm], collision[Y_nm], collision[Z_nm])
                    positions.append(position)

        return positions

    def get_scan_point_position_nm(self):
        if self._trajectories is None:
            self._read_data_file()

        return self._scanPointX, self._scanPointY

    def _read_data_file(self):
        lines = open(self._filepath, 'rb').readlines()

        trajectories = []
        number_collisions = None
        collisions = None
        for line in lines:
            if line.startswith(KEYWORD_TRAJECTORY):
                if number_collisions is not None:
                    trajectories.append(collisions)
            elif line.startswith(KEYWORD_SCAN_POINT_X):
                items = line.split()
                if len(items) == 2:
                    try:
                        self._scanPointX = float(items[1])
                    except ValueError:
                        pass
            elif line.startswith(KEYWORD_SCAN_POINT_Y):
                items = line.split()
                if len(items) == 2:
                    try:
                        self._scanPointY = float(items[1])
                    except ValueError:
                        pass
            elif line.startswith(KEYWORD_NUMBER_COLLISIONS):
                if number_collisions is not None:
                    assert len(collisions) == number_collisions
                    trajectories.append(collisions)

                items = line.split()
                number_collisions = int(items[1])
                collisions = []
            elif self._is_collision_data_line(line):
                collision = self._read_collision_data_line(line)
                collisions.append(collision)

        self._trajectories = trajectories

    @staticmethod
    def _is_collision_data_line(line):
        items = line.split()
        if len(items) == 10:
            try:
                float(items[0])
                return True
            except ValueError:
                return False

    @staticmethod
    def _read_collision_data_line(line):
        items = line.split()

        collision = {X_nm: float(items[0]), Y_nm: float(items[1]), Z_nm: float(items[2])}

        return collision
