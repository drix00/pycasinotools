#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
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
import os

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from casinotools.file_format.casino3.scan_points.base_pattern import BasePattern

# Globals and constants variables.

# Third party modules.

# Local modules.

# Globals and constants variables.


class ScanPointsFile(BasePattern):
    def __init__(self):
        self._number_points = 0
        self._width_max_nm = 0
        self._number_points_y = 0
        self._height_max_nm = 0
        self._number_points_z = 0
        self._beam_step_nm = 0
        self._center_point_nm = (0, 0)
        self._pixel_size_nm = 0

        super().__init__()

    def _init_data(self):
        self.set_number_points(0)
        self.set_width_nm(0)
        self.set_height_nm(0)
        self.set_center_point((0.0, 0.0))
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

    def set_center_point(self, point):
        assert len(point) == 2
        self._center_point_nm = point

    def _generate_scan_points(self):
        if self._height_max_nm == 0.0:
            self._generate_line_scan_x()
        elif self._width_max_nm == 0.0:
            self._generate_line_scan_y()
        else:
            self._generate_area_scan_xy()

    def _generate_line_scan_x(self):
        self._compute_separation_x_nm()

        y = self._center_point_nm[1]
        self._scan_points = []
        for x in self._get_range_x_nm():
            point = (x, y)
            self._scan_points.append(point)

    def _generate_line_scan_y(self):
        self._compute_separation_y_nm()

        x = self._center_point_nm[0]
        self._scan_points = []
        for y in self._get_range_y_nm():
            point = (x, y)
            self._scan_points.append(point)

    def _get_range_x_nm(self):
        x_sep = self._separation_nm
        x_min = -self._width_max_nm / 2.0 + x_sep / 2.0 + self._center_point_nm[0]
        x_max = self._width_max_nm / 2.0 + x_sep / 2.0 + self._center_point_nm[0]

        range_nm = np.arange(x_min, x_max, x_sep)

        return range_nm

    def _get_range_y_nm(self):
        y_sep = self._separation_nm
        y_min = -self._height_max_nm / 2.0 + y_sep / 2.0 + self._center_point_nm[1]
        y_max = self._height_max_nm / 2.0 + y_sep / 2.0 + self._center_point_nm[1]

        range_nm = np.arange(y_min, y_max, y_sep)

        return range_nm

    def _get_range_x2_nm(self):
        x_sep = self._width_max_nm / self._number_points_y
        x_min = -self._width_max_nm / 2.0 + x_sep / 2.0 + self._center_point_nm[0]
        x_max = self._width_max_nm / 2.0 + x_sep / 2.0 + self._center_point_nm[0]

        range_nm = np.arange(x_min, x_max, x_sep)

        return range_nm

    def _get_range_y2_nm(self):
        y_sep = self._height_max_nm / self._number_points_z
        y_min = -self._height_max_nm / 2.0 + y_sep / 2.0 + self._center_point_nm[1]
        y_max = self._height_max_nm / 2.0 + y_sep / 2.0 + self._center_point_nm[1]

        range_nm = np.arange(y_min, y_max, y_sep)

        return range_nm

    def _generate_area_scan_xy(self):
        if self._number_points != 0:
            self._compute_separation_nm()

            self._scan_points = []
            for x in self._get_range_x_nm():
                for y in self._get_range_y_nm():
                    point = (x, y)
                    self._scan_points.append(point)
        elif self._number_points_y is not None and self._number_points_z is not None:
            self._scan_points = []
            for x in self._get_range_x2_nm():
                for y in self._get_range_y2_nm():
                    point = (x, y)
                    self._scan_points.append(point)
        else:
            raise NotImplementedError

    def _compute_separation_x_nm(self):
        if self._number_points == 0 and self._pixel_size_nm is not None:
            self._separation_nm = self._pixel_size_nm
        elif self._number_points != 0:
            self._separation_nm = self._width_max_nm / self._number_points

    def _compute_separation_y_nm(self):
        if self._number_points == 0 and self._pixel_size_nm is not None:
            self._separation_nm = self._pixel_size_nm
        elif self._number_points != 0:
            self._separation_nm = self._height_max_nm / self._number_points

    def _compute_separation_nm(self):
        total_area_nm2 = self._width_max_nm * self._height_max_nm
        point_area_nm2 = total_area_nm2 / self._number_points

        self._separation_nm = math.sqrt(point_area_nm2)

    @staticmethod
    def _is_line_valid(line):
        if len(line) == 0:
            return False

        if (line[-1] != os.linesep) and (line[-1] != "\n") and (line[-1] != "\r") and (line[-1] != "\r\n"):
            return False

        try:
            items = line.split(',')
            _dummy_number1 = float(items[0].strip())
            _dummy_number2 = float(items[1].strip())
        except ValueError:
            return False

        if len(line) > 30:
            return False

        return True

    def _generate_lines_implementation(self):
        """
        Only two coordinates is used, for import in the CASINO GUI.
        """
        lines = []
        for point_nm in self._scan_points:
            line = "%f, %f\n" % point_nm
            lines.append(line)

        return lines


class ScanPointsFileScript(ScanPointsFile):
    def __init__(self):
        super().__init__()

    def _init_data(self):
        self.set_number_points(0)
        self.set_width_nm(0)
        self.set_height_nm(0)
        self.set_center_point((0.0, 0.0, 0.0))
        self._numberPointsY = None
        self._numberPointsZ = None

        self._pixel_size_nm = None
        self._separation_nm = None

    def set_center_point(self, point):
        assert len(point) == 3
        self._center_point_nm = point

    def set_pixel_size_nm(self, pixel_size_nm):
        self._pixel_size_nm = pixel_size_nm

    def set_line_scan_x(self):
        if self._number_points == 0 and self._width_max_nm is not None:
            number_points = self._width_max_nm / self._pixel_size_nm
            self.set_number_points(number_points)
        else:
            width_nm = self._pixel_size_nm * self._number_points
            self.set_width_nm(width_nm)
            self.set_height_nm(0)

    def set_line_scan_y(self):
        height_nm = self._pixel_size_nm * self._number_points
        self.set_width_nm(0)
        self.set_height_nm(height_nm)

    def set_line_scan_xy(self):
        number_points_per_direction = int(math.sqrt(self._number_points))

        height_nm = self._pixel_size_nm * number_points_per_direction
        width_nm = self._pixel_size_nm * number_points_per_direction
        self.set_width_nm(width_nm)
        self.set_height_nm(height_nm)

    def _generate_line_scan_x(self):
        self._compute_separation_x_nm()

        y = self._center_point_nm[1]
        z = self._center_point_nm[2]
        self._scan_points = []
        for x in self._get_range_x_nm():
            point = (x, y, z)
            self._scan_points.append(point)

    def _generate_line_scan_y(self):
        self._compute_separation_y_nm()

        x = self._center_point_nm[0]
        z = self._center_point_nm[2]
        self._scan_points = []
        for y in self._get_range_y_nm():
            point = (x, y, z)
            self._scan_points.append(point)

    def _generate_area_scan_xy(self):
        z = self._center_point_nm[2]
        if self._number_points != 0:
            self._compute_separation_nm()

            self._scan_points = []
            for x in self._get_range_x_nm():
                for y in self._get_range_y_nm():
                    point = (x, y, z)
                    self._scan_points.append(point)
        elif self._numberPointsY is not None and self._numberPointsZ is not None:
            self._scan_points = []
            for x in self._get_range_x2_nm():
                for y in self._get_range_y2_nm():
                    point = (x, y, z)
                    self._scan_points.append(point)
        else:
            raise NotImplementedError

    def _generate_lines_implementation(self):
        """
        With three coordinates is used, for import in the CASINO script console.
        """
        lines = []
        for point_nm in self._scan_points:
            line = "%f %f %f\n" % point_nm
            lines.append(line)

        return lines
