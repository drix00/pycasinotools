#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.scan_points.image_xz_pattern
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
from casinotools.file_format.casino3.scan_points.base_pattern import BasePattern
from casinotools.file_format.casino3.scan_points.line_x_pattern import LineXPattern

# Globals and constants variables.


class ImageXZPattern(BasePattern):
    def __init__(self):
        self._step_x_nm = 0
        self._range_x_nm = 0
        self._step_z_nm = 0
        self._range_z_nm = 0
        self._center_point_nm = (0, 0)

        super().__init__()

    def _init_data(self):
        self.set_step_x_nm(5.0)
        self.set_range_x_nm(10.0)
        self.set_step_z_nm(100.0)
        self.set_range_z_nm(100.0)
        self.set_center_point_nm((0.0, 0.0))

    def set_step_x_nm(self, step_nm):
        self._step_x_nm = step_nm

    def set_range_x_nm(self, range_nm):
        self._range_x_nm = range_nm

    def set_step_z_nm(self, step_nm):
        self._step_z_nm = step_nm

    def set_range_z_nm(self, range_nm):
        self._range_z_nm = range_nm

    def set_center_point_nm(self, center_point_nm):
        self._center_point_nm = center_point_nm

    @staticmethod
    def generate_filename(basename):
        filename = "{}.txt".format(basename)

        return filename

    def _generate_scan_points(self):
        for z in self._get_range_z():
            line = LineXPattern()
            line.set_range_nm(self._range_x_nm)
            line.set_step_nm(self._step_x_nm)
            line_center_point = (self._center_point_nm[0], z)
            line.set_center_point_nm(line_center_point)

            self.add_scan_points(line.get_scan_points())

    def _get_range_z(self):
        step_nm = self._step_z_nm
        return self._get_range_nm(self._range_z_nm, step_nm, self._center_point_nm[1])
