#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.scan_points.line_x_pattern
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

# Globals and constants variables.


class LineXPattern(BasePattern):
    def __init__(self):
        self._range_nm = 0
        self._step_nm = 0
        self._center_point_nm = (0, 0)

        super().__init__()

    def _init_data(self):
        self._range_nm = 10.0
        self._step_nm = 5.0
        self._center_point_nm = (0.0, 0.0)

    def set_range_nm(self, range_nm):
        self._range_nm = range_nm

    def set_step_nm(self, step_nm):
        self._step_nm = step_nm

    def set_center_point_nm(self, center_point_nm):
        self._center_point_nm = center_point_nm

    @staticmethod
    def generate_filename(basename):
        filename = "{}.txt".format(basename)

        return filename

    def _generate_scan_points(self):
        y = self._center_point_nm[1]
        self._scan_points = []
        for x in self._get_range_x_nm():
            point = (x, y)
            self._scan_points.append(point)

    def _get_range_x_nm(self):
        step_nm = self._step_nm
        return self._get_range_nm(self._range_nm, step_nm, self._center_point_nm[0])
