#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.scan_points.lines_pattern
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

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.casino3.scan_points.base_pattern import BasePattern
from casinotools.file_format.casino3.scan_points.rectangle_pattern import RectanglePattern

# Globals and constants variables.


class LinesPattern(BasePattern):
    def __init__(self):
        self._line_spacing_nm = 0
        self._line_width_nm = 0
        self._line_height_nm = 0
        self._beam_step_nm = 0
        self._number_lines = 0
        self._center_point_nm = (0, 0)

        super().__init__()

    def _init_data(self):
        self._line_spacing_nm = 10.0
        self._line_width_nm = 10.0
        self._line_height_nm = 100.0
        self._beam_step_nm = 5.0
        self._number_lines = 1
        self._center_point_nm = (0.0, 0.0)

    def set_line_spacing_nm(self, line_spacing_nm):
        self._line_spacing_nm = line_spacing_nm

    def set_line_width_nm(self, line_width_nm):
        self._line_width_nm = line_width_nm

    def set_line_height_nm(self, line_height_nm):
        self._line_height_nm = line_height_nm

    def set_beam_step_nm(self, beam_step_nm):
        self._beam_step_nm = beam_step_nm

    def set_number_lines(self, number_lines):
        if number_lines % 2 == 0:
            number_lines += 1
            logging.warning("Number of lines need to by odd, set to %i", number_lines)

        self._number_lines = number_lines

    def set_center_point_nm(self, center_point_nm):
        self._center_point_nm = center_point_nm

    @staticmethod
    def generate_filename(basename):
        filename = "{}.txt".format(basename)

        return filename

    def _generate_scan_points(self):
        rectangle = RectanglePattern()
        rectangle.set_width_nm(self._line_width_nm)
        rectangle.set_height_nm(self._line_height_nm)
        rectangle.set_beam_step_nm(self._beam_step_nm)
        rectangle.set_center_point_nm(self._center_point_nm)

        self.add_scan_points(rectangle.get_scan_points())

        number_lines_left = int((self._number_lines - 1) / 2)
        number_lines_right = int((self._number_lines - 1) / 2)

        for index in range(1, number_lines_right + 1, 1):
            x_nm, y_nm = self._center_point_nm
            x_nm += index * (self._line_spacing_nm + self._line_width_nm)
            center_point_nm = x_nm, y_nm
            rectangle.set_center_point_nm(center_point_nm)
            self.add_scan_points(rectangle.get_scan_points())

        for index in range(1, number_lines_left + 1, 1):
            x_nm, y_nm = self._center_point_nm
            x_nm -= index * (self._line_spacing_nm + self._line_width_nm)
            center_point_nm = x_nm, y_nm
            rectangle.set_center_point_nm(center_point_nm)
            self.add_scan_points(rectangle.get_scan_points())
