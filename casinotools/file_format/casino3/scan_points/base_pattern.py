#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.scan_points.base_pattern
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
import os.path

# Third party modules.
import numpy as np

# Local modules.

# Project modules.

# Globals and constants variables.


class BasePattern:
    def __init__(self):
        self._scan_points = []

        self._init_data()

    def _init_data(self):
        raise NotImplementedError

    def get_scan_points(self):
        self._generate_scan_points()
        return self._scan_points

    def set_scan_points(self, scan_points):
        self._scan_points = scan_points

    def add_scan_points(self, scan_points):
        self._scan_points.extend(scan_points)

    def add_scan_point(self, scan_point):
        self._scan_points.append(scan_point)

    def reset(self):
        self._scan_points = []

    def write(self, filepath, generate_scan_points=True, overwrite=True):
        if not os.path.isfile(filepath) or overwrite:
            lines = self._generate_lines(generate_scan_points)

            output_file = open(filepath, 'wb')
            output_file.writelines(lines)
            output_file.close()
            del output_file

    def _generate_lines(self, generate_scan_points=True):
        if generate_scan_points:
            self._generate_scan_points()

        if len(self._scan_points) == 0:
            logging.error("Empty scan points list.")
            return []

        self._unique_scan_points()

        lines = self._generate_lines_implementation()
        return lines

    def _generate_lines_implementation(self):
        raise NotImplementedError

    def _generate_scan_points(self):
        raise NotImplementedError

    def _unique_scan_points(self):
        unique_scan_points = set(self._scan_points)
        self._scan_points = sorted(unique_scan_points)

    @staticmethod
    def _get_range_nm(width, step, center_position):
        minimum = -width / 2.0 + center_position
        maximum = width / 2.0 + center_position

        scan_point_range = np.arange(minimum, maximum + step, step)

        return scan_point_range

    def get_number_points(self):
        self._generate_scan_points()
        return len(self._scan_points)
