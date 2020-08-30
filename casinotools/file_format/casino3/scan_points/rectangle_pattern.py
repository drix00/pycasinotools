#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.scan_points.rectangle_pattern
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
import numpy as np

# Local modules.

# Project modules.
from casinotools.file_format.casino3.scan_points.base_pattern import BasePattern

# Globals and constants variables.

# Local modules.

# Globals and constants variables.


class RectanglePattern(BasePattern):
    def __init__(self):
        self._number_points = 0
        self._width_max_nm = 0
        self._number_points_y = 0
        self._height_max_nm = 0
        self._number_points_z = 0
        self._beam_step_nm = 0
        self._center_point_nm = (0, 0)

        super().__init__()

    def _init_data(self):
        self.set_number_points(0)
        self.set_width_nm(0)
        self.set_height_nm(0)
        self.set_center_point_nm((0.0, 0.0))
        self._number_points_y = None
        self._number_points_z = None

        self._separation_nm = None

    def set_number_points(self, value):
        self._number_points = int(value)

    def set_width_nm(self, value, number_points=None):
        self._width_max_nm = float(value)
        self._number_points_y = number_points

    def set_height_nm(self, value, number_points=None):
        self._height_max_nm = float(value)
        self._number_points_z = number_points

    def set_beam_step_nm(self, beam_step_nm):
        self._beam_step_nm = beam_step_nm

    def set_center_point_nm(self, point_nm):
        assert len(point_nm) == 2
        self._center_point_nm = point_nm

    def _generate_scan_points(self):
        self.reset()
        for x in self._get_range_x_nm():
            for y in self._get_range_y_nm():
                scan_point = (x, y)
                self.add_scan_point(scan_point)

    def _get_range_x_nm(self):
        x_sep = self._beam_step_nm
        x_min = -self._width_max_nm / 2.0 + x_sep / 2.0 + self._center_point_nm[0]
        x_max = self._width_max_nm / 2.0 + x_sep / 2.0 + self._center_point_nm[0]

        range_nm = np.arange(x_min, x_max, x_sep)

        return range_nm

    def _get_range_y_nm(self):
        y_sep = self._beam_step_nm
        y_min = -self._height_max_nm / 2.0 + y_sep / 2.0 + self._center_point_nm[1]
        y_max = self._height_max_nm / 2.0 + y_sep / 2.0 + self._center_point_nm[1]

        range_nm = np.arange(y_min, y_max, y_sep)

        return range_nm
